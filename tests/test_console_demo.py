#!/usr/bin/env python3
"""
Test om de statische voortgangsbalk te demonstreren in de console
"""

import sys
import time

def demo_static_progress():
    """Demonstreer statische voortgangsbalk in console"""
    print("🎬 Demo statische voortgangsbalk:")
    print("=" * 50)
    
    # Simuleer Fast Whisper progress
    print("🎤 Fast Whisper verwerking...")
    for i in range(0, 101, 5):
        progress_text = f"🎤 Fast Whisper: {i}% - video.mp4"
        print(progress_text, end="\r")
        sys.stdout.flush()
        time.sleep(0.1)
    
    print("\n✅ Fast Whisper voltooid!")
    
    # Simuleer FFmpeg progress
    print("\n🎬 FFmpeg audio extractie...")
    for i in range(0, 101, 10):
        progress_text = f"🎬 FFmpeg: {i}% - audio.mp3"
        print(progress_text, end="\r")
        sys.stdout.flush()
        time.sleep(0.2)
    
    print("\n✅ FFmpeg voltooid!")
    print("\n🎉 Demo voltooid!")

if __name__ == "__main__":
    demo_static_progress()
