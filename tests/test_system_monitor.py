#!/usr/bin/env python3
"""
Test script voor de Enhanced System Monitor Plugin
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer

from magic_time_studio.ui_pyqt6.features.plugins.system_monitor_plugin import EnhancedSystemMonitorPlugin

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System Monitor Plugin Test")
        self.setGeometry(100, 100, 800, 600)
        
        # Maak centrale widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Maak plugin instance
        self.plugin = EnhancedSystemMonitorPlugin(self)
        self.plugin.initialize()
        
        # Krijg plugin widget
        plugin_widget = self.plugin.get_widget()
        layout.addWidget(plugin_widget)
        
        print("✅ Plugin widget succesvol geladen")
        print("📊 Plugin bevat de volgende tabs:")
        
        # Zoek naar tab widget
        from PyQt6.QtWidgets import QTabWidget
        tab_widget = plugin_widget.findChild(QTabWidget)
        if tab_widget:
            for i in range(tab_widget.count()):
                tab_name = tab_widget.tabText(i)
                print(f"  - {tab_name}")
        
        # Test monitoring thread
        QTimer.singleShot(2000, self.test_monitoring)
    
    def test_monitoring(self):
        """Test monitoring functionaliteit"""
        print("\n🧪 Test monitoring functionaliteit...")
        
        # Start monitoring
        if hasattr(self.plugin, 'start_monitoring'):
            self.plugin.start_monitoring()
            print("✅ Monitoring gestart")
            
            # Stop na 5 seconden
            QTimer.singleShot(5000, self.stop_monitoring)
        else:
            print("❌ start_monitoring methode niet gevonden")
    
    def stop_monitoring(self):
        """Stop monitoring"""
        if hasattr(self.plugin, 'stop_monitoring'):
            self.plugin.stop_monitoring()
            print("⏹️ Monitoring gestopt")
        else:
            print("❌ stop_monitoring methode niet gevonden")

def main():
    app = QApplication(sys.argv)
    
    # Test window
    window = TestWindow()
    window.show()
    
    print("🔌 System Monitor Plugin Test")
    print("📊 Plugin widget geladen")
    print("⏱️ Monitoring test start over 2 seconden")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 