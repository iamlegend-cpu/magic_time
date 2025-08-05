#!/usr/bin/env python3
"""
Test script voor GUI GPU monitoring
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'magic_time_studio'))

from PyQt6.QtWidgets import QApplication
from magic_time_studio.ui_pyqt6.features.system_monitor import SystemMonitorWidget

def test_gui_gpu():
    """Test GUI GPU monitoring"""
    print("🔍 Test GUI GPU Monitoring")
    print("=" * 50)
    
    # Maak QApplication
    app = QApplication(sys.argv)
    
    # Test SystemMonitorWidget
    print("\n📊 Test SystemMonitorWidget:")
    try:
        monitor = SystemMonitorWidget()
        gpu_percent = monitor.get_gpu_info()
        gpu_name = monitor.get_gpu_name()
        
        print(f"   GPU Percent: {gpu_percent}")
        print(f"   GPU Name: {gpu_name}")
        
        # Test update
        monitor.update_data()
        print(f"   Na update - GPU Percent: {monitor.get_gpu_info()}")
        
    except Exception as e:
        print(f"   ❌ SystemMonitorWidget error: {e}")
    
    # Test directe GPU monitoring
    print("\n📊 Test Directe GPU Monitoring:")
    try:
        import pynvml
        pynvml.nvmlInit()
        device_count = pynvml.nvmlDeviceGetCount()
        print(f"   GPU count: {device_count}")
        
        for i in range(device_count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            name = pynvml.nvmlDeviceGetName(handle)
            if isinstance(name, bytes):
                name = name.decode('utf-8')
            utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
            
            print(f"   GPU {i}: {name}")
            print(f"     GPU Utilization: {utilization.gpu}%")
        
    except Exception as e:
        print(f"   ❌ Directe GPU monitoring error: {e}")

if __name__ == "__main__":
    test_gui_gpu() 