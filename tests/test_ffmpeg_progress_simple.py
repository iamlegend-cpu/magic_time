#!/usr/bin/env python3
"""
Eenvoudige FFmpeg voortgangsbalk test
Toon alleen FFmpeg voortgang zonder test bestanden
"""

import os
import sys
from pathlib import Path

# Voeg project root toe aan Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_ffmpeg_progress_simple():
    """Test FFmpeg voortgangsbalk met eenvoudige audio conversie"""
    try:
        from magic_time_studio.processing.audio_processor import AudioProcessor
        
        # Maak audio processor
        audio_processor = AudioProcessor()
        
        if not audio_processor.ffmpeg_path:
            print("❌ FFmpeg niet gevonden")
            return False
        
        print("✅ FFmpeg gevonden")
        print(f"📁 FFmpeg pad: {audio_processor.ffmpeg_path}")
        
        # Maak een eenvoudige test audio met FFmpeg
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            test_audio_path = temp_file.name
        
        # FFmpeg commando om een test toon te maken
        cmd = [
            audio_processor.ffmpeg_path,
            "-f", "lavfi",
            "-i", "sine=frequency=1000:duration=3",
            "-ar", "16000",
            "-ac", "1",
            test_audio_path
        ]
        
        print(f"\n🎵 Maak test audio bestand (3 seconden)...")
        print(f"📁 Output: {test_audio_path}")
        
        import subprocess
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0 or not os.path.exists(test_audio_path):
            print(f"❌ Fout bij maken test audio: {result.stderr}")
            return False
        
        print("✅ Test audio bestand gemaakt")
        print(f"📊 Audio grootte: {os.path.getsize(test_audio_path)} bytes")
        
        # Test audio extractie met voortgangsbalk
        print(f"\n🎵 Start audio extractie met voortgangsbalk...")
        
        def progress_callback(progress, message):
            print(f"📊 FFmpeg Progress: {message}")
            return True  # Ga door
        
        audio_result = audio_processor.extract_audio_from_video(
            test_audio_path,  # Gebruik het audio bestand als "video" input
            output_dir=os.path.dirname(test_audio_path),
            audio_format="wav",
            progress_callback=progress_callback
        )
        
        if audio_result.get("success"):
            print("✅ Audio extractie succesvol!")
            print(f"📁 Audio bestand: {audio_result.get('audio_path')}")
            print(f"📊 Audio grootte: {os.path.getsize(audio_result.get('audio_path'))} bytes")
            
            # Cleanup
            try:
                os.unlink(test_audio_path)
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

def main():
    """Hoofdfunctie"""
    print("🎬 Start eenvoudige FFmpeg voortgang test...\n")
    
    # Test FFmpeg voortgang
    print("=" * 50)
    print("TEST: FFmpeg Voortgangsbalk")
    print("=" * 50)
    if not test_ffmpeg_progress_simple():
        print("❌ FFmpeg voortgang test gefaald")
        return False
    
    print("\n" + "=" * 50)
    print("✅ FFmpeg voortgangsbalk test geslaagd!")
    print("🎉 FFmpeg voortgangsbalk werkt correct!")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 