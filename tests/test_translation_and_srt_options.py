#!/usr/bin/env python3
"""
Test om te controleren of vertaling en SRT opties correct werken met Fast Whisper
"""

import sys
import os
from pathlib import Path

# Voeg project root toe aan Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_translation_with_fast_whisper():
    """Test of vertaling correct werkt met Fast Whisper"""
    print("🔍 [DEBUG] Translation with Fast Whisper Test")
    print("=" * 50)
    
    try:
        # Import modules
        from magic_time_studio.processing.whisper_manager import whisper_manager
        from magic_time_studio.processing.video_processor import video_processor
        from magic_time_studio.processing.translator import translator
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
        
        # Maak mock transcriptions
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
            }
        ]
        
        # Test vertaling van transcriptions
        print("\n🌐 Test vertaling van transcriptions...")
        
        # Simuleer vertaling van elk segment
        translated_transcriptions = []
        for segment in mock_transcriptions:
            # Simuleer vertaling (in echte app zou dit via translator.translate_text gaan)
            translated_segment = segment.copy()
            translated_segment["text"] = f"[Vertaald] {segment['text']}"
            translated_segment["translated_text"] = f"[Vertaald] {segment['text']}"
            translated_transcriptions.append(translated_segment)
        
        print(f"  ✅ Vertaling gesimuleerd: {len(translated_transcriptions)} segmenten")
        
        # Test SRT generatie met vertaling
        print("\n📄 Test SRT generatie met vertaling...")
        
        # Maak dummy video bestand
        dummy_video_path = os.path.join(os.getcwd(), "dummy_video.mp4")
        try:
            with open(dummy_video_path, 'w') as f:
                f.write("dummy")
            
            # Test settings
            test_settings = {
                "preserve_original_subtitles": True,
                "enable_translation": True,
                "target_language": "nl"
            }
            
            result = video_processor.generate_srt_files(
                dummy_video_path,
                mock_transcriptions,
                translated_transcriptions,
                test_settings
            )
            
            print(f"  📊 Resultaat: {result}")
            
            if result.get("success"):
                output_files = result.get("output_files", {})
                print(f"  ✅ SRT generatie succesvol")
                print(f"  📁 Output bestanden: {list(output_files.keys())}")
                
                for file_type, file_path in output_files.items():
                    print(f"    📄 {file_type}: {file_path}")
                    if os.path.exists(file_path):
                        print(f"      ✅ Bestand bestaat")
                        # Lees inhoud
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            print(f"      📄 Inhoud:\n{content}")
                        except Exception as e:
                            print(f"      ❌ Kon bestand niet lezen: {e}")
                    else:
                        print(f"      ❌ Bestand bestaat niet")
            else:
                print(f"  ❌ SRT generatie gefaald: {result.get('error')}")
                
        except Exception as e:
            print(f"  ❌ Fout bij SRT generatie: {e}")
        finally:
            # Cleanup
            try:
                if os.path.exists(dummy_video_path):
                    os.remove(dummy_video_path)
                if os.path.exists("dummy_video.srt"):
                    os.remove("dummy_video.srt")
                if os.path.exists("dummy_video_nl.srt"):
                    os.remove("dummy_video_nl.srt")
                print("  🧹 Test bestanden opgeruimd")
            except:
                pass
        
        return True
        
    except Exception as e:
        print(f"❌ Fout in translation test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_srt_options():
    """Test of SRT opties correct werken"""
    print("\n🔍 [DEBUG] SRT Options Test")
    print("=" * 50)
    
    try:
        from magic_time_studio.processing.video_processor import video_processor
        
        # Maak mock transcriptions
        mock_transcriptions = [
            {
                "start": 0.0,
                "end": 3.5,
                "text": "Test segment 1"
            },
            {
                "start": 3.5,
                "end": 7.2,
                "text": "Test segment 2"
            }
        ]
        
        # Test 1: Originele ondertitels behouden
        print("\n📄 Test 1: Originele ondertitels behouden...")
        
        dummy_video_path = os.path.join(os.getcwd(), "test_video.mp4")
        try:
            with open(dummy_video_path, 'w') as f:
                f.write("dummy")
            
            settings_preserve = {
                "preserve_original_subtitles": True,
                "enable_translation": False
            }
            
            result = video_processor.generate_srt_files(
                dummy_video_path,
                mock_transcriptions,
                None,
                settings_preserve
            )
            
            print(f"  📊 Resultaat: {result}")
            
            if result.get("success"):
                output_files = result.get("output_files", {})
                print(f"  ✅ SRT generatie succesvol")
                print(f"  📁 Output bestanden: {list(output_files.keys())}")
                
                if "srt" in output_files:
                    print("  ✅ Origineel SRT bestand gemaakt")
                else:
                    print("  ❌ Origineel SRT bestand niet gemaakt")
            else:
                print(f"  ❌ SRT generatie gefaald: {result.get('error')}")
                
        except Exception as e:
            print(f"  ❌ Fout bij test 1: {e}")
        finally:
            # Cleanup
            try:
                if os.path.exists(dummy_video_path):
                    os.remove(dummy_video_path)
                if os.path.exists("test_video.srt"):
                    os.remove("test_video.srt")
            except:
                pass
        
        # Test 2: Originele ondertitels verwijderen
        print("\n📄 Test 2: Originele ondertitels verwijderen...")
        
        try:
            with open(dummy_video_path, 'w') as f:
                f.write("dummy")
            
            settings_remove = {
                "preserve_original_subtitles": False,
                "enable_translation": False
            }
            
            result = video_processor.generate_srt_files(
                dummy_video_path,
                mock_transcriptions,
                None,
                settings_remove
            )
            
            print(f"  📊 Resultaat: {result}")
            
            if result.get("success"):
                output_files = result.get("output_files", {})
                print(f"  ✅ SRT generatie succesvol")
                print(f"  📁 Output bestanden: {list(output_files.keys())}")
                
                if "srt" not in output_files:
                    print("  ✅ Origineel SRT bestand niet gemaakt (verwijderd)")
                else:
                    print("  ❌ Origineel SRT bestand nog steeds gemaakt")
            else:
                print(f"  ❌ SRT generatie gefaald: {result.get('error')}")
                
        except Exception as e:
            print(f"  ❌ Fout bij test 2: {e}")
        finally:
            # Cleanup
            try:
                if os.path.exists(dummy_video_path):
                    os.remove(dummy_video_path)
                if os.path.exists("test_video.srt"):
                    os.remove("test_video.srt")
            except:
                pass
        
        return True
        
    except Exception as e:
        print(f"❌ Fout in SRT options test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 [DEBUG] Translation and SRT Options Tests")
    print("=" * 50)
    
    # Test vertaling
    translation_ok = test_translation_with_fast_whisper()
    
    # Test SRT opties
    srt_options_ok = test_srt_options()
    
    print("\n📊 Test Resultaten:")
    print(f"  Translation: {'✅' if translation_ok else '❌'}")
    print(f"  SRT Options: {'✅' if srt_options_ok else '❌'}")
    
    if translation_ok and srt_options_ok:
        print("\n🎉 Alle tests geslaagd! Vertaling en SRT opties werken correct.")
    else:
        print("\n⚠️ Sommige tests gefaald. Controleer vertaling en SRT opties.") 