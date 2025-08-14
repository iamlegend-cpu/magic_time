"""
Menu Handlers Mixin voor MainWindow
Bevat alle menu gerelateerde functies
"""

import os
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QDialog, QApplication
try:
    from ..config_window import ConfigWindow
except ImportError:
    ConfigWindow = None

try:
    from ..log_viewer import LogViewer
except ImportError:
    LogViewer = None

try:
    from ..components.menu_manager import MenuManager
except ImportError:
    MenuManager = None
# Lazy import van config_manager om circulaire import te voorkomen
def _get_config_manager():
    """Lazy config manager import om circulaire import te voorkomen"""
    try:
        from ...core.config import config_manager
        return config_manager
    except ImportError:
        try:
            from magic_time_studio.core.config import config_manager
            return config_manager
        except ImportError:
            return None

# Import processing modules
try:
    from ...core.all_functions import *
except ImportError:
    try:
        from magic_time_studio.core.all_functions import *
    except ImportError:
        pass

class MenuHandlersMixin:
    """Mixin voor menu handler functionaliteit"""
    
    def create_menu(self):
        """Maak menu aan"""
        menubar = self.menuBar()
        
        # Bestanden menu
        files_menu = menubar.addMenu("Bestanden")
        
        add_file_action = files_menu.addAction("📁 Bestand toevoegen")
        add_file_action.triggered.connect(self.add_file)
        
        add_folder_action = files_menu.addAction("📂 Map toevoegen")
        add_folder_action.triggered.connect(self.add_folder)
        
        files_menu.addSeparator()
        
        remove_action = files_menu.addAction("🗑️ Verwijder geselecteerd")
        remove_action.triggered.connect(self.remove_selected)
        
        # Verwijder de clear_list functionaliteit - gebruikers kunnen de hele lijst niet wissen
        # clear_action = files_menu.addAction("🗑️ Wis lijst")
        # clear_action.triggered.connect(self.clear_list)
        
        # Verwerking menu
        processing_menu = menubar.addMenu("Verwerking")
        
        start_action = processing_menu.addAction("▶️ Start verwerking")
        start_action.triggered.connect(self.start_processing)
        
        # Configuratie menu
        config_menu = menubar.addMenu("Configuratie")
        
        settings_action = config_menu.addAction("⚙️ Instellingen")
        settings_action.triggered.connect(self.show_config)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = help_menu.addAction("ℹ️ Over")
        about_action.triggered.connect(self.show_about)
    
    def add_file(self):
        """Voeg bestand toe via menu"""
        # Voorkom toevoegen tijdens verwerking
        if hasattr(self, 'processing_active') and self.processing_active:
            print("⚠️ Kan geen bestanden toevoegen tijdens verwerking")
            return
        
        files, _ = QFileDialog.getOpenFileNames(
            self, "Selecteer bestanden", "",
            "Video bestanden (*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm)"
        )
        added_count = 0
        video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']
        
        for file_path in files:
            # Filter alleen video bestanden
            if any(file_path.lower().endswith(ext) for ext in video_extensions):
                if file_path not in self.files_panel.get_file_list():
                    self.files_panel.file_list.append(file_path)
                    self.files_panel.file_list_widget.addItem(os.path.basename(file_path))
                    added_count += 1
        
        if added_count > 0:
            # Update remove button state na toevoegen
            self.files_panel.update_remove_button_state()
            self.update_status(f"✅ {added_count} video bestand(en) toegevoegd")
        else:
            self.update_status("⚠️ Geen video bestanden toegevoegd")
    
    def add_folder(self):
        """Voeg map toe via menu"""
        # Voorkom toevoegen tijdens verwerking
        if hasattr(self, 'processing_active') and self.processing_active:
            print("⚠️ Kan geen bestanden toevoegen tijdens verwerking")
            return
        
        folder = QFileDialog.getExistingDirectory(self, "Selecteer map")
        if folder:
            added_count = 0
            video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']
            
            # Zoek naar video bestanden in de map en subdirectories
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in video_extensions):
                        file_path = os.path.join(root, file)
                        if file_path not in self.files_panel.get_file_list():
                            self.files_panel.file_list.append(file_path)
                            self.files_panel.file_list_widget.addItem(os.path.basename(file_path))
                            added_count += 1
            
            if added_count > 0:
                # Update remove button state na toevoegen
                self.files_panel.update_remove_button_state()
                self.update_status(f"✅ {added_count} video bestand(en) uit map '{os.path.basename(folder)}' toegevoegd")
            else:
                self.update_status(f"⚠️ Geen video bestanden gevonden in map '{os.path.basename(folder)}'")
    
    def remove_selected(self):
        """Verwijder geselecteerd bestand via menu"""
        # Voorkom verwijdering tijdens verwerking
        if hasattr(self, 'processing_active') and self.processing_active:
            print("⚠️ Kan bestanden niet verwijderen tijdens verwerking")
            QMessageBox.warning(self, "Waarschuwing", "Kan bestanden niet verwijderen tijdens verwerking!")
            return
        
        current_row = self.files_panel.file_list_widget.currentRow()
        if current_row >= 0:
            # Voorkom verwijdering van het eerste bestand (index 0)
            if current_row == 0:
                print("⚠️ Kan het eerste bestand niet verwijderen tijdens verwerking")
                QMessageBox.warning(self, "Waarschuwing", "Kan het eerste bestand niet verwijderen!")
                return
            
            self.files_panel.file_list_widget.takeItem(current_row)
            self.files_panel.file_list.pop(current_row)
            # Update de remove button state na verwijdering
            self.files_panel.update_remove_button_state()
            self.update_status("Geselecteerd bestand verwijderd")
    
    def show_config(self):
        """Toon configuratie venster"""
        if self.processing_active:
            QMessageBox.warning(self, "Niet toegestaan", "Configuratie kan niet worden gewijzigd tijdens verwerking.")
            return
        
        self.config_window = ConfigWindow(self)
        self.config_window.set_callback(self.on_config_saved)
        if self.config_window.exec() == QDialog.DialogCode.Accepted:
            self.update_status("Configuratie opgeslagen")
    
    def on_config_saved(self, config=None):
        """Callback wanneer configuratie wordt opgeslagen"""
        print("💾 Configuratie opgeslagen, update UI")
        
        # Update vertaler status als settings panel bestaat
        if hasattr(self, 'settings_panel') and self.settings_panel:
            try:
                self.settings_panel.update_translator_status()
                print("✅ Vertaler status bijgewerkt")
            except Exception as e:
                print(f"⚠️ Fout bij updaten vertaler status: {e}")
        
        # Herlaad interface als panel zichtbaarheid is gewijzigd
        self.reload_interface()
    
    def show_log(self):
        """Toon log viewer"""
        if not self.log_viewer:
            self.log_viewer = LogViewer(self)
        self.log_viewer.show()
    
    def performance_test(self):
        """Performance test"""
        print("📊 Menu: Performance test")
        try:
            # Import performance tracker
            try:
                from ...models.performance_tracker import performance_tracker
            except ImportError:
                try:
                    from magic_time_studio.models.performance_tracker import performance_tracker
                except ImportError:
                    performance_tracker = None
            
            # Import diagnostiek functies
            try:
                from ...core.diagnostics import run_full_diagnostics, print_diagnostics
            except ImportError:
                try:
                    from magic_time_studio.core.diagnostics import run_full_diagnostics, print_diagnostics
                except ImportError:
                    run_full_diagnostics = None
                    print_diagnostics = None
            
            try:
                from ...core.diagnostics import cuda_test
            except ImportError:
                try:
                    from magic_time_studio.core.diagnostics import cuda_test
                except ImportError:
                    cuda_test = None

            if performance_tracker:
                performance_tracker.start_tracking()
                import time
                time.sleep(2)
                report = performance_tracker.generate_report()
                whisper_status = f"""
Whisper Model: {'Geladen' if hasattr(self, 'whisper_manager') and self.whisper_manager else 'Niet geladen'}
Whisper Type: {'whisperx' if hasattr(self, 'whisper_manager') and self.whisper_manager else 'Niet beschikbaar'}
"""
                report_text = report + whisper_status
                QMessageBox.information(self, "Performance Test", report_text)
            else:
                QMessageBox.warning(self, "Fout", "Performance tracker module niet gevonden.")
        except Exception as e:
            print(f"❌ Fout bij performance test: {e}")
            QMessageBox.critical(self, "Fout", f"Performance test gefaald: {e}")
    
    def whisper_diagnose(self):
        """WhisperX diagnose"""
        print("🎤 WhisperX diagnose gestart")
        try:
            from ...core.diagnostics import run_full_diagnostics, print_diagnostics
        except ImportError:
            try:
                from magic_time_studio.core.diagnostics import run_full_diagnostics, print_diagnostics
            except ImportError:
                run_full_diagnostics = None
                print_diagnostics = None
            
            # Voer volledige diagnostiek uit
            diagnostics = run_full_diagnostics()
            
            # Toon resultaten in een dialoog
            from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout
            
            dialog = QDialog(self.main_window)
            dialog.setWindowTitle("Magic Time Studio Diagnostics")
            dialog.setMinimumSize(600, 400)
            
            layout = QVBoxLayout(dialog)
            
            # Text area voor diagnostiek
            text_edit = QTextEdit()
            text_edit.setReadOnly(True)
            layout.addWidget(text_edit)
            
            # Voeg diagnostiek toe
            text_edit.append("🔍 Magic Time Studio Diagnostics")
            text_edit.append("=" * 50)
            
            # Systeem info
            system_info = diagnostics["system_info"]
            text_edit.append(f"🖥️ Platform: {system_info['platform']}")
            text_edit.append(f"🐍 Python: {system_info['python_version']}")
            text_edit.append(f"💻 Processor: {system_info['processor']}")
            
            # WhisperX info
            whisperx_info = diagnostics["whisperx"]
            text_edit.append(f"\n🎤 WhisperX: {'✅ Beschikbaar' if whisperx_info['whisperx_available'] else '❌ Niet beschikbaar'}")
            if whisperx_info['whisperx_available']:
                text_edit.append(f"   Versie: {whisperx_info['version']}")
                text_edit.append(f"   GPU: {'✅ Ondersteund' if whisperx_info['gpu_support'] else '❌ Niet ondersteund'}")
                if whisperx_info['gpu_support']:
                    text_edit.append(f"   GPU Aantal: {whisperx_info['gpu_count']}")
                    text_edit.append(f"   GPU Naam: {whisperx_info['gpu_name']}")
            
            # FFmpeg info
            ffmpeg_info = diagnostics["ffmpeg"]
            text_edit.append(f"\n🎬 FFmpeg: {'✅ Beschikbaar' if ffmpeg_info['ffmpeg_available'] else '❌ Niet beschikbaar'}")
            text_edit.append(f"   FFprobe: {'✅ Beschikbaar' if ffmpeg_info['ffprobe_available'] else '❌ Niet beschikbaar'}")
            if ffmpeg_info['version']:
                text_edit.append(f"   Versie: {ffmpeg_info['version']}")
            
            # Knoppen
            button_layout = QHBoxLayout()
            
            close_button = QPushButton("Sluiten")
            close_button.clicked.connect(dialog.accept)
            button_layout.addWidget(close_button)
            
            copy_button = QPushButton("Kopieer naar klembord")
            copy_button.clicked.connect(lambda: self._copy_diagnostics_to_clipboard(text_edit.toPlainText()))
            button_layout.addWidget(copy_button)
            
            layout.addLayout(button_layout)
            
            dialog.exec()
            
        except Exception as e:
            print(f"⚠️ Fout bij uitvoeren diagnostiek: {e}")
            # Fallback naar console output
            print_diagnostics()

    def cuda_test(self):
        """CUDA test (nu onderdeel van WhisperX diagnose)"""
        print("🔧 CUDA test gestart (via WhisperX diagnose)")
        self.whisper_diagnose()  # Gebruik de nieuwe diagnostiek
    
    def _copy_diagnostics_to_clipboard(self, text: str):
        """Kopieer diagnostiek naar klembord"""
        try:
            from PyQt6.QtWidgets import QApplication
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            print("✅ Diagnostiek gekopieerd naar klembord")
        except Exception as e:
            print(f"⚠️ Fout bij kopiëren naar klembord: {e}")
    
    def change_theme(self, theme_name: str):
        """Verander thema"""
        self.modern_styling.apply_theme(QApplication.instance(), theme_name)
        self.update_status(f"Thema gewijzigd naar: {theme_name}")
    
    def show_charts_panel(self):
        """Toon/verberg charts panel"""
        # Voorkom dat charts panel wordt verborgen tijdens verwerking
        if hasattr(self, 'processing_active') and self.processing_active:
            self.update_status("⚠️ Grafieken panel kan niet worden verborgen tijdens verwerking")
            return
        
        if "charts_panel" in self.visible_panels:
            # Panel is zichtbaar, verberg het
            self.charts_panel.hide()
            self.splitter.takeWidget(self.charts_panel)
            del self.visible_panels["charts_panel"]
            config_mgr = _get_config_manager()
            if config_mgr:
                config_mgr.set_panel_visibility("charts_panel", False)
            self.update_status("Grafieken panel verborgen")
        else:
            # Panel is verborgen, toon het
            self.splitter.addWidget(self.charts_panel)
            self.charts_panel.show()
            self.visible_panels["charts_panel"] = self.charts_panel
            config_mgr = _get_config_manager()
            if config_mgr:
                config_mgr.set_panel_visibility("charts_panel", True)
            self.update_status("Grafieken panel zichtbaar")
        
        # Pas window grootte aan
        self._adjust_window_size()
    
    def show_batch_panel(self):
        """Toon/verberg batch panel"""
        if "batch_panel" in self.visible_panels:
            # Panel is zichtbaar, verberg het
            self.batch_panel.hide()
            self.splitter.takeWidget(self.batch_panel)
            del self.visible_panels["batch_panel"]
            config_mgr = _get_config_manager()
            if config_mgr:
                config_mgr.set_panel_visibility("batch_panel", False)
            self.update_status("Batch panel verborgen")
        else:
            # Panel is verborgen, toon het
            self.splitter.addWidget(self.batch_panel)
            self.batch_panel.show()
            self.visible_panels["batch_panel"] = self.batch_panel
            config_mgr = _get_config_manager()
            if config_mgr:
                config_mgr.set_panel_visibility("batch_panel", True)
            self.update_status("Batch panel zichtbaar")
        
        # Pas window grootte aan
        self._adjust_window_size()
    
    def _adjust_window_size(self):
        """Pas window grootte aan op basis van zichtbare panels"""
        try:
            # Behoud maximized state
            if not self.isMaximized():
                self.showMaximized()
            
            # Force een layout update
            self.updateGeometry()
            self.update()
                
        except Exception as e:
            print(f"❌ Fout bij aanpassen window grootte: {e}")
    
    def show_about(self):
        """Toon about dialog"""
        about_text = """
Magic Time Studio v3.0

Een geavanceerde video ondertiteling applicatie met AI-powered transcriptie.

Functies:
• Automatische transcriptie met Whisper AI
• Ondersteuning voor meerdere video formaten
• Real-time verwerking en voortgang
• Moderne PyQt6 gebruikersinterface
• Configuratie en thema ondersteuning

Technologie:
• PyQt6 voor de gebruikersinterface
• OpenAI Whisper voor transcriptie
• FFmpeg voor video verwerking
• PyTorch voor AI modellen

Ontwikkeld met ❤️ voor content creators.
        """
        
        QMessageBox.about(self, "Over Magic Time Studio", about_text.strip()) 