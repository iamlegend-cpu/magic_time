#!/usr/bin/env python3
"""
Eenvoudige test om te controleren of CUDA nu werkt
"""

import sys
import os
from pathlib import Path

# Voeg project root toe aan Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_cuda_simple():
    """Test of CUDA nu werkt"""
    print("🔍 [DEBUG] CUDA Simple Test")
    print("=" * 50)
    
    try:
        # Test of faster_whisper kan importeren
        print("🔍 Test faster_whisper import...")
        from faster_whisper import WhisperModel
        print("✅ faster_whisper geïmporteerd")
        
        # Test of CUDA model kan laden
        print("🔍 Test CUDA model laden...")
        model = WhisperModel("tiny", device="cuda", compute_type="float16")
        print("✅ CUDA model geladen!")
        
        # Test of transcriptie werkt
        print("🔍 Test transcriptie...")
        # Maak een dummy audio bestand
        import numpy as np
        import wave
        
        # Maak een 1 seconde stilte bestand
        sample_rate = 16000
        duration = 1
        samples = np.zeros(sample_rate * duration, dtype=np.int16)
        
        with wave.open("test_audio.wav", "w") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(samples.tobytes())
        
        print("✅ Dummy audio bestand gemaakt")
        
        # Test transcriptie
        segments, info = model.transcribe("test_audio.wav")
        print("✅ Transcriptie werkt!")
        
        # Cleanup
        os.remove("test_audio.wav")
        print("✅ Test bestand opgeruimd")
        
        return True
        
    except Exception as e:
        print(f"❌ Fout in test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 [DEBUG] CUDA Simple Test")
    print("=" * 50)
    
    success = test_cuda_simple()
    
    if success:
        print("\n🎉 Test geslaagd! CUDA werkt.")
    else:
        print("\n⚠️ Test gefaald. CUDA werkt niet.") 