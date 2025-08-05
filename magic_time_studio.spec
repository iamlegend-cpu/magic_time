# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Add the project root to the path
project_root = os.getcwd()  # Use getcwd() instead of __file__
sys.path.insert(0, project_root)

# Collect all necessary data files and modules
datas = []
binaries = []
datas.extend(collect_data_files('magic_time_studio'))
datas.extend(collect_data_files('whisper'))
datas.extend(collect_data_files('torch'))
datas.extend(collect_data_files('torchaudio'))

# Add assets directory
assets_dir = os.path.join(project_root, 'assets')
if os.path.exists(assets_dir):
    datas.append((assets_dir, 'assets'))

# Add icon files specifically
icon_files = [
    os.path.join(project_root, 'assets', 'Magic_Time_Studio.ico'),
    os.path.join(project_root, 'assets', 'Magic_Time_Studio_wit.ico'),
]
for icon_file in icon_files:
    if os.path.exists(icon_file):
        datas.append((icon_file, 'assets'))

# Add ffmpeg if it exists
ffmpeg_path = os.path.join(project_root, 'assets', 'ffmpeg.exe')
if os.path.exists(ffmpeg_path):
    datas.append((ffmpeg_path, '.'))
    print(f"FFmpeg toegevoegd aan bundle: {ffmpeg_path}")
else:
    print(f"FFmpeg niet gevonden: {ffmpeg_path}")

# Add ffmpeg to binaries as well (in root directory)
if os.path.exists(ffmpeg_path):
    binaries.append((ffmpeg_path, '.'))
    print(f"FFmpeg toegevoegd aan binaries: {ffmpeg_path}")
    
    # Also add to datas with explicit root placement
    datas.append((ffmpeg_path, '.'))
    print(f"FFmpeg toegevoegd aan datas root: {ffmpeg_path}")

# Hidden imports
hiddenimports = [
    'magic_time_studio',
    'magic_time_studio.core',
    'magic_time_studio.ui_pyqt6',
    'magic_time_studio.ui_pyqt6.components',
    'magic_time_studio.ui_pyqt6.features',
    'magic_time_studio.processing',
    'magic_time_studio.models',
    'whisper',
    'torch',
    'torchaudio',
    'PyQt6',
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
    'numpy',
    'librosa',
    'soundfile',
    'tqdm',
]

# Exclude unnecessary modules to reduce size
excludes = [
    'matplotlib',
    'scipy.spatial.cKDTree',
    'scipy.spatial.transform',
    'scipy.special',
    'scipy.stats',
    'PIL',
    'tkinter',
    'IPython',
    'jupyter',
    'notebook',
    'pandas',
    'seaborn',
    'plotly',
    'bokeh',
]

a = Analysis(
    ['magic_time_studio/main_pyqt6.py'],
    pathex=[project_root],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[os.path.join(project_root, 'tools', 'hooks')],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Magic_Time_Studio',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Console window behouden voor debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(project_root, 'assets', 'Magic_Time_Studio_wit.ico'),  # Gebruik wit icoon voor betere zichtbaarheid
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Magic_Time_Studio',
) 