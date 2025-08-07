"""
Test script voor charts panel zonder verwerkings tab
Controleert of de verwerkings tab succesvol is verwijderd
"""

import sys
import os

# Voeg project root toe aan Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt

# Import de charts panel
try:
    from magic_time_studio.ui_pyqt6.components.charts_panel import ChartsPanel
    print("✅ ChartsPanel succesvol geïmporteerd")
except ImportError as e:
    print(f"❌ Import fout: {e}")
    sys.exit(1)

class TestChartsPanelWindow(QMainWindow):
    """Test window voor charts panel zonder verwerkings tab"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test: Charts Panel zonder Verwerkings Tab")
        self.setGeometry(100, 100, 1000, 700)
        
        # Centrale widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout(central_widget)
        
        # Test header
        header = QLabel("📊 Charts Panel Test - Verwerkings Tab Verwijderd")
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
        
        ✅ Charts Panel zonder Verwerkings Tab:
        • Systeem Monitoring tab
        • Performance Metrics tab
        • Geen verwerkingsvoortgang tab meer
        
        🚫 Verwijderd:
        • Verwerkingsvoortgang tab
        • ProcessingProgressChart functionaliteit
        • Charts verwerkings connections
        
        🎯 Beschikbare Tabs:
        • 🖥️ Systeem: System monitoring
        • ⚡ Performance: Performance metrics
        
        📝 Test Functionaliteit:
        • Controleer of alleen 2 tabs zichtbaar zijn
        • Test systeem monitoring functionaliteit
        • Test performance metrics functionaliteit
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
        
        # Charts Panel
        try:
            self.charts_panel = ChartsPanel()
            layout.addWidget(self.charts_panel)
            print("✅ Charts panel geladen")
        except Exception as e:
            print(f"❌ Fout bij laden charts panel: {e}")
            error_label = QLabel(f"❌ Charts panel fout: {e}")
            error_label.setStyleSheet("color: red; padding: 20px;")
            layout.addWidget(error_label)
        
        # Test functionaliteit
        self.test_charts_functionality()
    
    def test_charts_functionality(self):
        """Test de charts functionaliteit zonder verwerkings tab"""
        print("\n🧪 Test charts functionaliteit:")
        
        # Test 1: Check of charts panel bestaat
        if hasattr(self, 'charts_panel'):
            print("✅ Charts panel geladen")
        else:
            print("❌ Charts panel niet geladen")
            return
        
        # Test 2: Check tab widget
        if hasattr(self.charts_panel, 'tab_widget'):
            tab_count = self.charts_panel.tab_widget.count()
            print(f"✅ Tab widget gevonden met {tab_count} tabs")
            
            # Controleer welke tabs er zijn
            expected_tabs = ["🖥️ Systeem", "⚡ Performance"]
            actual_tabs = []
            
            for i in range(tab_count):
                tab_text = self.charts_panel.tab_widget.tabText(i)
                actual_tabs.append(tab_text)
                print(f"  - Tab {i+1}: {tab_text}")
            
            # Controleer of verwerkings tab is verwijderd
            if "🎬 Verwerking" not in actual_tabs:
                print("✅ Verwerkings tab succesvol verwijderd")
            else:
                print("❌ Verwerkings tab nog aanwezig")
            
            # Controleer of verwachte tabs er zijn
            for expected_tab in expected_tabs:
                if expected_tab in actual_tabs:
                    print(f"✅ {expected_tab} tab aanwezig")
                else:
                    print(f"❌ {expected_tab} tab niet gevonden")
        else:
            print("❌ Tab widget niet gevonden")
        
        # Test 3: Check of verwerkings functionaliteit is verwijderd
        if not hasattr(self.charts_panel, 'progress_chart'):
            print("✅ Progress chart verwijderd")
        else:
            print("❌ Progress chart nog aanwezig")
        
        if not hasattr(self.charts_panel, 'start_processing'):
            print("✅ Start processing methode verwijderd")
        else:
            print("❌ Start processing methode nog aanwezig")
        
        if not hasattr(self.charts_panel, 'file_completed'):
            print("✅ File completed methode verwijderd")
        else:
            print("❌ File completed methode nog aanwezig")
        
        if not hasattr(self.charts_panel, 'reset_progress'):
            print("✅ Reset progress methode verwijderd")
        else:
            print("❌ Reset progress methode nog aanwezig")
        
        # Test 4: Check of systeem monitor werkt
        if hasattr(self.charts_panel, 'system_monitor'):
            print("✅ Systeem monitor beschikbaar")
        else:
            print("❌ Systeem monitor niet gevonden")
        
        # Test 5: Check of performance chart werkt
        if hasattr(self.charts_panel, 'performance_chart'):
            print("✅ Performance chart beschikbaar")
        else:
            print("❌ Performance chart niet gevonden")
        
        print("\n📋 Gebruik instructies:")
        print("• Bekijk de beschikbare tabs in het charts panel")
        print("• Test systeem monitoring functionaliteit")
        print("• Test performance metrics functionaliteit")
        print("• Verwerkings tab zou niet meer zichtbaar moeten zijn")

def main():
    """Main functie"""
    print("🚀 Start test charts panel zonder verwerkings tab...")
    
    app = QApplication(sys.argv)
    
    # Test window
    window = TestChartsPanelWindow()
    window.show()
    
    print("✅ Test window geopend")
    print("📝 Charts panel zonder verwerkings tab is nu beschikbaar")
    print("🚫 Verwerkings tab is verwijderd")
    
    # Start event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 