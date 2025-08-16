"""
Main Window Parts Module
Bevat opgesplitste onderdelen van de MainWindow klasse
"""

from .main_window_core import MainWindow
from .window_setup import WindowSetupMixin
from .menu_handlers import MenuHandlersMixin
from .processing_handlers import ProcessingHandlersMixin
from .file_handlers import FileHandlersMixin
from .ui_updates import UIUpdatesMixin
from .window_state import WindowStateMixin

__all__ = [
    'MainWindow',
    'WindowSetupMixin',
    'MenuHandlersMixin', 
    'ProcessingHandlersMixin',
    'FileHandlersMixin',
    'UIUpdatesMixin',
    'WindowStateMixin'
] 