"""
Drag & Drop functionaliteit voor Magic Time Studio
"""

import os
from typing import List
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QDragLeaveEvent


class DragDropHandler:
    """Handler voor drag & drop functionaliteit"""
    
    def __init__(self, widget: QWidget):
        self.widget = widget
        self.setup_drag_drop()
    
    def setup_drag_drop(self):
        """Setup drag & drop voor widget"""
        self.widget.setAcceptDrops(True)
        self.widget.dragEnterEvent = self.drag_enter_event
        self.widget.dropEvent = self.drop_event
        self.widget.dragLeaveEvent = self.drag_leave_event
    
    def drag_enter_event(self, event: QDragEnterEvent):
        """Handle drag enter event"""
        if event.mimeData().hasUrls():
            # Controleer of er geldige bestanden zijn
            valid_files = []
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if is_valid_media_file(file_path):
                    valid_files.append(file_path)
            
            if valid_files:
                event.acceptProposedAction()
                # Visuele feedback
                self.widget.setStyleSheet("""
                    QWidget {
                        border: 2px dashed #4caf50;
                        background-color: rgba(76, 175, 80, 0.1);
                    }
                """)
    
    def drop_event(self, event: QDropEvent):
        """Handle drop event"""
        files = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if is_valid_media_file(file_path):
                files.append(file_path)
        
        # Reset styling
        self.widget.setStyleSheet("")
        
        if files:
            # Emit signal voor bestanden
            if hasattr(self.widget, 'files_dropped'):
                self.widget.files_dropped.emit(files)
    
    def drag_leave_event(self, event: QDragLeaveEvent):
        """Handle drag leave event"""
        # Reset styling
        self.widget.setStyleSheet("")

class DragDropZone(QLabel):
    """Speciale QLabel voor drag & drop"""
    
    # Signal voor gedropte bestanden
    files_dropped = pyqtSignal(list)  # List[str]
    
    def __init__(self, text: str = "Sleep bestanden hierheen"):
        super().__init__(text)
        self.processing_active = False  # Flag voor verwerking status
        self.setup_drag_drop()
        self.setup_styling()
    
    def setup_drag_drop(self):
        """Setup drag & drop"""
        self.handler = DragDropHandler(self)
        # Override de signal om onze eigen signal te gebruiken
        self.handler.widget = self
    
    def setup_styling(self):
        """Setup styling voor drag & drop zone"""
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumHeight(100)
        
        if self.processing_active:
            # Styling voor verwerking actief
            self.setStyleSheet("""
                QLabel {
                    border: 2px dashed #888888;
                    border-radius: 8px;
                    background-color: rgba(136, 136, 136, 0.1);
                    color: #888888;
                    font-size: 14px;
                    font-weight: bold;
                }
            """)
            self.setText("Verwerking actief - geen drag & drop mogelijk")
        else:
            # Normale styling
            self.setStyleSheet("""
                QLabel {
                    border: 2px dashed #555555;
                    border-radius: 8px;
                    background-color: rgba(255, 255, 255, 0.05);
                    color: #cccccc;
                    font-size: 14px;
                    font-weight: bold;
                }
                QLabel:hover {
                    border-color: #4caf50;
                    background-color: rgba(76, 175, 80, 0.1);
                }
            """)
            self.setText("Sleep bestanden hierheen")
    
    def set_processing_active(self, active: bool):
        """Stel processing active status in"""
        self.processing_active = active
        self.setup_styling()
    
    def drag_enter_event(self, event: QDragEnterEvent):
        """Handle drag enter event"""
        # Blokkeer drag & drop tijdens verwerking
        if self.processing_active:
            event.ignore()
            return
        
        if event.mimeData().hasUrls():
            # Controleer of er geldige bestanden zijn
            valid_files = []
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if is_valid_media_file(file_path):
                    valid_files.append(file_path)
            
            if valid_files:
                event.acceptProposedAction()
                # Visuele feedback
                self.setStyleSheet("""
                    QLabel {
                        border: 2px dashed #4caf50;
                        border-radius: 8px;
                        background-color: rgba(76, 175, 80, 0.2);
                        color: #4caf50;
                        font-size: 14px;
                        font-weight: bold;
                    }
                """)
    
    def drop_event(self, event: QDropEvent):
        """Handle drop event"""
        # Blokkeer drop tijdens verwerking
        if self.processing_active:
            event.ignore()
            return
        
        files = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if is_valid_media_file(file_path):
                files.append(file_path)
        
        # Reset styling
        self.setup_styling()
        
        if files:
            # Emit signal voor bestanden
            self.files_dropped.emit(files)
    
    def drag_leave_event(self, event: QDragLeaveEvent):
        """Handle drag leave event"""
        # Reset styling
        self.setup_styling()

def is_valid_media_file(file_path: str) -> bool:
    """Controleer of bestand een geldig media bestand is"""
    if not os.path.exists(file_path):
        return False
    
    # Ondersteunde bestandsextensies
    video_extensions = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'}
    audio_extensions = {'.mp3', '.wav', '.m4a', '.aac', '.flac', '.ogg', '.wma'}
    
    # Controleer extensie
    file_ext = os.path.splitext(file_path)[1].lower()
    return file_ext in video_extensions or file_ext in audio_extensions 