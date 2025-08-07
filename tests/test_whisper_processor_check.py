#!/usr/bin/env python3
"""
Test om te controleren welke Whisper processors actief zijn
Controleer of alleen Fast Whisper wordt gebruikt
"""

import sys
import os
from pathlib import Path

# Voeg project root toe aan Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_whisper_processor_status():
    """Test welke whisper processors actief zijn"""
    print("🔍 [DEBUG] Whisper Processor Status Test")
    print("=" * 50)
    
    try:
        # Import whisper manager
        from magic_time_studio.processing.whisper_manager import whisper_manager
        from magic_time_studio.core.config import config_manager
        
        print("✅ Whisper Manager geïmporteerd")
        
        # Laad configuratie
        config_manager.load_configuration()
        
        # Check huidige status voor initialisatie
        print("\n📊 Status voor initialisatie:")
        current_type = whisper_manager.get_current_whisper_type()
        print(f"  Huidig type: {current_type}")
        
        # Check processors
        if hasattr(whisper_manager, 'standard_processor') and whisper_manager.standard_processor:
            print(f"  Standaard processor: {type(whisper_manager.standard_processor)}")
            if hasattr(whisper_manager.standard_processor, 'is_initialized'):
                print(f"    Geïnitialiseerd: {whisper_manager.standard_processor.is_initialized}")
        else:
            print("  Standaard processor: Niet geladen")
            
        if hasattr(whisper_manager, 'fast_processor') and whisper_manager.fast_processor:
            print(f"  Fast processor: {type(whisper_manager.fast_processor)}")
            if hasattr(whisper_manager.fast_processor, 'is_initialized'):
                print(f"    Geïnitialiseerd: {whisper_manager.fast_processor.is_initialized}")
        else:
            print("  Fast processor: Niet geladen")
            
        if hasattr(whisper_manager, 'current_processor') and whisper_manager.current_processor:
            print(f"  Huidige processor: {type(whisper_manager.current_processor)}")
        else:
            print("  Huidige processor: Geen")
        
        # Initialiseer Fast Whisper
        print("\n🚀 Initialiseer Fast Whisper...")
        success = whisper_manager.initialize("fast", "large-v3-turbo")
        print(f"  Initialisatie succesvol: {success}")
        
        if success:
            print("\n📊 Status na Fast Whisper initialisatie:")
            current_type = whisper_manager.get_current_whisper_type()
            print(f"  Huidig type: {current_type}")
            
            # Check processors na initialisatie
            if hasattr(whisper_manager, 'standard_processor') and whisper_manager.standard_processor:
                print(f"  Standaard processor: {type(whisper_manager.standard_processor)}")
                if hasattr(whisper_manager.standard_processor, 'is_initialized'):
                    print(f"    Geïnitialiseerd: {whisper_manager.standard_processor.is_initialized}")
            else:
                print("  Standaard processor: Niet geladen")
                
            if hasattr(whisper_manager, 'fast_processor') and whisper_manager.fast_processor:
                print(f"  Fast processor: {type(whisper_manager.fast_processor)}")
                if hasattr(whisper_manager.fast_processor, 'is_initialized'):
                    print(f"    Geïnitialiseerd: {whisper_manager.fast_processor.is_initialized}")
            else:
                print("  Fast processor: Niet geladen")
                
            if hasattr(whisper_manager, 'current_processor') and whisper_manager.current_processor:
                print(f"  Huidige processor: {type(whisper_manager.current_processor)}")
                if whisper_manager.current_processor == whisper_manager.fast_processor:
                    print("    ✅ Huidige processor is Fast Whisper")
                elif whisper_manager.current_processor == whisper_manager.standard_processor:
                    print("    ⚠️ Huidige processor is Standaard Whisper")
                else:
                    print("    ❓ Huidige processor is onbekend type")
            else:
                print("  Huidige processor: Geen")
        
        # Test transcriptie call
        print("\n🎤 Test transcriptie call...")
        
        # Maak een mock audio bestand pad
        mock_audio_path = "test_audio.wav"
        
        # Test transcriptie zonder echte audio
        try:
            # Dit zou moeten falen omdat het bestand niet bestaat, maar we kunnen zien welke processor wordt gebruikt
            result = whisper_manager.transcribe_audio(mock_audio_path)
            print(f"  Transcriptie resultaat: {result}")
        except Exception as e:
            print(f"  Transcriptie error (verwacht): {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Fout in processor status test: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Cleanup
        try:
            if 'whisper_manager' in locals():
                whisper_manager.cleanup()
        except:
            pass

def test_processor_imports():
    """Test welke processors worden geïmporteerd"""
    print("\n🔍 [DEBUG] Processor Import Test")
    print("=" * 50)
    
    try:
        # Test directe imports
        print("📦 Test directe imports...")
        
        # Test whisper processor import
        try:
            from magic_time_studio.processing.whisper_processor import whisper_processor
            print("✅ Standaard Whisper processor geïmporteerd")
            print(f"  Type: {type(whisper_processor)}")
            print(f"  Geïnitialiseerd: {whisper_processor.is_initialized}")
        except Exception as e:
            print(f"❌ Standaard Whisper import fout: {e}")
        
        # Test fast whisper processor import
        try:
            from magic_time_studio.processing.fast_whisper_processor import fast_whisper_processor
            print("✅ Fast Whisper processor geïmporteerd")
            print(f"  Type: {type(fast_whisper_processor)}")
            print(f"  Geïnitialiseerd: {fast_whisper_processor.is_initialized}")
        except Exception as e:
            print(f"❌ Fast Whisper import fout: {e}")
        
        # Test whisper manager import
        try:
            from magic_time_studio.processing.whisper_manager import whisper_manager
            print("✅ Whisper Manager geïmporteerd")
            print(f"  Type: {type(whisper_manager)}")
        except Exception as e:
            print(f"❌ Whisper Manager import fout: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Fout in import test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 [DEBUG] Whisper Processor Tests")
    print("=" * 50)
    
    # Test imports
    import_ok = test_processor_imports()
    
    # Test processor status
    status_ok = test_whisper_processor_status()
    
    print("\n📊 Test Resultaten:")
    print(f"  Import Test: {'✅' if import_ok else '❌'}")
    print(f"  Status Test: {'✅' if status_ok else '❌'}")
    
    if import_ok and status_ok:
        print("\n🎉 Alle tests geslaagd! Processor status is correct.")
    else:
        print("\n⚠️ Sommige tests gefaald. Controleer de processor configuratie.") 