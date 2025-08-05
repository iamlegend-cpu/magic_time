"""
File Handlers Mixin voor MainWindow
Bevat alle file gerelateerde functies
"""

from typing import List
import os

class FileHandlersMixin:
    """Mixin voor file handler functionaliteit"""
    
    # on_files_dropped methode verwijderd - files_panel heeft eigen handler
    
    def on_file_selected(self, file_path: str):
        """Handle bestand selectie"""
        self.file_selected.emit(file_path) 