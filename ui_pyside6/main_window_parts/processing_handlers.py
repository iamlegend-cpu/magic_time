"""
Processing Handlers Mixin voor MainWindow
Bevat alle processing gerelateerde functies
"""

from typing import List, Dict
from PySide6.QtWidgets import QMessageBox, QApplication
import os

class ProcessingHandlersMixin:
    """Mixin voor processing handler functionaliteit"""
    
    def on_processing_started(self, files: List[str], settings: Dict):
        """Handle processing start"""
        print(f"🏠 MainWindow: on_processing_started aangeroepen met {len(files)} bestanden")
        
        # Als er geen bestanden zijn meegegeven, haal ze op uit de files panel
        if not files:
            print("🔍 [DEBUG] Geen bestanden meegegeven, haal op uit files panel")
            files = self.files_panel.get_file_list()
            print(f"🔍 [DEBUG] {len(files)} bestanden opgehaald uit files panel")
        
        # Als er geen instellingen zijn meegegeven, haal ze op uit de settings panel
        if not settings:
            print("🔍 [DEBUG] Geen instellingen meegegeven, haal op uit settings panel")
            try:
                # Probeer verschillende methoden om settings op te halen
                if hasattr(self.settings_panel, 'get_current_settings'):
                    settings = self.settings_panel.get_current_settings()
                elif hasattr(self.settings_panel, 'settings_panel') and hasattr(self.settings_panel.settings_panel, 'get_current_settings'):
                    settings = self.settings_panel.settings_panel.get_current_settings()
                elif hasattr(self.settings_panel, 'get_settings'):
                    settings = self.settings_panel.get_settings()
                else:
                    print("⚠️ [WAARSCHUWING] Kan geen settings ophalen uit settings panel")
                    settings = {}
            except Exception as e:
                print(f"⚠️ [WAARSCHUWING] Fout bij ophalen settings: {e}")
                settings = {}
            print(f"🔍 [DEBUG] Instellingen opgehaald: {settings}")
        
        # Controleer of er bestanden zijn
        if not files:
            print("⚠️ Geen bestanden gevonden voor verwerking")
            QMessageBox.warning(self, "Waarschuwing", "Geen bestanden geselecteerd! Voeg eerst bestanden toe via 'Bestand toevoegen' of 'Map toevoegen'.")
            return
        
        print(f"🏠 MainWindow: Start verwerking met {len(files)} bestanden")
        self.processing_active = True
        
        # Start GPU monitoring voor verwerking
        if hasattr(self, 'charts_panel'):
            self.charts_panel.start_processing_monitoring()
            # Informeer alleen GPU monitor over verwerkingsstatus
            if hasattr(self.charts_panel, 'gpu_monitor'):
                self.charts_panel.gpu_monitor.set_processing_status(True, True)  # WhisperX verwerking actief
        
        # Blokkeer UI tijdens verwerking
        self.block_ui_during_processing(True)
        
        # Start daadwerkelijke verwerking
        self.start_processing_from_panel(files, settings)
        
        # Emit signal voor andere componenten
        self.main_processing_started.emit(files, settings)
        # self.update_status("Verwerking gestart...")  # Uitgeschakeld - al zichtbaar in verwerkingsbalk
    

    
    def on_file_completed(self, file_path: str, output_path: str = None):
        """Handle file completed event"""
        print(f"🔍 [DEBUG] MainWindow.on_file_completed aangeroepen: {file_path}")
        
        # Voeg bestand toe aan completed list
        self.add_completed_file(file_path, output_path)
        
        # Verwijder bestand uit "nog te doen" lijst
        if hasattr(self, 'files_panel'):
            # Probeer eerst via file list manager
            if hasattr(self, 'processing_panel') and hasattr(self.processing_panel, 'file_list_manager'):
                print(f"🔍 Probeer bestand te verwijderen via file list manager: {file_path}")
                filename = os.path.basename(file_path)
                removal_success = self.processing_panel.file_list_manager.remove_completed_file_from_list(filename)
                
                if removal_success:
                    print(f"✅ Bestand succesvol verwijderd via file list manager: {filename}")
                else:
                    print(f"⚠️ Kon bestand niet verwijderen via file list manager, probeer direct: {filename}")
                    # Fallback: direct verwijderen
                    self.files_panel.remove_file(file_path)
                    print(f"🔍 [DEBUG] Bestand verwijderd uit files_panel: {file_path}")
            else:
                print(f"⚠️ File list manager niet beschikbaar, gebruik directe methode")
                self.files_panel.remove_file(file_path)
                print(f"🔍 [DEBUG] Bestand verwijderd uit files_panel: {file_path}")
        else:
            print(f"🔍 [DEBUG] Bestand niet gevonden in lijst: {file_path}")
    
    def update_progress(self, value: float, status: str = ""):
        """Update voortgangsbalk"""
        if hasattr(self, 'processing_panel'):
            self.processing_panel.update_progress(value, status)
            # Console output wordt al afgehandeld door update_progress
    
    def processing_finished(self):
        """Verwerking voltooid"""
        print("✅ MainWindow: processing_finished aangeroepen")
        self.processing_active = False
        
        # Stop GPU en FFmpeg monitoring na verwerking
        if hasattr(self, 'charts_panel'):
            self.charts_panel.stop_processing_monitoring()
            # Informeer monitors over verwerkingsstatus
            if hasattr(self.charts_panel, 'gpu_monitor'):
                self.charts_panel.gpu_monitor.set_processing_status(False, False)  # Verwerking gestopt
            if hasattr(self.charts_panel, 'ffmpeg_monitor'):
                self.charts_panel.ffmpeg_monitor.set_processing_status(False)  # Verwerking gestopt
        
        # Deblokkeer UI na verwerking
        self.block_ui_during_processing(False)
        
        # Zorg ervoor dat alle UI elementen weer beschikbaar zijn
        if hasattr(self, 'files_panel'):
            # Reset files panel state
            self.files_panel.processing_active = False
            self.files_panel.add_file_btn.setEnabled(True)
            self.files_panel.add_folder_btn.setEnabled(True)
            self.files_panel.file_list_widget.setEnabled(True)
            self.files_panel.clear_btn.setEnabled(True)
            self.files_panel.update_button_states()
            
            # Drag & drop zone is verwijderd, gebruik knoppen onderaan venster
            pass
        
        if hasattr(self, 'settings_panel'):
            # Ontdooi settings panel
            self.settings_panel.unfreeze_settings()
        
        if hasattr(self, 'batch_panel'):
            # Enable batch panel
            self.batch_panel.setEnabled(True)
        
        if hasattr(self, 'processing_panel'):
            # Reset processing panel
            if hasattr(self.processing_panel, 'processing_finished'):
                self.processing_panel.processing_finished()
            else:
                print("⚠️ processing_finished methode niet gevonden in processing_panel")
        
        # Enable menu items
        if hasattr(self, 'menuBar'):
            for action in self.menuBar().actions():
                action.setEnabled(True)
        
        # self.update_status("Verwerking voltooid!")  # Uitgeschakeld - al zichtbaar in verwerkingsbalk
        print("✅ MainWindow: UI volledig gedeblokkeerd")
    
    def add_completed_file(self, file_path: str, output_path: str = None):
        """Voeg voltooid bestand toe aan de lijst"""
        if hasattr(self, 'processing_panel'):
            self.processing_panel.add_completed_file(file_path, output_path)
            # self.update_status(f"✅ {os.path.basename(file_path)} voltooid")  # Uitgeschakeld - al zichtbaar in verwerkingsbalk
        else:
            print("⚠️ processing_panel niet beschikbaar")
    
    def get_completed_files(self) -> List[str]:
        """Haal voltooide bestanden lijst op"""
        if hasattr(self, 'processing_panel'):
            return self.processing_panel.get_completed_files()
        return []
    
    def _add_test_completed_files(self):
        """Test functie om voltooide bestanden toe te voegen"""
        test_files = [
            "test_video_1.mp4",
            "test_audio_1.mp3", 
            "test_video_2.avi"
        ]
        
        for file_path in test_files:
            self.add_completed_file(file_path, f"output_{file_path}")
        
        # self.update_status(f"✅ {len(test_files)} test bestanden toegevoegd aan voltooide lijst")  # Uitgeschakeld - al zichtbaar in verwerkingsbalk
    
    def test_completed_files(self):
        """Test voltooide bestanden functionaliteit"""
        self._add_test_completed_files()
    
    def start_processing_from_panel(self, files: List[str], settings: Dict):
        """Start verwerking wanneer ProcessingPanel start knop wordt ingedrukt (geoptimaliseerd)"""
        # Controleer of er al verwerking bezig is
        if hasattr(self, 'processing_active') and self.processing_active:
            print("⚠️ Verwerking al bezig, negeer start request")
            return
        
        print(f"🚀 Start verwerking met {len(files)} bestanden...")
        
        # Start GPU en FFmpeg monitoring
        if hasattr(self, 'charts_panel'):
            self.charts_panel.start_processing_monitoring()
            # Informeer monitors over verwerkingsstatus
            if hasattr(self.charts_panel, 'gpu_monitor'):
                self.charts_panel.gpu_monitor.set_processing_status(True, True)  # Verwerking gestart
            if hasattr(self.charts_panel, 'ffmpeg_monitor'):
                self.charts_panel.ffmpeg_monitor.set_processing_status(True)  # Verwerking gestart
        
        if not files:
            QMessageBox.warning(self, "Waarschuwing", "Geen bestanden geselecteerd! Voeg eerst bestanden toe via 'Bestand toevoegen' of 'Map toevoegen'.")
            return
        
        # Start verwerking direct met de doorgegeven bestanden en instellingen
        self.processing_panel.start_processing_with_settings(files, settings)
    
    def start_processing(self):
        """Start verwerking via menu (geoptimaliseerd)"""
        # Controleer of er al verwerking bezig is
        if hasattr(self, 'processing_active') and self.processing_active:
            print("⚠️ Verwerking al bezig, negeer start request")
            return
            
        files = self.files_panel.get_file_list()
        
        if not files:
            QMessageBox.warning(self, "Waarschuwing", "Geen bestanden geselecteerd! Voeg eerst bestanden toe via 'Bestand toevoegen' of 'Map toevoegen'.")
            return
        
        # Haal instellingen op uit settings panel
        settings = self.settings_panel.settings_panel.get_current_settings()
        
        print(f"🚀 Start verwerking via menu met {len(files)} bestanden...")
        # Start verwerking met instellingen
        self.processing_panel.start_processing_with_settings(files, settings)
    
 