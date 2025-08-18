import os
import subprocess
import time
import json
from pathlib import Path
from flask import Flask, request, send_from_directory, render_template_string, redirect, url_for, flash
from werkzeug.utils import secure_filename

# =====================================================
#  server.py — Offline Web Arayüzü (Flask)
#  Video/audio yükleme → app.py ile işleme → indirme
# =====================================================

APP_DIR = Path.cwd()
UPLOAD_DIR = APP_DIR / "uploads"
OUTPUT_DIR = APP_DIR / "outputs"
STATIC_DIR = APP_DIR / "static"
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)
(STATIC_DIR / "css").mkdir(exist_ok=True)
(STATIC_DIR / "js").mkdir(exist_ok=True)

ALLOWED_EXT = {'.mp4', '.mov', '.mkv', '.avi', '.webm', '.flv', '.m4v',
               '.mp3', '.wav', '.m4a', '.flac', '.aac', '.ogg'}

app = Flask(__name__)
app.secret_key = "offline-subtitle-secret"  # flash mesajları için

# ------------------- Yardımcı Fonksiyonlar -------------------
def _is_allowed(filename: str) -> bool:
    return Path(filename).suffix.lower() in ALLOWED_EXT


def _build_command(app_py: Path, input_path: Path, output_base: Path, formats: str,
                   style: str, language: str, include_ts: bool, model: str,
                   enhance_audio: bool, use_gpu: bool = False):
    """app.py için komut satırı oluştur"""
    cmd = [
        "python", str(app_py),
        "-i", str(input_path),
        "-o", str(output_base)
    ]

    if formats:
        cmd += ["--formats", formats]
    if style:
        cmd += ["--style", style]
    if language and language != "auto":
        cmd += ["--language", language]
    if include_ts:
        cmd += ["--include-timestamps"]
    if model:
        cmd += ["--model", model]
    if not enhance_audio:
        cmd += ["--no-audio-enhance"]
    if use_gpu:
        cmd += ["--gpu"]

    return cmd


def _safe_run_subprocess(cmd, timeout=3600):
    """Güvenli subprocess çalıştırma"""
    try:
        print(f"[DEBUG] Running command: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=APP_DIR  # Çalışma dizinini belirt
        )
        print(f"[DEBUG] STDOUT: {result.stdout}")
        if result.stderr:
            print(f"[DEBUG] STDERR: {result.stderr}")
        return result, None
    except subprocess.TimeoutExpired:
        return None, "İşlem zaman aşımına uğradı (1 saat)"
    except subprocess.CalledProcessError as e:
        error_msg = f"İşleme hatası (kod {e.returncode})"
        if e.stderr:
            error_msg += f": {e.stderr[:500]}"  # Hata mesajını kısalt
        return None, error_msg
    except FileNotFoundError:
        return None, "Python bulunamadı. PATH ayarlarınızı kontrol edin."
    except Exception as e:
        return None, f"Beklenmeyen hata: {str(e)}"


# ------------------- Flask Routes -------------------
@app.route("/", methods=["GET"])
def index():
    """Ana sayfa"""
    # Son oluşturulan dosyaları göster
    files = []
    if OUTPUT_DIR.exists():
        for f in sorted(OUTPUT_DIR.rglob("*"), key=lambda x: x.stat().st_mtime, reverse=True):
            if f.is_file():
                files.append(str(f.relative_to(OUTPUT_DIR)))

    return render_template('index.html', files=files)


