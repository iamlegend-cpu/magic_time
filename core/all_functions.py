"""
Alle functies importeren voor Magic Time Studio
Alleen WhisperX wordt ondersteund
"""

# Import core modules
try:
    from core import subtitle_functions
    from core import translation_functions
    from core import audio_functions
    from core import video_functions
    from core import whisper_functions
    from core import whisperx_srt_functions
    from core import file_functions
    from core import file_utilities
    from core import file_validation
    from core import file_search
    from core import file_operations
    from core import file_info
    from core import utils
    from core import config
    from core import logging
    from core import diagnostics
    from core import stop_manager
    print("✅ Core modules geladen")
except ImportError as e:
    print(f"⚠️ Fout bij laden core modules: {e}")
    # Fallback imports
    try:
        import subtitle_functions
        import translation_functions
        import audio_functions
        import video_functions
        import whisper_functions
        import whisperx_srt_functions
        import file_functions
        import file_utilities
        import file_validation
        import file_search
        import file_operations
        import file_info
        import utils
        import config
        import logging
        import diagnostics
        import stop_manager
        print("✅ Core modules geladen via fallback")
    except ImportError as e2:
        print(f"❌ Fout bij fallback imports: {e2}")

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
    'whisperx_srt_functions',
    
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
    transcribe_with_fallback,
    create_whisperx_srt_file,
    is_whisperx_srt_available
)

# WhisperX SRT functies
from .whisperx_srt_functions import (
    create_whisperx_srt_content,
    create_enhanced_srt_with_word_timing,
    validate_whisperx_transcriptions,
    get_whisperx_statistics
)

# Export WhisperX functies direct
__all__.extend([
    'load_whisperx_model',
    'transcribe_audio_whisperx', 
    'get_model_info',
    'transcribe_with_fallback',
    'create_whisperx_srt_file',
    'is_whisperx_srt_available',
    'create_whisperx_srt_content',
    'create_enhanced_srt_with_word_timing',
    'validate_whisperx_transcriptions',
    'get_whisperx_statistics'
])
