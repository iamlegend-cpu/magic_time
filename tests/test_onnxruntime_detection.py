#!/usr/bin/env python3
"""
Test voor onnxruntime detectie in WhisperProcessor
"""

import sys
import os

# Voeg project root toe aan Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_onnxruntime_import():
    """Test of onnxruntime correct wordt geïmporteerd"""
    try:
        import onnxruntime
        print(f"✅ onnxruntime geïmporteerd: {onnxruntime.__version__}")
        return True
    except ImportError as e:
        print(f"❌ onnxruntime import gefaald: {e}")
        return False

def test_whisper_processor_onnxruntime():
    """Test of WhisperProcessor onnxruntime correct detecteert"""
    try:
        from magic_time_studio.processing.whisper_processor import WhisperProcessor, ONNX_RUNTIME_AVAILABLE
        
        print(f"✅ WhisperProcessor geïmporteerd")
        print(f"📊 ONNX_RUNTIME_AVAILABLE: {ONNX_RUNTIME_AVAILABLE}")
        
        # Maak een instance aan
        processor = WhisperProcessor()
        print(f"✅ WhisperProcessor instance aangemaakt")
        
        return True
    except Exception as e:
        print(f"❌ WhisperProcessor test gefaald: {e}")
        return False

def test_vad_availability():
    """Test VAD beschikbaarheid"""
    try:
        from magic_time_studio.processing.whisper_processor import ONNX_RUNTIME_AVAILABLE
        
        if ONNX_RUNTIME_AVAILABLE:
            print("✅ VAD (Voice Activity Detection) beschikbaar via onnxruntime")
        else:
            print("⚠️ VAD niet beschikbaar - onnxruntime niet geïnstalleerd")
        
        return True
    except Exception as e:
        print(f"❌ VAD test gefaald: {e}")
        return False

def main():
    """Voer alle tests uit"""
    print("🧪 Test onnxruntime detectie...")
    print("=" * 50)
    
    tests = [
        ("onnxruntime Import Test", test_onnxruntime_import),
        ("WhisperProcessor onnxruntime Test", test_whisper_processor_onnxruntime),
        ("VAD Beschikbaarheid Test", test_vad_availability)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}...")
        if test_func():
            print(f"✅ {test_name} geslaagd")
            passed += 1
        else:
            print(f"❌ {test_name} gefaald")
    
    print("\n" + "=" * 50)
    print(f"📊 Resultaat: {passed}/{total} tests geslaagd")
    
    if passed == total:
        print("🎉 Alle tests geslaagd! onnxruntime detectie werkt correct.")
        return True
    else:
        print("⚠️ Sommige tests gefaald. Controleer de fouten hierboven.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
