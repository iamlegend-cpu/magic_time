# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('ui_pyside6', 'ui_pyside6'),
        ('assets', 'assets'),
        ('whisper_config.env', '.'),
    ],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtGui', 
        'PySide6.QtWidgets',
        'PySide6.QtNetwork',
        'torch',
        'torchaudio',
        'whisperx',
        'librosa',
        'ffmpeg',
        'libretranslate',
        'speechbrain',
        'pyannote.audio',
        'silero',
        'transformers',
        'accelerate',
        'optimum',
        'onnxruntime',
        'openai_whisper',
        'stable_ts',
        'faster_whisper',
        'numpy',
        'scipy',
        'matplotlib',
        'seaborn',
        'pandas',
        'requests',
        'urllib3',
        'certifi',
        'charset_normalizer',
        'idna',
        'psutil',
        'GPUtil',
    ],
    hookspath=['tools/hooks'],
    hooksconfig={},
    runtime_hooks=['tools/hooks/runtime_hook.py'],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Magic_Time_Studio',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Console enabled
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/Magic_Time_Studio.ico'
)

# OneDir optie (aanbevolen voor development en debugging)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Magic_Time_Studio'
)

# Build commando met --noconfirm voor snellere builds:
# pyinstaller magic_time_studio.spec --clean --noconfirm
