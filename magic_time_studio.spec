# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Data bestanden die meegenomen moeten worden
datas = [
    # Assets en configuratie
    ('assets', 'assets'),
    ('magic_time_studio/whisper_config.env', '.'),
    ('magic_time_studio/ui_pyqt6/themes.py', 'ui_pyqt6'),
    
    # Whisper modellen en data
    ('magic_time_studio/whisper_config.env', 'magic_time_studio'),
    
    # UI componenten
    ('magic_time_studio/ui_pyqt6/components', 'ui_pyqt6/components'),
    
    # Core modules
    ('magic_time_studio/core', 'core'),
    ('magic_time_studio/app_core', 'app_core'),
    ('magic_time_studio/processing', 'processing'),
    
    # Python bestanden die als data moeten worden meegenomen
    ('magic_time_studio/run.py', '.'),
    ('magic_time_studio/main_pyqt6.py', '.'),
    ('magic_time_studio/startup.py', '.'),
]

# Verborgen imports die PyInstaller niet automatisch vindt
hiddenimports = [
    # PyQt6
    'PyQt6.QtCore',
    'PyQt6.QtGui', 
    'PyQt6.QtWidgets',
    'PyQt6.QtNetwork',
    
    # Whisper en Fast Whisper
    'faster_whisper',
    'faster_whisper.whisper',
    'faster_whisper.audio',
    'faster_whisper.transcribe',
    'faster_whisper.utils',
    'faster_whisper.vad',
    
    # Torch (PyTorch) - uitgebreide imports voor standaard Whisper
    'torch',
    'torch._C',
    'torch._C._distributed_c10d',
    'torch._C._distributed_c10d_backend',
    'torch._C._distributed_c10d_backend_nccl',
    'torch._C._distributed_c10d_backend_gloo',
    'torch._C._distributed_c10d_backend_mpi',
    'torch._C._distributed_c10d_backend_ucc',
    'torch._C._distributed_c10d_backend_work',
    'torch._C._distributed_c10d_backend_work_mpi',
    'torch._C._distributed_c10d_backend_work_nccl',
    'torch._C._distributed_c10d_backend_work_gloo',
    'torch._C._distributed_c10d_backend_work_ucc',
    'torch.nn',
    'torch.nn.functional',
    'torch.optim',
    'torch.utils',
    'torch.utils.data',
    'torch.utils.data.dataloader',
    'torch.utils.data.dataset',
    'torch.utils.data.sampler',
    'torch.utils.data.worker',
    
    # Whisper (standaard)
    'whisper',
    'whisper.audio',
    'whisper.decoding',
    'whisper.model',
    'whisper.normalizers',
    'whisper.parsing',
    'whisper.timing',
    'whisper.transcribe',
    'whisper.utils',
    
    # Audio processing
    'numpy',
    'librosa',
    'librosa.core',
    'librosa.feature',
    'librosa.util',
    'soundfile',
    'av',
    'ffmpeg',
    
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
    
    # Magic Time Studio modules
    'magic_time_studio.app_core.main_entry',
    'magic_time_studio.app_core.magic_time_studio_pyqt6',
    'magic_time_studio.app_core.processing_modules.audio_processing',
    'magic_time_studio.app_core.processing_modules.video_processing',
    'magic_time_studio.app_core.processing_modules.whisper_processing',
    'magic_time_studio.app_core.processing_modules.translation_processing',
    'magic_time_studio.app_core.processing_thread',
    'magic_time_studio.ui_pyqt6.main_window',
    'magic_time_studio.ui_pyqt6.components.settings_panel',
    'magic_time_studio.ui_pyqt6.components.whisper_selector.whisper_selector_widget',
    'magic_time_studio.ui_pyqt6.components.whisper_selector.model_load_thread',
    'magic_time_studio.processing.whisper_manager',
    'magic_time_studio.processing.translator',
    'magic_time_studio.processing.video_processor',
    'magic_time_studio.processing.audio_processor',
    'magic_time_studio.core.config',
    'magic_time_studio.core.logging',
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
]

a = Analysis(
    ['magic_time_studio/run.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=['tools/hooks'],
    hooksconfig={},
    runtime_hooks=['tools/hooks/runtime_hook.py'],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    datas_excludes=['**/test*', '**/tests*', '**/doc*', '**/docs*'],
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
    name='Magic_Time_Studio'
)
