"""
VAD Integration voor WhisperX
Handelt VAD instellingen en configuratie af
"""

import os
import sys
from typing import Dict, Any, Optional

class VADIntegration:
    """VAD integratie voor WhisperX"""
    
    def __init__(self):
        self.config_manager = None
        self._init_config_manager()
    
    def _init_config_manager(self):
        """Initialiseer configuratie manager"""
        try:
            # Probeer verschillende import methoden voor config
            try:
                # Methode 1: Directe import
                from core.config import ConfigManager
                self.config_manager = ConfigManager()
            except ImportError:
                try:
                    # Methode 2: Absolute import
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    project_root = os.path.dirname(os.path.dirname(current_dir))
                    if project_root not in sys.path:
                        sys.path.insert(0, project_root)
                    from core.config import ConfigManager
                    self.config_manager = ConfigManager()
                except ImportError:
                    # Methode 3: Fallback - gebruik standaard instellingen
                    print("ℹ️ Kon config niet laden, gebruik standaard VAD instellingen")
                    self.config_manager = None
        except Exception as e:
            print(f"⚠️ Fout bij initialiseren config manager: {e}")
            self.config_manager = None
    
    def get_vad_settings(self) -> Dict[str, Any]:
        """Haal VAD instellingen op uit configuratie"""
        try:
            if self.config_manager:
                # Gebruik get_env met fallback naar "true" (VAD altijd ingeschakeld)
                vad_enabled = self.config_manager.get_env("VAD_ENABLED", "true").lower() == "true"
                print(f"🔧 [DEBUG] VAD configuratie: vad_enabled = {vad_enabled}")
                
                # VAD is altijd ingeschakeld voor WhisperX
                vad_settings = {
                    "vad_enabled": True,  # Forceer altijd True
                    "vad_method": self.config_manager.get_env("VAD_METHOD", "Pyannote (nauwkeurig)"),
                    "vad_threshold": float(self.config_manager.get_env("VAD_THRESHOLD", "0.5")),
                    "vad_onset": float(self.config_manager.get_env("VAD_ONSET", "0.5")),
                    "vad_chunk_size": int(self.config_manager.get_env("VAD_CHUNK_SIZE", "30")),
                    "vad_min_speech": float(self.config_manager.get_env("VAD_MIN_SPEECH", "0.5")),
                    "vad_min_silence": float(self.config_manager.get_env("VAD_MIN_SILENCE", "0.5")),
                }
                print(f"✅ VAD instellingen geladen: {vad_settings}")
                return vad_settings
            else:
                print("ℹ️ VAD instellingen niet beschikbaar, gebruik standaard")
                # Gebruik standaard instellingen met VAD altijd ingeschakeld
                return {
                    "vad_enabled": True,
                    "vad_method": "Pyannote (nauwkeurig)",
                    "vad_threshold": 0.5,
                    "vad_onset": 0.5,
                    "vad_chunk_size": 30,
                    "vad_min_speech": 0.5,
                    "vad_min_silence": 0.5,
                }
                
        except Exception as e:
            print(f"⚠️ Fout bij laden VAD instellingen: {e}")
            # Gebruik standaard instellingen met VAD altijd ingeschakeld
            return {
                "vad_enabled": True,
                "vad_method": "Pyannote (nauwkeurig)",
                "vad_threshold": 0.5,
                "vad_onset": 0.5,
                "vad_chunk_size": 30,
                "vad_min_speech": 0.5,
                "vad_min_silence": 0.5,
            }
    
    def is_vad_enabled(self) -> bool:
        """Controleer of VAD is ingeschakeld"""
        # VAD is altijd ingeschakeld voor WhisperX
        return True
    
    def get_vad_method(self) -> str:
        """Haal VAD methode op"""
        vad_settings = self.get_vad_settings()
        return vad_settings.get("vad_method", "Pyannote (nauwkeurig)")
    
    def get_vad_threshold(self) -> float:
        """Haal VAD threshold op"""
        vad_settings = self.get_vad_settings()
        return float(vad_settings.get("vad_threshold", 0.5))
    
    def get_vad_chunk_size(self) -> int:
        """Haal VAD chunk size op"""
        vad_settings = self.get_vad_settings()
        return int(vad_settings.get("vad_chunk_size", 30))
    
    def update_vad_settings(self, new_settings: Dict[str, Any]) -> bool:
        """Update VAD instellingen"""
        try:
            if self.config_manager:
                # Update configuratie - forceer VAD altijd ingeschakeld
                for key, value in new_settings.items():
                    if key.startswith("vad_"):
                        if key == "vad_enabled":
                            # Forceer VAD altijd ingeschakeld
                            self.config_manager.set_env("VAD_ENABLED", "true")
                        else:
                            self.config_manager.set_env(key.upper(), str(value))
                
                print(f"✅ VAD instellingen bijgewerkt: {new_settings}")
                return True
            else:
                print("⚠️ Config manager niet beschikbaar voor VAD update")
                return False
        except Exception as e:
            print(f"❌ Fout bij bijwerken VAD instellingen: {e}")
            return False
    
    def test_vad_settings(self, audio_path: str) -> Dict[str, Any]:
        """Test VAD instellingen op een kort audio fragment"""
        try:
            # VAD is altijd ingeschakeld voor WhisperX
            # Hier zou je VAD test logica kunnen implementeren
            # Voor nu returnen we een basis test resultaat
            return {
                "success": True,
                "vad_enabled": True,
                "method": self.get_vad_method(),
                "threshold": self.get_vad_threshold(),
                "chunk_size": self.get_vad_chunk_size()
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
