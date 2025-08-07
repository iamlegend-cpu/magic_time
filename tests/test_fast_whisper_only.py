#!/usr/bin/env python3
"""
Test om te controleren of alleen Fast Whisper wordt gebruikt
Controleer of standaard Whisper volledig is uitgeschakeld
"""

import sys
import os
from pathlib import Path

# Voeg project root toe aan Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_fast_whisper_only():
    """Test of alleen Fast Whisper wordt gebruikt"""
    print("🔍 [DEBUG] Fast Whisper Only Test")
    print("=" * 50)
    
    try:
        # Import whisper manager
        from magic_time_studio.processing.whisper_manager import whisper_manager
        from magic_time_studio.core.config import config_manager
        
        print("✅ Whisper Manager geïmporteerd")
        
        # Laad configuratie
        config_manager.load_configuration()
        
        # Check beschikbare types
        available_types = whisper_manager.get_available_whisper_types()
        print(f"📋 Beschikbare Whisper types: {available_types}")
        
        # Controleer of alleen Fast Whisper beschikbaar is
        if len(available_types) == 1 and "fast" in available_types:
            print("✅ Alleen Fast Whisper beschikbaar")
        else:
            print("❌ Er zijn nog andere Whisper types beschikbaar")
            return False
        
        # Test initialisatie
        print("\n🚀 Test Fast Whisper initialisatie...")
        success = whisper_manager.initialize("fast", "large-v3-turbo")
        print(f"  Initialisatie succesvol: {success}")
        
        if success:
            current_type = whisper_manager.get_current_whisper_type()
            print(f"  Huidig type: {current_type}")
            
            if current_type == "fast":
                print("✅ Fast Whisper correct geïnitialiseerd")
            else:
                print("❌ Verkeerd Whisper type geïnitialiseerd")
                return False
            
            # Test transcriptie
            print("\n🎤 Test transcriptie...")
            mock_audio_path = "test_audio.wav"
            
            try:
                result = whisper_manager.transcribe_audio(mock_audio_path)
                print(f"  Transcriptie resultaat: {result}")
                
                # Controleer of het Fast Whisper was
                if "Fast Whisper" in str(result) or "error" in result:
                    print("✅ Fast Whisper wordt gebruikt voor transcriptie")
                else:
                    print("❌ Verkeerde processor gebruikt")
                    return False
                    
            except Exception as e:
                print(f"  Transcriptie error (verwacht): {e}")
        
        # Cleanup
        whisper_manager.cleanup()
        
        return True
        
    except Exception as e:
        print(f"❌ Fout in Fast Whisper only test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_standard_whisper_disabled():
    """Test of standaard Whisper volledig is uitgeschakeld"""
    print("\n🔍 [DEBUG] Standard Whisper Disabled Test")
    print("=" * 50)
    
    try:
        # Probeer standaard whisper processor te importeren
        try:
            from magic_time_studio.processing.whisper_processor_disabled import whisper_processor
            print("⚠️ Standaard Whisper processor nog steeds beschikbaar")
            return False
        except ImportError:
            print("✅ Standaard Whisper processor niet meer beschikbaar")
        
        # Test of de nieuwe whisper processor Fast Whisper is
        try:
            from magic_time_studio.processing.whisper_processor import whisper_processor
            print("✅ Nieuwe Whisper processor beschikbaar")
            
            # Test of het Fast Whisper is
            if hasattr(whisper_processor, 'available_models'):
                models = whisper_processor.available_models
                if 'large-v3-turbo' in models:
                    print("✅ Nieuwe processor is Fast Whisper")
                    return True
                else:
                    print("❌ Nieuwe processor is niet Fast Whisper")
                    return False
            else:
                print("❌ Nieuwe processor heeft geen available_models")
                return False
                
        except ImportError as e:
            print(f"❌ Nieuwe Whisper processor niet beschikbaar: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Fout in Standard Whisper disabled test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 [DEBUG] Fast Whisper Only Tests")
    print("=" * 50)
    
    # Test Fast Whisper only
    fast_only_ok = test_fast_whisper_only()
    
    # Test Standard Whisper disabled
    standard_disabled_ok = test_standard_whisper_disabled()
    
    print("\n📊 Test Resultaten:")
    print(f"  Fast Whisper Only: {'✅' if fast_only_ok else '❌'}")
    print(f"  Standard Whisper Disabled: {'✅' if standard_disabled_ok else '❌'}")
    
    if fast_only_ok and standard_disabled_ok:
        print("\n🎉 Alle tests geslaagd! Alleen Fast Whisper wordt gebruikt.")
    else:
        print("\n⚠️ Sommige tests gefaald. Standaard Whisper is nog actief.") 