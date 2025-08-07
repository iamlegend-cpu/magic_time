#!/usr/bin/env python3
"""
Test om te controleren waarom Fast Whisper initialisatie faalt
"""

import sys
import os
from pathlib import Path

# Voeg project root toe aan Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_whisper_init():
    """Test Fast Whisper initialisatie"""
    print("🔍 [DEBUG] Whisper Initialisatie Test")
    print("=" * 50)
    
    try:
        from magic_time_studio.processing.whisper_manager import whisper_manager
        from magic_time_studio.core.config import config_manager
        
        # Laad configuratie
        print("📋 Laad configuratie...")
        config_manager.load_configuration()
        
        # Controleer beschikbare Whisper types
        print("🔍 Controleer beschikbare Whisper types...")
        available_types = whisper_manager.get_available_whisper_types()
        print(f"  Beschikbare types: {available_types}")
        
        # Controleer huidige status
        print("🔍 Controleer huidige status...")
        try:
            is_initialized = whisper_manager.is_initialized()
            print(f"  Is geïnitialiseerd: {is_initialized}")
        except AttributeError:
            print("  ⚠️ is_initialized methode niet beschikbaar")
        
        # Probeer initialisatie
        print("🔍 Probeer Fast Whisper initialisatie...")
        success = whisper_manager.initialize("fast", "large-v3-turbo")
        print(f"  Initialisatie succesvol: {success}")
        
        if not success:
            print("❌ Fast Whisper initialisatie gefaald")
            
            # Controleer of er een probleem is met de model
            print("🔍 Controleer beschikbare modellen...")
            try:
                from magic_time_studio.processing.whisper_processor import whisper_processor
                available_models = whisper_processor.get_available_models()
                print(f"  Beschikbare modellen: {available_models}")
            except Exception as e:
                print(f"  ❌ Kon modellen niet ophalen: {e}")
            
            return False
        
        print("✅ Fast Whisper initialisatie succesvol")
        
        # Controleer status na initialisatie
        try:
            is_initialized = whisper_manager.is_initialized()
            print(f"  Is geïnitialiseerd na init: {is_initialized}")
        except AttributeError:
            print("  ⚠️ is_initialized methode niet beschikbaar na init")
        
        return True
        
    except Exception as e:
        print(f"❌ Fout in test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 [DEBUG] Whisper Initialisatie Test")
    print("=" * 50)
    
    success = test_whisper_init()
    
    if success:
        print("\n🎉 Test geslaagd! Fast Whisper initialisatie werkt.")
    else:
        print("\n⚠️ Test gefaald. Fast Whisper initialisatie werkt niet.") 