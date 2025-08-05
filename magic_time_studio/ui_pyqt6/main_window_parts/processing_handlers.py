"""
Processing Handlers Mixin voor MainWindow
Bevat alle processing gerelateerde functies
"""

from typing import List, Dict
from PyQt6.QtWidgets import QMessageBox, QApplication
from magic_time_studio.processing import whisper_processor, translator, audio_processor
import os

class ProcessingHandlersMixin:
    """Mixin voor processing handler functionaliteit"""
    
    def on_processing_started(self, files: List[str], settings: Dict):
        """Handle processing start"""
        print(f"🏠 MainWindow: on_processing_started aangeroepen met {len(files)} bestanden")
        self.processing_active = True
        self.processing_started.emit(files, settings)
        self.update_status("Verwerking gestart...")
    
    def on_processing_stopped(self):
        """Handle processing stop"""
        self.processing_active = False
        self.processing_stopped.emit()
        self.update_status("Verwerking gestopt")
    
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
        """Handle voltooid bestand - verwijder uit "nog te doen" lijst"""
        print(f"🔍 [DEBUG] MainWindow.on_file_completed aangeroepen: {file_path}")
        
        # Zoek het bestand in de files panel lijst
        file_list = self.files_panel.get_file_list()
        print(f"🔍 [DEBUG] Bestanden in lijst: {len(file_list)}")
        for i, f in enumerate(file_list):
            print(f"🔍 [DEBUG] Bestand {i+1}: {f}")
        
        if file_path in file_list:
            # Vind de index van het bestand
            index = file_list.index(file_path)
            print(f"🔍 [DEBUG] Bestand gevonden op index: {index}")
            
            # Verwijder uit de lijst widget
            if index < self.files_panel.file_list_widget.count():
                self.files_panel.file_list_widget.takeItem(index)
                print(f"🔍 [DEBUG] Bestand verwijderd uit lijst widget")
            
            # Verwijder uit de interne lijst
            if index < len(self.files_panel.file_list):
                self.files_panel.file_list.pop(index)
                print(f"🔍 [DEBUG] Bestand verwijderd uit interne lijst")
            
            print(f"🗑️ Bestand verwijderd uit 'nog te doen' lijst: {file_path}")
            self.update_status(f"✅ {file_path} voltooid en verwijderd uit lijst")
        else:
            print(f"🔍 [DEBUG] Bestand niet gevonden in lijst: {file_path}")
    
    def on_charts_processing_started(self, files: List[str], settings: Dict):
        """Handle processing start voor charts panel"""
        if hasattr(self, 'charts_panel'):
            self.charts_panel.start_processing(len(files))
    
    def on_charts_file_completed(self, file_path: str):
        """Handle file completed voor charts panel"""
        if hasattr(self, 'charts_panel'):
            self.charts_panel.file_completed()
    
    def on_charts_processing_stopped(self):
        """Handle processing stop voor charts panel"""
        if hasattr(self, 'charts_panel'):
            self.charts_panel.reset_progress()
    
    def update_progress(self, value: float, status: str = ""):
        """Update voortgangsbalk"""
        if hasattr(self, 'processing_panel'):
            self.processing_panel.update_progress(value, status)
            # Voeg ook toe aan console output voor real-time updates
            if status:
                self.processing_panel.add_console_output(status, value / 100.0)
    
    def processing_finished(self):
        """Verwerking voltooid"""
        self.processing_active = False
        if hasattr(self, 'processing_panel'):
            self.processing_panel.processing_finished()
        self.update_status("Verwerking voltooid!")
    
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
        self.processing_panel.stop_processing()
        self.processing_active = False 