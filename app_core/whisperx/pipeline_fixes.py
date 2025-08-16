"""
Pipeline import fixes voor WhisperX
Handelt import conflicten en PyInstaller bundling af
"""

import os
import sys

def fix_pipeline_imports():
    """Fix Pipeline import conflicten voor PyInstaller bundling"""
    try:
        # Probeer eerst de normale imports
        import whisperx
        return True
    except ImportError as e:
        if "Pipeline" in str(e):
            print("🔧 Pipeline import conflict gedetecteerd - probeer alternatieve imports...")
            
            # Injecteer Pipeline classes in sys.modules
            try:
                # Pyannote audio Pipeline
                from pyannote.audio.core.pipeline import Pipeline as PyannoteAudioPipeline
                sys.modules['pyannote.audio.core.pipeline.Pipeline'] = PyannoteAudioPipeline
                print("✅ pyannote.audio.core.pipeline.Pipeline geïnjecteerd")
            except:
                pass
            
            try:
                # Transformers Pipeline
                from transformers.pipelines import Pipeline as TransformersPipeline
                sys.modules['transformers.pipelines.Pipeline'] = TransformersPipeline
                print("✅ transformers.pipelines.Pipeline geïnjecteerd")
            except:
                pass
            
            try:
                # Pyannote core Pipeline
                from pyannote.pipeline import Pipeline as PyannoteCorePipeline
                sys.modules['pyannote.pipeline.Pipeline'] = PyannoteCorePipeline
                print("✅ pyannote.pipeline.Pipeline geïnjecteerd")
            except:
                pass
            
            # Probeer opnieuw whisperx te importeren
            try:
                import whisperx
                print("✅ WhisperX import succesvol na Pipeline fix")
                return True
            except Exception as e2:
                print(f"❌ WhisperX import nog steeds gefaald: {e2}")
                return False
        else:
            print(f"❌ Andere import fout: {e}")
            return False

def get_meipass_path():
    """Krijg het MEIPASS pad voor PyInstaller bundling"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller bundling
        return sys._MEIPASS
    else:
        # Normale Python omgeving
        return os.path.dirname(os.path.abspath(__file__))

def setup_pyinstaller_paths():
    """Setup paden voor PyInstaller bundling"""
    meipass_path = get_meipass_path()
    
    # Voeg MEIPASS aan Python path toe
    if meipass_path not in sys.path:
        sys.path.insert(0, meipass_path)
        print(f"🔧 MEIPASS pad toegevoegd: {meipass_path}")
    
    # Voeg ook de parent directory toe voor magic_time_studio imports
    parent_dir = os.path.dirname(meipass_path)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
        print(f"🔧 Parent directory toegevoegd: {parent_dir}")
    
    return meipass_path

def force_pipeline_imports():
    """Forceer Pipeline imports door ze direct te laden"""
    try:
        print("🔧 Forceer Pipeline imports...")
        
        # Laad alle Pipeline classes direct
        import pyannote.audio.core.pipeline
        import pyannote.pipeline
        import transformers.pipelines
        
        # Maak aliassen voor Pipeline classes
        PyannoteAudioPipeline = pyannote.audio.core.pipeline.Pipeline
        PyannoteCorePipeline = pyannote.pipeline.Pipeline
        TransformersPipeline = transformers.pipelines.Pipeline
        
        # Injecteer in sys.modules
        sys.modules['pyannote.audio.core.pipeline.Pipeline'] = PyannoteAudioPipeline
        sys.modules['pyannote.pipeline.Pipeline'] = PyannoteCorePipeline
        sys.modules['transformers.pipelines.Pipeline'] = TransformersPipeline
        
        # Maak een globale Pipeline alias
        class PipelineAlias:
            """Alias class die beide Pipeline types kan afhandelen."""
            
            def __new__(cls, *args, **kwargs):
                # Probeer eerst pyannote.audio Pipeline
                try:
                    return PyannoteAudioPipeline(*args, **kwargs)
                except:
                    # Fallback naar transformers Pipeline
                    try:
                        return TransformersPipeline(*args, **kwargs)
                    except:
                        # Laatste fallback naar pyannote core Pipeline
                        return PyannoteCorePipeline(*args, **kwargs)
        
        # Injecteer de alias
        sys.modules['Pipeline'] = PipelineAlias
        globals()['Pipeline'] = PipelineAlias
        
        print("✅ Pipeline imports geforceerd")
        return True
        
    except Exception as e:
        print(f"❌ Pipeline imports forceren gefaald: {e}")
        return False

def initialize_pipeline_fixes():
    """Initialiseer alle Pipeline fixes"""
    # Fix Pipeline imports voordat we verder gaan
    if not fix_pipeline_imports():
        print("⚠️ Pipeline import fix gefaald - probeer geforceerde imports...")
        if not force_pipeline_imports():
            print("❌ Alle Pipeline import fixes gefaald - WhisperX functionaliteit mogelijk beperkt")
    
    # Setup PyInstaller paden
    meipass_path = setup_pyinstaller_paths()
    
    # Forceer Pipeline imports nogmaals
    force_pipeline_imports()
    
    return meipass_path
