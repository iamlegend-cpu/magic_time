#!/usr/bin/env python3
"""
Test script om te controleren of ffmpeg correct werkt in de gebouwde exe
"""

import os
import sys
import subprocess

def test_exe_ffmpeg():
    """Test ffmpeg in de gebouwde exe"""
    print("🧪 Test ffmpeg in gebouwde exe...")
    
    # Pad naar de exe directory
    exe_dir = os.path.join("dist", "Magic_Time_Studio")
    ffmpeg_path = os.path.join(exe_dir, "_internal", "ffmpeg.exe")
    
    print(f"📁 Exe directory: {exe_dir}")
    print(f"🔍 FFmpeg pad: {ffmpeg_path}")
    
    # Controleer of ffmpeg bestaat
    if not os.path.exists(ffmpeg_path):
        print(f"❌ FFmpeg niet gevonden: {ffmpeg_path}")
        return False
    
    print(f"✅ FFmpeg gevonden: {ffmpeg_path}")
    
    # Test ffmpeg functionaliteit
    try:
        result = subprocess.run([ffmpeg_path, "-version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ FFmpeg werkt correct!")
            print(f"📄 Versie info: {result.stdout[:200]}...")
            return True
        else:
            print(f"❌ FFmpeg fout: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ FFmpeg test fout: {e}")
        return False

def test_exe_structure():
    """Test de structuur van de gebouwde exe"""
    print("📦 Test exe structuur...")
    
    exe_dir = os.path.join("dist", "Magic_Time_Studio")
    
    # Controleer belangrijke bestanden
    important_files = [
        "Magic_Time_Studio.exe",
        "_internal/ffmpeg.exe",
        "_internal/assets/",
    ]
    
    for file_path in important_files:
        full_path = os.path.join(exe_dir, file_path)
        if os.path.exists(full_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} niet gevonden")
            return False
    
    return True

def main():
    """Hoofdfunctie"""
    print("🚀 Magic Time Studio Exe FFmpeg Test")
    print("=" * 40)
    
    # Test 1: Exe structuur
    if not test_exe_structure():
        return False
    
    # Test 2: FFmpeg functionaliteit
    if not test_exe_ffmpeg():
        return False
    
    print("🎉 Alle tests geslaagd!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 