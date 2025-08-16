"""
Magic Time Studio - PySide6 Hoofdapplicatie
Modulaire versie van de video ondertiteling applicatie met PySide6
"""

import os
import sys
import warnings
import socket
import threading
from typing import Optional

# PySide6 imports
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import QThread, Signal, QTimer
from PySide6.QtGui import QIcon

# Onderdruk waarschuwingen
warnings.filterwarnings("ignore", message="Failed to launch Triton kernels")
warnings.filterwarnings("ignore", message="Failed to launch Triton kernels, likely due to missing CUDA toolkit")
warnings.filterwarnings("ignore", message=".*Triton.*")

# Import onze modules
from core.config import config_manager
from core.stop_manager import stop_manager
from models.processing_queue import processing_queue
from models.progress_tracker import progress_tracker
from models.performance_tracker import performance_tracker

# Import PySide6 UI modules
from ui_pyside6.main_window import MainWindow
from ui_pyside6.themes import ThemeManager

# Import processing modules
from core.all_functions import *

from app_core.magic_time_studio_pyside6 import MagicTimeStudioPySide6
from app_core.processing_thread_new import ProcessingThread
from app_core.single_instance import acquire_single_instance_lock, release_single_instance_lock
from app_core.main_entry import main

if __name__ == "__main__":
    import sys
    sys.exit(main())
