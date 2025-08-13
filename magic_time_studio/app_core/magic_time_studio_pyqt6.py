"""
Magic Time Studio - PyQt6 Hoofdapplicatie
Modulaire versie met gescheiden managers voor betere organisatie
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIcon

# Import onze managers (deze zijn altijd beschikbaar)
from .ui_manager import UIManager
from .module_manager import ModuleManager
from .processing_manager import ProcessingManager
from .file_handler import FileHandler
from .cleanup_manager import CleanupManager
from .theme_manager import ThemeManager as AppThemeManager

# Veilige imports met fallbacks
try:
    from magic_time_studio.core.config import config_manager
except ImportError:
    print("⚠️ config_manager niet gevonden, maak fallback aan...")
    config_manager = None

try:
    from magic_time_studio.core.stop_manager import stop_manager
except ImportError:
    print("⚠️ stop_manager niet gevonden, maak fallback aan...")
    stop_manager = None

try:
    from magic_time_studio.ui_pyqt6.main_window import MainWindow
    print("✅ MainWindow succesvol geïmporteerd")
except ImportError as e:
    print(f"⚠️ MainWindow niet gevonden: {e}")
    print("🔍 Probeer alternatieve import...")
    try:
        from magic_time_studio.ui_pyqt6.main_window_parts.main_window_core import MainWindow
        print("✅ MainWindow geïmporteerd via main_window_core")
    except ImportError as e2:
        print(f"❌ Ook alternatieve import gefaald: {e2}")
        MainWindow = None

try:
    from magic_time_studio.ui_pyqt6.themes import ThemeManager
except ImportError:
    print("⚠️ ThemeManager niet gevonden, maak fallback aan...")
    ThemeManager = None

# Import processing modules
try:
    from magic_time_studio.core.all_functions import *
    print("✅ All functions geladen")
except ImportError:
    print("⚠️ all_functions niet gevonden, maak fallback aan...")

# Import specifieke modules
try:
    from magic_time_studio.core.translation_functions import *
    translator = "libretranslate"  # Default vertaler
    print("✅ Translation functions geladen")
except ImportError:
    print("⚠️ translation_functions niet gevonden, maak fallback aan...")
    translator = None

try:
    from magic_time_studio.core.audio_functions import *
    audio_processor = "ffmpeg"  # Default audio processor
    print("✅ Audio functions geladen")
except ImportError:
    print("⚠️ audio_functions niet gevonden, maak fallback aan...")
    audio_processor = None

try:
    from magic_time_studio.core.video_functions import *
    video_processor = "ffmpeg"  # Default video processor
    print("✅ Video functions geladen")
except ImportError:
    print("⚠️ video_functions niet gevonden, maak fallback aan...")
    video_processor = None

try:
    from .whisper_manager import whisper_manager
except ImportError:
    print("⚠️ whisper_manager niet gevonden, maak fallback aan...")
    whisper_manager = None

try:
    from .processing_thread_new import ProcessingThread
except ImportError:
    print("⚠️ ProcessingThread niet gevonden, maak fallback aan...")
    ProcessingThread = None

try:
    from .single_instance import release_single_instance_lock
except ImportError:
    print("⚠️ single_instance niet gevonden, maak fallback aan...")
    release_single_instance_lock = lambda: None

# Debug mode - zet op False om debug output uit te zetten
DEBUG_MODE = False

class MagicTimeStudioPyQt6:
    """Hoofdapplicatie klasse voor PyQt6"""
    
    def __init__(self):
        # Expose imports voor managers
        self.config_manager = config_manager
        self.stop_manager = stop_manager
        self.MainWindow = MainWindow
        self.ThemeManager = ThemeManager
        self.translator = translator
        self.audio_processor = audio_processor
        self.video_processor = video_processor
        self.whisper_manager = whisper_manager
        self.ProcessingThread = ProcessingThread
        self.release_single_instance_lock = release_single_instance_lock
        self.DEBUG_MODE = DEBUG_MODE
        
        # Controleer of kritieke modules beschikbaar zijn
        if self.config_manager is None:
            print("❌ config_manager is niet beschikbaar - dit kan problemen veroorzaken")
        
        # Initialiseer managers
        self.theme_manager = AppThemeManager(self)
        self.theme_manager.initialize_theme_manager()
        
        self.module_manager = ModuleManager(self)
        self.ui_manager = UIManager(self)
        self.processing_manager = ProcessingManager(self)
        self.file_handler = FileHandler(self)
        self.cleanup_manager = CleanupManager(self)
        
        # Initialiseer modules
        self.module_manager.initialize_modules()
    
    def create_ui(self):
        """Maak de PyQt6 gebruikersinterface"""
        return self.ui_manager.create_ui()
    
    def _on_file_selected(self, file_path: str):
        """Callback voor geselecteerd bestand"""
        return self.file_handler.on_file_selected(file_path)
    
    def _on_start_processing(self, files: list, settings: dict):
        """Start verwerking van bestanden"""
        return self.processing_manager.start_processing(files, settings)
    
    def _on_stop_processing(self):
        """Stop verwerking via StopManager"""
        return self.processing_manager.stop_processing()
    
    def run(self):
        """Start de applicatie"""
        print("🚀 Magic Time Studio PyQt6 wordt gestart...")
        
        try:
            # Maak UI
            self.create_ui()
            
            # Toon hoofdvenster
            if not self.ui_manager.show_main_window():
                return 1
            
            # Stel taakbalk icoon in na het tonen van het venster
            QTimer.singleShot(200, self.ui_manager.setTaskbarIcon)
            
            # Start event loop
            return self.ui_manager.app.exec()
            
        except Exception as e:
            print(f"❌ Fout bij starten applicatie: {e}")
            return 1
    
    def quit_app(self):
        """Sluit de applicatie"""
        print("👋 Magic Time Studio wordt afgesloten...")
        self.cleanup_manager.cleanup_on_exit()