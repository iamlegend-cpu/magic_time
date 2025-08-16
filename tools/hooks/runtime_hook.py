"""
Runtime hook voor PyInstaller - Magic Time Studio PySide6
Zorgt ervoor dat alle benodigde modules correct worden geladen
"""

import sys
import os

# Voeg project root toe aan Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Zorg ervoor dat PySide6 modules correct worden geladen
try:
    import PySide6
    import PySide6.QtCore
    import PySide6.QtGui
    import PySide6.QtWidgets
    import PySide6.QtNetwork
except ImportError as e:
    print(f"⚠️ PySide6 import fout: {e}")

# Zorg ervoor dat lokale modules correct worden geladen
try:
    import app_core
    import ui_pyside6
    import core
except ImportError as e:
    print(f"⚠️ Magic Time Studio module import fout: {e}")

# Zorg ervoor dat WhisperX en gerelateerde modules correct worden geladen
try:
    import torch
    import torchaudio
    import whisperx
    import librosa
    import ffmpeg
    import speechbrain
    import pyannote.audio
    import silero
    import transformers
    import accelerate
    import optimum
    import onnxruntime
    import openai_whisper
    import stable_ts
    import faster_whisper
except ImportError as e:
    print(f"⚠️ WhisperX gerelateerde module import fout: {e}")

print("✅ Runtime hook geladen voor Magic Time Studio PySide6")
