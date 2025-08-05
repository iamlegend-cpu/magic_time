"""
Magic Time Studio - PyQt6 Hoofdapplicatie
Modulaire versie van de video ondertiteling applicatie met PyQt6
"""

import os
import sys
import warnings
import socket
import threading
from typing import Optional

# PyQt6 imports
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QIcon

# Onderdruk waarschuwingen
warnings.filterwarnings("ignore", message="Failed to launch Triton kernels")
warnings.filterwarnings("ignore", message="Failed to launch Triton kernels, likely due to missing CUDA toolkit")
warnings.filterwarnings("ignore", message=".*Triton.*")

# Import onze modules
from magic_time_studio.core.config import config_manager
from magic_time_studio.core.stop_manager import stop_manager
from magic_time_studio.models.processing_queue import processing_queue
from magic_time_studio.models.progress_tracker import progress_tracker
from magic_time_studio.models.performance_tracker import performance_tracker

# Import PyQt6 UI modules
from magic_time_studio.ui_pyqt6.main_window import MainWindow
from magic_time_studio.ui_pyqt6.themes import ThemeManager

# Import processing modules
from magic_time_studio.processing import whisper_processor, translator, audio_processor, video_processor

from magic_time_studio.app_core.magic_time_studio_pyqt6 import MagicTimeStudioPyQt6
from magic_time_studio.app_core.processing_thread import ProcessingThread
from magic_time_studio.app_core.single_instance import acquire_single_instance_lock, release_single_instance_lock
from magic_time_studio.app_core.main_entry import main

if __name__ == "__main__":
    import sys
    sys.exit(main()) 