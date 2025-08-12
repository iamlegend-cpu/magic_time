"""
Magic Time Studio Core Module
Bevat alle core functionaliteit voor de applicatie
"""

# Import alle core modules
from . import config
from . import logging
from . import utils
from . import diagnostics
from . import stop_manager

# Import bestand modules
from . import file_functions
from . import file_validation
from . import file_info
from . import file_operations
from . import file_search
from . import file_utilities

# Import andere core modules
from . import audio_functions
from . import video_functions
from . import whisper_functions
from . import translation_functions
from . import subtitle_functions
from . import all_functions

# Export alle modules
__all__ = [
    'config',
    'logging', 
    'utils',
    'diagnostics',
    'stop_manager',
    'file_functions',
    'file_validation',
    'file_info',
    'file_operations',
    'file_search',
    'file_utilities',
    'audio_functions',
    'video_functions',
    'whisper_functions',
    'translation_functions',
    'subtitle_functions',
    'all_functions'
]

# Versie informatie
__version__ = "2.0.0"
__author__ = "Magic Time Studio Team"
__description__ = "Modulaire versie van Magic Time Studio met gescheiden functionaliteit" 