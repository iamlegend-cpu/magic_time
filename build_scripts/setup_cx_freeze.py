"""
Setup script voor cx_Freeze - Magic Time Studio PySide6
Gebruik: python setup_cx_freeze.py build
"""

import sys
import os
from cx_Freeze import setup, Executable

# Voeg project root toe aan Python path
project_root = r"d:\project\magic_time"
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Basis configuratie
build_exe_options = {
    "packages": [
        "PySide6",
        "torch",
        "torchaudio", 
        "whisperx",
        "librosa",
        "ffmpeg",
        "libretranslate",
        "speechbrain",
        "pyannote.audio",
        "silero",
        "transformers",
        "accelerate",
        "optimum",
        "onnxruntime",
        "openai_whisper",
        "stable_ts",
        "faster_whisper",
        "numpy",
        "scipy",
        "matplotlib",
        "seaborn",
        "pandas",
        "requests",
        "urllib3",
        "certifi",
        "charset_normalizer",
        "idna",
        "psutil",
        "GPUtil",
    ],
    "excludes": [],
    "include_files": [
        ("ui_pyside6", "ui_pyside6"),
        ("assets", "assets"),
        ("whisper_config.env", "whisper_config.env"),
    ],
    "include_msvcr": True,
}

# Executable configuratie
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Voor GUI applicatie zonder console

executables = [
    Executable(
        "run.py",
        base=base,
        target_name="Magic_Time_Studio.exe",
        icon="assets/Magic_Time_Studio.ico",
        shortcut_name="Magic Time Studio",
        shortcut_dir="DesktopFolder",
    )
]

# Setup configuratie
setup(
    name="Magic Time Studio",
    version="1.0.0",
    description="Magic Time Studio - Audio/Video Transcriptie en Vertaling",
    options={"build_exe": build_exe_options},
    executables=executables,
    requires=["PySide6", "torch", "whisperx"],
)
