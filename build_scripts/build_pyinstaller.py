#!/usr/bin/env python3
"""
Magic Time Studio - PyInstaller Build Script
Creates a standalone executable using PyInstaller
"""

import PyInstaller.__main__
import os
import sys
import shutil

# Get the current directory (project root)
current_dir = r"d:\project\magic_time"

# Clean previous build
build_dir = os.path.join(current_dir, "build_pyinstaller")
if os.path.exists(build_dir):
    shutil.rmtree(build_dir)

# Define the main script path relative to project root
main_script = os.path.join(current_dir, "run.py")

# Verify the main script exists
if not os.path.exists(main_script):
    print(f"❌ Hoofdscript niet gevonden: {main_script}")
    sys.exit(1)

print(f"✅ Hoofdscript gevonden: {main_script}")

# Define PyInstaller arguments
args = [
    main_script,  # Use absolute path to main script
    '--onedir',  # Create directory with executable and dependencies
    '--windowed',  # Hide console window
    '--name=Magic_Time_Studio',  # Executable name
    f'--icon={os.path.join(current_dir, "assets", "Magic_Time_Studio.ico")}',  # Application icon
    f'--version-file={os.path.join(current_dir, "version_info.txt")}',  # Version information
    '--distpath=build_pyinstaller',  # Output directory
    '--workpath=build_pyinstaller/work',  # Work directory
    '--specpath=build_pyinstaller',  # Spec file directory
    # Add data files with correct paths
    f'--add-data={os.path.join(current_dir, "ui_pyside6")};ui_pyside6',
    f'--add-data={os.path.join(current_dir, "assets")};assets',
    # Add binary files
    f'--add-binary={os.path.join(current_dir, "assets", "FFmpeg.exe")};.',
    # Hidden imports
    '--hidden-import=torch',
    '--hidden-import=torchaudio',
    '--hidden-import=torchvision',
    '--hidden-import=whisperx',
    '--hidden-import=librosa',
    '--hidden-import=transformers',
    '--hidden-import=speechbrain',
    '--hidden-import=pyannote.audio',
    '--hidden-import=accelerate',
    '--hidden-import=onnxruntime',
    '--hidden-import=openai_whisper',
    '--hidden-import=faster_whisper',
    '--hidden-import=numpy',
    '--hidden-import=numba',
    '--hidden-import=PySide6',
    '--hidden-import=cv2',
    '--hidden-import=PIL',
    '--hidden-import=scipy',
    '--hidden-import=matplotlib',
    '--hidden-import=pandas',
    '--hidden-import=requests',
    # Collect all packages
    '--collect-all=torch',
    '--collect-all=transformers',
    '--collect-all=librosa',
    '--collect-all=whisperx',
    '--collect-all=speechbrain',
    '--collect-all=pyannote.audio',
    '--collect-all=accelerate',
    '--collect-all=onnxruntime',
    '--collect-all=openai_whisper',
    '--collect-all=faster_whisper',
    '--collect-all=numba',
    '--collect-all=PySide6',
    '--collect-all=cv2',
    '--collect-all=PIL',
    '--collect-all=scipy',
    '--collect-all=matplotlib',
    '--collect-all=pandas',
    '--collect-all=requests',
    # Exclude modules
    '--exclude-module=tkinter',
    '--exclude-module=test',
    '--exclude-module=unittest',
    '--exclude-module=distutils',
    '--exclude-module=setuptools',
    '--exclude-module=pip',
    '--exclude-module=wheel',
    '--exclude-module=pkg_resources',  # Exclude problematic pkg_resources
    # Other options
    '--clean',  # Clean cache before building
    '--noconfirm'  # Don't ask for confirmation
]

print("🚀 Start PyInstaller build...")
print(f"📁 Project root: {current_dir}")
print(f"📁 Main script: {main_script}")
print(f"📁 Build output: {build_dir}")

# Run PyInstaller
PyInstaller.__main__.run(args)
