"""
Whisper Manager voor Magic Time Studio
Beheert zowel standaard Whisper als Faster Whisper
"""

import os
from typing import Optional, Dict, Any
from enum import Enum

class WhisperType(Enum):
    """Whisper type enumeratie"""
    STANDARD = "standard"
    FAST = "fast"

class WhisperManager:
    """Centrale Whisper beheerder"""
    
    def __init__(self):
        self.current_type = WhisperType.FAST
        self.current_model = "tiny"  # Default naar tiny
        self.is_initialized = False
        self.available_models = {
            WhisperType.STANDARD: ["tiny", "base", "small", "medium", "large", "large-v3"],
            WhisperType.FAST: ["tiny", "base", "small", "medium", "large", "large-v3"]
        }
        self.available_types = ["standard", "fast"]
        self.gpu_device = "cuda"  # Default GPU device
        self.compute_type = "float16"  # Default compute type
    
    def initialize(self, whisper_type: str, model: str) -> bool:
        """Initialiseer Whisper met opgegeven type en model"""
        try:
            # Converteer string naar enum
            if whisper_type.lower() == "fast":
                self.current_type = WhisperType.FAST
            else:
                self.current_type = WhisperType.STANDARD
            
            # Zorg ervoor dat het juiste model wordt gebruikt
            if model not in self.available_models[self.current_type]:
                print(f"⚠️ Model {model} niet beschikbaar voor {whisper_type}, gebruik tiny")
                model = "tiny"
            
            self.current_model = model
            
            # Controleer GPU status voor betere informatie
            print("🔍 Controleer GPU status...")
            gpu_status = self.check_gpu_status()
            
            # Probeer automatisch CUDA te forceren voor betere prestaties
            if whisper_type.lower() == "fast":
                cuda_available = self.force_cuda()
                # CUDA status wordt niet meer getoond om spam te voorkomen
            
            self.is_initialized = True
            
            print(f"✅ Whisper geïnitialiseerd: {self.current_type.value} - {self.current_model}")
            print(f"🔧 Device: {self.gpu_device}, Compute Type: {self.compute_type}")
            
            # Toon GPU samenvatting
            if gpu_status["available"]:
                print(f"🎯 GPU: {gpu_status['name']} ({gpu_status['memory_total']:.1f} GB) - {gpu_status['device'].upper()}")
            else:
                print("⚠️ GPU: Niet beschikbaar - CPU wordt gebruikt")
            
            return True
            
        except Exception as e:
            print(f"❌ Fout bij initialiseren Whisper: {e}")
            return False
    
    def get_current_type(self) -> str:
        """Krijg huidige Whisper type"""
        return self.current_type.value
    
    def get_current_model(self) -> str:
        """Krijg huidige model"""
        return self.current_model
    
    def is_model_loaded(self) -> bool:
        """Controleer of model geladen is"""
        return self.is_initialized
    
    def get_available_models(self, whisper_type: str = None) -> list:
        """Krijg beschikbare modellen voor opgegeven type"""
        if whisper_type is None:
            whisper_type = self.current_type
        elif whisper_type.lower() == "fast":
            whisper_type = WhisperType.FAST
        else:
            whisper_type = WhisperType.STANDARD
        
        return self.available_models.get(whisper_type, [])
    
    def get_available_whisper_types(self) -> list:
        """Krijg beschikbare Whisper types"""
        return self.available_types
    
    def get_gpu_device(self) -> str:
        """Krijg huidige GPU device"""
        return self.gpu_device
    
    def set_gpu_device(self, device: str) -> bool:
        """Stel GPU device in"""
        try:
            if device.lower() in ["cuda", "cpu"]:
                self.gpu_device = device.lower()
                
                # Als CUDA wordt geselecteerd, probeer het te forceren
                if device.lower() == "cuda":
                    cuda_available = self.force_cuda()
                    if not cuda_available:
                        self.gpu_device = "cpu"
                # GPU device status wordt niet meer getoond om spam te voorkomen
                
                return True
            else:
                print(f"⚠️ Ongeldige device: {device}, gebruik cuda of cpu")
                return False
        except Exception as e:
            print(f"❌ Fout bij instellen GPU device: {e}")
            return False
    
    def get_compute_type(self) -> str:
        """Krijg huidige compute type"""
        return self.compute_type
    
    def set_compute_type(self, compute_type: str) -> bool:
        """Stel compute type in"""
        try:
            valid_types = ["float16", "float32", "int8"]
            if compute_type.lower() in valid_types:
                self.compute_type = compute_type.lower()
                
                # Als float16 wordt geselecteerd, probeer CUDA te forceren voor betere prestaties
                if compute_type.lower() == "float16":
                    if self.gpu_device == "cuda":
                        self.force_cuda()
                # Compute type status wordt niet meer getoond om spam te voorkomen
                
                return True
            else:
                print(f"⚠️ Ongeldig compute type: {compute_type}, gebruik {', '.join(valid_types)}")
                return False
        except Exception as e:
            print(f"❌ Fout bij instellen compute type: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """Krijg model informatie"""
        return {
            "type": self.current_type.value,
            "model": self.current_model,
            "is_loaded": self.is_initialized,
            "gpu_device": self.gpu_device,
            "compute_type": self.compute_type
        }
    
    def force_cuda(self) -> bool:
        """Forceer CUDA gebruik"""
        try:
            # Controleer of CUDA beschikbaar is
            import torch
            if torch.cuda.is_available():
                # GPU informatie wordt niet meer getoond om spam te voorkomen
                self.gpu_device = "cuda"
                return True
            else:
                if not hasattr(self, '_cuda_checked') or not self._cuda_checked:
                    print("❌ CUDA niet beschikbaar - GPU versnelling niet mogelijk")
                    self._cuda_checked = True
                self.gpu_device = "cpu"
                return False
        except ImportError:
            if not hasattr(self, '_cuda_checked') or not self._cuda_checked:
                print("❌ PyTorch niet beschikbaar - kan CUDA niet controleren")
                self._cuda_checked = True
            self.gpu_device = "cpu"
            return False
    
    def check_gpu_status(self) -> Dict[str, Any]:
        """Controleer GPU status voor monitoring panel"""
        try:
            gpu_info = {
                "available": False,
                "device": "cpu",
                "name": "N/A",
                "memory_total": 0,
                "memory_used": 0,
                "memory_free": 0,
                "utilization": 0,
                "temperature": 0
            }
            
            # Probeer NVIDIA GPU via pynvml
            try:
                import pynvml
                pynvml.nvmlInit()
                device_count = pynvml.nvmlDeviceGetCount()
                
                if device_count > 0:
                    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                    name = pynvml.nvmlDeviceGetName(handle)
                    if isinstance(name, bytes):
                        name = name.decode('utf-8')
                    
                    memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                    utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
                    
                    # Probeer temperatuur op te halen
                    try:
                        temperature = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
                    except:
                        temperature = 0
                    
                    gpu_info.update({
                        "available": True,
                        "device": "cuda",
                        "name": name,
                        "memory_total": memory_info.total / (1024**3),  # GB
                        "memory_used": memory_info.used / (1024**3),   # GB
                        "memory_free": memory_info.free / (1024**3),   # GB
                        "utilization": utilization.gpu,
                        "temperature": temperature
                    })
                    
                    # NVIDIA GPU info wordt niet meer getoond om spam te voorkomen
                    pass
                    
            except ImportError:
                print("⚠️ pynvml niet beschikbaar, gebruik PyTorch fallback")
            except Exception as e:
                print(f"⚠️ Fout bij pynvml: {e}")
            
            # Fallback naar PyTorch CUDA
            if not gpu_info["available"]:
                try:
                    import torch
                    if torch.cuda.is_available():
                        gpu_info.update({
                            "available": True,
                            "device": "cuda",
                            "name": torch.cuda.get_device_name(0),
                            "memory_total": torch.cuda.get_device_properties(0).total_memory / (1024**3),
                            "memory_used": (torch.cuda.get_device_properties(0).total_memory - torch.cuda.memory_reserved(0)) / (1024**3),
                            "memory_free": torch.cuda.memory_reserved(0) / (1024**3)
                        })
                        
                        # PyTorch CUDA info wordt niet meer getoond om spam te voorkomen
                        
                        # Probeer automatisch CUDA te forceren
                        if self.gpu_device == "cuda":
                            self.force_cuda()
                    else:
                        if not hasattr(self, '_pytorch_cuda_not_available_printed'):
                            print("⚠️ PyTorch CUDA niet beschikbaar")
                            self._pytorch_cuda_not_available_printed = True
                except ImportError:
                    if not hasattr(self, '_pytorch_import_error_printed'):
                        print("⚠️ PyTorch niet beschikbaar")
                        self._pytorch_import_error_printed = True
                except Exception as e:
                    if not hasattr(self, '_pytorch_cuda_error_printed'):
                        print(f"⚠️ Fout bij PyTorch CUDA: {e}")
                        self._pytorch_cuda_error_printed = True
            
            # GPU samenvatting wordt niet meer getoond om spam te voorkomen
            pass
            
            return gpu_info
            
        except Exception as e:
            print(f"❌ Fout bij GPU status controle: {e}")
            return {
                "available": False,
                "device": "cpu",
                "name": "Error",
                "memory_total": 0,
                "memory_used": 0,
                "memory_free": 0,
                "utilization": 0,
                "temperature": 0
            }

# Globale instantie
whisper_manager = WhisperManager()
