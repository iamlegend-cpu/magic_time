"""
Standard Whisper Module voor Magic Time Studio
Handelt standaard Whisper transcriptie af
"""

import os
from typing import Optional, Dict, Any

class StandardWhisper:
    """Standaard Whisper implementatie"""
    
    def __init__(self):
        self.model = None
        self.device = "cpu"  # Default naar CPU
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
        except ImportError:
            print("⚠️ PyTorch niet beschikbaar - gebruik CPU")
            self.gpu_available = False
        except Exception as e:
            print(f"⚠️ GPU controle gefaald: {e} - gebruik CPU")
            self.gpu_available = False
    
    def load_model(self, model_name: str, device: str = None) -> bool:
        """Laad Whisper model"""
        try:
            # Gebruik opgegeven device of detecteer beste optie
            if device is None:
                device = "cuda" if self.gpu_available else "cpu"
            
            print(f"📥 Laad standaard Whisper model: {model_name} op {device}")
            
            # Import en laad echte OpenAI Whisper
            try:
                import whisper
            except ImportError as e:
                print(f"❌ Whisper module niet beschikbaar: {e}")
                return False
            
            # Controleer of CUDA beschikbaar is als we het willen gebruiken
            if device == "cuda" and not self.gpu_available:
                print("⚠️ CUDA niet beschikbaar - schakel over naar CPU")
                device = "cpu"
            
            # Probeer het model te laden met betere error handling
            try:
                # Forceer CPU als er problemen zijn met CUDA
                if device == "cuda":
                    try:
                        self.model = whisper.load_model(model_name, device=device)
                    except Exception as cuda_error:
                        print(f"⚠️ CUDA laden gefaald: {cuda_error} - probeer CPU")
                        device = "cpu"
                        self.model = whisper.load_model(model_name, device="cpu")
                else:
                    self.model = whisper.load_model(model_name, device=device)
                
                self.device = device
                self.is_loaded = True
                
                print(f"✅ Standaard Whisper model geladen: {model_name} op {device}")
                return True
                
            except Exception as model_error:
                print(f"❌ Fout bij laden model: {model_error}")
                
                # Probeer fallback naar CPU als GPU faalt
                if device != "cpu":
                    print("🔄 Probeer fallback naar CPU...")
                    try:
                        self.model = whisper.load_model(model_name, device="cpu")
                        self.device = "cpu"
                        self.is_loaded = True
                        print(f"✅ Standaard Whisper model geladen op CPU: {model_name}")
                        return True
                    except Exception as cpu_error:
                        print(f"❌ CPU fallback ook gefaald: {cpu_error}")
                        return False
                return False
            
        except Exception as e:
            print(f"❌ Onverwachte fout bij laden standaard Whisper model: {e}")
            return False
    
    def transcribe(self, audio_path: str, language: str = None) -> Optional[Dict[str, Any]]:
        """Transcribeer audio met standaard Whisper"""
        try:
            if not self.is_loaded:
                print("❌ Model niet geladen")
                return None
            
            print(f"🎤 Standaard Whisper transcriptie: {audio_path}")
            
            # Voer echte transcriptie uit
            result = self.model.transcribe(
                audio_path,
                language=language,
                verbose=False
            )
            
            # Converteer naar gewenst formaat
            transcriptions = []
            for segment in result["segments"]:
                transcriptions.append({
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"].strip()
                })
            
            final_result = {
                "transcript": result["text"].strip(),
                "transcriptions": transcriptions,
                "language": result.get("language", "auto"),
                "type": "standard"
            }
            
            print(f"✅ Standaard Whisper transcriptie voltooid: {len(transcriptions)} segmenten")
            return final_result
            
        except Exception as e:
            print(f"❌ Fout bij standaard Whisper transcriptie: {e}")
            return None
    
    def get_model_info(self) -> Dict[str, Any]:
        """Krijg model informatie"""
        return {
            "type": "standard",
            "model": str(self.model) if self.model else None,
            "device": self.device,
            "is_loaded": self.is_loaded
        }
