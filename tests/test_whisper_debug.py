#!/usr/bin/env python3
"""
Debug test voor Whisper Manager
Controleer welke processors geladen zijn en of Fast Whisper correct werkt
"""

import sys
import os
from pathlib import Path

# Voeg project root toe aan Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_whisper_manager_debug():
    """Debug test voor Whisper Manager"""
    print("🔍 [DEBUG] Whisper Manager Debug Test")
    print("=" * 50)
    
    try:
        # Import whisper manager
        from magic_time_studio.processing.whisper_manager import whisper_manager
        print("✅ Whisper Manager geïmporteerd")
        
        # Check beschikbare types
        available_types = whisper_manager.get_available_whisper_types()
        print(f"📋 Beschikbare Whisper types: {available_types}")
        
        # Check huidige status
        current_type = whisper_manager.get_current_whisper_type()
        print(f"🎯 Huidig Whisper type: {current_type}")
        
        # Check of modellen geladen zijn
        is_loaded = whisper_manager.is_model_loaded()
        print(f"📦 Model geladen: {is_loaded}")
        
        # Check processor status
        print("\n🔧 Processor Status:")
        if hasattr(whisper_manager, 'standard_processor') and whisper_manager.standard_processor:
            print(f"  - Standaard processor: {type(whisper_manager.standard_processor)}")
            if hasattr(whisper_manager.standard_processor, 'is_initialized'):
                print(f"    Geïnitialiseerd: {whisper_manager.standard_processor.is_initialized}")
        else:
            print("  - Standaard processor: Niet geladen")
            
        if hasattr(whisper_manager, 'fast_processor') and whisper_manager.fast_processor:
            print(f"  - Fast processor: {type(whisper_manager.fast_processor)}")
            if hasattr(whisper_manager.fast_processor, 'is_initialized'):
                print(f"    Geïnitialiseerd: {whisper_manager.fast_processor.is_initialized}")
        else:
            print("  - Fast processor: Niet geladen")
            
        if hasattr(whisper_manager, 'current_processor') and whisper_manager.current_processor:
            print(f"  - Huidige processor: {type(whisper_manager.current_processor)}")
        else:
            print("  - Huidige processor: Geen")
        
        # Test Fast Whisper initialisatie
        print("\n🚀 Test Fast Whisper initialisatie:")
        success = whisper_manager.initialize("fast", "large-v3-turbo")
        print(f"  Initialisatie succesvol: {success}")
        
        if success:
            current_type = whisper_manager.get_current_whisper_type()
            print(f"  Huidig type na initialisatie: {current_type}")
            
            is_loaded = whisper_manager.is_model_loaded()
            print(f"  Model geladen na initialisatie: {is_loaded}")
            
            # Check processor status na initialisatie
            if hasattr(whisper_manager, 'current_processor') and whisper_manager.current_processor:
                print(f"  Huidige processor type: {type(whisper_manager.current_processor)}")
                
                # Test model info
                model_info = whisper_manager.get_model_info()
                print(f"  Model info: {model_info}")
            else:
                print("  ❌ Geen huidige processor na initialisatie")
        
        # Cleanup
        whisper_manager.cleanup()
        print("\n🧹 Cleanup voltooid")
        
        return True
        
    except Exception as e:
        print(f"❌ Fout in debug test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fast_whisper_import():
    """Test Fast Whisper import"""
    print("\n🔍 [DEBUG] Fast Whisper Import Test")
    print("=" * 50)
    
    try:
        # Test directe import
        from faster_whisper import WhisperModel
        print("✅ Faster Whisper geïmporteerd")
        
        # Test model loading
        print("📦 Test model loading...")
        model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")
        print("✅ Fast Whisper model geladen")
        
        # Cleanup
        del model
        print("🧹 Model opgeruimd")
        
        return True
        
    except ImportError as e:
        print(f"❌ Faster Whisper niet geïnstalleerd: {e}")
        return False
    except Exception as e:
        print(f"❌ Fout bij Fast Whisper test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_standard_whisper_import():
    """Test Standard Whisper import"""
    print("\n🔍 [DEBUG] Standard Whisper Import Test")
    print("=" * 50)
    
    try:
        # Test directe import
        import whisper
        print("✅ Standard Whisper geïmporteerd")
        
        # Test model loading
        print("📦 Test model loading...")
        model = whisper.load_model("base", device="cpu")
        print("✅ Standard Whisper model geladen")
        
        # Cleanup
        del model
        print("🧹 Model opgeruimd")
        
        return True
        
    except ImportError as e:
        print(f"❌ Standard Whisper niet geïnstalleerd: {e}")
        return False
    except Exception as e:
        print(f"❌ Fout bij Standard Whisper test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 [DEBUG] Whisper Debug Tests")
    print("=" * 50)
    
    # Test imports
    standard_ok = test_standard_whisper_import()
    fast_ok = test_fast_whisper_import()
    
    # Test whisper manager
    manager_ok = test_whisper_manager_debug()
    
    print("\n📊 Test Resultaten:")
    print(f"  Standard Whisper: {'✅' if standard_ok else '❌'}")
    print(f"  Fast Whisper: {'✅' if fast_ok else '❌'}")
    print(f"  Whisper Manager: {'✅' if manager_ok else '❌'}")
    
    if not fast_ok:
        print("\n💡 Oplossing: Installeer Fast Whisper met:")
        print("   pip install faster-whisper")
    
    if not standard_ok:
        print("\n💡 Oplossing: Installeer Standard Whisper met:")
        print("   pip install openai-whisper") 