@app.route("/generate_subtitles", methods=["POST"])
def generate_subtitles():
    """Ana işleme endpoint'i"""
    try:
        # Dosya kontrolü
        if 'file' not in request.files:
            flash("Dosya yüklenmedi", "error")
            return redirect(url_for('index'))

        uploaded_file = request.files['file']
        if uploaded_file.filename == "":
            flash("Dosya seçilmedi", "error")
            return redirect(url_for('index'))

        if not _is_allowed(uploaded_file.filename):
            allowed_str = ", ".join(sorted(ALLOWED_EXT))
            flash(f"Desteklenmeyen dosya türü. Desteklenen: {allowed_str}", "error")
            return redirect(url_for('index'))

        # Dosyayı güvenli şekilde kaydet
        safe_name = secure_filename(uploaded_file.filename)
        if not safe_name:
            flash("Geçersiz dosya adı", "error")
            return redirect(url_for('index'))

        input_path = UPLOAD_DIR / safe_name
        uploaded_file.save(str(input_path))

        # Dosya boyutu kontrolü (isteğe bağlı)
        file_size = input_path.stat().st_size
        if file_size > 500 * 1024 * 1024:  # 500MB limit
            flash("Dosya çok büyük (500MB limit)", "error")
            input_path.unlink()  # Dosyayı sil
            return redirect(url_for('index'))

        print(f"[DEBUG] Uploaded file: {safe_name} ({file_size / 1024 / 1024:.1f}MB)")

        # Form parametrelerini al ve temizle
        formats = request.form.get('formats', 'video,srt').strip()
        style = request.form.get('style', 'default').strip()
        language = request.form.get('language', 'auto').strip()
        include_ts = request.form.get('include_timestamps') is not None
        no_enhance = request.form.get('no_enhance_audio') is not None
        model = request.form.get('model', 'base').strip()
        use_gpu = request.form.get('gpu') is not None

        # Format kontrolü
        valid_formats = {'video', 'srt', 'vtt', 'ass', 'txt'}
        format_list = [f.strip().lower() for f in formats.split(',') if f.strip()]
        invalid_formats = [f for f in format_list if f not in valid_formats]

        if invalid_formats:
            flash(f"Geçersiz format(lar): {', '.join(invalid_formats)}", "error")
            return redirect(url_for('index'))

        # Çıktı dizini oluştur
        base_name = Path(safe_name).stem
        output_base = OUTPUT_DIR / base_name
        output_base.mkdir(exist_ok=True)

        # app.py varlığını kontrol et
        app_py = APP_DIR / "app.py"
        if not app_py.exists():
            flash("app.py bulunamadı. server.py ile aynı klasörde olmalı.", "error")
            return redirect(url_for('index'))

        # Komutu oluştur
        cmd = _build_command(
            app_py=app_py,
            input_path=input_path,
            output_base=output_base,
            formats=formats,
            style=style,
            language=language,
            include_ts=include_ts,
            model=model,
            enhance_audio=(not no_enhance),
            use_gpu=use_gpu
        )

        # İşlem başlangıç zamanını kaydet
        start_time = time.time()
        print(f"[INFO] Starting processing at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"[INFO] Command: {' '.join(cmd)}")

        # İşlemi çalıştır
        result, error = _safe_run_subprocess(cmd)

        # İşlem süresini hesapla
        processing_time = time.time() - start_time
        print(f"[INFO] Processing completed in {processing_time:.2f} seconds")

        if error:
            flash(error, "error")
            return redirect(url_for('index'))

        # Başarılı işlem - çıktı dosyalarını listele
        produced_files = []
        if output_base.exists():
            for f in sorted(output_base.rglob("*")):
                if f.is_file():
                    rel_path = f.relative_to(OUTPUT_DIR)
                    produced_files.append(str(rel_path))

        # Yüklenen dosyayı temizle
        try:
            if input_path.exists():
                input_path.unlink()
        except:
            pass

        if not produced_files:
            flash("Çıktı dosyası oluşturulamadı. Logları kontrol edin.", "error")
            return redirect(url_for('index'))

        # Başarı mesajı
        flash(f"✅ Başarıyla tamamlandı! {len(produced_files)} dosya oluşturuldu. İşlem süresi: {processing_time:.1f} saniye", "success")

        # Ana sayfaya yönlendir
        return redirect(url_for('index'))

    except Exception as e:
        print(f"[ERROR] Sistem hatası: {str(e)}")
        flash(f"Sistem hatası: {str(e)}", "error")
        return redirect(url_for('index'))


@app.route('/outputs')
def list_outputs():
    """Tüm çıktı dosyalarını listele"""
    files = []
    if OUTPUT_DIR.exists():
        for f in sorted(OUTPUT_DIR.rglob("*"), key=lambda x: x.stat().st_mtime, reverse=True):
            if f.is_file():
                files.append(f.relative_to(OUTPUT_DIR))

    return render_template('index.html', files=files, show_all=True)


@app.route('/download/<path:filename>')
def download_output(filename: str):
    """Çıktı dosyasını indir"""
    try:
        file_path = OUTPUT_DIR / filename
        if not file_path.exists() or not file_path.is_file():
            flash("Dosya bulunamadı", "error")
            return redirect(url_for('index'))

        # Güvenlik: dosyanın OUTPUT_DIR içinde olduğundan emin ol
        try:
            file_path.resolve().relative_to(OUTPUT_DIR.resolve())
        except ValueError:
            flash("Güvenlik: Erişim reddedildi", "error")
            return redirect(url_for('index'))

        return send_from_directory(
            OUTPUT_DIR,
            filename,
            as_attachment=True,
            download_name=Path(filename).name
        )
    except Exception as e:
        flash(f"İndirme hatası: {str(e)}", "error")
        return redirect(url_for('index'))


@app.route('/clear')
def clear_files():
    """Upload ve output klasörlerini temizle"""
    try:
        count = 0
        # Upload klasörünü temizle
        if UPLOAD_DIR.exists():
            for f in UPLOAD_DIR.iterdir():
                if f.is_file():
                    f.unlink()
                    count += 1

        # Output klasörünü temizle
        if OUTPUT_DIR.exists():
            for f in OUTPUT_DIR.rglob("*"):
                if f.is_file():
                    f.unlink()
                    count += 1
            # Boş klasörleri de sil
            for d in OUTPUT_DIR.iterdir():
                if d.is_dir():
                    try:
                        d.rmdir()
                    except:
                        pass

        flash(f"✅ {count} dosya temizlendi", "success")
    except Exception as e:
        flash(f"Temizleme hatası: {str(e)}", "error")

    return redirect(url_for('index'))


# API endpoint for progress tracking (future enhancement)
@app.route('/api/status/<task_id>')
def get_status(task_id):
    """Get processing status for a task"""
    # This could be enhanced with Redis or database for real progress tracking
    return {"status": "processing", "progress": 50}


@app.errorhandler(404)
def not_found(e):
    return redirect(url_for('index'))


@app.errorhandler(500)
def server_error(e):
    flash("Sunucu hatası oluştu", "error")
    return redirect(url_for('index'))


# ------------------- Çalıştır -------------------
if __name__ == "__main__":
    print(f"🚀 Offline Subtitle Tool Web Interface")
    print(f"📁 Upload Directory: {UPLOAD_DIR}")
    print(f"📁 Output Directory: {OUTPUT_DIR}")
    print(f"📁 Static Directory: {STATIC_DIR}")
    print(f"🌐 Server: http://127.0.0.1:5000")
    print(f"⚠️  app.py dosyasının aynı klasörde olduğundan emin olun!")

    app.run(host="127.0.0.1", port=5000, debug=True)