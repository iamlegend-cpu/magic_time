"""
Processing Panel component voor Magic Time Studio
Modulaire versie die gebruik maakt van gescheiden componenten
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Signal

from .processing_panel_ui import ProcessingPanelUI
from .processing_controller import ProcessingController
from .progress_handler import ProgressHandler
from .file_list_manager import FileListManager
from .gpu_status_manager import GPUStatusManager
from .processing_cleanup import ProcessingCleanup
from .log_manager import LogManager
from .processing_core import ProcessingCore
from .file_manager import FileManager

class ProcessingPanel(QWidget):
    """Verwerking paneel - modulaire versie"""
    
    # Signals
    processing_started = Signal(list, dict)
    file_completed = Signal(str, str)  # file_path, output_path
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Initialiseer UI component
        self.ui = ProcessingPanelUI()
        
        # Stel layout in voor dit paneel
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.ui)
        
        # Initialiseer managers
        self.file_manager = FileManager()
        self.processing_core = ProcessingCore(self.file_manager, self._log_message)
        self.processing_core.parent = self
        
        # Initialiseer componenten
        self.gpu_manager = GPUStatusManager(self.ui)
        self.cleanup_manager = ProcessingCleanup(self.ui, self.ui.progress_tracker, self.gpu_manager)
        self.file_list_manager = FileListManager(self.ui, self.file_manager)
        self.log_manager = LogManager(self.ui)
        self.progress_handler = ProgressHandler(self.ui, self.ui.progress_tracker)
        self.processing_controller = ProcessingController(
            self.ui, self.file_manager, self.processing_core, 
            self.ui.progress_tracker, self.gpu_manager, self.cleanup_manager
        )
        
        # Stel signals in
        self.progress_handler.set_signals(self.file_completed, self._on_cleanup_needed)
        
        # Maak progress_handler beschikbaar in UI
        self.ui.progress_handler = self.progress_handler
        
        # Verbind UI knoppen
        self._connect_ui_signals()
        
        # Kopieer UI naar deze klasse voor backward compatibility
        self._copy_ui_references()
    
    def _connect_ui_signals(self):
        """Verbind UI knoppen aan hun handlers"""
        # Start knop
        self.ui.start_btn.clicked.connect(self.processing_controller.start_processing_direct)
        
        # Log knoppen
        self.ui.clear_log_btn.clicked.connect(self.log_manager.clear_log)
        self.ui.copy_log_btn.clicked.connect(self.log_manager.copy_log)
    
    def _copy_ui_references(self):
        """Kopieer UI referenties naar deze klasse voor backward compatibility"""
        # Progress bar
        self.progress_bar = self.ui.progress_bar
        
        # Labels
        self.status_label = self.ui.status_label
        self.timing_label = self.ui.timing_label
        
        # Knoppen
        self.start_btn = self.ui.start_btn
        self.clear_log_btn = self.ui.clear_log_btn
        self.copy_log_btn = self.ui.copy_log_btn
        
        # Text areas
        self.log_text = self.ui.log_text
        self.completed_list = self.ui.completed_list
        
        # Progress tracker
        self.progress_tracker = self.ui.progress_tracker
        
        # Timer
        self.progress_timer = self.processing_controller.progress_timer
        
        # Status
        self.is_processing = self.ui.is_processing
    
    def _log_message(self, message: str):
        """Log message via log manager"""
        self.log_manager.log_message(message)
    
    def _on_cleanup_needed(self):
        """Callback voor cleanup signal"""
        self.cleanup_manager.complete_processing_cleanup()
    
    def start_processing_direct(self):
        """Start verwerking direct - backward compatibility"""
        self.processing_controller.start_processing_direct()
    
    def start_processing_with_settings(self, files, settings):
        """Start verwerking met instellingen - backward compatibility"""
        self.processing_controller.start_processing_with_settings(files, settings)
    
    def complete_processing(self):
        """Markeer verwerking als voltooid - backward compatibility"""
        self.cleanup_manager.complete_processing()
    
    def reset(self):
        """Reset het paneel naar begin staat - backward compatibility"""
        self.cleanup_manager.reset_panel(self.file_manager)
    
    def add_completed_file(self, file_path: str, output_path: str = None):
        """Voeg een voltooid bestand toe - backward compatibility"""
        # Gebruik output_path als deze beschikbaar is, anders file_path
        filename = output_path if output_path else file_path
        self.file_list_manager.add_completed_file(filename, output_path)
    
    def clear_completed_files(self):
        """Wis de voltooide bestanden lijst - backward compatibility"""
        self.file_list_manager.clear_completed_files()
    
    def get_completed_files(self):
        """Haal de lijst met voltooide bestanden op - backward compatibility"""
        return self.file_list_manager.get_completed_files()
    
    def update_progress(self, value, step_progress=None):
        """Update de progress bar - backward compatibility"""
        self.log_manager.update_progress(value, step_progress)
    
    def update_status(self, status):
        """Update de status label - backward compatibility"""
        self.log_manager.update_status(status)
    
    def log_message(self, message: str):
        """Voeg een bericht toe aan de log - backward compatibility"""
        self.log_manager.log_message(message)
    
    def clear_log(self):
        """Wis de log - backward compatibility"""
        self.log_manager.clear_log()
    
    def copy_log(self):
        """Kopieer de log naar klembord - backward compatibility"""
        self.log_manager.copy_log()
