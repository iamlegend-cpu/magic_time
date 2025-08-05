"""
Progress tracking voor Magic Time Studio
"""

import time
from datetime import timedelta
from typing import Optional
from magic_time_studio.core.utils import safe_config
from magic_time_studio.core.logging import logger

class ProgressTracker:
    """Beheert voortgang tracking voor video verwerking"""
    
    def __init__(self, progress_bar: Optional[object] = None, status_label: Optional[object] = None):
        self.progress_bar = progress_bar
        self.status_label = status_label
        self.start_time = None
        self.total_blocks = 0
        self.completed_blocks = 0
        self.failed_blocks = 0
        
    def set_widgets(self, progress_bar: Optional[object] = None, status_label: Optional[object] = None) -> None:
        """Zet de widgets voor voortgang tracking"""
        if progress_bar is not None:
            self.progress_bar = progress_bar
        if status_label is not None:
            self.status_label = status_label
    
    def start_tracking(self, total_blocks: int) -> None:
        """Start het tracken van voortgang"""
        self.start_time = time.time()
        self.total_blocks = total_blocks
        self.completed_blocks = 0
        self.failed_blocks = 0
        self.update_progress(0)
        logger.log_debug(f"📊 Progress tracking gestart voor {total_blocks} blokken")
        
    def update_progress(self, completed_blocks: int, failed_blocks: int = 0) -> None:
        """Update de voortgangsbalk met percentage en timer"""
        self.completed_blocks = completed_blocks
        self.failed_blocks = failed_blocks
        
        if self.total_blocks > 0 and self.start_time is not None:
            percentage = (completed_blocks / self.total_blocks) * 100
            
            # Update progress bar (PyQt6 QProgressBar)
            if self.progress_bar is not None:
                if hasattr(self.progress_bar, "setValue"):
                    self.progress_bar.setValue(int(percentage))
                elif hasattr(self.progress_bar, "setRange"):
                    self.progress_bar.setRange(0, 100)
                    self.progress_bar.setValue(int(percentage))
            
            # Bereken tijd
            elapsed_time = time.time() - self.start_time
            elapsed_str = str(timedelta(seconds=int(elapsed_time)))
            
            if completed_blocks > 0:
                avg_time_per_block = elapsed_time / completed_blocks
                remaining_blocks = self.total_blocks - completed_blocks
                eta_seconds = avg_time_per_block * remaining_blocks
                eta_str = str(timedelta(seconds=int(eta_seconds)))
                status_text = (
                    f"Voortgang: {percentage:.1f}% | Blok {completed_blocks}/{self.total_blocks} | "
                    f"Verstreken: {elapsed_str} | ETA: {eta_str}"
                )
            else:
                status_text = f"Voortgang: {percentage:.1f}% | Blok {completed_blocks}/{self.total_blocks} | Verstreken: {elapsed_str}"
            
            # Update status label (PyQt6 QLabel)
            if self.status_label is not None:
                if hasattr(self.status_label, "setText"):
                    self.status_label.setText(status_text)
                else:
                    safe_config(self.status_label, text=status_text)
    
    def complete(self) -> None:
        """Markeer als voltooid"""
        if self.start_time is not None:
            total_time = time.time() - self.start_time
            total_time_str = str(timedelta(seconds=int(total_time)))
            status_text = f"✅ Voltooid! Totale tijd: {total_time_str}"
        else:
            status_text = "✅ Voltooid!"
        
        if self.status_label is not None:
            if hasattr(self.status_label, "setText"):
                self.status_label.setText(status_text)
            else:
                safe_config(self.status_label, text=status_text)
        
        logger.log_debug("✅ Progress tracking voltooid")
    
    def reset(self) -> None:
        """Reset de progress tracker"""
        self.start_time = None
        self.total_blocks = 0
        self.completed_blocks = 0
        self.failed_blocks = 0
        
        if self.progress_bar is not None:
            if hasattr(self.progress_bar, "setValue"):
                self.progress_bar.setValue(0)
            else:
                safe_config(self.progress_bar, value=0)
        
        if self.status_label is not None:
            if hasattr(self.status_label, "setText"):
                self.status_label.setText("Klaar voor verwerking")
            else:
                safe_config(self.status_label, text="Klaar voor verwerking")
    
    def get_progress_percentage(self) -> float:
        """Krijg het voortgangspercentage"""
        if self.total_blocks > 0:
            return (self.completed_blocks / self.total_blocks) * 100
        return 0.0
    
    def get_elapsed_time(self) -> float:
        """Krijg de verstreken tijd in seconden"""
        if self.start_time is not None:
            return time.time() - self.start_time
        return 0.0
    
    def get_estimated_remaining_time(self) -> float:
        """Krijg de geschatte resterende tijd in seconden"""
        if self.completed_blocks > 0 and self.start_time is not None:
            elapsed_time = time.time() - self.start_time
            avg_time_per_block = elapsed_time / self.completed_blocks
            remaining_blocks = self.total_blocks - self.completed_blocks
            return avg_time_per_block * remaining_blocks
        return 0.0

# Globale progress tracker instantie
progress_tracker = ProgressTracker() 