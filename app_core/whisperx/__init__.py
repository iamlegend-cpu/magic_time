"""
WhisperX modules voor Magic Time Studio
Modulaire structuur voor WhisperX functionaliteit
"""

from .pipeline_fixes import fix_pipeline_imports, setup_pyinstaller_paths
from .model_manager import WhisperXModelManager
from .transcription_core import TranscriptionCore
from .vad_integration import VADIntegration
from .whisperx_processor import WhisperXProcessor

__all__ = [
    'fix_pipeline_imports',
    'setup_pyinstaller_paths',
    'WhisperXModelManager',
    'TranscriptionCore', 
    'VADIntegration',
    'WhisperXProcessor'
]
