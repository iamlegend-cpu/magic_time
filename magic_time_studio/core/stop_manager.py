"""
Stop Manager voor Magic Time Studio
Beheert het stoppen van processen en opruimen van temp bestanden
"""

import os
import tempfile
import glob
import shutil
import subprocess
from typing import List, Optional

# Absolute imports in plaats van relative imports
try:
    from magic_time_studio.core.config import config_manager
except ImportError:
    # Fallback voor directe import
    import sys
    sys.path.append('..')
    from core.config import config_manager


class StopManager:
    """Manager voor het stoppen van processen en opruimen van temp bestanden"""
    
    def __init__(self):
        self.processing_thread = None
        self.main_window = None
    
    def set_processing_thread(self, thread):
        """Stel de processing thread in"""
        self.processing_thread = thread
    
    def set_main_window(self, window):
        """Stel de main window in"""
        self.main_window = window
    
    def stop_all_processes(self):
        """Stop alle processen en ruim temp bestanden op"""
        print("🛑 StopManager: Stop alle processen...")
        
        # Stop processing thread
        if self.processing_thread and self.processing_thread.isRunning():
            print("🛑 Stop processing thread...")
            self.processing_thread.stop()
            self.processing_thread.wait(5000)  # Wacht max 5 seconden
        
        # Stop Whisper processen
        self._stop_whisper_processes()
        
        # Stop LibreTranslate processen
        self._stop_libretranslate_processes()
        
        # Stop FFmpeg processen
        self._stop_ffmpeg_processes()
        
        # Ruim temp bestanden op
        self._cleanup_temp_files()
        
        # Reset processing_active flag
        if self.main_window:
            self.main_window.processing_active = False
        
        print("✅ StopManager: Alle processen gestopt en temp bestanden opgeruimd")
    
    def _stop_whisper_processes(self):
        """Stop Whisper processen"""
        try:
            import whisper
            if hasattr(whisper, 'model_cache'):
                print("🗑️ Ruim Whisper model cache op...")
                whisper.model_cache.clear()
        except Exception as e:
            print(f"⚠️ Kon Whisper cache niet opruimen: {e}")
        
        # Stop Whisper subprocessen
        self._stop_subprocesses_by_keywords(["whisper", "python"])
    
    def _stop_libretranslate_processes(self):
        """Stop LibreTranslate processen"""
        try:
            import requests
            # Probeer LibreTranslate te stoppen als het draait
            translator_url = config_manager.get_env("LIBRETRANSLATE_SERVER", "100.90.127.78:5000")
            if translator_url:
                try:
                    response = requests.get(f"http://{translator_url}/health", timeout=2)
                    if response.status_code == 200:
                        print("🛑 LibreTranslate is actief, maar kan niet gestopt worden via API")
                except:
                    pass  # LibreTranslate draait niet of is niet bereikbaar
        except Exception as e:
            print(f"⚠️ Kon LibreTranslate status niet controleren: {e}")
        
        # Stop LibreTranslate subprocessen
        self._stop_subprocesses_by_keywords(["libretranslate", "translate"])
    
    def _stop_ffmpeg_processes(self):
        """Stop FFmpeg processen"""
        self._stop_subprocesses_by_keywords(["ffmpeg"])
    
    def _stop_subprocesses_by_keywords(self, keywords: List[str]):
        """Stop subprocessen op basis van keywords in command line"""
        try:
            import psutil
            current_process = psutil.Process()
            
            # Zoek naar child processen van de huidige applicatie
            children = current_process.children(recursive=True)
            for child in children:
                try:
                    # Controleer of het een relevant proces is
                    cmdline = child.cmdline()
                    cmdline_str = " ".join(cmdline).lower()
                    
                    if any(keyword in cmdline_str for keyword in keywords):
                        print(f"🛑 Stop subproces: {child.pid} - {' '.join(cmdline[:3])}")
                        child.terminate()
                        try:
                            child.wait(timeout=3)  # Wacht 3 seconden
                        except psutil.TimeoutExpired:
                            print(f"⚠️ Forceer stop van proces {child.pid}")
                            child.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass  # Proces bestaat niet meer of geen toegang
        except Exception as e:
            print(f"⚠️ Kon subprocessen niet stoppen: {e}")
    
    def _cleanup_temp_files(self):
        """Ruim alle temp bestanden op"""
        print("🗑️ Ruim temp bestanden op...")
        
        # Temp directory
        temp_dir = tempfile.gettempdir()
        
        # Zoek naar temp bestanden van Magic Time Studio
        patterns = [
            os.path.join(temp_dir, "*_audio.wav"),
            os.path.join(temp_dir, "*_audio.mp3"),
            os.path.join(temp_dir, "magic_time_*"),
            os.path.join(temp_dir, "whisper_*"),
            os.path.join(temp_dir, "libretranslate_*"),
            os.path.join(temp_dir, "ffmpeg_*"),
        ]
        
        cleaned_count = 0
        for pattern in patterns:
            try:
                files = glob.glob(pattern)
                for file_path in files:
                    try:
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                            print(f"🗑️ Verwijderd: {os.path.basename(file_path)}")
                            cleaned_count += 1
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path, ignore_errors=True)
                            print(f"🗑️ Verwijderd map: {os.path.basename(file_path)}")
                            cleaned_count += 1
                    except Exception as e:
                        print(f"⚠️ Kon bestand niet verwijderen {file_path}: {e}")
            except Exception as e:
                print(f"⚠️ Fout bij zoeken naar pattern {pattern}: {e}")
        
        # Zoek ook in de huidige directory naar temp bestanden
        current_dir_patterns = [
            "*_audio.wav",
            "*_audio.mp3",
            "temp_*",
            "whisper_*",
        ]
        
        for pattern in current_dir_patterns:
            try:
                files = glob.glob(pattern)
                for file_path in files:
                    try:
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                            print(f"🗑️ Verwijderd uit huidige directory: {file_path}")
                            cleaned_count += 1
                    except Exception as e:
                        print(f"⚠️ Kon bestand niet verwijderen {file_path}: {e}")
            except Exception as e:
                print(f"⚠️ Fout bij zoeken naar pattern {pattern}: {e}")
        
        print(f"✅ {cleaned_count} temp bestanden opgeruimd")
    
    def force_kill_processes(self):
        """Forceer het stoppen van alle processen"""
        print("💀 Forceer stop van alle processen...")
        
        try:
            import psutil
            current_process = psutil.Process()
            
            # Zoek naar alle child processen
            children = current_process.children(recursive=True)
            for child in children:
                try:
                    cmdline = child.cmdline()
                    print(f"💀 Forceer stop van proces: {child.pid} - {' '.join(cmdline[:3])}")
                    child.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
        except Exception as e:
            print(f"⚠️ Kon processen niet forceer stoppen: {e}")


# Globale instantie
stop_manager = StopManager() 