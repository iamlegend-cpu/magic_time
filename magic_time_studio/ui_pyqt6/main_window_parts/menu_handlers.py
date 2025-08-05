"""
Menu Handlers Mixin voor MainWindow
Bevat alle menu gerelateerde functies
"""

import os
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QDialog, QApplication
from magic_time_studio.ui_pyqt6.config_window import ConfigWindow
from magic_time_studio.ui_pyqt6.log_viewer import LogViewer
from magic_time_studio.ui_pyqt6.components.menu_manager import MenuManager
from magic_time_studio.core.config import config_manager
from magic_time_studio.processing import whisper_processor, translator, audio_processor

class MenuHandlersMixin:
    """Mixin voor menu handler functionaliteit"""
    
    def create_menu(self):
        """Maak de menubalk"""
        self.menu_manager = MenuManager(self)
        
        # Connect menu signals
        self.menu_manager.add_file_triggered.connect(self.add_file)
        self.menu_manager.add_folder_triggered.connect(self.add_folder)
        self.menu_manager.remove_selected_triggered.connect(self.remove_selected)
        self.menu_manager.clear_list_triggered.connect(self.clear_list)
        self.menu_manager.start_processing_triggered.connect(self.start_processing)
        self.menu_manager.stop_processing_triggered.connect(self.stop_processing)
        self.menu_manager.show_config_triggered.connect(self.show_config)
        self.menu_manager.show_log_triggered.connect(self.show_log)
        self.menu_manager.performance_test_triggered.connect(self.performance_test)
        self.menu_manager.cuda_test_triggered.connect(self.cuda_test)
        self.menu_manager.whisper_diagnose_triggered.connect(self.whisper_diagnose)
        self.menu_manager.test_completed_files_triggered.connect(self.test_completed_files)
        self.menu_manager.theme_changed.connect(self.change_theme)
        self.menu_manager.exit_triggered.connect(self.close)
        
        # View menu signals
        self.menu_manager.show_charts_triggered.connect(self.show_charts_panel)
        self.menu_manager.show_batch_triggered.connect(self.show_batch_panel)
    
    def add_file(self):
        """Voeg bestand toe via menu"""
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
            self.update_status(f"✅ {added_count} video bestand(en) toegevoegd")
        else:
            self.update_status("⚠️ Geen video bestanden toegevoegd")
    
    def add_folder(self):
        """Voeg map toe via menu"""
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
                self.update_status(f"✅ {added_count} video bestand(en) uit map '{os.path.basename(folder)}' toegevoegd")
            else:
                self.update_status(f"⚠️ Geen video bestanden gevonden in map '{os.path.basename(folder)}'")
    
    def remove_selected(self):
        """Verwijder geselecteerd bestand via menu"""
        current_row = self.files_panel.file_list_widget.currentRow()
        if current_row >= 0:
            self.files_panel.file_list_widget.takeItem(current_row)
            self.files_panel.file_list.pop(current_row)
            self.update_status("Geselecteerd bestand verwijderd")
    
    def clear_list(self):
        """Wis de lijst via menu"""
        self.files_panel.file_list_widget.clear()
        self.files_panel.file_list.clear()
        self.update_status("Lijst gewist")
    
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
        self.settings_panel.settings_panel.update_translator_status()
        
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
            from magic_time_studio.models.performance_tracker import performance_tracker
            performance_tracker.start_tracking()
            import time
            time.sleep(2)
            report = performance_tracker.generate_report()
            extra_status = f"""
Whisper Model: {'Geladen' if whisper_processor.is_model_loaded() else 'Niet geladen'}
FFmpeg: {'Beschikbaar' if audio_processor.is_ffmpeg_available() else 'Niet beschikbaar'}
Vertaler: {translator.get_current_service()}
"""
            report_text = report + extra_status
            QMessageBox.information(self, "Performance Test", report_text)
        except Exception as e:
            print(f"❌ Fout bij performance test: {e}")
            QMessageBox.critical(self, "Fout", f"Performance test gefaald: {e}")
    
    def whisper_diagnose(self):
        """Whisper diagnose"""
        print("🎤 Whisper diagnose gestart")
        try:
            from magic_time_studio.core.diagnostics import whisper_diagnose
            result = whisper_diagnose()
            QMessageBox.information(self, "Whisper Diagnose", result)
        except Exception as e:
            print(f"❌ Fout bij Whisper diagnose: {e}")
            QMessageBox.critical(self, "Fout", f"Whisper diagnose gefaald: {e}")

    def cuda_test(self):
        """CUDA test"""
        print("🔧 CUDA test gestart")
        try:
            from magic_time_studio.core.diagnostics import cuda_test
            result = cuda_test()
            QMessageBox.information(self, "CUDA Test", result)
        except Exception as e:
            print(f"❌ Fout bij CUDA test: {e}")
            QMessageBox.critical(self, "Fout", f"CUDA test gefaald: {e}")
    
    def change_theme(self, theme_name: str):
        """Verander thema"""
        self.modern_styling.apply_theme(QApplication.instance(), theme_name)
        self.update_status(f"Thema gewijzigd naar: {theme_name}")
    
    def show_charts_panel(self):
        """Toon/verberg charts panel"""
        if "charts" in self.visible_panels:
            # Panel is zichtbaar, verberg het
            self.charts_panel.hide()
            self.splitter.removeWidget(self.charts_panel)
            del self.visible_panels["charts"]
            config_manager.set_panel_visibility("charts", False)
            self.update_status("Grafieken panel verborgen")
        else:
            # Panel is verborgen, toon het
            self.splitter.addWidget(self.charts_panel)
            self.charts_panel.show()
            self.visible_panels["charts"] = self.charts_panel
            config_manager.set_panel_visibility("charts", True)
            self.update_status("Grafieken panel zichtbaar")
    
    def show_batch_panel(self):
        """Toon/verberg batch panel"""
        if "batch" in self.visible_panels:
            # Panel is zichtbaar, verberg het
            self.batch_panel.hide()
            self.splitter.removeWidget(self.batch_panel)
            del self.visible_panels["batch"]
            config_manager.set_panel_visibility("batch", False)
            self.update_status("Batch panel verborgen")
        else:
            # Panel is verborgen, toon het
            self.splitter.addWidget(self.batch_panel)
            self.batch_panel.show()
            self.visible_panels["batch"] = self.batch_panel
            config_manager.set_panel_visibility("batch", True)
            self.update_status("Batch panel zichtbaar") 