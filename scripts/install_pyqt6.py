#!/usr/bin/env python3
"""
Installatie script voor PyQt6 dependencies
"""

import subprocess
import sys
import os

def install_pyqt6():
    """Installeer PyQt6 dependencies"""
    print("🚀 Installeren van PyQt6 dependencies...")
    
    try:
        # Installeer PyQt6
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt6>=6.5.0"])
        print("✅ PyQt6 geïnstalleerd")
        
        # Installeer extra PyQt6 modules
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt6-Qt6>=6.5.0"])
        print("✅ PyQt6-Qt6 geïnstalleerd")
        
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt6-sip>=13.5.0"])
        print("✅ PyQt6-sip geïnstalleerd")
        
        print("\n🎉 PyQt6 installatie voltooid!")
        print("Je kunt nu de PyQt6 versie starten met: python run_pyqt6.py")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Fout bij installeren: {e}")
        return False
    
    return True

def test_pyqt6():
    """Test of PyQt6 correct is geïnstalleerd"""
    print("🧪 Testen van PyQt6 installatie...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import Qt
        print("✅ PyQt6 import succesvol")
        
        # Test een eenvoudige applicatie
        app = QApplication([])
        print("✅ PyQt6 applicatie gestart")
        app.quit()
        print("✅ PyQt6 test voltooid")
        
        return True
        
    except ImportError as e:
        print(f"❌ PyQt6 import fout: {e}")
        return False
    except Exception as e:
        print(f"❌ PyQt6 test fout: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Magic Time Studio - PyQt6 Installatie")
    print("=" * 50)
    
    # Installeer PyQt6
    if install_pyqt6():
        # Test de installatie
        if test_pyqt6():
            print("\n🎉 Alles is klaar! Je kunt nu de PyQt6 versie gebruiken.")
        else:
            print("\n⚠️ Er zijn problemen met de PyQt6 installatie.")
    else:
        print("\n❌ Installatie gefaald.") 