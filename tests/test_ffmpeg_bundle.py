#!/usr/bin/env python3
"""
Test script om te controleren of ffmpeg correct wordt gevonden in de bundle
"""

import os
import sys
import subprocess

def test_ffmpeg_finding():
    """Test ffmpeg finding logic"""
    print("🔍 Test ffmpeg finding...")
    
    # Test bundle directory detection
    if getattr(sys, 'frozen', False):
        bundle_dir = os.path.dirname(sys.executable)
        print(f"📦 Bundle directory: {bundle_dir}")
    else:
        bundle_dir = os.getcwd()
        print(f"📁 Development directory: {bundle_dir}")
    
    # Test possible ffmpeg locations
    possible_paths = [
        "ffmpeg",
        "ffmpeg.exe",
        os.path.join(bundle_dir, "ffmpeg.exe"),
        os.path.join(bundle_dir, "assets", "ffmpeg.exe"),
    ]
    
    found_ffmpeg = None
    for path in possible_paths:
        print(f"🔍 Checking: {path}")
        if os.path.exists(path):
            print(f"✅ File exists: {path}")
            try:
                result = subprocess.run([path, "-version"], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(f"✅ FFmpeg works: {path}")
                    found_ffmpeg = path
                    break
                else:
                    print(f"❌ FFmpeg failed: {result.stderr}")
            except Exception as e:
                print(f"❌ FFmpeg error: {e}")
        else:
            print(f"❌ File not found: {path}")
    
    if found_ffmpeg:
        print(f"🎉 FFmpeg found and working: {found_ffmpeg}")
        return True
    else:
        print("❌ FFmpeg not found or not working")
        return False

if __name__ == "__main__":
    success = test_ffmpeg_finding()
    sys.exit(0 if success else 1) 