"""
Alle functies importeren voor Magic Time Studio
Alleen WhisperX wordt ondersteund
"""

# Import alle core functies
from . import file_functions
from . import file_operations
from . import file_search
from . import file_utilities
from . import file_validation
from . import file_info
from . import audio_functions
from . import video_functions
from . import subtitle_functions
from . import translation_functions
from . import whisper_functions
from . import utils
from . import logging
from . import config
from . import stop_manager

# Export alle beschikbare functies
__all__ = [
    # File functies
    'file_functions',
    'file_operations', 
    'file_search',
    'file_utilities',
    'file_validation',
    'file_info',
    
    # Media functies
    'audio_functions',
    'video_functions',
    'subtitle_functions',
    'translation_functions',
    
    # WhisperX functies
    'whisper_functions',
    
    # Utility functies
    'utils',
    'logging',
    'config',
    'stop_manager',
]

# WhisperX specifieke functies
from .whisper_functions import (
    load_whisperx_model,
    transcribe_audio_whisperx,
    get_model_info,
    transcribe_with_fallback
)

# Export WhisperX functies direct
__all__.extend([
    'load_whisperx_model',
    'transcribe_audio_whisperx', 
    'get_model_info',
    'transcribe_with_fallback'
])
