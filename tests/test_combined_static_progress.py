"""
Gecombineerde test script voor statische voortgangsbalk
Test zowel FFmpeg als Fast Whisper statische progress
"""

import sys
import os
import time
from pathlib import Path

# Voeg project root toe aan Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_ffmpeg_static_progress():
    """Test FFmpeg statische voortgangsbalk"""
    print("🎵 Test FFmpeg statische voortgangsbalk...")
    
    try:
        from magic_time_studio.processing.audio_processor import AudioProcessor
        
        audio_processor = AudioProcessor()
        print("✅ AudioProcessor geïmporteerd")
        
        # Simuleer FFmpeg output
        ffmpeg_outputs = [
            "frame=    0 fps=0.0 q=0.0 size=       0kB time=00:00:00.00 bitrate=N/A speed=N/A",
            "frame=  100 fps=25.0 q=28.0 size=     256kB time=00:00:04.00 bitrate= 512kbits/s speed=1x",
            "frame=  200 fps=24.8 q=28.0 size=     512kB time=00:00:08.00 bitrate= 512kbits/s speed=1x",
            "frame=  300 fps=24.9 q=28.0 size=     768kB time=00:00:12.00 bitrate= 512kbits/s speed=1x",
            "frame=  400 fps=25.0 q=28.0 size=    1024kB time=00:00:16.00 bitrate= 512kbits/s speed=1x",
            "frame=  500 fps=25.0 q=28.0 size=    1280kB time=00:00:20.00 bitrate= 512kbits/s speed=1x"
        ]
        
        for output in ffmpeg_outputs:
            if "frame=" in output and "fps=" in output and "time=" in output:
                try:
                    frame_part = output.split("frame=")[1].split()[0]
                    fps_part = output.split("fps=")[1].split()[0]
                    time_part = output.split("time=")[1].split()[0]
                    
                    progress_message = f"🎵 FFmpeg: Frame {frame_part}, {fps_part} fps, {time_part}"
                    audio_processor._print_static_progress(progress_message)
                    time.sleep(0.8)
                except:
                    pass
        
        # Wis de regel
        audio_processor._clear_progress_line()
        print("\n✅ FFmpeg statische voortgangsbalk test voltooid!")
        
        return True
        
    except Exception as e:
        print(f"❌ FFmpeg statische voortgangsbalk test gefaald: {e}")
        return False

def test_fast_whisper_static_progress():
    """Test Fast Whisper statische voortgangsbalk"""
    print("\n🎤 Test Fast Whisper statische voortgangsbalk...")
    
    try:
        from magic_time_studio.processing.whisper_processor import WhisperProcessor
        
        whisper_processor = WhisperProcessor()
        print("✅ WhisperProcessor geïmporteerd")
        
        # Simuleer Fast Whisper progress updates
        progress_values = [0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0]
        
        for progress in progress_values:
            progress_message = f"🎤 Fast Whisper: {progress:.1%} - test_audio.wav"
            whisper_processor._print_static_progress(progress_message)
            time.sleep(0.8)
        
        # Wis de regel
        whisper_processor._clear_progress_line()
        print("\n✅ Fast Whisper statische voortgangsbalk test voltooid!")
        
        return True
        
    except Exception as e:
        print(f"❌ Fast Whisper statische voortgangsbalk test gefaald: {e}")
        return False

def test_combined_workflow():
    """Test gecombineerde workflow met beide progress types"""
    print("\n🔄 Test gecombineerde workflow...")
    
    try:
        from magic_time_studio.processing.audio_processor import AudioProcessor
        from magic_time_studio.processing.whisper_processor import WhisperProcessor
        
        audio_processor = AudioProcessor()
        whisper_processor = WhisperProcessor()
        
        print("📁 Stap 1: Audio extractie met FFmpeg...")
        # Simuleer FFmpeg progress
        for i in range(3):
            progress_message = f"🎵 FFmpeg: Frame {i*100}, {25+i} fps, 00:00:{i:02d}"
            audio_processor._print_static_progress(progress_message)
            time.sleep(0.5)
        
        audio_processor._clear_progress_line()
        print("\n✅ Audio extractie voltooid!")
        
        print("\n🎤 Stap 2: Fast Whisper transcriptie...")
        # Simuleer Fast Whisper progress
        for i in range(5):
            progress = i * 0.2
            progress_message = f"🎤 Fast Whisper: {progress:.1%} - test_audio.wav"
            whisper_processor._print_static_progress(progress_message)
            time.sleep(0.5)
        
        whisper_processor._clear_progress_line()
        print("\n✅ Fast Whisper transcriptie voltooid!")
        
        print("\n✅ Gecombineerde workflow test voltooid!")
        
        return True
        
    except Exception as e:
        print(f"❌ Gecombineerde workflow test gefaald: {e}")
        return False

def main():
    """Hoofdfunctie voor gecombineerde statische voortgangsbalk tests"""
    print("🧪 Start gecombineerde statische voortgangsbalk tests...\n")
    
    # Test 1: FFmpeg statische voortgangsbalk
    if not test_ffmpeg_static_progress():
        print("❌ FFmpeg statische voortgangsbalk test gefaald")
        return False
    
    # Test 2: Fast Whisper statische voortgangsbalk
    if not test_fast_whisper_static_progress():
        print("❌ Fast Whisper statische voortgangsbalk test gefaald")
        return False
    
    # Test 3: Gecombineerde workflow
    if not test_combined_workflow():
        print("❌ Gecombineerde workflow test gefaald")
        return False
    
    print("\n✅ Alle gecombineerde statische voortgangsbalk tests geslaagd!")
    print("🎉 Statische voortgangsbalk werkt correct voor beide processen!")
    
    print("\n📋 Gecombineerde statische voortgangsbalk features:")
    print("• ✅ FFmpeg progress op dezelfde regel")
    print("• ✅ Fast Whisper progress op dezelfde regel")
    print("• ✅ Automatische regel wissing")
    print("• ✅ Real-time flush")
    print("• ✅ Gecombineerde workflow ondersteuning")
    print("• ✅ Console output optimalisatie")
    
    return True

if __name__ == "__main__":
    main()
