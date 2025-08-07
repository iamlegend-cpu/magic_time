"""
Fast Whisper processor voor Magic Time Studio
Beheert audio transcriptie met Fast Whisper (geoptimaliseerde versie van OpenAI Whisper)
"""

import os
import tempfile
import subprocess
import json
import sys
import time
from typing import Dict, Any, List, Optional, Tuple

# Probeer onnxruntime te importeren voor VAD ondersteuning
try:
    import onnxruntime
    ONNX_RUNTIME_AVAILABLE = True
except ImportError:
    ONNX_RUNTIME_AVAILABLE = False

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
    """Processor voor Fast Whisper audio transcriptie"""
    
    def __init__(self):
        # Fast Whisper ondersteunt meer modellen inclusief large-v3-turbo
        self.available_models = [
            "tiny", "base", "small", "medium", "large",
            "large-v1", "large-v2", "large-v3", 
            "large-v3-turbo", "turbo"  # Nieuwe turbo modellen
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
        self.current_model = None
        self.is_initialized = False
        self.last_progress_line = ""  # Added for static progress
        
        # Laad configuratie uit environment variables
        self.default_model = config_manager.get_env("DEFAULT_FAST_WHISPER_MODEL", "large-v3-turbo")
        # Device: kies cuda als beschikbaar, anders cpu
        requested_device = config_manager.get_env("FAST_WHISPER_DEVICE", "auto")
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
            logger.log_debug(f"[DEBUG] Fast Whisper device ingesteld op: {self.device}")
        
    def _print_static_progress(self, message: str, end: str = "\r"):
        """Print een statische voortgangsbalk die op dezelfde regel blijft"""
        # Wis de vorige regel als die langer is
        if len(self.last_progress_line) > len(message):
            print(" " * len(self.last_progress_line), end="\r")
        
        print(message, end=end)
        self.last_progress_line = message
        
        # Force flush voor real-time output
        sys.stdout.flush()
    
    def _clear_progress_line(self):
        """Wis de huidige voortgangsregel"""
        if self.last_progress_line:
            print(" " * len(self.last_progress_line), end="\r")
            self.last_progress_line = ""
            sys.stdout.flush()

    def initialize(self, model_name: str = None) -> bool:
        """Initialiseer Fast Whisper met specifiek model"""
        try:
            # Gebruik default model als geen model opgegeven
            if model_name is None:
                model_name = self.default_model
            
            if model_name not in self.available_models:
                if DEBUG_MODE:
                    logger.log_debug(f"❌ Onbekend Fast Whisper model: {model_name}")
                return False
            
            # Probeer Fast Whisper te importeren
            try:
                from faster_whisper import WhisperModel
                
                # Probeer eerst CUDA, fallback naar CPU als dat faalt
                try:
                    if DEBUG_MODE:
                        logger.log_debug(f"🔍 [DEBUG] Fast Whisper: Probeer CUDA initialisatie met model: {model_name}")
                    
                    self.current_model = WhisperModel(
                        model_name, 
                        device="cuda",
                        compute_type="float16"
                    )
                    
                    self.is_initialized = True
                    if DEBUG_MODE:
                        logger.log_debug(f"✅ Fast Whisper model '{model_name}' geladen op CUDA")
                    return True
                    
                except Exception as cuda_error:
                    if DEBUG_MODE:
                        logger.log_debug(f"⚠️ CUDA initialisatie gefaald: {cuda_error}")
                        logger.log_debug("🔄 Probeer CPU fallback...")
                    
                    # Fallback naar CPU
                    self.current_model = WhisperModel(
                        model_name, 
                        device="cpu",
                        compute_type="int8"
                    )
                    
                    self.is_initialized = True
                    if DEBUG_MODE:
                        logger.log_debug(f"✅ Fast Whisper model '{model_name}' geladen op CPU (fallback)")
                    return True
                    
            except ImportError:
                logger.log_debug("❌ Fast Whisper niet geïnstalleerd. Installeer met: pip install faster-whisper")
                return False
            except Exception as e:
                if DEBUG_MODE:
                    logger.log_debug(f"❌ Fout bij laden Fast Whisper model: {e}")
                return False
                
        except Exception as e:
            if DEBUG_MODE:
                logger.log_debug(f"❌ Fout bij initialiseren Fast Whisper: {e}")
            return False
    
    def transcribe_audio(self, audio_path: str, language: str = "en", 
                        progress_callback: Optional[callable] = None,
                        stop_callback: Optional[callable] = None) -> Dict[str, Any]:
        """Transcribeer audio bestand met Fast Whisper"""
        try:
            if not self.is_initialized:
                logger.log_debug("❌ Fast Whisper niet geïnitialiseerd")
                return {"error": "Fast Whisper niet geïnitialiseerd"}
            
            # Normaliseer het audio pad om backslash problemen te voorkomen
            audio_path = os.path.normpath(audio_path)
            
            print(f"🔍 [DEBUG] Fast Whisper: Start transcriptie van {safe_basename(audio_path)}")
            print(f"🔍 [DEBUG] Fast Whisper: Audio pad: {audio_path}")
            
            # Check of audio bestand bestaat
            if not os.path.exists(audio_path):
                logger.log_debug(f"❌ Audio bestand niet gevonden: {audio_path}")
                return {"error": f"Audio bestand niet gevonden: {audio_path}"}
            
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
                logger.log_debug(f"🎤 Start Fast Whisper transcriptie: {safe_basename(audio_path)}")
            
            # Progress callback wrapper
            def progress_wrapper(progress):
                # Beperk progress tot 100%
                progress_bar = min(progress, 1.0)
                
                # Voeg extra feedback toe tijdens "vastgelopen" fase (85-95%)
                if 0.85 <= progress_bar <= 0.95:
                    progress_message = f"🎤 Fast Whisper: {progress_bar:.1%} (GPU verwerking...) - {safe_basename(audio_path)}"
                else:
                    progress_message = f"🎤 Fast Whisper: {progress_bar:.1%} - {safe_basename(audio_path)}"
                
                self._print_static_progress(progress_message)
                
                if progress_callback:
                    # Controleer of callback nog geldig is
                    try:
                        result = progress_callback(progress_bar)
                        if result is False:  # Callback vraagt om te stoppen
                            return False
                    except Exception as e:
                        print(f"🔍 [DEBUG] Fast Whisper callback error: {e}")
                        return False
                # Alleen log bij belangrijke milestones als debug mode aan staat
                if DEBUG_MODE and progress_bar in [0.0, 0.25, 0.5, 0.75, 0.85, 1.0]:
                    logger.log_debug(f"🎤 Fast Whisper: {progress_bar:.0%} - {safe_basename(audio_path)}")
                return True
            
            # Voer transcriptie uit met progress tracking
            import time
            
            # Start progress tracking
            start_time = time.time()
            if progress_callback:
                progress_wrapper(0.0)  # Start op 0%
                if DEBUG_MODE:
                    logger.log_debug("🎤 Fast Whisper: Audio laden...")
            
            # Real-time progress tracking tijdens transcriptie
            import threading
            import time
            
            # Start een timer om progress te simuleren tijdens transcriptie
            progress_value = 0.0
            progress_stopped = False
            transcription_complete = False
            
            def update_progress():
                nonlocal progress_value, progress_stopped, transcription_complete
                while not progress_stopped and not transcription_complete:
                    # Check voor stop signal
                    if stop_callback and stop_callback():
                        if DEBUG_MODE:
                            logger.log_debug("🛑 Fast Whisper transcriptie gestopt door gebruiker")
                        progress_stopped = True
                        break
                    
                    time.sleep(0.2)  # Langzamere updates om GPU werk te simuleren
                    progress_value += 0.003  # Kleinere increment voor realistischere progress
                    
                    # Beperk progress tot 95% (laat 5% over voor finale verwerking)
                    if progress_value > 0.95:
                        progress_value = 0.95
                    
                    # Als transcriptie klaar is, ga naar 100%
                    if transcription_complete:
                        progress_value = 1.0
                        if progress_callback:
                            print(f"🔍 [DEBUG] Fast Whisper: Progress naar 100% na voltooiing")
                            progress_wrapper(1.0)  # Update naar 100%
                        # Wis de progress line bij voltooiing
                        self._clear_progress_line()
                        break
                    elif progress_value >= 0.85:
                        # Wacht tot transcriptie klaar is, maar update nog steeds
                        # Dit simuleert de "vastgelopen" fase waar GPU nog bezig is
                        if progress_callback:
                            if not progress_wrapper(progress_value):
                                # Callback vraagt om te stoppen
                                progress_stopped = True
                                break
                        continue
                    
                    if progress_callback:
                        if not progress_wrapper(progress_value):
                            # Callback vraagt om te stoppen
                            progress_stopped = True
                            break
            
            # Start progress thread
            progress_thread = threading.Thread(target=update_progress, daemon=True)
            progress_thread.start()
            
            # Voer transcriptie uit met Fast Whisper
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
                
                # Probeer transcriptie met VAD filter
                vad_available = ONNX_RUNTIME_AVAILABLE
                if not vad_available:
                    logger.log_debug("⚠️ onnxruntime niet beschikbaar, VAD wordt uitgeschakeld")
                
                try:
                    if vad_available:
                        segments, info = self.current_model.transcribe(
                            audio_path,
                            language=language,
                            beam_size=5,
                            best_of=5,
                            vad_filter=True,  # VAD filter aan
                            vad_parameters=dict(min_silence_duration_ms=500)
                        )
                    else:
                        # VAD niet beschikbaar, gebruik zonder VAD
                        segments, info = self.current_model.transcribe(
                            audio_path,
                            language=language,
                            beam_size=5,
                            best_of=5,
                            vad_filter=False,  # VAD filter uit
                            vad_parameters=None
                        )
                except Exception as vad_error:
                    # Als VAD filter faalt, probeer zonder VAD
                    if "VAD filter" in str(vad_error) or "onnxruntime" in str(vad_error):
                        logger.log_debug(f"⚠️ VAD filter gefaald, probeer zonder VAD: {vad_error}")
                        segments, info = self.current_model.transcribe(
                            audio_path,
                            language=language,
                            beam_size=5,
                            best_of=5,
                            vad_filter=False,  # VAD filter uit als fallback
                            vad_parameters=None
                        )
                    else:
                        # Andere fout, probeer met Engels als fallback
                        logger.log_debug(f"⚠️ Transcriptie gefaald, probeer met 'en' als fallback: {vad_error}")
                        try:
                            if vad_available:
                                segments, info = self.current_model.transcribe(
                                    audio_path,
                                    language="en",
                                    beam_size=5,
                                    best_of=5,
                                    vad_filter=True,  # VAD filter aan
                                    vad_parameters=dict(min_silence_duration_ms=500)
                                )
                            else:
                                segments, info = self.current_model.transcribe(
                                    audio_path,
                                    language="en",
                                    beam_size=5,
                                    best_of=5,
                                    vad_filter=False,  # VAD filter uit
                                    vad_parameters=None
                                )
                        except Exception as vad_error2:
                            # Als VAD filter faalt, probeer zonder VAD
                            if "VAD filter" in str(vad_error2) or "onnxruntime" in str(vad_error2):
                                logger.log_debug(f"⚠️ VAD filter gefaald, probeer zonder VAD: {vad_error2}")
                                segments, info = self.current_model.transcribe(
                                    audio_path,
                                    language="en",
                                    beam_size=5,
                                    best_of=5,
                                    vad_filter=False,  # VAD filter uit als fallback
                                    vad_parameters=None
                                )
                            else:
                                raise vad_error2
                
                # Markeer transcriptie als voltooid
                transcription_complete = True
                print(f"🔍 [DEBUG] Fast Whisper transcriptie voltooid: {safe_basename(audio_path)}")
                print(f"🔍 [DEBUG] Fast Whisper: Start verwerking van {len(list(segments))} segmenten...")
                
                # Wacht even tot progress thread stopt
                time.sleep(1.0)
                
                # Verwerk resultaten
                transcriptions = []
                full_text = ""
                
                for segment in segments:
                    segment_text = segment.text.strip()
                    transcriptions.append({
                        "start": segment.start,
                        "end": segment.end,
                        "text": segment_text,
                        "language": info.language
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
                        "language": info.language
                    }]
                
                if DEBUG_MODE:
                    logger.log_debug(f"✅ Fast Whisper transcriptie voltooid: {len(transcriptions)} segmenten, {len(full_text)} karakters")
                
                result = {
                    "success": True,
                    "transcript": full_text,
                    "transcriptions": transcriptions,
                    "language": info.language,
                    "duration": info.duration,
                    "segments": len(transcriptions)
                }
                
            finally:
                # Herstel originele streams
                sys.stdout = original_stdout
                sys.stderr = original_stderr
                
                # Stop progress thread
                progress_stopped = True
                transcription_complete = True
                print(f"🔍 [DEBUG] Fast Whisper progress thread gestopt: {safe_basename(audio_path)}")
                
                # Wacht tot progress thread stopt
                if 'progress_thread' in locals() and progress_thread.is_alive():
                    if DEBUG_MODE:
                        logger.log_debug("🛑 Wacht tot progress thread stopt...")
                    progress_thread.join(timeout=3.0)  # Wacht maximaal 3 seconden
                    if DEBUG_MODE:
                        logger.log_debug("✅ Progress thread gestopt")
            
            # Check of transcriptie gestopt is
            if stop_callback and stop_callback():
                if DEBUG_MODE:
                    logger.log_debug("🛑 Fast Whisper transcriptie gestopt")
                return {"error": "Transcriptie gestopt door gebruiker"}
            
            # Update progress naar 100% bij voltooiing
            if progress_callback:
                print(f"🔍 [DEBUG] Fast Whisper: Finale progress update naar 100%")
                progress_wrapper(1.0)  # Voltooid op 100%
                # Wis de progress line bij voltooiing
                self._clear_progress_line()
            
            elapsed_time = time.time() - start_time
            if DEBUG_MODE:
                logger.log_debug(f"⏱️ Fast Whisper transcriptie voltooid in {elapsed_time:.1f} seconden")
            
            return result
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij Fast Whisper transcriptie: {e}")
            return {"error": str(e)}
    
    def detect_language(self, audio_path: str) -> str:
        """Detecteer taal van audio bestand met Fast Whisper"""
        try:
            if not self.is_initialized:
                logger.log_debug("❌ Fast Whisper niet geïnitialiseerd voor taal detectie")
                return "en"
            
            logger.log_debug(f"🌍 Fast Whisper taal detectie: {safe_basename(audio_path)}")
            
            # Fast Whisper kan automatisch taal detecteren
            segments, info = self.current_model.transcribe(
                audio_path,
                language=None,  # Auto-detect
                beam_size=1,
                best_of=1
            )
            
            detected_language = info.language
            if DEBUG_MODE:
                logger.log_debug(f"🌍 Gedetecteerde taal: {detected_language}")
            
            return detected_language
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij Fast Whisper taal detectie: {e}")
            return "en"
    
    def get_model_info(self) -> Dict[str, Any]:
        """Krijg informatie over huidig Fast Whisper model"""
        if not self.is_initialized:
            return {"error": "Model niet geladen"}
        
        try:
            return {
                "model_name": self.current_model.model_name if hasattr(self.current_model, 'model_name') else "unknown",
                "device": str(self.device),  # Gebruik self.device in plaats van self.current_model.device
                "compute_type": self.current_model.compute_type if hasattr(self.current_model, 'compute_type') else "unknown",
                "is_multilingual": True
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_available_models(self) -> List[str]:
        """Krijg lijst van beschikbare Fast Whisper modellen"""
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
            logger.log_debug("🧹 Fast Whisper resources opgeruimd")
        except Exception as e:
            logger.log_debug(f"❌ Fout bij opruimen Fast Whisper: {e}")

# Globale Whisper processor instantie
whisper_processor = WhisperProcessor() 