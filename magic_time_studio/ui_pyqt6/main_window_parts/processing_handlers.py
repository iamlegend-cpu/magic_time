"""
Processing Handlers Mixin voor MainWindow
Bevat alle processing gerelateerde functies
"""

from typing import List, Dict
from PyQt6.QtWidgets import QMessageBox, QApplication
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
            settings = self.settings_panel.settings_panel.get_current_settings()
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
        
        # Blokkeer UI tijdens verwerking
        self.block_ui_during_processing(True)
        
        self.processing_started.emit(files, settings)
        self.update_status("Verwerking gestart...")
    
    def on_processing_stopped(self):
        """Handle processing stop"""
        print("🛑 MainWindow: on_processing_stopped aangeroepen")
        self.processing_active = False
        
        # Stop GPU monitoring na verwerking
        if hasattr(self, 'charts_panel'):
            self.charts_panel.stop_processing_monitoring()
        
        # Deblokkeer UI na verwerking
        self.block_ui_during_processing(False)
        
        # Zorg ervoor dat alle UI elementen weer beschikbaar zijn
        if hasattr(self, 'files_panel'):
            # Reset files panel state
            self.files_panel.processing_active = False
            
            # Toevoegen knoppen blijven altijd beschikbaar
            self.files_panel.add_file_btn.setEnabled(True)
            self.files_panel.add_folder_btn.setEnabled(True)
            self.files_panel.file_list_widget.setEnabled(True)
            
            # Update button states (verwijder/wis knoppen worden hier gecontroleerd)
            self.files_panel.update_button_states()
            
            # Drag & drop zone is verwijderd, gebruik knoppen onderaan venster
            pass
        
        if hasattr(self, 'settings_panel'):
            # Ontdooi settings panel
            self.settings_panel.unfreeze_settings()
        
        if hasattr(self, 'batch_panel'):
            # Enable batch panel
            self.batch_panel.setEnabled(True)
        
        # Enable menu items
        if hasattr(self, 'menuBar'):
            for action in self.menuBar().actions():
                action.setEnabled(True)
        
        self.processing_stopped.emit()
        self.update_status("Verwerking gestopt")
        print("✅ MainWindow: UI gedeblokkeerd na stoppen")
    
    def _on_processing_started(self, files: List[str], settings: Dict):
        """Internal handler voor processing start"""
        print(f"🏠 MainWindow: _on_processing_started aangeroepen met {len(files)} bestanden")
        # Deze methode wordt aangeroepen door de signal connection
        # De daadwerkelijke verwerking wordt afgehandeld door de hoofdapplicatie
    
    def _on_processing_stopped(self):
        """Internal handler voor processing stop"""
        print("🛑 Stop verwerking")
        # Deze methode wordt aangeroepen door de signal connection
    
    def on_file_completed(self, file_path: str):
        """Handle file completed event"""
        print(f"🔍 [DEBUG] MainWindow.on_file_completed aangeroepen: {file_path}")
        
        # Verwijder bestand uit "nog te doen" lijst
        if hasattr(self, 'files_panel'):
            self.files_panel.remove_file(file_path)
            print(f"🔍 [DEBUG] Bestand verwijderd uit files_panel: {file_path}")
        else:
            print(f"🔍 [DEBUG] Bestand niet gevonden in lijst: {file_path}")
    
    def update_progress(self, value: float, status: str = ""):
        """Update voortgangsbalk"""
        if hasattr(self, 'processing_panel'):
            self.processing_panel.update_progress(value, status)
            # Voeg ook toe aan console output voor real-time updates
            if status:
                self.processing_panel.add_console_output(status, value / 100.0)
    
    def processing_finished(self):
        """Verwerking voltooid"""
        print("✅ MainWindow: processing_finished aangeroepen")
        self.processing_active = False
        
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
        
        self.update_status("Verwerking voltooid!")
        print("✅ MainWindow: UI volledig gedeblokkeerd")
    
    def add_completed_file(self, file_path: str, output_path: str = None):
        """Voeg voltooid bestand toe aan de lijst"""
        print(f"🔍 [DEBUG] MainWindow.add_completed_file aangeroepen: {file_path}")
        if hasattr(self, 'processing_panel'):
            print(f"🔍 [DEBUG] processing_panel bestaat, roep add_completed_file aan...")
            self.processing_panel.add_completed_file(file_path, output_path)
            self.update_status(f"✅ {os.path.basename(file_path)} voltooid")
            print(f"🔍 [DEBUG] add_completed_file voltooid")
        else:
            print(f"🔍 [DEBUG] ERROR: processing_panel bestaat niet!")
    
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
        
        self.update_status(f"✅ {len(test_files)} test bestanden toegevoegd aan voltooide lijst")
    
    def test_completed_files(self):
        """Test voltooide bestanden functionaliteit"""
        self._add_test_completed_files()
    
    def start_processing_from_panel(self, files: List[str], settings: Dict):
        """Start verwerking wanneer ProcessingPanel start knop wordt ingedrukt"""
        # Controleer of er al verwerking bezig is
        if hasattr(self, 'processing_active') and self.processing_active:
            print("⚠️ Verwerking al bezig, negeer start request")
            return
            
        # Haal bestanden op uit FilesPanel
        files = self.files_panel.get_file_list()
        
        print(f"🔍 [DEBUG] MainWindow.start_processing_from_panel: {len(files)} bestanden in lijst")
        for i, file_path in enumerate(files):
            print(f"🔍 [DEBUG] MainWindow.start_processing_from_panel: Bestand {i+1}: {file_path}")
        
        if not files:
            QMessageBox.warning(self, "Waarschuwing", "Geen bestanden geselecteerd! Voeg eerst bestanden toe via 'Bestand toevoegen' of 'Map toevoegen'.")
            return
        
        # Haal instellingen op uit settings panel
        settings = self.settings_panel.settings_panel.get_current_settings()
        
        print(f"🔍 [DEBUG] MainWindow.start_processing_from_panel: Start verwerking met {len(files)} bestanden")
        # Start verwerking met instellingen
        self.processing_panel.start_processing_with_settings(files, settings)
    
    def start_processing(self):
        """Start verwerking via menu"""
        # Controleer of er al verwerking bezig is
        if hasattr(self, 'processing_active') and self.processing_active:
            print("⚠️ Verwerking al bezig, negeer start request")
            return
            
        files = self.files_panel.get_file_list()
        
        print(f"🔍 [DEBUG] MainWindow.start_processing: {len(files)} bestanden in lijst")
        for i, file_path in enumerate(files):
            print(f"🔍 [DEBUG] MainWindow.start_processing: Bestand {i+1}: {file_path}")
        
        if not files:
            QMessageBox.warning(self, "Waarschuwing", "Geen bestanden geselecteerd! Voeg eerst bestanden toe via 'Bestand toevoegen' of 'Map toevoegen'.")
            return
        
        # Haal instellingen op uit settings panel
        settings = self.settings_panel.settings_panel.get_current_settings()
        
        print(f"🔍 [DEBUG] MainWindow.start_processing: Start verwerking met {len(files)} bestanden")
        # Start verwerking met instellingen
        self.processing_panel.start_processing_with_settings(files, settings)
    
    def stop_processing(self):
        """Stop verwerking via menu"""
        print("🛑 MainWindow: stop_processing aangeroepen")
        try:
            if hasattr(self, 'processing_panel'):
                print("🛑 MainWindow: Roep processing_panel.stop_processing() aan...")
                self.processing_panel.stop_processing()
            else:
                print("⚠️ MainWindow: processing_panel bestaat niet")
            
            # Reset processing_active flag
            self.processing_active = False
            print("✅ MainWindow: Stop verwerking voltooid")
        except Exception as e:
            print(f"❌ Fout bij stoppen verwerking: {e}")
            # Probeer alsnog de UI te resetten
            self.processing_active = False 