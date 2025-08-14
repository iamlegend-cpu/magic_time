"""
Whisper Processor Module voor Magic Time Studio
Handelt speech-to-text transcriptie af met WhisperX (enige ondersteunde optie)
"""

import os
from typing import Optional, Dict, Any

# Import alleen WhisperX
try:
    from ..whisperx_processor import WhisperXProcessor
    from ..whisper_manager import whisper_manager
except ImportError:
    # Fallback als imports falen
    WhisperXProcessor = None
    whisper_manager = None

class WhisperProcessor:
    """Whisper transcriptie module - alleen WhisperX ondersteund"""
    
    def __init__(self, processing_thread):
        self.processing_thread = processing_thread
        
        # Gebruik singleton WhisperX processor
        self.whisperx_processor = WhisperXProcessor()
        
        self.settings = None  # Instellingen worden later ingesteld
        
        # Initialiseer Whisper manager (zonder model te laden)
        if whisper_manager:
            # Detecteer automatisch beste device en compute type
            whisper_type = "whisperx"  # Alleen WhisperX ondersteund
            
            # Detecteer automatisch beste device
            device, compute_type = self._detect_best_device()
            
            print(f"🚀 WhisperProcessor: {whisper_type} - wacht op model instellingen")
            
            # Stel GPU instellingen in
            whisper_manager.set_gpu_device(device)
            whisper_manager.set_compute_type(compute_type)
            
            # Initialiseer whisper manager (zonder model)
            whisper_manager.initialize(whisper_type, None)
            
            print(f"✅ WhisperProcessor geïnitialiseerd - wacht op model instellingen")
        else:
            print("⚠️ Whisper manager niet beschikbaar")
    
    def _detect_best_device(self):
        """Detecteer automatisch beste device en compute type"""
        try:
            import torch
            
            # Schakel TF32 in voor betere prestaties en om waarschuwingen te voorkomen
            try:
                torch.backends.cuda.matmul.allow_tf32 = True
                torch.backends.cudnn.allow_tf32 = True
                print("✅ TF32 ingeschakeld voor betere CUDA prestaties")
            except Exception as e:
                print(f"⚠️ Kon TF32 niet inschakelen: {e}")
            
            if torch.cuda.is_available():
                # CUDA beschikbaar - gebruik GPU
                device = "cuda"
                compute_type = "float16"
                print("✅ CUDA gedetecteerd - gebruik GPU")
            else:
                # Geen CUDA - gebruik CPU
                device = "cpu"
                compute_type = "float32"
                print("⚠️ CUDA niet beschikbaar - gebruik CPU")
        except ImportError:
            # PyTorch niet beschikbaar - gebruik CPU
            device = "cpu"
            compute_type = "float32"
            print("⚠️ PyTorch niet beschikbaar - gebruik CPU")
        except Exception as e:
            # Fallback naar CPU bij fouten
            device = "cpu"
            compute_type = "float32"
            print(f"⚠️ Fout bij device detectie: {e} - gebruik CPU")
        
        return device, compute_type
    
    def set_settings(self, settings: dict):
        """Stel instellingen in voor de processor"""
        try:
            if not settings:
                print("⚠️ Geen instellingen ontvangen")
                return
            
            print(f"🔧 Stel WhisperX instellingen in: {settings}")
            
            # Sla instellingen op
            self.settings = settings.copy()
            
            # Haal WhisperX instellingen op
            whisper_type = settings.get("whisper_type", "whisperx")
            whisperx_model = settings.get("whisper_model", "tiny")
            
            # Controleer of VAD instellingen zijn gewijzigd
            current_vad_settings = getattr(self, 'current_vad_settings', {})
            new_vad_settings = {
                "vad_enabled": settings.get("vad_enabled", False),
                "vad_method": settings.get("vad_method", "Silero (snel)"),
                "vad_threshold": settings.get("vad_threshold", 0.5),
                "vad_onset": settings.get("vad_onset", 0.5),
                "vad_chunk_size": settings.get("vad_chunk_size", 30),
                "vad_min_speech": settings.get("vad_min_speech", 0.5),
                "vad_min_silence": settings.get("vad_min_silence", 0.5),
            }
            
            # Controleer of VAD instellingen zijn gewijzigd
            vad_settings_changed = (
                current_vad_settings.get("vad_enabled") != new_vad_settings["vad_enabled"] or
                current_vad_settings.get("vad_method") != new_vad_settings["vad_method"] or
                abs(current_vad_settings.get("vad_threshold", 0.5) - new_vad_settings["vad_threshold"]) > 0.01 or
                abs(current_vad_settings.get("vad_onset", 0.5) - new_vad_settings["vad_onset"]) > 0.01 or
                current_vad_settings.get("vad_chunk_size", 30) != new_vad_settings["vad_chunk_size"] or
                abs(current_vad_settings.get("vad_min_speech", 0.5) - new_vad_settings["vad_min_speech"]) > 0.01 or
                abs(current_vad_settings.get("vad_min_silence", 0.5) - new_vad_settings["vad_min_silence"]) > 0.01
            )
            
            if vad_settings_changed:
                print(f"🔄 VAD instellingen gewijzigd, herlaad model")
                
                # Herlaad model met nieuwe VAD instellingen
                if self.whisperx_processor:
                    success = self.whisperx_processor.reload_model_with_vad_settings(whisperx_model, new_vad_settings)
                    if success:
                        print(f"✅ WhisperX model herladen met VAD instellingen: {whisperx_model}")
                        # Update de huidige VAD instellingen
                        self.current_vad_settings = new_vad_settings.copy()
                    else:
                        print(f"❌ WhisperX model herladen met VAD instellingen gefaald: {whisperx_model}")
                        # Probeer normale herlading als fallback
                        success = self.whisperx_processor.load_model(whisperx_model)
                        if success:
                            print(f"✅ WhisperX model herladen (fallback): {whisperx_model}")
                            self.whisperx_processor.current_model = whisperx_model
                        else:
                            print(f"❌ Fallback naar gekozen model gefaald: {whisperx_model}")
                            # Probeer een kleiner model als fallback
                            fallback_models = ["tiny", "base", "small", "medium", "large-v3"]
                            fallback_success = False
                            
                            for fallback_model in fallback_models:
                                if fallback_model != whisperx_model:
                                    print(f"🔄 Probeer fallback naar {fallback_model} model...")
                                    success = self.whisperx_processor.load_model(fallback_model)
                                    if success:
                                        print(f"✅ WhisperX fallback model geladen: {fallback_model}")
                                        self.whisperx_processor.current_model = fallback_model
                                        fallback_success = True
                                        break
                            
                            if not fallback_success:
                                print(f"❌ Alle fallback modellen gefaald")
            
            # Initialiseer whisper manager met het gekozen model
            if whisper_manager:
                whisper_manager.initialize(whisper_type, whisperx_model)
            
            # Controleer of het model moet worden herladen (alleen als VAD niet is gewijzigd)
            if not vad_settings_changed:
                current_model = getattr(self.whisperx_processor, 'current_model', None)
                if current_model != whisperx_model:
                    print(f"🔄 Model wijziging: {current_model} -> {whisperx_model}")
                    
                    # Herlaad het model met nieuwe instellingen
                    if self.whisperx_processor:
                        success = self.whisperx_processor.load_model(whisperx_model)
                        if success:
                            print(f"✅ WhisperX model herladen: {whisperx_model}")
                            # Update de huidige model referentie
                            self.whisperx_processor.current_model = whisperx_model
                        else:
                            print(f"❌ WhisperX model herladen gefaald: {whisperx_model}")
                            # Probeer een kleiner model als fallback
                            fallback_models = ["tiny", "base", "small", "medium", "large-v3"]
                            fallback_success = False
                            
                            for fallback_model in fallback_models:
                                if fallback_model != whisperx_model:
                                    print(f"🔄 Probeer fallback naar {fallback_model} model...")
                                    success = self.whisperx_processor.load_model(fallback_model)
                                    if success:
                                        print(f"✅ WhisperX fallback model geladen: {fallback_model}")
                                        self.whisperx_processor.current_model = fallback_model
                                        fallback_success = True
                                        break
                            
                            if not fallback_success:
                                print(f"❌ Alle fallback modellen gefaald")
                else:
                    print(f"✅ Model hoeft niet te worden herladen: {whisperx_model}")
            
            print(f"✅ WhisperX instellingen ingesteld: {whisperx_model}")
            
        except Exception as e:
            print(f"❌ Fout bij instellen WhisperX instellingen: {e}")
            import traceback
            traceback.print_exc()
    
    def transcribe_audio(self, audio_path: str, settings: dict = None) -> Optional[Dict[str, Any]]:
        """Transcribeer audio met WhisperX"""
        try:
            if not self.whisperx_processor:
                print("❌ WhisperX processor niet beschikbaar")
                return None
            
            # Gebruik instellingen als beschikbaar, anders defaults
            if settings and isinstance(settings, dict):
                self.set_settings(settings)
            else:
                print(f"⚠️ Geen geldige instellingen ontvangen: {type(settings)} - {settings}")
                # Gebruik standaard instellingen
                default_settings = {
                    "whisper_type": "whisperx",
                    "whisper_model": "tiny",  # Veranderd van "medium" naar "tiny"
                    "language": "en",
                    "vad_enabled": True,  # Altijd VAD aan
                    "vad_method": "Silero (snel)",
                    "vad_threshold": 0.5,
                    "vad_onset": 0.5,
                    "vad_chunk_size": 30,
                    "vad_min_speech": 0.5,
                    "vad_min_silence": 0.5,
                }
                self.set_settings(default_settings)
                
                # Haal de gekozen model naam op uit de settings
                if hasattr(self, 'settings') and self.settings:
                    model_name = self.settings.get("whisper_model", "tiny")
                    print(f"🔍 [DEBUG] WhisperProcessor: Gebruik gekozen model: {model_name}")
                else:
                    model_name = "tiny"
                    print(f"🔍 [DEBUG] WhisperProcessor: Gebruik default model: {model_name}")
            
            # Haal taal instellingen op uit configuratie
            try:
                # Probeer verschillende import methoden
                try:
                    from ...core.config import ConfigManager
                except ImportError:
                    try:
                        from magic_time_studio.core.config import ConfigManager
                    except ImportError:
                        # Fallback naar directe configuratie
                        ConfigManager = None
                
                if ConfigManager:
                    config_manager = ConfigManager()
                    default_language = config_manager.get_env("DEFAULT_LANGUAGE", "en")
                    auto_detect_language = config_manager.get_env("AUTO_DETECT_LANGUAGE", "false").lower() == "true"
                else:
                    # Fallback waarden
                    default_language = "en"
                    auto_detect_language = False
                
                # Bepaal welke taal te gebruiken
                if settings and isinstance(settings, dict) and settings.get('language'):
                    # Gebruik taal uit settings
                    language = settings.get('language')
                elif auto_detect_language:
                    # Laat WhisperX automatisch taal detecteren
                    language = None
                else:
                    # Gebruik standaard taal uit configuratie
                    language = default_language
                    
            except Exception as e:
                print(f"⚠️ Kon taal configuratie niet laden: {e}")
                # Fallback naar Engels
                language = "en"
            
            # Maak progress callback functie die updates doorgeeft aan GUI
            def progress_callback(progress: float, message: str):
                """Progress callback voor WhisperX transcriptie met GUI updates"""
                try:
                    # Converteer naar percentage (0-100)
                    percentage = int(progress * 100)
                    
                    # Stuur progress update naar processing thread voor GUI update
                    if hasattr(self.processing_thread, 'progress_updated'):
                        self.processing_thread.progress_updated.emit(percentage, message)
                    
                except Exception as e:
                    print(f"⚠️ Fout in progress callback: {e}")
            
            # Haal VAD instellingen op uit de huidige settings
            vad_settings = None
            if hasattr(self, 'settings') and self.settings:
                vad_enabled = self.settings.get("vad_enabled", False)
                
                # Alleen VAD instellingen doorgeven als VAD daadwerkelijk is ingeschakeld
                if vad_enabled:
                    # Gebruik WhisperX methode naam als beschikbaar, anders UI naam
                    vad_method = self.settings.get("vad_method_whisperx", self.settings.get("vad_method", "silero"))
                    
                    vad_settings = {
                        "vad_enabled": True,
                        "vad_method": vad_method,  # WhisperX methode naam
                        "vad_threshold": self.settings.get("vad_threshold", 0.5),
                        "vad_onset": self.settings.get("vad_onset", 0.5),
                        "vad_chunk_size": self.settings.get("vad_chunk_size", 30),
                        "vad_min_speech": self.settings.get("vad_min_speech", 0.5),
                        "vad_min_silence": self.settings.get("vad_min_silence", 0.5),
                    }
                    print(f"🔧 VAD ingeschakeld - instellingen voor transcriptie: {vad_settings}")
                    print(f"🔧 VAD methode: {vad_method}")
                else:
                    print(f"🔧 VAD uitgeschakeld - geen VAD instellingen doorgegeven")
            
            # Start transcriptie met of zonder VAD instellingen (geen dubbele berichten)
            if vad_settings and vad_settings.get("vad_enabled", False):
                print(f"🎤 Start WhisperX transcriptie met VAD: {audio_path}")
            else:
                print(f"🎤 Start WhisperX transcriptie zonder VAD: {audio_path}")
                
            result = self.whisperx_processor.transcribe_with_alignment(
                audio_path, 
                language=language, 
                progress_callback=progress_callback,
                vad_settings=vad_settings
            )
            
            if result:
                print(f"✅ WhisperX transcriptie voltooid: {len(result.get('transcriptions', []))} segmenten")
                return result
            else:
                print("❌ WhisperX transcriptie gefaald")
                return None
                
        except Exception as e:
            print(f"❌ Fout bij WhisperX transcriptie: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def save_transcript(self, transcript: str, output_path: str) -> bool:
        """Sla transcript op als SRT bestand"""
        try:
            # Maak SRT bestand
            srt_content = f"1\n00:00:00,000 --> 00:00:05,000\n{transcript}\n\n"
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(srt_content)
            
            print(f"✅ Transcript opgeslagen: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Fout bij opslaan transcript: {e}")
            return False
