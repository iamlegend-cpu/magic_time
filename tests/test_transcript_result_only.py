#!/usr/bin/env python3
"""
Test die alleen de transcript_result controleert
"""

import sys
import os
from pathlib import Path

# Voeg project root toe aan Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_transcript_result_only():
    """Test alleen de transcript_result"""
    print("🔍 [DEBUG] Transcript Result Only Test")
    print("=" * 50)
    
    try:
        # Test met een bestaand audio bestand
        test_audio_path = r"D:\Films & Serie\Film\28.Years.Later.2025_audio.wav"
        
        if not os.path.exists(test_audio_path):
            print(f"❌ Audio bestand niet gevonden: {test_audio_path}")
            return False
        
        print(f"✅ Audio bestand gevonden: {test_audio_path}")
        
        # Test Fast Whisper transcriptie
        print("\n🎤 Test Fast Whisper transcriptie...")
        
        from magic_time_studio.processing.whisper_manager import whisper_manager
        from magic_time_studio.core.config import config_manager
        
        # Laad configuratie
        config_manager.load_configuration()
        
        # Initialiseer Fast Whisper
        success = whisper_manager.initialize("fast", "large-v3-turbo")
        print(f"  Initialisatie succesvol: {success}")
        
        if not success:
            print("❌ Fast Whisper initialisatie gefaald")
            return False
        
        def progress_callback(progress_bar):
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
        
        # Test of transcript_result geldig is
        if not transcript and not transcriptions:
            print("  ❌ Transcript result is leeg")
            return False
        
        print("  ✅ Transcript result is geldig")
        
        return True
        
    except Exception as e:
        print(f"❌ Fout in test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 [DEBUG] Transcript Result Only Test")
    print("=" * 50)
    
    success = test_transcript_result_only()
    
    if success:
        print("\n🎉 Test geslaagd! Transcript result is geldig.")
    else:
        print("\n⚠️ Test gefaald. Controleer transcript result.") 