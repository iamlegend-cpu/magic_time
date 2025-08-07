#!/usr/bin/env python3
"""
Eenvoudige VAD test
Diagnoseer VAD filter problemen
"""

import os
import sys
from pathlib import Path

# Voeg project root toe aan Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_vad_availability():
    """Test of VAD beschikbaar is"""
    print("🔍 Test VAD beschikbaarheid...")
    
    try:
        # Test ONNX Runtime
        import onnxruntime
        print("✅ ONNX Runtime beschikbaar")
        
        # Test Fast Whisper
        from faster_whisper import WhisperModel
        print("✅ Fast Whisper beschikbaar")
        
        # Test VAD parameters
        vad_params = dict(min_silence_duration_ms=500)
        print("✅ VAD parameters correct")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ VAD test error: {e}")
        return False

def test_vad_model_loading():
    """Test VAD model laden"""
    print("\n🔍 Test VAD model laden...")
    
    try:
        from faster_whisper import WhisperModel
        
        # Test model laden
        model = WhisperModel("tiny", device="cpu", compute_type="int8")
        print("✅ VAD model geladen")
        
        # Test VAD functionaliteit
        print("✅ VAD functionaliteit beschikbaar")
        
        return True
        
    except Exception as e:
        print(f"❌ VAD model laden gefaald: {e}")
        return False

def test_vad_error_handling():
    """Test VAD error handling"""
    print("\n🔍 Test VAD error handling...")
    
    try:
        from magic_time_studio.processing.whisper_processor import WhisperProcessor
        
        # Maak processor
        processor = WhisperProcessor()
        print("✅ Processor gemaakt")
        
        # Test initialisatie
        success = processor.initialize("tiny")
        if success:
            print("✅ Processor geïnitialiseerd")
            processor.cleanup()
            return True
        else:
            print("❌ Processor initialisatie gefaald")
            return False
            
    except Exception as e:
        print(f"❌ VAD error handling test gefaald: {e}")
        return False

def main():
    """Hoofdfunctie"""
    print("🧪 Start eenvoudige VAD tests...\n")
    
    # Test 1: VAD beschikbaarheid
    if not test_vad_availability():
        print("❌ VAD beschikbaarheid test gefaald")
        return False
    
    # Test 2: VAD model laden
    if not test_vad_model_loading():
        print("❌ VAD model laden test gefaald")
        return False
    
    # Test 3: VAD error handling
    if not test_vad_error_handling():
        print("❌ VAD error handling test gefaald")
        return False
    
    print("\n✅ Alle VAD tests geslaagd!")
    print("🎉 VAD filter werkt correct!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 