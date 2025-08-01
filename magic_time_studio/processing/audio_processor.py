"""
Audio processor voor Magic Time Studio
Beheert audio extractie en verwerking met FFmpeg
"""

import os
import subprocess
import tempfile
from typing import Dict, Any, Optional, Tuple
from ..core.logging import logger
from ..core.config import config_manager
from ..core.utils import safe_basename

class AudioProcessor:
    """Processor voor audio extractie en verwerking"""
    
    def __init__(self):
        self.supported_audio_formats = ['.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg']
        self.supported_video_formats = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']
        self.ffmpeg_path = self._find_ffmpeg()
        
    def _find_ffmpeg(self) -> str:
        """Zoek FFmpeg executable"""
        # Probeer verschillende locaties
        possible_paths = [
            "ffmpeg",  # In PATH
            "ffmpeg.exe",  # Windows
            os.path.join(os.getcwd(), "ffmpeg.exe"),  # Huidige directory
            os.path.join(os.getcwd(), "assets", "ffmpeg.exe"),  # Assets directory
        ]
        
        for path in possible_paths:
            try:
                result = subprocess.run([path, "-version"], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    logger.log_debug(f"✅ FFmpeg gevonden: {path}")
                    return path
            except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
                continue
        
        logger.log_debug("❌ FFmpeg niet gevonden")
        return None
    
    def extract_audio_from_video(self, video_path: str, output_dir: Optional[str] = None,
                                audio_format: str = "wav") -> Dict[str, Any]:
        """Extracteer audio uit video bestand"""
        try:
            if not self.ffmpeg_path:
                return {"error": "FFmpeg niet gevonden"}
            
            if not os.path.exists(video_path):
                return {"error": "Video bestand niet gevonden"}
            
            # Bepaal output directory
            if output_dir is None:
                output_dir = os.path.dirname(video_path)
            
            os.makedirs(output_dir, exist_ok=True)
            
            # Genereer output bestandsnaam
            video_name = safe_basename(video_path)
            name_without_ext = os.path.splitext(video_name)[0]
            audio_filename = f"{name_without_ext}_audio.{audio_format}"
            audio_path = os.path.join(output_dir, audio_filename)
            
            logger.log_debug(f"🎵 Start audio extractie: {safe_basename(video_path)}")
            
            # FFmpeg commando voor audio extractie
            cmd = [
                self.ffmpeg_path,
                "-i", video_path,
                "-vn",  # Geen video
                "-acodec", "pcm_s16le" if audio_format == "wav" else "copy",
                "-ar", "16000",  # Sample rate voor Whisper
                "-ac", "1",  # Mono
                "-y",  # Overschrijf bestaand bestand
                audio_path
            ]
            
            # Voer FFmpeg uit
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0 and os.path.exists(audio_path):
                # Krijg bestandsgrootte
                file_size = os.path.getsize(audio_path)
                
                logger.log_debug(f"✅ Audio extractie voltooid: {safe_basename(audio_path)}")
                
                return {
                    "success": True,
                    "audio_path": audio_path,
                    "file_size": file_size,
                    "format": audio_format
                }
            else:
                error_msg = result.stderr if result.stderr else "Onbekende FFmpeg fout"
                logger.log_debug(f"❌ Audio extractie gefaald: {error_msg}")
                return {"error": f"FFmpeg fout: {error_msg}"}
                
        except subprocess.TimeoutExpired:
            logger.log_debug("❌ Audio extractie timeout")
            return {"error": "Timeout bij audio extractie"}
        except Exception as e:
            logger.log_debug(f"❌ Fout bij audio extractie: {e}")
            return {"error": str(e)}
    
    def get_video_info(self, video_path: str) -> Dict[str, Any]:
        """Krijg informatie over video bestand"""
        try:
            if not self.ffmpeg_path:
                return {"error": "FFmpeg niet gevonden"}
            
            if not os.path.exists(video_path):
                return {"error": "Video bestand niet gevonden"}
            
            # FFmpeg commando voor video info
            cmd = [
                self.ffmpeg_path,
                "-i", video_path,
                "-f", "null",
                "-"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            # Parse FFmpeg output voor informatie
            info = self._parse_ffmpeg_info(result.stderr)
            
            # Voeg bestandsgrootte toe
            if os.path.exists(video_path):
                info["file_size"] = os.path.getsize(video_path)
            
            logger.log_debug(f"📹 Video info opgehaald: {safe_basename(video_path)}")
            
            return {
                "success": True,
                "info": info
            }
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij ophalen video info: {e}")
            return {"error": str(e)}
    
    def _parse_ffmpeg_info(self, ffmpeg_output: str) -> Dict[str, Any]:
        """Parse FFmpeg output voor video/audio informatie"""
        info = {
            "duration": 0,
            "video_codec": "unknown",
            "audio_codec": "unknown",
            "resolution": "unknown",
            "fps": 0,
            "bitrate": 0
        }
        
        try:
            lines = ffmpeg_output.split('\n')
            
            for line in lines:
                line = line.strip()
                
                # Duration
                if "Duration:" in line:
                    duration_str = line.split("Duration:")[1].split(",")[0].strip()
                    info["duration"] = self._parse_duration(duration_str)
                
                # Video stream
                elif "Video:" in line:
                    video_parts = line.split("Video:")[1].split(",")
                    if video_parts:
                        info["video_codec"] = video_parts[0].strip()
                        
                        # Resolution
                        for part in video_parts:
                            if "x" in part and part.strip().split()[0].replace("x", "").isdigit():
                                info["resolution"] = part.strip().split()[0]
                                break
                        
                        # FPS
                        for part in video_parts:
                            if "fps" in part:
                                fps_str = part.strip().split()[0]
                                try:
                                    info["fps"] = float(fps_str)
                                except:
                                    pass
                                break
                
                # Audio stream
                elif "Audio:" in line:
                    audio_parts = line.split("Audio:")[1].split(",")
                    if audio_parts:
                        info["audio_codec"] = audio_parts[0].strip()
                
                # Bitrate
                elif "bitrate:" in line:
                    bitrate_str = line.split("bitrate:")[1].split()[0]
                    try:
                        info["bitrate"] = int(bitrate_str)
                    except:
                        pass
                        
        except Exception as e:
            logger.log_debug(f"❌ Fout bij parsen FFmpeg info: {e}")
        
        return info
    
    def _parse_duration(self, duration_str: str) -> float:
        """Parse duration string naar seconden"""
        try:
            # Format: HH:MM:SS.ms
            parts = duration_str.split(":")
            if len(parts) == 3:
                hours = int(parts[0])
                minutes = int(parts[1])
                seconds = float(parts[2])
                return hours * 3600 + minutes * 60 + seconds
        except:
            pass
        return 0
    
    def check_audio_quality(self, audio_path: str) -> Dict[str, Any]:
        """Controleer audio kwaliteit"""
        try:
            if not self.ffmpeg_path:
                return {"error": "FFmpeg niet gevonden"}
            
            if not os.path.exists(audio_path):
                return {"error": "Audio bestand niet gevonden"}
            
            # FFmpeg commando voor audio analyse
            cmd = [
                self.ffmpeg_path,
                "-i", audio_path,
                "-af", "volumedetect",
                "-f", "null",
                "-"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            # Parse volume detectie output
            volume_info = self._parse_volume_info(result.stderr)
            
            logger.log_debug(f"🔊 Audio kwaliteit gecontroleerd: {safe_basename(audio_path)}")
            
            return {
                "success": True,
                "quality": volume_info
            }
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij audio kwaliteit check: {e}")
            return {"error": str(e)}
    
    def _parse_volume_info(self, ffmpeg_output: str) -> Dict[str, Any]:
        """Parse volume detectie output"""
        info = {
            "mean_volume": 0,
            "max_volume": 0,
            "silence_duration": 0
        }
        
        try:
            lines = ffmpeg_output.split('\n')
            
            for line in lines:
                line = line.strip()
                
                if "mean_volume:" in line:
                    mean_str = line.split("mean_volume:")[1].split()[0]
                    try:
                        info["mean_volume"] = float(mean_str)
                    except:
                        pass
                
                elif "max_volume:" in line:
                    max_str = line.split("max_volume:")[1].split()[0]
                    try:
                        info["max_volume"] = float(max_str)
                    except:
                        pass
                        
        except Exception as e:
            logger.log_debug(f"❌ Fout bij parsen volume info: {e}")
        
        return info
    
    def is_video_file(self, file_path: str) -> bool:
        """Controleer of bestand een video is"""
        if not file_path:
            return False
        
        _, ext = os.path.splitext(file_path.lower())
        return ext in self.supported_video_formats
    
    def is_audio_file(self, file_path: str) -> bool:
        """Controleer of bestand een audio bestand is"""
        if not file_path:
            return False
        
        _, ext = os.path.splitext(file_path.lower())
        return ext in self.supported_audio_formats
    
    def get_supported_formats(self) -> Dict[str, list]:
        """Krijg ondersteunde formaten"""
        return {
            "video": self.supported_video_formats,
            "audio": self.supported_audio_formats
        }
    
    def is_ffmpeg_available(self) -> bool:
        """Controleer of FFmpeg beschikbaar is"""
        return self.ffmpeg_path is not None

# Globale audio processor instantie
audio_processor = AudioProcessor() 