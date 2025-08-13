"""
Core modules voor Magic Time Studio
"""

# Import alle core modules - alleen de basis modules
try:
    from . import config
    from . import logging
    from . import utils
    from . import diagnostics
    print("✅ Core modules geladen")
except ImportError as e:
    print(f"⚠️ Fout bij laden core modules: {e}")

# Versie informatie
__version__ = "2.0.0"
__author__ = "Magic Time Studio Team"
__description__ = "Modulaire versie van Magic Time Studio met gescheiden functionaliteit" 