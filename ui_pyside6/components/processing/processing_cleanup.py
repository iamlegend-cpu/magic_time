"""
Processing Cleanup component voor Magic Time Studio
Bevat alle cleanup en reset logica
"""

from PySide6.QtCore import QObject

class ProcessingCleanup(QObject):
    """Beheert alle cleanup en reset operaties"""
    
    def __init__(self, ui_component, progress_tracker, gpu_manager):
        super().__init__()
        self.ui = ui_component
        self.progress_tracker = progress_tracker
        self.gpu_manager = gpu_manager
    
    def complete_processing_cleanup(self):
        """Complete cleanup na verwerking"""
        try:
            print(f"🧹 [CLEANUP] Start complete cleanup")
            
            # Reset UI status
            self.ui.is_processing = False
            self.ui.start_btn.setEnabled(True)
            self.ui.status_label.setText("✅ Verwerking voltooid")
            self.ui.timing_label.setText("⏱️ Voltooid!")
            
            # Stop progress timer
            if hasattr(self.ui, 'progress_timer'):
                self.ui.progress_timer.stop()
            
            # Reset progress tracker
            if self.progress_tracker:
                self.progress_tracker.reset()
            
            # Reset GPU Monitor naar rood
            self.gpu_manager.update_gpu_monitor_status(False)
            
            print(f"🧹 [CLEANUP] Complete cleanup voltooid")
            
        except Exception as e:
            print(f"⚠️ [WAARSCHUWING] Fout tijdens complete cleanup: {e}")
    
    def complete_processing(self):
        """Markeer verwerking als voltooid"""
        try:
            self.ui.is_processing = False
            self.ui.start_btn.setEnabled(True)
            self.ui.progress_bar.setValue(100)
            self.ui.status_label.setText("✅ Verwerking voltooid")
            self.ui.timing_label.setText("⏱️ Voltooid!")
            
            # Stop timer
            if hasattr(self.ui, 'progress_timer'):
                self.ui.progress_timer.stop()
            
            if self.progress_tracker:
                self.progress_tracker.reset()
            
            print(f"🔧 [DEBUG] ProcessingPanel: Verwerking voltooid, status gereset")
            
            # Reset GPU Monitor naar rood (verwerking gestopt)
            self.gpu_manager.update_gpu_monitor_status(False)
            
        except Exception as e:
            print(f"⚠️ [DEBUG] Fout bij complete processing: {e}")
    
    def reset_panel(self, file_manager):
        """Reset het paneel naar begin staat"""
        try:
            self.ui.is_processing = False
            self.ui.start_btn.setEnabled(True)
            self.ui.progress_bar.setValue(0)
            self.ui.timing_label.setText("⏱️ ETA: --:-- | Verstreken: --:--")
            self.ui.status_label.setText("Klaar voor verwerking")
            
            file_manager.clear_completed_files()
            if hasattr(self.ui, 'completed_list'):
                self.ui.completed_list.clear()
            
            if self.progress_tracker:
                self.progress_tracker.reset()
            
            if hasattr(self.ui, 'progress_timer'):
                self.ui.progress_timer.stop()
                
        except Exception as e:
            print(f"⚠️ [DEBUG] Fout bij reset panel: {e}")
