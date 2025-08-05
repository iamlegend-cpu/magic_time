#!/usr/bin/env python3
"""
Build script voor Magic Time Studio exe
Zorgt ervoor dat ffmpeg correct wordt meegenomen
"""

import os
import sys
import subprocess
import shutil

def check_ffmpeg():
    """Controleer of ffmpeg aanwezig is"""
    print("🔍 Controleren of ffmpeg aanwezig is...")
    
    ffmpeg_path = os.path.join("assets", "ffmpeg.exe")
    if os.path.exists(ffmpeg_path):
        print(f"✅ FFmpeg gevonden: {ffmpeg_path}")
        return True
    else:
        print(f"❌ FFmpeg niet gevonden: {ffmpeg_path}")
        return False

def build_exe():
    """Bouw de exe met PyInstaller"""
    print("🔨 Starten van exe build...")
    
    # Controleer of ffmpeg aanwezig is
    if not check_ffmpeg():
        print("❌ Kan niet bouwen zonder ffmpeg")
        return False
    
    # PyInstaller commando
    cmd = [
        "pyinstaller",
        "--clean",
        "--noconfirm",
        "magic_time_studio.spec"
    ]
    
    print(f"🚀 Uitvoeren: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Exe build succesvol!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build gefaald: {e}")
        print(f"Stderr: {e.stderr}")
        return False

def test_exe():
    """Test de gebouwde exe"""
    print("🧪 Testen van gebouwde exe...")
    
    exe_path = os.path.join("dist", "Magic_Time_Studio", "Magic_Time_Studio.exe")
    if not os.path.exists(exe_path):
        print(f"❌ Exe niet gevonden: {exe_path}")
        return False
    
    print(f"✅ Exe gevonden: {exe_path}")
    
    # Test ffmpeg in de bundle
    bundle_dir = os.path.join("dist", "Magic_Time_Studio")
    ffmpeg_in_bundle = os.path.join(bundle_dir, "ffmpeg.exe")
    
    if os.path.exists(ffmpeg_in_bundle):
        print(f"✅ FFmpeg in bundle: {ffmpeg_in_bundle}")
        return True
    else:
        print(f"❌ FFmpeg niet in bundle: {ffmpeg_in_bundle}")
        return False

def main():
    """Hoofdfunctie"""
    print("🚀 Magic Time Studio Exe Builder")
    print("=" * 40)
    
    # Stap 1: Controleer ffmpeg
    if not check_ffmpeg():
        return False
    
    # Stap 2: Bouw exe
    if not build_exe():
        return False
    
    # Stap 3: Test exe
    if not test_exe():
        return False
    
    print("🎉 Build en test succesvol!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 