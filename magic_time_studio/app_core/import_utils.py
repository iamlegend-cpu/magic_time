"""
Import utilities voor Magic Time Studio
Bevat veilige imports en fallback logica
"""

# Import processing modules
try:
    from magic_time_studio.core import all_functions
except ImportError:
    all_functions = None

def safe_import_config_manager():
    """Veilige import van config manager met fallback"""
    try:
        from magic_time_studio.core.config import config_manager
        if config_manager is None:
            print("⚠️ config_manager is None, maak fallback aan...")
            return None
        return config_manager
    except ImportError as e:
        print(f"⚠️ config_manager niet gevonden: {e}, maak fallback aan...")
        return None

def safe_import_stop_manager():
    """Veilige import van stop manager met fallback"""
    try:
        from magic_time_studio.core.stop_manager import stop_manager
        if stop_manager is None:
            print("⚠️ stop_manager is None, maak fallback aan...")
            return None
        return stop_manager
    except ImportError as e:
        print(f"⚠️ stop_manager niet gevonden: {e}, maak fallback aan...")
        return None

def safe_import_main_window():
    """Veilige import van MainWindow met fallback"""
    try:
        from magic_time_studio.ui_pyqt6.main_window import MainWindow
        if MainWindow is None:
            print("⚠️ MainWindow is None, maak fallback aan...")
            return None
        return MainWindow
    except ImportError as e:
        print(f"⚠️ MainWindow niet gevonden: {e}, maak fallback aan...")
        return None

def safe_import_theme_manager():
    """Veilige import van ThemeManager met fallback"""
    try:
        from magic_time_studio.ui_pyqt6.themes import ThemeManager
        if ThemeManager is None:
            print("⚠️ ThemeManager is None, maak fallback aan...")
            return None
        return ThemeManager
    except ImportError as e:
        print(f"⚠️ ThemeManager niet gevonden: {e}, maak fallback aan...")
        return None

def safe_import_processing_modules():
    """Veilige import van processing modules met fallbacks"""
    try:
        # Import specifieke modules in plaats van wildcard
        from magic_time_studio.core import all_functions
        # Alle functies zijn nu beschikbaar via all_functions
        return True, True, True
    except ImportError as e:
        print(f"⚠️ Processing modules niet gevonden: {e}, maak fallbacks aan...")
        return None, None, None

def safe_import_whisper_manager():
    """Veilige import van whisper manager met fallback"""
    try:
        # Import specifieke modules in plaats van wildcard
        from magic_time_studio.core import whisper_functions
        # Whisper functies zijn nu beschikbaar via whisper_functions
        return True
    except ImportError as e:
        print(f"⚠️ whisper_manager niet gevonden: {e}, maak fallback aan...")
        return None

def safe_import_processing_thread():
    """Veilige import van ProcessingThread met fallback"""
    try:
        from magic_time_studio.app_core.processing_thread_new import ProcessingThread
        if ProcessingThread is None:
            print("⚠️ ProcessingThread is None, maak fallback aan...")
            return None
        return ProcessingThread
    except ImportError as e:
        print(f"⚠️ ProcessingThread niet gevonden: {e}, maak fallback aan...")
        return None

def safe_import_single_instance():
    """Veilige import van single instance met fallback"""
    try:
        from magic_time_studio.app_core.single_instance import release_single_instance_lock
        if release_single_instance_lock is None:
            print("⚠️ single_instance is None, maak fallback aan...")
            return lambda: None
        return release_single_instance_lock
    except ImportError as e:
        print(f"⚠️ single_instance niet gevonden: {e}, maak fallback aan...")
        return lambda: None
