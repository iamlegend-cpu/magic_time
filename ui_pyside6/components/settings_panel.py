"""
Settings Panel - Import Wrapper
Dit bestand is opgesplitst in modulaire componenten voor betere onderhoudbaarheid
"""

# Import alle functionaliteit uit de modulaire structuur
from .settings_panel_core import SettingsPanel
from .settings_translator import TranslatorSettings
from .settings_whisper import WhisperSettings
from .settings_subtitles import SubtitleSettings
from .settings_vad import VadSettings

# Export alle klassen voor backward compatibility
__all__ = [
    'SettingsPanel',
    'TranslatorSettings',
    'WhisperSettings',
    'SubtitleSettings',
    'VadSettings'
]
