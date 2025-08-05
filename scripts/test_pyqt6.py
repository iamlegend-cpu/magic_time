#!/usr/bin/env python3
"""
Test script voor PyQt6 versie van Magic Time Studio
"""

import sys
import os
import time

# Voeg de project directory toe aan Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

def test_pyqt6_import():
    """Test of PyQt6 correct kan worden geïmporteerd"""
    print("🧪 Testen van PyQt6 imports...")
    
    try:
        from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
        from PyQt6.QtCore import Qt, pyqtSignal
        from PyQt6.QtGui import QIcon
        print("✅ PyQt6 imports succesvol")
        return True
    except ImportError as e:
        print(f"❌ PyQt6 import fout: {e}")
        return False

def test_magic_time_pyqt6():
    """Test of Magic Time Studio PyQt6 modules kunnen worden geïmporteerd"""
    print("🧪 Testen van Magic Time Studio PyQt6 modules...")
    
    try:
        from magic_time_studio.ui_pyqt6.main_window import MainWindow
        from magic_time_studio.ui_pyqt6.themes import ThemeManager
        print("✅ Magic Time Studio PyQt6 modules succesvol")
        return True
    except ImportError as e:
        print(f"❌ Magic Time Studio PyQt6 import fout: {e}")
        return False

def test_simple_pyqt6_app():
    """Test een eenvoudige PyQt6 applicatie"""
    print("🧪 Testen van eenvoudige PyQt6 applicatie...")
    
    try:
        from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
        from PyQt6.QtCore import QTimer
        
        app = QApplication([])
        
        # Maak een eenvoudig venster
        window = QMainWindow()
        window.setWindowTitle("PyQt6 Test")
        window.setGeometry(100, 100, 400, 300)
        
        # Maak centrale widget
        central_widget = QWidget()
        window.setCentralWidget(central_widget)
        
        # Maak layout
        layout = QVBoxLayout(central_widget)
        
        # Maak test knop
        button = QPushButton("Test Knop")
        button.clicked.connect(lambda: print("✅ PyQt6 knop werkt!"))
        layout.addWidget(button)
        
        # Toon venster
        window.show()
        
        # Sluit na 2 seconden
        timer = QTimer()
        timer.timeout.connect(app.quit)
        timer.start(2000)
        
        # Start event loop
        app.exec()
        
        print("✅ PyQt6 applicatie test succesvol")
        return True
        
    except Exception as e:
        print(f"❌ PyQt6 applicatie test fout: {e}")
        return False

def test_magic_time_pyqt6_app():
    """Test Magic Time Studio PyQt6 applicatie"""
    print("🧪 Testen van Magic Time Studio PyQt6 applicatie...")
    
    try:
        from magic_time_studio.main_pyqt6 import MagicTimeStudioPyQt6
        
        # Maak applicatie
        app = MagicTimeStudioPyQt6()
        
        # Test UI creatie
        app.create_ui()
        
        print("✅ Magic Time Studio PyQt6 applicatie test succesvol")
        return True
        
    except Exception as e:
        print(f"❌ Magic Time Studio PyQt6 applicatie test fout: {e}")
        return False

def main():
    """Hoofdfunctie voor tests"""
    print("=" * 60)
    print("Magic Time Studio - PyQt6 Test Suite")
    print("=" * 60)
    
    tests = [
        ("PyQt6 Imports", test_pyqt6_import),
        ("Magic Time Studio PyQt6 Modules", test_magic_time_pyqt6),
        ("Eenvoudige PyQt6 Applicatie", test_simple_pyqt6_app),
        ("Magic Time Studio PyQt6 Applicatie", test_magic_time_pyqt6_app)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 40)
        
        try:
            if test_func():
                print(f"✅ {test_name} - GESLAAGD")
                passed += 1
            else:
                print(f"❌ {test_name} - GEFAALD")
        except Exception as e:
            print(f"❌ {test_name} - FOUT: {e}")
    
    print("\n" + "=" * 60)
    print(f"Test Resultaten: {passed}/{total} tests geslaagd")
    
    if passed == total:
        print("🎉 Alle tests geslaagd! PyQt6 is klaar voor gebruik.")
        print("\nJe kunt nu de PyQt6 versie starten met:")
        print("  python run_pyqt6.py")
        print("  python magic_time_studio/run.py --pyqt6")
    else:
        print("⚠️ Sommige tests gefaald. Controleer de installatie.")
        print("\nInstalleer PyQt6 met:")
        print("  python install_pyqt6.py")
    
    print("=" * 60)

if __name__ == "__main__":
    main() 