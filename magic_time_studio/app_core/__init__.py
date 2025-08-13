"""
Magic Time Studio App Core Module
Bevat alle core applicatie functionaliteit
"""

# Import alle app_core modules - alleen als beschikbaar
try:
    from . import main_entry
except ImportError:
    pass

try:
    from . import magic_time_studio_pyqt6
except ImportError:
    pass

try:
    from . import processing_manager
except ImportError:
    pass

try:
    from . import processing_thread_new
except ImportError:
    pass

try:
    from . import whisper_manager
except ImportError:
    pass

try:
    from . import fast_whisper
except ImportError:
    pass

try:
    from . import standard_whisper
except ImportError:
    pass

try:
    from . import cleanup_manager
except ImportError:
    pass

try:
    from . import file_handler
except ImportError:
    pass

try:
    from . import import_utils
except ImportError:
    pass

try:
    from . import module_manager
except ImportError:
    pass

try:
    from . import theme_manager
except ImportError:
    pass

try:
    from . import ui_manager
except ImportError:
    pass

# Export alle modules
__all__ = [
    'main_entry',
    'magic_time_studio_pyqt6',
    'processing_manager',
    'processing_thread_new',
    'whisper_manager',
    'fast_whisper',
    'standard_whisper',
    'cleanup_manager',
    'file_handler',
    'import_utils',
    'module_manager',
    'theme_manager',
    'ui_manager'
]

# Versie informatie
__version__ = "2.0.0"
__author__ = "Magic Time Studio Team"
__description__ = "App Core module voor Magic Time Studio"
