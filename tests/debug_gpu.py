#!/usr/bin/env python3
"""
Debug script voor GPU monitoring
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'magic_time_studio'))

def debug_gpu_monitoring():
    """Debug GPU monitoring"""
    print("🔍 Debug GPU Monitoring")
    print("=" * 50)
    
    # Test 1: Directe pynvml test
    print("\n📊 Test 1: Directe pynvml:")
    try:
        import pynvml
        pynvml.nvmlInit()
        device_count = pynvml.nvmlDeviceGetCount()
        print(f"   GPU count: {device_count}")
        
        total_utilization = 0
        for i in range(device_count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            name = pynvml.nvmlDeviceGetName(handle)
            if isinstance(name, bytes):
                name = name.decode('utf-8')
            utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
            memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            
            print(f"   GPU {i}: {name}")
            print(f"     GPU Utilization: {utilization.gpu}%")
            print(f"     Memory Utilization: {utilization.memory}%")
            print(f"     Memory Used: {memory_info.used / (1024**3):.1f} GB")
            print(f"     Memory Total: {memory_info.total / (1024**3):.1f} GB")
            
            total_utilization += utilization.gpu
        
        print(f"   Totaal GPU Utilization: {total_utilization}%")
        
    except Exception as e:
        print(f"   ❌ pynvml error: {e}")
    
    # Test 2: PyTorch CUDA test
    print("\n📊 Test 2: PyTorch CUDA:")
    try:
        import torch
        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            print(f"   GPU count: {gpu_count}")
            
            total_memory_percent = 0
            for i in range(gpu_count):
                memory_allocated = torch.cuda.memory_allocated(i)
                memory_total = torch.cuda.get_device_properties(i).total_memory
                memory_percent = (memory_allocated / memory_total) * 100
                name = torch.cuda.get_device_name(i)
                
                print(f"   GPU {i}: {name}")
                print(f"     Memory Percent: {memory_percent:.1f}%")
                
                total_memory_percent += memory_percent
            
            print(f"   Totaal Memory Percent: {total_memory_percent:.1f}%")
        else:
            print("   ❌ CUDA niet beschikbaar")
    except Exception as e:
        print(f"   ❌ PyTorch error: {e}")
    
    # Test 3: System Monitor test
    print("\n📊 Test 3: System Monitor:")
    try:
        from magic_time_studio.ui_pyqt6.features.system_monitor import SystemMonitorWidget
        
        monitor = SystemMonitorWidget()
        gpu_percent = monitor.get_gpu_info()
        gpu_name = monitor.get_gpu_name()
        
        print(f"   GPU Percent: {gpu_percent}")
        print(f"   GPU Name: {gpu_name}")
        
    except Exception as e:
        print(f"   ❌ System Monitor error: {e}")
    
    # Test 4: System Monitor Plugin test
    print("\n📊 Test 4: System Monitor Plugin:")
    try:
        from magic_time_studio.ui_pyqt6.features.plugins.system_monitor_plugin import EnhancedSystemMonitorThread
        
        monitor_thread = EnhancedSystemMonitorThread()
        gpu_info = monitor_thread.get_detailed_gpu_info()
        
        print(f"   GPU Info: {gpu_info}")
        
        # Bereken totaal
        total_gpu_utilization = 0
        for gpu_id, gpu_data in gpu_info.items():
            if 'gpu_utilization' in gpu_data:
                total_gpu_utilization += gpu_data['gpu_utilization']
            elif 'memory_percent' in gpu_data:
                total_gpu_utilization += gpu_data['memory_percent']
        
        print(f"   Totaal GPU Utilization: {total_gpu_utilization:.1f}%")
        
    except Exception as e:
        print(f"   ❌ System Monitor Plugin error: {e}")

if __name__ == "__main__":
    debug_gpu_monitoring() 