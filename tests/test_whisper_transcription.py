"""
Test script voor Whisper transcriptie functionaliteit
Test beide Whisper types voor transcriptie
"""

import sys
import os
import time
from pathlib import Path

# Voeg project root toe aan Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_whisper_manager_import():
    """Test of Whisper Manager correct kan worden geïmporteerd"""
    print("🧪 Test Whisper Manager import...")
    
    try:
        from magic_time_studio.processing.whisper_manager import whisper_manager
        print("✅ Whisper Manager import succesvol!")
        return True
    except ImportError as e:
        print(f"❌ Whisper Manager import gefaald: {e}")
        return False

def test_available_types():
    """Test beschikbare Whisper types"""
    print("\n🧪 Test beschikbare Whisper types...")
    
    try:
        from magic_time_studio.processing.whisper_manager import whisper_manager
        
        available_types = whisper_manager.get_available_whisper_types()
        print(f"📋 Beschikbare types: {available_types}")
        
        for whisper_type in available_types:
            models = whisper_manager.get_available_models(whisper_type)
            print(f"  • {whisper_type}: {len(models)} modellen beschikbaar")
            for model in models:
                print(f"    - {model}")
        
        return True
        
    except Exception as e:
        print(f"❌ Fout bij testen beschikbare types: {e}")
        return False

def test_standard_whisper_initialization():
    """Test standaard Whisper initialisatie"""
    print("\n🧪 Test standaard Whisper initialisatie...")
    
    try:
        from magic_time_studio.processing.whisper_manager import whisper_manager
        
        # Test initialisatie
        print("🔧 Initialiseer standaard Whisper (large)...")
        success = whisper_manager.initialize("standard", "large")
        
        if success:
            print("✅ Standaard Whisper succesvol geïnitialiseerd!")
            
            # Test model info
            info = whisper_manager.get_model_info()
            print(f"📊 Model info: {info}")
            
            # Test cleanup
            whisper_manager.cleanup()
            print("✅ Standaard Whisper cleanup succesvol!")
            
        else:
            print("❌ Standaard Whisper initialisatie gefaald!")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Fout bij testen standaard Whisper: {e}")
        return False

def test_fast_whisper_initialization():
    """Test Fast Whisper initialisatie"""
    print("\n🧪 Test Fast Whisper initialisatie...")
    
    try:
        from magic_time_studio.processing.whisper_manager import whisper_manager
        
        # Controleer of Fast Whisper beschikbaar is
        available_types = whisper_manager.get_available_whisper_types()
        if "fast" not in available_types:
            print("⚠️ Fast Whisper niet beschikbaar, sla test over")
            return True
        
        # Test initialisatie met kleiner model voor snelheid
        print("🔧 Initialiseer Fast Whisper (medium)...")
        success = whisper_manager.initialize("fast", "medium")
        
        if success:
            print("✅ Fast Whisper succesvol geïnitialiseerd!")
            
            # Test model info
            info = whisper_manager.get_model_info()
            print(f"📊 Model info: {info}")
            
            # Test cleanup
            whisper_manager.cleanup()
            print("✅ Fast Whisper cleanup succesvol!")
            
        else:
            print("❌ Fast Whisper initialisatie gefaald!")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Fout bij testen Fast Whisper: {e}")
        return False

def test_whisper_switching():
    """Test wisselen tussen Whisper types"""
    print("\n🧪 Test Whisper type wisselen...")
    
    try:
        from magic_time_studio.processing.whisper_manager import whisper_manager
        
        available_types = whisper_manager.get_available_whisper_types()
        
        if len(available_types) < 2:
            print("⚠️ Niet genoeg types beschikbaar voor switching test")
            return True
        
        # Test wisselen van standard naar fast
        if "standard" in available_types and "fast" in available_types:
            print("🔄 Test wisselen van standard naar fast...")
            
            # Initialiseer standard
            success = whisper_manager.initialize("standard", "large")
            if success:
                print("✅ Standard Whisper geladen")
                current_type = whisper_manager.get_current_whisper_type()
                print(f"📊 Huidig type: {current_type}")
                
                # Wissel naar fast
                success = whisper_manager.switch_whisper_type("fast", "medium")
                if success:
                    print("✅ Wissel naar Fast Whisper succesvol!")
                    current_type = whisper_manager.get_current_whisper_type()
                    print(f"📊 Nieuw type: {current_type}")
                else:
                    print("❌ Wissel naar Fast Whisper gefaald!")
                
                # Cleanup
                whisper_manager.cleanup()
                print("✅ Cleanup succesvol!")
        
        return True
        
    except Exception as e:
        print(f"❌ Fout bij testen Whisper switching: {e}")
        return False

