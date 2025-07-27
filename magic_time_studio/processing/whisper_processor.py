"""
Whisper processor voor Magic Time Studio
Beheert audio transcriptie met OpenAI Whisper
"""

import os
import tempfile
import subprocess
import json
from typing import Dict, Any, List, Optional, Tuple
from ..core.logging import logger
from ..core.config import config_manager
from ..core.utils import safe_basename

class WhisperProcessor:
    """Processor voor Whisper audio transcriptie"""
    
    def __init__(self):
        self.available_models = ["tiny", "base", "small", "medium", "large"]
        self.supported_languages = {
            "auto": "Automatisch detecteren",
            "nl": "Nederlands",
            "en": "Engels", 
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
        self.current_model = None
        self.is_initialized = False
        
        # Laad configuratie uit environment variables
        self.default_model = config_manager.get_env("DEFAULT_WHISPER_MODEL", "base")
        self.device = config_manager.get_env("WHISPER_DEVICE", "cpu")
        
    def initialize(self, model_name: str = None) -> bool:
        """Initialiseer Whisper met specifiek model"""
        try:
            # Gebruik default model als geen model opgegeven
            if model_name is None:
                model_name = self.default_model
            
            if model_name not in self.available_models:
                logger.log_debug(f"❌ Onbekend Whisper model: {model_name}")
                return False
            
            # Probeer Whisper te importeren
            try:
                import whisper
                self.current_model = whisper.load_model(model_name)
                self.is_initialized = True
                logger.log_debug(f"✅ Whisper model '{model_name}' geladen")
                return True
            except ImportError:
                logger.log_debug("❌ Whisper niet geïnstalleerd. Installeer met: pip install openai-whisper")
                return False
            except Exception as e:
                logger.log_debug(f"❌ Fout bij laden Whisper model: {e}")
                return False
                
        except Exception as e:
            logger.log_debug(f"❌ Fout bij initialiseren Whisper: {e}")
            return False
    
    def transcribe_audio(self, audio_path: str, language: str = "auto", 
                        progress_callback: Optional[callable] = None) -> Dict[str, Any]:
        """Transcribeer audio bestand met Whisper"""
        try:
            if not self.is_initialized:
                logger.log_debug("❌ Whisper niet geïnitialiseerd")
                return {"error": "Whisper niet geïnitialiseerd"}
            
            if not os.path.exists(audio_path):
                logger.log_debug(f"❌ Audio bestand niet gevonden: {audio_path}")
                return {"error": "Audio bestand niet gevonden"}
            
            logger.log_debug(f"🎤 Start transcriptie: {safe_basename(audio_path)}")
            
            # Progress callback wrapper
            def progress_wrapper(progress):
                if progress_callback:
                    progress_callback(progress)
                logger.log_debug(f"📊 Transcriptie voortgang: {progress:.1%}")
            
            # Voer transcriptie uit
            import whisper
            
            # Zet taal om naar Whisper formaat
            whisper_language = None if language == "auto" else language
            
            result = self.current_model.transcribe(
                audio_path,
                language=whisper_language,
                verbose=False,
                progress_callback=progress_wrapper
            )
            
            # Verwerk resultaat
            transcriptions = []
            for segment in result["segments"]:
                transcriptions.append({
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"].strip(),
                    "language": result.get("language", language)
                })
            
            logger.log_debug(f"✅ Transcriptie voltooid: {len(transcriptions)} segmenten")
            
            return {
                "success": True,
                "transcriptions": transcriptions,
                "language": result.get("language", language),
                "duration": result.get("duration", 0),
                "segments": len(transcriptions)
            }
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij transcriptie: {e}")
            return {"error": str(e)}
    
    def detect_language(self, audio_path: str) -> str:
        """Detecteer taal van audio bestand"""
        try:
            if not self.is_initialized:
                logger.log_debug("❌ Whisper niet geïnitialiseerd voor taal detectie")
                return "auto"
            
            logger.log_debug(f"🌍 Taal detectie: {safe_basename(audio_path)}")
            
            import whisper
            
            # Laad audio en detecteer taal
            audio = whisper.load_audio(audio_path)
            audio = whisper.pad_or_trim(audio)
            
            # Log mel spectrogram
            mel = whisper.log_mel_spectrogram(audio).to(self.current_model.device)
            
            # Detecteer taal
            _, probs = self.current_model.detect_language(mel)
            detected_language = max(probs, key=probs.get)
            
            logger.log_debug(f"✅ Taal gedetecteerd: {detected_language}")
            return detected_language
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij taal detectie: {e}")
            return "auto"
    
    def get_model_info(self) -> Dict[str, Any]:
        """Krijg informatie over huidig model"""
        if not self.is_initialized:
            return {"error": "Model niet geladen"}
        
        try:
            return {
                "model_name": self.current_model.name if hasattr(self.current_model, 'name') else "unknown",
                "model_size": self.current_model.dims if hasattr(self.current_model, 'dims') else "unknown",
                "device": str(self.current_model.device),
                "is_multilingual": True
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_available_models(self) -> List[str]:
        """Krijg lijst van beschikbare modellen"""
        return self.available_models.copy()
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Krijg lijst van ondersteunde talen"""
        return self.supported_languages.copy()
    
    def is_model_loaded(self) -> bool:
        """Controleer of model geladen is"""
        return self.is_initialized and self.current_model is not None
    
    def cleanup(self):
        """Ruim resources op"""
        try:
            if self.current_model:
                del self.current_model
                self.current_model = None
            self.is_initialized = False
            logger.log_debug("🧹 Whisper resources opgeruimd")
        except Exception as e:
            logger.log_debug(f"❌ Fout bij opruimen Whisper: {e}")

# Globale Whisper processor instantie
whisper_processor = WhisperProcessor() 