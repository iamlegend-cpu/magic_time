"""
Whisper processor voor Magic Time Studio
Beheert audio transcriptie met OpenAI Whisper
"""

import os
import tempfile
import subprocess
import json
from typing import Dict, Any, List, Optional, Tuple

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

class WhisperProcessor:
    """Processor voor Whisper audio transcriptie"""
    
    def __init__(self):
        self.available_models = ["tiny", "base", "small", "medium", "large"]
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
        self.current_model = None
        self.is_initialized = False
        
        # Laad configuratie uit environment variables
        self.default_model = config_manager.get_env("DEFAULT_WHISPER_MODEL", "large")
        # Device: kies cuda als beschikbaar, anders cpu
        requested_device = config_manager.get_env("WHISPER_DEVICE", "auto")
        import torch
        cuda_available = torch.cuda.is_available()
        if DEBUG_MODE:
            logger.log_debug(f"[DEBUG] CUDA beschikbaar: {cuda_available}")
        if requested_device == "cuda" or (requested_device == "auto" and cuda_available):
            self.device = "cuda"
        elif requested_device == "mps" or (requested_device == "auto" and hasattr(torch.backends, "mps") and torch.backends.mps.is_available()):
            self.device = "mps"
        else:
            self.device = "cpu"
        if DEBUG_MODE:
            logger.log_debug(f"[DEBUG] Whisper device ingesteld op: {self.device}")
        
    def initialize(self, model_name: str = None) -> bool:
        """Initialiseer Whisper met specifiek model"""
        try:
            # Gebruik default model als geen model opgegeven
            if model_name is None:
                model_name = self.default_model
            
            if model_name not in self.available_models:
                if DEBUG_MODE:
                    logger.log_debug(f"❌ Onbekend Whisper model: {model_name}")
                return False
            
            # Probeer Whisper te importeren
            try:
                import whisper
                self.current_model = whisper.load_model(model_name, device=self.device)
                self.is_initialized = True
                if DEBUG_MODE:
                    logger.log_debug(f"✅ Whisper model '{model_name}' geladen op device: {self.device}")
                return True
            except ImportError:
                logger.log_debug("❌ Whisper niet geïnstalleerd. Installeer met: pip install openai-whisper")
                return False
            except Exception as e:
                if DEBUG_MODE:
                    logger.log_debug(f"❌ Fout bij laden Whisper model: {e}")
                return False
                
        except Exception as e:
            if DEBUG_MODE:
                logger.log_debug(f"❌ Fout bij initialiseren Whisper: {e}")
            return False
    
    def transcribe_audio(self, audio_path: str, language: str = "en", 
                        progress_callback: Optional[callable] = None,
                        stop_callback: Optional[callable] = None) -> Dict[str, Any]:
        """Transcribeer audio bestand met Whisper"""
        try:
            # Controleer of whisper geïnitialiseerd is
            if not self.is_initialized:
                logger.log_debug("❌ Whisper niet geïnitialiseerd")
                return {"error": "Whisper niet geïnitialiseerd"}
            
            # Controleer of audio bestand bestaat
            if not os.path.exists(audio_path):
                logger.log_debug(f"❌ Audio bestand niet gevonden: {audio_path}")
                return {"error": "Audio bestand niet gevonden"}
            
            # Controleer of audio bestand leesbaar is
            try:
                file_size = os.path.getsize(audio_path)
                if file_size == 0:
                    logger.log_debug(f"❌ Audio bestand is leeg: {audio_path}")
                    return {"error": "Audio bestand is leeg"}
                if DEBUG_MODE:
                    logger.log_debug(f"📁 Audio bestand grootte: {file_size} bytes")
            except Exception as e:
                logger.log_debug(f"❌ Kan audio bestand niet lezen: {e}")
                return {"error": f"Kan audio bestand niet lezen: {e}"}
            
            if DEBUG_MODE:
                logger.log_debug(f"🎤 Start transcriptie: {safe_basename(audio_path)}")
            
            # Progress callback wrapper
            def progress_wrapper(progress):
                if progress_callback:
                    # Gebruik voortgangsbalk in plaats van percentage
                    progress_bar = create_progress_bar(progress, 40, safe_basename(audio_path))
                    progress_callback(progress_bar)
                # Alleen log bij belangrijke milestones als debug mode aan staat
                if DEBUG_MODE and progress in [0.0, 0.25, 0.5, 0.75, 1.0]:
                    logger.log_debug(f"🎤 Whisper: {progress:.0%} - {safe_basename(audio_path)}")
            
            # Voer transcriptie uit met progress tracking
            import whisper
            import time
            
            # Gebruik standaard Engels als taal
            whisper_language = "en"
            
            # Start progress tracking
            start_time = time.time()
            if progress_callback:
                progress_wrapper(0.0)  # Start op 0%
                if DEBUG_MODE:
                    logger.log_debug("🎤 Whisper: Audio laden...")
            
            # Laad audio bestand
            audio = whisper.load_audio(audio_path)
            if progress_callback:
                progress_wrapper(0.15)  # 15% - Audio geladen
                if DEBUG_MODE:
                    logger.log_debug("🎤 Whisper: Audio voorbereiden...")
            
            # Pad en trim audio
            audio = whisper.pad_or_trim(audio)
            if progress_callback:
                progress_wrapper(0.25)  # 25% - Audio geprepareerd
                if DEBUG_MODE:
                    logger.log_debug("🎤 Whisper: Mel spectrogram genereren...")
            
            # Genereer mel spectrogram
            mel = whisper.log_mel_spectrogram(audio).to(self.current_model.device)
            if progress_callback:
                progress_wrapper(0.35)  # 35% - Mel spectrogram voltooid
                if DEBUG_MODE:
                    logger.log_debug("🎤 Whisper: Transcriptie starten...")
            
            # Voer transcriptie uit met real-time progress updates
            if progress_callback:
                progress_wrapper(0.45)  # 45% - Transcriptie start
                if DEBUG_MODE:
                    logger.log_debug("🎤 Whisper: Transcriptie bezig...")
            
            # Real-time progress tracking tijdens transcriptie
            import threading
            import time
            
            # Start een timer om progress te simuleren tijdens transcriptie
            progress_value = 0.45
            progress_stopped = False
            transcription_complete = False
            
            def update_progress():
                nonlocal progress_value, progress_stopped, transcription_complete
                while not progress_stopped and not transcription_complete:
                    # Check voor stop signal
                    if stop_callback and stop_callback():
                        if DEBUG_MODE:
                            logger.log_debug("🛑 Whisper transcriptie gestopt door gebruiker")
                        progress_stopped = True
                        break
                    
                    time.sleep(1.0)  # Update elke 1 seconde voor realistischere updates
                    progress_value += 0.005  # Zeer kleine increment voor realistische progress
                    
                    # Ga door tot 90% als transcriptie klaar is
                    if transcription_complete:
                        progress_value = 1.0
                        break
                    elif progress_value >= 0.90:
                        # Wacht tot transcriptie klaar is
                        continue
                    
                    if progress_callback:
                        progress_wrapper(progress_value)
            
            # Start progress thread
            progress_thread = threading.Thread(target=update_progress, daemon=True)
            progress_thread.start()
            
            # Voer transcriptie uit met error handling
            try:
                # Zorg ervoor dat stdout/stderr correct zijn ingesteld voor PyInstaller
                import sys
                import io
                
                # Backup van originele streams
                original_stdout = sys.stdout
                original_stderr = sys.stderr
                
                # Stel dummy streams in als de originele None zijn
                if sys.stdout is None:
                    sys.stdout = io.StringIO()
                if sys.stderr is None:
                    sys.stderr = io.StringIO()
                
                try:
                    result = self.current_model.transcribe(
                        audio_path,
                        language=whisper_language,
                        verbose=False
                    )
                    # Markeer transcriptie als voltooid
                    transcription_complete = True
                except RuntimeError as e:
                    error_msg = str(e)
                    if "channels" in error_msg or "size" in error_msg or "dimension" in error_msg or "Unsupported language" in error_msg:
                        logger.log_debug(f"⚠️ Transcriptie gefaald, probeer met 'en' als fallback: {error_msg}")
                        # Laatste poging met Engels als fallback
                        result = self.current_model.transcribe(
                            audio_path,
                            language="en",
                            verbose=False
                        )
                        transcription_complete = True
                    else:
                        raise e
                finally:
                    # Herstel originele streams
                    sys.stdout = original_stdout
                    sys.stderr = original_stderr
            finally:
                # Stop progress thread
                progress_stopped = True
                transcription_complete = True
            
            # Check of transcriptie gestopt is
            if stop_callback and stop_callback():
                if DEBUG_MODE:
                    logger.log_debug("🛑 Whisper transcriptie gestopt")
                return {"error": "Transcriptie gestopt door gebruiker"}
            
            # Update progress naar 100% bij voltooiing
            if progress_callback:
                progress_wrapper(1.0)  # Voltooid op 100%
            
            elapsed_time = time.time() - start_time
            if DEBUG_MODE:
                logger.log_debug(f"⏱️ Transcriptie voltooid in {elapsed_time:.1f} seconden")
            
            # Verwerk resultaat
            transcriptions = []
            full_text = ""
            for segment in result["segments"]:
                segment_text = segment["text"].strip()
                transcriptions.append({
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment_text,
                    "language": result.get("language", language)
                })
                full_text += segment_text + " "
            
            # Verwijder extra spaties
            full_text = full_text.strip()
            
            # Check of er daadwerkelijk spraak is gedetecteerd
            if not full_text or full_text.isspace():
                if DEBUG_MODE:
                    logger.log_debug(f"⚠️ Geen spraak gedetecteerd in: {safe_basename(audio_path)}")
                full_text = "[Geen spraak gedetecteerd in deze video]"
                transcriptions = [{
                    "start": 0.0,
                    "end": 10.0,
                    "text": full_text,
                    "language": result.get("language", language)
                }]
            
            if DEBUG_MODE:
                logger.log_debug(f"✅ Transcriptie voltooid: {len(transcriptions)} segmenten, {len(full_text)} karakters")
            
            return {
                "success": True,
                "transcript": full_text,  # Gebruik "transcript" voor consistentie
                "transcriptions": transcriptions,
                "language": result.get("language", language),
                "duration": result.get("duration", 0),
                "segments": len(transcriptions)
            }
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij transcriptie: {e}")
            return {"error": str(e)}
    
    def detect_language(self, audio_path: str) -> str:
        """Detecteer taal van audio bestand - standaard Engels"""
        try:
            if not self.is_initialized:
                logger.log_debug("❌ Whisper niet geïnitialiseerd voor taal detectie")
                return "en"
            
            logger.log_debug(f"🌍 Taal detectie: {safe_basename(audio_path)} - standaard Engels")
            
            # Retourneer standaard Engels
            return "en"
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij taal detectie: {e}")
            return "en"
    
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