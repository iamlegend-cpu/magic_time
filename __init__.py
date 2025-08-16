"""
Magic Time Studio - Root Package
Dit bestand zorgt ervoor dat PyInstaller alle modules correct kan vinden
"""

# Zorg ervoor dat alle modules beschikbaar zijn
try:
    from core import *
    from app_core import *
    from ui_pyside6 import *
    from models import *
    print("✅ Root package: Alle modules geladen")
except ImportError as e:
    print(f"⚠️ Root package: Fout bij laden modules: {e}")

# Export alle belangrijke modules
__all__ = [
    'magic_time_studio',
    'core',
    'app_core', 
    'ui_pyqt6',
    'models'
]
