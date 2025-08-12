"""
File Handler voor Magic Time Studio PyQt6
Beheert alle bestand-gerelateerde functionaliteit
"""

class FileHandler:
    """Beheert alle bestand-gerelateerde functionaliteit"""
    
    def __init__(self, main_app):
        self.main_app = main_app
        
    def on_file_selected(self, file_path: str):
        """Callback voor geselecteerd bestand"""
        print(f"📁 Bestand geselecteerd: {file_path}")
        if self.main_app.ui_manager.main_window:
            try:
                # Update status
                self.main_app.ui_manager.main_window.update_status(f"📁 Bestand geselecteerd: {file_path}")
                print("✅ Status bijgewerkt")
            except Exception as e:
                print(f"⚠️ Fout bij bijwerken status: {e}")
        else:
            print("⚠️ main_window is None, geen status update mogelijk")
