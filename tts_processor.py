#!/usr/bin/env python3
"""
Multi-language TTS Video Processor
==================================

Extends the subtitle generator with TTS capabilities:
- Converts subtitles to speech in multiple languages
- Combines TTS audio with original video
- Embeds subtitles into final videos
- Supports multiple TTS engines (gTTS, edge-tts)
"""

import asyncio
import os
import tempfile
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import subprocess
import json
import time

# TTS imports
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

from pydub import AudioSegment
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip


class TTSEngine(str, Enum):
    GTTS = "gtts"
    EDGE_TTS = "edge_tts"


class SupportedLanguage(str, Enum):
    TURKISH = "tr"
    ENGLISH = "en"
    FRENCH = "fr"
    GERMAN = "de"
    SPANISH = "es"
    ITALIAN = "it"
    PORTUGUESE = "pt"
    RUSSIAN = "ru"
    JAPANESE = "ja"
    KOREAN = "ko"
    CHINESE = "zh"
    ARABIC = "ar"


@dataclass
class TTSConfig:
    engine: TTSEngine
    language: str
    voice: Optional[str] = None
    speed: float = 1.0
    pitch: float = 1.0
    volume: float = 1.0


@dataclass
class SubtitleSegment:
    start: float
    end: float
    text: str
    duration: float


