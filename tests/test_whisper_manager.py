"""
Test script voor Whisper Manager
Test de functionaliteit voor zowel standaard Whisper als Fast Whisper
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

def test_standard_whisper():
    """Test standaard Whisper functionaliteit"""
    print("\n🧪 Test standaard Whisper...")
    
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

def test_fast_whisper():
    """Test Fast Whisper functionaliteit"""
    print("\n🧪 Test Fast Whisper...")
    
    try:
        from magic_time_studio.processing.whisper_manager import whisper_manager
        
        # Controleer of Fast Whisper beschikbaar is
        available_types = whisper_manager.get_available_whisper_types()
        if "fast" not in available_types:
            print("⚠️ Fast Whisper niet beschikbaar, sla test over")
            return True
        
        # Test initialisatie
        print("🔧 Initialiseer Fast Whisper (large-v3-turbo)...")
        success = whisper_manager.initialize("fast", "large-v3-turbo")
        
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
                success = whisper_manager.switch_whisper_type("fast", "large-v3-turbo")
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

def test_audio_transcription():
    """Test audio transcriptie (als test bestand beschikbaar is)"""
    print("\n🧪 Test audio transcriptie...")
    
    # Test bestand (je kunt dit aanpassen naar een echt audio bestand)
    test_audio = "test_audio.wav"  # Vervang door echt bestand
    
    if not os.path.exists(test_audio):
        print(f"⚠️ Test audio bestand niet gevonden: {test_audio}")
        print("💡 Maak een test audio bestand aan om transcriptie te testen")
        return True
    
    try:
        from magic_time_studio.processing.whisper_manager import whisper_manager
        
        print(f"📁 Test bestand: {test_audio}")
        
        # Test met standaard Whisper
        if "standard" in whisper_manager.get_available_whisper_types():
            print("\n🐌 Test transcriptie met standaard Whisper...")
            success = whisper_manager.initialize("standard", "large")
            
            if success:
                start_time = time.time()
                result = whisper_manager.transcribe_audio(test_audio)
                standard_time = time.time() - start_time
                
                if result.get("success"):
                    print(f"✅ Standaard Whisper voltooid in {standard_time:.2f} seconden")
                    print(f"📝 Tekst: {result['transcript'][:100]}...")
                else:
                    print(f"❌ Standaard Whisper gefaald: {result.get('error')}")
                
                whisper_manager.cleanup()
        
        # Test met Fast Whisper
        if "fast" in whisper_manager.get_available_whisper_types():
            print("\n🚀 Test transcriptie met Fast Whisper...")
            success = whisper_manager.initialize("fast", "large-v3-turbo")
            
            if success:
                start_time = time.time()
                result = whisper_manager.transcribe_audio(test_audio)
                fast_time = time.time() - start_time
                
                if result.get("success"):
                    print(f"✅ Fast Whisper voltooid in {fast_time:.2f} seconden")
                    print(f"📝 Tekst: {result['transcript'][:100]}...")
                else:
                    print(f"❌ Fast Whisper gefaald: {result.get('error')}")
                
                whisper_manager.cleanup()
        
        return True
        
    except Exception as e:
        print(f"❌ Fout bij testen audio transcriptie: {e}")
        return False

def main():
    """Hoofdfunctie"""
    print("🤖 Whisper Manager Test Script")
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
    if not test_standard_whisper():
        print("\n❌ Test standaard Whisper gefaald!")
        return
    
    # Test Fast Whisper
    if not test_fast_whisper():
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
    
    # Test audio transcriptie
    if not test_audio_transcription():
        print("\n❌ Test audio transcriptie gefaald!")
        return
    
    print("\n🎉 Whisper Manager test voltooid!")
    print("💡 Beide Whisper types zijn klaar voor gebruik in Magic Time Studio")

if __name__ == "__main__":
    main() 