#!/usr/bin/env python3
"""
Eenvoudige test voor grafieken zichtbaarheid
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import QTimer
import random

def main():
    app = QApplication(sys.argv)
    
    # Maak hoofdvenster
    window = QMainWindow()
    window.setWindowTitle("Grafieken Test")
    window.setGeometry(100, 100, 1000, 800)
    
    central_widget = QWidget()
    layout = QVBoxLayout(central_widget)
    
    try:
        from magic_time_studio.ui_pyqt6.components.charts_panel import ChartsPanel
        charts_panel = ChartsPanel()
        layout.addWidget(charts_panel)
        
        # Voeg test knop toe
        test_button = QPushButton("Test Data Toevoegen")
        layout.addWidget(test_button)
        
        def add_test_data():
            """Voeg test data toe aan grafieken"""
            print("Test data toevoegen...")
            
            # Voeg data toe aan system monitor
            if hasattr(charts_panel, 'system_monitor'):
                # Simuleer CPU data
                cpu_value = random.uniform(10, 90)
                charts_panel.system_monitor.cpu_chart.add_data_point(cpu_value)
                print(f"CPU data toegevoegd: {cpu_value}")
                
                # Simuleer RAM data
                ram_value = random.uniform(20, 80)
                charts_panel.system_monitor.memory_chart.add_data_point(ram_value)
                print(f"RAM data toegevoegd: {ram_value}")
                
                # Simuleer GPU data
                gpu_value = random.uniform(5, 50)
                charts_panel.system_monitor.gpu_chart.add_data_point(gpu_value)
                print(f"GPU data toegevoegd: {gpu_value}")
        
        test_button.clicked.connect(add_test_data)
        
        # Start timer voor automatische updates
        timer = QTimer()
        timer.timeout.connect(add_test_data)
        timer.start(2000)  # Elke 2 seconden
        
        window.setCentralWidget(central_widget)
        window.show()
        
        print("✅ Test venster geopend")
        print("Klik op 'Test Data Toevoegen' of wacht op automatische updates")
        
        app.exec()
        
    except Exception as e:
        print(f"❌ Fout: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 