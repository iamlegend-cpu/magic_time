#!/usr/bin/env python3
"""
Test voor de modulaire structuur van ProcessingThread
"""

import sys
import os

# Voeg project root toe aan Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_modular_imports():
    """Test of alle modules correct importeren"""
    try:
        from magic_time_studio.app_core.processing_thread import ProcessingThread
        print("✅ ProcessingThread geïmporteerd")
        
        from magic_time_studio.app_core.processing_modules import (
            AudioProcessor, 
            WhisperProcessor, 
            TranslationProcessor, 
            VideoProcessor
        )
        print("✅ Alle processing modules geïmporteerd")
        
        return True
    except Exception as e:
        print(f"❌ Import fout: {e}")
        return False

def test_module_creation():
    """Test of modules correct aangemaakt kunnen worden"""
    try:
        from magic_time_studio.app_core.processing_thread import ProcessingThread
        
        # Mock data voor test
        files = ["test.mp4"]
        settings = {
            'whisper_type': 'fast',
            'whisper_model': 'large-v3-turbo',
            'enable_translation': False,
            'subtitle_type': 'softcoded'
        }
        
        # Maak ProcessingThread aan
        thread = ProcessingThread(files, settings)
        print("✅ ProcessingThread aangemaakt")
        
        # Test of modules correct geïnitialiseerd zijn
        assert hasattr(thread, 'audio_processor')
        assert hasattr(thread, 'whisper_processor')
        assert hasattr(thread, 'translation_processor')
        assert hasattr(thread, 'video_processor')
        
        print("✅ Alle modules correct geïnitialiseerd")
        return True
        
    except Exception as e:
        print(f"❌ Module creatie fout: {e}")
        return False

def test_module_functionality():
    """Test basis functionaliteit van modules"""
    try:
        from magic_time_studio.app_core.processing_thread import ProcessingThread
        
        # Mock data
        files = ["test.mp4"]
        settings = {
            'whisper_type': 'fast',
            'whisper_model': 'large-v3-turbo',
            'enable_translation': False,
            'subtitle_type': 'softcoded'
        }
        
        thread = ProcessingThread(files, settings)
        
        # Test of modules de juiste methodes hebben
        assert hasattr(thread.audio_processor, 'extract_audio')
        assert hasattr(thread.whisper_processor, 'transcribe_audio')
        assert hasattr(thread.translation_processor, 'translate_content')
        assert hasattr(thread.video_processor, 'process_video')
        
        print("✅ Alle modules hebben de juiste methodes")
        return True
        
    except Exception as e:
        print(f"❌ Module functionaliteit fout: {e}")
        return False

def main():
    """Voer alle tests uit"""
    print("🧪 Test modulaire structuur...")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_modular_imports),
        ("Module Creatie Test", test_module_creation),
        ("Module Functionaliteit Test", test_module_functionality)
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
        print("🎉 Alle tests geslaagd! Modulaire structuur werkt correct.")
        return True
    else:
        print("⚠️ Sommige tests gefaald. Controleer de fouten hierboven.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
