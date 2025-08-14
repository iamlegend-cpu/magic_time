"""
WhisperX Core Processor
Hoofdklasse voor WhisperX transcriptie met word-level alignment
"""

import os
import time
import shutil
import tempfile
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime, timedelta

import whisperx
import torch

# Import lokale modules
from .whisperx_time_estimator import TimeEstimator
from .whisperx_vad import VADManager, VADTester, VADOptimizer
from .whisperx_utils import (
    convert_to_standard_format, 
    create_accurate_srt, 
    seconds_to_srt_timestamp,
    get_model_info,
    cleanup_cuda_context,
    setup_tf32
)

class WhisperXProcessor:
    """WhisperX implementatie met word-level alignment voor accurate SRT"""
    
    # Singleton instance
    _instance = None
    _lock = None
    
    def __new__(cls):
        """Singleton pattern - zorg ervoor dat er maar één instance is"""
        if cls._instance is None:
            # Thread-safe singleton
            if cls._lock is None:
                import threading
                cls._lock = threading.Lock()
            
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(WhisperXProcessor, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        # Voorkom meerdere initialisaties
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        # Voeg FFmpeg toe aan PATH vanuit assets directory
        from .import_utils import setup_ffmpeg_path
        setup_ffmpeg_path()
        
        # Schakel TF32 in voor betere prestaties
        setup_tf32()
        
        self.model = None
        self.align_model = None
        self.align_extend = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.compute_type = "float16" if self.device == "cuda" else "float32"
        self.is_loaded = False
        self.gpu_available = torch.cuda.is_available()
        self.current_model = None  # Houd bij welk model geladen is
        
        # Initialiseer modules
        self.time_estimator = TimeEstimator()
        self.vad_manager = VADManager()
        
        print(f"🔧 WhisperX Processor geïnitialiseerd op {self.device}")
        if self.gpu_available:
            print(f"🎯 GPU: {torch.cuda.get_device_name(0)}")
        
        # Markeer als geïnitialiseerd
        self._initialized = True
    
    def load_model(self, model_name: str = "large-v3") -> bool:
        """Laad WhisperX model met VAD (altijd ingeschakeld)"""
        try:
            print(f"📥 Laad WhisperX model: {model_name} op {self.device}")
            
            # Laad WhisperX model MET VAD opties (altijd ingeschakeld)
            # Probeer verschillende VAD methoden in volgorde van voorkeur
            vad_methods = ["silero", "pyannote", "auditok"]
            vad_method = "silero"  # Standaard fallback
            
            # Probeer de beste VAD methode te gebruiken
            for method in vad_methods:
                try:
                    print(f"🔍 Probeer VAD methode: {method}")
                    self.model = whisperx.load_model(
                        model_name, 
                        self.device, 
                        compute_type=self.compute_type,
                        language=None,  # Auto-detect
                        vad_method=method,  # Probeer deze VAD methode
                        vad_options={
                            "chunk_size": 30,  # Standaard chunk size
                            "vad_onset": 0.5,  # Standaard onset threshold
                            "vad_offset": 0.5,  # Standaard offset threshold
                        }
                    )
                    vad_method = method
                    print(f"✅ VAD methode {method} succesvol geladen")
                    break
                except Exception as e:
                    print(f"⚠️ VAD methode {method} gefaald: {e}")
                    continue
            
            if not self.model:
                # Fallback naar model zonder VAD als alle methoden falen
                print("⚠️ Alle VAD methoden gefaald, laad model zonder VAD")
                self.model = whisperx.load_model(
                    model_name, 
                    self.device, 
                    compute_type=self.compute_type,
                    language=None
                )
                vad_method = "geen"
            
            print(f"✅ WhisperX model geladen met VAD methode: {vad_method}")
            
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
            print(f"✅ WhisperX model geladen: {model_name}")
            return True
            
        except Exception as e:
            print(f"❌ Fout bij laden WhisperX model: {e}")
            return False
    
    def reload_model_with_vad_settings(self, model_name: str, vad_settings: Dict[str, Any]) -> bool:
        """Herlaad WhisperX model met VAD instellingen (altijd ingeschakeld)"""
        print(f"🔄 Herlaad WhisperX model met VAD instellingen: {model_name}")
        
        # VAD is altijd ingeschakeld, gebruik instellingen of standaard waarden
        if vad_settings and vad_settings.get("vad_enabled", True):
            # Converteer VAD methode naar WhisperX formaat
            whisperx_vad_method = self.vad_manager.convert_vad_method(
                vad_settings.get("vad_method", "Silero (snel)")
            )
            
            # Maak VAD opties
            vad_options = self.vad_manager.create_vad_options(vad_settings)
            
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
        
        # Laad WhisperX model MET VAD instellingen
        self.model = whisperx.load_model(
            model_name, 
            self.device, 
            compute_type=self.compute_type,
            language=None,  # Auto-detect
            vad_method=whisperx_vad_method,
            vad_options=vad_options
        )
        
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
        print(f"✅ WhisperX model herladen: {model_name}")
        print(f"🎯 VAD methode: {whisperx_vad_method}")
        print(f"🎯 VAD opties: {vad_options}")
        return True
    
    def transcribe_with_alignment(self, audio_path: str, language: Optional[str] = None, 
                                 progress_callback: Optional[Callable[[float, str], None]] = None,
                                 vad_settings: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Transcribeer audio met WhisperX en word-level alignment"""
        try:
            # Controleer of model geladen is
            if not self.model:
                print("❌ WhisperX model niet geladen")
                return None
            
            # Controleer of audio bestand bestaat
            if not os.path.exists(audio_path):
                print(f"❌ Audio bestand niet gevonden: {audio_path}")
                return None
            
            # Laad VAD instellingen uit configuratie als niet opgegeven
            if vad_settings is None:
                try:
                    from ...core.config import ConfigManager
                    config_manager = ConfigManager()
                    vad_enabled = config_manager.get("vad_enabled", False)
                    
                    # Alleen VAD instellingen laden als VAD daadwerkelijk is ingeschakeld
                    if vad_enabled:
                        vad_settings = {
                            "vad_enabled": True,
                            "vad_method": config_manager.get("vad_method", "Silero (snel)"),
                            "vad_threshold": config_manager.get("vad_threshold", 0.5),
                            "vad_onset": config_manager.get("vad_onset", 0.5),
                            "vad_chunk_size": config_manager.get("vad_chunk_size", 30),
                            "vad_min_speech": config_manager.get("vad_min_speech", 0.5),
                            "vad_min_silence": config_manager.get("vad_min_silence", 0.5),
                        }
                    else:
                        vad_settings = {"vad_enabled": False}
                except Exception as e:
                    print(f"⚠️ Kon VAD instellingen niet laden uit configuratie: {e}")
                    # Fallback naar VAD uitgeschakeld
                    vad_settings = {"vad_enabled": False}
            
            # Controleer of VAD daadwerkelijk is ingeschakeld
            vad_enabled = vad_settings.get("vad_enabled", False) if vad_settings else False
            
            # Bereken ETA voor deze transcriptie
            audio_duration = self.time_estimator.get_audio_duration(audio_path)
            if audio_duration:
                # Haal huidige model naam op
                model_name = getattr(self.model, 'name', 'large-v3')
                eta_info = self.time_estimator.estimate_time(audio_duration, model_name, self.device)
                if eta_info:
                    eta_message = self.time_estimator.format_eta(eta_info)
                    print(f"⏱️ {eta_message}")
                    if progress_callback:
                        progress_callback(0.02, f"⏱️ {eta_message}")
                else:
                    print(f"⏱️ Audio duur: {audio_duration:.1f}s | Model: {model_name}")
            else:
                print("⏱️ Kon audio duur niet bepalen voor ETA")
            
            # Stap 1: Basis transcriptie met of zonder VAD
            if vad_enabled:
                if progress_callback:
                    progress_callback(0.05, "🎤 WhisperX: Start basis transcriptie met VAD...")
                
                try:
                    print(f"🎯 Start WhisperX transcriptie met VAD: {audio_path}")
                    print(f"🔧 VAD instellingen: methode={vad_settings.get('vad_method', 'Silero')}, threshold={vad_settings.get('vad_threshold', 0.5):.2f}, onset={vad_settings.get('vad_onset', 0.5):.2f}")
                    
                    if progress_callback:
                        progress_callback(0.1, "🎤 WhisperX: Basis transcriptie met VAD...")
                except Exception as e:
                    print(f"❌ Fout bij VAD transcriptie: {e}")
                    vad_enabled = False  # Fallback naar transcriptie zonder VAD
            else:
                # VAD is uitgeschakeld - gebruik basis transcriptie
                if progress_callback:
                    progress_callback(0.05, "🎤 WhisperX: Start basis transcriptie zonder VAD...")
                
                print(f"🎤 Start WhisperX transcriptie zonder VAD: {audio_path}")
                print(f"🔧 VAD uitgeschakeld - gebruik basis transcriptie")
                
                if progress_callback:
                    progress_callback(0.1, "🎤 WhisperX: Basis transcriptie zonder VAD...")
            
            # Voer basis transcriptie uit
            try:
                if vad_enabled:
                    # Met VAD - gebruik chunk_size voor betere segmentatie
                    result = self.model.transcribe(
                        audio_path,
                        language=language,
                        chunk_size=vad_settings.get("vad_chunk_size", 30)
                    )
                else:
                    # Zonder VAD - gebruik standaard transcriptie
                    result = self.model.transcribe(
                        audio_path,
                        language=language
                        # Geen chunk_size - voorkomt VAD gebruik
                    )
                
                if progress_callback:
                    progress_callback(0.3, f"🎤 WhisperX: Basis transcriptie voltooid ({len(result.get('segments', []))} segmenten)")
                
            except Exception as e:
                print(f"❌ Fout bij basis transcriptie: {e}")
                return None
            
            # Stap 2: Language detection en alignment model (10% van de tijd)
            if progress_callback:
                progress_callback(0.35, "🎤 WhisperX: Language detection...")
            
            # Voer alleen taal detectie uit als geen taal is ingesteld
            if language is None:
                language = result["language"]
                print(f"🌍 Gedetecteerde taal: {language}")
            else:
                print(f"🌍 Gebruik ingestelde taal: {language}")
            
            if progress_callback:
                progress_callback(0.4, f"🌍 Taal: {language}")
            
            # Skip alignment als VAD is uitgeschakeld om Pyannote VAD te voorkomen
            if not vad_enabled:
                print(f"🔧 VAD uitgeschakeld - skip word-level alignment om Pyannote VAD te voorkomen")
                if progress_callback:
                    progress_callback(0.9, "🔧 Word-level alignment overgeslagen (VAD uitgeschakeld)")
                
                # Return basis transcriptie zonder alignment
                return {
                    "transcriptions": convert_to_standard_format({"segments": result["segments"]}),
                    "language": language,
                    "word_alignments": [],
                    "model": "whisperx"
                }
            
            # VAD is ingeschakeld - voer alignment uit
            if progress_callback:
                progress_callback(0.45, "🎤 WhisperX: Alignment model laden...")
            
            # Laad juiste alignment model voor de taal
            try:
                if self.align_model is None:
                    self.align_model, self.align_extend = whisperx.load_align_model(
                        language_code=language,
                        device=self.device
                    )
                    print(f"✅ Alignment model geladen voor taal: {language}")
                else:
                    print(f"✅ Alignment model al geladen")
            except Exception as e:
                print(f"❌ Kon alignment model niet laden voor taal {language}: {e}")
                # Fallback naar basis transcriptie zonder alignment
                return {
                    "transcriptions": convert_to_standard_format({"segments": result["segments"]}),
                    "language": language,
                    "word_alignments": [],
                    "model": "whisperx"
                }
            
            # Stap 3: Word-level alignment (50% van de tijd)
            if progress_callback:
                progress_callback(0.5, "🎤 WhisperX: Word-level alignment...")
            
            try:
                # Voer word-level alignment uit
                result = whisperx.align(
                    result["segments"],
                    self.align_model,
                    self.align_extend,
                    audio_path,
                    self.device,
                    return_char_alignments=False
                )
                
                if progress_callback:
                    progress_callback(0.9, "🎤 WhisperX: Word-level alignment voltooid")
                
                print(f"✅ Word-level alignment voltooid: {len(result.get('segments', []))} segmenten")
                
            except Exception as e:
                print(f"❌ Fout bij word-level alignment: {e}")
                # Fallback naar basis transcriptie zonder alignment
                return {
                    "transcriptions": convert_to_standard_format({"segments": result["segments"]}),
                    "language": language,
                    "word_alignments": [],
                    "model": "whisperx"
                }
            
            # Stap 4: Converteer naar standaard formaat (5% van de tijd)
            if progress_callback:
                progress_callback(0.95, "🎤 WhisperX: Converteer naar standaard formaat...")
            
            try:
                # Converteer naar standaard formaat
                transcriptions = convert_to_standard_format(result)
                
                if progress_callback:
                    progress_callback(1.0, "🎤 WhisperX: Transcriptie voltooid!")
                
                print(f"✅ Transcriptie voltooid: {len(transcriptions)} segmenten")
                
                return {
                    "transcriptions": transcriptions,
                    "language": language,
                    "word_alignments": result.get("word_segments", []),
                    "model": "whisperx"
                }
                
            except Exception as e:
                print(f"❌ Fout bij converteren naar standaard formaat: {e}")
                return None
                
        except Exception as e:
            print(f"❌ Fout bij WhisperX transcriptie: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def create_accurate_srt(self, transcriptions: List[Dict[str, Any]], 
                           word_alignments: List[Dict[str, Any]] = None) -> str:
        """Genereer SRT met WhisperX word-level timing voor maximale accuracy"""
        return create_accurate_srt(transcriptions, word_alignments)
    
    def get_model_info(self) -> Dict[str, Any]:
        """Krijg informatie over het geladen model"""
        return get_model_info(self.device, self.compute_type, self.gpu_available, self.is_loaded)
    
    def cleanup(self):
        """Ruim geheugen op - inclusief CUDA/GPU context"""
        try:
            print("🧹 WhisperX geheugen opruimen...")
            
            # Stop CUDA context eerst
            cleanup_cuda_context()
            
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
    
    def test_vad_settings(self, audio_path: str, vad_settings: Dict[str, Any]) -> Dict[str, Any]:
        """Test VAD instellingen op een kort audio fragment"""
        if not self.model:
            return {"success": False, "error": "Model niet geladen"}
        
        vad_tester = VADTester(self.model)
        return vad_tester.test_vad_settings(audio_path, vad_settings)
    
    def optimize_vad_settings(self, audio_path: str, target_speech_ratio: float = 0.6) -> Dict[str, Any]:
        """Optimaliseer VAD instellingen voor betere resultaten"""
        if not self.model:
            return {"success": False, "error": "Model niet geladen"}
        
        vad_tester = VADTester(self.model)
        vad_optimizer = VADOptimizer(vad_tester)
        return vad_optimizer.optimize_vad_settings(audio_path, target_speech_ratio)
