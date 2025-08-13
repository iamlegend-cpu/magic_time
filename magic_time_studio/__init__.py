"""
Magic Time Studio - Modulaire versie
Een geavanceerde applicatie voor automatische ondertiteling en vertaling van video's
"""

__version__ = "2.0.0"
__author__ = "Magic Time Studio Team"

# Veilige imports met fallbacks
try:
    from magic_time_studio.core.config import *
except ImportError as e:
    print(f"⚠️ Core config import gefaald: {e}")

try:
    from magic_time_studio.core.logging import *
except ImportError as e:
    print(f"⚠️ Core logging import gefaald: {e}")

try:
    from magic_time_studio.core.utils import *
except ImportError as e:
    print(f"⚠️ Core utils import gefaald: {e}") 