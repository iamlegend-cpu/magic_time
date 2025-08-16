"""
System Monitor voor Batch Processor
Bewaakt systeem resources tijdens batch verwerking
"""

import psutil
import time
import threading
from typing import Dict, Any

class SystemMonitor:
    """Systeem resource monitor voor batch processing"""
    
    def __init__(self):
        self.is_monitoring = False
        self.monitor_thread = None
        self.status_callback = None
        
    def start(self):
        """Start systeem monitoring"""
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
    def stop(self):
        """Stop systeem monitoring"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1.0)
    
    def get_status(self) -> Dict[str, Any]:
        """Haal huidige systeem status op"""
        try:
            # CPU gebruik
            cpu_percent = psutil.cpu_percent(interval=0.1)
            
            # RAM gebruik
            memory = psutil.virtual_memory()
            ram_percent = memory.percent
            ram_used_gb = memory.used / (1024**3)
            ram_total_gb = memory.total / (1024**3)
            
            # GPU/VRAM (als beschikbaar)
            vram_info = self._get_vram_info()
            
            return {
                'cpu_percent': cpu_percent,
                'ram_percent': ram_percent,
                'ram_used_gb': round(ram_used_gb, 1),
                'ram_total_gb': round(ram_total_gb, 1),
                'vram_used_gb': vram_info.get('used_gb', 0),
                'vram_total_gb': vram_info.get('total_gb', 0),
                'timestamp': time.time()
            }
            
        except Exception as e:
            print(f"⚠️ Fout bij ophalen systeem status: {e}")
            return {
                'cpu_percent': 0,
                'ram_percent': 0,
                'ram_used_gb': 0,
                'ram_total_gb': 0,
                'vram_used_gb': 0,
                'vram_total_gb': 0,
                'timestamp': time.time()
            }
    
    def _get_vram_info(self) -> Dict[str, float]:
        """Haal VRAM informatie op (als beschikbaar)"""
        try:
            # Probeer GPU info op te halen via verschillende methoden
            import GPUtil
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = gpus[0]  # Gebruik eerste GPU
                return {
                    'used_gb': gpu.memoryUsed / 1024,
                    'total_gb': gpu.memoryTotal / 1024
                }
        except ImportError:
            pass
        except Exception as e:
            print(f"⚠️ Kon GPU info niet ophalen: {e}")
        
        return {'used_gb': 0, 'total_gb': 0}
    
    def is_safe_to_process(self) -> bool:
        """Controleer of het veilig is om te verwerken"""
        try:
            status = self.get_status()
            
            # Veilige limieten
            max_cpu = 90  # Max 90% CPU
            max_ram = 85  # Max 85% RAM
            max_vram = 90  # Max 90% VRAM
            
            # Controleer limieten
            if status['cpu_percent'] > max_cpu:
                print(f"⚠️ CPU gebruik te hoog: {status['cpu_percent']}%")
                return False
                
            if status['ram_percent'] > max_ram:
                print(f"⚠️ RAM gebruik te hoog: {status['ram_percent']}%")
                return False
                
            if status['vram_used_gb'] > 0 and status['vram_total_gb'] > 0:
                vram_percent = (status['vram_used_gb'] / status['vram_total_gb']) * 100
                if vram_percent > max_vram:
                    print(f"⚠️ VRAM gebruik te hoog: {vram_percent:.1f}%")
                    return False
            
            return True
            
        except Exception as e:
            print(f"⚠️ Fout bij veiligheidscontrole: {e}")
            return True  # Fallback naar veilig
    
    def _monitor_loop(self):
        """Monitoring loop thread"""
        while self.is_monitoring:
            try:
                status = self.get_status()
                if self.status_callback:
                    self.status_callback(status)
                time.sleep(2)  # Update elke 2 seconden
            except Exception as e:
                print(f"⚠️ Fout in monitoring loop: {e}")
                time.sleep(5)  # Langere pauze bij fout 