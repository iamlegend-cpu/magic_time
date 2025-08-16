#!/usr/bin/env python3
"""
Magic Time Studio - cx_Freeze Build Script
Creates a standalone executable using cx_Freeze
"""

import sys
import os
from cx_Freeze import setup, Executable

# Add the project root to the path
project_root = r"d:\project\magic_time"
sys.path.insert(0, project_root)

# Define the main executable
main_executable = Executable(
    "run.py",
    base=None,  # Use console base for debugging
    target_name="Magic_Time_Studio.exe",
    icon=None  # Add icon path if you have one
)

# Define build options
build_options = {
    "packages": [
        "torch",
        "torchaudio", 
        "torchvision",
        "whisperx",
        "librosa",
        "transformers",
        "speechbrain",
        "pyannote.audio",
        "accelerate",
        "onnxruntime",
        "openai_whisper",
        "faster_whisper",
        "numpy",
        "numba",
        "PySide6",
        "cv2",
        "PIL",
        "scipy",
        "matplotlib",
        "pandas",
        "requests",
        "json",
        "threading",
        "queue",
        "time",
        "datetime",
        "pathlib",
        "shutil",
        "subprocess",
        "tempfile",
        "zipfile",
        "tarfile",
        "pickle",
        "sqlite3",
        "xml",
        "html",
        "urllib",
        "ssl",
        "hashlib",
        "base64",
        "collections",
        "itertools",
        "functools",
        "operator",
        "re",
        "math",
        "statistics",
        "random",
        "logging",
        "warnings",
        "traceback",
        "inspect",
        "types",
        "weakref",
        "copy",
        "pprint",
        "textwrap",
        "difflib",
        "string",
        "unicodedata",
        "locale",
        "gettext",
        "argparse",
        "optparse",
        "configparser",
        "csv",
        "netrc",
        "xdrlib",
        "plistlib",
        "shelve",
        "dbm",
        "zlib",
        "gzip",
        "bz2",
        "lzma",
        "glob",
        "fnmatch",
        "linecache",
        "copyreg",
        "marshal"
    ],
    "excludes": [
        "tkinter",
        "test",
        "unittest",
        "distutils",
        "setuptools",
        "pip",
        "wheel"
    ],
    "include_files": [
        ("ui_pyside6/", "ui_pyside6/"),
        ("assets/", "assets/")
    ],
    "optimize": 2,
    "build_exe": "build_cx_freeze"
}

# Setup configuration
setup(
    name="Magic Time Studio",
    version="1.0.0",
    description="AI-powered audio transcription and translation studio",
    options={"build_exe": build_options},
    executables=[main_executable]
)
