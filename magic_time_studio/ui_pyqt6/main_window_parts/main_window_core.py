"""
Main Window Core voor PyQt6
Hoofdklasse die alle mixins combineert
"""

from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtCore import pyqtSignal
from ..themes import ThemeManager
from ..features.modern_styling import ModernStyling
from ..components.settings_panel_wrapper import SettingsPanelWrapper
from ..components.files_panel import FilesPanel
from ..components.processing_panel import ProcessingPanel
from ..components.charts_panel import ChartsPanel
from ..components.batch_panel import BatchPanel

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
    """PyQt6 Hoofdvenster van Magic Time Studio"""
    
    # Signals
    processing_started = pyqtSignal(list, dict)  # files, settings
    processing_stopped = pyqtSignal()
    file_selected = pyqtSignal(str)
    
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
        self.setup_connections()
        
        # Pas moderne styling toe
        self.theme_manager.apply_theme(QApplication.instance(), "dark")
        
        print("🏠 PyQt6 Hoofdvenster aangemaakt")
    
    def changeEvent(self, event):
        """Handle window state changes - roep mixin changeEvent aan"""
        # Roep de mixin changeEvent aan
        WindowStateMixin.changeEvent(self, event)
        # Roep ook de parent changeEvent aan
        super().changeEvent(event) 