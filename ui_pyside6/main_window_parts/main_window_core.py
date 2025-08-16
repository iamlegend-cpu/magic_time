"""
Main Window Core voor PySide6
Hoofdklasse die alle mixins combineert
"""

from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import Signal
from ..themes import ThemeManager
from ..features.modern_styling import ModernStyling
from ..components.settings_panel_wrapper import SettingsPanelWrapper
from ..components.files_panel import FilesPanel
from ..components.processing_panel import ProcessingPanel
from ..components.charts_panel import ChartsPanel
from ..components.batch_panel import BatchPanel
from ..components.completed_files_panel import CompletedFilesPanel

from .window_setup import WindowSetupMixin
from .menu_handlers import MenuHandlersMixin
from .processing_handlers import ProcessingHandlersMixin
from .file_handlers import FileHandlersMixin
from .ui_updates import UIUpdatesMixin
from .window_state import WindowStateMixin

class MainWindow(
    QMainWindow,
    WindowSetupMixin,
    MenuHandlersMixin,
    ProcessingHandlersMixin,
    FileHandlersMixin,
    UIUpdatesMixin,
    WindowStateMixin
):
    """PySide6 Hoofdvenster van Magic Time Studio"""
    
    # Signals - must be class attributes in PySide6, renamed to avoid conflicts
    main_processing_started = Signal(list, dict)  # files, settings
    main_file_selected = Signal(str)
    main_file_completed = Signal(str, str)  # file_path, output_path
    
    def __init__(self):
        super().__init__()
        
        self.theme_manager = ThemeManager()
        self.modern_styling = ModernStyling()
        self.processing_active = False
        self.config_window = None
        self.log_viewer = None
        
        self.setup_window()
        self.create_menu()
        self.create_main_interface()
        self.create_status_bar()
        self.setup_timers()
        
        # Setup connections after panels are created
        self.setup_connections()
        
        print("🏠 PySide6 Hoofdvenster aangemaakt")
    
    def changeEvent(self, event):
        """Handle window state changes - roep mixin changeEvent aan"""
        # Roep de mixin changeEvent aan
        WindowStateMixin.changeEvent(self, event)
        # Roep ook de parent changeEvent aan
        super().changeEvent(event) 