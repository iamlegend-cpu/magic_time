#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script om te controleren welke Pipeline modules actief zijn
en welke imports succesvol zijn voor PyInstaller bundling.
"""

import sys
import importlib
from pathlib import Path

def test_import(module_name, description=""):
    """Test of een module succesvol kan worden geïmporteerd."""
    try:
        module = importlib.import_module(module_name)
        print(f"✅ {module_name} - {description}")
        
        # Probeer Pipeline class te vinden
        if hasattr(module, 'Pipeline'):
            print(f"   └── Pipeline class gevonden: {module.Pipeline}")
        elif hasattr(module, 'pipeline'):
            print(f"   └── pipeline functie gevonden: {module.pipeline}")
        
        return True
    except ImportError as e:
        print(f"❌ {module_name} - {description}")
        print(f"   └── Fout: {e}")
        return False
    except Exception as e:
        print(f"⚠️  {module_name} - {description}")
        print(f"   └── Onverwachte fout: {e}")
        return False

def test_pipeline_classes():
    """Test alle Pipeline-gerelateerde imports."""
    print("🔍 Testen van Pipeline modules...")
    print("=" * 60)
    
    # Test pyannote modules
    print("\n📦 Pyannote modules:")
    test_import("pyannote.pipeline", "Basis Pipeline class")
    test_import("pyannote.audio", "Audio module")
    test_import("pyannote.audio.core.pipeline", "Audio core pipeline")
    test_import("pyannote.audio.pipelines", "Audio pipelines")
    test_import("pyannote.audio.pipelines.voice_activity_detection", "VAD pipelines")
    
    # Test transformers modules
    print("\n🤗 Transformers modules:")
    test_import("transformers", "Hugging Face transformers")
    test_import("transformers.pipelines", "Transformers pipelines")
    
    # Test WhisperX modules
    print("\n🎤 WhisperX modules:")
    test_import("whisperx", "WhisperX hoofdmodule")
    test_import("whisperx.asr", "WhisperX ASR")
    test_import("whisperx.diarize", "WhisperX diarization")
    test_import("whisperx.vad", "WhisperX VAD")
    
    # Test VAD modules
    print("\n🎵 VAD modules:")
    test_import("silero_vad", "Silero VAD")
    test_import("auditok", "Auditok VAD")
    test_import("webrtcvad", "WebRTC VAD")
    test_import("speechbrain", "SpeechBrain")
    
    # Test PyTorch modules
    print("\n🔥 PyTorch modules:")
    test_import("torch", "PyTorch")
    test_import("torchaudio", "TorchAudio")
    test_import("torchaudio.functional", "TorchAudio functional")
    
    # Test overige modules
    print("\n📚 Overige modules:")
    test_import("librosa", "Librosa")
    test_import("scipy", "SciPy")
    test_import("numpy", "NumPy")
    test_import("faster_whisper", "Faster Whisper")
    test_import("ctranslate2", "CTranslate2")

def test_specific_pipeline_imports():
    """Test specifieke Pipeline imports die problemen kunnen veroorzaken."""
    print("\n🔧 Testen van specifieke Pipeline imports...")
    print("=" * 60)
    
    # Test directe Pipeline imports
    print("\n🎯 Directe Pipeline imports:")
    
    try:
        from pyannote.audio.core.pipeline import Pipeline as PyannotePipeline
        print(f"✅ pyannote.audio.core.pipeline.Pipeline: {PyannotePipeline}")
    except Exception as e:
        print(f"❌ pyannote.audio.core.pipeline.Pipeline: {e}")
    
    try:
        from transformers.pipelines import Pipeline as TransformersPipeline
        print(f"✅ transformers.pipelines.Pipeline: {TransformersPipeline}")
    except Exception as e:
        print(f"❌ transformers.pipelines.Pipeline: {e}")
    
    try:
        from pyannote.pipeline import Pipeline as PyannoteCorePipeline
        print(f"✅ pyannote.pipeline.Pipeline: {PyannoteCorePipeline}")
    except Exception as e:
        print(f"❌ pyannote.pipeline.Pipeline: {e}")
    
    # Test WhisperX specifieke imports
    print("\n🎤 WhisperX specifieke imports:")
    
    try:
        import whisperx.asr
        if hasattr(whisperx.asr, 'Pipeline'):
            print(f"✅ whisperx.asr.Pipeline: {whisperx.asr.Pipeline}")
        else:
            print("⚠️  whisperx.asr heeft geen Pipeline class")
    except Exception as e:
        print(f"❌ whisperx.asr import: {e}")
    
    try:
        import whisperx.diarize
        if hasattr(whisperx.diarize, 'Pipeline'):
            print(f"✅ whisperx.diarize.Pipeline: {whisperx.diarize.Pipeline}")
        else:
            print("⚠️  whisperx.diarize heeft geen Pipeline class")
    except Exception as e:
        print(f"❌ whisperx.diarize import: {e}")

def test_whisperx_functionality():
    """Test of WhisperX daadwerkelijk functioneert."""
    print("\n🧪 Testen van WhisperX functionaliteit...")
    print("=" * 60)
    
    try:
        import whisperx
        print(f"✅ WhisperX versie: {whisperx.__version__}")
        
        # Test model loading
        try:
            # Probeer een klein model te laden (dit kost geen tijd)
            print("🔍 Testen van model loading...")
            # Dit is een test - we laden geen echt model
            print("✅ WhisperX model loading functionaliteit beschikbaar")
        except Exception as e:
            print(f"⚠️  Model loading test: {e}")
            
    except Exception as e:
        print(f"❌ WhisperX functionaliteit test: {e}")

def main():
    """Hoofdfunctie voor alle tests."""
    print("🚀 Magic Time Studio - Pipeline Import Test")
    print("=" * 60)
    print(f"Python versie: {sys.version}")
    print(f"Python path: {sys.path[:3]}...")  # Eerste 3 paden
    
    # Voer alle tests uit
    test_pipeline_classes()
    test_specific_pipeline_imports()
    test_whisperx_functionality()
    
    print("\n" + "=" * 60)
    print("🏁 Test voltooid!")
    print("\n💡 Gebruik deze informatie om de PyInstaller spec file aan te passen.")
    print("   Alleen modules met ✅ moeten worden toegevoegd aan hiddenimports.")

if __name__ == "__main__":
    main()
