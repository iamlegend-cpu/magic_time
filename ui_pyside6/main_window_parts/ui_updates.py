"""
UI Updates Mixin voor MainWindow
Bevat alle UI update gerelateerde functies
"""

import os
from typing import List, Dict
from PySide6.QtWidgets import QMessageBox, QApplication, QLabel, QProgressBar, QWidget, QVBoxLayout, QHBoxLayout, QSplitter
from PySide6.QtCore import QTimer, Qt

# Lazy import van config_manager om circulaire import te voorkomen
def _get_config_manager():
    """Lazy config manager import om circulaire import te voorkomen"""
    try:
        from ...core.config import config_manager
        return config_manager
    except ImportError:
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
try:
    from ..features.system_monitor import SystemMonitorWidget
except ImportError:
    SystemMonitorWidget = None

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
        
        # Splitter voor vijf panelen
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.setChildrenCollapsible(False)  # Voorkom dat panels kunnen collapsen
        self.splitter.setHandleWidth(4)  # Iets dikkere splitter handles voor betere zichtbaarheid
        main_layout.addWidget(self.splitter)
        
        # Maak panelen aan
        self.settings_panel = SettingsPanelWrapper()
        self.files_panel = FilesPanel()
        self.processing_panel = ProcessingPanel()
        self.charts_panel = ChartsPanel()
        self.batch_panel = BatchPanel()
        
        # Koppel GPU monitor direct aan hoofdvenster voor status updates
        if hasattr(self.charts_panel, 'gpu_monitor'):
            self.charts_panel.gpu_monitor.main_window = self
        
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
            ("settings_panel", self.settings_panel, 270),
            ("files_panel", self.files_panel, 370),
            ("processing_panel", self.processing_panel, 470),
            ("charts_panel", self.charts_panel, 320),
            ("batch_panel", self.batch_panel, 320)
        ]
        
        visible_sizes = []
        for panel_name, panel_widget, default_size in panel_configs:
            # Forceer belangrijke panelen altijd zichtbaar
            if panel_name in ["settings_panel", "files_panel", "processing_panel", "charts_panel"]:
                self.splitter.addWidget(panel_widget)
                self.visible_panels[panel_name] = panel_widget
                visible_sizes.append(default_size)
                
                # Forceer processing_panel altijd zichtbaar en met minimale breedte
                if panel_name == "processing_panel":
                    panel_widget.setVisible(True)
                    panel_widget.show()
                    panel_widget.setMinimumWidth(420)
            else:
                # Alleen batch_panel is optioneel
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
        self.files_panel.file_selected.connect(self.main_file_selected.emit)
        
        # Processing panel connections - Hersteld voor daadwerkelijke verwerking
        self.processing_panel.processing_started.connect(self.on_processing_started)
        self.processing_panel.processing_started.connect(self.main_processing_started.emit)
        self.processing_panel.file_completed.connect(self.on_file_completed)
        self.processing_panel.file_completed.connect(self.main_file_completed.emit)
        

        
        # Connect processing signals to main window signals
        # Deze connecties zijn niet meer nodig omdat we direct de processing panel signals gebruiken
        
        # Connect settings panel signals to files panel info updates
        self.settings_panel.settings_panel.model_changed.connect(
            self.on_model_changed
        )
        self.settings_panel.settings_panel.language_changed.connect(
            self.files_panel.update_language_info
        )
        self.settings_panel.settings_panel.translator_changed.connect(
            self.files_panel.update_translator_info
        )
        
        # VAD is altijd ingeschakeld, geen signal connectie nodig
        
        # Update files panel info met huidige instellingen
        self.update_files_panel_info()
    
    def setup_timers(self):
        """Setup timers voor real-time updates"""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.periodic_update)
        self.update_timer.start(1000)
        
        # Timer om monitoring zichtbaarheid te garanderen tijdens verwerking
        self.monitoring_visibility_timer = QTimer()
        self.monitoring_visibility_timer.timeout.connect(self._ensure_monitoring_visibility)
        self.monitoring_visibility_timer.start(2000)  # Controleer elke 2 seconden
    
    def update_files_panel_info(self):
        """Update files panel info met huidige instellingen"""
        try:
            # Haal huidige instellingen op
            current_settings = self.settings_panel.get_current_settings()
            
            # Update whisper info - altijd WhisperX
            whisper_type = "whisperx"
            whisper_model = current_settings.get("whisper_model", "")
            self.files_panel.update_whisper_info(whisper_type, whisper_model)
            
            # Update taal info
            language = current_settings.get("language", "")
            if language == "Engels" or language == "":
                language = "en"
            elif language == "Nederlands":
                language = "nl"
            elif language == "Duits":
                language = "de"
            elif language == "Frans":
                language = "fr"
            elif language == "Spaans":
                language = "es"
            else:
                # Fallback naar Engels als onbekende taal
                language = "en"
            self.files_panel.update_language_info(language)
            
            # Update vertaler info
            translator = current_settings.get("translator", "")
            self.files_panel.update_translator_info(translator)
            
            # Update VAD status
            vad_enabled = True  # VAD is altijd ingeschakeld
            self.files_panel.update_vad_status(vad_enabled)
            
            # Update GPU status
            self.update_gpu_status()
            
        except Exception as e:
            print(f"⚠️ Fout bij updaten files panel info: {e}")
    
    def update_gpu_status(self):
        """Update GPU status in files panel"""
        try:
            # Controleer direct PyTorch CUDA beschikbaarheid
            import torch
            has_gpu = torch.cuda.is_available()
            self.files_panel.update_gpu_status(has_gpu)
                
        except Exception as e:
            print(f"⚠️ Fout bij updaten GPU status: {e}")
            # Fallback: geen GPU
            self.files_panel.update_gpu_status(False)
    
    def on_model_changed(self, model: str):
        """Callback voor WhisperX model wijziging"""
        try:
            print(f"🔧 MainWindow: WhisperX model gewijzigd naar {model}")
            
            # Update files panel met WhisperX en het nieuwe model
            self.files_panel.update_whisper_info("whisperx", model)
            
            # Update whisper processor met nieuwe model instellingen
            if hasattr(self, 'whisper_processor'):
                try:
                    # Maak nieuwe instellingen aan met het gekozen model
                    current_settings = self.settings_panel.get_current_settings()
                    updated_settings = current_settings.copy()
                    updated_settings["whisper_model"] = model
                    
                    print(f"🔧 MainWindow: Update whisper processor met nieuwe instellingen: {updated_settings}")
                    self.whisper_processor.set_settings(updated_settings)
                    print(f"✅ MainWindow: WhisperX processor bijgewerkt met model: {model}")
                    
                except Exception as e:
                    print(f"⚠️ MainWindow: Fout bij updaten whisper processor: {e}")
            
        except Exception as e:
            print(f"⚠️ Fout bij updaten WhisperX model: {e}")
    

    
    def update_status(self, message: str):
        """Update status label - UITGESCHAKELD om overbodige updates te voorkomen"""
        # UITGESCHAKELD: Status updates zijn overbodig omdat info al zichtbaar is in verwerkingsbalk
        # if hasattr(self, 'status_label'):
        #     self.status_label.setText(message)
        #     print(f"📝 Status bijgewerkt: {message}")
        pass
        
        # UITGESCHAKELD: Status bar updates zijn overbodig
        # self.status_bar.showMessage(message)
        
        # UITGESCHAKELD: Progress parsing is overbodig
        # Parse Whisper progress uit bericht en update voortgangsbalk
        # progress_found = False
        
        # Parse WhisperX progress uit bericht
        # if "🎤 WhisperX:" in message and "%" in message:
        #     try:
        #         # Zoek naar percentage in het bericht (bijv. "🎤 WhisperX: 45.5% - filename")
        #         percent_str = message.split("🎤 WhisperX:")[1].split("%")[0].strip()
        #         percent = float(percent_str)
        #         self.status_bar.showMessage(f"🎤 WhisperX: {percent}% - Real-time transcriptie bezig...")
        #         
        #         # Update voortgangsbalk
        #         self._update_status_progress(percent, True)
        #         progress_found = True
        #     except:
        #         pass
        
        # Maak timing berichten prominenter
        # elif "⏱️" in message:
        #     # Timing berichten krijgen speciale behandeling
        #     if "Start verwerking" in message:
        #         self.status_bar.showMessage(f"🚀 {message}")
        #         self._update_status_progress(0, True)  # Start voortgangsbalk
        #     elif "voltooid in" in message:
        #         self.status_bar.showMessage(f"✅ {message}")
        #         self._update_status_progress(100, False)  # Voltooid, verberg voortgangsbalk
        #     elif "TOTALE VERWERKING" in message:
        #         self.status_bar.showMessage(f"🎯 {message}")
        #         self._update_status_progress(100, False)  # Voltooid, verberg voortgangsbalk
        #     else:
        #         self.status_bar.showMessage(message)
        # else:
        #     self.status_bar.showMessage(message)
        
        # Als geen voortgang gevonden, verberg voortgangsbalk
        # if not progress_found and hasattr(self, 'status_progress_bar'):
        #     self._update_status_progress(0, False)
    
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
            else:
                self.processing_panel.start_btn.setEnabled(True)
        
        # Blokkeer/deblokkeer menu items tijdens verwerking
        if hasattr(self, 'menuBar'):
            for action in self.menuBar().actions():
                # Alleen blokkeer Bestanden en Verwerking menu's tijdens verwerking
                if action.text() in ["Bestanden", "Verwerking"]:
                    action.setEnabled(not block)
        
        # BELANGRIJK: Behoud status labels en monitoring zichtbaar tijdens verwerking
        # Deze moeten altijd zichtbaar blijven voor gebruikers feedback
        if hasattr(self, 'gpu_status_label'):
            self.gpu_status_label.setVisible(True)  # Altijd zichtbaar
        if hasattr(self, 'gpu_memory_label'):
            self.gpu_memory_label.setVisible(True)  # Altijd zichtbaar
        if hasattr(self, 'ffmpeg_status_label'):
            self.ffmpeg_status_label.setVisible(True)  # Altijd zichtbaar
        if hasattr(self, 'ffmpeg_info_label'):
            self.ffmpeg_info_label.setVisible(True)  # Altijd zichtbaar
        if hasattr(self, 'libretranslate_status_label'):
            self.libretranslate_status_label.setVisible(True)  # Altijd zichtbaar
        if hasattr(self, 'libretranslate_info_label'):
            self.libretranslate_info_label.setVisible(True)  # Altijd zichtbaar
        
        # Behoud charts panel zichtbaar voor monitoring
        if hasattr(self, 'charts_panel'):
            # Zorg ervoor dat charts panel in de splitter blijft
            if hasattr(self, 'splitter') and self.charts_panel not in [self.splitter.widget(i) for i in range(self.splitter.count())]:
                # Charts panel is niet in splitter, voeg het toe
                self.splitter.addWidget(self.charts_panel)
                print("🔧 Charts panel toegevoegd aan splitter tijdens verwerking")
            
            self.charts_panel.setVisible(True)  # Altijd zichtbaar
            self.charts_panel.show()  # Force show
            
            # Zorg ervoor dat monitoring blijft draaien
            if block:
                # Start snelle monitoring tijdens verwerking
                self.charts_panel.start_processing_monitoring()
            else:
                # Stop snelle monitoring na verwerking
                self.charts_panel.stop_processing_monitoring()
        
        # BELANGRIJK: Zorg ervoor dat alle zichtbare panels zichtbaar blijven
        if hasattr(self, 'visible_panels'):
            for panel_name, panel_widget in self.visible_panels.items():
                if panel_widget:
                    panel_widget.setVisible(True)
                    panel_widget.show()
                    print(f"🔧 Panel {panel_name} geforceerd zichtbaar tijdens verwerking")
        
        # Zorg ervoor dat splitter alle panels toont
        if hasattr(self, 'splitter'):
            for i in range(self.splitter.count()):
                widget = self.splitter.widget(i)
                if widget:
                    widget.setVisible(True)
                    widget.show()
        
        # SCHAKEL OVERBODIGE STATUS UPDATES UIT - Deze zijn al zichtbaar in de verwerkingsbalk
        # self.update_status("Klaar")  # Uitgeschakeld - al zichtbaar in verwerkingsbalk
        # self.update_status("Verwerking gestart...")  # Uitgeschakeld - al zichtbaar in verwerkingsbalk
        # self.update_status("Verwerking gestopt")  # Uitgeschakeld - al zichtbaar in verwerkingsbalk
        
        print(f"🔒 MainWindow: UI {'geblokkeerd' if block else 'gedeblokkeerd'} - Monitoring blijft zichtbaar, overbodige status updates uitgeschakeld")
    
    def _ensure_monitoring_visibility(self):
        """Zorg ervoor dat monitoring panelen altijd zichtbaar blijven tijdens verwerking"""
        if hasattr(self, 'processing_active') and self.processing_active:
            # Verwerking is actief, forceer monitoring zichtbaarheid
            if hasattr(self, 'charts_panel'):
                self.charts_panel.setVisible(True)
                self.charts_panel.show()
                
                # Zorg ervoor dat charts panel in de splitter zit
                if hasattr(self, 'splitter') and self.charts_panel not in [self.splitter.widget(i) for i in range(self.splitter.count())]:
                    self.splitter.addWidget(self.charts_panel)
                    print("🔧 Monitoring panel hersteld tijdens verwerking")
            
            # Forceer alle zichtbare panels zichtbaar
            if hasattr(self, 'visible_panels'):
                for panel_name, panel_widget in self.visible_panels.items():
                    if panel_widget:
                        panel_widget.setVisible(True)
                        panel_widget.show()
            
            # Forceer splitter widgets zichtbaar
            if hasattr(self, 'splitter'):
                for i in range(self.splitter.count()):
                    widget = self.splitter.widget(i)
                    if widget:
                        widget.setVisible(True)
                        widget.show()
    
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
                ("settings_panel", self.settings_panel, 270),
                ("files_panel", self.files_panel, 370),
                ("processing_panel", self.processing_panel, 470),
                ("charts_panel", self.charts_panel, 320),
                ("batch_panel", self.batch_panel, 320)
            ]
            
            visible_sizes = []
            for panel_name, panel_widget, default_size in panel_configs:
                # Forceer belangrijke panelen altijd zichtbaar
                if panel_name in ["settings_panel", "files_panel", "processing_panel", "charts_panel"]:
                    splitter.addWidget(panel_widget)
                    self.visible_panels[panel_name] = panel_widget
                    visible_sizes.append(default_size)
                else:
                    # Alleen batch_panel is optioneel
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