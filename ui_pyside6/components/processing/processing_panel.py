"""
Processing Panel component voor Magic Time Studio
Modulaire versie die gebruik maakt van gescheiden componenten
"""

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal

from .processing_panel_modular import ProcessingPanel as ModularProcessingPanel

class ProcessingPanel(ModularProcessingPanel):
    """Verwerking paneel - modulaire versie (backward compatibility wrapper)"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
