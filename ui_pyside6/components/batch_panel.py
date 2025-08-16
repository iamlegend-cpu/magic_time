"""
Batch Panel component voor Magic Time Studio
Handelt batch verwerking af
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox
)
from PySide6.QtCore import Qt

from ..features.batch_queue import BatchQueueManager

class BatchPanel(QWidget):
    """Batch verwerking paneel"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup de UI"""
        layout = QVBoxLayout(self)
        
        batch_group = QGroupBox("🔄 Batch Verwerking")
        batch_layout = QVBoxLayout(batch_group)
        
        # Batch queue manager
        self.batch_queue = BatchQueueManager()
        batch_layout.addWidget(self.batch_queue)
        
        layout.addWidget(batch_group) 