"""
Diagnostische functies voor Magic Time Studio
Bevat Whisper diagnose, CUDA test en documentatie openen
"""

import webbrowser
# Import processing modules
from .all_functions import *

def whisper_diagnose():
    """Geef informatie over het geladen Whisper-model"""
    if not whisper_manager.is_model_loaded():
        return "Whisper model is niet geladen."
    info = whisper_manager.get_model_info()
    if 'error' in info:
        return f"Fout: {info['error']}"
    return (
        f"Whisper model: {info.get('model_name', 'onbekend')}\n"
        f"Model size: {info.get('model_size', 'onbekend')}\n"
        f"Device: {info.get('device', 'onbekend')}\n"
        f"Multilingual: {'Ja' if info.get('is_multilingual') else 'Nee'}"
    )

def cuda_test():
    """Test of CUDA beschikbaar is voor Whisper (PyTorch)"""
    try:
        import torch
        cuda_available = torch.cuda.is_available()
        device_count = torch.cuda.device_count() if cuda_available else 0
        device_name = torch.cuda.get_device_name(0) if cuda_available and device_count > 0 else 'n.v.t.'
        return (
            f"CUDA beschikbaar: {'Ja' if cuda_available else 'Nee'}\n"
            f"Aantal CUDA devices: {device_count}\n"
            f"Device naam: {device_name}"
        )
    except ImportError:
        return "PyTorch is niet geïnstalleerd."
    except Exception as e:
        return f"Fout bij CUDA test: {e}"

def open_documentatie():
    """Open de online documentatie in de browser"""
    url = "https://github.com/magic-time-studio/magic_time_studio/wiki"
    try:
        webbrowser.open(url)
        return f"Documentatie geopend: {url}"
    except Exception as e:
        return f"Kon documentatie niet openen: {e}"

def check_system_requirements():
    """Controleer systeem vereisten"""
    print("🔍 Systeem vereisten controle...")
    
    # Python versie
    import sys
    python_version = sys.version_info
    print(f"🐍 Python: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Platform
    print(f"💻 Platform: {sys.platform}")
    
    # PyInstaller status
    if hasattr(sys, '_MEIPASS'):
        print("📦 PyInstaller: Gedetecteerd (bundled executable)")
    else:
        print("📦 PyInstaller: Niet gedetecteerd (normale Python omgeving)")
    
    # Controleer optionele packages
    optional_packages = []
    
    try:
        import torch
        print("✅ PyTorch: Beschikbaar")
    except ImportError:
        print("⚠️ PyTorch: Niet beschikbaar")
        optional_packages.append("torch")
    
    try:
        import whisper
        print("✅ Whisper: Beschikbaar")
    except ImportError:
        print("⚠️ Whisper: Niet beschikbaar")
        optional_packages.append("whisper")
    
    try:
        import faster_whisper
        print("✅ Faster Whisper: Beschikbaar")
    except ImportError:
        print("⚠️ Faster Whisper: Niet beschikbaar")
        optional_packages.append("faster_whisper")
    
    if optional_packages:
        print(f"💡 Ontbrekende optionele packages: {', '.join(optional_packages)}")
        print("💡 Deze packages zijn nodig voor whisper functionaliteit")
        print("💡 Het programma kan starten maar whisper features werken niet")
    
    return len(optional_packages) == 0

def get_project_info():
    """Krijg project informatie"""
    import os
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller bundle
        bundle_dir = sys._MEIPASS
        print(f"📁 Project root: {bundle_dir}")
        return bundle_dir
    else:
        # Normale Python omgeving
        current_dir = os.getcwd()
        print(f"📁 Project root: {current_dir}")
        return current_dir

if __name__ == "__main__":
    check_system_requirements()
    get_project_info() 