"""
Test script voor Whisper-only interface
Controleert of de interface alleen Whisper evaluatie heeft zonder subtitle preview
"""

import sys
import os

# Voeg project root toe aan Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt

# Import de aangepaste interface
try:
    from magic_time_studio.ui_pyqt6.features.subtitle_preview import SubtitlePreviewWidget
    print("✅ SubtitlePreviewWidget (Whisper-only) succesvol geïmporteerd")
except ImportError as e:
    print(f"❌ Import fout: {e}")
    sys.exit(1)

class TestWhisperOnlyWindow(QMainWindow):
    """Test window voor Whisper-only interface"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test: Whisper-Only Interface")
        self.setGeometry(100, 100, 1400, 900)
        
        # Centrale widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout(central_widget)
        
        # Test header
        header = QLabel("🤖 Whisper-Only Interface Test")
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
        
        ✅ Whisper-Only Interface:
        • Video player met resize functionaliteit
        • Whisper model evaluatie zonder subtitle preview
        • Model vergelijking en aanbevelingen
        • Geen subtitle preview tekst meer
        
        🎥 Functionaliteit:
        • Sleep video bestanden naar de video player
        • Kies Whisper model (tiny, base, small, medium, large)
        • Klik 'Evalueer' voor model analyse
        • Bekijk aanbevelingen voor optimale kwaliteit
        • Gebruik video resize opties
        
        🚫 Verwijderd:
        • Subtitle preview text area
        • Subtitle loading functionaliteit
        • Sync offset controls
        • Subtitle timing issues
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
        test_whisper_btn = QPushButton("🤖 Test Whisper Evaluatie")
        test_whisper_btn.clicked.connect(self.test_whisper_evaluation)
        test_layout.addWidget(test_whisper_btn)
        
        test_video_btn = QPushButton("🎬 Test Video Player")
        test_video_btn.clicked.connect(self.test_video_player)
        test_layout.addWidget(test_video_btn)
        
        test_resize_btn = QPushButton("📐 Test Resize")
        test_resize_btn.clicked.connect(self.test_resize_functionality)
        test_layout.addWidget(test_resize_btn)
        
        test_layout.addStretch()
        
        layout.addWidget(test_controls)
        
        # Interface
        try:
            self.interface = SubtitlePreviewWidget()
            layout.addWidget(self.interface)
            print("✅ Whisper-only interface geladen")
        except Exception as e:
            print(f"❌ Fout bij laden interface: {e}")
            error_label = QLabel(f"❌ Interface fout: {e}")
            error_label.setStyleSheet("color: red; padding: 20px;")
            layout.addWidget(error_label)
        
        # Test functionaliteit
        self.test_whisper_only_functionality()
    
    def test_whisper_only_functionality(self):
        """Test de Whisper-only functionaliteit"""
        print("\n🧪 Test Whisper-only functionaliteit:")
        
        # Test 1: Check of subtitle preview is verwijderd
        if hasattr(self, 'interface'):
            if not hasattr(self.interface, 'subtitle_text'):
                print("✅ Subtitle preview text area verwijderd")
            else:
                print("❌ Subtitle preview text area nog aanwezig")
            
            if not hasattr(self.interface, 'load_subtitle_button'):
                print("✅ Subtitle load button verwijderd")
            else:
                print("❌ Subtitle load button nog aanwezig")
            
            if not hasattr(self.interface, 'sync_offset_input'):
                print("✅ Sync offset input verwijderd")
            else:
                print("❌ Sync offset input nog aanwezig")
        
        # Test 2: Check of Whisper evaluatie werkt
        if hasattr(self, 'interface') and hasattr(self.interface, 'evaluate_whisper_model'):
            print("✅ Whisper evaluatie functionaliteit beschikbaar")
        else:
            print("❌ Whisper evaluatie functionaliteit niet gevonden")
        
        # Test 3: Check of model selectie werkt
        if hasattr(self, 'interface') and hasattr(self.interface, 'model_combo'):
            print("✅ Model selectie beschikbaar")
        else:
            print("❌ Model selectie niet gevonden")
        
        # Test 4: Check of video player werkt
        if hasattr(self, 'interface') and hasattr(self.interface, 'vlc_player'):
            print("✅ Video player beschikbaar")
        else:
            print("❌ Video player niet gevonden")
        
        print("\n📋 Gebruik instructies:")
        print("• Sleep video bestanden naar de video player")
        print("• Kies Whisper model en klik 'Evalueer'")
        print("• Bekijk evaluatie resultaten in rechter paneel")
        print("• Gebruik video resize opties")
        print("• Geen subtitle preview meer - alleen Whisper evaluatie")
    
    def test_whisper_evaluation(self):
        """Test Whisper evaluatie"""
        print("🧪 Test Whisper evaluatie...")
        
        if hasattr(self, 'interface') and hasattr(self.interface, 'evaluate_whisper_model'):
            self.interface.evaluate_whisper_model()
            print("✅ Whisper evaluatie uitgevoerd")
        else:
            print("❌ Whisper evaluatie functie niet gevonden")
    
    def test_video_player(self):
        """Test video player functionaliteit"""
        print("🧪 Test video player...")
        
        if hasattr(self, 'interface') and hasattr(self.interface, 'vlc_player'):
            print("✅ Video player beschikbaar")
            print("📝 Gebruik drag & drop voor video bestanden")
        else:
            print("❌ Video player niet gevonden")
    
    def test_resize_functionality(self):
        """Test resize functionaliteit"""
        print("🧪 Test resize functionaliteit...")
        
        if hasattr(self, 'interface') and hasattr(self.interface, 'vlc_player'):
            if hasattr(self.interface.vlc_player, 'resize_button'):
                print("✅ Resize button beschikbaar")
            else:
                print("❌ Resize button niet gevonden")
        else:
            print("❌ Video player niet gevonden")

def main():
    """Main functie"""
    print("🚀 Start test Whisper-only interface...")
    
    app = QApplication(sys.argv)
    
    # Test window
    window = TestWhisperOnlyWindow()
    window.show()
    
    print("✅ Test window geopend")
    print("📝 Whisper-only interface is nu beschikbaar")
    print("🚫 Subtitle preview functionaliteit is verwijderd")
    
    # Start event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 