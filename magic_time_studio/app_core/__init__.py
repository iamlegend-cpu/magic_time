"""
Magic Time Studio App Core
Beheert de kern functionaliteit van de applicatie
"""

# Import core modules
from . import import_utils
from . import module_manager
from . import processing_manager
from . import ui_manager
from . import theme_manager
from . import cleanup_manager
from . import file_handler
from . import single_instance

# Import WhisperX modules
from . import whisperx_core
from . import whisperx_vad
from . import whisperx_time_estimator
from . import whisperx_utils
from . import whisperx_processor

# Import processing modules
from . import processing_modules

# Import main entry point
from . import main_entry

__all__ = [
    'import_utils',
    'module_manager', 
    'processing_manager',
    'ui_manager',
    'theme_manager',
    'cleanup_manager',
    'file_handler',
    'single_instance',
    'whisperx_core',
    'whisperx_vad',
    'whisperx_time_estimator',
    'whisperx_utils',
    'whisperx_processor',
    'processing_modules',
    'main_entry'
]

# Versie informatie
__version__ = "2.0.0"
__author__ = "Magic Time Studio Team"
__description__ = "App Core module voor Magic Time Studio"
