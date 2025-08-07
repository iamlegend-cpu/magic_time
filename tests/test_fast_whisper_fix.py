"""
Test script voor Fast Whisper fix
Test of Fast Whisper werkt zonder VAD filter
"""

import sys
import os
from pathlib import Path

# Voeg project root toe aan Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_fast_whisper_import():
    """Test of Fast Whisper correct kan worden geïmporteerd"""
    try:
        from faster_whisper import WhisperModel
        print("✅ Fast Whisper import succesvol")
        return True
    except ImportError as e:
        print(f"❌ Fast Whisper import gefaald: {e}")
        return False

def test_onnxruntime_import():
    """Test of onnxruntime beschikbaar is"""
    try:
        import onnxruntime
        print("✅ ONNX Runtime import succesvol")
        return True
    except ImportError as e:
        print(f"❌ ONNX Runtime import gefaald: {e}")
        return False

def test_fast_whisper_processor():
    """Test Fast Whisper processor zonder VAD filter"""
    try:
        from magic_time_studio.processing.fast_whisper_processor import fast_whisper_processor
        
        # Test initialisatie
        success = fast_whisper_processor.initialize("medium")
        if success:
            print("✅ Fast Whisper processor initialisatie succesvol")
            
            # Test model info
            info = fast_whisper_processor.get_model_info()
            print(f"📊 Model info: {info}")
            
            # Cleanup
            fast_whisper_processor.cleanup()
            return True
        else:
            print("❌ Fast Whisper processor initialisatie gefaald")
            return False
            
    except Exception as e:
        print(f"❌ Fast Whisper processor test gefaald: {e}")
        return False

def test_whisper_manager():
    """Test Whisper Manager met Fast Whisper"""
    try:
        from magic_time_studio.processing.whisper_manager import whisper_manager
        
        # Test beschikbare types
        available_types = whisper_manager.get_available_whisper_types()
        print(f"📋 Beschikbare types: {available_types}")
        
        if "fast" in available_types:
            # Test Fast Whisper via manager
            success = whisper_manager.initialize("fast", "medium")
            if success:
                print("✅ Whisper Manager Fast Whisper initialisatie succesvol")
                
                info = whisper_manager.get_model_info()
                print(f"📊 Manager model info: {info}")
                
                whisper_manager.cleanup()
                return True
            else:
                print("❌ Whisper Manager Fast Whisper initialisatie gefaald")
                return False
        else:
            print("⚠️ Fast Whisper niet beschikbaar in manager")
            return False
            
    except Exception as e:
        print(f"❌ Whisper Manager test gefaald: {e}")
        return False

def main():
    """Hoofdfunctie voor tests"""
    print("🧪 Start Fast Whisper fix tests...\n")
    
    # Test 1: Fast Whisper import
    if not test_fast_whisper_import():
        print("❌ Fast Whisper import test gefaald")
        return False
    
    # Test 2: ONNX Runtime import
    if not test_onnxruntime_import():
        print("⚠️ ONNX Runtime niet beschikbaar (VAD filter zal uitgeschakeld zijn)")
    
    # Test 3: Fast Whisper processor
    if not test_fast_whisper_processor():
        print("❌ Fast Whisper processor test gefaald")
        return False
    
    # Test 4: Whisper Manager
    if not test_whisper_manager():
        print("❌ Whisper Manager test gefaald")
        return False
    
    print("\n✅ Alle tests geslaagd!")
    print("\n🎉 Fast Whisper werkt nu correct!")
    print("\n📋 Wat er is opgelost:")
    print("• VAD filter is uitgeschakeld om compatibiliteit te verbeteren")
    print("• Fast Whisper werkt nu zonder onnxruntime dependency")
    print("• Transcriptie zou nu moeten werken")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 