from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
import os
from pathlib import Path
import asyncio
import threading
from datetime import datetime
import subprocess

# Import the core subtitle generator from server.py
from server import OfflineSubtitleGenerator, SubtitleStyle, LanguageCode, MultilingualTTSProcessor, TTSEngine
from multilingual_processor import SupportedLanguage
# from ffmpeg_error import FFmpegError # FFmpegError is not defined in server.py

app = Flask(__name__)
app.secret_key = 'your_secret_key' # Change this to a strong, random key in production

UPLOAD_FOLDER = Path('uploads')
OUTPUT_FOLDER = Path('output')
UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Global instance of the generator for persistent model loading
# This will ensure the model is loaded once and reused across requests
subtitle_generator = None
tts_processor = None

def get_subtitle_generator():
    global subtitle_generator
    if subtitle_generator is None:
        # Ensure to set appropriate model, use_gpu, enhance_audio defaults
        # These can be overridden by form submissions
        subtitle_generator = OfflineSubtitleGenerator(whisper_model="base", use_gpu=False, enhance_audio=True)
        print("[INFO] OfflineSubtitleGenerator başlatıldı.")
    return subtitle_generator

def get_tts_processor():
    global tts_processor
    if tts_processor is None:
        tts_processor = MultilingualTTSProcessor()
        print("[INFO] MultilingualTTSProcessor başlatıldı.")
    return tts_processor

# Helper to get language names
def get_language_names_map():
    return {
        "tr": "Türkçe",
        "en": "İngilizce",
        "fr": "Fransızca",
        "de": "Almanca",
        "es": "İspanyolca",
        "it": "İtalyanca",
        "pt": "Portekizce",
        "ru": "Rusça",
        "ja": "Japonca",
        "ko": "Korece",
        "zh": "Çince",
        "ar": "Arapça",
    }

@app.route('/')
def index():
    print("[INFO] / rotasına erişildi.")
    supported_languages = get_language_names_map()
    files = get_output_files()
    print(f"[INFO] Çıktı klasöründeki dosyalar: {files}")
    return render_template('index.html', supported_languages=supported_languages, files=files)

def get_output_files():
    # List files recursively from OUTPUT_FOLDER and return paths relative to it
    files = sorted([str(f.relative_to(OUTPUT_FOLDER)) for f in OUTPUT_FOLDER.rglob('*') if f.is_file()])
    print(f"[INFO] get_output_files çağrıldı, bulunan dosyalar: {files}")
    return files

@app.route('/list_outputs')
def list_outputs():
    print("[INFO] /list_outputs rotasına erişildi.")
    files = get_output_files()
    return render_template('files.html', files=files)

@app.route('/download/<path:filename>')
def download_output(filename):
    print(f"[INFO] /download/{filename} rotasına erişildi.")
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)

