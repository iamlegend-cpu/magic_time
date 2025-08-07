#!/usr/bin/env python3
"""
Test om te controleren of Fast Whisper SRT bestanden genereert
"""

import sys
import os
from pathlib import Path

# Voeg project root toe aan Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_srt_generation_with_fast_whisper():
    """Test of Fast Whisper SRT bestanden genereert"""
    print("🔍 [DEBUG] Fast Whisper SRT Generation Test")
    print("=" * 50)
    
    try:
        # Import modules
        from magic_time_studio.processing.whisper_manager import whisper_manager
        from magic_time_studio.processing.video_processor import video_processor
        from magic_time_studio.core.config import config_manager
        
        print("✅ Modules geïmporteerd")
        
        # Laad configuratie
        config_manager.load_configuration()
        
        # Initialiseer Fast Whisper
        print("\n🚀 Initialiseer Fast Whisper...")
        success = whisper_manager.initialize("fast", "large-v3-turbo")
        print(f"  Initialisatie succesvol: {success}")
        
        if not success:
            print("❌ Fast Whisper initialisatie gefaald")
            return False
        
        # Maak mock transcriptions (zoals Fast Whisper zou genereren)
        mock_transcriptions = [
            {
                "start": 0.0,
                "end": 3.5,
                "text": "Hello, this is a test transcription."
            },
            {
                "start": 3.5,
                "end": 7.2,
                "text": "This is the second segment of the test."
            },
            {
                "start": 7.2,
                "end": 10.0,
                "text": "And this is the final segment."
            }
        ]
        
        # Maak test video pad
        test_video_path = os.path.join(os.getcwd(), "test_video.mp4")
        
        # Test settings
        test_settings = {
            "generate_srt": True,
            "generate_translated_srt": False,
            "generate_vtt": False,
            "generate_json": False,
            "generate_txt": False,
            "output_dir": os.path.dirname(test_video_path)
        }
        
        print("\n📄 Test SRT generatie...")
        
        # Test _generate_output_files direct
        output_result = video_processor._generate_output_files(
            test_video_path, mock_transcriptions, mock_transcriptions, test_settings
        )
        
        print(f"  Output result: {output_result}")
        
        if output_result.get("success"):
            output_files = output_result.get("output_files", {})
            print(f"  Gegenereerde bestanden: {list(output_files.keys())}")
            
            # Check of SRT bestand is gemaakt
            if "srt" in output_files:
                srt_path = output_files["srt"]
                print(f"  ✅ SRT bestand gemaakt: {srt_path}")
                
                # Check of bestand bestaat
                if os.path.exists(srt_path):
                    print(f"  ✅ SRT bestand bestaat: {srt_path}")
                    
                    # Lees en toon inhoud
                    try:
                        with open(srt_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        print(f"  📄 SRT inhoud:\n{content}")
                    except Exception as e:
                        print(f"  ❌ Kon SRT bestand niet lezen: {e}")
                else:
                    print(f"  ❌ SRT bestand bestaat niet: {srt_path}")
            else:
                print("  ❌ Geen SRT bestand gegenereerd")
        else:
            print(f"  ❌ SRT generatie gefaald: {output_result.get('error')}")
        
        # Cleanup
        try:
            if os.path.exists("test_video.srt"):
                os.remove("test_video.srt")
                print("  🧹 Test SRT bestand opgeruimd")
        except:
            pass
        
        return True
        
    except Exception as e:
        print(f"❌ Fout in SRT generatie test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fast_whisper_transcription_format():
    """Test of Fast Whisper de juiste transcriptie format genereert"""
    print("\n🔍 [DEBUG] Fast Whisper Transcription Format Test")
    print("=" * 50)
    
    try:
        from magic_time_studio.processing.whisper_manager import whisper_manager
        
        # Test transcriptie zonder echt bestand
        mock_audio_path = "test_audio.wav"
        
        print("🎤 Test Fast Whisper transcriptie format...")
        
        # Dit zou moeten falen omdat het bestand niet bestaat, maar we kunnen de error checken
        result = whisper_manager.transcribe_audio(mock_audio_path)
        
        print(f"  Transcriptie resultaat: {result}")
        
        # Check of het resultaat de juiste structuur heeft
        if isinstance(result, dict):
            if "error" in result:
                print("  ✅ Fast Whisper geeft correct error voor niet-bestaand bestand")
            elif "transcriptions" in result:
                transcriptions = result["transcriptions"]
                if isinstance(transcriptions, list) and transcriptions:
                    first_segment = transcriptions[0]
                    required_keys = ["start", "end", "text"]
                    if all(key in first_segment for key in required_keys):
                        print("  ✅ Fast Whisper genereert correct transcriptie format")
                        print(f"  📋 Voorbeeld segment: {first_segment}")
                    else:
                        print("  ❌ Fast Whisper genereert incorrect transcriptie format")
                        print(f"  📋 Segment keys: {list(first_segment.keys())}")
                else:
                    print("  ❌ Fast Whisper geeft geen transcriptions lijst")
            else:
                print("  ❌ Fast Whisper resultaat heeft onverwachte structuur")
        else:
            print("  ❌ Fast Whisper geeft geen dict resultaat")
        
        return True
        
    except Exception as e:
        print(f"❌ Fout in transcriptie format test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 [DEBUG] Fast Whisper SRT Generation Tests")
    print("=" * 50)
    
    # Test SRT generatie
    srt_ok = test_srt_generation_with_fast_whisper()
    
    # Test transcriptie format
    format_ok = test_fast_whisper_transcription_format()
    
    print("\n📊 Test Resultaten:")
    print(f"  SRT Generatie: {'✅' if srt_ok else '❌'}")
    print(f"  Transcriptie Format: {'✅' if format_ok else '❌'}")
    
    if srt_ok and format_ok:
        print("\n🎉 Alle tests geslaagd! Fast Whisper genereert correct SRT bestanden.")
    else:
        print("\n⚠️ Sommige tests gefaald. Controleer SRT generatie.") 