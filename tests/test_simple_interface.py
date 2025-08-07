"""
Test script voor vereenvoudigde interface
Controleert of de interface werkt zonder VLC, Whisper en verwerkings functionaliteit
"""

import sys
import os

# Voeg project root toe aan Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt

# Import de vereenvoudigde interface
try:
    from magic_time_studio.ui_pyqt6.features.subtitle_preview import SubtitlePreviewWidget
    print("✅ SubtitlePreviewWidget (vereenvoudigd) succesvol geïmporteerd")
except ImportError as e:
    print(f"❌ Import fout: {e}")
    sys.exit(1)

class TestSimpleInterfaceWindow(QMainWindow):
    """Test window voor vereenvoudigde interface"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test: Vereenvoudigde Interface")
        self.setGeometry(100, 100, 800, 600)
        
        # Centrale widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout(central_widget)
        
        # Test header
        header = QLabel("🎬 Vereenvoudigde Interface Test")
        header.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #ffffff;
                background-color: #2d2d2d;
                padding: 10px;
                border-radius: 5px;
                margin: 5px;
            }
        """)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Test instructies
        instructions = QLabel("""
        📋 Test Instructies:
        
        ✅ Vereenvoudigde Interface:
        • Eenvoudige informatie weergave
        • Status logging functionaliteit
        • Drag & drop voor bestanden
        • Geen VLC video player
        • Geen Whisper evaluatie
        • Geen verwerkings functionaliteit
        
        🎯 Functionaliteit:
        • Sleep bestanden naar de interface
        • Bekijk status informatie
        • Eenvoudige logging van acties
        
        🚫 Verwijderd:
        • VLC video player
        • Whisper model evaluatie
        • Verwerkings tabs en functionaliteit
        • Complexe subtitle preview
        """)
        instructions.setStyleSheet("""
            QLabel {
                background-color: #1e1e1e;
                border: 1px solid #444444;
                border-radius: 3px;
                padding: 10px;
                margin: 5px;
                color: #cccccc;
                font-size: 11px;
                line-height: 1.4;
            }
        """)
        layout.addWidget(instructions)
        
        # Test controls
        test_controls = QWidget()
        test_layout = QHBoxLayout(test_controls)
        
        # Test knoppen
        test_status_btn = QPushButton("📊 Test Status Update")
        test_status_btn.clicked.connect(self.test_status_update)
        test_layout.addWidget(test_status_btn)
        
        test_drag_btn = QPushButton("🖱️ Test Drag & Drop")
        test_drag_btn.clicked.connect(self.test_drag_drop)
        test_layout.addWidget(test_drag_btn)
        
        test_layout.addStretch()
        
        layout.addWidget(test_controls)
        
        # Interface
        try:
            self.interface = SubtitlePreviewWidget()
            layout.addWidget(self.interface)
            print("✅ Vereenvoudigde interface geladen")
        except Exception as e:
            print(f"❌ Fout bij laden interface: {e}")
            error_label = QLabel(f"❌ Interface fout: {e}")
            error_label.setStyleSheet("color: red; padding: 20px;")
            layout.addWidget(error_label)
        
        # Test functionaliteit
        self.test_simple_functionality()
    
    def test_simple_functionality(self):
        """Test de vereenvoudigde functionaliteit"""
        print("\n🧪 Test vereenvoudigde functionaliteit:")
        
        # Test 1: Check of VLC is verwijderd
        if hasattr(self, 'interface'):
            if not hasattr(self.interface, 'vlc_player'):
                print("✅ VLC video player verwijderd")
            else:
                print("❌ VLC video player nog aanwezig")
            
            if not hasattr(self.interface, 'model_combo'):
                print("✅ Whisper model selectie verwijderd")
            else:
                print("❌ Whisper model selectie nog aanwezig")
            
            if not hasattr(self.interface, 'evaluate_btn'):
                print("✅ Whisper evaluatie button verwijderd")
            else:
                print("❌ Whisper evaluatie button nog aanwezig")
        
        # Test 2: Check of status functionaliteit werkt
        if hasattr(self, 'interface') and hasattr(self.interface, 'update_status'):
            print("✅ Status update functionaliteit beschikbaar")
        else:
            print("❌ Status update functionaliteit niet gevonden")
        
        # Test 3: Check of drag & drop werkt
        if hasattr(self, 'interface') and hasattr(self.interface, 'files_dropped'):
            print("✅ Drag & drop functionaliteit beschikbaar")
        else:
            print("❌ Drag & drop functionaliteit niet gevonden")
        
        # Test 4: Check of status text area bestaat
        if hasattr(self, 'interface') and hasattr(self.interface, 'status_text'):
            print("✅ Status text area beschikbaar")
        else:
            print("❌ Status text area niet gevonden")
        
        print("\n📋 Gebruik instructies:")
        print("• Sleep bestanden naar de interface")
        print("• Bekijk status informatie in het tekstveld")
        print("• Gebruik de test knoppen voor functionaliteit")
        print("• Eenvoudige interface zonder complexe features")
    
    def test_status_update(self):
        """Test status update functionaliteit"""
        print("🧪 Test status update...")
        
        if hasattr(self, 'interface') and hasattr(self.interface, 'update_status'):
            self.interface.update_status("Test status update uitgevoerd")
            print("✅ Status update uitgevoerd")
        else:
            print("❌ Status update functie niet gevonden")
    
    def test_drag_drop(self):
        """Test drag & drop functionaliteit"""
        print("🧪 Test drag & drop...")
        
        if hasattr(self, 'interface') and hasattr(self.interface, 'files_dropped'):
            print("✅ Drag & drop functionaliteit beschikbaar")
            print("📝 Sleep bestanden naar de interface om te testen")
        else:
            print("❌ Drag & drop functionaliteit niet gevonden")

def main():
    """Main functie"""
    print("🚀 Start test vereenvoudigde interface...")
    
    app = QApplication(sys.argv)
    
    # Test window
    window = TestSimpleInterfaceWindow()
    window.show()
    
    print("✅ Test window geopend")
    print("📝 Vereenvoudigde interface is nu beschikbaar")
    print("🚫 Alle complexe functionaliteit is verwijderd")
    
    # Start event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 