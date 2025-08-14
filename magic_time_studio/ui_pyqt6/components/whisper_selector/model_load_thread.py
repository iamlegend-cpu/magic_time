"""
Model Load Thread voor Whisper Selector
Thread voor het laden van Whisper modellen in de achtergrond
"""

import time
import threading
from PyQt6.QtCore import QThread, pyqtSignal

# Import core modules
try:
    from core.logging import logger
except ImportError:
    logger = None


class ModelLoadThread(QThread):
    """Thread voor het laden van Whisper modellen"""
    
    # Signals
    finished = pyqtSignal(bool)  # success
    
    def __init__(self, whisper_type, model_name, device="cuda", compute_type="float16"):
        super().__init__()
        self.whisper_type = whisper_type
        self.model_name = model_name
        self.device = device
        self.compute_type = compute_type
    
    def run(self):
        """Voer model laden uit"""
        try:
            print(f"🔄 Start laden van {self.whisper_type} model: {self.model_name} op {self.device} ({self.compute_type})")
            
            # Import whisper manager
            try:
                from app_core.whisper_manager import whisper_manager
                if whisper_manager:
                    # Stel GPU instellingen in
                    whisper_manager.set_gpu_device(self.device)
                    whisper_manager.set_compute_type(self.compute_type)
                    
                    # Initialiseer whisper
                    success = whisper_manager.initialize(self.whisper_type, self.model_name)
                    
                    if success:
                        print(f"✅ {self.whisper_type} model {self.model_name} succesvol geladen op {self.device}")
                    else:
                        print(f"❌ {self.whisper_type} model {self.model_name} laden gefaald op {self.device}")
                    
                    self.finished.emit(success)
                    return
                    
            except ImportError:
                print("⚠️ Whisper manager niet beschikbaar")
            except Exception as e:
                print(f"❌ Fout bij whisper manager: {e}")
            
            # Fallback - probeer direct WhisperX
            if self.whisper_type == "whisperx":
                try:
                    from app_core.whisperx_processor import WhisperXProcessor
                    whisperx = WhisperXProcessor()
                    success = whisperx.initialize(self.model_name, self.device, self.compute_type)
                    
                    if success:
                        print(f"✅ WhisperX model {self.model_name} succesvol geladen op {self.device}")
                    else:
                        print(f"❌ WhisperX model {self.model_name} laden gefaald op {self.device}")
                    
                    self.finished.emit(success)
                    return
                    
                except ImportError:
                    print("⚠️ WhisperX niet beschikbaar")
                except Exception as e:
                    print(f"❌ Fout bij WhisperX: {e}")
            
            # Als alle methoden falen
            print(f"❌ Kon {self.whisper_type} model {self.model_name} niet laden")
            self.finished.emit(False)
            
        except Exception as e:
            print(f"❌ Fout bij laden model in thread: {e}")
            if logger:
                logger.log_debug(f"❌ Fout bij laden model in thread: {e}")
            self.finished.emit(False)
