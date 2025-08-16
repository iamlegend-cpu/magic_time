"""
Panels module voor Magic Time Studio
"""

from .settings_panel_wrapper import SettingsPanelWrapper
from .files_panel import FilesPanel
from .processing_panel import ProcessingPanel
from .charts_panel import ChartsPanel
from .batch_panel import BatchPanel
from .completed_files_panel import CompletedFilesPanel

__all__ = [
    'SettingsPanelWrapper',
    'FilesPanel',
    'ProcessingPanel',
    'ChartsPanel',
    'BatchPanel',
    'CompletedFilesPanel'
] 