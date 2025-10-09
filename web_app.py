from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os
from pathlib import Path
import threading
from datetime import datetime
import json

# Import the core subtitle generator from app.py
from app import OfflineSubtitleGenerator, SubtitleStyle, LanguageCode

app = Flask(__name__)
app.secret_key = 'simple_subtitle_generator_key_2024'

UPLOAD_FOLDER = Path('uploads')
OUTPUT_FOLDER = Path('output')
UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Global instance of the generator for persistent model loading
subtitle_generator = None

def get_subtitle_generator():
    global subtitle_generator
    if subtitle_generator is None:
        subtitle_generator = OfflineSubtitleGenerator(
            whisper_model="base", 
            use_gpu=False, 
            enhance_audio=True, 
            style=SubtitleStyle.GRUNGE_BRUSH
        )
        print("[INFO] OfflineSubtitleGenerator başlatıldı (Grunge stil).")
    return subtitle_generator

@app.route('/')
def index():
    print("[INFO] / rotasına erişildi.")
    files = get_output_files()
    print(f"[INFO] Çıktı klasöründeki dosyalar: {files}")
    return render_template('index.html', files=files)

def get_output_files():
    # List files recursively from OUTPUT_FOLDER and return paths relative to it
    files = sorted([str(f.relative_to(OUTPUT_FOLDER)) for f in OUTPUT_FOLDER.rglob('*') if f.is_file()])
    print(f"[INFO] get_output_files çağrıldı, bulunan dosyalar: {files}")
    return files

@app.route('/download/<path:filename>')
def download_output(filename):
    print(f"[INFO] /download/{filename} rotasına erişildi.")
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    print("[INFO] /upload rotasına POST isteği geldi.")
    if 'file' not in request.files:
        print("[ERROR] /upload: Dosya yüklenemedi: Dosya bulunamadı.")
        flash('Dosya yüklenemedi: Dosya bulunamadı', 'error')
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        print("[ERROR] /upload: Dosya adı boş.")
        flash('Dosya yüklenemedi: Dosya adı boş', 'error')
        return redirect(url_for('index'))

    if file:
        filename = file.filename
        filepath = app.config['UPLOAD_FOLDER'] / filename
        print(f"[INFO] /upload: Yüklenen dosya adı: {filename}, geçici yol: {filepath}")
        
        try:
            file.save(filepath)
            print(f"[INFO] /upload: Dosya başarıyla kaydedildi: {filepath}")
        except Exception as e:
            print(f"[ERROR] /upload: Dosya kaydedilirken hata oluştu: {str(e)}")
            flash(f"Dosya kaydedilirken hata oluştu: {str(e)}", "error")
            return redirect(url_for('index'))

        # Get form parameters
        output_formats_str = request.form.get('formats', 'srt,video')
        output_formats = [fmt.strip() for fmt in output_formats_str.split(',')]
        language = request.form.get('language', 'auto')
        whisper_model = request.form.get('model', 'base')
        use_gpu = 'gpu' in request.form
        no_audio_enhance = 'no_enhance_audio' in request.form
        include_timestamps = 'include_timestamps' in request.form

        print(f"[INFO] /upload: Form verileri - formats: {output_formats}, language: {language}, model: {whisper_model}, use_gpu: {use_gpu}, no_audio_enhance: {no_audio_enhance}, include_timestamps: {include_timestamps}")

        try:
            generator = get_subtitle_generator()
            generator.model_name = whisper_model
            generator.use_gpu = False  # Force GPU usage to False for stability
            generator.enhance_audio = not no_audio_enhance
            print("[INFO] /upload: SubtitleGenerator ayarları güncellendi.")

            task_id = f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            session_output_dir = app.config['OUTPUT_FOLDER'] / task_id
            session_output_dir.mkdir(exist_ok=True)
            print(f"[INFO] /upload: Oturum çıktı dizini oluşturuldu: {session_output_dir}")

            # Run processing in a separate thread to avoid blocking Flask
            def run_processing():
                try:
                    print(f"[INFO] /upload: Altyazı işleme başlatılıyor: {filepath}")
                    results = generator.process_one(
                        src=filepath,
                        out_dir=session_output_dir,
                        formats=output_formats,
                        language=language,
                        include_ts=include_timestamps
                    )
                    print(f"[INFO] /upload: Altyazı işleme tamamlandı. Sonuçlar: {results}")
                    
                    # Store success result in a file for the main thread to read
                    result_file = session_output_dir / "processing_result.json"
                    with open(result_file, 'w') as f:
                        json.dump({"success": True, "results": results}, f)
                        
                except Exception as e:
                    print(f"[ERROR] /upload: Video işlenirken hata oluştu: {str(e)}")
                    # Store error result in a file for the main thread to read
                    result_file = session_output_dir / "processing_result.json"
                    with open(result_file, 'w') as f:
                        json.dump({"success": False, "error": str(e)}, f)
                finally:
                    if filepath.exists():
                        filepath.unlink()
                        print(f"[INFO] /upload: Geçici dosya silindi: {filepath}")
                    print(f"[INFO] Görev {task_id} tamamlandı.")

            processing_thread = threading.Thread(target=run_processing)
            processing_thread.start()
            print(f"[INFO] /upload: İşleme arka plan iş parçacığında başlatıldı. Task ID: {task_id}")

            flash('Video işleniyor... Lütfen bekleyiniz. İşlem tamamlandığında sonuçlar görünecektir.', 'info')
            return redirect(url_for('index'))

        except Exception as e:
            print(f"[ERROR] /upload: Sistem hatası: {str(e)}")
            flash(f'Sistem hatası: {str(e)}', 'error')
            if filepath.exists():
                filepath.unlink()
                print(f"[INFO] /upload: Hata durumunda geçici dosya silindi: {filepath}")
            return redirect(url_for('index'))

@app.route('/clear', methods=['GET'])
def clear_files():
    print("[INFO] /clear rotasına GET isteği geldi.")
    try:
        for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER']]:
            print(f"[INFO] Temizleniyor: {folder}")
            for item in folder.iterdir():
                if item.is_file():
                    item.unlink()
                    print(f"[INFO] Dosya silindi: {item}")
                elif item.is_dir():
                    for sub_item in list(item.rglob('*'))[::-1]:  # Delete in reverse order
                        if sub_item.is_file():
                            sub_item.unlink()
                            print(f"[INFO] Alt dosya silindi: {sub_item}")
                        elif sub_item.is_dir():
                            sub_item.rmdir()
                            print(f"[INFO] Alt dizin silindi: {sub_item}")
                    item.rmdir()
                    print(f"[INFO] Dizin silindi: {item}")
        
        flash('Tüm yüklenen ve çıktı dosyaları temizlendi!', 'success')
        print("[INFO] Tüm dosyalar başarıyla temizlendi.")
    except Exception as e:
        print(f"[ERROR] Dosyalar temizlenirken hata oluştu: {str(e)}")
        flash(f'Dosyalar temizlenirken hata oluştu: {str(e)}', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    print("[INFO] Flask uygulaması başlatılıyor...")
    app.run(debug=True, host="0.0.0.0", port=5113)
    print("[INFO] Flask uygulaması kapatıldı.")