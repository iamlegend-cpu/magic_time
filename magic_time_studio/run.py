"""
Magic Time Studio - Hoofdlauncher
Start de applicatie met PyQt6 GUI

Gebruik:
1. Zorg dat je in de project root directory bent
2. Activeer je virtual environment: pyqt_venv\Scripts\activate (Windows)
3. Start het programma: python magic_time_studio/run.py

Dependencies:
- Vereist: PyQt6, numpy
- Optioneel: torch, whisper, librosa (voor volledige functionaliteit)
"""

import sys
import os
from pathlib import Path
import traceback

def setup_environment():
    """Setup de Python omgeving voor Magic Time Studio"""
    # Voeg project root toe aan Python path
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    
    # Voeg magic_time_studio directory toe aan path
    studio_path = Path(__file__).parent
    sys.path.insert(0, str(studio_path))
    
    # Stel werkdirectory in naar project root
    os.chdir(project_root)
    
    # Alleen essentiële informatie tonen
    print(f"🚀 Magic Time Studio wordt gestart...")
    print(f"📁 Project root: {project_root}")

def check_dependencies():
    """Controleer of alle benodigde dependencies beschikbaar zijn"""
    required_packages = [
        'PyQt6',
        'numpy'
    ]
    
    # Optionele packages die later geladen kunnen worden
    optional_packages = [
        'torch',
        'whisper',
        'librosa'  # Verplaatst naar optioneel
    ]
    
    missing_required = []
    missing_optional = []
    
    # Controleer required packages
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} - Beschikbaar")
        except ImportError:
            missing_required.append(package)
            print(f"❌ {package} - Niet beschikbaar")
    
    # Controleer optionele packages
    for package in optional_packages:
        try:
            __import__(package)
            print(f"✅ {package} - Beschikbaar")
        except ImportError:
            missing_optional.append(package)
            print(f"⚠️  {package} - Niet beschikbaar")
    
    if missing_required:
        print(f"\n❌ Ontbrekende required packages: {', '.join(missing_required)}")
        print("💡 Deze packages zijn essentieel om het programma te starten")
        return False
    
    if missing_optional:
        print(f"\n⚠️  Ontbrekende optionele packages: {', '.join(missing_optional)}")
        if 'whisper' in missing_optional:
            print("💡 Whisper is nodig voor transcriptie functionaliteit")
        if 'librosa' in missing_optional:
            print("💡 Librosa is nodig voor geavanceerde audio analyse")
        if 'torch' in missing_optional:
            print("💡 PyTorch is nodig voor whisper modellen")
        print("💡 Het programma kan starten maar sommige features werken niet")
    
    return True

def main():
    """Start Magic Time Studio met PyQt6 GUI"""
    try:
        # Setup omgeving
        setup_environment()
        
        # Controleer dependencies
        print("\n🔍 Controleer dependencies...")
        if not check_dependencies():
            print("\n❌ Kan niet starten - ontbrekende dependencies")
            return 1
        
        print("\n✅ Alle dependencies beschikbaar!")
        print("🚀 Start Magic Time Studio...")
        
        # Import en start de applicatie via main_entry
        from app_core.main_entry import main as studio_main
        return studio_main()
        
    except ImportError as e:
        print(f"\n❌ Fout bij importeren PyQt6 modules: {e}")
        print("💡 Zorg ervoor dat alle dependencies zijn geïnstalleerd in je virtual environment")
        print("💡 Activeer je virtual environment: pyqt_venv\\Scripts\\activate")
        print("💡 Installeer ontbrekende packages: pip install PyQt6 numpy")
        return 1
    except Exception as e:
        print(f"\n❌ Onverwachte fout: {e}")
        print("💡 Controleer of alle bestanden aanwezig zijn")
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n💥 Onherstelbare fout: {e}")
        sys.exit(1) 