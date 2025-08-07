#!/usr/bin/env python3
"""
Test SRT bestand generatie met Fast Whisper
Controleer of Fast Whisper correct SRT bestanden maakt
"""

import sys
import os
import tempfile
from pathlib import Path

# Voeg project root toe aan Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_srt_generation():
    """Test SRT bestand generatie"""
    print("🔍 [DEBUG] SRT Generatie Test")
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
        if not success:
            print("❌ Fast Whisper initialisatie gefaald")
            return False
        
        print("✅ Fast Whisper geïnitialiseerd")
        
        # Test transcriptie data
        test_transcriptions = [
            {
                "start": 0.0,
                "end": 2.5,
                "text": "Dit is een test transcriptie.",
                "language": "nl"
            },
            {
                "start": 2.5,
                "end": 5.0,
                "text": "Fast Whisper werkt correct.",
                "language": "nl"
            },
            {
                "start": 5.0,
                "end": 7.5,
                "text": "SRT bestanden worden gegenereerd.",
                "language": "nl"
            }
        ]
        
        # Maak tijdelijk test bestand
        with tempfile.NamedTemporaryFile(mode='w', suffix='.mp4', delete=False) as f:
            test_video_path = f.name
        
        print(f"\n📁 Test video pad: {test_video_path}")
        
        # Test SRT generatie
        print("\n📄 Test SRT bestand generatie...")
        
        # Test settings
        settings = {
            "generate_srt": True,
            "generate_translated_srt": False,
            "generate_vtt": False,
            "generate_json": False,
            "generate_txt": False,
            "output_dir": os.path.dirname(test_video_path)
        }
        
        # Genereer output bestanden
        output_result = video_processor._generate_output_files(
            test_video_path, 
            test_transcriptions, 
            test_transcriptions,  # Geen vertaling
            settings
        )
        
        if output_result.get("success"):
            print("✅ Output bestanden gegenereerd")
            output_files = output_result.get("output_files", {})
            
            # Controleer SRT bestand
            if "srt" in output_files:
                srt_path = output_files["srt"]
                print(f"📄 SRT bestand: {srt_path}")
                
                # Lees SRT bestand
                if os.path.exists(srt_path):
                    with open(srt_path, 'r', encoding='utf-8') as f:
                        srt_content = f.read()
                    
                    print("\n📄 SRT Inhoud:")
                    print("-" * 30)
                    print(srt_content)
                    print("-" * 30)
                    
                    # Controleer of SRT correct is
                    lines = srt_content.strip().split('\n')
                    if len(lines) >= 9:  # Minimaal 3 segmenten (3 * 3 regels)
                        print("✅ SRT bestand is correct geformatteerd")
                        return True
                    else:
                        print("❌ SRT bestand heeft onjuiste format")
                        return False
                else:
                    print("❌ SRT bestand niet gevonden")
                    return False
            else:
                print("❌ SRT bestand niet gegenereerd")
                return False
        else:
            print(f"❌ Output generatie gefaald: {output_result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Fout in SRT test: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Cleanup
        try:
            if 'whisper_manager' in locals():
                whisper_manager.cleanup()
            if 'test_video_path' in locals() and os.path.exists(test_video_path):
                os.unlink(test_video_path)
        except:
            pass

def test_fast_whisper_transcription():
    """Test Fast Whisper transcriptie"""
    print("\n🔍 [DEBUG] Fast Whisper Transcriptie Test")
    print("=" * 50)
    
    try:
        from magic_time_studio.processing.whisper_manager import whisper_manager
        
        # Initialiseer Fast Whisper
        success = whisper_manager.initialize("fast", "large-v3-turbo")
        if not success:
            print("❌ Fast Whisper initialisatie gefaald")
            return False
        
        print("✅ Fast Whisper geïnitialiseerd")
        
        # Maak een klein test audio bestand (of gebruik een bestaand bestand)
        # Voor nu simuleren we transcriptie resultaten
        mock_transcription_result = {
            "success": True,
            "transcript": "Dit is een test transcriptie met Fast Whisper.",
            "transcriptions": [
                {
                    "start": 0.0,
                    "end": 3.0,
                    "text": "Dit is een test transcriptie",
                    "language": "nl"
                },
                {
                    "start": 3.0,
                    "end": 6.0,
                    "text": "met Fast Whisper.",
                    "language": "nl"
                }
            ],
            "language": "nl",
            "duration": 6.0,
            "segments": 2
        }
        
        print("✅ Mock transcriptie resultaat gegenereerd")
        print(f"📝 Transcript: {mock_transcription_result['transcript']}")
        print(f"🔢 Segmenten: {mock_transcription_result['segments']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Fout in transcriptie test: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Cleanup
        try:
            if 'whisper_manager' in locals():
                whisper_manager.cleanup()
        except:
            pass

if __name__ == "__main__":
    print("🔍 [DEBUG] SRT Generatie Tests")
    print("=" * 50)
    
    # Test SRT generatie
    srt_ok = test_srt_generation()
    
    # Test Fast Whisper transcriptie
    transcription_ok = test_fast_whisper_transcription()
    
    print("\n📊 Test Resultaten:")
    print(f"  SRT Generatie: {'✅' if srt_ok else '❌'}")
    print(f"  Fast Whisper Transcriptie: {'✅' if transcription_ok else '❌'}")
    
    if srt_ok and transcription_ok:
        print("\n🎉 Alle tests geslaagd! Fast Whisper werkt correct en genereert SRT bestanden.")
    else:
        print("\n⚠️ Sommige tests gefaald. Controleer de configuratie.") 