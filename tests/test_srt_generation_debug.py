#!/usr/bin/env python3
"""
Debug test om te controleren of SRT generatie wordt aangeroepen
"""

import sys
import os
from pathlib import Path

# Voeg project root toe aan Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_srt_generation_debug():
    """Debug test voor SRT generatie"""
    print("🔍 [DEBUG] SRT Generation Debug Test")
    print("=" * 50)
    
    try:
        # Import modules
        from magic_time_studio.processing.video_processor import video_processor
        
        print("✅ Video processor geïmporteerd")
        
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
        
        # Test generate_srt_files direct via _create_srt_file
        print(f"\n📄 Test SRT generatie direct...")
        
        # Test _create_srt_file direct
        test_srt_path = os.path.join(os.getcwd(), "test_video.srt")
        
        try:
            video_processor._create_srt_file(mock_transcriptions, test_srt_path)
            print(f"✅ SRT bestand direct gemaakt: {test_srt_path}")
            
            if os.path.exists(test_srt_path):
                print(f"✅ SRT bestand bestaat")
                # Lees inhoud
                try:
                    with open(test_srt_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    print(f"📄 Inhoud:\n{content}")
                except Exception as e:
                    print(f"❌ Kon bestand niet lezen: {e}")
            else:
                print(f"❌ SRT bestand bestaat niet")
        except Exception as e:
            print(f"❌ Fout bij direct maken SRT: {e}")
        
        # Test generate_srt_files (zonder video bestand check)
        print(f"\n📄 Test generate_srt_files...")
        
        # Maak een dummy video bestand
        dummy_video_path = os.path.join(os.getcwd(), "dummy_video.mp4")
        try:
            with open(dummy_video_path, 'w') as f:
                f.write("dummy")
            
            result = video_processor.generate_srt_files(
                dummy_video_path,
                mock_transcriptions,
                None  # Geen vertaling
            )
            
            print(f"📊 Resultaat: {result}")
            
            if result.get("success"):
                output_files = result.get("output_files", {})
                print(f"✅ SRT generatie succesvol")
                print(f"📁 Output bestanden: {list(output_files.keys())}")
                
                for file_type, file_path in output_files.items():
                    print(f"  📄 {file_type}: {file_path}")
                    if os.path.exists(file_path):
                        print(f"    ✅ Bestand bestaat")
                    else:
                        print(f"    ❌ Bestand bestaat niet")
            else:
                print(f"❌ SRT generatie gefaald: {result.get('error')}")
                
        except Exception as e:
            print(f"❌ Fout bij generate_srt_files: {e}")
        finally:
            # Cleanup
            try:
                if os.path.exists(dummy_video_path):
                    os.remove(dummy_video_path)
                if os.path.exists("test_video.srt"):
                    os.remove("test_video.srt")
                if os.path.exists("dummy_video.srt"):
                    os.remove("dummy_video.srt")
                print("  🧹 Test bestanden opgeruimd")
            except:
                pass
        
        return True
        
    except Exception as e:
        print(f"❌ Fout in debug test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_settings_debug():
    """Debug test voor settings"""
    print("\n🔍 [DEBUG] Settings Debug Test")
    print("=" * 50)
    
    try:
        # Import settings panel
        from magic_time_studio.ui_pyqt6.components.settings_panel import SettingsPanel
        from magic_time_studio.core.config import config_manager
        
        print("✅ Settings panel geïmporteerd")
        
        # Laad configuratie
        config_manager.load_configuration()
        
        # Maak settings panel
        settings_panel = SettingsPanel()
        
        # Haal huidige settings op
        current_settings = settings_panel.get_current_settings()
        
        print(f"📋 Huidige settings: {current_settings}")
        
        # Check belangrijke settings voor SRT generatie
        important_settings = [
            'whisper_type',
            'whisper_model',
            'language',
            'content_type',
            'enable_translation',
            'target_language',
            'preserve_original_subtitles'
        ]
        
        print("\n🔍 Belangrijke settings:")
        for setting in important_settings:
            value = current_settings.get(setting, "Niet ingesteld")
            print(f"  {setting}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Fout in settings debug test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 [DEBUG] SRT Generation Debug Tests")
    print("=" * 50)
    
    # Test SRT generatie
    srt_ok = test_srt_generation_debug()
    
    # Test settings
    settings_ok = test_settings_debug()
    
    print("\n📊 Test Resultaten:")
    print(f"  SRT Generatie: {'✅' if srt_ok else '❌'}")
    print(f"  Settings: {'✅' if settings_ok else '❌'}")
    
    if srt_ok and settings_ok:
        print("\n🎉 Alle tests geslaagd! SRT generatie werkt correct.")
    else:
        print("\n⚠️ Sommige tests gefaald. Controleer SRT generatie.") 