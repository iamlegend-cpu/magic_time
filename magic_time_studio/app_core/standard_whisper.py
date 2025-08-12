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
        self.device = "cuda"  # Forceer CUDA
        self.is_loaded = False
    
    def load_model(self, model_name: str, device: str = "cuda") -> bool:
        """Laad Whisper model"""
        try:
            # Forceer altijd CUDA
            if device != "cuda":
                print(f"⚠️ Device {device} overschreven naar cuda")
                device = "cuda"
            
            print(f"📥 Laad standaard Whisper model: {model_name} op {device}")
            
            # Import en laad echte OpenAI Whisper
            import whisper
            
            # Controleer of CUDA beschikbaar is
            import torch
            if not torch.cuda.is_available():
                print("❌ CUDA niet beschikbaar - kan niet laden")
                return False
            
            # Laad het model op CUDA
            self.model = whisper.load_model(model_name, device=device)
            self.device = device
            self.is_loaded = True
            
            print(f"✅ Standaard Whisper model geladen: {model_name} op CUDA")
            return True
            
        except Exception as e:
            print(f"❌ Fout bij laden standaard Whisper model: {e}")
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
