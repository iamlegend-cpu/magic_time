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
        main_layout.setContentsMargins(8, 8, 8, 8)  # Iets grotere margins
        main_layout.setSpacing(8)  # Iets grotere spacing
        
        # Splitter voor zes panelen
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.setChildrenCollapsible(False)  # Voorkom dat panels kunnen collapsen
        self.splitter.setHandleWidth(4)  # Iets dikkere splitter handles voor betere zichtbaarheid
        main_layout.addWidget(self.splitter)
        
        # Maak panelen
        self.settings_panel = SettingsPanelWrapper()
        self.files_panel = FilesPanel()
        self.processing_panel = ProcessingPanel()
        self.charts_panel = ChartsPanel()
        self.batch_panel = BatchPanel()
        
        # Stel minimum groottes in voor alle panels
        self.settings_panel.setMinimumWidth(220)
        self.files_panel.setMinimumWidth(320)
        self.processing_panel.setMinimumWidth(420)
        self.charts_panel.setMinimumWidth(270)
        self.batch_panel.setMinimumWidth(270)
        
        # Stel maximum groottes in voor alle panels
        self.settings_panel.setMaximumWidth(320)
        self.files_panel.setMaximumWidth(520)
        self.processing_panel.setMaximumWidth(620)
        self.charts_panel.setMaximumWidth(420)
        self.batch_panel.setMaximumWidth(420)
        
        # Voeg panelen toe aan splitter (alleen zichtbare)
        self.visible_panels = {}
        panel_configs = [
            ("settings", self.settings_panel, 270),
            ("files", self.files_panel, 370),
            ("processing", self.processing_panel, 470),
            ("charts", self.charts_panel, 320),
            ("batch", self.batch_panel, 320)
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
        
        # Stel window in op maximized state
        self.showMaximized()
        
        # Force een layout update
        self.updateGeometry()
        self.update()
    
    def setup_connections(self):
        """Setup signal connections"""
        # Files panel connections
        # self.files_panel.files_dropped.connect(self.on_files_dropped)  # Verwijderd - files_panel heeft eigen handler
        self.files_panel.file_selected.connect(self.on_file_selected)
        
        # Processing panel connections
        self.processing_panel.processing_started.connect(self.on_processing_started)
        self.processing_panel.processing_stopped.connect(self.on_processing_stopped)
        self.processing_panel.file_completed.connect(self.on_file_completed)
        
        # Connect processing signals to main window signals
        self.processing_started.connect(self._on_processing_started)
        self.processing_stopped.connect(self._on_processing_stopped)
        
        # Connect stop processing signal to app core
        self.processing_stopped.connect(self._on_stop_processing)
    
    def update_status(self, message: str):
        """Update status met real-time updates"""
        # Update status bar
        self.status_bar.showMessage(message)
        
        # Parse Whisper progress uit bericht
        if "🎤 Fast Whisper:" in message and "%" in message:
            try:
                # Zoek naar percentage in het bericht (bijv. "🎤 Fast Whisper: 45.5% - filename")
                percent_str = message.split("🎤 Fast Whisper:")[1].split("%")[0].strip()
                percent = float(percent_str)
                self.status_bar.showMessage(f"🎤 Fast Whisper: {percent}% - Real-time transcriptie bezig...")
            except:
                pass
        else:
            self.status_bar.showMessage(message)
    
    def _on_stop_processing(self):
        """Handle stop processing signal"""
        print("🛑 UI: Stop processing signal ontvangen")
        # De daadwerkelijke stop wordt afgehandeld door de app core
        # Deze methode is alleen voor UI updates
        self.update_status("Verwerking gestopt door gebruiker")
    
    def block_ui_during_processing(self, block: bool):
        """Blokkeer UI elementen tijdens verwerking"""
        print(f"🔒 MainWindow: block_ui_during_processing({block}) aangeroepen")
        
        # Stel processing_active flag in op hoofdapplicatie niveau
        self.processing_active = block
        
        if hasattr(self, 'files_panel'):
            # Stel processing_active flag in op files panel
            self.files_panel.processing_active = block
            
            # Update drag & drop zone status
            if hasattr(self.files_panel, 'drag_drop_zone'):
                self.files_panel.drag_drop_zone.set_processing_active(block)
            
            # Blokkeer/deblokkeer bestanden beheer
            # Toevoegen knoppen blijven beschikbaar tijdens verwerking
            self.files_panel.add_file_btn.setEnabled(True)
            self.files_panel.add_folder_btn.setEnabled(True)
            self.files_panel.file_list_widget.setEnabled(True)
            
            # Update button states op basis van verwerking status
            if block:
                # Gebruik speciale methode voor tijdens verwerking
                self.files_panel.update_button_states_during_processing()
            else:
                # Gebruik normale methode
                self.files_panel.update_button_states()
        
        if hasattr(self, 'settings_panel'):
            # Bevries/ontdooi settings panel
            if block:
                self.settings_panel.freeze_settings()
            else:
                self.settings_panel.unfreeze_settings()
        
        if hasattr(self, 'batch_panel'):
            # Blokkeer/deblokkeer batch panel
            self.batch_panel.setEnabled(not block)
        
        # Processing panel knoppen worden al beheerd door ProcessingPanel
        if hasattr(self, 'processing_panel'):
            if block:
                self.processing_panel.start_btn.setEnabled(False)
                self.processing_panel.stop_btn.setEnabled(True)
            else:
                self.processing_panel.start_btn.setEnabled(True)
                self.processing_panel.stop_btn.setEnabled(False)
        
        # Blokkeer/deblokkeer menu items tijdens verwerking
        if hasattr(self, 'menuBar'):
            for action in self.menuBar().actions():
                # Alleen blokkeer Bestanden en Verwerking menu's tijdens verwerking
                if action.text() in ["Bestanden", "Verwerking"]:
                    action.setEnabled(not block)
        
        print(f"🔒 MainWindow: UI {'geblokkeerd' if block else 'gedeblokkeerd'}")
    
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
                ("settings", self.settings_panel, 270),
                ("files", self.files_panel, 370),
                ("processing", self.processing_panel, 470),
                ("charts", self.charts_panel, 320),
                ("batch", self.batch_panel, 320)
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
                
                # Behoud maximized state
                if not self.isMaximized():
                    self.showMaximized()
                
                # Force een layout update
                self.updateGeometry()
                self.update()
            
        except Exception as e:
            print(f"❌ Fout bij herladen interface: {e}")
            self.update_status("Fout bij herladen interface") 