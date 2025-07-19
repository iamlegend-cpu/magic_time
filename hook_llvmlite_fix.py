import os
import sys

# Runtime hook om llvmlite DLL loading te fixen
def _fix_llvmlite_dll():
    """Fix llvmlite DLL loading in frozen applications"""
    try:
        if hasattr(sys, '_MEIPASS'):
            # Voeg zowel de hoofdmap als de llvmlite\binding submap toe aan PATH
            os.environ['PATH'] = (
                sys._MEIPASS + os.pathsep +
                os.path.join(sys._MEIPASS, "llvmlite", "binding") + os.pathsep +
                os.environ.get('PATH', '')
            )
    except Exception:
        pass  # Als er iets misgaat, ga door

# Voer de fix uit bij import
_fix_llvmlite_dll() 