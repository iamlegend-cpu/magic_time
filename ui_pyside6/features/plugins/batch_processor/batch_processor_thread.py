"""
Smart Batch Processor Thread
Intelligente batch processor met parallel processing
"""

import os
import psutil
import threading
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from PySide6.QtCore import QThread, Signal

from .system_monitor import SystemMonitor

class SmartBatchProcessorThread(QThread):
    """Intelligente batch processor met systeem monitoring"""
    progress_updated = Signal(int, str)
    file_processed = Signal(str, str)  # filename, status
    batch_finished = Signal()
    error_occurred = Signal(str)
    system_status = Signal(dict)  # CPU, RAM, VRAM info
    
    def __init__(self, files: List[str], settings: Dict[str, Any]):
        super().__init__()
        self.files = files
        self.settings = settings
        self.is_running = True
        self.max_workers = self.calculate_optimal_workers()
        self.system_monitor = SystemMonitor()
        
    def calculate_optimal_workers(self) -> int:
        """Bereken optimaal aantal workers op basis van systeem"""
        try:
            # Systeem info
            cpu_count = psutil.cpu_count()
            memory_gb = psutil.virtual_memory().total / (1024**3)
            
            # Whisper model grootte (Large = ~3GB)
            whisper_memory_gb = 3.0
            
            # Bereken veilige worker count
            max_by_cpu = min(cpu_count, 4)  # Max 4 CPU cores
            max_by_memory = int(memory_gb / (whisper_memory_gb + 1))  # +1GB buffer
            
            optimal_workers = min(max_by_cpu, max_by_memory, 2)  # Veilig maximum
            
            print(f"🔧 Optimal workers: CPU={max_by_cpu}, RAM={max_by_memory}, Final={optimal_workers}")
            return optimal_workers
            
        except Exception as e:
            print(f"⚠️ Kon optimale workers niet berekenen: {e}")
            return 1  # Fallback naar sequential
    
    def run(self):
        """Voer intelligente batch verwerking uit"""
        try:
            total_files = len(self.files)
            completed_files = 0
            
            # Start systeem monitoring
            self.system_monitor.start()
            
            # Gebruik ThreadPoolExecutor voor parallel processing
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Submit alle taken
                future_to_file = {
                    executor.submit(self.process_single_file, file_path): file_path 
                    for file_path in self.files
                }
                
                # Verwerk resultaten als ze klaar zijn
                for future in as_completed(future_to_file):
                    if not self.is_running:
                        break
                    
                    file_path = future_to_file[future]
                    filename = os.path.basename(file_path)
                    
                    try:
                        result = future.result()
                        status = "✅ Voltooid"
                        completed_files += 1
                        
                    except Exception as e:
                        result = f"❌ Fout: {e}"
                        status = "❌ Gefaald"
                    
                    # Update progress
                    progress = int((completed_files / total_files) * 100)
                    self.progress_updated.emit(progress, f"Verwerkt: {filename}")
                    self.file_processed.emit(filename, status)
                    
                    # Wacht tot systeem veilig is voor volgende verwerking
                    while not self.system_monitor.is_safe_to_process() and self.is_running:
                        self.msleep(1000)  # Wacht 1 seconde
                    
                    if not self.is_running:
                        break
            
            # Stop monitoring
            self.system_monitor.stop()
            
            # Emit finished signal
            if self.is_running:
                self.batch_finished.emit()
            else:
                self.error_occurred.emit("Batch verwerking gestopt door gebruiker")
                
        except Exception as e:
            self.error_occurred.emit(f"Batch verwerking fout: {e}")
            self.system_monitor.stop()
    
    def process_single_file(self, file_path: str) -> str:
        """Verwerk een enkel bestand"""
        try:
            # Hier zou de daadwerkelijke verwerking plaatsvinden
            # Voor nu simuleren we alleen verwerking
            import time
            time.sleep(2)  # Simuleer verwerking tijd
            
            return f"Verwerkt: {os.path.basename(file_path)}"
            
        except Exception as e:
            raise Exception(f"Fout bij verwerken {file_path}: {e}")
    
    def stop(self):
        """Stop de batch verwerking"""
        self.is_running = False
        self.system_monitor.stop() 