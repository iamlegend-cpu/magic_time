"""
Processing Panel UI component voor Magic Time Studio
Bevat alleen UI setup en styling
"""

import os
import sys
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QProgressBar, QGroupBox, QTextEdit
)
from PySide6.QtCore import Qt

from .progress_tracker import ProgressTracker, FallbackProgressTracker

class ProcessingPanelUI(QWidget):
    """UI component voor Processing Panel - alleen setup en styling"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # UI componenten
        self.status_label = None
        self.progress_bar = None

        self.timing_label = None
        self.start_btn = None
        self.log_text = None
        self.clear_log_btn = None
        self.copy_log_btn = None
        self.completed_list = None
        self.progress_tracker = None
        self.progress_handler = None  # Wordt ingesteld door ProcessingPanel
        
        self.setup_ui()
        self._init_progress_tracker()
    
    def setup_ui(self):
        """Setup de UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Verwerking groep
        processing_group = QGroupBox("⚙️ Verwerking")
        processing_layout = QVBoxLayout(processing_group)
        processing_layout.setSpacing(8)
        
        # Status label
        self.status_label = QLabel("Klaar voor verwerking")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #e2e8f0;
                font-size: 12px;
                padding: 8px;
                background-color: #2d3748;
                border-radius: 6px;
                border: 1px solid #4a5568;
            }
        """)
        processing_layout.addWidget(self.status_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #4a5568;
                border-radius: 8px;
                text-align: center;
                font-weight: bold;
                font-size: 12px;
                color: #ffffff;
                background: #1a202c;
                height: 25px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a90e2, stop:1 #63b3ed);
                border-radius: 6px;
                margin: 2px;
            }
        """)
        processing_layout.addWidget(self.progress_bar)
        
        # ETA en timing informatie
        self.timing_label = QLabel("⏱️ ETA: --:-- | Verstreken: --:--")
        self.timing_label.setStyleSheet("""
            QLabel {
                color: #a0aec0;
                font-size: 10px;
                padding: 4px;
                background-color: #1a202c;
                border-radius: 4px;
                border: 1px solid #2d3748;
            }
        """)
        processing_layout.addWidget(self.timing_label)
        
        # Start knop
        self.start_btn = QPushButton("▶️ Start Verwerking")
        self.start_btn.setProperty("class", "primary")
        processing_layout.addWidget(self.start_btn)
        
        # Log output
        log_group = QGroupBox("📋 Log Output")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(120)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #1a202c;
                color: #e2e8f0;
                border: 1px solid #4a5568;
                border-radius: 6px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 10px;
                padding: 8px;
            }
        """)
        log_layout.addWidget(self.log_text)
        
        # Log knoppen
        log_buttons_layout = QHBoxLayout()
        
        self.clear_log_btn = QPushButton("🗑️ Wissen")
        log_buttons_layout.addWidget(self.clear_log_btn)
        
        self.copy_log_btn = QPushButton("📋 Kopiëren")
        log_buttons_layout.addWidget(self.copy_log_btn)
        
        log_layout.addLayout(log_buttons_layout)
        
        # Completed files groep
        completed_group = QGroupBox("✅ Voltooide Bestanden")
        completed_layout = QVBoxLayout(completed_group)
        
        self.completed_list = QTextEdit()
        self.completed_list.setReadOnly(True)
        self.completed_list.setMinimumHeight(150)
        self.completed_list.setMaximumHeight(200)
        self.completed_list.setStyleSheet("""
            QTextEdit {
                background-color: #1a202c;
                color: #48bb78;
                border: 1px solid #4a5568;
                border-radius: 6px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
                padding: 10px;
            }
        """)
        completed_layout.addWidget(self.completed_list)
        
        # Voeg groepen toe aan layout
        layout.addWidget(log_group)
        layout.addWidget(processing_group)
        layout.addWidget(completed_group)
    
    def _init_progress_tracker(self):
        """Initialiseer de progress tracker"""
        try:
            # Voeg project root toe aan Python path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
            
            if project_root not in sys.path:
                sys.path.insert(0, project_root)
            
            # Probeer models.progress_tracker te importeren
            try:
                from models.progress_tracker import ProgressTracker
                self.progress_tracker = ProgressTracker(self.progress_bar, self.status_label)
            except ImportError:
                # Fallback naar lokale ProgressTracker
                self.progress_tracker = ProgressTracker(self.progress_bar, self.status_label)
        except Exception:
            # Gebruik fallback tracker
            self.progress_tracker = FallbackProgressTracker(self.progress_bar, self.status_label)
