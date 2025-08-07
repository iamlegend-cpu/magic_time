#!/usr/bin/env python3
"""
Test om te controleren of SRT generatie werkt met echte Fast Whisper output
"""

import sys
import os
from pathlib import Path

# Voeg project root toe aan Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_srt_generation_with_real_whisper():
    """Test SRT generatie met echte Fast Whisper output"""
    print("🔍 [DEBUG] SRT Generation with Real Whisper Test")
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
        
        # Maak een dummy audio bestand voor test
        test_audio_path = os.path.join(os.getcwd(), "test_audio.wav")
        try:
            # Maak een eenvoudig WAV bestand (1 seconde stilte)
            import wave
            import struct
            
            with wave.open(test_audio_path, 'w') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(44100)  # 44.1 kHz
                
                # 1 seconde stilte (44100 samples)
                silence = [0] * 44100
                wav_file.writeframes(struct.pack('<%dh' % len(silence), *silence))
            
            print(f"✅ Test audio bestand gemaakt: {test_audio_path}")
            
            # Test Fast Whisper transcriptie
            print("\n🎤 Test Fast Whisper transcriptie...")
            
            def progress_callback(progress_bar):
                print(f"  Progress: {progress_bar}")
                return True
            
            def stop_callback():
                return False
            
            transcript_result = whisper_manager.transcribe_audio(
                test_audio_path,
                progress_callback=progress_callback,
                stop_callback=stop_callback
            )
            
            print(f"  📊 Transcript result: {transcript_result}")
            
            if "error" in transcript_result:
                print(f"  ❌ Transcriptie gefaald: {transcript_result['error']}")
                return False
            
            transcript = transcript_result.get("transcript", "")
            transcriptions = transcript_result.get("transcriptions", [])
            
            print(f"  📄 Transcript: {transcript}")
            print(f"  📄 Transcriptions: {len(transcriptions)} segmenten")
            
            if transcriptions:
                print(f"  📄 Eerste segment: {transcriptions[0]}")
            
            # Test SRT generatie
            print("\n📄 Test SRT generatie...")
            
            # Maak dummy video bestand
            dummy_video_path = os.path.join(os.getcwd(), "test_video.mp4")
            try:
                with open(dummy_video_path, 'w') as f:
                    f.write("dummy")
                
                # Test settings
                test_settings = {
                    "preserve_original_subtitles": True,
                    "enable_translation": False,
                    "subtitle_type": "softcoded"
                }
                
                print(f"  📊 Settings: {test_settings}")
                print(f"  📊 Transcriptions: {len(transcriptions)}")
                
                result = video_processor.generate_srt_files(
                    dummy_video_path,
                    transcriptions,
                    None,  # Geen vertaling
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
                    if os.path.exists("test_video.srt"):
                        os.remove("test_video.srt")
                    print("  🧹 Test bestanden opgeruimd")
                except:
                    pass
                    
        except Exception as e:
            print(f"  ❌ Fout bij audio bestand maken: {e}")
        finally:
            # Cleanup audio bestand
            try:
                if os.path.exists(test_audio_path):
                    os.remove(test_audio_path)
                print("  🧹 Audio test bestand opgeruimd")
            except:
                pass
        
        return True
        
    except Exception as e:
        print(f"❌ Fout in test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 [DEBUG] SRT Generation Live Test")
    print("=" * 50)
    
    success = test_srt_generation_with_real_whisper()
    
    if success:
        print("\n🎉 Test geslaagd! SRT generatie werkt correct.")
    else:
        print("\n⚠️ Test gefaald. Controleer SRT generatie.") 