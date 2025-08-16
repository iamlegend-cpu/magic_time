"""
Test bestand voor VAD dependencies
Controleert welke VAD packages beschikbaar zijn
"""

import sys
import os

def test_vad_dependencies():
    """Test welke VAD dependencies beschikbaar zijn"""
    print("🔍 Test VAD dependencies...")
    
    # Test pyannote.audio
    try:
        import pyannote.audio
        print("✅ pyannote.audio beschikbaar")
        print(f"   Versie: {pyannote.audio.__version__}")
    except ImportError:
        print("❌ pyannote.audio niet beschikbaar")
    
    # Test silero
    try:
        import torch
        print("✅ torch beschikbaar")
        print(f"   Versie: {torch.__version__}")
        
        # Test silero VAD
        try:
            from silero_vad import load_model, get_speech_timestamps
            print("✅ silero_vad beschikbaar")
        except ImportError:
            print("❌ silero_vad niet beschikbaar")
    except ImportError:
        print("❌ torch niet beschikbaar")
    
    # Test auditok
    try:
        import auditok
        print("✅ auditok beschikbaar")
        print(f"   Versie: {auditok.__version__}")
    except ImportError:
        print("❌ auditok niet beschikbaar")
    
    # Test whisperx
    try:
        import whisperx
        print("✅ whisperx beschikbaar")
        print(f"   Versie: {whisperx.__version__}")
    except ImportError:
        print("❌ whisperx niet beschikbaar")
    
    # Test CUDA beschikbaarheid
    try:
        import torch
        if torch.cuda.is_available():
            print("✅ CUDA beschikbaar")
            print(f"   CUDA versie: {torch.version.cuda}")
            print(f"   Aantal GPUs: {torch.cuda.device_count()}")
            print(f"   Huidige GPU: {torch.cuda.get_device_name()}")
        else:
            print("❌ CUDA niet beschikbaar")
    except ImportError:
        print("❌ Kan CUDA status niet controleren (torch niet beschikbaar)")
    
    print("\n🔧 VAD dependency test voltooid")

if __name__ == "__main__":
    test_vad_dependencies()
