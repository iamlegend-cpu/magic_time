"""
Audio Processor Module voor Magic Time Studio
Handelt audio extractie en verwerking af
"""

import os
import tempfile
import subprocess
from typing import Optional

class AudioProcessor:
    """Audio verwerking module"""
    
    def __init__(self, processing_thread):
        self.processing_thread = processing_thread
        self.temp_dir = tempfile.gettempdir()
        self.settings = None  # Instellingen worden later ingesteld
    
    def set_settings(self, settings: dict):
        """Stel instellingen in voor de audio processor"""
        print(f"🔍 [DEBUG] AudioProcessor.set_settings: Ontvangen instellingen = {settings}")
        self.settings = settings
        print(f"🔍 [DEBUG] AudioProcessor.set_settings: self.settings ingesteld = {self.settings}")
    
    def extract_audio(self, video_path: str) -> Optional[str]:
        """Extraheer audio uit video bestand met FFmpeg"""
        try:
            print(f"🔍 [DEBUG] AudioProcessor.extract_audio: self.settings = {self.settings}")
            
            # Maak temp bestand voor audio
            video_name = os.path.splitext(os.path.basename(video_path))[0]
            audio_path = os.path.join(self.temp_dir, f"{video_name}_audio.wav")
            
            print(f"🔊 Audio extractie: {video_path} -> {audio_path}")
            
            # Update status
            self.processing_thread.status_updated.emit("🔊 Audio wordt geëxtraheerd...")
            self.processing_thread.progress_updated.emit(25.0, "Audio extractie...")
            
            # FFmpeg commando voor audio extractie
            cmd = [
                "ffmpeg", "-i", video_path,
                "-vn",  # Geen video
                "-acodec", "pcm_s16le",  # PCM 16-bit
                "-ar", "16000",  # 16kHz sample rate (optimaal voor Whisper)
                "-ac", "1",  # Mono
                "-y",  # Overschrijf bestaand bestand
                audio_path
            ]
            
            # Voer FFmpeg uit
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0 and os.path.exists(audio_path):
                print(f"✅ Audio succesvol geëxtraheerd: {audio_path}")
                return audio_path
            else:
                print(f"❌ FFmpeg fout: {result.stderr}")
                self.processing_thread.error_occurred.emit(f"Audio extractie gefaald: {result.stderr}")
                return None
            
        except subprocess.TimeoutExpired:
            print("❌ Audio extractie timeout (5 minuten)")
            self.processing_thread.error_occurred.emit("Audio extractie timeout")
            return None
        except Exception as e:
            print(f"❌ Fout bij audio extractie: {e}")
            self.processing_thread.error_occurred.emit(f"Audio extractie gefaald: {e}")
            return None
    
    def cleanup_audio(self, audio_path: str):
        """Ruim audio bestand op"""
        try:
            if os.path.exists(audio_path):
                os.remove(audio_path)
                print(f"🧹 Audio bestand opgeruimd: {audio_path}")
        except Exception as e:
            print(f"⚠️ Kon audio bestand niet opruimen: {e}")
    
    def get_audio_duration(self, audio_path: str) -> Optional[float]:
        """Bepaal de duur van een audio bestand met FFprobe"""
        try:
            cmd = [
                "ffprobe", "-v", "quiet",
                "-show_entries", "format=duration",
                "-of", "csv=p=0",
                audio_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                duration = float(result.stdout.strip())
                return duration
            else:
                print(f"❌ FFprobe fout: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"❌ Fout bij bepalen audio duur: {e}")
            return None
