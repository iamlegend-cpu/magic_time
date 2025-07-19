# -*- mode: python ; coding: utf-8 -*-

import os
import inspect
import sys

# Patch inspect functions before importing torch
def fake_getsource(*args, **kwargs):
    return ""

def fake_getsourcefile(*args, **kwargs):
    return None

inspect.getsource = fake_getsource
inspect.getsourcefile = fake_getsourcefile

# Import torch after patching inspect
try:
    import torch
    torch_available = True
except ImportError:
    torch_available = False
    print("WARNING: torch not available")

from glob import glob
import numpy

# Vind de torch-libs als beschikbaar
torch_binaries = []
if torch_available:
    try:
        torch_dir = os.path.dirname(torch.__file__)
        torch_binaries = [(dll, 'torch/lib') for dll in glob(os.path.join(torch_dir, 'lib', '*.dll'))]
        torch_binaries += [(dll, 'torch') for dll in glob(os.path.join(torch_dir, '*.dll'))]
        # Voeg specifieke DLL's toe
        torch_lib_dir = os.path.join(torch_dir, 'lib')
        specific_dlls = ['torch.dll', 'torch_cpu.dll', 'c10.dll', 'c10_cuda.dll']
        for dll_name in specific_dlls:
            dll_path = os.path.join(torch_lib_dir, dll_name)
            if os.path.exists(dll_path):
                torch_binaries.append((dll_path, 'torch/lib'))
    except Exception as e:
        torch_binaries = []
        print(f"WARNING: torch binaries niet gevonden: {e}")

# Voeg numpy DLL's toe
try:
    numpy_dir = os.path.dirname(numpy.__file__)
    numpy_binaries = [(dll, 'numpy') for dll in glob(os.path.join(numpy_dir, '*.dll'))]
except Exception as e:
    numpy_binaries = []
    print(f"WARNING: numpy binaries niet gevonden: {e}")

# Voeg eventueel extra binaries toe (zoals ffmpeg)
extra_binaries = []
if os.path.exists('ffmpeg.exe'):
    extra_binaries.append(('ffmpeg.exe', '.'))

# Gebruik relatieve paden in plaats van hardcoded absolute paden
import llvmlite
llvmlite_dir = os.path.join(os.path.dirname(llvmlite.__file__), 'binding')

# Zoek naar scipy _ccallback_c bestand
scipy_ccallback = None
try:
    import scipy
    scipy_dir = os.path.dirname(scipy.__file__)
    scipy_lib_dir = os.path.join(scipy_dir, '_lib')
    for file in os.listdir(scipy_lib_dir):
        if file.startswith('_ccallback_c') and file.endswith('.pyd'):
            scipy_ccallback = os.path.join(scipy_lib_dir, file)
            break
except Exception as e:
    print(f"WARNING: scipy _ccallback_c niet gevonden: {e}")

binaries = torch_binaries + numpy_binaries + extra_binaries

# Voeg llvmlite en scipy binaries toe als ze bestaan
if os.path.exists(os.path.join(llvmlite_dir, 'llvmlite.dll')):
    binaries.append((os.path.join(llvmlite_dir, 'llvmlite.dll'), 'llvmlite/binding'))

if scipy_ccallback and os.path.exists(scipy_ccallback):
    binaries.append((scipy_ccallback, 'scipy/_lib'))

import os
# Verwijder alle extra_datas voor librosa, alleen assets blijven over

# Verwijder de testhook (indien aanwezig)
try:
    os.remove('hooks/hook_runtime_test.py')
except Exception:
    pass

a = Analysis(
    ['Magic_Time_Studio_v1.9.4.py'],
    pathex=[],
    binaries=binaries,
    datas=[
        ('assets', 'assets'),
        ('hooks', 'hooks'),
        ('venv/Lib/site-packages/whisper/assets/mel_filters.npz', 'whisper/assets'),
        ('venv/Lib/site-packages/whisper/assets/multilingual.tiktoken', 'whisper/assets'),
    ],
    hiddenimports=[
        'torch', 'torch._C',
        'torch._C._variable_functions', 'torch._C._nn', 'torch._C._fft', 'torch._C._linalg',
        'torch._C._sparse', 'torch._C._special', 'torch._C._cuda', 'torch._C._autograd',
        'torch._C._distributed_c10d', 'torch._C._functions', 'torch._C._jit', 'torch._C._nvfuser',
        'torch._C._onnx', 'torch._C._profiler', 'torch._C._quantized', 'torch._C._serialization',
        'torch._C._tensor', 'torch._C._testing', 'torch._C._utils', 'torch._C._variable',
        'torch._C._view', 'torch._C._vmap', 'torch._C._xla',
        'whisper',
        'googletrans', 'deepl', 'librosa', 'psutil', 'cpuinfo',
        'numpy', 'numpy.core._methods', 'numpy.lib.format',
        # MoviePy hidden imports
        'moviepy.editor',
        'moviepy.audio.io.AudioFileClip',
        'moviepy.video.io.VideoFileClip',
        'moviepy.video.io.ffmpeg_reader',
        'moviepy.video.io.ffmpeg_writer',
        'moviepy.video.io.ImageSequenceClip',
        'moviepy.audio.io.ffmpeg_audiowriter',
        'moviepy.audio.io.ffmpeg_audioreader',
        'moviepy.video.fx.all',
        'moviepy.audio.fx.all',
        'moviepy.video.io.ffmpeg_tools',
        'moviepy.video.fx.fadein',
        'moviepy.video.fx.fadeout',
        'moviepy.video.fx.invert_colors',
        'moviepy.video.fx.resize',
        'moviepy.video.fx.speedx',
        'moviepy.video.fx.time_mirror',
        'moviepy.video.fx.time_symmetrize',
        'moviepy.audio.fx.audio_fadein',
        'moviepy.audio.fx.audio_fadeout',
        'moviepy.audio.fx.volumex',
        # Voeg hier meer toe als je andere AI/ML-libs gebruikt
    ],
    hookspath=['hooks'],  # <-- Custom hooks map (mag blijven)
    hooksconfig={},
    # Gebruik relatieve paden voor runtime_hooks
    runtime_hooks=[
        'hooks/hook_torch_inspect.py',
        'hooks/hook_llvmlite_fix.py',
        'hooks/hook_torch_dll_fix.py',
    ],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Magic_Time_Studio_v1.9.4',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Geen consolevenster meer
    windowed=True,  # Start als echte Windows-app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets\\Magic_Time_Studio.ico',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Magic_Time_Studio_v1.9.4'
) 