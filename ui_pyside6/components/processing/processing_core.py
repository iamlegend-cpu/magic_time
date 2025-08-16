"""
Processing Core voor Magic Time Studio
Handelt de daadwerkelijke verwerking van bestanden af
"""

import os
from typing import List, Dict, Optional
from .file_manager import FileManager

# Import ProcessingThread
try:
    from app_core.processing_thread_new import ProcessingThread
except ImportError:
    # Fallback import
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    from app_core.processing_thread_new import ProcessingThread

class ProcessingCore:
    """Core verwerkingslogica"""
    
    def __init__(self, file_manager: FileManager, log_callback=None):
        self.file_manager = file_manager
        self.log_callback = log_callback
        self.is_processing = False
        self.files_to_process = []
    
    def start_processing(self, files: List[str], settings: Dict = None) -> bool:
        """Start verwerking van bestanden"""
        try:
            if not files:
                print("⚠️ [WAARSCHUWING] Geen bestanden om te verwerken")
                return False
            
            # Controleer of er al een verwerking bezig is
            if self.is_processing:
                print("⚠️ [WAARSCHUWING] Verwerking is al bezig, negeer start request")
                return False
            
            print(f"🚀 [START] Verwerking gestart voor {len(files)} bestand(en)")
            print(f"🔧 [DEBUG] ProcessingCore: Ontvangen instellingen: {settings}")
            
            # Markeer als bezig
            self.is_processing = True
            
            # Start verwerking in aparte thread
            self.processing_thread = ProcessingThread(files, self, settings)
            self.processing_thread.progress_updated.connect(self.update_progress)
            self.processing_thread.status_updated.connect(self.update_status)
            self.processing_thread.error_occurred.connect(self.handle_error)
            self.processing_thread.processing_completed.connect(self.handle_completion)
            self.processing_thread.processing_finished.connect(self.handle_completion)  # Connect alias
            
            print(f"🔧 [BEZIG] Processing thread gestart")
            self.processing_thread.start()
            
            # Start thread asynchroon zonder te wachten
            print(f"✅ [DEBUG] Processing thread gestart (asynchroon)")
            
            # GPU Monitor status wordt nu bijgewerkt door ProcessingPanel
            # self._update_gpu_monitor_status(True)
            
            return True
            
        except Exception as e:
            print(f"❌ [FOUT] Fout bij starten verwerking: {e}")
            self.is_processing = False
            return False
    
    def _log_message(self, message: str):
        """Log een bericht via callback"""
        if self.log_callback:
            self.log_callback(message)
    
    def update_progress(self, progress: float, message: str):
        """Update progress van verwerking"""
        if self.log_callback:
            self.log_callback(f"📊 Progress: {progress:.1f}% - {message}")
    
    def update_status(self, message: str):
        """Update status van verwerking"""
        if self.log_callback:
            self.log_callback(f"ℹ️ Status: {message}")
    
    def handle_error(self, error: str):
        """Handle fouten tijdens verwerking"""
        if self.log_callback:
            self.log_callback(f"❌ Fout: {error}")
        self.is_processing = False
        
        # GPU Monitor status wordt nu bijgewerkt door ProcessingPanel
        # self._update_gpu_monitor_status(False)
        
        print(f"🔧 [DEBUG] ProcessingCore: Fout opgetreden, status gereset")
    
    def handle_completion(self):
        """Handle voltooiing van verwerking"""
        if self.log_callback:
            self.log_callback("✅ Verwerking voltooid")
        self.is_processing = False
        
        # Cleanup thread veilig
        if hasattr(self, 'processing_thread') and self.processing_thread:
            try:
                self.processing_thread.cleanup()
                print(f"🔧 [DEBUG] ProcessingCore: Thread cleanup uitgevoerd")
            except Exception as e:
                print(f"⚠️ [WAARSCHUWING] Kon thread cleanup niet uitvoeren: {e}")
        
        # GPU Monitor status wordt nu bijgewerkt door ProcessingPanel
        # self._update_gpu_monitor_status(False)
        
        print(f"🔧 [DEBUG] ProcessingCore: Verwerking voltooid, status gereset")
    
    def add_completed_file(self, file_path: str, output_path: str = None):
        """Voeg een voltooid bestand toe"""
        if hasattr(self, 'log_callback') and self.log_callback:
            try:
                # Zoek naar ProcessingPanel om completed file toe te voegen
                if hasattr(self, 'parent') and self.parent:
                    if hasattr(self.parent, 'add_completed_file'):
                        self.parent.add_completed_file(file_path, output_path)
                        print(f"🔧 [DEBUG] Completed file toegevoegd: {file_path}")
                    else:
                        print(f"⚠️ [DEBUG] ProcessingPanel heeft geen add_completed_file methode")
            except Exception as e:
                print(f"⚠️ [WAARSCHUWING] Fout bij toevoegen completed file: {e}")
    
    def get_processing_status(self) -> bool:
        """Haal verwerkingsstatus op"""
        return self.is_processing
    
    def get_files_to_process(self) -> List[str]:
        """Haal lijst met te verwerken bestanden op"""
        return self.files_to_process.copy()
    
    def _update_gpu_monitor_status(self, is_active: bool):
        """Update GPU Monitor status"""
        try:
            # Zoek naar GPU Monitor via file_manager
            if hasattr(self.file_manager, 'find_main_window'):
                main_window = self.file_manager.find_main_window(None)
                if main_window and hasattr(main_window, 'charts_panel'):
                    charts_panel = main_window.charts_panel
                    if hasattr(charts_panel, 'gpu_monitor'):
                        charts_panel.gpu_monitor.set_processing_status(is_active, is_active)
                        print(f"🔧 [DEBUG] GPU Monitor status bijgewerkt: {is_active}")
        except Exception as e:
            print(f"⚠️ [WAARSCHUWING] Kon GPU Monitor status niet bijwerken: {e}")
