"""
WhisperX Model Manager
Handelt het laden en beheren van WhisperX modellen af
"""

import os
import whisperx
import torch
from typing import Dict, Any, Optional

class WhisperXModelManager:
    """Manager voor WhisperX modellen"""
    
    def __init__(self, device: str = "cuda", compute_type: str = "float16"):
        self.device = device
        self.compute_type = compute_type
        self.model = None
        self.align_model = None
        self.align_extend = None
        self.current_model = None
        self.is_loaded = False
        self._model_cache = {}  # Cache voor geladen modellen
    
    def load_model(self, model_name: str = "large-v3", vad_settings: Dict[str, Any] = None) -> bool:
        """Laad WhisperX model met VAD (altijd ingeschakeld)"""
        # Controleer of het model al geladen is
        if self.is_loaded and self.current_model == model_name and self.model is not None:
            print(f"✅ Model {model_name} is al geladen, skip loading")
            return True
            
        try:
            print(f"📥 Laad WhisperX model: {model_name} op {self.device}")
            
            # Gebruik doorgegeven VAD instellingen of standaard waarden
            if vad_settings and vad_settings.get("vad_enabled", True):
                preferred_vad_method = vad_settings.get("vad_method_whisperx", "pyannote")
                print(f"🔧 [DEBUG] Gebruik voorkeur VAD methode: {preferred_vad_method}")
                print(f"🔧 [DEBUG] VAD instellingen: device={self.device}, compute_type={self.compute_type}")
                
                # Probeer eerst de voorkeur VAD methode
                try:
                    print(f"🔍 Probeer voorkeur VAD methode: {preferred_vad_method}")
                    # Gebruik veilige compute type voor CPU
                    safe_compute_type = "int8" if self.device == "cpu" else self.compute_type
                    print(f"🔧 [DEBUG] Gebruik compute_type: {safe_compute_type}")
                    
                    # Maak VAD opties op basis van instellingen
                    vad_options = {
                        "chunk_size": vad_settings.get("vad_chunk_size", 30),
                        "vad_onset": vad_settings.get("vad_onset", 0.5),
                        "vad_offset": vad_settings.get("vad_onset", 0.5),  # Gebruik onset als offset
                    }
                    
                    self.model = whisperx.load_model(
                        model_name, 
                        self.device, 
                        compute_type=safe_compute_type,
                        language=None,  # Auto-detect
                        vad_method=preferred_vad_method,
                        vad_options=vad_options
                    )
                    vad_method = preferred_vad_method
                    print(f"✅ Voorkeur VAD methode {preferred_vad_method} succesvol geladen")
                    print(f"🔧 VAD opties gebruikt: {vad_options}")
                    
                except Exception as e:
                    print(f"⚠️ Voorkeur VAD methode {preferred_vad_method} gefaald: {e}")
                    
                    # Fallback naar andere beschikbare VAD methoden (pyannote eerst)
                    fallback_methods = ["pyannote", "auditok", "silero"]
                    fallback_methods = [m for m in fallback_methods if m != preferred_vad_method]
                    
                    for method in fallback_methods:
                        try:
                            print(f"🔍 Probeer fallback VAD methode: {method}")
                            self.model = whisperx.load_model(
                                model_name, 
                                self.device, 
                                compute_type=safe_compute_type,
                                language=None,
                                vad_method=method,
                                vad_options=vad_options
                            )
                            vad_method = method
                            print(f"✅ Fallback VAD methode {method} succesvol geladen")
                            break
                        except Exception as e:
                            print(f"⚠️ Fallback VAD methode {method} gefaald: {e}")
                            continue
                    
                    # Als alle VAD methoden falen, probeer zonder VAD
                    if not self.model:
                        try:
                            print("🔍 Probeer model zonder VAD te laden...")
                            self.model = whisperx.load_model(
                                model_name, 
                                self.device, 
                                compute_type=safe_compute_type,
                                language=None
                            )
                            print("✅ Model zonder VAD succesvol geladen")
                            vad_method = "geen"
                        except Exception as e:
                            print(f"❌ Alle model loading methoden gefaald: {e}")
                            return False
            else:
                # Geen VAD instellingen, gebruik standaard aanpak (pyannote eerst)
                print("🔧 Geen VAD instellingen, gebruik standaard VAD loading")
                vad_methods = ["pyannote", "auditok", "silero"]
                vad_method = None
                
                for method in vad_methods:
                    try:
                        print(f"🔍 Probeer VAD methode: {method}")
                        safe_compute_type = "int8" if self.device == "cpu" else self.compute_type
                        
                        self.model = whisperx.load_model(
                            model_name, 
                            self.device, 
                            compute_type=safe_compute_type,
                            language=None,
                            vad_method=method,
                            vad_options={
                                "chunk_size": 30,
                                "vad_onset": 0.5,
                                "vad_offset": 0.5,
                            }
                        )
                        vad_method = method
                        print(f"✅ VAD methode {method} succesvol geladen")
                        break
                    except Exception as e:
                        print(f"⚠️ VAD methode {method} gefaald: {e}")
                        continue
                
                if not self.model:
                    print("❌ Alle VAD methoden gefaald")
                    return False
            
            print(f"✅ WhisperX model geladen met VAD methode: {vad_method}")
            
            # Laad alignment model voor accurate timestamps
            if self.align_model is None:
                try:
                    self.align_model, self.align_extend = whisperx.load_align_model(
                        language_code="en",  # Altijd Engels voor alignment
                        device=self.device
                    )
                    print("✅ Alignment model geladen")
                except Exception as e:
                    print(f"⚠️ Kon alignment model niet laden: {e}")
                    self.align_model = None
                    self.align_extend = None
            
            self.current_model = model_name  # Update het huidige model
            self.is_loaded = True
            print(f"✅ WhisperX model geladen: {model_name}")
            return True
            
        except Exception as e:
            print(f"❌ Fout bij laden WhisperX model: {e}")
            return False
    
    def reload_model_with_vad_settings(self, model_name: str, vad_settings: Dict[str, Any]) -> bool:
        """Herlaad WhisperX model met VAD instellingen (altijd ingeschakeld)"""
        # Controleer of we echt moeten herladen
        if (self.is_loaded and self.current_model == model_name and 
            self.model is not None and not self._vad_settings_changed(vad_settings)):
            print(f"✅ Model {model_name} hoeft niet te worden herladen - VAD instellingen ongewijzigd")
            return True
            
        print(f"🔄 Herlaad WhisperX model met VAD instellingen: {model_name}")
        
        # VAD is altijd ingeschakeld, gebruik instellingen of standaard waarden
        if vad_settings and vad_settings.get("vad_enabled", True):
            # Converteer VAD methode naar WhisperX formaat
            from ..whisperx_vad import VADManager
            vad_manager = VADManager()
            whisperx_vad_method = vad_manager.convert_vad_method(
                vad_settings.get("vad_method", "Silero (snel)")
            )
            
            # Maak VAD opties
            vad_options = vad_manager.create_vad_options(vad_settings)
            
            print(f"🔧 VAD opties: {vad_options}")
        else:
            # Gebruik standaard VAD instellingen
            whisperx_vad_method = "silero"
            vad_options = {
                "chunk_size": 30,
                "vad_onset": 0.5,
                "vad_offset": 0.5,
            }
            print(f"🔧 Standaard VAD opties: {vad_options}")
        
        try:
            # Laad WhisperX model MET VAD instellingen
            # Gebruik veilige compute type voor CPU
            safe_compute_type = "int8" if self.device == "cpu" else self.compute_type
            self.model = whisperx.load_model(
                model_name, 
                self.device, 
                compute_type=safe_compute_type,
                language=None,  # Auto-detect
                vad_method=whisperx_vad_method,
                vad_options=vad_options
            )
        except Exception as e:
            print(f"❌ Fout bij laden WhisperX model: {e}")
            return False
        
        # Laad alignment model voor accurate timestamps
        if self.align_model is None:
            try:
                self.align_model, self.align_extend = whisperx.load_align_model(
                    language_code="en",  # Altijd Engels voor alignment
                    device=self.device
                )
            except Exception as e:
                print(f"⚠️ Kon alignment model niet laden: {e}")
                self.align_model = None
                self.align_extend = None
        
        self.current_model = model_name  # Update het huidige model
        self.is_loaded = True
        self._last_vad_settings = vad_settings.copy() if vad_settings else {}
        print(f"✅ WhisperX model herladen: {model_name}")
        print(f"🎯 VAD methode: {whisperx_vad_method}")
        print(f"🎯 VAD opties: {vad_options}")
        return True
    
    def _vad_settings_changed(self, new_settings: Dict[str, Any]) -> bool:
        """Controleer of VAD instellingen zijn veranderd"""
        if not hasattr(self, '_last_vad_settings'):
            return True
        
        if not new_settings:
            return False
            
        # Vergelijk alleen relevante VAD instellingen
        relevant_keys = ['vad_method', 'vad_threshold', 'vad_onset', 'vad_chunk_size']
        for key in relevant_keys:
            if (key in new_settings and key in self._last_vad_settings and 
                new_settings[key] != self._last_vad_settings[key]):
                return True
        return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """Krijg informatie over het geladen model"""
        return {
            "device": self.device,
            "compute_type": self.compute_type,
            "gpu_available": torch.cuda.is_available(),
            "is_loaded": self.is_loaded,
            "current_model": self.current_model,
            "has_align_model": self.align_model is not None
        }
    
    def cleanup(self):
        """Ruim geheugen op - inclusief CUDA/GPU context"""
        try:
            print("🧹 WhisperX geheugen opruimen...")
            
            # Ruim PyTorch modellen op
            if self.model:
                del self.model
                self.model = None
            if self.align_model:
                del self.align_model
                self.align_model = None
            if self.align_extend:
                del self.align_extend
                self.align_extend = None
            
            # Reset status
            self.is_loaded = False
            self.current_model = None
            
            print("🧹 WhisperX geheugen opgeruimd")
            
        except Exception as e:
            print(f"⚠️ Fout bij cleanup: {e}")
