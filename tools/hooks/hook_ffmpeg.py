"""
Hook voor FFmpeg in PyInstaller
Zorgt ervoor dat FFmpeg correct wordt meegenomen in de exe
"""

import os
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

# Voeg ffmpeg.exe toe aan de binaries
binaries = []

# Zoek ffmpeg.exe in verschillende locaties
possible_ffmpeg_paths = [
    os.path.join(os.path.dirname(__file__), '..', 'assets', 'ffmpeg.exe'),
    os.path.join(os.getcwd(), 'assets', 'ffmpeg.exe'),
    'assets/ffmpeg.exe',
]

for ffmpeg_path in possible_ffmpeg_paths:
    if os.path.exists(ffmpeg_path):
        print(f"✅ FFmpeg gevonden: {ffmpeg_path}")
        binaries.append((ffmpeg_path, '.'))
        break
else:
    print("⚠️ FFmpeg niet gevonden in assets directory")

# Hook functie voor PyInstaller
def hook_ffmpeg(hook_api):
    """Hook voor FFmpeg"""
    for ffmpeg_path in possible_ffmpeg_paths:
        if os.path.exists(ffmpeg_path):
            hook_api.add_binaries([(ffmpeg_path, '.')])
            print(f"✅ FFmpeg toegevoegd aan bundle: {ffmpeg_path}")
            break
    else:
        print("⚠️ FFmpeg niet gevonden voor bundle") 