"""
UI Components voor Magic Time Studio
"""

from .menu_manager import MenuManager
from .settings_panel import SettingsPanel
from .settings_panel_wrapper import SettingsPanelWrapper
from .files_panel import FilesPanel
from .processing_panel import ProcessingPanel
from .charts_panel import ChartsPanel
from .batch_panel import BatchPanel

__all__ = [
    'MenuManager',
    'SettingsPanel',
    'SettingsPanelWrapper',
    'FilesPanel',
    'ProcessingPanel',
    'ChartsPanel',
    'BatchPanel'
] 