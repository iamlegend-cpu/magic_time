"""
Whisper Manager voor Magic Time Studio
Beheert zowel standaard Whisper als Fast Whisper met keuze optie
"""

import os
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum

# Absolute imports in plaats van relative imports
try:
    from magic_time_studio.core.logging import logger
    from magic_time_studio.core.config import config_manager
    from magic_time_studio.core.utils import safe_basename, create_progress_bar
except ImportError:
    # Fallback voor directe import
    import sys
    sys.path.append('..')
    from core.logging import logger
    from core.config import config_manager
    from core.utils import safe_basename, create_progress_bar

# Debug mode - zet op False om debug output uit te zetten
DEBUG_MODE = False

class WhisperType(Enum):
    """Enum voor verschillende Whisper types"""
    STANDARD = "standard"
    FAST = "fast"

class WhisperManager:
    """Manager voor zowel standaard Whisper als Fast Whisper"""
    
    def __init__(self):
        self.current_whisper_type = None
        self.standard_processor = None
        self.fast_processor = None
        self.current_processor = None
        
        # Laad configuratie
        self.default_whisper_type = config_manager.get_env("WHISPER_TYPE", "fast")
        self.default_model = config_manager.get_env("DEFAULT_WHISPER_MODEL", "large")
        self.default_fast_model = config_manager.get_env("DEFAULT_FAST_WHISPER_MODEL", "large-v3-turbo")
        
        # Beschikbare modellen per type
        self.standard_models = ["tiny", "base", "small", "medium", "large"]
        self.fast_models = [
            "tiny", "base", "small", "medium", "large",
            "large-v1", "large-v2", "large-v3", 
            "large-v3-turbo", "turbo"
        ]
        
        self.supported_languages = {
            "en": "Engels", 
            "nl": "Nederlands",
            "de": "Duits",
            "fr": "Frans",
            "es": "Spaans",
            "it": "Italiaans",
            "pt": "Portugees",
            "ru": "Russisch",
            "ja": "Japans",
            "ko": "Koreaans",
            "zh": "Chinees"
        }
        
        if DEBUG_MODE:
            logger.log_debug(f"[DEBUG] WhisperManager geïnitialiseerd met default type: {self.default_whisper_type}")
    
    def get_available_whisper_types(self) -> List[str]:
        """Krijg lijst van beschikbare Whisper types"""
        types = []
        
        # Controleer of Fast Whisper beschikbaar is
        try:
            from faster_whisper import WhisperModel
            types.append("fast")
            if DEBUG_MODE:
                logger.log_debug("[DEBUG] Fast Whisper beschikbaar")
        except ImportError:
            if DEBUG_MODE:
                logger.log_debug("[DEBUG] Fast Whisper niet beschikbaar")
        
        return types
    
    def get_available_models(self, whisper_type: str = None) -> List[str]:
        """Krijg lijst van beschikbare modellen voor specifiek type"""
        if whisper_type is None:
            whisper_type = self.default_whisper_type
        
        if whisper_type == "fast":
            return self.fast_models.copy()
        else:
            return self.standard_models.copy()
    
    def initialize(self, whisper_type: str = None, model_name: str = None) -> bool:
        """Initialiseer Whisper met specifiek type en model"""
        try:
            # Gebruik altijd Fast Whisper, ongeacht wat er wordt opgegeven
            whisper_type = "fast"
            
            # Controleer of Fast Whisper beschikbaar is
            available_types = self.get_available_whisper_types()
            if whisper_type not in available_types:
                if DEBUG_MODE:
                    logger.log_debug(f"❌ Fast Whisper niet beschikbaar")
                return False
            
            # Bepaal model naam - gebruik altijd Fast Whisper model
            if model_name is None:
                model_name = self.default_fast_model
            
            # Controleer of model beschikbaar is voor Fast Whisper
            available_models = self.get_available_models(whisper_type)
            if model_name not in available_models:
                if DEBUG_MODE:
                    logger.log_debug(f"❌ Model {model_name} niet beschikbaar voor Fast Whisper")
                return False
            
            # Initialiseer alleen Fast Whisper
            return self._initialize_fast_whisper(model_name)
                
        except Exception as e:
            if DEBUG_MODE:
                logger.log_debug(f"❌ Fout bij initialiseren Whisper: {e}")
            return False
    
    def _initialize_standard_whisper(self, model_name: str) -> bool:
        """Initialiseer standaard Whisper - UITGESCHAKELD"""
        if DEBUG_MODE:
            logger.log_debug("❌ Standaard Whisper is uitgeschakeld - gebruik Fast Whisper")
        return False
    
    def _initialize_fast_whisper(self, model_name: str) -> bool:
        """Initialiseer Fast Whisper"""
        try:
            from magic_time_studio.processing.whisper_processor import whisper_processor
            
            # Ruim oude processor op
            if hasattr(self, 'standard_processor') and self.standard_processor:
                try:
                    self.standard_processor.cleanup()
                except:
                    pass
                self.standard_processor = None
            
            self.fast_processor = whisper_processor
            success = self.fast_processor.initialize(model_name)
            
            if success:
                self.current_whisper_type = WhisperType.FAST
                self.current_processor = self.fast_processor
                print(f"🔍 [DEBUG] Whisper Manager: Fast Whisper geïnitialiseerd met model: {model_name}")
                if DEBUG_MODE:
                    logger.log_debug(f"✅ Fast Whisper geïnitialiseerd met model: {model_name}")
                return True
            else:
                print(f"🔍 [DEBUG] Whisper Manager: Fast Whisper initialisatie gefaald voor model: {model_name}")
                if DEBUG_MODE:
                    logger.log_debug(f"❌ Fast Whisper initialisatie gefaald voor model: {model_name}")
                return False
                
        except Exception as e:
            print(f"🔍 [DEBUG] Whisper Manager: Fout bij initialiseren Fast Whisper: {e}")
            if DEBUG_MODE:
                logger.log_debug(f"❌ Fout bij initialiseren Fast Whisper: {e}")
            return False
    
    def transcribe_audio(self, audio_path: str, language: str = "en", 
                        progress_callback: Optional[callable] = None,
                        stop_callback: Optional[callable] = None) -> Dict[str, Any]:
        """Transcribeer audio bestand met huidige processor"""
        try:
            if not self.current_processor:
                logger.log_debug("❌ Geen Whisper processor geïnitialiseerd")
                return {"error": "Geen Whisper processor geïnitialiseerd"}
            
            if DEBUG_MODE:
                whisper_type_name = "Fast Whisper" if self.current_whisper_type == WhisperType.FAST else "Standaard Whisper"
                logger.log_debug(f"🎤 Start transcriptie met {whisper_type_name}: {safe_basename(audio_path)}")
                print(f"🔍 [DEBUG] Whisper Manager: Gebruik {whisper_type_name} voor transcriptie")
            
            # Stop eventuele oude callbacks
            if hasattr(self, '_old_progress_callback') and self._old_progress_callback:
                try:
                    self._old_progress_callback = None
                except:
                    pass
            
            # Sla nieuwe callback op
            self._old_progress_callback = progress_callback
            
            # Gebruik alleen de huidige processor
            return self.current_processor.transcribe_audio(
                audio_path, 
                language, 
                progress_callback, 
                stop_callback
            )
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij transcriptie: {e}")
            return {"error": str(e)}
    
    def detect_language(self, audio_path: str) -> str:
        """Detecteer taal van audio bestand"""
        try:
            if not self.current_processor:
                logger.log_debug("❌ Geen Whisper processor geïnitialiseerd voor taal detectie")
                return "en"
            
            return self.current_processor.detect_language(audio_path)
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij taal detectie: {e}")
            return "en"
    
    def get_model_info(self) -> Dict[str, Any]:
        """Krijg informatie over huidig model"""
        if not self.current_processor:
            return {"error": "Geen processor geladen"}
        
        try:
            info = self.current_processor.get_model_info()
            info["whisper_type"] = self.current_whisper_type.value
            return info
        except Exception as e:
            return {"error": str(e)}
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Krijg lijst van ondersteunde talen"""
        return self.supported_languages.copy()
    
    def get_current_whisper_type(self) -> str:
        """Krijg huidig Whisper type"""
        if self.current_whisper_type:
            return self.current_whisper_type.value
        return "none"
    
    def is_model_loaded(self) -> bool:
        """Controleer of model geladen is"""
        return (self.current_processor is not None and 
                self.current_processor.is_model_loaded())
    
    def switch_whisper_type(self, whisper_type: str, model_name: str = None) -> bool:
        """Wissel naar ander Whisper type - alleen Fast Whisper ondersteund"""
        try:
            if DEBUG_MODE:
                logger.log_debug(f"🔄 Wissel naar Whisper type: {whisper_type}")
            
            # Force altijd Fast Whisper
            if whisper_type != "fast":
                if DEBUG_MODE:
                    logger.log_debug(f"⚠️ Alleen Fast Whisper ondersteund, force naar 'fast'")
                whisper_type = "fast"
            
            # Cleanup huidige processor
            self.cleanup()
            
            # Initialiseer Fast Whisper
            return self.initialize(whisper_type, model_name)
            
        except Exception as e:
            if DEBUG_MODE:
                logger.log_debug(f"❌ Fout bij wisselen Whisper type: {e}")
            return False
    
    def get_performance_comparison(self) -> Dict[str, Any]:
        """Krijg performance vergelijking tussen Whisper types"""
        comparison = {
            "standard_available": "standard" in self.get_available_whisper_types(),
            "fast_available": "fast" in self.get_available_whisper_types(),
            "current_type": self.get_current_whisper_type(),
            "recommendations": []
        }
        
        # Voeg aanbevelingen toe
        if comparison["fast_available"]:
            comparison["recommendations"].append({
                "type": "fast",
                "reason": "2-4x sneller dan standaard Whisper",
                "model": "large-v3-turbo"
            })
        
        if comparison["standard_available"]:
            comparison["recommendations"].append({
                "type": "standard",
                "reason": "Stabiel en goed getest",
                "model": "large"
            })
        
        return comparison
    
    def cleanup(self):
        """Ruim resources op"""
        try:
            if self.standard_processor:
                self.standard_processor.cleanup()
                self.standard_processor = None
            
            if self.fast_processor:
                self.fast_processor.cleanup()
                self.fast_processor = None
            
            self.current_processor = None
            self.current_whisper_type = None
            
            if DEBUG_MODE:
                logger.log_debug("🧹 WhisperManager resources opgeruimd")
                
        except Exception as e:
            if DEBUG_MODE:
                logger.log_debug(f"❌ Fout bij opruimen WhisperManager: {e}")

# Globale Whisper manager instantie
whisper_manager = WhisperManager() 