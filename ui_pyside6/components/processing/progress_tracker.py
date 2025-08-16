"""
Progress Tracker voor Magic Time Studio
Handelt ETA en progress berekening af
"""

import time
from PySide6.QtWidgets import QProgressBar, QLabel

class ProgressTracker:
    """Progress tracker voor verwerking"""
    
    def __init__(self, progress_bar: QProgressBar, status_label: QLabel):
        self.progress_bar = progress_bar
        self.status_label = status_label
        self.start_time = None
        self.total_steps = 0
        self.current_step = 0
    
    def start_tracking(self, total_steps: int):
        """Start progress tracking"""
        self.start_time = time.time()
        self.total_steps = total_steps
        self.current_step = 0
        
        if self.progress_bar:
            self.progress_bar.setValue(0)
        if self.status_label:
            self.status_label.setText("Verwerking gestart...")
    
    def update_step(self, step: int):
        """Update huidige stap"""
        self.current_step = step
        if self.progress_bar and self.total_steps > 0:
            progress = int((step / self.total_steps) * 100)
            self.progress_bar.setValue(progress)
            # print(f"🔧 [DEBUG] ProgressTracker: Stap {step}/{self.total_steps} ({progress}%)")
    
    def update_progress(self, progress_percent: float):
        """Update progress op basis van percentage (0-100)"""
        if self.total_steps > 0:
            # Bereken huidige stap op basis van percentage
            self.current_step = max(1, int((progress_percent / 100) * self.total_steps))
            if self.progress_bar:
                self.progress_bar.setValue(int(progress_percent))
            print(f"🔧 [DEBUG] ProgressTracker: Progress {progress_percent:.1f}% -> Stap {self.current_step}/{self.total_steps}")
        else:
            # Directe progress update zonder stap berekening
            if self.progress_bar:
                self.progress_bar.setValue(int(progress_percent))
    
    def get_eta(self) -> str:
        """Bereken geschatte resterende tijd"""
        try:
            if not self.start_time or self.total_steps == 0:
                return "--:--"
            
            current_time = time.time()
            elapsed = current_time - self.start_time
            
            if self.current_step == 0:
                return "--:--"
            
            # Bereken gemiddelde tijd per stap
            avg_time_per_step = elapsed / self.current_step
            remaining_steps = self.total_steps - self.current_step
            remaining_time = remaining_steps * avg_time_per_step
            
            # Debug output (UITGESCHAKELD)
            # print(f"🔧 [DEBUG] ETA: elapsed={elapsed:.1f}s, step={self.current_step}/{self.total_steps}, avg={avg_time_per_step:.1f}s, remaining={remaining_time:.1f}s")
            
            # Format tijd
            if remaining_time >= 3600:  # Meer dan 1 uur
                hours = int(remaining_time // 3600)
                minutes = int((remaining_time % 3600) // 60)
                return f"{hours:02d}:{minutes:02d}:00"
            else:
                minutes = int(remaining_time // 60)
                seconds = int(remaining_time % 60)
                return f"{minutes:02d}:{seconds:02d}"
        except Exception as e:
            print(f"⚠️ [DEBUG] ETA berekening fout: {e}")
            return "--:--"
    
    def get_eta_improved(self) -> str:
        """Verbeterde ETA berekening met progress percentage"""
        try:
            if not self.start_time or self.total_steps == 0:
                return "--:--"
            
            current_time = time.time()
            elapsed = current_time - self.start_time
            
            if self.current_step == 0:
                return "--:--"
            
            # Bereken progress percentage
            progress_percent = (self.current_step / self.total_steps) * 100
            
            if progress_percent <= 0:
                return "--:--"
            
            # Bereken gemiddelde tijd per percentage punt
            time_per_percent = elapsed / progress_percent
            remaining_percent = 100 - progress_percent
            remaining_time = remaining_percent * time_per_percent
            
            # Debug output
            print(f"🔧 [DEBUG] Verbeterde ETA: progress={progress_percent:.1f}%, elapsed={elapsed:.1f}s, time_per_%={time_per_percent:.1f}s, remaining={remaining_time:.1f}s")
            
            # Format tijd
            if remaining_time >= 3600:  # Meer dan 1 uur
                hours = int(remaining_time // 3600)
                minutes = int((remaining_time % 3600) // 60)
                return f"{hours:02d}:{minutes:02d}:00"
            else:
                minutes = int(remaining_time // 60)
                seconds = int(remaining_time % 60)
                return f"{minutes:02d}:{seconds:02d}"
        except Exception as e:
            print(f"⚠️ [DEBUG] Verbeterde ETA berekening fout: {e}")
            return "--:--"
    
    def get_elapsed_time(self) -> str:
        """Bereken verstreken tijd"""
        try:
            if not self.start_time:
                return "--:--"
            
            elapsed = time.time() - self.start_time
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            return f"{minutes:02d}:{seconds:02d}"
        except:
            return "--:--"
    
    def reset(self):
        """Reset de tracker"""
        self.start_time = None
        self.total_steps = 0
        self.current_step = 0
        
        if self.progress_bar:
            self.progress_bar.setValue(0)
        if self.status_label:
            self.status_label.setText("Klaar voor verwerking")
    
    def reset_for_next_file(self):
        """Reset timing voor volgend bestand, behoud total_steps"""
        self.start_time = time.time()
        self.current_step = 0
        
        if self.progress_bar:
            self.progress_bar.setValue(0)
        if self.status_label:
            self.status_label.setText("Volgend bestand gestart...")
        
        print(f"🔧 [DEBUG] ProgressTracker gereset voor volgend bestand - nieuwe start_time ingesteld")


class FallbackProgressTracker(ProgressTracker):
    """Fallback progress tracker voor als de hoofd tracker niet beschikbaar is"""
    
    def __init__(self, progress_bar: QProgressBar, status_label: QLabel):
        super().__init__(progress_bar, status_label)
