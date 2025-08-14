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
        self._stop_timeout = 2  # Verlaagd van 5 naar 2 seconden voor snellere stop
    
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
                # Wacht maximaal 0.5 seconde voor processing thread (verlaagd van 1s)
                if hasattr(self.processing_thread, 'wait'):
                    self.processing_thread.wait(500)
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
        
        # Wacht tot alle stop threads klaar zijn (max 0.5 seconde, verlaagd van 1s)
        for thread in stop_threads:
            thread.join(timeout=0.5)
        
        # Ruim temp bestanden op
        cleanup_thread = threading.Thread(target=self._cleanup_temp_files, daemon=True)
        cleanup_thread.start()
        cleanup_thread.join(timeout=0.25)  # Verlaagd van 0.5s
        
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
        
        # Als er nog steeds processen draaien, forceer stop (verlaagd van 2s naar 1s)
        if elapsed_time > 1.0:
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
    
    def emergency_cuda_stop(self):
        """Noodstop voor CUDA/GPU processen - gebruik alleen als laatste redmiddel"""
        try:
            print("🚨 EMERGENCY CUDA STOP - Forceer stop van alle GPU processen...")
            
            # Stop alle CUDA context
            self._stop_cuda_context()
            
            # Forceer GPU reset via nvidia-smi
            try:
                import subprocess
                
                # Windows
                if os.name == 'nt':
                    try:
                        # Forceer GPU reset
                        result = subprocess.run([
                            'nvidia-smi', '--gpu-reset', '--force'
                        ], capture_output=True, text=True, timeout=10)
                        
                        if result.returncode == 0:
                            print("✅ GPU emergency reset succesvol")
                        else:
                            print(f"⚠️ GPU emergency reset gefaald: {result.stderr}")
                            
                    except FileNotFoundError:
                        print("⚠️ nvidia-smi niet gevonden")
                    except subprocess.TimeoutExpired:
                        print("⚠️ GPU emergency reset timeout")
                
                # Linux/Mac
                else:
                    try:
                        # Forceer GPU reset
                        result = subprocess.run([
                            'nvidia-smi', '--gpu-reset', '--force'
                        ], capture_output=True, text=True, timeout=10)
                        
                        if result.returncode == 0:
                            print("✅ GPU emergency reset succesvol")
                        else:
                            print(f"⚠️ GPU emergency reset gefaald: {result.stderr}")
                            
                    except FileNotFoundError:
                        print("⚠️ nvidia-smi niet gevonden")
                    except subprocess.TimeoutExpired:
                        print("⚠️ GPU emergency reset timeout")
                        
            except Exception as e:
                print(f"⚠️ Fout bij GPU emergency reset: {e}")
            
            # Forceer stop van alle GPU processen
            self._force_kill_gpu_processes()
            
            # Als laatste redmiddel: forceer stop van alle Python processen
            try:
                import psutil
                for proc in psutil.process_iter(['pid', 'name']):
                    try:
                        if proc.info['name'] == 'python.exe' or proc.info['name'] == 'python':
                            print(f"💀 Emergency stop Python proces: {proc.info['pid']}")
                            proc.kill()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
            except Exception as e:
                print(f"⚠️ Fout bij emergency Python stop: {e}")
            
            print("🚨 Emergency CUDA stop voltooid")
            
        except Exception as e:
            print(f"⚠️ Fout bij emergency CUDA stop: {e}")
    
    def get_gpu_status(self):
        """Haal GPU status op voor debugging"""
        try:
            import subprocess
            
            # Probeer nvidia-smi te gebruiken
            try:
                result = subprocess.run([
                    'nvidia-smi', '--query-gpu=index,name,memory.used,memory.total,utilization.gpu', 
                    '--format=csv,noheader,nounits'
                ], capture_output=True, text=True, timeout=5)
                
                if result.returncode == 0:
                    gpu_info = result.stdout.strip().split('\n')
                    print("🎮 GPU Status:")
                    for line in gpu_info:
                        if line.strip():
                            parts = line.split(', ')
                            if len(parts) >= 5:
                                gpu_id, name, mem_used, mem_total, util = parts
                                print(f"  GPU {gpu_id}: {name} - Memory: {mem_used}/{mem_total}MB - Util: {util}%")
                else:
                    print("⚠️ Kon GPU status niet ophalen")
                    
            except FileNotFoundError:
                print("⚠️ nvidia-smi niet gevonden")
            except subprocess.TimeoutExpired:
                print("⚠️ GPU status timeout")
                
        except Exception as e:
            print(f"⚠️ Fout bij ophalen GPU status: {e}")
    
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
    
    def _stop_whisper_processes(self):
        """Stop alle Whisper processen die mogelijk vastlopen - inclusief CUDA/GPU processen"""
        try:
            print("🛑 StopManager: Stop alle Whisper processen (inclusief CUDA/GPU)...")
            
            # Stop CUDA context eerst om GPU processen te bevrijden
            self._stop_cuda_context()
            
            # Zoek naar Python processen die Whisper gebruiken
            try:
                import psutil
                for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                    try:
                        cmdline = proc.info['cmdline']
                        if cmdline and any('whisper' in arg.lower() for arg in cmdline):
                            print(f"🛑 StopManager: Stop Whisper proces {proc.info['pid']}")
                            proc.terminate()
                            proc.wait(timeout=2)  # Verlaagd van 5s naar 2s
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
    
    def _stop_cuda_context(self):
        """Stop CUDA context om GPU processen te bevrijden"""
        try:
            print("🛑 StopManager: Stop CUDA context...")
            
            # Probeer PyTorch CUDA context te stoppen
            try:
                import torch
                if torch.cuda.is_available():
                    print("🛑 StopManager: PyTorch CUDA beschikbaar, stop context...")
                    
                    # Stop alle CUDA streams
                    if hasattr(torch.cuda, 'empty_cache'):
                        torch.cuda.empty_cache()
                        print("✅ CUDA cache geleegd")
                    
                    # Reset CUDA device
                    if hasattr(torch.cuda, 'reset_peak_memory_stats'):
                        torch.cuda.reset_peak_memory_stats()
                        print("✅ CUDA memory stats gereset")
                    
                    # Synchroniseer CUDA
                    if hasattr(torch.cuda, 'synchronize'):
                        torch.cuda.synchronize()
                        print("✅ CUDA gesynchroniseerd")
                        
            except ImportError:
                print("🛑 StopManager: PyTorch niet beschikbaar")
            except Exception as e:
                print(f"⚠️ StopManager: Fout bij PyTorch CUDA stop: {e}")
            
            # Probeer TensorFlow CUDA context te stoppen
            try:
                import tensorflow as tf
                if hasattr(tf, 'config') and hasattr(tf.config, 'experimental'):
                    print("🛑 StopManager: TensorFlow beschikbaar, stop CUDA context...")
                    # TensorFlow heeft geen directe CUDA stop methode, maar we kunnen memory vrijmaken
                    if hasattr(tf, 'keras'):
                        tf.keras.backend.clear_session()
                        print("✅ TensorFlow Keras sessie opgeruimd")
            except ImportError:
                print("🛑 StopManager: TensorFlow niet beschikbaar")
            except Exception as e:
                print(f"⚠️ StopManager: Fout bij TensorFlow stop: {e}")
            
            # Forceer CUDA processen te stoppen via nvidia-smi (als beschikbaar)
            self._force_stop_cuda_processes()
            
        except Exception as e:
            print(f"⚠️ StopManager: Fout bij stoppen CUDA context: {e}")
    
    def _force_stop_cuda_processes(self):
        """Forceer stop van CUDA/GPU processen via nvidia-smi"""
        try:
            print("🛑 StopManager: Forceer stop van CUDA/GPU processen...")
            
            # Probeer nvidia-smi te gebruiken om GPU processen te stoppen
            try:
                import subprocess
                
                # Windows: gebruik nvidia-smi
                if os.name == 'nt':
                    # Zoek naar nvidia-smi in PATH
                    try:
                        # Stop alle processen op alle GPU's
                        result = subprocess.run([
                            'nvidia-smi', '--gpu-reset'
                        ], capture_output=True, text=True, timeout=5)
                        
                        if result.returncode == 0:
                            print("✅ GPU reset succesvol uitgevoerd")
                        else:
                            print(f"⚠️ GPU reset gefaald: {result.stderr}")
                            
                    except FileNotFoundError:
                        print("⚠️ nvidia-smi niet gevonden in PATH")
                    except subprocess.TimeoutExpired:
                        print("⚠️ GPU reset timeout, forceer stop...")
                        # Forceer stop van alle Python processen die GPU gebruiken
                        self._force_kill_gpu_processes()
                
                # Linux/Mac: gebruik nvidia-smi
                else:
                    try:
                        # Stop alle processen op alle GPU's
                        result = subprocess.run([
                            'nvidia-smi', '--gpu-reset'
                        ], capture_output=True, text=True, timeout=5)
                        
                        if result.returncode == 0:
                            print("✅ GPU reset succesvol uitgevoerd")
                        else:
                            print(f"⚠️ GPU reset gefaald: {result.stderr}")
                            
                    except FileNotFoundError:
                        print("⚠️ nvidia-smi niet gevonden in PATH")
                    except subprocess.TimeoutExpired:
                        print("⚠️ GPU reset timeout, forceer stop...")
                        # Forceer stop van alle Python processen die GPU gebruiken
                        self._force_kill_gpu_processes()
                        
            except Exception as e:
                print(f"⚠️ Fout bij nvidia-smi: {e}")
                # Fallback: forceer stop van GPU processen
                self._force_kill_gpu_processes()
                
        except Exception as e:
            print(f"⚠️ StopManager: Fout bij forceer stop CUDA processen: {e}")
    
    def _force_kill_gpu_processes(self):
        """Forceer stop van alle processen die GPU gebruiken"""
        try:
            print("💀 StopManager: Forceer stop van GPU processen...")
            
            import psutil
            
            # Zoek naar processen die GPU gebruiken
            gpu_keywords = [
                "cuda", "gpu", "nvidia", "whisper", "faster-whisper", 
                "torch", "tensorflow", "tensorrt", "cudnn"
            ]
            
            killed_count = 0
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = proc.info.get('cmdline', [])
                    cmdline_str = " ".join(cmdline).lower()
                    
                    # Check of proces GPU keywords bevat
                    if any(keyword in cmdline_str for keyword in gpu_keywords):
                        print(f"💀 Forceer stop GPU proces: {proc.info['pid']} - {proc.info['name']}")
                        proc.kill()
                        killed_count += 1
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            
            print(f"✅ {killed_count} GPU processen geforceerd gestopt")
            
        except Exception as e:
            print(f"⚠️ StopManager: Fout bij forceer stop GPU processen: {e}")
    
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


# Globale instantie
stop_manager = StopManager() 