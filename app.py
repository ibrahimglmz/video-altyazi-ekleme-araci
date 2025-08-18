#!/usr/bin/env python3
"""
Offline Professional Video Subtitle Generator (No API)
=====================================================

A high-performance, offline CLI tool that:
- Transcribes audio/video locally with optimized Whisper models
- Generates SRT/VTT/TXT/ASS subtitles with advanced formatting
- Embeds hard subtitles into videos with style-preserving techniques
- Supports GPU acceleration (when available)
- Includes intelligent audio preprocessing
- Features comprehensive error handling
- Offers batch processing with progress tracking

Requirements:
  pip install openai-whisper pydub tqdm faster-whisper torchaudio
  # Requires ffmpeg/ffprobe in PATH

Usage examples:
  python pro_subtitle_tool.py -i input.mp4 --formats video,ass --style cinema --gpu
  python pro_subtitle_tool.py -i media_folder --batch --language tr --formats srt,vtt --model large
"""

import argparse
import os
import sys
import json
import shutil
import subprocess
import warnings
import signal
import threading
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import platform

# Suppress unnecessary warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Global progress tracking
PROGRESS_CALLBACK = None
CURRENT_TASK = None

# -----------------------------
# Configuration
# -----------------------------
VIDEO_EXTS = {'.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.m4v', '.mpg', '.mpeg'}
AUDIO_EXTS = {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.opus'}
ALLOWED_EXTS = VIDEO_EXTS | AUDIO_EXTS

# Progress tracking class
class ProgressTracker:
    def __init__(self, callback=None):
        self.callback = callback
        self.current_step = 0
        self.total_steps = 5
        self.current_message = "Initializing..."
        
    def update(self, step: int, message: str):
        self.current_step = step
        self.current_message = message
        progress = int((step / self.total_steps) * 100)
        
        print(f"[PROGRESS] {progress}% - {message}")
        
        if self.callback:
            self.callback(progress, message)


# Hardware acceleration settings
USE_GPU = False
COMPUTE_TYPE = "float16"  # float16 or int8 for faster-whisper


class LanguageCode(str, Enum):
    AUTO = "auto"
    TR = "tr"
    EN = "en"
    ES = "es"
    FR = "fr"
    DE = "de"
    IT = "it"
    PT = "pt"
    RU = "ru"
    JA = "ja"
    KO = "ko"
    ZH = "zh"
    AR = "ar"


class SubtitleStyle(str, Enum):
    DEFAULT = "default"
    BOLD = "bold"
    ELEGANT = "elegant"
    CINEMA = "cinema"
    MODERN = "modern"
    MINIMAL = "minimal"
    TERMINAL = "terminal"


@dataclass
class SubtitleConfig:
    font_name: str
    font_size: int
    font_color: str
    outline_color: str
    shadow_color: str
    background_color: str
    background_opacity: float
    outline_width: int
    shadow_offset: int
    alignment: int  # 1=left, 2=center, 3=right
    margin_vertical: int
    margin_horizontal: int
    max_chars_per_line: int
    line_spacing: int
    wrap_style: int  # 0=smart, 1=end-of-line, 2=no-word-wrap, 3=smart-with-bottom


# -----------------------------
# Utilities
# -----------------------------

def get_system_fonts() -> List[str]:
    """Attempt to get system fonts based on OS"""
    system = platform.system()
    if system == "Windows":
        return ["Arial", "Segoe UI", "Calibri", "Times New Roman"]
    elif system == "Darwin":
        return ["Helvetica", "Arial", "Menlo", "Times New Roman"]
    else:  # Linux and others
        return ["DejaVu Sans", "Liberation Sans", "Arial", "FreeSans"]


def run(cmd: List[str], check: bool = True, capture: bool = True, timeout: int = 300) -> subprocess.CompletedProcess:
    """Run command with better error handling and timeout"""
    kwargs = {
        'stdout': subprocess.PIPE if capture else None,
        'stderr': subprocess.PIPE if capture else None,
        'text': True,
        'timeout': timeout
    }
    try:
        proc = subprocess.run(cmd, **kwargs)
        if check and proc.returncode != 0:
            raise RuntimeError(f"Command failed (code {proc.returncode}): {' '.join(cmd)}\nSTDERR:\n{proc.stderr}")
        return proc
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"Command timed out: {' '.join(cmd)}")


