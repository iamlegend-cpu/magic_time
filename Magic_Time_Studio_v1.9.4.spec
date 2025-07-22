# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Magic_Time_Studio_v1.9.4.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets/*', 'assets'),
        ('hooks/*', 'hooks'),
        ('venv/Lib/site-packages/whisper/assets/mel_filters.npz', 'whisper/assets'),
        ('venv/Lib/site-packages/whisper/assets/multilingual.tiktoken', 'whisper/assets'),
        ('venv/Lib/site-packages/whisper/assets/gpt2.tiktoken', 'whisper/assets'),
    ],
    hiddenimports=[
        'torch', 'torch._C',
        'torch._C._variable_functions', 'torch._C._nn', 'torch._C._fft', 'torch._C._linalg',
        'torch._C._sparse', 'torch._C._special', 'torch._C._autograd',
        'torch._C._distributed_c10d', 'torch._C._functions', 'torch._C._jit', 'torch._C._nvfuser',
        'torch._C._onnx', 'torch._C._profiler', 'torch._C._quantized', 'torch._C._serialization',
        'torch._C._tensor', 'torch._C._testing', 'torch._C._utils', 'torch._C._variable',
        'torch._C._view', 'torch._C._vmap', 'torch._C._xla',
        'whisper',
        'googletrans', 'deepl', 'librosa', 'psutil', 'cpuinfo', 'numpy', 'scipy',
        'PIL', 'moviepy.editor', 'moviepy.audio.io.AudioFileClip', 'moviepy.video.io.VideoFileClip',
        'moviepy.video.io.ffmpeg_reader', 'moviepy.video.io.ffmpeg_writer', 'moviepy.video.io.ImageSequenceClip',
        'moviepy.audio.io.ffmpeg_audiowriter', 'moviepy.audio.io.ffmpeg_audioreader', 'moviepy.video.fx.all',
        'moviepy.audio.fx.all', 'moviepy.video.io.ffmpeg_tools', 'moviepy.video.fx.fadein', 'moviepy.video.fx.fadeout',
        'moviepy.video.fx.invert_colors', 'moviepy.video.fx.resize', 'moviepy.video.fx.speedx',
        'moviepy.video.fx.time_mirror', 'moviepy.video.fx.time_symmetrize',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Magic_Time_Studio_v1.9.4',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Zet console aan voor logging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/Magic_Time_Studio.ico',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Magic_Time_Studio_v1.9.4',
)
