"""
Processing Controller component voor Magic Time Studio
Bevat alle processing control logica
"""

from typing import List, Dict
from PySide6.QtCore import QObject, QTimer
import os
import time

class ProcessingController(QObject):
    """Beheert alle processing control operaties"""
    
    def __init__(self, ui_component, file_manager, processing_core, progress_tracker, gpu_manager, cleanup_manager):
        super().__init__()
        self.ui = ui_component
        self.file_manager = file_manager
        self.processing_core = processing_core
        self.progress_tracker = progress_tracker
        self.gpu_manager = gpu_manager
        self.cleanup_manager = cleanup_manager
        
        # UI status
        self.ui.is_processing = False
        
        # Progress tracking
        self._last_progress = 0.0
        
        # Timer setup
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self._update_progress_display)
    
    def start_processing_direct(self):
        """Start verwerking direct"""
        if self.ui.is_processing:
            self._log_message("⚠️ Verwerking is al bezig")
            return
        
        # Zoek main window en haal bestanden op
        main_window = self.file_manager.find_main_window(self.ui)
        if not main_window:
            self._log_message("❌ Kan geen main window vinden")
            return
        
        files = self.file_manager.get_files_from_main_window(main_window)
        if not files:
            self._log_message("❌ Geen bestanden gevonden")
            self._log_message("💡 Voeg eerst bestanden toe via 'Bestand' of 'Map' knoppen")
            return
        
        if files:
            self._log_message(f"📁 {len(files)} bestanden gevonden in files panel")
        
        # Haal instellingen op
        settings = self.file_manager.get_settings_from_main_window(main_window)
        print(f"🔧 [DEBUG] ProcessingPanel: Instellingen opgehaald uit main window: {settings}")
        
        # Start verwerking
        self._start_processing(files, settings)
    
    def start_processing_with_settings(self, files: List[str], settings: Dict):
        """Start verwerking met specifieke instellingen"""
        if self.ui.is_processing:
            self._log_message("⚠️ Verwerking is al bezig")
            return
        
        print(f"🚀 ProcessingPanel: Start verwerking met {len(files)} bestanden")
        print(f"🔧 [DEBUG] ProcessingPanel: Ontvangen instellingen: {settings}")
        
        # Start verwerking
        self._start_processing(files, settings)
    
    def _start_processing(self, files: List[str], settings: Dict):
        """Start de verwerking"""
        print(f"🔧 [DEBUG] ProcessingPanel: Start verwerking met instellingen: {settings}")
        
        # Start progress tracking
        if self.progress_tracker:
            self.progress_tracker.start_tracking(len(files))
            print(f"🔧 [DEBUG] ProgressTracker gestart voor {len(files)} bestanden")
            self.progress_timer.start(5000)  # Update elke 5 seconden in plaats van elke seconde
        
        # Stel bestanden in voor progress handler
        if hasattr(self.ui, 'progress_handler'):
            self.ui.progress_handler.set_processing_files(files)
            print(f"🔧 [DEBUG] ProgressHandler ingesteld voor {len(files)} bestanden")
        
        # Reset progress tracking
        self._last_progress = 0.0
        
        # Update UI status
        self.ui.is_processing = True
        self.ui.start_btn.setEnabled(False)
        self.ui.progress_bar.setValue(0)
        self.ui.status_label.setText(f"Verwerking gestart voor {len(files)} bestanden...")
        
        # Start verwerking via core
        success = self.processing_core.start_processing(files, settings)
        
        if not success:
            # Verwerking kon niet starten (bijv. al bezig)
            self._log_message("⚠️ Verwerking kon niet starten - al bezig")
            self._complete_processing()
            return
        
        # Verbind progress updates van de processing core
        if hasattr(self.processing_core, 'processing_thread') and self.processing_core.processing_thread:
            self.processing_core.processing_thread.progress_updated.connect(self._on_progress_updated)
            self.processing_core.processing_thread.status_updated.connect(self._on_status_updated)
            print(f"🔧 [DEBUG] Progress signals verbonden aan processing thread")
        
        # Forceer GPU Monitor naar groen (WhisperX actief)
        self.gpu_manager.force_gpu_monitor_green()
        
        # Emit signal
        if hasattr(self.ui, 'processing_started'):
            self.ui.processing_started.emit(files, settings)
    
    def _update_progress_display(self):
        """Update de progress display real-time"""
        try:
            if self.progress_tracker and self.ui.is_processing:
                # Update ETA minder frequent (elke 5 seconden in plaats van elke seconde)
                current_time = time.time()
                if not hasattr(self, '_last_eta_update'):
                    self._last_eta_update = 0
                
                if current_time - self._last_eta_update >= 5.0:  # Update elke 5 seconden
                    # Gebruik ETA voor huidige bestand en resterende bestanden
                    current_file_eta = self.progress_tracker.get_eta_for_current_file()
                    remaining_files_eta = self.progress_tracker.get_eta_for_remaining_files()
                    elapsed_str = self.progress_tracker.get_elapsed_time()
                    
                    # Update timing label
                    if current_file_eta and current_file_eta != "--:--":
                        if remaining_files_eta and remaining_files_eta != "--:--":
                            self.ui.timing_label.setText(f"⏱️ Huidig: {current_file_eta} | Totaal: {remaining_files_eta} | Verstreken: {elapsed_str}")
                        else:
                            self.ui.timing_label.setText(f"⏱️ Huidig: {current_file_eta} | Verstreken: {elapsed_str}")
                    else:
                        self.ui.timing_label.setText(f"⏱️ ETA: --:-- | Verstreken: {elapsed_str}")
                    
                    self._last_eta_update = current_time
                
        except Exception as e:
            print(f"⚠️ [DEBUG] Fout in progress display update: {e}")
            self.ui.timing_label.setText("⏱️ ETA: --:-- | Verstreken: --:--")
    
    def _on_progress_updated(self, progress: float, message: str):
        """Handle progress updates van de processing thread"""
        # Geef door aan ProgressHandler
        if hasattr(self.ui, 'progress_handler'):
            # Controleer of dit een nieuw bestand is (progress reset naar 0%)
            if progress <= 5.0 and hasattr(self, '_last_progress') and self._last_progress > 50.0:
                print(f"🔧 [DEBUG] Nieuw bestand gedetecteerd - progress reset van {self._last_progress:.1f}% naar {progress:.1f}%")
                # Reset progress bar voor nieuw bestand
                self.ui.progress_bar.setValue(0)
                
                # Start nieuw bestand in progress tracker
                if hasattr(self.ui, 'progress_handler') and hasattr(self.ui.progress_handler, 'current_file_index'):
                    current_file_index = self.ui.progress_handler.current_file_index
                    if hasattr(self.ui.progress_handler, 'processing_files') and current_file_index < len(self.ui.progress_handler.processing_files):
                        filename = os.path.basename(self.ui.progress_handler.processing_files[current_file_index])
                        if hasattr(self.ui, 'progress_tracker'):
                            self.ui.progress_tracker.start_file(current_file_index, filename)
            
            # Update last progress
            self._last_progress = progress
            
            self.ui.progress_handler.handle_progress_update(progress, message)
        else:
            print(f"⚠️ [DEBUG] Geen progress_handler gevonden in UI")
    
    def _on_status_updated(self, status: str):
        """Handle status updates van de processing thread"""
        # Geef door aan ProgressHandler
        if hasattr(self.ui, 'progress_handler'):
            self.ui.progress_handler.handle_status_update(status)
        else:
            print(f"⚠️ [DEBUG] Geen progress_handler gevonden in UI")
    
    def _complete_processing(self):
        """Markeer verwerking als voltooid"""
        self.ui.is_processing = False
        self.ui.start_btn.setEnabled(True)
        self.ui.progress_bar.setValue(100)
        self.ui.status_label.setText("✅ Verwerking voltooid")
        self.ui.timing_label.setText("⏱️ Voltooid!")
        
        # Stop timer
        self.progress_timer.stop()
        
        if self.progress_tracker:
            self.progress_tracker.reset()
        
        # Roep cleanup aan
        if self.cleanup_manager:
            self.cleanup_manager.complete_processing_cleanup()
        
        print(f"🔧 [DEBUG] ProcessingPanel: Verwerking voltooid, status gereset")
        
        # Reset GPU Monitor naar rood (verwerking gestopt)
        self.gpu_manager.update_gpu_monitor_status(False)
    
    def _log_message(self, message: str):
        """Voeg een bericht toe aan de log"""
        try:
            from datetime import datetime
            timestamp = datetime.now().strftime("%H:%M:%S")
            formatted_message = f"[{timestamp}] {message}"
            self.ui.log_text.append(formatted_message)
            
            # Auto-scroll naar beneden
            scrollbar = self.ui.log_text.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
        except Exception:
            pass
