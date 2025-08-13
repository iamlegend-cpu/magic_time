"""
Magic Time Studio - Root Package
Dit bestand zorgt ervoor dat PyInstaller alle modules correct kan vinden
"""

# Zorg ervoor dat alle modules beschikbaar zijn
try:
    from magic_time_studio.core import *
    from magic_time_studio.app_core import *
    from magic_time_studio.ui_pyqt6 import *
    from magic_time_studio.models import *
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
