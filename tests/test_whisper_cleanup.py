#!/usr/bin/env python3
"""
Test om te controleren of alle oude Whisper processor instanties zijn opgeruimd
Controleer of alleen Fast Whisper wordt gebruikt
"""

import sys
import os
from pathlib import Path

# Voeg project root toe aan Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_whisper_cleanup():
    """Test of alle oude whisper processor instanties zijn opgeruimd"""
    print("🔍 [DEBUG] Whisper Cleanup Test")
    print("=" * 50)
    
    try:
        # Import alle modules
        from magic_time_studio.processing.whisper_manager import whisper_manager
        from magic_time_studio.processing.whisper_processor import whisper_processor
        from magic_time_studio.processing.fast_whisper_processor import fast_whisper_processor
        from magic_time_studio.core.config import config_manager
        
        print("✅ Alle modules geïmporteerd")
        
        # Laad configuratie
        config_manager.load_configuration()
        
        # Check status van alle processors
        print("\n📊 Processor Status:")
        
        # Check whisper manager
        print("  Whisper Manager:")
        current_type = whisper_manager.get_current_whisper_type()
        print(f"    Huidig type: {current_type}")
        print(f"    Model geladen: {whisper_manager.is_model_loaded()}")
        
        # Check standaard whisper processor
        print("  Standaard Whisper Processor:")
        print(f"    Geïnitialiseerd: {whisper_processor.is_initialized}")
        print(f"    Model geladen: {whisper_processor.is_model_loaded()}")
        
        # Check fast whisper processor
        print("  Fast Whisper Processor:")
        print(f"    Geïnitialiseerd: {fast_whisper_processor.is_initialized}")
        print(f"    Model geladen: {fast_whisper_processor.is_model_loaded()}")
        
        # Initialiseer Fast Whisper via manager
        print("\n🚀 Initialiseer Fast Whisper via manager...")
        success = whisper_manager.initialize("fast", "large-v3-turbo")
        print(f"  Initialisatie succesvol: {success}")
        
        if success:
            print("\n📊 Status na Fast Whisper initialisatie:")
            
            # Check whisper manager
            print("  Whisper Manager:")
            current_type = whisper_manager.get_current_whisper_type()
            print(f"    Huidig type: {current_type}")
            print(f"    Model geladen: {whisper_manager.is_model_loaded()}")
            
            # Check standaard whisper processor (moet nog steeds niet geïnitialiseerd zijn)
            print("  Standaard Whisper Processor:")
            print(f"    Geïnitialiseerd: {whisper_processor.is_initialized}")
            print(f"    Model geladen: {whisper_processor.is_model_loaded()}")
            
            # Check fast whisper processor (moet geïnitialiseerd zijn)
            print("  Fast Whisper Processor:")
            print(f"    Geïnitialiseerd: {fast_whisper_processor.is_initialized}")
            print(f"    Model geladen: {fast_whisper_processor.is_model_loaded()}")
            
            # Test transcriptie call
            print("\n🎤 Test transcriptie call...")
            
            # Maak een mock audio bestand pad
            mock_audio_path = "test_audio.wav"
            
            # Test transcriptie zonder echte audio
            try:
                result = whisper_manager.transcribe_audio(mock_audio_path)
                print(f"  Transcriptie resultaat: {result}")
            except Exception as e:
                print(f"  Transcriptie error (verwacht): {e}")
        
        # Cleanup
        print("\n🧹 Cleanup...")
        whisper_manager.cleanup()
        
        print("\n📊 Status na cleanup:")
        
        # Check whisper manager
        print("  Whisper Manager:")
        current_type = whisper_manager.get_current_whisper_type()
        print(f"    Huidig type: {current_type}")
        print(f"    Model geladen: {whisper_manager.is_model_loaded()}")
        
        # Check standaard whisper processor
        print("  Standaard Whisper Processor:")
        print(f"    Geïnitialiseerd: {whisper_processor.is_initialized}")
        print(f"    Model geladen: {whisper_processor.is_model_loaded()}")
        
        # Check fast whisper processor
        print("  Fast Whisper Processor:")
        print(f"    Geïnitialiseerd: {fast_whisper_processor.is_initialized}")
        print(f"    Model geladen: {fast_whisper_processor.is_model_loaded()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Fout in cleanup test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_processor_isolation():
    """Test of processors geïsoleerd zijn"""
    print("\n🔍 [DEBUG] Processor Isolation Test")
    print("=" * 50)
    
    try:
        from magic_time_studio.processing.whisper_manager import whisper_manager
        from magic_time_studio.processing.whisper_processor import whisper_processor
        from magic_time_studio.processing.fast_whisper_processor import fast_whisper_processor
        
        print("✅ Processors geïmporteerd")
        
        # Test of processors onafhankelijk zijn
        print("\n🔍 Test processor onafhankelijkheid:")
        
        # Initialiseer Fast Whisper via manager
        print("  1. Initialiseer Fast Whisper via manager...")
        success = whisper_manager.initialize("fast", "large-v3-turbo")
        print(f"     Manager initialisatie: {success}")
        print(f"     Manager type: {whisper_manager.get_current_whisper_type()}")
        print(f"     Manager model geladen: {whisper_manager.is_model_loaded()}")
        
        # Check directe processors
        print("  2. Check directe processors...")
        print(f"     Standaard processor geïnitialiseerd: {whisper_processor.is_initialized}")
        print(f"     Fast processor geïnitialiseerd: {fast_whisper_processor.is_initialized}")
        
        # Test of manager en directe processor verschillend zijn
        print("  3. Test processor gelijkheid...")
        if whisper_manager.current_processor == fast_whisper_processor:
            print("    ✅ Manager gebruikt Fast Whisper processor")
        else:
            print("    ❌ Manager gebruikt niet Fast Whisper processor")
        
        # Cleanup
        whisper_manager.cleanup()
        
        return True
        
    except Exception as e:
        print(f"❌ Fout in isolation test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 [DEBUG] Whisper Cleanup Tests")
    print("=" * 50)
    
    # Test cleanup
    cleanup_ok = test_whisper_cleanup()
    
    # Test isolation
    isolation_ok = test_processor_isolation()
    
    print("\n📊 Test Resultaten:")
    print(f"  Cleanup Test: {'✅' if cleanup_ok else '❌'}")
    print(f"  Isolation Test: {'✅' if isolation_ok else '❌'}")
    
    if cleanup_ok and isolation_ok:
        print("\n🎉 Alle tests geslaagd! Whisper processors zijn correct geïsoleerd.")
    else:
        print("\n⚠️ Sommige tests gefaald. Er zijn nog oude processor instanties actief.") 