@app.route('/upload', methods=['POST'])
async def upload_file():
    print("[INFO] /upload rotasına POST isteği geldi.")
    if 'file' not in request.files:
        print("[ERROR] /upload: Dosya yüklenemedi: Dosya bulunamadı.")
        flash('Dosya yüklenemedi: Dosya bulunamadı', 'error')
        return redirect(url_for('index', _external=True))

    file = request.files['file']
    if file.filename == '':
        print("[ERROR] /upload: Dosya adı boş.")
        flash('Dosya yüklenemedi: Dosya adı boş', 'error')
        return redirect(url_for('index', _external=True))

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
            return redirect(url_for('index', _external=True))

        output_formats = request.form.getlist('formats') # Changed to 'formats'
        subtitle_style = request.form.get('style', 'default') # Changed to 'style'
        language = request.form.get('language', 'auto')
        whisper_model = request.form.get('model', 'base') # Changed to 'model'
        use_gpu = 'gpu' in request.form
        no_audio_enhance = 'no_enhance_audio' in request.form # Changed to 'no_enhance_audio'
        tts_languages_str = request.form.get('tts_languages', '')
        tts_engine_str = request.form.get('tts_engine', 'edge_tts')
        no_embed_subtitles = 'no_embed_subtitles' in request.form
        original_audio_mix = float(request.form.get('original_audio_mix', 0.3))

        print(f"[INFO] /upload: Form verileri - formats: {output_formats}, style: {subtitle_style}, language: {language}, model: {whisper_model}, use_gpu: {use_gpu}, no_audio_enhance: {no_audio_enhance}, tts_languages: {tts_languages_str}, tts_engine: {tts_engine_str}, no_embed_subtitles: {no_embed_subtitles}, original_audio_mix: {original_audio_mix}")

        tts_languages = [lang.strip().lower() for lang in tts_languages_str.split(',') if lang.strip()]
        tts_engine = TTSEngine.GTTS if tts_engine_str.lower() == "gtts" else TTSEngine.EDGE_TTS
        embed_subtitles = not no_embed_subtitles

        try:
            generator = get_subtitle_generator()
            generator.model_name = whisper_model
            generator.use_gpu = use_gpu
            generator.enhance_audio = not no_audio_enhance
            generator.tts_processor = get_tts_processor() # Ensure TTS processor is set
            print("[INFO] /upload: SubtitleGenerator ayarları güncellendi.")

            task_id = f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            session_output_dir = app.config['OUTPUT_FOLDER'] / task_id
            session_output_dir.mkdir(exist_ok=True)
            print(f"[INFO] /upload: Oturum çıktı dizini oluşturuldu: {session_output_dir}")

            # Run processing in a separate thread to avoid blocking Flask
            # and use asyncio for the actual processing
            def run_processing():
                async def _run():
                    try:
                        if tts_languages:
                            print(f"[INFO] /upload: Çok dilli TTS işlemi başlatılıyor: {filepath}")
                            results = await generator.process_with_multilingual_tts(
                                src=filepath,
                                out_dir=session_output_dir,
                                formats=output_formats,
                                style=SubtitleStyle(subtitle_style),
                                language=language,
                                include_ts=('txt' in output_formats),
                                tts_languages=tts_languages,
                                embed_subtitles=embed_subtitles,
                                tts_engine=tts_engine,
                                original_audio_mix=original_audio_mix
                            )
                            print(f"[INFO] /upload: Çok dilli TTS işlemi tamamlandı. Sonuçlar: {results}")
                        else:
                            print(f"[INFO] /upload: Tekli video/ses işleme başlatılıyor: {filepath}")
                            results = generator.process_one(
                                src=filepath,
                                out_dir=session_output_dir,
                                formats=output_formats,
                                style=SubtitleStyle(subtitle_style),
                                language=language,
                                include_ts=('txt' in output_formats)
                            )
                            print(f"[INFO] /upload: Tekli video/ses işleme tamamlandı. Sonuçlar: {results}")
                        flash('Video başarıyla işlendi!', 'success')
                    except Exception as e:
                        print(f"[ERROR] /upload: Video işlenirken hata oluştu: {str(e)}")
                        flash(f'Video işlenirken hata oluştu: {str(e)}', 'error')
                    finally:
                        if filepath.exists():
                            filepath.unlink()
                            print(f"[INFO] /upload: Geçici dosya silindi: {filepath}")
                        with app.app_context():
                            print(f"[INFO] Görev {task_id} tamamlandı.")
                asyncio.run(_run())

            processing_thread = threading.Thread(target=run_processing)
            processing_thread.start()
            print(f"[INFO] /upload: İşleme arka plan iş parçacığında başlatıldı. Task ID: {task_id}")

            flash('Video işleniyor... Lütfen bekleyiniz. İşlem tamamlandığında sonuçlar görünecektir.', 'info')
            return redirect(url_for('index', _external=True))

        except Exception as e:
            print(f"[ERROR] /upload: Sistem hatası: {str(e)}")
            flash(f'Sistem hatası: {str(e)}', 'error')
            if filepath.exists():
                filepath.unlink()
                print(f"[INFO] /upload: Hata durumunda geçici dosya silindi: {filepath}")
            return redirect(url_for('index', _external=True))