def ffprobe_info(path: Path) -> Dict[str, Any]:
    """Get detailed media info with ffprobe"""
    if not shutil.which("ffprobe"):
        raise RuntimeError("ffprobe not found in PATH. Please install ffmpeg.")

    cmd = [
        "ffprobe", "-v", "error",
        "-print_format", "json",
        "-show_format", "-show_streams",
        "-show_chapters", "-show_entries", "format=duration",
        str(path)
    ]

    proc = run(cmd, check=False)
    try:
        return json.loads(proc.stdout) if proc.stdout else {}
    except json.JSONDecodeError:
        return {}


def is_video(path: Path) -> bool:
    """Check if file is a video based on extension and content"""
    ext_check = path.suffix.lower() in VIDEO_EXTS
    if not ext_check:
        return False

    # Additional content check
    info = ffprobe_info(path)
    return any(s.get('codec_type') == 'video' for s in info.get('streams', []))


def is_audio(path: Path) -> bool:
    """Check if file is audio based on extension and content"""
    ext_check = path.suffix.lower() in AUDIO_EXTS
    if not ext_check:
        return False

    info = ffprobe_info(path)
    streams = info.get('streams', [])
    return any(s.get('codec_type') == 'audio' for s in streams) or len(streams) == 0


def hex_to_ass(hex_color: str, alpha: str = "00") -> str:
    """Convert #RRGGBB to ASS format &HAABBGGRR"""
    h = hex_color.lstrip('#')
    if len(h) == 3:  # Short form #RGB
        h = ''.join([c * 2 for c in h])
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"&H{alpha}{b:02X}{g:02X}{r:02X}"


