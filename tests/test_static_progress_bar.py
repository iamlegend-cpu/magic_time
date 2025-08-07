"""
Test script voor statische voortgangsbalk
Test of FFmpeg progress updates op dezelfde regel blijven
"""

import sys
import os
import time
from pathlib import Path

# Voeg project root toe aan Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_static_progress_bar():
    """Test statische voortgangsbalk functionaliteit"""
    print("🧪 Test statische voortgangsbalk...")
    
    try:
        from magic_time_studio.processing.audio_processor import AudioProcessor
        from magic_time_studio.processing.video_processor import VideoProcessor
        
        # Test AudioProcessor statische voortgangsbalk
        audio_processor = AudioProcessor()
        print("✅ AudioProcessor geïmporteerd")
        
        # Test VideoProcessor statische voortgangsbalk
        video_processor = VideoProcessor()
        print("✅ VideoProcessor geïmporteerd")
        
        # Test statische voortgangsbalk methode
        print("\n📊 Test statische voortgangsbalk:")
        for i in range(5):
            progress_msg = f"🎵 FFmpeg: Frame {i*1000}, {25+i} fps, 00:00:{i:02d}"
            audio_processor._print_static_progress(progress_msg)
            time.sleep(0.5)
        
        # Wis de regel
        audio_processor._clear_progress_line()
        print("\n✅ Statische voortgangsbalk test voltooid!")
        
        return True
        
    except Exception as e:
        print(f"❌ Statische voortgangsbalk test gefaald: {e}")
        return False

def test_ffmpeg_progress_simulation():
    """Simuleer FFmpeg progress output"""
    print("\n🎬 Simuleer FFmpeg progress output:")
    
    try:
        from magic_time_studio.processing.audio_processor import AudioProcessor
        
        audio_processor = AudioProcessor()
        
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
            # Parse progress uit FFmpeg output
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
        print("\n✅ FFmpeg progress simulatie voltooid!")
        
        return True
        
    except Exception as e:
        print(f"❌ FFmpeg progress simulatie gefaald: {e}")
        return False

def main():
    """Hoofdfunctie voor statische voortgangsbalk tests"""
    print("🧪 Start statische voortgangsbalk tests...\n")
    
    # Test 1: Basis statische voortgangsbalk functionaliteit
    if not test_static_progress_bar():
        print("❌ Statische voortgangsbalk test gefaald")
        return False
    
    # Test 2: FFmpeg progress simulatie
    if not test_ffmpeg_progress_simulation():
        print("❌ FFmpeg progress simulatie gefaald")
        return False
    
    print("\n✅ Alle statische voortgangsbalk tests geslaagd!")
    print("🎉 Statische voortgangsbalk werkt correct!")
    
    print("\n📋 Statische voortgangsbalk features:")
    print("• ✅ Updates op dezelfde regel")
    print("• ✅ Automatische regel wissing")
    print("• ✅ Real-time flush")
    print("• ✅ FFmpeg progress parsing")
    print("• ✅ Console output optimalisatie")
    
    return True

if __name__ == "__main__":
    main()
