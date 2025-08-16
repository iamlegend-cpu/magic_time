"""
Eenvoudige interface voor Magic Time Studio
Vereenvoudigde versie zonder VLC en Whisper evaluatie
"""

import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QGroupBox, QPushButton, QTextEdit
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QDragLeaveEvent


class SubtitlePreviewWidget(QWidget):
    """Eenvoudige interface zonder VLC en Whisper evaluatie"""
    
    # Signals
    files_dropped = Signal(list)  # Gedropte bestanden
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setup_ui()
        self.setup_drag_drop()
    
    def setup_ui(self):
        """Setup de eenvoudige UI"""
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("🎬 Magic Time Studio Interface")
        header.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #ffffff;
                background-color: #2d2d2d;
                padding: 10px;
                border-radius: 5px;
                margin: 5px;
            }
        """)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Info sectie
        info_group = QGroupBox("ℹ️ Informatie")
        info_layout = QVBoxLayout(info_group)
        
        info_text = QLabel("""
        Welkom bij Magic Time Studio!
        
        Deze interface is vereenvoudigd en bevat geen:
        • VLC video player functionaliteit
        • Whisper model evaluatie
        • Complexe subtitle preview
        
        Gebruik deze interface voor eenvoudige taken.
        """)
        info_text.setStyleSheet("""
            QLabel {
                color: #cccccc;
                font-size: 12px;
                line-height: 1.4;
                padding: 10px;
            }
        """)
        info_layout.addWidget(info_text)
        
        layout.addWidget(info_group)
        
        # Status sectie
        status_group = QGroupBox("📊 Status")
        status_layout = QVBoxLayout(status_group)
        
        self.status_text = QTextEdit()
        self.status_text.setPlaceholderText("Status informatie verschijnt hier...")
        self.status_text.setMaximumHeight(150)
        self.status_text.setReadOnly(True)
        status_layout.addWidget(self.status_text)
        
        layout.addWidget(status_group)
        
        # Voeg stretch toe
        layout.addStretch()
    

    
    def update_status(self, message: str):
        """Update status bericht"""
        if hasattr(self, 'status_text'):
            self.status_text.append(f"[{self.get_current_time()}] {message}")
    
    def get_current_time(self):
        """Get huidige tijd string"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
    

    
    def setup_drag_drop(self):
        """Setup drag & drop functionaliteit"""
        self.setAcceptDrops(True)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            # Visuele feedback
            self.setStyleSheet("""
                QWidget {
                    border: 2px dashed #4caf50;
                    background-color: rgba(76, 175, 80, 0.1);
                }
            """)
    
    def dropEvent(self, event: QDropEvent):
        """Handle drop event"""
        files = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if os.path.exists(file_path):
                files.append(file_path)
        
        # Reset styling
        self.setStyleSheet("")
        
        if files:
            # Emit signal voor gedropte bestanden
            self.files_dropped.emit(files)
            
            # Update status
            self.update_status(f"Bestanden gedropt: {len(files)} bestanden")
            for file_path in files:
                self.update_status(f"  - {os.path.basename(file_path)}")
    
    def dragLeaveEvent(self, event: QDragLeaveEvent):
        """Handle drag leave event"""
        # Reset styling
        self.setStyleSheet("") 