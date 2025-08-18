import os
import subprocess
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
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

ALLOWED_EXT = {'.mp4', '.mov', '.mkv', '.avi', '.webm', '.flv', '.m4v',
               '.mp3', '.wav', '.m4a', '.flac', '.aac', '.ogg'}

app = Flask(__name__)
app.secret_key = "offline-subtitle-secret"  # flash mesajları için

# ------------------- HTML Şablon -------------------
INDEX_HTML = """
<!doctype html>
<html lang="tr">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Offline Subtitle Tool</title>
  <style>
    body{font:16px/1.4 system-ui,Segoe UI,Roboto,Arial,sans-serif;background:#0b1220;color:#e5e7eb;margin:0}
    .wrap{max-width:900px;margin:40px auto;padding:0 16px}
    .card{background:#0f172a;border:1px solid #334155;border-radius:14px;padding:18px}
    h1{margin:0 0 10px;font-size:24px}
    label{display:block;margin:10px 0 6px;color:#cbd5e1}
    input[type=file],input[type=text],select{width:100%;padding:10px;border-radius:10px;border:1px solid #475569;background:#0b1220;color:#e5e7eb;box-sizing:border-box}
    .row{display:flex;gap:10px;flex-wrap:wrap}
    .btn{appearance:none;border:none;background:#22c55e;color:#0b1220;border-radius:12px;padding:10px 14px;font-weight:700;cursor:pointer;transition:background 0.2s}
    .btn:hover{background:#16a34a}
    .btn:disabled{background:#374151;cursor:not-allowed}
    .btn.alt{background:#1f2937;color:#e5e7eb;border:1px solid #475569}
    .btn.alt:hover{background:#374151}
    .muted{color:#94a3b8}
    .hr{height:1px;background:#334155;margin:14px 0}
    ul{padding-left:18px}
    .err{background:#7f1d1d;color:#fecaca;border:1px solid #ef4444;padding:8px 10px;border-radius:10px;margin-bottom:10px}
    .ok{background:#052e21;color:#a7f3d0;border:1px solid #10b981;padding:8px 10px;border-radius:10px;margin-bottom:10px}
    a.dl{display:inline-block;margin:6px 6px 0 0;padding:8px 12px;border:1px solid #475569;border-radius:10px;color:#e5e7eb;text-decoration:none;transition:all 0.2s}
    a.dl:hover{background:#374151;border-color:#64748b}
    .checkbox-row{display:flex;gap:20px;flex-wrap:wrap;align-items:center;margin-top:8px}
    .checkbox-item{display:flex;gap:8px;align-items:center;margin:0}
    .checkbox-item input[type=checkbox]{width:auto}
    .processing{display:none;background:#1e40af;color:#dbeafe;border:1px solid #3b82f6;padding:8px 10px;border-radius:10px;margin-bottom:10px}
    .file-info{background:#1e293b;border:1px solid #475569;border-radius:8px;padding:10px;margin:10px 0;font-size:14px}
  </style>
  <script>
    function showProcessing() {
      const form = document.querySelector('form');
      const btn = document.querySelector('button[type=submit]');
      const processing = document.querySelector('.processing');

      if (form && btn && processing) {
        btn.disabled = true;
        btn.textContent = 'İşleniyor...';
        processing.style.display = 'block';
      }
    }
  </script>
</head>
<body>
  <div class="wrap">
    <h1>Offline Subtitle Tool <span class="muted">(Tarayıcıdan kullanım)</span></h1>
    <div class="card">
      {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        {% for cat, msg in messages %}
          <div class="{{ 'ok' if cat=='success' else 'err' }}">{{ msg }}</div>
        {% endfor %}
      {% endif %}
      {% endwith %}

      <div class="processing">
        ⏳ Dosya işleniyor... Bu işlem birkaç dakika sürebilir.
      </div>

      <form method="post" action="{{ url_for('generate_subtitles') }}" enctype="multipart/form-data" onsubmit="showProcessing()">
        <label>Video/Audio dosyası</label>
        <input type="file" name="file" accept="video/*,audio/*" required />

        <div class="row">
          <div style="flex:1;min-width:220px">
            <label>Çıktı formatları (virgülle ayrılmış)</label>
            <input type="text" name="formats" value="video,srt" placeholder="video,srt,vtt,ass,txt" />
            <div class="muted" style="font-size:12px;margin-top:4px">
              Örnek: srt,vtt,video veya sadece srt
            </div>
          </div>
          <div style="flex:1;min-width:220px">
            <label>Dil (ISO kodu veya auto)</label>
            <input type="text" name="language" value="auto" placeholder="auto, tr, en, es..." />
            <div class="muted" style="font-size:12px;margin-top:4px">
              auto: otomatik tespit
            </div>
          </div>
        </div>

        <div class="row">
          <div style="flex:1;min-width:220px">
            <label>Altyazı stili</label>
            <select name="style">
              <option value="default">Default</option>
              <option value="bold">Bold</option>
              <option value="elegant">Elegant</option>
              <option value="cinema">Cinema</option>
              <option value="modern">Modern</option>
              <option value="minimal">Minimal</option>
              <option value="terminal">Terminal</option>
            </select>
          </div>
          <div style="flex:1;min-width:220px">
            <label>Whisper modeli</label>
            <select name="model">
              <option value="tiny">Tiny (hızlı, düşük kalite)</option>
              <option value="base" selected>Base (dengeli)</option>
              <option value="small">Small (iyi kalite)</option>
              <option value="medium">Medium (yüksek kalite)</option>
              <option value="large">Large (en iyi kalite, yavaş)</option>
            </select>
          </div>
        </div>

        <div class="checkbox-row">
          <label class="checkbox-item">
            <input type="checkbox" name="include_timestamps" />
            TXT çıktısında zaman damgası
          </label>
          <label class="checkbox-item">
            <input type="checkbox" name="no_enhance_audio" />
            Ses iyileştirmesini kapat
          </label>
          <label class="checkbox-item">
            <input type="checkbox" name="gpu" />
            GPU hızlandırma (varsa)
          </label>
        </div>

        <div class="hr"></div>
        <div class="row">
          <button class="btn" type="submit">🎬 Altyazı Oluştur</button>
          <a class="btn alt" href="{{ url_for('list_outputs') }}">📁 Tüm Çıktılar</a>
          <a class="btn alt" href="{{ url_for('clear_files') }}">🗑️ Temizle</a>
        </div>
        <div class="file-info">
          <strong>Desteklenen formatlar:</strong> MP4, AVI, MOV, MKV, WebM, MP3, WAV, M4A, FLAC vb.<br>
          <strong>Gereksinimler:</strong> Python, ffmpeg/ffprobe kurulu olmalı
        </div>
      </form>
    </div>

    {% if files %}
      <div class="card" style="margin-top:16px">
        <h2>📥 İndirilebilir Çıktılar ({{ files|length }} dosya)</h2>
        {% if files|length > 10 %}
          <div class="muted">Son işlem sonuçları:</div>
        {% endif %}
        <ul>
          {% for f in files[:20] %}
            <li>
              <a class="dl" href="{{ url_for('download_output', filename=f) }}">
                📄 {{ f }}
              </a>
              <span class="muted">({{ f.split('.')[-1].upper() }})</span>
            </li>
          {% endfor %}
          {% if files|length > 20 %}
            <li class="muted">... ve {{ files|length - 20 }} dosya daha</li>
          {% endif %}
        </ul>
      </div>
    {% endif %}
  </div>
</body>
</html>
"""


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

    return render_template_string(INDEX_HTML, files=files)


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

        # İşlemi çalıştır
        result, error = _safe_run_subprocess(cmd)

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
        flash(f"✅ Başarıyla tamamlandı! {len(produced_files)} dosya oluşturuldu.", "success")

        # Sonuçları göster
        return render_template_string(INDEX_HTML, files=produced_files)

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

    html = f"""
    <h1>📁 Tüm Çıktılar ({len(files)} dosya)</h1>
    <p><a href="{url_for('index')}">← Ana sayfaya dön</a></p>
    <ul>
    """
    for f in files:
        file_size = (OUTPUT_DIR / f).stat().st_size
        size_str = f"{file_size / 1024 / 1024:.1f}MB" if file_size > 1024 * 1024 else f"{file_size / 1024:.1f}KB"
        html += f'<li><a href="{url_for("download_output", filename=f)}">{f}</a> <em>({size_str})</em></li>'
    html += "</ul>"
    return render_template_string(html)


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
    print(f"🌐 Server: http://127.0.0.1:5000")
    print(f"⚠️  app.py dosyasının aynı klasörde olduğundan emin olun!")

    app.run(host="127.0.0.1", port=5000, debug=True)