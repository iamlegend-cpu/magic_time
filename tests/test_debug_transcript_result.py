#!/usr/bin/env python3
"""
Test om te debuggen wat er gebeurt met transcript_result na Fast Whisper transcriptie
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from magic_time_studio.processing.whisper_manager import whisper_manager
from magic_time_studio.processing import audio_processor

def test_debug_transcript_result():
    print("🔍 [DEBUG] Test transcript_result debug")
    print("=" * 50)
    
    # Test met een dummy audio bestand
    test_audio_path = "test_audio.wav"
    
    # Maak een dummy audio bestand
    import wave
    import numpy as np
    
    # Maak een eenvoudig audio bestand
    sample_rate = 16000
    duration = 5  # 5 seconden
    samples = np.sin(2 * np.pi * 440 * np.linspace(0, duration, sample_rate * duration))
    
    with wave.open(test_audio_path, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes((samples * 32767).astype(np.int16).tobytes())
    
    print(f"✅ Test audio bestand gemaakt: {test_audio_path}")
    
    try:
        # Initialiseer Fast Whisper
        print("🔍 [DEBUG] Initialiseer Fast Whisper...")
        if not whisper_manager.initialize("fast", "tiny"):
            print("❌ Fast Whisper initialisatie gefaald")
            return False
        
        print("✅ Fast Whisper geïnitialiseerd")
        
        # Voer transcriptie uit
        print("🔍 [DEBUG] Start transcriptie...")
        transcript_result = whisper_manager.transcribe_audio(test_audio_path)
        
        print(f"🔍 [DEBUG] transcript_result type: {type(transcript_result)}")
        print(f"🔍 [DEBUG] transcript_result: {transcript_result}")
        
        if isinstance(transcript_result, dict):
            print(f"🔍 [DEBUG] transcript_result keys: {list(transcript_result.keys())}")
            
            # Test de logica uit ProcessingThread
            if transcript_result and "error" not in transcript_result:
                print("✅ Transcript result is geldig")
                
                transcript = transcript_result.get("transcript", "")
                transcriptions = transcript_result.get("transcriptions", [])
                
                print(f"🔍 [DEBUG] transcript length: {len(transcript)}")
                print(f"🔍 [DEBUG] transcriptions count: {len(transcriptions)}")
                
                if transcriptions:
                    print(f"🔍 [DEBUG] First transcription: {transcriptions[0]}")
                
                print("✅ Logica test geslaagd!")
            else:
                print("❌ Transcript result is ongeldig of bevat error")
                if "error" in transcript_result:
                    print(f"🔍 [DEBUG] Error: {transcript_result['error']}")
        else:
            print(f"❌ transcript_result is geen dict: {type(transcript_result)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Fout tijdens test: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Ruim test bestand op
        if os.path.exists(test_audio_path):
            os.remove(test_audio_path)
            print(f"🗑️ Test bestand opgeruimd: {test_audio_path}")

if __name__ == "__main__":
    success = test_debug_transcript_result()
    if success:
        print("🎉 Test voltooid!")
    else:
        print("❌ Test gefaald!") 