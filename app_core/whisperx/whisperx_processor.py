"""
WhisperX Processor - Hoofdklasse
Coördineert alle WhisperX functionaliteit
"""

import os
import torch
from typing import Dict, Any, List, Optional, Callable

# Import lokale modules
from .pipeline_fixes import initialize_pipeline_fixes
from .model_manager import WhisperXModelManager
from .transcription_core import TranscriptionCore
from .vad_integration import VADIntegration

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
        
        # Initialiseer Pipeline fixes
        initialize_pipeline_fixes()
        
        # Voeg FFmpeg toe aan PATH vanuit assets directory
        from ..import_utils import setup_ffmpeg_path
        setup_ffmpeg_path()
        
        # Zorg ervoor dat FFmpeg beschikbaar is voor WhisperX
        self._setup_ffmpeg_for_whisperx()
        
        # Schakel TF32 in voor betere prestaties
        from ..whisperx_utils import setup_tf32
        setup_tf32()
        
        # Initialiseer device en compute type
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.compute_type = "float16" if self.device == "cuda" else "int8"
        self.gpu_available = torch.cuda.is_available()
        
        # Initialiseer componenten
        self.model_manager = WhisperXModelManager(self.device, self.compute_type)
        self.vad_integration = VADIntegration()
        
        # Import en initialiseer time estimator
        from ..whisperx_time_estimator import TimeEstimator
        self.time_estimator = TimeEstimator()
        
        # Initialiseer transcription core
        self.transcription_core = TranscriptionCore(
            self.model_manager, 
            self.time_estimator, 
            self.vad_integration
        )
        
        print(f"🔧 WhisperX Processor geïnitialiseerd op {self.device}")
        if self.gpu_available:
            print(f"🎯 GPU: {torch.cuda.get_device_name(0)}")
        
        # Markeer als geïnitialiseerd
        self._initialized = True
        self._last_model_name = None
        self._last_vad_settings = None
    
    def _setup_ffmpeg_for_whisperx(self):
        """Zorg ervoor dat FFmpeg beschikbaar is voor WhisperX"""
        try:
            # Zoek naar FFmpeg in verschillende locaties
            ffmpeg_paths = [
                os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "ffmpeg.exe"),  # magic_time/assets
                os.path.join(os.getcwd(), "assets", "ffmpeg.exe"),  # huidige werkdirectory/assets
                "assets/ffmpeg.exe",  # relatieve assets directory
                "ffmpeg.exe"  # Als het al in PATH staat
            ]
            
            ffmpeg_found = None
            for path in ffmpeg_paths:
                if os.path.exists(path):
                    ffmpeg_found = path
                    break
            
            if ffmpeg_found:
                # Voeg FFmpeg directory toe aan PATH
                ffmpeg_dir = os.path.dirname(os.path.abspath(ffmpeg_found))
                if ffmpeg_dir not in os.environ.get("PATH", ""):
                    os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")
                    print(f"🔧 FFmpeg toegevoegd aan PATH voor WhisperX: {ffmpeg_dir}")
                
                # Stel ook FFMPEG_BINARY environment variable in
                os.environ["FFMPEG_BINARY"] = ffmpeg_found
                print(f"🔧 FFMPEG_BINARY ingesteld: {ffmpeg_found}")
                
                # Test of FFmpeg nu beschikbaar is
                try:
                    import subprocess
                    result = subprocess.run([ffmpeg_found, "-version"], 
                                         capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        print("✅ FFmpeg succesvol ingesteld voor WhisperX")
                    else:
                        print(f"⚠️ FFmpeg test gefaald: {result.stderr}")
                except Exception as e:
                    print(f"⚠️ FFmpeg test error: {e}")
            else:
                print("⚠️ FFmpeg niet gevonden voor WhisperX")
                
        except Exception as e:
            print(f"⚠️ Fout bij instellen FFmpeg voor WhisperX: {e}")
    
    def load_model(self, model_name: str = "large-v3", vad_settings: Dict[str, Any] = None) -> bool:
        """Laad WhisperX model"""
        # Controleer of we echt moeten laden
        if (self._last_model_name == model_name and 
            self.model_manager.is_loaded and 
            self.model_manager.current_model == model_name):
            print(f"✅ Model {model_name} is al geladen, skip loading")
            return True
            
        self._last_model_name = model_name
        return self.model_manager.load_model(model_name, vad_settings)
    
    def reload_model_with_vad_settings(self, model_name: str, vad_settings: Dict[str, Any]) -> bool:
        """Herlaad WhisperX model met VAD instellingen"""
        # Controleer of we echt moeten herladen
        if (self._last_model_name == model_name and 
            self._last_vad_settings == vad_settings and
            self.model_manager.is_loaded and 
            self.model_manager.current_model == model_name):
            print(f"✅ Model {model_name} hoeft niet te worden herladen - instellingen ongewijzigd")
            return True
            
        self._last_model_name = model_name
        self._last_vad_settings = vad_settings.copy() if vad_settings else None
        return self.model_manager.reload_model_with_vad_settings(model_name, vad_settings)
    
    def transcribe_with_alignment(self, audio_path: str, language: Optional[str] = None, 
                                 progress_callback: Optional[Callable[[float, str], None]] = None,
                                 vad_settings: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Transcribeer audio met WhisperX en word-level alignment"""
        return self.transcription_core.transcribe_with_alignment(
            audio_path, language, progress_callback, vad_settings
        )
    
    def create_accurate_srt(self, transcriptions: List[Dict[str, Any]], 
                           word_alignments: List[Dict[str, Any]] = None) -> str:
        """Genereer SRT met WhisperX word-level timing voor maximale accuracy"""
        from ..whisperx_utils import create_accurate_srt
        return create_accurate_srt(transcriptions, word_alignments)
    
    def get_model_info(self) -> Dict[str, Any]:
        """Krijg informatie over het geladen model"""
        return self.model_manager.get_model_info()
    
    def cleanup(self):
        """Ruim geheugen op - inclusief CUDA/GPU context"""
        try:
            print("🧹 WhisperX geheugen opruimen...")
            
            # Stop CUDA context eerst
            from ..whisperx_utils import cleanup_cuda_context
            cleanup_cuda_context()
            
            # Ruim modellen op via model manager
            self.model_manager.cleanup()
            
            print("🧹 WhisperX geheugen opgeruimd")
            
        except Exception as e:
            print(f"⚠️ Fout bij cleanup: {e}")
    
    def test_vad_settings(self, audio_path: str, vad_settings: Dict[str, Any]) -> Dict[str, Any]:
        """Test VAD instellingen op een kort audio fragment"""
        if not self.model_manager.model:
            return {"success": False, "error": "Model niet geladen"}
        
        from ..whisperx_vad import VADTester
        vad_tester = VADTester(self.model_manager.model)
        return vad_tester.test_vad_settings(audio_path, vad_settings)
    
    def optimize_vad_settings(self, audio_path: str, target_speech_ratio: float = 0.6) -> Dict[str, Any]:
        """Optimaliseer VAD instellingen voor betere resultaten"""
        if not self.model_manager.model:
            return {"success": False, "error": "Model niet geladen"}
        
        from ..whisperx_vad import VADTester, VADOptimizer
        vad_tester = VADTester(self.model_manager.model)
        vad_optimizer = VADOptimizer(vad_tester)
        return vad_optimizer.optimize_vad_settings(audio_path, target_speech_ratio)
    
    def get_vad_status(self) -> Dict[str, Any]:
        """Haal VAD status op"""
        return {
            "enabled": self.vad_integration.is_vad_enabled(),
            "method": self.vad_integration.get_vad_method(),
            "threshold": self.vad_integration.get_vad_threshold(),
            "chunk_size": self.vad_integration.get_vad_chunk_size()
        }
    
    def update_vad_settings(self, new_settings: Dict[str, Any]) -> bool:
        """Update VAD instellingen"""
        return self.vad_integration.update_vad_settings(new_settings)
