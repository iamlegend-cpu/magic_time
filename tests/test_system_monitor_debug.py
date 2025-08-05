#!/usr/bin/env python3
"""
Test script voor SystemMonitorWidget debugging
"""

import sys
import os

# Voeg project root toe aan Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer

def test_system_monitor(app):
    """Test SystemMonitorWidget"""
    try:
        from magic_time_studio.ui_pyqt6.features.system_monitor import SystemMonitorWidget
        print("✅ SystemMonitorWidget import succesvol")
        
        # Test widget aanmaken
        monitor = SystemMonitorWidget()
        print("✅ SystemMonitorWidget aangemaakt")
        
        # Test of widget zichtbaar is
        print(f"Widget zichtbaar: {monitor.isVisible()}")
        print(f"Widget grootte: {monitor.size()}")
        print(f"Widget minimum grootte: {monitor.minimumSize()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Fout bij SystemMonitorWidget test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_real_time_chart(app):
    """Test RealTimeChart"""
    try:
        from magic_time_studio.ui_pyqt6.features.real_time_chart import RealTimeChart
        print("✅ RealTimeChart import succesvol")
        
        # Test chart aanmaken
        chart = RealTimeChart("Test Chart")
        print("✅ RealTimeChart aangemaakt")
        
        # Test data toevoegen
        chart.add_data_point(50.0)
        print("✅ Data toegevoegd aan chart")
        
        return True
        
    except Exception as e:
        print(f"❌ Fout bij RealTimeChart test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_charts_panel(app):
    """Test ChartsPanel"""
    try:
        from magic_time_studio.ui_pyqt6.components.charts_panel import ChartsPanel
        print("✅ ChartsPanel import succesvol")
        
        # Test panel aanmaken
        panel = ChartsPanel()
        print("✅ ChartsPanel aangemaakt")
        
        # Test tabs
        print(f"Aantal tabs: {panel.tab_widget.count()}")
        for i in range(panel.tab_widget.count()):
            tab_text = panel.tab_widget.tabText(i)
            print(f"Tab {i}: {tab_text}")
        
        return True
        
    except Exception as e:
        print(f"❌ Fout bij ChartsPanel test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Hoofdfunctie"""
    print("🔍 SystemMonitorWidget Debug Test")
    print("=" * 50)
    
    # Maak QApplication eerst
    app = QApplication(sys.argv)
    print("✅ QApplication aangemaakt")
    
    # Test imports
    print("\n1. Test imports...")
    real_time_ok = test_real_time_chart(app)
    system_monitor_ok = test_system_monitor(app)
    charts_panel_ok = test_charts_panel(app)
    
    if not all([real_time_ok, system_monitor_ok, charts_panel_ok]):
        print("\n❌ Een of meer tests gefaald!")
        return
    
    print("\n✅ Alle imports succesvol!")
    
    # Test met GUI
    print("\n2. Test met GUI...")
    
    # Maak test venster
    window = QMainWindow()
    window.setWindowTitle("SystemMonitorWidget Test")
    window.setGeometry(100, 100, 800, 600)
    
    central_widget = QWidget()
    layout = QVBoxLayout(central_widget)
    
    try:
        from magic_time_studio.ui_pyqt6.components.charts_panel import ChartsPanel
        charts_panel = ChartsPanel()
        layout.addWidget(charts_panel)
        print("✅ ChartsPanel toegevoegd aan GUI")
        
        window.setCentralWidget(central_widget)
        window.show()
        
        print("✅ Test venster getoond")
        print("Controleer of de grafieken zichtbaar zijn...")
        
        # Start timer voor updates
        timer = QTimer()
        timer.timeout.connect(lambda: print("Timer tick"))
        timer.start(5000)  # Elke 5 seconden
        
        app.exec()
        
    except Exception as e:
        print(f"❌ Fout bij GUI test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 