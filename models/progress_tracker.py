"""
Progress tracking voor Magic Time Studio
Vereenvoudigde versie met betere ETA afhandeling per bestand
"""

import time
from typing import Dict, Optional

class ProgressTracker:
    """Beheert voortgang tracking voor video verwerking met verbeterde ETA per bestand"""
    
    def __init__(self, progress_bar: Optional[object] = None, status_label: Optional[object] = None):
        self.progress_bar = progress_bar
        self.status_label = status_label
        self.start_time = None
        self.total_files = 0
        self.current_file_index = 0
        self.current_file_start_time = None
        self.file_durations = {}  # Sla duur per bestand op
        
    def set_widgets(self, progress_bar: Optional[object] = None, status_label: Optional[object] = None) -> None:
        """Zet de widgets voor voortgang tracking"""
        if progress_bar is not None:
            self.progress_bar = progress_bar
        if status_label is not None:
            self.status_label = status_label
    
    def start_tracking(self, total_files: int) -> None:
        """Start het tracken van voortgang voor meerdere bestanden"""
        self.start_time = time.time()
        self.total_files = total_files
        self.current_file_index = 0
        self.current_file_start_time = time.time()
        
        if self.progress_bar:
            self.progress_bar.setValue(0)
        if self.status_label:
            self.status_label.setText(f"Verwerking gestart voor {total_files} bestanden...")
        
        print(f"🔧 [DEBUG] ProgressTracker: Gestart voor {total_files} bestanden")
    
    def start_file(self, file_index: int, filename: str) -> None:
        """Start verwerking van een nieuw bestand"""
        try:
            self.current_file_index = file_index
            self.current_file_start_time = time.time()
            
            if self.status_label:
                self.status_label.setText(f"🔄 Bestand {file_index + 1}/{self.total_files}: {filename}")
            
            if self.progress_bar:
                # Reset progress bar voor nieuw bestand
                self.progress_bar.setValue(0)
            
            print(f"🔄 Start bestand {file_index + 1}/{self.total_files}: {filename}")
            
        except Exception as e:
            print(f"⚠️ [DEBUG] Fout bij starten bestand: {e}")
    
    def update_file_progress(self, progress: float):
        """Update de voortgang van het huidige bestand"""
        try:
            if self.progress_bar:
                # Toon progress voor huidige bestand (0-100% per bestand)
                self.progress_bar.setValue(int(progress))
                
                # Update overall progress in status label (alleen bij belangrijke momenten)
                if self.total_files > 0 and progress % 25 == 0:  # Alleen bij 25%, 50%, 75%, 100%
                    if hasattr(self, 'status_label') and self.status_label:
                        self.status_label.setText(f"Bestand {self.current_file_index + 1}/{self.total_files}: {progress:.0f}%")
        except Exception as e:
            print(f"⚠️ Fout bij update_file_progress: {e}")
    
    def complete_file(self, filename: str) -> None:
        """Markeer een bestand als voltooid en bereken duur"""
        try:
            if self.current_file_start_time:
                duration = time.time() - self.current_file_start_time
                self.file_durations[filename] = duration
                print(f"✅ Bestand voltooid: {filename} (duur: {duration:.1f}s)")
            
            # Update overall progress
            if self.progress_bar and self.total_files > 0:
                overall_progress = int(((self.current_file_index + 1) / self.total_files) * 100)
                self.progress_bar.setValue(overall_progress)
                print(f"📊 Overall progress: {overall_progress}% ({self.current_file_index + 1}/{self.total_files})")
            
            if self.status_label:
                self.status_label.setText(f"✅ Bestand {self.current_file_index + 1}/{self.total_files} voltooid: {filename}")
                
        except Exception as e:
            print(f"⚠️ Fout bij voltooien bestand: {e}")
    
    def get_eta_for_current_file(self) -> str:
        """Bereken ETA voor het huidige bestand op basis van gemiddelde duur"""
        try:
            if not self.current_file_start_time or not self.file_durations:
                return "--:--"
            
            current_time = time.time()
            elapsed = current_time - self.current_file_start_time
            
            # Bereken gemiddelde duur per bestand
            avg_duration = sum(self.file_durations.values()) / len(self.file_durations)
            
            # Bereken resterende tijd voor huidige bestand
            remaining_time = max(0, avg_duration - elapsed)
            
            # Converteer naar MM:SS formaat
            minutes = int(remaining_time // 60)
            seconds = int(remaining_time % 60)
            return f"{minutes:02d}:{seconds:02d}"
            
        except Exception:
            return "--:--"
    
    def get_eta_for_remaining_files(self) -> str:
        """Bereken ETA voor alle resterende bestanden"""
        try:
            if not self.start_time or self.total_files == 0:
                return "--:--"
            
            if not self.file_durations:
                return "--:--"
            
            current_time = time.time()
            elapsed = current_time - self.start_time
            
            # Bereken gemiddelde duur per bestand
            avg_duration = sum(self.file_durations.values()) / len(self.file_durations)
            
            # Bereken resterende bestanden
            remaining_files = self.total_files - self.current_file_index - 1
            
            # Bereken resterende tijd voor huidige bestand
            current_file_remaining = 0
            if self.current_file_start_time:
                current_file_elapsed = current_time - self.current_file_start_time
                current_file_remaining = max(0, avg_duration - current_file_elapsed)
            
            # Totale resterende tijd
            total_remaining = current_file_remaining + (remaining_files * avg_duration)
            
            # Converteer naar MM:SS formaat
            minutes = int(total_remaining // 60)
            seconds = int(total_remaining % 60)
            return f"{minutes:02d}:{seconds:02d}"
            
        except Exception:
            return "--:--"
    
    def get_elapsed_time(self) -> str:
        """Haal verstreken tijd op in MM:SS formaat"""
        try:
            if not self.start_time:
                return "--:--"
            
            elapsed = time.time() - self.start_time
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            return f"{minutes:02d}:{seconds:02d}"
        except Exception:
            return "--:--"
    
    def reset(self) -> None:
        """Reset de progress tracker"""
        self.start_time = None
        self.total_files = 0
        self.current_file_index = 0
        self.current_file_start_time = None
        self.file_durations.clear()
        
        if self.progress_bar:
            self.progress_bar.setValue(0)
        if self.status_label:
            self.status_label.setText("Klaar voor verwerking")
    
    def reset_for_next_file(self) -> None:
        """Reset timing voor volgend bestand, behoud total_files en file_durations"""
        self.current_file_start_time = time.time()
        
        # Reset progress bar naar 0% voor nieuw bestand
        if self.progress_bar:
            self.progress_bar.setValue(0)
        
        print(f"🔄 ProgressTracker gereset voor volgend bestand - nieuwe current_file_start_time ingesteld")
    
    def complete(self) -> None:
        """Markeer alle bestanden als voltooid"""
        if self.progress_bar:
            self.progress_bar.setValue(100)
        if self.status_label:
            self.status_label.setText("Verwerking voltooid!")