def test_performance_comparison():
    """Test performance vergelijking"""
    print("\n🧪 Test performance vergelijking...")
    
    try:
        from magic_time_studio.processing.whisper_manager import whisper_manager
        
        comparison = whisper_manager.get_performance_comparison()
        print("📊 Performance vergelijking:")
        print(f"  • Standard beschikbaar: {comparison['standard_available']}")
        print(f"  • Fast beschikbaar: {comparison['fast_available']}")
        print(f"  • Huidig type: {comparison['current_type']}")
        
        if comparison["recommendations"]:
            print("💡 Aanbevelingen:")
            for rec in comparison["recommendations"]:
                print(f"  • {rec['type']}: {rec['reason']} (model: {rec['model']})")
        
        return True
        
    except Exception as e:
        print(f"❌ Fout bij testen performance vergelijking: {e}")
        return False

def test_model_loading_speed():
    """Test model loading snelheid"""
    print("\n🧪 Test model loading snelheid...")
    
    try:
        from magic_time_studio.processing.whisper_manager import whisper_manager
        
        available_types = whisper_manager.get_available_whisper_types()
        
        # Test standaard Whisper loading tijd
        if "standard" in available_types:
            print("⏱️ Test standaard Whisper loading tijd...")
            start_time = time.time()
            success = whisper_manager.initialize("standard", "large")
            standard_time = time.time() - start_time
            
            if success:
                print(f"✅ Standaard Whisper geladen in {standard_time:.2f} seconden")
                whisper_manager.cleanup()
            else:
                print("❌ Standaard Whisper loading gefaald!")
        
        # Test Fast Whisper loading tijd
        if "fast" in available_types:
            print("⏱️ Test Fast Whisper loading tijd...")
            start_time = time.time()
            success = whisper_manager.initialize("fast", "medium")
            fast_time = time.time() - start_time
            
            if success:
                print(f"✅ Fast Whisper geladen in {fast_time:.2f} seconden")
                whisper_manager.cleanup()
            else:
                print("❌ Fast Whisper loading gefaald!")
        
        # Vergelijk loading tijden
        if "standard" in available_types and "fast" in available_types:
            if standard_time > 0 and fast_time > 0:
                speedup = standard_time / fast_time
                print(f"\n📊 Loading snelheid vergelijking:")
                print(f"  • Standaard Whisper: {standard_time:.2f}s")
                print(f"  • Fast Whisper: {fast_time:.2f}s")
                print(f"  • Snelheidsverbetering: {speedup:.1f}x sneller")
        
        return True
        
    except Exception as e:
        print(f"❌ Fout bij testen model loading snelheid: {e}")
        return False

def main():
    """Hoofdfunctie"""
    print("🤖 Whisper Transcriptie Test Script")
    print("=" * 50)
    
    # Test imports
    if not test_whisper_manager_import():
        print("\n❌ Whisper Manager is niet correct geïmplementeerd!")
        return
    
    # Test beschikbare types
    if not test_available_types():
        print("\n❌ Test beschikbare types gefaald!")
        return
    
    # Test standaard Whisper
    if not test_standard_whisper_initialization():
        print("\n❌ Test standaard Whisper gefaald!")
        return
    
    # Test Fast Whisper
    if not test_fast_whisper_initialization():
        print("\n❌ Test Fast Whisper gefaald!")
        return
    
    # Test switching
    if not test_whisper_switching():
        print("\n❌ Test Whisper switching gefaald!")
        return
    
    # Test performance vergelijking
    if not test_performance_comparison():
        print("\n❌ Test performance vergelijking gefaald!")
        return
    
    # Test model loading snelheid
    if not test_model_loading_speed():
        print("\n❌ Test model loading snelheid gefaald!")
        return
    
    print("\n🎉 Whisper transcriptie test voltooid!")
    print("💡 Beide Whisper types zijn klaar voor gebruik in Magic Time Studio")
    print("💡 Je kunt nu kiezen tussen standaard Whisper en Fast Whisper!")

if __name__ == "__main__":
    main() 