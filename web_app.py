from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
import os
from pathlib import Path
import asyncio
import threading
from datetime import datetime

# Import the core subtitle generator from server.py
from server import OfflineSubtitleGenerator, SubtitleStyle, LanguageCode, MultilingualTTSProcessor, TTSEngine
from multilingual_processor import SupportedLanguage # FFmpegError is not defined in server.py

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
        subtitle_generator = OfflineSubtitleGenerator(whisper_model="base", use_gpu=False, enhance_audio=True)
    return subtitle_generator

def get_tts_processor():
    global tts_processor
    if tts_processor is None:
        tts_processor = MultilingualTTSProcessor()
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
    supported_languages = get_language_names_map()
    return render_template('index.html', supported_languages=supported_languages, files=get_output_files())

def get_output_files():
    return sorted([str(f.relative_to(app.config['OUTPUT_FOLDER'])) for f in app.config['OUTPUT_FOLDER'].rglob('*') if f.is_file()])

@app.route('/list_outputs')
def list_outputs():
    files = get_output_files()
    return render_template('files.html', files=files)

@app.route('/download/<path:filename>')
def download_output(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)

@app.route('/upload', methods=['POST'])
async def upload_file():
    if 'file' not in request.files:
        flash('Dosya yüklenemedi: Dosya bulunamadı', 'error')
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        flash('Dosya yüklenemedi: Dosya adı boş', 'error')
        return redirect(url_for('index'))

    if file:
        filename = file.filename
        filepath = app.config['UPLOAD_FOLDER'] / filename
        file.save(filepath)

        output_formats = request.form.getlist('output_formats')
        subtitle_style = request.form.get('subtitle_style', 'default')
        language = request.form.get('language', 'auto')
        whisper_model = request.form.get('whisper_model', 'base')
        use_gpu = 'use_gpu' in request.form
        no_audio_enhance = 'no_audio_enhance' in request.form
        tts_languages_str = request.form.get('tts_languages', '')
        tts_engine_str = request.form.get('tts_engine', 'edge_tts')
        no_embed_subtitles = 'no_embed_subtitles' in request.form
        original_audio_mix = float(request.form.get('original_audio_mix', 0.3))

        tts_languages = [lang.strip().lower() for lang in tts_languages_str.split(',') if lang.strip()]
        tts_engine = TTSEngine.GTTS if tts_engine_str.lower() == "gtts" else TTSEngine.EDGE_TTS
        embed_subtitles = not no_embed_subtitles

        try:
            generator = get_subtitle_generator()
            generator.model_name = whisper_model
            generator.use_gpu = use_gpu
            generator.enhance_audio = not no_audio_enhance
            generator.tts_processor = get_tts_processor() # Ensure TTS processor is set

            task_id = f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            session_output_dir = app.config['OUTPUT_FOLDER'] / task_id
            session_output_dir.mkdir(exist_ok=True)

            # Run processing in a separate thread to avoid blocking Flask
            # and use asyncio for the actual processing
            def run_processing():
                async def _run():
                    try:
                        if tts_languages:
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
                        else:
                            results = generator.process_one(
                                src=filepath,
                                out_dir=session_output_dir,
                                formats=output_formats,
                                style=SubtitleStyle(subtitle_style),
                                language=language,
                                include_ts=('txt' in output_formats)
                            )
                        flash('Video başarıyla işlendi!', 'success')
                        # You might want to store results in session or a database
                        # to display them on a results page.
                        # For now, just redirect to index.
                        # return redirect(url_for('results', task_id=task_id))
                    except Exception as e:
                        flash(f'Video işlenirken hata oluştu: {str(e)}', 'error')
                    finally:
                        # Clean up uploaded file after processing
                        if filepath.exists():
                            filepath.unlink()
                        # Redirect in the same thread after processing
                        with app.app_context():
                            print(f"Task {task_id} completed, redirecting.")
                            # This redirect won't work directly because it's a separate thread
                            # For a real app, you'd use websockets or similar to update the client
                asyncio.run(_run())

            # Start the processing in a new thread
            processing_thread = threading.Thread(target=run_processing)
            processing_thread.start()

            flash('Video işleniyor... Lütfen bekleyiniz. İşlem tamamlandığında sonuçlar görünecektir.', 'info')
            return redirect(url_for('index'))

        except Exception as e:
            flash(f'Sistem hatası: {str(e)}', 'error')
            # Clean up uploaded file if an error occurs before processing starts
            if filepath.exists():
                filepath.unlink()
            return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5241
    )

