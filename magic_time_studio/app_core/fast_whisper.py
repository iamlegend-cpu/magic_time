"""
Fast Whisper Module voor Magic Time Studio
Handelt Faster Whisper transcriptie af
"""

import os
from typing import Optional, Dict, Any

class FastWhisper:
    """Faster Whisper implementatie"""
    
    def __init__(self):
        self.model = None
        self.device = "cpu"  # Default naar CPU
        self.compute_type = "float32"  # Default naar float32 voor CPU
        self.is_loaded = False
        self.gpu_available = False
        self._check_gpu_availability()
    
    def _check_gpu_availability(self):
        """Controleer GPU beschikbaarheid"""
        try:
            import torch
            self.gpu_available = torch.cuda.is_available()
            if self.gpu_available:
                print("✅ CUDA beschikbaar - GPU kan worden gebruikt")
            else:
                print("⚠️ CUDA niet beschikbaar - gebruik CPU")
            self._gpu_checked = True
        except ImportError:
            print("⚠️ PyTorch niet beschikbaar - gebruik CPU")
            self.gpu_available = False
        except Exception as e:
            print(f"⚠️ GPU controle gefaald: {e} - gebruik CPU")
            self.gpu_available = False
    
    def load_model(self, model_name: str, device: str = None, compute_type: str = None) -> bool:
        """Laad Faster Whisper model"""
        try:
            # Gebruik opgegeven device of detecteer beste optie
            if device is None:
                device = "cuda" if self.gpu_available else "cpu"
            
            # Stel compute type in op basis van device
            if compute_type is None:
                if device == "cuda":
                    compute_type = "float16"  # GPU ondersteunt float16
                else:
                    compute_type = "float32"  # CPU ondersteunt float32 beter
            
            print(f"📥 Laad Faster Whisper model: {model_name} op {device} ({compute_type})")
            
            # Import en laad echte Faster Whisper
            from faster_whisper import WhisperModel
            
            # Laad het model op opgegeven device
            self.model = WhisperModel(model_name, device=device, compute_type=compute_type)
            self.device = device
            self.compute_type = compute_type
            self.is_loaded = True
            
            print(f"✅ Faster Whisper model geladen: {model_name} op {device}")
            return True
            
        except Exception as e:
            print(f"❌ Fout bij laden Faster Whisper model op {device}: {e}")
            # Probeer fallback naar CPU als GPU faalt
            if device != "cpu":
                print("🔄 Probeer fallback naar CPU...")
                try:
                    self.model = WhisperModel(model_name, device="cpu", compute_type="float32")
                    self.device = "cpu"
                    self.compute_type = "float32"
                    self.is_loaded = True
                    print(f"✅ Faster Whisper model geladen op CPU: {model_name}")
                    return True
                except Exception as cpu_error:
                    print(f"❌ CPU fallback ook gefaald: {cpu_error}")
                    return False
            return False
    
    def transcribe(self, audio_path: str, language: str = None, beam_size: int = 5, progress_callback=None) -> Optional[Dict[str, Any]]:
        """Transcribeer audio met Faster Whisper en voortgang tracking"""
        try:
            if not self.is_loaded:
                print("❌ Model niet geladen")
                return None
            
            print(f"🎤 Faster Whisper transcriptie: {audio_path}")
            
            # Voer transcriptie uit met voortgang tracking
            segments, info = self.model.transcribe(
                audio_path, 
                language=language,
                beam_size=beam_size,
                vad_filter=False  # VAD uitgeschakeld
            )
            
            # Converteer naar gewenst formaat met voortgang tracking
            transcriptions = []
            full_text = ""
            total_segments = 0
            
            # Tel eerst het totale aantal segmenten voor voortgang berekening
            try:
                # Maak een kopie van de segments iterator om te tellen
                segments_copy = list(segments)
                total_segments = len(segments_copy)
                segments = segments_copy
            except:
                # Als we niet kunnen tellen, gebruik een schatting
                total_segments = 10  # Default schatting
            
            print(f"📊 Transcriptie gestart: {total_segments} segmenten verwacht")
            
            for i, segment in enumerate(segments):
                transcriptions.append({
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text.strip()
                })
                full_text += segment.text.strip() + " "
                
                # Update voortgang elke 2 segmenten of bij elk segment als er weinig zijn
                if total_segments <= 10 or i % 2 == 0:
                    progress = (i + 1) / total_segments
                    if progress_callback:
                        progress_callback(progress, f"🎤 Faster Whisper: {progress*100:.1f}% - {os.path.basename(audio_path)}")
                    else:
                        print(f"🎤 Faster Whisper: {progress*100:.1f}% - {os.path.basename(audio_path)}")
            
            result = {
                "transcript": full_text.strip(),
                "transcriptions": transcriptions,
                "language": info.language if info.language else "auto",
                "confidence": info.language_probability if hasattr(info, 'language_probability') else 0.0,
                "type": "fast",
                "device": self.device,
                "compute_type": self.compute_type,
                "beam_size": beam_size
            }
            
            print(f"✅ Faster Whisper transcriptie voltooid: {len(transcriptions)} segmenten op {self.device}")
            return result
            
        except Exception as e:
            print(f"❌ Fout bij Faster Whisper transcriptie: {e}")
            return None
    
    def get_model_info(self) -> Dict[str, Any]:
        """Krijg model informatie"""
        return {
            "type": "fast",
            "model": str(self.model) if self.model else None,
            "device": self.device,
            "compute_type": self.compute_type,
            "is_loaded": self.is_loaded,
            "gpu_available": self.gpu_available
        }
    
    def get_available_compute_types(self) -> list:
        """Krijg beschikbare compute types"""
        return ["float16", "float32", "int8"]
    
    def get_device_info(self) -> Dict[str, Any]:
        """Krijg device informatie voor monitoring"""
        try:
            if self.device == "cuda" and self.gpu_available:
                import torch
                if torch.cuda.is_available():
                    return {
                        "device": "cuda",
                        "name": torch.cuda.get_device_name(0),
                        "memory_total": torch.cuda.get_device_properties(0).total_memory / (1024**3),
                        "memory_used": torch.cuda.memory_allocated(0) / (1024**3),
                        "memory_free": (torch.cuda.get_device_properties(0).total_memory - torch.cuda.memory_allocated(0)) / (1024**3)
                    }
            else:
                return {
                    "device": "cpu",
                    "name": "CPU",
                    "memory_total": 0,
                    "memory_used": 0,
                    "memory_free": 0
                }
        except Exception as e:
            print(f"⚠️ Fout bij ophalen device info: {e}")
            return {
                "device": "unknown",
                "name": "Unknown",
                "memory_total": 0,
                "memory_used": 0,
                "memory_free": 0
            }
    
    def get_gpu_status(self) -> Dict[str, Any]:
        """Krijg GPU status voor monitoring"""
        try:
            if self.device == "cuda" and self.gpu_available:
                import torch
                if torch.cuda.is_available():
                    # Probeer GPU utilization op te halen via pynvml
                    try:
                        import pynvml
                        pynvml.nvmlInit()
                        device_count = pynvml.nvmlDeviceGetCount()
                        if device_count > 0:
                            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                            utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
                            memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                            
                            return {
                                "available": True,
                                "device": "cuda",
                                "utilization": utilization.gpu,
                                "memory_used": memory_info.used / (1024**3),
                                "memory_total": memory_info.total / (1024**3),
                                "name": torch.cuda.get_device_name(0),
                                "temperature": 0
                            }
                    except:
                        pass
                    
                    # Fallback naar PyTorch alleen
                    memory_allocated = torch.cuda.memory_allocated(0) / (1024**3)
                    memory_total = torch.cuda.get_device_properties(0).total_memory / (1024**3)
                    
                    # Bereken utilization op basis van memory gebruik
                    utilization = 0
                    if memory_total > 0:
                        utilization = min(100, int((memory_allocated / memory_total) * 100))
                    
                    return {
                        "available": True,
                        "device": "cuda",
                        "utilization": utilization,
                        "memory_used": memory_allocated,
                        "memory_total": memory_total,
                        "name": f"Fast Whisper ({torch.cuda.get_device_name(0)})",
                        "temperature": 0
                    }
            
            # Geen GPU beschikbaar
            return {
                "available": False,
                "device": "cpu",
                "utilization": 0,
                "memory_used": 0,
                "memory_total": 0,
                "name": "CPU",
                "temperature": 0
            }
            
        except Exception as e:
            print(f"⚠️ Fout bij ophalen GPU status: {e}")
            # Return een veilige fallback dictionary in plaats van None
            return {
                "available": False,
                "device": "unknown",
                "utilization": 0,
                "memory_used": 0,
                "memory_total": 0,
                "name": "Unknown",
                "temperature": 0
            }
    
    def switch_device(self, new_device: str) -> bool:
        """Schakel over naar ander device"""
        try:
            if new_device not in ["cuda", "cpu"]:
                print(f"⚠️ Ongeldig device: {new_device}")
                return False
            
            if new_device == "cuda" and not self.gpu_available:
                print("❌ CUDA niet beschikbaar")
                return False
            
            if self.device == new_device:
                print(f"ℹ️ Al op device: {new_device}")
                return True
            
            print(f"🔄 Schakel over naar device: {new_device}")
            self.device = new_device
            
            # Herlaad model op nieuw device als het geladen is
            if self.is_loaded and self.model:
                current_model_name = str(self.model).split("(")[0].strip()
                return self.load_model(current_model_name, new_device, self.compute_type)
            
            return True
            
        except Exception as e:
            print(f"❌ Fout bij device switch: {e}")
            return False
