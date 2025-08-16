"""
Import utilities voor Magic Time Studio
Bevat veilige imports en fallback logica
"""

import os
import sys

def setup_tf32():
    """Schakel TF32 in voor betere CUDA prestaties en om waarschuwingen te voorkomen"""
    try:
        # Stel environment variables in voordat pyannote.audio wordt geladen
        os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:128"
        os.environ["CUDA_LAUNCH_BLOCKING"] = "0"
        
        # Schakel TF32 in via environment variables (wordt gerespecteerd door pyannote.audio)
        os.environ["TORCH_ALLOW_TF32_CUBLAS_OVERRIDE"] = "1"
        
        import torch
        if torch.cuda.is_available():
            torch.backends.cuda.matmul.allow_tf32 = True
            torch.backends.cudnn.allow_tf32 = True
            print("✅ TF32 ingeschakeld voor betere CUDA prestaties")
            return True
        else:
            print("⚠️ CUDA niet beschikbaar - TF32 niet nodig")
            return False
    except Exception as e:
        print(f"⚠️ Kon TF32 niet inschakelen: {e}")
        return False

def setup_ffmpeg_path():
    """Voeg FFmpeg toe aan PATH vanuit assets directory"""
    try:
        # Controleer of we in een PyInstaller exe draaien
        if getattr(sys, 'frozen', False):
            # We draaien in een PyInstaller exe
            base_path = sys._MEIPASS
            ffmpeg_path = os.path.join(base_path, "assets")
            print(f"🔍 [EXE] Zoek FFmpeg in: {ffmpeg_path}")
        else:
            # We draaien als Python script
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)  # Ga één niveau omhoog naar magic_time
            ffmpeg_path = os.path.join(project_root, "assets")
            print(f"🔍 [SCRIPT] Zoek FFmpeg in: {ffmpeg_path}")
        
        if os.path.exists(os.path.join(ffmpeg_path, "ffmpeg.exe")):
            if ffmpeg_path not in os.environ.get("PATH", ""):
                os.environ["PATH"] = ffmpeg_path + os.pathsep + os.environ.get("PATH", "")
                print(f"🔧 FFmpeg toegevoegd aan PATH: {ffmpeg_path}")
                return True
            else:
                print(f"✅ FFmpeg al beschikbaar in PATH: {ffmpeg_path}")
                return True
        else:
            print(f"⚠️ FFmpeg niet gevonden in: {ffmpeg_path}")
            
            # Probeer alternatieve locaties
            alt_paths = []
            if getattr(sys, 'frozen', False):
                # In exe context, probeer verschillende paden
                alt_paths = [
                    os.path.join(base_path, "magic_time_studio", "assets"),
                    os.path.join(base_path, "assets"),
                    "assets"
                ]
            else:
                # In script context, probeer normale paden
                alt_paths = [
                    os.path.join(project_root, "assets"),  # magic_time/assets
                    os.path.join(os.getcwd(), "assets"),   # huidige werkdirectory/assets
                    "assets"                               # relatieve assets directory
                ]
            
            for alt_path in alt_paths:
                if os.path.exists(os.path.join(alt_path, "ffmpeg.exe")):
                    if alt_path not in os.environ.get("PATH", ""):
                        os.environ["PATH"] = alt_path + os.pathsep + os.environ.get("PATH", "")
                        print(f"🔧 FFmpeg toegevoegd aan PATH via alternatief pad: {alt_path}")
                        return True
                    else:
                        print(f"✅ FFmpeg al beschikbaar in PATH via alternatief pad: {alt_path}")
                        return True
            
            return False
    except Exception as e:
        print(f"⚠️ Fout bij instellen FFmpeg PATH: {e}")
        return False

# PyInstaller-compatibele imports - probeer eerst de volledige module path
try:
    from core import all_functions
    print("✅ all_functions import succesvol via core")
except ImportError as e:
    print(f"⚠️ all_functions import mislukt: {e}")
    all_functions = None

def safe_import_config_manager():
    """Veilige import van config manager met fallback"""
    try:
        from core.config import config_manager
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
        from core.stop_manager import stop_manager
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
        from ui_pyside6.main_window import MainWindow
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
        from ui_pyside6.themes import ThemeManager
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
        from core import all_functions
        # Alle functies zijn nu beschikbaar via all_functions
        return True, True, True
    except ImportError as e:
        print(f"⚠️ Processing modules niet gevonden: {e}, maak fallbacks aan...")
        return None, None, None

def safe_import_whisper_manager():
    """Veilige import van whisper manager met fallback"""
    try:
        # Import specifieke modules in plaats van wildcard
        from core import whisper_functions
        # Whisper functies zijn nu beschikbaar via whisper_functions
        return True
    except ImportError as e:
        print(f"⚠️ whisper_manager niet gevonden: {e}, maak fallback aan...")
        return None

def safe_import_processing_thread():
    """Veilige import van ProcessingThread met fallback"""
    try:
        from app_core.processing_thread_new import ProcessingThread
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
        from app_core.single_instance import release_single_instance_lock
        if release_single_instance_lock is None:
            print("⚠️ single_instance is None, maak fallback aan...")
            return lambda: None
        return release_single_instance_lock
    except ImportError as e:
        print(f"⚠️ single_instance niet gevonden: {e}, maak fallback aan...")
        return lambda: None