@app.route('/record_and_process', methods=['POST'])
async def record_and_process():
    print("[INFO] /record_and_process rotasına POST isteği geldi.")
    video_file = request.files.get('video_file')
    audio_file = request.files.get('audio_file')

    if not audio_file and not video_file:
        print("[ERROR] /record_and_process: Dosya yüklenemedi: En az bir ses veya video dosyası gerekli.")
        flash('Dosya yüklenemedi: En az bir ses veya video dosyası gerekli.', 'error')
        return redirect(url_for('index', _external=True, tab='record_audio'))

    temp_video_path = None
    temp_audio_path = None
    output_video_path = None

    try:
        task_id = f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}_recorded"
        session_output_dir = app.config['OUTPUT_FOLDER'] / task_id
        session_output_dir.mkdir(exist_ok=True)
        print(f"[INFO] /record_and_process: Oturum çıktı dizini oluşturuldu: {session_output_dir}")

        if video_file:
            video_filename = video_file.filename
            temp_video_path = app.config['UPLOAD_FOLDER'] / video_filename
            video_file.save(temp_video_path)
            print(f"[INFO] /record_and_process: Video dosyası kaydedildi: {temp_video_path}")

        if audio_file:
            audio_filename = audio_file.filename
            temp_audio_path = app.config['UPLOAD_FOLDER'] / audio_filename
            audio_file.save(temp_audio_path)
            print(f"[INFO] /record_and_process: Ses dosyası kaydedildi: {temp_audio_path}")

        final_source_path = temp_audio_path
        if temp_video_path and temp_audio_path:
            output_video_path = session_output_dir / f"combined_{temp_video_path.stem}.mp4"
            command = [
                'ffmpeg',
                '-i', str(temp_video_path),
                '-i', str(temp_audio_path),
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-map', '0:v:0',
                '-map', '1:a:0',
                '-y',
                str(output_video_path)
            ]
            print(f"[INFO] /record_and_process: FFmpeg birleştirme komutu: {' '.join(command)}")
            subprocess.run(command, check=True, capture_output=True)
            final_source_path = output_video_path
            print(f"[INFO] /record_and_process: Video ve ses birleştirildi: {output_video_path}")
        elif temp_video_path:
            final_source_path = temp_video_path
            print(f"[INFO] /record_and_process: Sadece video dosyası kullanılıyor: {final_source_path}")
        
        if not final_source_path or not final_source_path.exists():
            print("[ERROR] /record_and_process: İşlenecek nihai kaynak dosyası bulunamadı.")
            raise Exception("İşlenecek nihai kaynak dosyası bulunamadı.")

        # Subtitle generation parameters
        subtitle_style = request.form.get('style', 'default')
        language = request.form.get('language', 'auto')
        whisper_model = request.form.get('model', 'base')
        use_gpu = 'gpu' in request.form
        embed_subtitles = 'embed_subtitles' in request.form

        print(f"[INFO] /record_and_process: Form verileri - style: {subtitle_style}, language: {language}, model: {whisper_model}, use_gpu: {use_gpu}, embed_subtitles: {embed_subtitles}")

        generator = get_subtitle_generator()
        generator.model_name = whisper_model
        generator.use_gpu = use_gpu
        generator.enhance_audio = True
        generator.tts_processor = get_tts_processor()
        print("[INFO] /record_and_process: SubtitleGenerator ayarları güncellendi.")

        def run_processing_record():
            async def _run():
                try:
                    formats = ['srt']
                    if embed_subtitles: 
                        formats.append('video')
                    
                    if not temp_video_path and 'video' in formats:
                        formats.remove('video')
                        print("[WARN] /record_and_process: Video dosyası sağlanmadığı için videoya altyazı gömme devre dışı bırakıldı.")

                    print(f"[INFO] /record_and_process: Altyazı üretme başlatılıyor: {final_source_path}, formatlar: {formats}")
                    results = generator.process_one(
                        src=final_source_path,
                        out_dir=session_output_dir,
                        formats=formats,
                        style=SubtitleStyle(subtitle_style),
                        language=language,
                        include_ts=False,
                    )
                    print(f"[INFO] /record_and_process: Altyazı üretme tamamlandı. Sonuçlar: {results}")
                    flash('Video ve kaydedilen ses başarıyla işlendi, altyazılar oluşturuldu!', 'success')
                except subprocess.CalledProcessError as e:
                    error_output = e.stderr.decode('utf-8') if e.stderr else 'Bilinmeyen FFmpeg hatası.'
                    print(f"[ERROR] /record_and_process: FFmpeg hatası: {error_output}")
                    flash(f'FFmpeg hatası: {error_output}', 'error')
                except Exception as e:
                    print(f"[ERROR] /record_and_process: Ses ve video işlenirken hata oluştu: {str(e)}")
                    flash(f'Ses ve video işlenirken hata oluştu: {str(e)}', 'error')
                finally:
                    if temp_video_path and temp_video_path.exists():
                        temp_video_path.unlink()
                        print(f"[INFO] /record_and_process: Geçici video dosyası silindi: {temp_video_path}")
                    if temp_audio_path and temp_audio_path.exists():
                        temp_audio_path.unlink()
                        print(f"[INFO] /record_and_process: Geçici ses dosyası silindi: {temp_audio_path}")
                    # if output_video_path and output_video_path.exists() and output_video_path != final_source_path:
                    #     output_video_path.unlink()
                    #     print(f"[INFO] /record_and_process: Birleştirilmiş çıktı dosyası silindi: {output_video_path}")
            asyncio.run(_run())

        processing_thread = threading.Thread(target=run_processing_record)
        processing_thread.start()
        print(f"[INFO] /record_and_process: İşleme arka plan iş parçacığında başlatıldı. Task ID: {task_id}")

        flash('Video ve kaydedilen ses işleniyor... Lütfen bekleyiniz.', 'info')
        return redirect(url_for('index', _external=True, tab='record_audio'))

    except subprocess.CalledProcessError as e:
        error_output = e.stderr.decode('utf-8') if e.stderr else 'Bilinmeyen FFmpeg hatası.'
        print(f"[CRITICAL] /record_and_process: Ana FFmpeg hatası: {error_output}")
        flash(f'FFmpeg hatası: {error_output}', 'error')
        if temp_video_path and temp_video_path.exists(): temp_video_path.unlink()
        if temp_audio_path and temp_audio_path.exists(): temp_audio_path.unlink()
        return redirect(url_for('index', _external=True, tab='record_audio'))

    except Exception as e:
        print(f"[CRITICAL] /record_and_process: Ana sistem hatası: {str(e)}")
        flash(f'Sistem hatası: {str(e)}', 'error')
        if temp_video_path and temp_video_path.exists(): temp_video_path.unlink()
        if temp_audio_path and temp_audio_path.exists(): temp_audio_path.unlink()
        return redirect(url_for('index', _external=True, tab='record_audio'))

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
                    for sub_item in list(item.rglob('*'))[::-1]: # Delete in reverse order to clear files before dirs
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
    return redirect(url_for('index', _external=True))


if __name__ == '__main__':
    print("[INFO] Flask uygulaması başlatılıyor...")
    app.run(debug=True, host="0.0.0.0", port=5001)
    print("[INFO] Flask uygulaması kapatıldı.")

