"""
Core modules voor Magic Time Studio
"""

# Import alle core modules - alleen de basis modules
try:
    from . import subtitle_functions
    from . import translation_functions
    from . import audio_functions
    from . import video_functions
    from . import whisper_functions
    from . import whisperx_srt_functions
    from . import file_functions
    from . import file_utilities
    from . import file_validation
    from . import file_search
    from . import file_operations
    from . import file_info
    from . import utils
    from . import config
    from . import logging
    from . import diagnostics
    from . import stop_manager
    print("✅ Core modules geladen")
except ImportError as e:
    print(f"⚠️ Fout bij laden core modules: {e}")

# Versie informatie
__version__ = "2.0.0"
__author__ = "Magic Time Studio Team"
__description__ = "Modulaire versie van Magic Time Studio met gescheiden functionaliteit" 