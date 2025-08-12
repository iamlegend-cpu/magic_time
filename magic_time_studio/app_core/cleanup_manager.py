"""
Cleanup Manager voor Magic Time Studio PyQt6
Beheert alle cleanup en afsluit functionaliteit
"""

import os
import tempfile

class CleanupManager:
    """Beheert alle cleanup en afsluit functionaliteit"""
    
    def __init__(self, main_app):
        self.main_app = main_app
        
    def cleanup_on_exit(self):
        """Voer cleanup uit bij afsluiten"""
        # Stop verwerking als actief via StopManager
        self._stop_processing_on_exit()
        
        # Release single instance lock
        self._release_single_instance_lock()
        
        # Ruim oude lock files op
        self._cleanup_old_lock_files()
        
        # Sluit applicatie
        if self.main_app.ui_manager.app:
            self.main_app.ui_manager.app.quit()
    
    def _stop_processing_on_exit(self):
        """Stop verwerking bij afsluiten"""
        if (self.main_app.processing_manager.processing_thread and 
            hasattr(self.main_app.processing_manager.processing_thread, 'isRunning') and 
            self.main_app.processing_manager.processing_thread.isRunning()):
            print("🛑 Stop verwerking bij afsluiten...")
            if self.main_app.stop_manager:
                try:
                    self.main_app.stop_manager.stop_all_processes()
                    print("✅ Verwerking gestopt bij afsluiten")
                except Exception as e:
                    print(f"⚠️ Fout bij stoppen verwerking bij afsluiten: {e}")
            else:
                print("⚠️ StopManager niet geïnitialiseerd, geen verwerking gestopt bij afsluiten")
    
    def _release_single_instance_lock(self):
        """Release single instance lock"""
        if hasattr(self.main_app, 'lock_file') and self.main_app.release_single_instance_lock:
            try:
                self.main_app.release_single_instance_lock(self.main_app.lock_file)
                print("✅ Single instance lock vrijgegeven")
            except Exception as e:
                print(f"⚠️ Fout bij vrijgeven single instance lock: {e}")
    
    def _cleanup_old_lock_files(self):
        """Ruim oude lock files op"""
        try:
            old_lock_file = os.path.join(tempfile.gettempdir(), "magic_time_studio.lock")
            if os.path.exists(old_lock_file):
                os.remove(old_lock_file)
                print(f"🗑️ Oude lock file verwijderd: {old_lock_file}")
        except Exception as e:
            print(f"⚠️ Kon oude lock file niet verwijderen: {e}")
