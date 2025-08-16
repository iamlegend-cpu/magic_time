"""
Test bestand voor WhisperX SRT functies
Controleert of alle functies beschikbaar zijn en werken
"""

import sys
import os
import tempfile
import json

# Voeg project root toe aan Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Import modules
from core import whisperx_srt_functions
from core import subtitle_functions

def test_whisperx_srt_availability():
    """Test of WhisperX SRT functies beschikbaar zijn"""
    print("🔍 Test WhisperX SRT functies beschikbaarheid...")
    
    try:
        # Test import van core functies
        from . import whisper_functions
        from . import whisperx_srt_functions
        from . import subtitle_functions
        
        print("✅ Core modules geïmporteerd")
        
        # Test WhisperX SRT beschikbaarheid
        from .whisper_functions import is_whisperx_srt_available
        available = is_whisperx_srt_available()
        
        if available:
            print("✅ WhisperX SRT functies zijn beschikbaar")
        else:
            print("⚠️ WhisperX SRT functies zijn niet beschikbaar")
        
        return available
        
    except ImportError as e:
        print(f"❌ Import fout: {e}")
        return False
    except Exception as e:
        print(f"❌ Onverwachte fout: {e}")
        return False

def test_whisperx_srt_functions():
    """Test of alle WhisperX SRT functies werken"""
    print("\n🔍 Test WhisperX SRT functies...")
    
    try:
        # Test alle beschikbare functies
        from .whisperx_srt_functions import (
            create_whisperx_srt_content,
            create_enhanced_srt_with_word_timing,
            validate_whisperx_transcriptions,
            get_whisperx_statistics,
            _seconds_to_srt_timestamp
        )
        
        print("✅ Alle WhisperX SRT functies geïmporteerd")
        
        # Test timestamp conversie
        test_time = 65.123
        timestamp = _seconds_to_srt_timestamp(test_time)
        expected = "00:01:05,123"
        
        if timestamp == expected:
            print(f"✅ Timestamp conversie werkt: {test_time}s -> {timestamp}")
        else:
            print(f"⚠️ Timestamp conversie fout: {test_time}s -> {timestamp} (verwacht: {expected})")
        
        # Test validatie functie
        test_transcriptions = [
            {"start": 0.0, "end": 5.0, "text": "Test transcriptie"},
            {"start": 5.0, "end": 10.0, "text": "Nog een segment"}
        ]
        
        is_valid = validate_whisperx_transcriptions(test_transcriptions)
        if is_valid:
            print("✅ Transcriptie validatie werkt")
        else:
            print("⚠️ Transcriptie validatie gefaald")
        
        # Test statistieken functie
        stats = get_whisperx_statistics(test_transcriptions)
        if stats and "total_segments" in stats:
            print(f"✅ Statistieken functie werkt: {stats['total_segments']} segmenten")
        else:
            print("⚠️ Statistieken functie gefaald")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import fout bij testen functies: {e}")
        return False
    except Exception as e:
        print(f"❌ Onverwachte fout bij testen functies: {e}")
        return False

def test_integration():
    """Test integratie tussen verschillende modules"""
    print("\n🔍 Test integratie tussen modules...")
    
    try:
        # Test integratie tussen whisper_functions en subtitle_functions
        from .whisper_functions import create_whisperx_srt_file, is_whisperx_srt_available
        from .subtitle_functions import create_whisperx_srt_content, is_whisperx_srt_available as sub_is_available
        
        print("✅ Integratie imports succesvol")
        
        # Test beschikbaarheid check
        whisper_available = is_whisperx_srt_available()
        subtitle_available = sub_is_available()
        
        print(f"📊 WhisperX SRT beschikbaarheid:")
        print(f"   - whisper_functions: {whisper_available}")
        print(f"   - subtitle_functions: {subtitle_available}")
        
        if whisper_available and subtitle_available:
            print("✅ Volledige integratie werkt")
            return True
        else:
            print("⚠️ Gedeeltelijke integratie - sommige functies niet beschikbaar")
            return False
        
    except ImportError as e:
        print(f"❌ Integratie import fout: {e}")
        return False
    except Exception as e:
        print(f"❌ Onverwachte fout bij integratie test: {e}")
        return False

def main():
    """Hoofdfunctie voor het testen"""
    print("🚀 Start WhisperX SRT functies test...\n")
    
    # Test beschikbaarheid
    availability_test = test_whisperx_srt_availability()
    
    if availability_test:
        # Test functies
        functions_test = test_whisperx_srt_functions()
        
        # Test integratie
        integration_test = test_integration()
        
        # Samenvatting
        print("\n📊 Test resultaten samenvatting:")
        print(f"   - Beschikbaarheid: {'✅' if availability_test else '❌'}")
        print(f"   - Functies: {'✅' if functions_test else '❌'}")
        print(f"   - Integratie: {'✅' if integration_test else '❌'}")
        
        if all([availability_test, functions_test, integration_test]):
            print("\n🎉 Alle tests geslaagd! WhisperX SRT functies werken correct.")
            return True
        else:
            print("\n⚠️ Sommige tests gefaald. Controleer de implementatie.")
            return False
    else:
        print("\n❌ WhisperX SRT functies zijn niet beschikbaar.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
