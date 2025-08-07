#!/usr/bin/env python3
"""
Test om te controleren of SRT bestanden in de juiste directory worden gegenereerd
"""

import sys
import os
from pathlib import Path

# Voeg project root toe aan Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_srt_output_directory():
    """Test of SRT bestanden in de juiste directory worden gegenereerd"""
    print("🔍 [DEBUG] SRT Output Directory Test")
    print("=" * 50)
    
    try:
        from magic_time_studio.processing.video_processor import video_processor
        
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
        
        # Test met een video pad dat spaties en speciale karakters bevat
        test_video_path = r"D:\Films & Serie\Film\test_video.mp4"
        
        # Maak dummy video bestand
        try:
            # Maak directory als deze niet bestaat
            os.makedirs(os.path.dirname(test_video_path), exist_ok=True)
            
            with open(test_video_path, 'w') as f:
                f.write("dummy")
            
            print(f"✅ Test video bestand gemaakt: {test_video_path}")
            
            # Test settings
            test_settings = {
                "preserve_original_subtitles": True,
                "enable_translation": False,
                "subtitle_type": "softcoded"
            }
            
            print(f"📊 Settings: {test_settings}")
            print(f"📊 Video path: {test_video_path}")
            print(f"📊 Expected output dir: {os.path.dirname(test_video_path)}")
            
            result = video_processor.generate_srt_files(
                test_video_path,
                mock_transcriptions,
                None,  # Geen vertaling
                test_settings
            )
            
            print(f"📊 Resultaat: {result}")
            
            if result.get("success"):
                output_files = result.get("output_files", {})
                print(f"✅ SRT generatie succesvol")
                print(f"📁 Output bestanden: {list(output_files.keys())}")
                
                for file_type, file_path in output_files.items():
                    print(f"  📄 {file_type}: {file_path}")
                    print(f"    📁 Directory: {os.path.dirname(file_path)}")
                    print(f"    📁 Expected: {os.path.dirname(test_video_path)}")
                    
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
                    
                    # Controleer of bestand in juiste directory staat
                    expected_dir = os.path.dirname(test_video_path)
                    actual_dir = os.path.dirname(file_path)
                    
                    if expected_dir == actual_dir:
                        print(f"      ✅ Bestand staat in juiste directory")
                    else:
                        print(f"      ❌ Bestand staat in verkeerde directory")
                        print(f"         Verwacht: {expected_dir}")
                        print(f"         Werkelijk: {actual_dir}")
            else:
                print(f"❌ SRT generatie gefaald: {result.get('error')}")
                
        except Exception as e:
            print(f"❌ Fout bij test: {e}")
        finally:
            # Cleanup
            try:
                if os.path.exists(test_video_path):
                    os.remove(test_video_path)
                # Verwijder gegenereerde SRT bestanden
                expected_srt_path = os.path.join(os.path.dirname(test_video_path), "test_video.srt")
                if os.path.exists(expected_srt_path):
                    os.remove(expected_srt_path)
                print("🧹 Test bestanden opgeruimd")
            except:
                pass
        
        return True
        
    except Exception as e:
        print(f"❌ Fout in test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 [DEBUG] SRT Output Directory Test")
    print("=" * 50)
    
    success = test_srt_output_directory()
    
    if success:
        print("\n🎉 Test geslaagd! SRT bestanden worden in juiste directory gegenereerd.")
    else:
        print("\n⚠️ Test gefaald. Controleer SRT output directory.") 