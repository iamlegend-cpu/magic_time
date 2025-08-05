"""
UI Updates Mixin voor MainWindow
Bevat alle UI update gerelateerde functies
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QApplication
from PyQt6.QtCore import Qt
from magic_time_studio.core.config import config_manager
from magic_time_studio.ui_pyqt6.components.settings_panel_wrapper import SettingsPanelWrapper
from magic_time_studio.ui_pyqt6.components.files_panel import FilesPanel
from magic_time_studio.ui_pyqt6.components.processing_panel import ProcessingPanel
from magic_time_studio.ui_pyqt6.components.charts_panel import ChartsPanel
from magic_time_studio.ui_pyqt6.components.batch_panel import BatchPanel

class UIUpdatesMixin:
    """Mixin voor UI update functionaliteit"""
    
    def create_main_interface(self):
        """Maak de hoofdinterface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Hoofdlayout
        main_layout = QHBoxLayout(central_widget)
        
        # Splitter voor zes panelen
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(self.splitter)
        
        # Maak panelen
        self.settings_panel = SettingsPanelWrapper()
        self.files_panel = FilesPanel()
        self.processing_panel = ProcessingPanel()
        self.charts_panel = ChartsPanel()
        self.batch_panel = BatchPanel()
        
        # Voeg panelen toe aan splitter (alleen zichtbare)
        self.visible_panels = {}
        panel_configs = [
            ("settings", self.settings_panel, 250),
            ("files", self.files_panel, 450),
            ("processing", self.processing_panel, 500),
            ("charts", self.charts_panel, 350),
            ("batch", self.batch_panel, 300)
        ]
        
        visible_sizes = []
        for panel_name, panel_widget, default_size in panel_configs:
            if config_manager.is_panel_visible(panel_name):
                self.splitter.addWidget(panel_widget)
                self.visible_panels[panel_name] = panel_widget
                visible_sizes.append(default_size)
        
        # Stel splitter proporties in voor zichtbare panels
        if visible_sizes:
            self.splitter.setSizes(visible_sizes)
    
    def setup_connections(self):
        """Setup signal connections"""
        # Files panel connections
        # self.files_panel.files_dropped.connect(self.on_files_dropped)  # Verwijderd - files_panel heeft eigen handler
        self.files_panel.file_selected.connect(self.on_file_selected)
        
        # Processing panel connections
        self.processing_panel.processing_started.connect(self.on_processing_started)
        self.processing_panel.processing_stopped.connect(self.on_processing_stopped)
        self.processing_panel.file_completed.connect(self.on_file_completed)
        
        # Charts panel connections
        if hasattr(self, 'charts_panel'):
            # Verbind verwerking events met charts panel
            self.processing_panel.processing_started.connect(self.on_charts_processing_started)
            self.processing_panel.file_completed.connect(self.on_charts_file_completed)
            self.processing_panel.processing_stopped.connect(self.on_charts_processing_stopped)
        
        # Connect processing signals to main window signals
        self.processing_started.connect(self._on_processing_started)
        self.processing_stopped.connect(self._on_processing_stopped)
        
        # Connect processing panel start button to main window start processing
        self.processing_panel.processing_started.connect(self.start_processing_from_panel)
    
    def update_status(self, message: str):
        """Update status met real-time updates"""
        # Update status bar
        self.status_bar.showMessage(message)
        
        # Voor Whisper updates, toon real-time progress in status bar
        if "🎤 Whisper:" in message and "%" in message:
            # Extraheer percentage voor real-time display
            try:
                percent_part = message.split("%")[0]
                percent = percent_part.split(":")[-1].strip()
                self.status_bar.showMessage(f"🎤 Whisper: {percent}% - Real-time transcriptie bezig...")
            except:
                self.status_bar.showMessage(message)
        else:
            self.status_bar.showMessage(message)
    
    def reload_interface(self):
        """Herlaad de interface op basis van nieuwe configuratie"""
        try:
            # Vind de splitter in de layout
            central_widget = self.centralWidget()
            if not central_widget:
                return
                
            layout = central_widget.layout()
            if not layout:
                return
                
            # Zoek naar de splitter (meestal het tweede item)
            splitter = None
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item and hasattr(item.widget(), 'setSizes'):
                    splitter = item.widget()
                    break
            
            if not splitter:
                print("❌ Splitter niet gevonden")
                return
            
            # Verwijder alle widgets uit de splitter
            while splitter.count() > 0:
                widget = splitter.widget(0)
                widget.setParent(None)
            
            # Voeg alleen zichtbare panels toe
            self.visible_panels = {}
            panel_configs = [
                ("settings", self.settings_panel, 250),
                ("files", self.files_panel, 450),
                ("processing", self.processing_panel, 500),
                ("charts", self.charts_panel, 350),
                ("batch", self.batch_panel, 300)
            ]
            
            visible_sizes = []
            for panel_name, panel_widget, default_size in panel_configs:
                if config_manager.is_panel_visible(panel_name):
                    splitter.addWidget(panel_widget)
                    self.visible_panels[panel_name] = panel_widget
                    visible_sizes.append(default_size)
            
            # Stel splitter proporties in voor zichtbare panels
            if visible_sizes:
                splitter.setSizes(visible_sizes)
            
            self.update_status("Interface herladen")
            
        except Exception as e:
            print(f"❌ Fout bij herladen interface: {e}")
            self.update_status("Fout bij herladen interface") 