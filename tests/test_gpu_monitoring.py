#!/usr/bin/env python3
"""
Test script voor GPU monitoring
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'magic_time_studio'))

def test_gpu_monitoring():
    """Test GPU monitoring"""
    print("🔍 Test GPU Monitoring")
    print("=" * 50)
    
    # Test pynvml
    print("\n📊 Test pynvml:")
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
            memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
            temperature = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
            
            print(f"   GPU {i}: {name}")
            print(f"     Memory: {memory_info.used / (1024**3):.1f} GB / {memory_info.total / (1024**3):.1f} GB ({memory_info.used / memory_info.total * 100:.1f}%)")
            print(f"     GPU Utilization: {utilization.gpu}%")
            print(f"     Memory Utilization: {utilization.memory}%")
            print(f"     Temperature: {temperature}°C")
            
    except Exception as e:
        print(f"   ❌ pynvml error: {e}")
    
    # Test PyTorch CUDA
    print("\n📊 Test PyTorch CUDA:")
    try:
        import torch
        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            print(f"   CUDA GPU count: {gpu_count}")
            
            for i in range(gpu_count):
                name = torch.cuda.get_device_name(i)
                memory_allocated = torch.cuda.memory_allocated(i)
                memory_total = torch.cuda.get_device_properties(i).total_memory
                memory_percent = (memory_allocated / memory_total) * 100
                
                print(f"   GPU {i}: {name}")
                print(f"     Memory: {memory_allocated / (1024**3):.1f} GB / {memory_total / (1024**3):.1f} GB ({memory_percent:.1f}%)")
        else:
            print("   ❌ CUDA niet beschikbaar")
    except Exception as e:
        print(f"   ❌ PyTorch error: {e}")
    
    # Test system monitor
    print("\n📊 Test System Monitor:")
    try:
        from magic_time_studio.ui_pyqt6.features.system_monitor import SystemMonitorWidget
        
        # Maak een dummy widget
        import PyQt6.QtWidgets
        app = PyQt6.QtWidgets.QApplication([])
        
        monitor = SystemMonitorWidget()
        
        # Test GPU info
        gpu_percent = monitor.get_gpu_info()
        gpu_name = monitor.get_gpu_name()
        
        print(f"   GPU Percent: {gpu_percent}")
        print(f"   GPU Name: {gpu_name}")
        
    except Exception as e:
        print(f"   ❌ System Monitor error: {e}")

if __name__ == "__main__":
    test_gpu_monitoring() 