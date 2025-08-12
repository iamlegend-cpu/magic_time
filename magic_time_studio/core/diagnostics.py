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