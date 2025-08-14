"""
UI Components voor Magic Time Studio
Beheert alle UI componenten en panels
"""

# Import core components
from . import panels
from . import menu_manager
from . import files_panel
from . import processing_panel
from . import completed_files_panel
from . import batch_panel
from . import charts_panel

# Import settings components
from . import settings_panel_core
from . import settings_translator
from . import settings_whisper
from . import settings_subtitles
from . import settings_vad
from . import settings_panel

# Import whisper selector
from . import whisper_selector

__all__ = [
    'panels',
    'menu_manager',
    'files_panel',
    'processing_panel',
    'completed_files_panel',
    'batch_panel',
    'charts_panel',
    'settings_panel_core',
    'settings_translator',
    'settings_whisper',
    'settings_subtitles',
    'settings_vad',
    'settings_panel',
    'whisper_selector'
] 