def srt_time(seconds: float) -> str:
    """Convert seconds to SRT timestamp format"""
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((td.total_seconds() % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def vtt_time(seconds: float) -> str:
    """Convert seconds to VTT timestamp format"""
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((td.total_seconds() % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


def smart_split(text: str, max_chars: int) -> List[str]:
    """Intelligently split text into lines respecting word boundaries"""
    text = text.strip()
    if len(text) <= max_chars:
        return [text]

    words = text.split()
    lines = []
    current_line = []
    current_length = 0

    for word in words:
        word_length = len(word)

        # If word itself is too long, split it
        if word_length > max_chars:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = []
                current_length = 0

            # Split the long word
            parts = [word[i:i + max_chars] for i in range(0, word_length, max_chars)]
            lines.extend(parts[:-1])
            current_line = [parts[-1]]
            current_length = len(parts[-1])
            continue

        # Check if adding this word would exceed the limit
        space_needed = 1 if current_line else 0
        if current_length + word_length + space_needed > max_chars:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_length = word_length
        else:
            current_line.append(word)
            current_length += word_length

    if current_line:
        lines.append(' '.join(current_line))

    return lines


def estimate_transcription_time(duration: float, model_size: str) -> float:
    """Estimate transcription time based on duration and model size"""
    # Approximate factors (seconds of processing per second of audio)
    factors = {
        'tiny': 0.3,
        'base': 0.5,
        'small': 0.8,
        'medium': 1.2,
        'large': 2.0,
        'large-v2': 2.2,
        'large-v3': 2.0
    }
    factor = factors.get(model_size.lower(), 1.5)
    return duration * factor


# -----------------------------
# Style Presets
# -----------------------------

def style_preset(style: SubtitleStyle) -> SubtitleConfig:
    """Create style configuration based on preset"""
    system_fonts = get_system_fonts()
    base_font = system_fonts[0] if system_fonts else "Arial"

    if style == SubtitleStyle.BOLD:
        return SubtitleConfig(
            font_name=base_font,
            font_size=28,
            font_color="#FFFFFF",
            outline_color="#000000",
            shadow_color="#000000",
            background_color="#222222",
            background_opacity=0.85,
            outline_width=3,
            shadow_offset=2,
            alignment=2,  # Center
            margin_vertical=40,
            margin_horizontal=30,
            max_chars_per_line=42,
            line_spacing=5,
            wrap_style=0  # Smart
        )

    elif style == SubtitleStyle.ELEGANT:
        font = "Times New Roman" if "Times New Roman" in system_fonts else base_font
        return SubtitleConfig(
            font_name=font,
            font_size=26,
            font_color="#F5F5DC",  # Beige
            outline_color="#2F2F2F",
            shadow_color="#1A1A1A",
            background_color="#2F2F2F",
            background_opacity=0.7,
            outline_width=1,
            shadow_offset=1,
            alignment=2,
            margin_vertical=50,
            margin_horizontal=60,
            max_chars_per_line=45,
            line_spacing=8,
            wrap_style=0
        )

    elif style == SubtitleStyle.CINEMA:
        return SubtitleConfig(
            font_name="Arial",
            font_size=32,
            font_color="#FFD700",  # Gold
            outline_color="#000000",
            shadow_color="#000000",
            background_color="#000000",
            background_opacity=0.9,
            outline_width=2,
            shadow_offset=3,
            alignment=2,
            margin_vertical=30,
            margin_horizontal=20,
            max_chars_per_line=38,
            line_spacing=4,
            wrap_style=3  # Smart with bottom alignment
        )

    elif style == SubtitleStyle.MODERN:
        font = "Roboto" if "Roboto" in system_fonts else "Arial"
        return SubtitleConfig(
            font_name=font,
            font_size=24,
            font_color="#00FF41",  # Matrix green
            outline_color="#1A1A1A",
            shadow_color="#0A0A0A",
            background_color="#1A1A1A",
            background_opacity=0.7,
            outline_width=1,
            shadow_offset=2,
            alignment=2,
            margin_vertical=35,
            margin_horizontal=40,
            max_chars_per_line=50,
            line_spacing=6,
            wrap_style=0
        )

    elif style == SubtitleStyle.MINIMAL:
        return SubtitleConfig(
            font_name=base_font,
            font_size=20,
            font_color="#FFFFFF",
            outline_color="#000000",
            shadow_color="#000000",
            background_color="#000000",
            background_opacity=0.5,
            outline_width=0,
            shadow_offset=0,
            alignment=2,
            margin_vertical=20,
            margin_horizontal=10,
            max_chars_per_line=55,
            line_spacing=3,
            wrap_style=1  # End of line
        )

    elif style == SubtitleStyle.TERMINAL:
        font = "Courier New" if "Courier New" in system_fonts else "Monospace"
        return SubtitleConfig(
            font_name=font,
            font_size=22,
            font_color="#00FF00",  # Green
            outline_color="#003300",
            shadow_color="#001100",
            background_color="#000000",
            background_opacity=0.8,
            outline_width=0,
            shadow_offset=1,
            alignment=1,  # Left
            margin_vertical=25,
            margin_horizontal=50,
            max_chars_per_line=60,
            line_spacing=2,
            wrap_style=1
        )

    # Default style
    return SubtitleConfig(
        font_name=base_font,
        font_size=24,
        font_color="#FFFFFF",
        outline_color="#000000",
        shadow_color="#000000",
        background_color="#000000",
        background_opacity=0.7,
        outline_width=2,
        shadow_offset=1,
        alignment=2,
        margin_vertical=30,
        margin_horizontal=20,
        max_chars_per_line=50,
        line_spacing=5,
        wrap_style=0
    )


# -----------------------------
# Core Subtitle Generator
# -----------------------------

class OfflineSubtitleGenerator:
    def __init__(self, whisper_model: str = "base", enhance_audio: bool = True, use_gpu: bool = False):
        self.model_name = whisper_model
        self.enhance_audio = enhance_audio
        self.use_gpu = use_gpu
        self._model = None
        self._processor = None
        self.progress_tracker = ProgressTracker()

        if not shutil.which("ffmpeg"):
            raise RuntimeError("ffmpeg not found in PATH. Please install ffmpeg.")

        # Verify basic whisper installation
        try:
            import whisper
        except ImportError:
            raise ImportError("Whisper not installed. Run: pip install openai-whisper")

    def set_progress_callback(self, callback):
        """Set progress callback function"""
        self.progress_tracker.callback = callback

    def load_model(self):
        """Lazy load the Whisper model with error handling"""
        if self._model is not None:
            return self._model

        self.progress_tracker.update(1, f"Loading Whisper model: {self.model_name}")

        try:
            import whisper
            from whisper.utils import get_writer

            print(f"[+] Loading Whisper model: {self.model_name} ({'GPU' if self.use_gpu else 'CPU'})")

            # Use faster-whisper if available
            if self.use_gpu:
                try:
                    from faster_whisper import WhisperModel
                    self._model = WhisperModel(
                        self.model_name,
                        device="cuda",
                        compute_type=COMPUTE_TYPE,
                        download_root=str(Path.home() / ".cache" / "whisper")
                    )
                    self._processor = "faster"
                    print("[+] Using faster-whisper with GPU acceleration")
                    self.progress_tracker.update(2, "Model loaded with GPU acceleration")
                    return self._model
                except ImportError:
                    print("[!] faster-whisper not available, falling back to standard whisper")

            # Fall back to standard whisper
            self._model = whisper.load_model(
                self.model_name,
                download_root=str(Path.home() / ".cache" / "whisper"),
                device="cuda" if self.use_gpu else "cpu"
            )
            self._processor = "standard"
            self.progress_tracker.update(2, "Model loaded successfully")
            return self._model

        except Exception as e:
            raise RuntimeError(f"Failed to load Whisper model: {str(e)}")

    def extract_audio(self, src: Path, dst_wav: Path) -> Tuple[float, int]:
        """Extract and enhance audio, returning duration and sample rate"""
        self.progress_tracker.update(2, "Extracting and processing audio...")
        
        # Validate input file
        if not src.exists():
            raise FileNotFoundError(f"Source file not found: {src}")

        # Get source file info
        src_info = ffprobe_info(src)
        if not any(s.get('codec_type') == 'audio' for s in src_info.get('streams', [])):
            raise ValueError(f"No audio stream found in source file: {src}")

        # Build audio filters
        filters = []
        if self.enhance_audio:
            filters = [
                "highpass=f=80",  # Remove low frequency rumble
                "lowpass=f=8000",  # Remove high frequency noise
                "dynaudnorm=p=0.5",  # More controlled dynamic normalization
                "aresample=async=1000",  # Smooth resampling
                "volume=1.2",  # Volume boost
                "compand=attacks=0:decays=0.3:points=-80/-80|-12/-12|0/-3"  # Soft compression
            ]

        try:
            # Build and run FFmpeg command
            cmd = [
                "ffmpeg",
                "-y",  # Overwrite output
                "-hide_banner",  # Cleaner output
                "-loglevel", "error",  # Only show errors
                "-i", str(src),  # Input file
                *(["-af", ",".join(filters)] if filters else []),
                "-vn",  # Disable video
                "-ac", "1",  # Mono audio
                "-ar", "16000",  # 16kHz sample rate
                "-acodec", "pcm_s16le",  # 16-bit PCM
                "-fflags", "+genpts",  # Generate proper timestamps
                "-f", "wav",  # WAV format
                str(dst_wav)  # Output file
            ]

            # Run with timeout
            run(cmd, timeout=300)

            # Verify output file
            if not dst_wav.exists() or dst_wav.stat().st_size == 0:
                raise RuntimeError("Audio extraction failed - empty output file")

            # Get output file metadata
            dst_info = ffprobe_info(dst_wav)
            if not dst_info:
                raise RuntimeError("Could not read output file metadata")

            # Extract duration and sample rate
            duration = float(dst_info.get('format', {}).get('duration', 0))
            if duration <= 0:
                raise RuntimeError("Invalid duration in output file")

            audio_streams = [s for s in dst_info.get('streams', [])
                             if s.get('codec_type') == 'audio']
            if not audio_streams:
                raise RuntimeError("No audio stream in output file")

            sample_rate = int(audio_streams[0].get('sample_rate', 16000))
            if sample_rate not in {8000, 16000, 44100, 48000}:
                sample_rate = 16000  # Fallback to standard Whisper sample rate

            self.progress_tracker.update(3, f"Audio extracted: {duration:.1f}s")
            return duration, sample_rate

        except subprocess.TimeoutExpired:
            raise RuntimeError("Audio extraction timed out (5 minutes)")
        except Exception as e:
            # Clean up partial output file if exists
            if dst_wav.exists():
                try:
                    dst_wav.unlink()
                except:
                    pass
            raise RuntimeError(f"Audio extraction failed: {str(e)}")

    def transcribe(self, audio_path: Path, language: Optional[str]) -> Dict[str, Any]:
        """Transcribe audio with Whisper, handling both standard and faster-whisper"""
        self.progress_tracker.update(3, "Starting transcription...")
        
        model = self.load_model()
        lang = None if (language in (None, "", LanguageCode.AUTO.value)) else language

        # Get duration for progress estimation
        duration = float(ffprobe_info(audio_path).get('format', {}).get('duration', 0))
        estimated_time = estimate_transcription_time(duration, self.model_name)
        print(f"[+] Transcribing ({estimated_time:.1f}s estimated)...")
        self.progress_tracker.update(3, f"Transcribing audio ({estimated_time:.1f}s estimated)...")

        if self._processor == "faster":
            # faster-whisper API
            segments, info = model.transcribe(
                str(audio_path),
                language=lang,
                beam_size=5,
                vad_filter=True,
                word_timestamps=True
            )

            # Convert to standard whisper format
            result = {
                "segments": [],
                "language": info.language,
                "text": ""
            }

            for segment in segments:
                seg_dict = {
                    "id": segment.id,
                    "seek": segment.seek,
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text,
                    "words": []
                }

                if segment.words:
                    for word in segment.words:
                        seg_dict["words"].append({
                            "word": word.word,
                            "start": word.start,
                            "end": word.end,
                            "probability": word.probability
                        })

                result["segments"].append(seg_dict)
                result["text"] += segment.text

            self.progress_tracker.update(4, f"Transcription complete: {len(result['segments'])} segments")
            return result
        else:
            # Standard whisper API
            result = model.transcribe(
                str(audio_path),
                language=lang,
                word_timestamps=True,
                verbose=False
            )
            self.progress_tracker.update(4, f"Transcription complete: {len(result.get('segments', []))} segments")
            return result

    def write_srt(self, segments: List[Dict[str, Any]], cfg: SubtitleConfig, out_path: Path):
        """Write subtitles in SRT format with proper line breaks"""
        with out_path.open('w', encoding='utf-8-sig') as f:
            for i, seg in enumerate(segments, 1):
                start, end = float(seg['start']), float(seg['end'])
                text = str(seg['text']).strip().replace('\n', ' ')
                lines = smart_split(text, cfg.max_chars_per_line)

                f.write(f"{i}\n")
                f.write(f"{srt_time(start)} --> {srt_time(end)}\n")
                f.write("\n".join(lines) + "\n\n")

    def write_vtt(self, segments: List[Dict[str, Any]], cfg: SubtitleConfig, out_path: Path):
        """Write subtitles in WebVTT format"""
        with out_path.open('w', encoding='utf-8-sig') as f:
            f.write("WEBVTT\n\n")
            for i, seg in enumerate(segments, 1):
                start, end = float(seg['start']), float(seg['end'])
                text = str(seg['text']).strip().replace('\n', ' ')
                lines = smart_split(text, cfg.max_chars_per_line)

                f.write(f"{i}\n")
                f.write(f"{vtt_time(start)} --> {vtt_time(end)}\n")
                f.write("\n".join(lines) + "\n\n")

    def write_ass(self, segments: List[Dict[str, Any]], cfg: SubtitleConfig, out_path: Path):
        """Write subtitles in Advanced SubStation Alpha format with full styling"""
        with out_path.open('w', encoding='utf-8-sig') as f:
            # ASS header with style definition
            f.write("[Script Info]\n")
            f.write("Title: Generated Subtitles\n")
            f.write("ScriptType: v4.00+\n")
            f.write("WrapStyle: {}\n".format(cfg.wrap_style))
            f.write("ScaledBorderAndShadow: yes\n")
            f.write("PlayResX: 384\n")
            f.write("PlayResY: 288\n\n")

            f.write("[V4+ Styles]\n")
            f.write("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, ")
            f.write("Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, ")
            f.write("Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")

            # Fixed background color format
            alpha_hex = hex(int(cfg.background_opacity * 255))[2:].zfill(2).upper()

            f.write("Style: Default,{},{},{},{},{},{},0,0,0,0,100,100,0,0,1,{},{},{},{},{},{},1\n\n".format(
                cfg.font_name,
                cfg.font_size,
                hex_to_ass(cfg.font_color),
                hex_to_ass(cfg.font_color),
                hex_to_ass(cfg.outline_color),
                hex_to_ass(cfg.background_color, alpha_hex),
                cfg.outline_width,
                cfg.shadow_offset,
                cfg.alignment,
                cfg.margin_horizontal,
                cfg.margin_horizontal,
                cfg.margin_vertical
            ))

            f.write("[Events]\n")
            f.write("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")

            for seg in segments:
                start, end = float(seg['start']), float(seg['end'])
                text = str(seg['text']).strip().replace('\n', ' ')
                lines = smart_split(text, cfg.max_chars_per_line)
                joined_text = "\\N".join(lines)  # ASS uses \N for line breaks

                f.write("Dialogue: 0,{},{},".format(
                    vtt_time(start).replace('.', ','),
                    vtt_time(end).replace('.', ',')
                ))
                f.write("Default,,0,0,0,," + joined_text + "\n")

    def write_txt(self, segments: List[Dict[str, Any]], include_ts: bool, out_path: Path):
        """Write plain text transcript with optional timestamps"""
        with out_path.open('w', encoding='utf-8') as f:
            if include_ts:
                for seg in segments:
                    f.write(f"[{srt_time(seg['start'])} --> {srt_time(seg['end'])}] {seg['text'].strip()}\n")
            else:
                full_text = " ".join(seg['text'].strip() for seg in segments)
                f.write(full_text)

    def embed_subs(self, video: Path, subtitle_path: Path, out_video: Path, cfg: SubtitleConfig):
        """Embed subtitles into video using advanced ffmpeg filters"""
        self.progress_tracker.update(4, "Embedding subtitles into video...")
        
        # Determine subtitle format
        sub_ext = subtitle_path.suffix.lower()

        if sub_ext == '.ass':
            # ASS subtitles retain their styling
            vf = f"subtitles='{subtitle_path.as_posix()}'"
        else:
            # Convert other formats to styled ASS
            style = (
                f"FontName={cfg.font_name},"
                f"FontSize={cfg.font_size},"
                f"PrimaryColour={hex_to_ass(cfg.font_color)},"
                f"BackColour={hex_to_ass(cfg.background_color, hex(int(cfg.background_opacity * 255))[2:].zfill(2))},"
                f"OutlineColour={hex_to_ass(cfg.outline_color)},"
                f"BorderStyle=1,"
                f"Outline={cfg.outline_width},"
                f"Shadow={cfg.shadow_offset},"
                f"Alignment={cfg.alignment},"
                f"MarginV={cfg.margin_vertical},"
                f"MarginL={cfg.margin_horizontal},"
                f"MarginR={cfg.margin_horizontal}"
            )
            # Escape path for subtitle filter
            escaped_path = str(subtitle_path).replace('\\', '\\\\').replace(':', '\\:')
            vf = f"subtitles='{escaped_path}':force_style='{style}'"

        cmd = [
            "ffmpeg", "-y", "-i", str(video),
            "-vf", vf,
            "-c:v", "libx264", "-preset", "medium", "-crf", "23",
            "-c:a", "copy",
            "-movflags", "+faststart",
            str(out_video)
        ]

        print("[+] Embedding subtitles into video...")
        run(cmd, capture=False, timeout=900)  # 15 minute timeout for video processing

    def process_one(self, src: Path, out_dir: Path, formats: List[str], style: SubtitleStyle,
                    language: str, include_ts: bool) -> Dict[str, str]:
        """Process a single media file"""
        self.progress_tracker.update(1, f"Starting processing: {src.name}")
        
        out_dir.mkdir(parents=True, exist_ok=True)
        cfg = style_preset(style)

        # Create output filename based on source name and timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        stem = f"{src.stem}_{timestamp}" if src.stem else timestamp

        # Temporary files
        tmp_audio = out_dir / f"{stem}.tmp.wav"

        print(f"[+] Processing: {src.name}")

        # Verify media has audio
        info = ffprobe_info(src)
        has_audio = any(s.get('codec_type') == 'audio' for s in info.get('streams', [])) if info else True

        if not has_audio and is_video(src):
            raise RuntimeError("Video file has no audio track.")

        # Prepare audio
        audio_path = None
        if is_video(src):
            try:
                duration, _ = self.extract_audio(src, tmp_audio)
                print(f"[+] Extracted audio: {duration:.1f}s")
                audio_path = tmp_audio
            except Exception as e:
                raise RuntimeError(f"Audio extraction failed: {str(e)}")
        else:
            audio_path = src

        # Transcribe
        try:
            result = self.transcribe(audio_path, language)
            segments = result.get('segments', [])

            if not segments:
                raise RuntimeError("No speech detected in audio.")

            print(
                f"[+] Transcription complete: {len(segments)} segments, language: {result.get('language', 'unknown')}")
        except Exception as e:
            raise RuntimeError(f"Transcription failed: {str(e)}")
        finally:
            # Cleanup temp audio
            if tmp_audio.exists():
                try:
                    tmp_audio.unlink()
                except:
                    pass

        self.progress_tracker.update(4, "Generating subtitle files...")

        # Generate requested output formats
        written = {}

        if 'srt' in formats:
            srt_path = out_dir / f"{stem}.srt"
            self.write_srt(segments, cfg, srt_path)
            written['srt'] = str(srt_path)

        if 'vtt' in formats:
            vtt_path = out_dir / f"{stem}.vtt"
            self.write_vtt(segments, cfg, vtt_path)
            written['vtt'] = str(vtt_path)

        if 'ass' in formats:
            ass_path = out_dir / f"{stem}.ass"
            self.write_ass(segments, cfg, ass_path)
            written['ass'] = str(ass_path)

        if 'txt' in formats:
            txt_path = out_dir / f"{stem}.txt"
            self.write_txt(segments, include_ts, txt_path)
            written['txt'] = str(txt_path)

        if 'video' in formats and is_video(src):
            out_video = out_dir / f"{stem}_subtitled{src.suffix.lower()}"

            # Use ASS if available, otherwise SRT
            subtitle_path = written.get('ass') or written.get('srt')
            if not subtitle_path:
                srt_path = out_dir / f"{stem}.srt"
                self.write_srt(segments, cfg, srt_path)
                written['srt'] = str(srt_path)
                subtitle_path = srt_path

            try:
                self.embed_subs(src, Path(subtitle_path), out_video, cfg)
                written['video'] = str(out_video)
            except Exception as e:
                raise RuntimeError(f"Failed to embed subtitles: {str(e)}")

        self.progress_tracker.update(5, "Processing complete!")
        return written


# -----------------------------
# CLI Interface
# -----------------------------

def parse_args() -> argparse.Namespace:
    """Parse command line arguments with improved help and defaults"""
    p = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""Offline Professional Subtitle Generator (no API)

Features:
- Local processing with Whisper AI
- Multiple output formats (SRT, VTT, ASS, TXT, embedded video)
- Advanced subtitle styling
- GPU acceleration support
- Batch processing
""")

    p.add_argument('-i', '--input', required=True,
                   help='Input file or folder path')
    p.add_argument('-o', '--output', default='output',
                   help='Output directory (default: output)')
    p.add_argument('--formats', default='srt,video',
                   help='Comma-separated output formats: video,srt,vtt,ass,txt (default: srt,video)')
    p.add_argument('--style', default='default',
                   choices=[e.value for e in SubtitleStyle],
                   help='Subtitle style preset (default: default)')
    p.add_argument('--language', default='auto',
                   help='Language code (auto, en, tr, etc.) or "auto" for detection')
    p.add_argument('--include-timestamps', action='store_true',
                   help='Include timestamps in TXT output')
    p.add_argument('--model', default='base',
                   choices=['tiny', 'base', 'small', 'medium', 'large'],
                   help='Whisper model size (default: base)')
    p.add_argument('--no-audio-enhance', action='store_true',
                   help='Disable audio enhancement filters')
    p.add_argument('--batch', action='store_true',
                   help='Process all media files in input folder')
    p.add_argument('--gpu', action='store_true',
                   help='Enable GPU acceleration if available')
    p.add_argument('--overwrite', action='store_true',
                   help='Overwrite existing output files')
    p.add_argument('--verbose', action='store_true',
                   help='Enable verbose output')

    return p.parse_args()


def collect_inputs(inp: Path, batch: bool) -> List[Path]:
    """Collect input files with validation"""
    if not inp.exists():
        raise SystemExit(f"Error: Input path not found: {inp}")

    if batch:
        if not inp.is_dir():
            raise SystemExit("Error: --batch requires a directory input")

        files = []
        for ext in ALLOWED_EXTS:
            files.extend(inp.rglob(f'*{ext}'))

        if not files:
            raise SystemExit(f"No supported media files found in: {inp}")

        return sorted(files)
    else:
        if inp.is_dir():
            files = [f for f in inp.iterdir() if f.suffix.lower() in ALLOWED_EXTS]
            if not files:
                raise SystemExit(f"No media files in directory. Use --batch for folders: {inp}")
            return [files[0]]

        if inp.suffix.lower() not in ALLOWED_EXTS:
            raise SystemExit(f"Unsupported file type: {inp.suffix}")

        return [inp]


def signal_handler(signum, frame):
    """Handle interrupt signals gracefully"""
    print("\n[!] Processing interrupted by user")
    sys.exit(1)


def main():
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    args = parse_args()

    # Validate formats
    formats = [f.strip().lower() for f in args.formats.split(',') if f.strip()]
    valid_formats = {'video', 'srt', 'vtt', 'ass', 'txt'}
    for f in formats:
        if f not in valid_formats:
            raise SystemExit(f"Invalid format: {f}. Choose from: {', '.join(valid_formats)}")

    # Initialize generator
    try:
        gen = OfflineSubtitleGenerator(
            whisper_model=args.model,
            enhance_audio=not args.no_audio_enhance,
            use_gpu=args.gpu
        )
    except Exception as e:
        raise SystemExit(f"Initialization failed: {str(e)}")

    # Process files
    input_files = collect_inputs(Path(args.input), args.batch)
    output_dir = Path(args.output)

    print(f"\n[i] Processing {len(input_files)} file(s) with {args.model} model")
    print(f"[i] Output formats: {', '.join(formats)}")
    print(f"[i] Style: {args.style}")
    print(f"[i] Language: {args.language}\n")
    print(f"[i] GPU acceleration: {'enabled' if args.gpu else 'disabled'}")
    print(f"[i] Audio enhancement: {'enabled' if not args.no_audio_enhance else 'disabled'}")

    success_count = 0
    start_time = datetime.now()

    for idx, src in enumerate(input_files, 1):
        try:
            print(f"\n=== Processing {idx}/{len(input_files)}: {src.name} ===")
            file_start_time = datetime.now()

            outputs = gen.process_one(
                src=src,
                out_dir=output_dir,
                formats=formats,
                style=SubtitleStyle(args.style),
                language=args.language,
                include_ts=args.include_timestamps
            )

            file_duration = datetime.now() - file_start_time
            print(f"[+] File processed in {file_duration.total_seconds():.1f} seconds")

            for fmt, path in outputs.items():
                print(f"  → {fmt.upper()}: {Path(path).name}")

            success_count += 1

        except Exception as e:
            print(f"\n[!] Failed to process {src.name}: {str(e)}", file=sys.stderr)
            continue

    total_duration = datetime.now() - start_time
    print(f"\nCompleted: {success_count} of {len(input_files)} files processed successfully")
    print(f"Total processing time: {total_duration.total_seconds():.1f} seconds")
    print(f"Output directory: {output_dir.absolute()}")


if __name__ == '__main__':
    main()