"""
Processing components voor Magic Time Studio
Modulaire structuur voor verwerking functionaliteit
"""

from .processing_core import ProcessingCore
from .progress_tracker import ProgressTracker
from .file_manager import FileManager
from .processing_panel import ProcessingPanel

__all__ = [
    'ProcessingCore',
    'ProgressTracker', 
    'FileManager',
    'ProcessingPanel'
]
