#!/usr/bin/env python3
"""
Test FFmpeg voortgangsbalk
Toon alleen FFmpeg voortgang zonder Whisper
"""

import os
import sys
import tempfile
from pathlib import Path

# Voeg project root toe aan Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_ffmpeg_progress():
    """Test FFmpeg voortgangsbalk"""
    try:
        from magic_time_studio.processing.audio_processor import AudioProcessor
        
        # Maak audio processor
        audio_processor = AudioProcessor()
        
        if not audio_processor.ffmpeg_path:
            print("❌ FFmpeg niet gevonden")
            return False
        
        print("✅ FFmpeg gevonden")
        print(f"📁 FFmpeg pad: {audio_processor.ffmpeg_path}")
        
        # Maak een test video bestand
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
            test_video_path = temp_file.name
        
        # Maak een eenvoudige test video met FFmpeg
        cmd = [
            audio_processor.ffmpeg_path,
            "-f", "lavfi",
            "-i", "testsrc=duration=5:size=320x240:rate=1",
            "-f", "lavfi",
            "-i", "sine=frequency=1000:duration=5",
            "-c:v", "libx264",
            "-c:a", "aac",
            "-shortest",
            test_video_path
        ]
        
        print(f"\n🎬 Maak test video bestand...")
        print(f"📁 Output: {test_video_path}")
        
        import subprocess
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0 or not os.path.exists(test_video_path):
            print(f"❌ Fout bij maken test video: {result.stderr}")
            return False
        
        print("✅ Test video bestand gemaakt")
        print(f"📊 Video grootte: {os.path.getsize(test_video_path)} bytes")
        
        # Test audio extractie met voortgangsbalk
        print(f"\n🎵 Start audio extractie met voortgangsbalk...")
        
        def progress_callback(progress, message):
            print(f"📊 FFmpeg Progress: {progress:.1%} - {message}")
            return True  # Ga door
        
        audio_result = audio_processor.extract_audio_from_video(
            test_video_path,
            output_dir=os.path.dirname(test_video_path),
            audio_format="wav",
            progress_callback=progress_callback
        )
        
        if audio_result.get("success"):
            print("✅ Audio extractie succesvol!")
            print(f"📁 Audio bestand: {audio_result.get('audio_path')}")
            print(f"📊 Audio grootte: {os.path.getsize(audio_result.get('audio_path'))} bytes")
            
            # Cleanup
            try:
                os.unlink(test_video_path)
                os.unlink(audio_result.get('audio_path'))
                print("🧹 Test bestanden opgeruimd")
            except:
                pass
            
            return True
        else:
            print(f"❌ Audio extractie gefaald: {audio_result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ FFmpeg voortgang test gefaald: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ffmpeg_progress_detailed():
    """Test gedetailleerde FFmpeg voortgang"""
    try:
        from magic_time_studio.processing.audio_processor import AudioProcessor
        
        # Maak audio processor
        audio_processor = AudioProcessor()
        
        if not audio_processor.ffmpeg_path:
            print("❌ FFmpeg niet gevonden")
            return False
        
        # Maak een test video bestand
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
            test_video_path = temp_file.name
        
        # Maak een langere test video voor betere voortgang
        cmd = [
            audio_processor.ffmpeg_path,
            "-f", "lavfi",
            "-i", "testsrc=duration=10:size=640x480:rate=30",
            "-f", "lavfi",
            "-i", "sine=frequency=1000:duration=10",
            "-c:v", "libx264",
            "-c:a", "aac",
            "-shortest",
            test_video_path
        ]
        
        print(f"\n🎬 Maak langere test video (10 seconden)...")
        
        import subprocess
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0 or not os.path.exists(test_video_path):
            print(f"❌ Fout bij maken test video: {result.stderr}")
            return False
        
        print("✅ Test video bestand gemaakt")
        print(f"📊 Video grootte: {os.path.getsize(test_video_path)} bytes")
        
        # Test audio extractie met gedetailleerde voortgang
        print(f"\n🎵 Start gedetailleerde audio extractie...")
        
        progress_updates = []
        
        def detailed_progress_callback(progress, message):
            progress_updates.append((progress, message))
            print(f"📊 FFmpeg: {progress:.1%} - {message}")
            return True
        
        audio_result = audio_processor.extract_audio_from_video(
            test_video_path,
            output_dir=os.path.dirname(test_video_path),
            audio_format="wav",
            progress_callback=detailed_progress_callback
        )
        
        if audio_result.get("success"):
            print("✅ Audio extractie succesvol!")
            print(f"📊 Aantal voortgang updates: {len(progress_updates)}")
            
            # Toon voortgang details
            if progress_updates:
                print("\n📋 Voortgang details:")
                for i, (progress, message) in enumerate(progress_updates):
                    print(f"  {i+1:2d}. {progress:.1%} - {message}")
            
            # Cleanup
            try:
                os.unlink(test_video_path)
                os.unlink(audio_result.get('audio_path'))
                print("🧹 Test bestanden opgeruimd")
            except:
                pass
            
            return True
        else:
            print(f"❌ Audio extractie gefaald: {audio_result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Gedetailleerde FFmpeg voortgang test gefaald: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Hoofdfunctie"""
    print("🎬 Start FFmpeg voortgang tests...\n")
    
    # Test 1: Basis FFmpeg voortgang
    print("=" * 50)
    print("TEST 1: Basis FFmpeg Voortgang")
    print("=" * 50)
    if not test_ffmpeg_progress():
        print("❌ Basis FFmpeg voortgang test gefaald")
        return False
    
    # Test 2: Gedetailleerde FFmpeg voortgang
    print("\n" + "=" * 50)
    print("TEST 2: Gedetailleerde FFmpeg Voortgang")
    print("=" * 50)
    if not test_ffmpeg_progress_detailed():
        print("❌ Gedetailleerde FFmpeg voortgang test gefaald")
        return False
    
    print("\n" + "=" * 50)
    print("✅ Alle FFmpeg voortgang tests geslaagd!")
    print("🎉 FFmpeg voortgangsbalk werkt correct!")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 