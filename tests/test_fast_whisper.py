"""
Test script voor Fast Whisper
Vergelijkt Fast Whisper met standaard Whisper voor snelheid en kwaliteit
"""

import sys
import os
import time
from pathlib import Path

# Voeg project root toe aan Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_fast_whisper_import():
    """Test of Fast Whisper correct kan worden geïmporteerd"""
    print("🧪 Test Fast Whisper import...")
    
    try:
        from fast_whisper import WhisperModel
        print("✅ Fast Whisper import succesvol!")
        return True
    except ImportError as e:
        print(f"❌ Fast Whisper import gefaald: {e}")
        print("💡 Installeer Fast Whisper met: pip install fast-whisper")
        return False

def test_fast_whisper_processor():
    """Test de Fast Whisper processor"""
    print("\n🧪 Test Fast Whisper processor...")
    
    try:
        from magic_time_studio.processing.fast_whisper_processor import fast_whisper_processor
        
        # Test initialisatie
        print("📋 Beschikbare modellen:")
        models = fast_whisper_processor.get_available_models()
        for model in models:
            print(f"  • {model}")
        
        # Test model laden
        print(f"\n🔧 Test model laden: large-v3-turbo")
        success = fast_whisper_processor.initialize("large-v3-turbo")
        
        if success:
            print("✅ Fast Whisper model succesvol geladen!")
            
            # Toon model informatie
            info = fast_whisper_processor.get_model_info()
            print(f"📊 Model info: {info}")
            
            # Test cleanup
            fast_whisper_processor.cleanup()
            print("✅ Fast Whisper cleanup succesvol!")
            
        else:
            print("❌ Fast Whisper model laden gefaald!")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Fout bij testen Fast Whisper processor: {e}")
        return False

def compare_whisper_speeds():
    """Vergelijk snelheid van Fast Whisper vs standaard Whisper"""
    print("\n🏁 Vergelijk Whisper snelheden...")
    
    # Test bestand (je kunt dit aanpassen naar een echt audio bestand)
    test_audio = "test_audio.wav"  # Vervang door echt bestand
    
    if not os.path.exists(test_audio):
        print(f"⚠️ Test audio bestand niet gevonden: {test_audio}")
        print("💡 Maak een test audio bestand aan om snelheid te vergelijken")
        return
    
    print(f"📁 Test bestand: {test_audio}")
    
    # Test Fast Whisper
    try:
        from magic_time_studio.processing.fast_whisper_processor import fast_whisper_processor
        
        print("\n🚀 Test Fast Whisper (large-v3-turbo)...")
        fast_whisper_processor.initialize("large-v3-turbo")
        
        start_time = time.time()
        result = fast_whisper_processor.transcribe_audio(test_audio)
        fast_whisper_time = time.time() - start_time
        
        if result.get("success"):
            print(f"✅ Fast Whisper voltooid in {fast_whisper_time:.2f} seconden")
            print(f"📝 Tekst: {result['transcript'][:100]}...")
        else:
            print(f"❌ Fast Whisper gefaald: {result.get('error')}")
        
        fast_whisper_processor.cleanup()
        
    except Exception as e:
        print(f"❌ Fast Whisper test gefaald: {e}")
    
    # Test standaard Whisper
    try:
        from magic_time_studio.processing.whisper_processor import whisper_processor
        
        print("\n🐌 Test standaard Whisper (large)...")
        whisper_processor.initialize("large")
        
        start_time = time.time()
        result = whisper_processor.transcribe_audio(test_audio)
        standard_whisper_time = time.time() - start_time
        
        if result.get("success"):
            print(f"✅ Standaard Whisper voltooid in {standard_whisper_time:.2f} seconden")
            print(f"📝 Tekst: {result['transcript'][:100]}...")
        else:
            print(f"❌ Standaard Whisper gefaald: {result.get('error')}")
        
        whisper_processor.cleanup()
        
    except Exception as e:
        print(f"❌ Standaard Whisper test gefaald: {e}")
    
    # Vergelijk snelheden
    try:
        speedup = standard_whisper_time / fast_whisper_time
        print(f"\n📊 Snelheidsvergelijking:")
        print(f"  • Fast Whisper: {fast_whisper_time:.2f}s")
        print(f"  • Standaard Whisper: {standard_whisper_time:.2f}s")
        print(f"  • Snelheidsverbetering: {speedup:.1f}x sneller")
        
        if speedup > 1.5:
            print("🎉 Fast Whisper is significant sneller!")
        elif speedup > 1.1:
            print("✅ Fast Whisper is sneller")
        else:
            print("⚠️ Geen significante snelheidsverbetering")
            
    except:
        print("⚠️ Kon snelheid niet vergelijken")

def main():
    """Hoofdfunctie"""
    print("🤖 Fast Whisper Test Script")
    print("=" * 50)
    
    # Test imports
    if not test_fast_whisper_import():
        print("\n❌ Fast Whisper is niet correct geïnstalleerd!")
        print("💡 Voer eerst het install script uit: python scripts/install_fast_whisper.py")
        return
    
    # Test processor
    if not test_fast_whisper_processor():
        print("\n❌ Fast Whisper processor test gefaald!")
        return
    
    # Vergelijk snelheden
    compare_whisper_speeds()
    
    print("\n🎉 Fast Whisper test voltooid!")
    print("💡 Fast Whisper is klaar voor gebruik in Magic Time Studio")

if __name__ == "__main__":
    main() 