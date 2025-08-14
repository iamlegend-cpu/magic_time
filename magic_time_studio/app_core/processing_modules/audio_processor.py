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
        
        # Bepaal FFmpeg pad
        self.ffmpeg_path = self._find_ffmpeg()
        self.ffprobe_path = self._find_ffprobe()
        
        print(f"🔍 [DEBUG] AudioProcessor: ffmpeg_path = {self.ffmpeg_path}")
        print(f"🔍 [DEBUG] AudioProcessor: ffprobe_path = {self.ffprobe_path}")
    
    def _find_ffmpeg(self) -> str:
        """Zoek naar FFmpeg executable"""
        # Mogelijke locaties voor FFmpeg
        possible_paths = [
            # PyInstaller bundle (root directory)
            "ffmpeg.exe",
            # Assets directory in bundle
            "assets/ffmpeg.exe",
            # Relatieve paden voor development
            "assets/ffmpeg.exe",
            # Absolute paden voor development
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "ffmpeg.exe"),
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "assets", "ffmpeg.exe"),
            # Als het in PATH staat
            "ffmpeg"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                print(f"✅ FFmpeg gevonden: {path}")
                return path
        
        print("⚠️ FFmpeg niet gevonden, probeer 'ffmpeg' commando")
        return "ffmpeg"
    
    def _find_ffprobe(self) -> str:
        """Zoek naar FFprobe executable"""
        # Mogelijke locaties voor FFprobe
        possible_paths = [
            # PyInstaller bundle (root directory)
            "ffprobe.exe",
            # Assets directory in bundle
            "assets/ffprobe.exe",
            # Relatieve paden voor development
            "assets/ffprobe.exe",
            # Absolute paden voor development
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "ffprobe.exe"),
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "assets", "ffprobe.exe"),
            # Als het in PATH staat
            "ffprobe"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                print(f"✅ FFprobe gevonden: {path}")
                return path
        
        # Als ffprobe niet bestaat, gebruik ffmpeg als fallback
        print("⚠️ FFprobe niet gevonden, gebruik FFmpeg als fallback")
        return self.ffmpeg_path
    
    def set_settings(self, settings: dict):
        """Stel instellingen in voor de audio processor"""
        print(f"🔍 [DEBUG] AudioProcessor.set_settings: Ontvangen instellingen = {settings}")
        self.settings = settings
        print(f"🔍 [DEBUG] AudioProcessor.set_settings: self.settings ingesteld = {self.settings}")
    
    def extract_audio(self, video_path: str) -> Optional[str]:
        """Extraheer audio uit video bestand met FFmpeg"""
        try:
            print(f"🔍 [DEBUG] AudioProcessor.extract_audio: self.settings = {self.settings}")
            
            # Genereer audio bestandsnaam
            video_name = os.path.splitext(os.path.basename(video_path))[0]
            # Verwijder alle speciale karakters en spaties, maak het zo eenvoudig mogelijk
            safe_video_name = "".join(c for c in video_name if c.isalnum())
            # Gebruik een zeer korte naam om problemen te voorkomen
            audio_filename = f"test.wav"
            
            # Gebruik altijd temp directory om problemen met spaties in pad namen te voorkomen
            import tempfile
            temp_dir = tempfile.gettempdir()
            audio_path = os.path.join(temp_dir, audio_filename)
            print(f"🔧 Gebruik temp directory voor audio: {temp_dir}")
            print(f"🔧 Zeer eenvoudige bestandsnaam: {audio_filename}")
            
            print(f"🔊 Audio extractie: {video_path} -> {audio_path}")
            
            # Update status (geen dubbele berichten)
            self.processing_thread.progress_updated.emit(25.0, "Audio extractie...")
            
            # FFmpeg commando voor audio extractie
            cmd = [
                self.ffmpeg_path, "-i", video_path,
                "-vn",  # Geen video
                "-acodec", "pcm_s16le",  # PCM 16-bit
                "-ar", "16000",  # 16kHz sample rate (optimaal voor Whisper)
                "-ac", "1",  # Mono
                "-y",  # Overschrijf bestaand bestand
                audio_path
            ]
            
            # Voer FFmpeg uit
            print(f"🔍 FFmpeg commando: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0 and os.path.exists(audio_path):
                # Controleer of bestand toegankelijk is
                try:
                    # Test of bestand kan worden geopend
                    with open(audio_path, 'rb') as test_file:
                        test_file.read(1024)  # Lees eerste 1KB
                    
                    # Controleer bestandsgrootte
                    file_size = os.path.getsize(audio_path)
                    if file_size > 0:
                        # Normaliseer het pad
                        audio_path = os.path.abspath(os.path.normpath(audio_path))
                        print(f"✅ Audio succesvol geëxtraheerd: {audio_path}")
                        print(f"🔍 Bestandsgrootte: {file_size} bytes")
                        print(f"🔍 Genormaliseerd pad: {audio_path}")
                        return audio_path
                    else:
                        print(f"❌ Audio bestand is leeg: {audio_path}")
                        return None
                        
                except Exception as e:
                    print(f"❌ Audio bestand niet toegankelijk: {e}")
                    return None
            else:
                error_msg = f"FFmpeg fout (code {result.returncode}): {result.stderr}"
                if result.stdout:
                    error_msg += f"\nOutput: {result.stdout}"
                print(f"❌ {error_msg}")
                self.processing_thread.error_occurred.emit(f"Audio extractie gefaald: {error_msg}")
                return None
            
        except subprocess.TimeoutExpired:
            print("❌ Audio extractie timeout (5 minuten)")
            self.processing_thread.error_occurred.emit("Audio extractie timeout - probeer een kortere video of controleer FFmpeg")
            return None
        except FileNotFoundError as e:
            error_msg = f"FFmpeg niet gevonden: {e}"
            print(f"❌ {error_msg}")
            print(f"🔍 Gezochte FFmpeg pad: {self.ffmpeg_path}")
            self.processing_thread.error_occurred.emit(f"Audio extractie gefaald: {error_msg}")
            return None
        except Exception as e:
            print(f"❌ Fout bij audio extractie: {e}")
            self.processing_thread.error_occurred.emit(f"Audio extractie gefaald: {e}")
            return None
    
    def get_audio_path(self, video_path: str) -> str:
        """Genereer het pad naar het audio bestand voor een video bestand"""
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        # Verwijder alle speciale karakters en spaties, maak het zo eenvoudig mogelijk
        safe_video_name = "".join(c for c in video_name if c.isalnum())
        # Gebruik een zeer korte naam om problemen te voorkomen
        audio_filename = f"audio_{safe_video_name[:10]}.wav"
        
        # Zoek eerst in temp directory
        import tempfile
        temp_dir = tempfile.gettempdir()
        temp_audio_path = os.path.join(temp_dir, audio_filename)
        if os.path.exists(temp_audio_path):
            return temp_audio_path
        
        # Als het bestand niet bestaat in temp directory, return het verwachte pad
        return temp_audio_path
    
    def cleanup_audio_by_video(self, video_path: str) -> bool:
        """Verwijder het audio bestand dat bij een video bestand hoort"""
        try:
            audio_path = self.get_audio_path(video_path)
            if os.path.exists(audio_path):
                os.remove(audio_path)
                print(f"🧹 Audio bestand opgeruimd: {audio_path}")
                return True
            return False
        except Exception as e:
            print(f"⚠️ Fout bij opruimen audio bestand: {e}")
            return False
    
    def get_audio_duration(self, audio_path: str) -> Optional[float]:
        """Bepaal de duur van een audio bestand"""
        try:
            # Probeer eerst met FFprobe als het beschikbaar is
            if (os.path.exists(self.ffprobe_path) and 
                not self.ffprobe_path.endswith("ffmpeg") and
                self.ffprobe_path != self.ffmpeg_path and
                "ffprobe" in self.ffprobe_path):
                
                cmd = [
                    self.ffprobe_path, "-v", "quiet",
                    "-show_entries", "format=duration",
                    "-of", "csv=p=0",
                    audio_path
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    duration = float(result.stdout.strip())
                    return duration
                else:
                    print(f"⚠️ FFprobe fout: {result.stderr}")
            
            # Fallback: gebruik FFmpeg om duur te bepalen
            print(f"🔍 Gebruik FFmpeg om audio duur te bepalen: {audio_path}")
            cmd = [
                self.ffmpeg_path, "-i", audio_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0 and result.stderr:
                # Parse duration uit FFmpeg output
                import re
                duration_match = re.search(r'Duration: (\d{2}):(\d{2}):(\d{2})\.(\d{2})', result.stderr)
                if duration_match:
                    hours = int(duration_match.group(1))
                    minutes = int(duration_match.group(2))
                    seconds = int(duration_match.group(3))
                    centiseconds = int(duration_match.group(4))
                    
                    total_seconds = hours * 3600 + minutes * 60 + seconds + centiseconds / 100
                    print(f"✅ Audio duur bepaald: {total_seconds:.2f} seconden")
                    return total_seconds
                else:
                    print(f"⚠️ Kon duration niet parsen uit FFmpeg output")
            else:
                print(f"⚠️ FFmpeg commando succesvol maar geen output")
            
            print("⚠️ Kon audio duur niet bepalen")
            return None
                
        except Exception as e:
            print(f"❌ Fout bij bepalen audio duur: {e}")
            return None
