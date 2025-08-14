"""
Whisper Manager voor Magic Time Studio
Alleen WhisperX ondersteund - voor maximale accuracy
"""

import os
from typing import Dict, Any

class WhisperManager:
    """Eenvoudige Whisper Manager - alleen WhisperX ondersteund"""
    
    def __init__(self):
        # Alleen WhisperX ondersteund
        self.current_type = "whisperx"
        self.current_model = None  # Geen model geladen bij start
        self.is_initialized = False
        
        # Beschikbare modellen
        self.available_models = ["tiny", "base", "small", "medium", "large", "large-v3", "large-v3-turbo"]
        self.available_types = ["whisperx"]  # Alleen WhisperX
        
        # Device instellingen
        self.gpu_device = "cuda"  # Default GPU
        self.compute_type = "float16"  # Default compute type
    
    def initialize(self, whisper_type: str, model: str = None) -> bool:
        """Initialiseer WhisperX (enige optie)"""
        try:
            # Controleer of het een ondersteund type is
            if whisper_type.lower() != "whisperx":
                print(f"❌ {whisper_type} wordt niet ondersteund. Alleen WhisperX is beschikbaar.")
                return False
            
            # Als geen model wordt opgegeven, initialiseer alleen de basis instellingen
            if model is None:
                self.is_initialized = True
                print(f"✅ WhisperX basis geïnitialiseerd (geen model geladen)")
                
                # Controleer GPU status
                gpu_available = self.check_cuda_availability()
                if gpu_available:
                    self.gpu_device = "cuda"
                    self.compute_type = "float16"
                else:
                    self.gpu_device = "cpu"
                    self.compute_type = "float32"
                
                return True
            
            # Controleer of het model beschikbaar is
            if model not in self.available_models:
                print(f"⚠️ Model {model} niet beschikbaar, gebruik large-v3")
                model = "large-v3"
            
            self.current_model = model
            self.is_initialized = True
            
            # Controleer GPU status
            gpu_available = self.check_cuda_availability()
            if gpu_available:
                self.gpu_device = "cuda"
                self.compute_type = "float16"
            else:
                self.gpu_device = "cpu"
                self.compute_type = "float32"
            
            print(f"✅ WhisperX geïnitialiseerd met model: {model}")
            return True
            
        except Exception as e:
            print(f"❌ Fout bij initialiseren WhisperX: {e}")
            return False
    
    def get_current_type(self) -> str:
        """Krijg huidige type (altijd whisperx)"""
        return self.current_type
    
    def get_current_model(self) -> str:
        """Krijg huidige model"""
        return self.current_model
    
    def is_model_loaded(self) -> bool:
        """Controleer of model geladen is"""
        return self.is_initialized
    
    def get_available_models(self, whisper_type: str = None) -> list:
        """Krijg beschikbare modellen"""
        return self.available_models
    
    def get_available_whisper_types(self) -> list:
        """Krijg beschikbare types (altijd alleen whisperx)"""
        return self.available_types
    
    def get_gpu_device(self) -> str:
        """Krijg huidige GPU device"""
        return self.gpu_device
    
    def set_gpu_device(self, device: str) -> bool:
        """Stel GPU device in"""
        if device.lower() in ["cuda", "cpu"]:
            self.gpu_device = device.lower()
            
            # Update compute type voor CPU
            if device.lower() == "cpu":
                self.compute_type = "float32"
            elif device.lower() == "cuda" and self.check_cuda_availability():
                self.compute_type = "float16"
            else:
                print("⚠️ CUDA niet beschikbaar, gebruik CPU")
                self.gpu_device = "cpu"
                self.compute_type = "float32"
            
            return True
        else:
            print(f"❌ Ongeldige device: {device}")
            return False
    
    def get_compute_type(self) -> str:
        """Krijg huidige compute type"""
        return self.compute_type
    
    def set_compute_type(self, compute_type: str) -> bool:
        """Stel compute type in"""
        valid_types = ["float16", "float32", "int8"]
        if compute_type.lower() in valid_types:
            self.compute_type = compute_type.lower()
            
            # Controleer of float16 mogelijk is
            if compute_type.lower() == "float16" and not self.check_cuda_availability():
                print("⚠️ float16 vereist CUDA, gebruik float32")
                self.compute_type = "float32"
            
            return True
        else:
            print(f"❌ Ongeldig compute type: {compute_type}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """Krijg model informatie"""
        return {
            "type": self.current_type,
            "model": self.current_model,
            "is_loaded": self.is_initialized,
            "gpu_device": self.gpu_device,
            "compute_type": self.compute_type,
            "description": "WhisperX - Enige optie voor maximale accuracy"
        }
    
    def check_cuda_availability(self) -> bool:
        """Controleer of CUDA beschikbaar is"""
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False
        except Exception:
            return False
    
    def force_cuda(self) -> bool:
        """Probeer CUDA te gebruiken"""
        if self.check_cuda_availability():
            self.gpu_device = "cuda"
            self.compute_type = "float16"
            return True
        else:
            self.gpu_device = "cpu"
            self.compute_type = "float32"
            return False
    
    def check_gpu_status(self) -> Dict[str, Any]:
        """Controleer GPU status"""
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
            
            # Probeer PyTorch CUDA
            if self.check_cuda_availability():
                import torch
                gpu_info.update({
                    "available": True,
                    "device": "cuda",
                    "name": torch.cuda.get_device_name(0),
                    "memory_total": torch.cuda.get_device_properties(0).total_memory / (1024**3),
                    "memory_used": (torch.cuda.get_device_properties(0).total_memory - torch.cuda.memory_reserved(0)) / (1024**3),
                    "memory_free": torch.cuda.memory_reserved(0) / (1024**3)
                })
            
            return gpu_info
            
        except Exception:
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
