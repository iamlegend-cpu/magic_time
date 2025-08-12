"""
Stop Manager voor Magic Time Studio
Beheert het stoppen van processen en opruimen van temp bestanden
"""

import os
import tempfile
import glob
import shutil
import subprocess
import time
import threading
from typing import List, Optional

# Lazy import om circulaire import te voorkomen
_config_manager = None

def _get_config_manager():
    """Lazy config manager import om circulaire import te voorkomen"""
    global _config_manager
    if _config_manager is None:
        try:
            from .config import config_manager
            _config_manager = config_manager
        except ImportError:
            # Fallback voor directe import
            import sys
            sys.path.append('..')
            try:
                from core.config import config_manager
                _config_manager = config_manager
            except ImportError:
                _config_manager = None
    return _config_manager


class StopManager:
    """Manager voor het stoppen van processen en opruimen van temp bestanden"""
    
    def __init__(self):
        self.processing_thread = None
        self.main_window = None
        self._stop_timeout = 5  # 5 seconden timeout voor stoppen
    
    def set_processing_thread(self, thread):
        """Stel de processing thread in"""
        self.processing_thread = thread
    
    def set_main_window(self, window):
        """Stel de main window in"""
        self.main_window = window
    
    def stop_all_processes(self):
        """Stop alle processen en ruim temp bestanden op binnen 5 seconden"""
        print("🛑 StopManager: Stop alle processen binnen 5 seconden...")
        start_time = time.time()
        
        # Stop processing thread eerst
        if self.processing_thread and hasattr(self.processing_thread, 'isRunning') and self.processing_thread.isRunning():
            print("🛑 Stop processing thread...")
            try:
                self.processing_thread.stop()
                # Wacht maximaal 1 seconde voor processing thread
                if hasattr(self.processing_thread, 'wait'):
                    self.processing_thread.wait(1000)
                print("✅ Processing thread gestopt")
            except Exception as e:
                print(f"⚠️ Fout bij stoppen processing thread: {e}")
        
        # Stop alle processen parallel voor snellere stop
        stop_threads = []
        
        # Stop Whisper processen in aparte thread
        whisper_thread = threading.Thread(target=self._stop_whisper_processes, daemon=True)
        whisper_thread.start()
        stop_threads.append(whisper_thread)
        
        # Stop LibreTranslate processen in aparte thread
        libretranslate_thread = threading.Thread(target=self._stop_libretranslate_processes, daemon=True)
        libretranslate_thread.start()
        stop_threads.append(libretranslate_thread)
        
        # Stop FFmpeg processen in aparte thread
        ffmpeg_thread = threading.Thread(target=self._stop_ffmpeg_processes, daemon=True)
        ffmpeg_thread.start()
        stop_threads.append(ffmpeg_thread)
        
        # Wacht tot alle stop threads klaar zijn (max 1 seconde)
        for thread in stop_threads:
            thread.join(timeout=1.0)
        
        # Ruim temp bestanden op
        cleanup_thread = threading.Thread(target=self._cleanup_temp_files, daemon=True)
        cleanup_thread.start()
        cleanup_thread.join(timeout=0.5)
        
        # Reset processing_active flag
        if self.main_window:
            try:
                self.main_window.processing_active = False
                # Roep ook de processing_finished methode aan als die bestaat
                if hasattr(self.main_window, 'processing_finished'):
                    self.main_window.processing_finished()
            except Exception as e:
                print(f"⚠️ Fout bij resetten main window: {e}")
        
        elapsed_time = time.time() - start_time
        print(f"✅ StopManager: Alle processen gestopt en temp bestanden opgeruimd in {elapsed_time:.1f}s")
        
        # Als er nog steeds processen draaien, forceer stop
        if elapsed_time > 2.0:
            print("⚠️ StopManager: Stop duurde te lang, forceer stop van resterende processen...")
            self.force_kill_processes()
        
        # Forceer stop van alle Python processen die nog draaien
        try:
            import psutil
            current_process = psutil.Process()
            children = current_process.children(recursive=True)
            for child in children:
                try:
                    cmdline = " ".join(child.cmdline()).lower()
                    if any(keyword in cmdline for keyword in ["ffmpeg", "whisper", "python", "faster-whisper"]):
                        print(f"💀 Forceer stop van subproces: {child.pid} - {cmdline[:50]}")
                        child.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        except Exception as e:
            print(f"⚠️ Fout bij forceer stop van subprocessen: {e}")
        
        # Forceer stop van alle processen met relevante keywords
        try:
            import psutil
            keywords = ["whisper", "faster-whisper", "ffmpeg", "libretranslate", "translate", "python"]
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = proc.info.get('cmdline', [])
                    cmdline_str = " ".join(cmdline).lower()
                    
                    if any(keyword in cmdline_str for keyword in keywords):
                        print(f"💀 Forceer stop van proces: {proc.info['pid']} - {proc.info['name']}")
                        proc.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
        except Exception as e:
            print(f"⚠️ Fout bij forceer stop van processen: {e}")
    
    def _stop_whisper_processes(self):
        """Stop alle Whisper processen die mogelijk vastlopen"""
        try:
            print("🛑 StopManager: Stop alle Whisper processen...")
            
            # Zoek naar Python processen die Whisper gebruiken
            try:
                import psutil
                for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                    try:
                        cmdline = proc.info['cmdline']
                        if cmdline and any('whisper' in arg.lower() for arg in cmdline):
                            print(f"🛑 StopManager: Stop Whisper proces {proc.info['pid']}")
                            proc.terminate()
                            proc.wait(timeout=5)
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                        pass
            except ImportError:
                print("🛑 StopManager: psutil niet beschikbaar, gebruik alternatieve methode")
                # Alternatieve methode zonder psutil
                try:
                    if os.name == 'nt':  # Windows
                        os.system('taskkill /f /im python.exe 2>nul')
                    else:  # Linux/Mac
                        os.system('pkill -f whisper 2>/dev/null')
                except:
                    pass
            
            print("✅ StopManager: Whisper processen gestopt")
            
        except Exception as e:
            print(f"⚠️ StopManager: Fout bij stoppen Whisper processen: {e}")
    
    def force_stop_whisper(self):
        """Forceer stop van alle Whisper processen"""
        try:
            print("🛑 StopManager: Forceer stop van alle Whisper processen...")
            
            # Gebruik agressievere methode
            try:
                import psutil
                for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                    try:
                        cmdline = proc.info['cmdline']
                        if cmdline and any('whisper' in arg.lower() for arg in cmdline):
                            print(f"🛑 StopManager: Forceer stop Whisper proces {proc.info['pid']}")
                            proc.kill()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
            except ImportError:
                # Alternatieve methode
                if os.name == 'nt':  # Windows
                    os.system('taskkill /f /im python.exe /f 2>nul')
                else:  # Linux/Mac
                    os.system('pkill -9 -f whisper 2>/dev/null')
            
            print("✅ StopManager: Alle Whisper processen geforceerd gestopt")
            
        except Exception as e:
            print(f"⚠️ StopManager: Fout bij geforceerd stoppen: {e}")
    
    def _stop_libretranslate_processes(self):
        """Stop LibreTranslate processen"""
        try:
            import requests
            # Probeer LibreTranslate te stoppen als het draait
            config_mgr = _get_config_manager()
            translator_url = config_mgr.get_env("LIBRETRANSLATE_SERVER", "") if config_mgr else ""
            if translator_url:
                try:
                    response = requests.get(f"http://{translator_url}/health", timeout=1)
                    if response.status_code == 200:
                        print("🛑 LibreTranslate is actief, maar kan niet gestopt worden via API")
                except:
                    pass  # LibreTranslate draait niet of is niet bereikbaar
        except Exception as e:
            print(f"⚠️ Kon LibreTranslate status niet controleren: {e}")
        
        # Stop LibreTranslate subprocessen
        self._stop_subprocesses_by_keywords(["libretranslate", "translate"])
        self._force_stop_processes_by_keywords(["libretranslate", "translate"])
    
    def _stop_ffmpeg_processes(self):
        """Stop FFmpeg processen"""
        self._stop_subprocesses_by_keywords(["ffmpeg"])
        self._force_stop_processes_by_keywords(["ffmpeg"])
    
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
                            child.wait(timeout=1)  # Wacht 1 seconde
                        except psutil.TimeoutExpired:
                            print(f"⚠️ Forceer stop van proces {child.pid}")
                            child.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass  # Proces bestaat niet meer of geen toegang
        except Exception as e:
            print(f"⚠️ Kon subprocessen niet stoppen: {e}")
    
    def _force_stop_processes_by_keywords(self, keywords: List[str]):
        """Forceer stop van processen op basis van keywords"""
        try:
            import psutil
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = proc.info.get('cmdline', [])
                    cmdline_str = " ".join(cmdline).lower()
                    
                    if any(keyword in cmdline_str for keyword in keywords):
                        print(f"💀 Forceer stop van proces: {proc.info['pid']} - {proc.info['name']}")
                        proc.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
        except Exception as e:
            print(f"⚠️ Kon processen niet forceer stoppen: {e}")
    
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
            
            # Zoek ook naar processen met relevante keywords
            keywords = ["whisper", "faster-whisper", "ffmpeg", "libretranslate", "translate", "python"]
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = proc.info.get('cmdline', [])
                    cmdline_str = " ".join(cmdline).lower()
                    
                    if any(keyword in cmdline_str for keyword in keywords):
                        print(f"💀 Forceer stop van proces: {proc.info['pid']} - {proc.info['name']}")
                        proc.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
                    
        except Exception as e:
            print(f"⚠️ Kon processen niet forceer stoppen: {e}")


# Globale instantie
stop_manager = StopManager() 