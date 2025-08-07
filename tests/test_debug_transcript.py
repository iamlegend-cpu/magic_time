#!/usr/bin/env python3
"""
Test om te controleren wat er gebeurt met de transcript_result na Fast Whisper
"""

import sys
import os
from pathlib import Path

# Voeg project root toe aan Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_debug_transcript():
    """Test wat er gebeurt met de transcript_result"""
    print("🔍 [DEBUG] Debug Transcript Test")
    print("=" * 50)
    
    try:
        from magic_time_studio.processing.whisper_manager import whisper_manager
        from magic_time_studio.core.config import config_manager
        
        # Laad configuratie
        config_manager.load_configuration()
        
        # Initialiseer Fast Whisper
        print("\n🚀 Initialiseer Fast Whisper...")
        success = whisper_manager.initialize("fast", "large-v3-turbo")
        print(f"  Initialisatie succesvol: {success}")
        
        if not success:
            print("❌ Fast Whisper initialisatie gefaald")
            return False
        
        # Test met een bestaand audio bestand
        test_audio_path = r"D:\Films & Serie\Film\28.Years.Later.2025_audio.wav"
        
        if not os.path.exists(test_audio_path):
            print(f"❌ Audio bestand niet gevonden: {test_audio_path}")
            return False
        
        print(f"✅ Audio bestand gevonden: {test_audio_path}")
        
        def progress_callback(progress_bar):
            print(f"🔍 [DEBUG] Fast Whisper progress: {progress_bar}% - {os.path.basename(test_audio_path)}")
            return True
        
        def stop_callback():
            return False
        
        print("\n🎤 Start Fast Whisper transcriptie...")
        transcript_result = whisper_manager.transcribe_audio(
            test_audio_path,
            progress_callback=progress_callback,
            stop_callback=stop_callback
        )
        
        print(f"\n📊 Transcript result: {transcript_result}")
        
        if "error" in transcript_result:
            print(f"❌ Transcriptie gefaald: {transcript_result['error']}")
            return False
        
        transcript = transcript_result.get("transcript", "")
        transcriptions = transcript_result.get("transcriptions", [])
        
        print(f"📄 Transcript length: {len(transcript)}")
        print(f"📄 Transcriptions count: {len(transcriptions)}")
        
        if transcriptions:
            print(f"📄 First transcription: {transcriptions[0]}")
        
        # Test of transcript_result geldig is
        if not transcript and not transcriptions:
            print("❌ Transcript result is leeg")
            return False
        
        print("✅ Transcript result is geldig")
        
        # Test wat er gebeurt na transcriptie
        print("\n🔍 [DEBUG] Test wat er gebeurt na transcriptie...")
        
        # Simuleer de logica uit processing_thread.py
        if transcript_result and "error" not in transcript_result:
            print("✅ Transcript result is geldig, ga door naar volgende stap")
            
            # Test vertaling sectie
            print("🔍 [DEBUG] Test vertaling sectie...")
            enable_translation = False  # Simuleer geen vertaling
            print(f"  Enable translation: {enable_translation}")
            
            if enable_translation:
                print("  🔍 [DEBUG] Vertaling ingeschakeld")
                # Hier zou vertaling logica komen
            else:
                print("  🔍 [DEBUG] Geen vertaling")
                translated_transcriptions = transcriptions
            
            # Test video verwerking sectie
            print("🔍 [DEBUG] Test video verwerking sectie...")
            from magic_time_studio.processing.video_processor import video_processor
            
            # Mock settings
            settings = {
                "subtitle_type": "softcoded",
                "preserve_original_subtitles": True,
                "enable_translation": False
            }
            
            print(f"  Settings: {settings}")
            
            # Test SRT generatie
            print("🔍 [DEBUG] Test SRT generatie...")
            video_result = video_processor.generate_srt_files(
                test_audio_path.replace("_audio.wav", ".mp4"),  # Mock video path
                transcriptions,
                None,  # No translation
                settings
            )
            
            print(f"  Video result: {video_result}")
            
            if "error" in video_result:
                print(f"  ❌ SRT generatie gefaald: {video_result['error']}")
                return False
            else:
                print("  ✅ SRT generatie succesvol")
        
        return True
        
    except Exception as e:
        print(f"❌ Fout in test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 [DEBUG] Debug Transcript Test")
    print("=" * 50)
    
    success = test_debug_transcript()
    
    if success:
        print("\n🎉 Test geslaagd! Transcript result is geldig.")
    else:
        print("\n⚠️ Test gefaald. Controleer transcript result.") 