class MultilingualTTSProcessor:
    def __init__(self, temp_dir: Optional[Path] = None):
        self.temp_dir = temp_dir or Path(tempfile.mkdtemp())
        self.temp_dir.mkdir(exist_ok=True)
        
        # Language configurations for different TTS engines
        self.language_configs = {
            TTSEngine.GTTS: {
                SupportedLanguage.TURKISH: TTSConfig(TTSEngine.GTTS, "tr"),
                SupportedLanguage.ENGLISH: TTSConfig(TTSEngine.GTTS, "en"),
                SupportedLanguage.FRENCH: TTSConfig(TTSEngine.GTTS, "fr"),
                SupportedLanguage.GERMAN: TTSConfig(TTSEngine.GTTS, "de"),
                SupportedLanguage.SPANISH: TTSConfig(TTSEngine.GTTS, "es"),
                SupportedLanguage.ITALIAN: TTSConfig(TTSEngine.GTTS, "it"),
                SupportedLanguage.PORTUGUESE: TTSConfig(TTSEngine.GTTS, "pt"),
                SupportedLanguage.RUSSIAN: TTSConfig(TTSEngine.GTTS, "ru"),
                SupportedLanguage.JAPANESE: TTSConfig(TTSEngine.GTTS, "ja"),
                SupportedLanguage.KOREAN: TTSConfig(TTSEngine.GTTS, "ko"),
                SupportedLanguage.CHINESE: TTSConfig(TTSEngine.GTTS, "zh"),
                SupportedLanguage.ARABIC: TTSConfig(TTSEngine.GTTS, "ar"),
            },
            TTSEngine.EDGE_TTS: {
                SupportedLanguage.TURKISH: TTSConfig(TTSEngine.EDGE_TTS, "tr-TR", "tr-TR-EmelNeural"),
                SupportedLanguage.ENGLISH: TTSConfig(TTSEngine.EDGE_TTS, "en-US", "en-US-JennyNeural"),
                SupportedLanguage.FRENCH: TTSConfig(TTSEngine.EDGE_TTS, "fr-FR", "fr-FR-DeniseNeural"),
                SupportedLanguage.GERMAN: TTSConfig(TTSEngine.EDGE_TTS, "de-DE", "de-DE-KatjaNeural"),
                SupportedLanguage.SPANISH: TTSConfig(TTSEngine.EDGE_TTS, "es-ES", "es-ES-ElviraNeural"),
                SupportedLanguage.ITALIAN: TTSConfig(TTSEngine.EDGE_TTS, "it-IT", "it-IT-ElsaNeural"),
                SupportedLanguage.PORTUGUESE: TTSConfig(TTSEngine.EDGE_TTS, "pt-BR", "pt-BR-FranciscaNeural"),
                SupportedLanguage.RUSSIAN: TTSConfig(TTSEngine.EDGE_TTS, "ru-RU", "ru-RU-SvetlanaNeural"),
                SupportedLanguage.JAPANESE: TTSConfig(TTSEngine.EDGE_TTS, "ja-JP", "ja-JP-NanamiNeural"),
                SupportedLanguage.KOREAN: TTSConfig(TTSEngine.EDGE_TTS, "ko-KR", "ko-KR-SunHiNeural"),
                SupportedLanguage.CHINESE: TTSConfig(TTSEngine.EDGE_TTS, "zh-CN", "zh-CN-XiaoxiaoNeural"),
                SupportedLanguage.ARABIC: TTSConfig(TTSEngine.EDGE_TTS, "ar-SA", "ar-SA-ZariyahNeural"),
            }
        }

    def parse_srt_file(self, srt_path: Path) -> List[SubtitleSegment]:
        """Parse SRT file and extract subtitle segments"""
        segments = []
        
        with open(srt_path, 'r', encoding='utf-8-sig') as f:
            content = f.read().strip()
        
        blocks = content.split('\n\n')
        
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) < 3:
                continue
                
            try:
                # Parse timestamp line (format: 00:00:01,000 --> 00:00:03,000)
                timestamp_line = lines[1]
                start_str, end_str = timestamp_line.split(' --> ')
                
                start = self._parse_timestamp(start_str)
                end = self._parse_timestamp(end_str)
                
                # Join text lines
                text = ' '.join(lines[2:]).strip()
                
                if text:  # Only add non-empty segments
                    segments.append(SubtitleSegment(
                        start=start,
                        end=end,
                        text=text,
                        duration=end - start
                    ))
                    
            except (ValueError, IndexError) as e:
                print(f"[WARNING] Skipping malformed subtitle block: {e}")
                continue
        
        return segments

    def _parse_timestamp(self, timestamp_str: str) -> float:
        """Convert SRT timestamp to seconds"""
        # Format: 00:00:01,000
        time_part, ms_part = timestamp_str.split(',')
        h, m, s = map(int, time_part.split(':'))
        ms = int(ms_part)
        
        return h * 3600 + m * 60 + s + ms / 1000.0

    async def generate_tts_audio(self, text: str, config: TTSConfig, output_path: Path) -> bool:
        """Generate TTS audio for given text"""
        try:
            if config.engine == TTSEngine.GTTS and GTTS_AVAILABLE:
                return await self._generate_gtts_audio(text, config, output_path)
            elif config.engine == TTSEngine.EDGE_TTS and EDGE_TTS_AVAILABLE:
                return await self._generate_edge_tts_audio(text, config, output_path)
            else:
                print(f"[ERROR] TTS engine {config.engine} not available")
                return False
                
        except Exception as e:
            print(f"[ERROR] TTS generation failed: {e}")
            return False

    async def _generate_gtts_audio(self, text: str, config: TTSConfig, output_path: Path) -> bool:
        """Generate audio using Google TTS"""
        try:
            tts = gTTS(text=text, lang=config.language, slow=False)
            tts.save(str(output_path))
            return True
        except Exception as e:
            print(f"[ERROR] gTTS failed: {e}")
            return False

    async def _generate_edge_tts_audio(self, text: str, config: TTSConfig, output_path: Path) -> bool:
        """Generate audio using Edge TTS"""
        try:
            communicate = edge_tts.Communicate(text, config.voice)
            await communicate.save(str(output_path))
            return True
        except Exception as e:
            print(f"[ERROR] Edge TTS failed: {e}")
            return False

    async def create_tts_audio_track(self, segments: List[SubtitleSegment], 
                                   config: TTSConfig, video_duration: float) -> Optional[Path]:
        """Create complete TTS audio track from subtitle segments"""
        print(f"[+] Generating TTS audio for {len(segments)} segments in {config.language}")
        
        # Create silent audio track with video duration
        silent_audio = AudioSegment.silent(duration=int(video_duration * 1000))
        
        # Generate TTS for each segment
        for i, segment in enumerate(segments):
            print(f"[+] Processing segment {i+1}/{len(segments)}: {segment.text[:50]}...")
            
            # Generate TTS audio for this segment
            segment_audio_path = self.temp_dir / f"segment_{i}_{config.language}.mp3"
            
            success = await self.generate_tts_audio(segment.text, config, segment_audio_path)
            if not success:
                print(f"[WARNING] Failed to generate TTS for segment {i+1}")
                continue
            
            try:
                # Load generated audio
                tts_audio = AudioSegment.from_file(str(segment_audio_path))
                
                # Adjust speed to fit segment duration
                target_duration = segment.duration * 1000  # Convert to milliseconds
                current_duration = len(tts_audio)
                
                if current_duration > 0:
                    speed_ratio = current_duration / target_duration
                    if speed_ratio > 0.5:  # Only adjust if not too extreme
                        tts_audio = tts_audio.speedup(playback_speed=speed_ratio)
                
                # Insert at correct position
                start_ms = int(segment.start * 1000)
                end_ms = int(segment.end * 1000)
                
                # Ensure audio fits within segment bounds
                if len(tts_audio) > (end_ms - start_ms):
                    tts_audio = tts_audio[:end_ms - start_ms]
                
                # Overlay on silent track
                silent_audio = silent_audio.overlay(tts_audio, position=start_ms)
                
                # Clean up temporary file
                segment_audio_path.unlink()
                
            except Exception as e:
                print(f"[WARNING] Failed to process segment {i+1}: {e}")
                continue
        
        # Export final audio track
        output_path = self.temp_dir / f"tts_audio_{config.language}.wav"
        silent_audio.export(str(output_path), format="wav")
        
        print(f"[+] TTS audio track created: {output_path}")
        return output_path

    def combine_video_with_tts(self, video_path: Path, tts_audio_path: Path, 
                              output_path: Path, mix_ratio: float = 0.3) -> bool:
        """Combine original video with TTS audio"""
        try:
            print(f"[+] Combining video with TTS audio...")
            
            # Load video and audio
            video = VideoFileClip(str(video_path))
            tts_audio = AudioFileClip(str(tts_audio_path))
            
            # Get original audio if exists
            original_audio = video.audio
            
            if original_audio:
                # Mix original audio (reduced volume) with TTS
                original_audio = original_audio.volumex(mix_ratio)
                tts_audio = tts_audio.volumex(1.0)
                
                # Ensure same duration
                min_duration = min(original_audio.duration, tts_audio.duration, video.duration)
                original_audio = original_audio.subclip(0, min_duration)
                tts_audio = tts_audio.subclip(0, min_duration)
                
                # Composite audio tracks
                final_audio = CompositeAudioClip([original_audio, tts_audio])
            else:
                # Use only TTS audio
                final_audio = tts_audio.subclip(0, video.duration)
            
            # Set audio to video
            final_video = video.set_audio(final_audio)
            
            # Write output
            final_video.write_videofile(
                str(output_path),
                codec='libx264',
                audio_codec='aac',
                temp_audiofile=str(self.temp_dir / 'temp_audio.m4a'),
                remove_temp=True,
                verbose=False,
                logger=None
            )
            
            # Clean up
            video.close()
            tts_audio.close()
            if original_audio:
                original_audio.close()
            final_audio.close()
            final_video.close()
            
            print(f"[+] Video with TTS created: {output_path}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to combine video with TTS: {e}")
            return False

    def embed_subtitles_to_video(self, video_path: Path, subtitle_path: Path, 
                                output_path: Path) -> bool:
        """Embed subtitles into video using ffmpeg"""
        try:
            print(f"[+] Embedding subtitles into video...")
            
            # Determine subtitle format and build filter
            sub_ext = subtitle_path.suffix.lower()
            
            if sub_ext == '.ass':
                vf = f"ass='{subtitle_path.as_posix()}'"
            else:  # SRT or VTT
                vf = f"subtitles='{subtitle_path.as_posix()}'"
            
            cmd = [
                "ffmpeg", "-y",
                "-i", str(video_path),
                "-vf", vf,
                "-c:v", "libx264", "-preset", "medium", "-crf", "23",
                "-c:a", "copy",
                "-movflags", "+faststart",
                str(output_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
            
            if result.returncode == 0:
                print(f"[+] Subtitles embedded successfully: {output_path}")
                return True
            else:
                print(f"[ERROR] FFmpeg failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Failed to embed subtitles: {e}")
            return False

    async def process_multilingual_video(self, video_path: Path, subtitle_path: Path,
                                       languages: List[str], output_dir: Path,
                                       embed_subtitles: bool = True,
                                       tts_engine: TTSEngine = TTSEngine.EDGE_TTS,
                                       original_audio_mix: float = 0.3) -> Dict[str, List[Path]]:
        """Process video for multiple languages"""
        
        results = {
            'tts_audio': [],
            'videos_with_tts': [],
            'videos_with_subtitles': [],
            'combined_videos': []
        }
        
        try:
            # Parse subtitles
            segments = self.parse_srt_file(subtitle_path)
            if not segments:
                print("[ERROR] No subtitle segments found")
                return results
            
            # Get video duration
            video = VideoFileClip(str(video_path))
            video_duration = video.duration
            video.close()
            
            print(f"[+] Processing {len(segments)} subtitle segments for {len(languages)} languages")
            
            # Process each language
            for lang_code in languages:
                try:
                    print(f"\n[+] Processing language: {lang_code}")
                    
                    # Get TTS configuration
                    if tts_engine not in self.language_configs:
                        print(f"[ERROR] TTS engine {tts_engine} not supported")
                        continue
                        
                    if lang_code not in self.language_configs[tts_engine]:
                        print(f"[ERROR] Language {lang_code} not supported for {tts_engine}")
                        continue
                    
                    config = self.language_configs[tts_engine][lang_code]
                    
                    # Create TTS audio track
                    tts_audio_path = await self.create_tts_audio_track(
                        segments, config, video_duration
                    )
                    
                    if not tts_audio_path or not tts_audio_path.exists():
                        print(f"[ERROR] Failed to create TTS audio for {lang_code}")
                        continue
                    
                    # Save TTS audio as MP3
                    tts_mp3_path = output_dir / f"tts_audio_{lang_code}.mp3"
                    audio = AudioSegment.from_wav(str(tts_audio_path))
                    audio.export(str(tts_mp3_path), format="mp3", bitrate="192k")
                    results['tts_audio'].append(tts_mp3_path)
                    
                    # Create video with TTS
                    video_with_tts_path = output_dir / f"video_with_tts_{lang_code}.mp4"
                    success = self.combine_video_with_tts(
                        video_path, tts_audio_path, video_with_tts_path, original_audio_mix
                    )
                    
                    if success:
                        results['videos_with_tts'].append(video_with_tts_path)
                        
                        # Embed subtitles if requested
                        if embed_subtitles:
                            video_with_subs_path = output_dir / f"final_video_{lang_code}_with_subtitles.mp4"
                            sub_success = self.embed_subtitles_to_video(
                                video_with_tts_path, subtitle_path, video_with_subs_path
                            )
                            
                            if sub_success:
                                results['videos_with_subtitles'].append(video_with_subs_path)
                                results['combined_videos'].append(video_with_subs_path)
                            else:
                                # If subtitle embedding fails, use video without subtitles
                                results['combined_videos'].append(video_with_tts_path)
                        else:
                            results['combined_videos'].append(video_with_tts_path)
                    
                    # Clean up temporary TTS audio
                    if tts_audio_path and tts_audio_path.exists():
                        tts_audio_path.unlink()
                        
                except Exception as e:
                    print(f"[ERROR] Failed to process language {lang_code}: {e}")
                    continue
            
            return results
            
        except Exception as e:
            print(f"[ERROR] Multilingual processing failed: {e}")
            return results

    def cleanup(self):
        """Clean up temporary files"""
        try:
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
        except Exception as e:
            print(f"[WARNING] Failed to clean up temp directory: {e}")

    def __del__(self):
        self.cleanup()


# Utility functions
def get_available_tts_engines() -> List[TTSEngine]:
    """Get list of available TTS engines"""
    engines = []
    if GTTS_AVAILABLE:
        engines.append(TTSEngine.GTTS)
    if EDGE_TTS_AVAILABLE:
        engines.append(TTSEngine.EDGE_TTS)
    return engines


def get_supported_languages(engine: TTSEngine) -> List[str]:
    """Get supported languages for a TTS engine"""
    processor = MultilingualTTSProcessor()
    if engine in processor.language_configs:
        return list(processor.language_configs[engine].keys())
    return []


async def main():
    """Test function"""
    # Example usage
    processor = MultilingualTTSProcessor()
    
    # Test with sample data
    video_path = Path("sample_video.mp4")
    subtitle_path = Path("sample_subtitles.srt")
    output_dir = Path("multilingual_output")
    output_dir.mkdir(exist_ok=True)
    
    languages = ["tr", "en", "fr", "de"]
    
    if video_path.exists() and subtitle_path.exists():
        results = await processor.process_multilingual_video(
            video_path=video_path,
            subtitle_path=subtitle_path,
            languages=languages,
            output_dir=output_dir,
            embed_subtitles=True,
            tts_engine=TTSEngine.EDGE_TTS
        )
        
        print("\n[+] Processing Results:")
        for category, files in results.items():
            print(f"  {category}: {len(files)} files")
            for file in files:
                print(f"    - {file}")
    
    processor.cleanup()


if __name__ == "__main__":
    asyncio.run(main())