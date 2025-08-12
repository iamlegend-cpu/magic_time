"""
UI Updates Mixin voor MainWindow
Bevat alle UI update gerelateerde functies
"""

import os
from typing import List, Dict
from PyQt6.QtWidgets import QMessageBox, QApplication, QLabel, QProgressBar, QWidget, QVBoxLayout, QHBoxLayout, QSplitter
from PyQt6.QtCore import QTimer, Qt

# Lazy import van config_manager om circulaire import te voorkomen
def _get_config_manager():
    """Lazy config manager import om circulaire import te voorkomen"""
    try:
        from core.config import config_manager
        return config_manager
    except ImportError:
        return None

# Import UI componenten
from ..components.settings_panel_wrapper import SettingsPanelWrapper
from ..components.files_panel import FilesPanel
from ..components.processing_panel import ProcessingPanel
from ..components.charts_panel import ChartsPanel
from ..components.batch_panel import BatchPanel

# Import features
from ..features.system_monitor import SystemMonitorWidget

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
            config_mgr = _get_config_manager()
            if config_mgr and config_mgr.is_panel_visible(panel_name):
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
        
        # Update files panel info met huidige instellingen
        self.update_files_panel_info()
    
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
        # Verwijder deze connecties - ze veroorzaken een oneindige loop
        # self.processing_started.connect(self._on_processing_started)
        # self.processing_stopped.connect(self._on_processing_stopped)
        
        # Connect settings panel signals to files panel info updates
        self.settings_panel.settings_panel.whisper_type_changed.connect(
            self.on_whisper_type_changed
        )
        self.settings_panel.settings_panel.model_changed.connect(
            self.on_model_changed
        )
        self.settings_panel.settings_panel.language_changed.connect(
            self.files_panel.update_language_info
        )
        self.settings_panel.settings_panel.translator_changed.connect(
            self.files_panel.update_translator_info
        )
        self.settings_panel.settings_panel.vad_enabled_changed.connect(
            self.files_panel.update_vad_status
        )
        
        # Connect whisper type en model signals
        self.settings_panel.settings_panel.whisper_type_changed.connect(
            self.on_whisper_type_changed
        )
        self.settings_panel.settings_panel.model_changed.connect(
            self.on_model_changed
        )
        
        # Update files panel info met huidige instellingen
        self.update_files_panel_info()
    
    def update_files_panel_info(self):
        """Update files panel info met huidige instellingen"""
        try:
            # Haal huidige instellingen op
            current_settings = self.settings_panel.get_current_settings()
            
            # Update whisper info
            whisper_type = current_settings.get("whisper_type", "")
            whisper_model = current_settings.get("whisper_model", "")
            self.files_panel.update_whisper_info(whisper_type, whisper_model)
            
            # Update taal info
            language = current_settings.get("language", "")
            if language == "Auto detectie":
                language = "Auto detectie"
            elif language == "Engels":
                language = "en"
            elif language == "Nederlands":
                language = "nl"
            elif language == "Duits":
                language = "de"
            elif language == "Frans":
                language = "fr"
            elif language == "Spaans":
                language = "es"
            self.files_panel.update_language_info(language)
            
            # Update vertaler info
            translator = current_settings.get("translator", "")
            self.files_panel.update_translator_info(translator)
            
            # Update VAD status
            vad_enabled = current_settings.get("vad_enabled", False)
            self.files_panel.update_vad_status(vad_enabled)
            
            # Update GPU status
            self.update_gpu_status()
            
        except Exception as e:
            print(f"⚠️ Fout bij updaten files panel info: {e}")
    
    def update_gpu_status(self):
        """Update GPU status in files panel"""
        try:
            # Probeer GPU info op te halen via system monitor
            from magic_time_studio.ui_pyqt6.features.system_monitor import SystemMonitorWidget
            
            monitor = SystemMonitorWidget()
            gpu_percent = monitor.get_gpu_info()
            
            if gpu_percent is not None:
                self.files_panel.update_gpu_status(True)
            else:
                self.files_panel.update_gpu_status(False)
                
        except Exception as e:
            print(f"⚠️ Fout bij updaten GPU status: {e}")
            # Fallback: probeer PyTorch CUDA
            try:
                import torch
                has_gpu = torch.cuda.is_available()
                self.files_panel.update_gpu_status(has_gpu)
            except:
                self.files_panel.update_gpu_status(False)
    
    def on_whisper_type_changed(self, whisper_type: str):
        """Callback voor whisper type wijziging"""
        try:
            # Haal huidige model op
            current_settings = self.settings_panel.get_current_settings()
            current_model = current_settings.get("whisper_model", "")
            
            # Update files panel met beide waarden
            self.files_panel.update_whisper_info(whisper_type, current_model)
            
        except Exception as e:
            print(f"⚠️ Fout bij updaten whisper type: {e}")
    
    def on_model_changed(self, model: str):
        """Callback voor model wijziging"""
        try:
            # Haal huidige whisper type op
            current_settings = self.settings_panel.get_current_settings()
            current_type = current_settings.get("whisper_type", "")
            
            # Update files panel met beide waarden
            self.files_panel.update_whisper_info(current_type, model)
            
        except Exception as e:
            print(f"⚠️ Fout bij updaten model: {e}")
    

    
    def update_status(self, message: str):
        """Update status met real-time updates en voortgangsbalk"""
        # Update status label
        if hasattr(self, 'status_label'):
            self.status_label.setText(message)
        
        # Update status bar
        self.status_bar.showMessage(message)
        
        # Parse Whisper progress uit bericht en update voortgangsbalk
        progress_found = False
        
        # Parse Fast Whisper progress uit bericht
        if "🎤 Fast Whisper:" in message and "%" in message:
            try:
                # Zoek naar percentage in het bericht (bijv. "🎤 Fast Whisper: 45.5% - filename")
                percent_str = message.split("🎤 Fast Whisper:")[1].split("%")[0].strip()
                percent = float(percent_str)
                self.status_bar.showMessage(f"🎤 Fast Whisper: {percent}% - Real-time transcriptie bezig...")
                
                # Update voortgangsbalk
                self._update_status_progress(percent, True)
                progress_found = True
            except:
                pass
        
        # Parse Standaard Whisper progress uit bericht
        elif "🔧 Standaard Whisper:" in message and "%" in message:
            try:
                # Zoek naar percentage in het bericht (bijv. "🔧 Standaard Whisper: 45.5% | Verstreken: 01:23 | ETA: 02:45 | filename")
                percent_str = message.split("🔧 Standaard Whisper:")[1].split("%")[0].strip()
                percent = float(percent_str)
                
                # Haal ETA en verstreken tijd uit het bericht
                if "ETA:" in message and "Verstreken:" in message:
                    try:
                        elapsed_part = message.split("Verstreken:")[1].split("|")[0].strip()
                        eta_part = message.split("ETA:")[1].split("|")[0].strip()
                        filename_part = message.split("|")[-1].strip()
                        
                        status_msg = f"🔧 Standaard Whisper: {percent}% | Verstreken: {elapsed_part} | ETA: {eta_part} | {filename_part}"
                        self.status_bar.showMessage(status_msg)
                        
                        # Update voortgangsbalk
                        self._update_status_progress(percent, True)
                        progress_found = True
                        return
                    except:
                        pass
                
                # Fallback naar eenvoudige status
                self.status_bar.showMessage(f"🔧 Standaard Whisper: {percent}% - Transcriptie bezig...")
                
                # Update voortgangsbalk
                self._update_status_progress(percent, True)
                progress_found = True
            except:
                pass
        
        # Maak timing berichten prominenter
        elif "⏱️" in message:
            # Timing berichten krijgen speciale behandeling
            if "Start verwerking" in message:
                self.status_bar.showMessage(f"🚀 {message}")
                self._update_status_progress(0, True)  # Start voortgangsbalk
            elif "voltooid in" in message:
                self.status_bar.showMessage(f"✅ {message}")
                self._update_status_progress(100, False)  # Voltooid, verberg voortgangsbalk
            elif "TOTALE VERWERKING" in message:
                self.status_bar.showMessage(f"🎯 {message}")
                self._update_status_progress(100, False)  # Voltooid, verberg voortgangsbalk
            else:
                self.status_bar.showMessage(message)
        else:
            self.status_bar.showMessage(message)
        
        # Als geen voortgang gevonden, verberg voortgangsbalk
        if not progress_found and hasattr(self, 'status_progress_bar'):
            self._update_status_progress(0, False)
    
    def _update_status_progress(self, percent: float, visible: bool):
        """Update de voortgangsbalk in de statusbalk"""
        if hasattr(self, 'status_progress_bar'):
            self.status_progress_bar.setValue(int(percent))
            self.status_progress_bar.setVisible(visible)
            
            # Update kleur op basis van voortgang
            if percent >= 100:
                # Groen voor voltooid
                self.status_progress_bar.setStyleSheet("""
                    QProgressBar {
                        border: 1px solid #555555;
                        border-radius: 3px;
                        text-align: center;
                        background-color: #2e2e2e;
                        color: #ffffff;
                        font-size: 10px;
                    }
                    QProgressBar::chunk {
                        background-color: #4caf50;
                        border-radius: 2px;
                    }
                """)
            elif percent >= 50:
                # Blauw voor halverwege
                self.status_progress_bar.setStyleSheet("""
                    QProgressBar {
                        border: 1px solid #555555;
                        border-radius: 3px;
                        text-align: center;
                        background-color: #2e2e2e;
                        color: #ffffff;
                        font-size: 10px;
                    }
                    QProgressBar::chunk {
                        background-color: #2196f3;
                        border-radius: 2px;
                    }
                """)
            else:
                # Oranje voor begin
                self.status_progress_bar.setStyleSheet("""
                    QProgressBar {
                        border: 1px solid #555555;
                        border-radius: 3px;
                        text-align: center;
                        background-color: #2e2e2e;
                        color: #ffffff;
                        font-size: 10px;
                    }
                    QProgressBar::chunk {
                        background-color: #ff9800;
                        border-radius: 2px;
                    }
                """)
    
    def _on_stop_processing(self):
        """Handle stop processing signal"""
        print("🛑 UI: Stop processing signal ontvangen")
        # De daadwerkelijke stop wordt afgehandeld door de app core
        # Deze methode is alleen voor UI updates
        self.update_status("Verwerking gestopt door gebruiker")
        
        # Reset voortgangsbalk
        if hasattr(self, 'status_progress_bar'):
            self._update_status_progress(0, False)
    
    def block_ui_during_processing(self, block: bool):
        """Blokkeer UI elementen tijdens verwerking"""
        print(f"🔒 MainWindow: block_ui_during_processing({block}) aangeroepen")
        
        # Stel processing_active flag in op hoofdapplicatie niveau
        self.processing_active = block
        
        if hasattr(self, 'files_panel'):
            # Stel processing_active flag in op files panel
            self.files_panel.processing_active = block
            
            # Update drag & drop zone status (maar blokkeer niet)
            # Drag & drop zone is verwijderd, gebruik knoppen onderaan venster
            pass
            
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
                config_mgr = _get_config_manager()
                if config_mgr and config_mgr.is_panel_visible(panel_name):
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