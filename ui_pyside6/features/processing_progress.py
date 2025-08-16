"""
Verwerkingsvoortgang chart voor Magic Time Studio
Toon voortgang van bestandsverwerking en integreer met subtitle preview
"""

import time
from datetime import timedelta
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Signal
from .subtitle_preview import SubtitlePreviewWidget


class ProcessingProgressChart(QWidget):
    """Grafiek voor verwerkingsvoortgang"""
    
    progress_updated = Signal(float)  # Signal voor voortgang updates
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.processing_start_time = None
        self.files_processed = 0
        self.total_files = 0
    
    def setup_ui(self):
        """Setup de UI"""
        layout = QVBoxLayout(self)
        
        # Titel
        title = QLabel("🎬 Verwerking & Whisper Model Evaluatie")
        title.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff;")
        layout.addWidget(title)
        
        # Alleen preview widget - meer ruimte voor video player
        self.preview_widget = SubtitlePreviewWidget()
        layout.addWidget(self.preview_widget)
    
    def start_processing(self, total_files: int):
        """Start verwerking tracking"""
        self.processing_start_time = time.time()
        self.total_files = total_files
        self.files_processed = 0
        # Progress bar is verwijderd, gebruik alleen labels
        self.preview_widget.files_label.setText(f"Files: 0/{total_files}")
        self.preview_widget.current_file_label.setText("Huidig: -")
        self.preview_widget.eta_label.setText("ETA: -")
        self.preview_widget.elapsed_label.setText("Tijd: 00:00")
    
    def update_progress(self, progress: float, current_file: str = "", eta: str = ""):
        """Update voortgang"""
        # Progress bar is verwijderd, gebruik alleen signal
        self.progress_updated.emit(progress)
        
        if current_file:
            self.preview_widget.current_file_label.setText(f"Huidig: {current_file}")
        
        if eta:
            self.preview_widget.eta_label.setText(f"ETA: {eta}")
        
        # Update verstreken tijd
        if self.processing_start_time:
            elapsed = time.time() - self.processing_start_time
            elapsed_str = str(timedelta(seconds=int(elapsed)))
            # Kortere tijd format
            if ":" in elapsed_str:
                parts = elapsed_str.split(":")
                if len(parts) >= 3:
                    self.preview_widget.elapsed_label.setText(f"Tijd: {parts[1]}:{parts[2]}")
                else:
                    self.preview_widget.elapsed_label.setText(f"Tijd: {elapsed_str}")
            else:
                self.preview_widget.elapsed_label.setText(f"Tijd: {elapsed_str}")
    
    def file_completed(self):
        """Bestand voltooid"""
        self.files_processed += 1
        self.preview_widget.files_label.setText(f"Files: {self.files_processed}/{self.total_files}")
        
        # Bereken ETA
        if self.files_processed > 0 and self.processing_start_time:
            elapsed = time.time() - self.processing_start_time
            avg_time_per_file = elapsed / self.files_processed
            remaining_files = self.total_files - self.files_processed
            eta_seconds = remaining_files * avg_time_per_file
            eta_str = str(timedelta(seconds=int(eta_seconds)))
            self.preview_widget.eta_label.setText(f"ETA: {eta_str}")
    
    def reset_progress(self):
        """Reset voortgang"""
        # Progress bar is verwijderd, reset alleen labels
        self.preview_widget.current_file_label.setText("Huidig: -")
        self.preview_widget.files_label.setText("Files: 0/0")
        self.preview_widget.eta_label.setText("ETA: -")
        self.preview_widget.elapsed_label.setText("Tijd: 00:00")
        self.preview_widget.update() 