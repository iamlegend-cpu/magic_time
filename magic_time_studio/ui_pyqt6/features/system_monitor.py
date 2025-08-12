"""
Systeem monitoring widget voor Magic Time Studio
Toon CPU, geheugen, GPU en temperatuur informatie
"""

import os
import psutil
import time
from typing import Optional, Tuple
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QGroupBox, QProgressBar
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from .real_time_chart import RealTimeChart

class SystemMonitorWidget(QWidget):
    """Widget voor real-time systeem monitoring"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_timer()
        
        # Cache voor GPU informatie om onnodige herhaalde checks te voorkomen
        self.gpu_cache = {}
        self.gpu_cache_timeout = 2  # Cache voor 2 seconden voor real-time monitoring
        self.last_gpu_check = 0
    
    def setup_ui(self):
        """Setup de UI componenten"""
        layout = QVBoxLayout()
        
        # Titel
        title = QLabel("📊 Systeem Monitoring")
        title.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff;")
        layout.addWidget(title)
        
        # Charts container - verticale layout met horizontale grafieken
        charts_layout = QVBoxLayout()
        charts_layout.setSpacing(10)  # Spacing tussen grafieken
        
        # CPU Chart
        cpu_group = QGroupBox("🖥️ CPU")
        cpu_layout = QVBoxLayout(cpu_group)
        cpu_layout.setContentsMargins(10, 10, 10, 10)  # Normale margins
        self.cpu_chart = RealTimeChart("CPU Gebruik", max_points=50)
        self.cpu_chart.setMinimumHeight(120)  # Grotere hoogte voor betere zichtbaarheid
        self.cpu_chart.setMinimumWidth(300)   # Minimum breedte
        self.cpu_chart.setVisible(True)  # Expliciet zichtbaar maken
        cpu_layout.addWidget(self.cpu_chart)
        
        # CPU Progress Bar
        self.cpu_progress = QProgressBar()
        self.cpu_progress.setRange(0, 100)
        self.cpu_progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #444;
                border-radius: 5px;
                text-align: center;
                background-color: #2a2a2a;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 3px;
            }
        """)
        cpu_layout.addWidget(self.cpu_progress)
        
        charts_layout.addWidget(cpu_group)
        
        # RAM Chart
        ram_group = QGroupBox("💾 RAM")
        ram_layout = QVBoxLayout(ram_group)
        ram_layout.setContentsMargins(10, 10, 10, 10)
        self.ram_chart = RealTimeChart("RAM Gebruik", max_points=50)
        self.ram_chart.setMinimumHeight(120)
        self.ram_chart.setMinimumWidth(300)
        self.ram_chart.setVisible(True)
        ram_layout.addWidget(self.ram_chart)
        
        # RAM Progress Bar
        self.ram_progress = QProgressBar()
        self.ram_progress.setRange(0, 100)
        self.ram_progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #444;
                border-radius: 5px;
                text-align: center;
                background-color: #2a2a2a;
            }
            QProgressBar::chunk {
                background-color: #2196F3;
                border-radius: 3px;
            }
        """)
        ram_layout.addWidget(self.ram_progress)
        
        charts_layout.addWidget(ram_group)
        
        # GPU Chart
        gpu_group = QGroupBox("🎮 GPU")
        gpu_layout = QVBoxLayout(gpu_group)
        gpu_layout.setContentsMargins(10, 10, 10, 10)
        self.gpu_chart = RealTimeChart("GPU Gebruik", max_points=50)
        self.gpu_chart.setMinimumHeight(120)
        self.gpu_chart.setMinimumWidth(300)
        self.gpu_chart.setVisible(True)
        gpu_layout.addWidget(self.gpu_chart)
        
        # GPU Progress Bar
        self.gpu_progress = QProgressBar()
        self.gpu_progress.setRange(0, 100)
        self.gpu_progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #444;
                border-radius: 5px;
                text-align: center;
                background-color: #2a2a2a;
            }
            QProgressBar::chunk {
                background-color: #FF9800;
                border-radius: 3px;
            }
        """)
        gpu_layout.addWidget(self.gpu_progress)
        
        charts_layout.addWidget(gpu_group)
        
        layout.addLayout(charts_layout)
        self.setLayout(layout)
    
    def setup_timer(self):
        """Setup timer voor real-time updates"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_monitoring)
        self.timer.start(1000)  # Update elke seconde voor real-time GPU monitoring
    
    def update_monitoring(self):
        """Update alle monitoring data"""
        try:
            # Update CPU
            cpu_percent = psutil.cpu_percent(interval=0.1)
            if hasattr(self, 'cpu_chart') and self.cpu_chart and hasattr(self.cpu_chart, 'add_data_point'):
                self.cpu_chart.add_data_point(cpu_percent)
            self.cpu_progress.setValue(int(cpu_percent))
            
            # Update RAM
            memory = psutil.virtual_memory()
            ram_percent = memory.percent
            if hasattr(self, 'ram_chart') and self.ram_chart and hasattr(self.ram_chart, 'add_data_point'):
                self.ram_chart.add_data_point(ram_percent)
            self.ram_progress.setValue(int(ram_percent))
            
            # Update GPU - probeer altijd GPU status op te halen
            gpu_info = self.get_gpu_info()
            if gpu_info and gpu_info.get('name'):
                gpu_percent = gpu_info.get('utilization', 0)
                if hasattr(self, 'gpu_chart') and self.gpu_chart and hasattr(self.gpu_chart, 'add_data_point'):
                    self.gpu_chart.add_data_point(gpu_percent)
                self.gpu_progress.setValue(int(gpu_percent))
                
                # Debug info (alleen bij eerste keer)
                if not hasattr(self, '_gpu_debug_printed'):
                    print(f"🎯 GPU Monitoring actief: {gpu_info.get('name')} - Utilization: {gpu_percent}%")
                    self._gpu_debug_printed = True
            else:
                # GPU niet beschikbaar - toon 0 maar blijf monitoring aan
                if hasattr(self, 'gpu_chart') and self.gpu_chart and hasattr(self.gpu_chart, 'add_data_point'):
                    self.gpu_chart.add_data_point(0)
                self.gpu_progress.setValue(0)
                
                # Debug info (alleen bij eerste keer)
                if not hasattr(self, '_gpu_not_found_printed'):
                    print("⚠️ GPU Monitoring: Geen GPU informatie gevonden")
                    self._gpu_not_found_printed = True
            
        except Exception as e:
            print(f"⚠️ Fout bij monitoring update: {e}")
    
    def get_gpu_info(self):
        """Krijg GPU informatie - NVIDIA GPU's + Fast Whisper GPU's (met caching)"""
        import time
        current_time = time.time()
        
        # Controleer cache - maar probeer altijd Fast Whisper GPU info op te halen
        if (current_time - self.last_gpu_check) < self.gpu_cache_timeout and self.gpu_cache:
            # Probeer nog steeds Fast Whisper GPU info op te halen voor real-time monitoring
            fast_whisper_gpu = self.get_fast_whisper_gpu_info()
            if fast_whisper_gpu:
                self.gpu_cache = fast_whisper_gpu
                self.last_gpu_check = current_time
                return fast_whisper_gpu
            # Als er geen Fast Whisper GPU info is, probeer PyTorch CUDA
            try:
                import torch
                if torch.cuda.is_available():
                    memory_allocated = torch.cuda.memory_allocated(0)
                    memory_reserved = torch.cuda.memory_reserved(0)
                    memory_total = torch.cuda.get_device_properties(0).total_memory
                    
                    if memory_allocated > 0 or memory_reserved > 0:
                        gpu_info = {
                            'utilization': 0,
                            'memory_used': memory_allocated / (1024**3),
                            'memory_total': memory_total / (1024**3),
                            'name': f"CUDA GPU ({torch.cuda.get_device_name(0)})",
                            'temperature': 0
                        }
                        self.gpu_cache = gpu_info
                        self.last_gpu_check = current_time
                        return gpu_info
            except:
                pass
            return self.gpu_cache
        
        # Probeer altijd GPU info op te halen
        try:
            # Probeer eerst echte GPU utilization via pynvml (zoals Taakbeheer)
            try:
                import pynvml
                pynvml.nvmlInit()
                device_count = pynvml.nvmlDeviceGetCount()
                if device_count > 0:
                    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                    utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
                    memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                    name = pynvml.nvmlDeviceGetName(handle)
                    if isinstance(name, bytes):
                        name = name.decode('utf-8')
                    
                    # Gebruik echte GPU utilization (zoals Taakbeheer)
                    real_utilization = utilization.gpu
                    
                    gpu_info = {
                        'utilization': real_utilization,  # Echte GPU utilization
                        'memory_used': memory_info.used / (1024**3),
                        'memory_total': memory_info.total / (1024**3),
                        'name': f"GPU ({name})",
                        'temperature': 0
                    }
                    self.gpu_cache = gpu_info
                    self.last_gpu_check = current_time
                    return gpu_info
            except:
                pass
            
            # Probeer Fast Whisper GPU status als fallback
            fast_whisper_gpu = self.get_fast_whisper_gpu_info()
            if fast_whisper_gpu:
                self.gpu_cache = fast_whisper_gpu
                self.last_gpu_check = current_time
                return fast_whisper_gpu
            
            # Als laatste fallback, probeer direct PyTorch CUDA
            try:
                import torch
                if torch.cuda.is_available():
                    memory_allocated = torch.cuda.memory_allocated(0)
                    memory_total = torch.cuda.get_device_properties(0).total_memory
                    
                    # Toon altijd GPU info, ook als memory 0 is
                    gpu_info = {
                        'utilization': 0,  # Standaard 0% als geen actieve verwerking
                        'memory_used': memory_allocated / (1024**3),
                        'memory_total': memory_total / (1024**3),
                        'name': f"CUDA GPU ({torch.cuda.get_device_name(0)})",
                        'temperature': 0
                    }
                    self.gpu_cache = gpu_info
                    self.last_gpu_check = current_time
                    return gpu_info
            except:
                pass
            
            # Geen GPU gevonden
            self.gpu_cache = None
            self.last_gpu_check = current_time
            return None
                
        except Exception as e:
            # Alleen printen als dit de eerste keer is
            if not hasattr(self, '_gpu_info_error_printed'):
                # print(f"⚠️ Fout bij GPU info ophalen: {e}")  # Uitgeschakeld
                self._gpu_info_error_printed = True
            self.gpu_cache = None
            self.last_gpu_check = current_time
            return None
    
    def get_fast_whisper_gpu_info(self):
        """Krijg Fast Whisper GPU informatie"""
        try:
            # Probeer eerst echte GPU utilization via pynvml (zoals Taakbeheer)
            try:
                import pynvml
                pynvml.nvmlInit()
                device_count = pynvml.nvmlDeviceGetCount()
                if device_count > 0:
                    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                    utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
                    memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                    name = pynvml.nvmlDeviceGetName(handle)
                    if isinstance(name, bytes):
                        name = name.decode('utf-8')
                    
                    # Gebruik echte GPU utilization (zoals Taakbeheer)
                    real_utilization = utilization.gpu
                    
                    return {
                        'utilization': real_utilization,  # Echte GPU utilization
                        'memory_used': memory_info.used / (1024**3),
                        'memory_total': memory_info.total / (1024**3),
                        'name': f"GPU ({name})",
                        'temperature': 0
                    }
            except:
                pass
            
            # Fallback naar PyTorch CUDA als pynvml niet werkt
            import torch
            if torch.cuda.is_available():
                memory_allocated = torch.cuda.memory_allocated(0)
                memory_reserved = torch.cuda.memory_reserved(0)
                memory_total = torch.cuda.get_device_properties(0).total_memory
                
                # Bereken utilization op basis van memory gebruik
                utilization = 0
                if memory_total > 0:
                    # Gebruik memory_allocated voor real-time utilization
                    utilization = min(100, int((memory_allocated / memory_total) * 100))
                
                # Toon altijd GPU info, ook als memory 0 is (voor monitoring)
                return {
                    'utilization': utilization,
                    'memory_used': memory_allocated / (1024**3),
                    'memory_total': memory_total / (1024**3),
                    'name': f"CUDA GPU ({torch.cuda.get_device_name(0)})",
                    'temperature': 0
                }
        except ImportError:
            pass
        except Exception as e:
            # Alleen printen als dit de eerste keer is
            if not hasattr(self, '_pytorch_error_printed'):
                print(f"⚠️ Fout bij PyTorch CUDA check: {e}")
                self._pytorch_error_printed = True
        
        # Fallback naar Fast Whisper GPU status
        try:
            from app_core.fast_whisper import FastWhisper
            fast_whisper = FastWhisper()
            gpu_status = fast_whisper.get_gpu_status()
            
            if gpu_status and gpu_status.get('available'):
                # Bereken utilization op basis van memory gebruik
                memory_used = gpu_status.get('memory_used', 0)
                memory_total = gpu_status.get('memory_total', 0)
                utilization = 0
                
                if memory_total > 0:
                    utilization = min(100, int((memory_used / memory_total) * 100))
                
                return {
                    'utilization': utilization,
                    'memory_used': memory_used,
                    'memory_total': memory_total,
                    'name': gpu_status.get('name', 'Fast Whisper GPU'),
                    'temperature': 0
                }
        except ImportError:
            pass
        except Exception as e:
            # Alleen printen als dit de eerste keer is
            if not hasattr(self, '_fast_whisper_error_printed'):
                # print(f"⚠️ Fout bij Fast Whisper GPU check: {e}")  # Uitgeschakeld
                self._fast_whisper_error_printed = True
        
        return None
    
    def get_gpu_name(self):
        """Krijg dynamische GPU naam - NVIDIA GPU's + Fast Whisper GPU's (met caching)"""
        # Gebruik gecachte GPU info als beschikbaar
        if self.gpu_cache and self.gpu_cache.get('name'):
            gpu_name = self.gpu_cache.get('name', 'N/A')
            # Kort de naam in voor betere weergave
            if len(gpu_name) > 20:
                gpu_name = gpu_name[:17] + "..."
            return gpu_name
        
        # Probeer eerst Fast Whisper GPU naam
        try:
            from app_core.fast_whisper import FastWhisper
            fast_whisper = FastWhisper()
            gpu_status = fast_whisper.get_gpu_status()
            
            if gpu_status and gpu_status.get('available'):
                gpu_name = gpu_status.get('name', 'Fast Whisper GPU')
                # Kort de naam in voor betere weergave
                if len(gpu_name) > 20:
                    gpu_name = gpu_name[:17] + "..."
                return gpu_name
        except:
            pass
        
        # Probeer NVIDIA GPU via pynvml
        try:
            import pynvml
            pynvml.nvmlInit()
            device_count = pynvml.nvmlDeviceGetCount()
            # Alleen eerste GPU (dedicated) gebruiken
            if device_count > 0:
                handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                name = pynvml.nvmlDeviceGetName(handle)
                if isinstance(name, bytes):
                    name = name.decode('utf-8')
                # Alleen NVIDIA GPU's ondersteunen
                if 'NVIDIA' in name:
                    # Kort de naam in voor betere weergave
                    if len(name) > 20:
                        # Verwijder "NVIDIA " prefix en kort in
                        if name.startswith("NVIDIA "):
                            name = name[7:]  # Verwijder "NVIDIA "
                        # Kort in tot 20 karakters
                        if len(name) > 20:
                            name = name[:17] + "..."
                    return name
        except:
            pass
        
        return None
    
    def start_processing_monitoring(self):
        """Start snelle monitoring tijdens verwerking"""
        try:
            # Verhoog update frequentie tijdens verwerking
            if hasattr(self, 'timer'):
                self.timer.stop()
                self.timer.start(1000)  # Elke seconde tijdens verwerking
            print("✅ Snelle monitoring gestart voor verwerking")
        except Exception as e:
            print(f"⚠️ Fout bij starten snelle monitoring: {e}")
    
    def stop_processing_monitoring(self):
        """Stop snelle monitoring na verwerking"""
        try:
            # Herstel normale update frequentie
            if hasattr(self, 'timer'):
                self.timer.stop()
                self.timer.start(5000)  # Terug naar elke 5 seconden
            print("✅ Normale monitoring hersteld na verwerking")
        except Exception as e:
            print(f"⚠️ Fout bij stoppen snelle monitoring: {e}") 