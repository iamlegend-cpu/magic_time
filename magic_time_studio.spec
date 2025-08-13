# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Bestanden en mappen die gekopieerd moeten worden
datas = [
    # Magic Time Studio modules
    ('magic_time_studio', 'magic_time_studio'),
    ('magic_time_studio/core', 'magic_time_studio/core'),
    ('magic_time_studio/app_core', 'magic_time_studio/app_core'),
    ('magic_time_studio/ui_pyqt6', 'magic_time_studio/ui_pyqt6'),
    ('magic_time_studio/models', 'magic_time_studio/models'),
    
    # Assets
    ('assets', 'assets'),
    
    # Config bestanden
    ('magic_time_studio/whisper_config.env', 'magic_time_studio'),
    
    # Unittest module (handmatig toevoegen)
    ('C:/Python311/Lib/unittest', 'unittest'),
]

# Verborgen imports die PyInstaller niet automatisch vindt
hiddenimports = [
    # PyQt6
    'PyQt6.QtCore',
    'PyQt6.QtGui', 
    'PyQt6.QtWidgets',
    'PyQt6.QtNetwork',
    
    # Magic Time Studio package
    'magic_time_studio',
    
    # Whisper en Fast Whisper
    'faster_whisper',
    'whisper',
    
    # Torch (PyTorch) - CUDA versie
    'torch',
    'torch.nn',
    'torch.utils',
    
    # Audio processing
    'numpy',
    'librosa',
    'soundfile',
    'av',
    
    # Machine learning
    'numba',
    'llvmlite',
    'ctranslate2',
    'tokenizers',
    
    # HTTP requests voor vertaling
    'requests',
    'urllib3',
    'certifi',
    'charset_normalizer',
    
    # GPU monitoring
    'pynvml',
    
    # Extra imports voor betere compatibiliteit
    'pathlib',
    'os',
    'sys',
    'threading',
    'queue',
    'datetime',
    'json',
    'pickle',
    'hashlib',
    'shutil',
    'tempfile',
    'subprocess',
    'webbrowser',
    'time',
    'logging',
    'typing',
    'collections',
    'itertools',
    'functools',
    'contextlib',
    'inspect',
    'importlib',
    
    # PyTorch dependencies
    'unittest',
]

# Exclude onnodige modules om de exe kleiner te maken
excludes = [
    'tkinter',
    'matplotlib',
    'scipy',
    'pandas',
    'IPython',
    'jupyter',
    'notebook',
    'pytest',
    'unittest',
    'test',
    'tests',
    'doc',
    'docs',
    '*.pyc',
    '__pycache__',
]

# Runtime hooks voor betere pad handling
runtime_hooks = ['tools/hooks/runtime_hook.py']

a = Analysis(
    ['magic_time_studio/run.py'],  # Gebruik run.py als entry point
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=['tools/hooks'],
    hooksconfig={},
    runtime_hooks=runtime_hooks,
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    datas_excludes=['**/test*', '**/tests*', '**/doc*', '**/docs*', '**/__pycache__*', '**/*.pyc'],
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

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
    console=True,  # Console venster tonen
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/Magic_Time_Studio.ico',  # Hoofdicon
    noconfirm=True,  # Automatisch overschrijven zonder bevestiging
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
    noconfirm=True,  # Automatisch overschrijven zonder bevestiging
)
