"""
Magic Time Studio - Hoofdlauncher
Start de applicatie met PyQt6 GUI
"""

import sys
import os
from pathlib import Path

# Voeg project root toe aan Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Start Magic Time Studio met PyQt6 GUI"""
    try:
        # Import en start PyQt6 versie
        from magic_time_studio.main_pyqt6 import main as pyqt6_main
        pyqt6_main()
        
    except ImportError as e:
        print(f"❌ Fout bij importeren PyQt6 modules: {e}")
        print("💡 Zorg ervoor dat PyQt6 is geïnstalleerd: pip install PyQt6")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Onverwachte fout: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 