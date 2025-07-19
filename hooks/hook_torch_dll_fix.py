import os
import sys

# Runtime hook om PyTorch DLL loading te fixen
def _fix_torch_dll():
    """Fix PyTorch DLL loading in frozen applications"""
    try:
        if hasattr(sys, '_MEIPASS'):
            # In frozen applicatie - voeg torch/lib toe aan PATH
            torch_lib_path = os.path.join(sys._MEIPASS, 'torch', 'lib')
            if os.path.exists(torch_lib_path):
                os.environ['PATH'] = torch_lib_path + os.pathsep + os.environ.get('PATH', '')
    except Exception:
        pass  # Als er iets misgaat, ga door

# Voer de fix uit bij import
_fix_torch_dll() 