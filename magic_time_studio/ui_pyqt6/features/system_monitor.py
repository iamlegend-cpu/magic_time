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
                border: 2px solid #4caf50;
                border-radius: 5px;
                text-align: center;
                background-color: #2e2e2e;
            }
            QProgressBar::chunk {
                background-color: #4caf50;
                border-radius: 3px;
            }
        """)
        cpu_layout.addWidget(self.cpu_progress)
        charts_layout.addWidget(cpu_group)
        
        # Memory Chart
        memory_group = QGroupBox("💾 RAM")
        memory_layout = QVBoxLayout(memory_group)
        memory_layout.setContentsMargins(10, 10, 10, 10)
        self.memory_chart = RealTimeChart("Geheugen Gebruik", max_points=50)
        self.memory_chart.setMinimumHeight(120)  # Grotere hoogte
        self.memory_chart.setMinimumWidth(300)   # Minimum breedte
        self.memory_chart.setVisible(True)  # Expliciet zichtbaar maken
        memory_layout.addWidget(self.memory_chart)
        
        # Memory Progress Bar
        self.memory_progress = QProgressBar()
        self.memory_progress.setRange(0, 100)
        self.memory_progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #2196f3;
                border-radius: 5px;
                text-align: center;
                background-color: #2e2e2e;
            }
            QProgressBar::chunk {
                background-color: #2196f3;
                border-radius: 3px;
            }
        """)
        memory_layout.addWidget(self.memory_progress)
        charts_layout.addWidget(memory_group)
        
        # GPU Chart
        gpu_group = QGroupBox("🎮 GPU")
        gpu_layout = QVBoxLayout(gpu_group)
        gpu_layout.setContentsMargins(10, 10, 10, 10)
        self.gpu_chart = RealTimeChart("GPU Gebruik", max_points=50)
        self.gpu_chart.setMinimumHeight(120)  # Grotere hoogte
        self.gpu_chart.setMinimumWidth(300)   # Minimum breedte
        self.gpu_chart.setVisible(True)  # Expliciet zichtbaar maken
        gpu_layout.addWidget(self.gpu_chart)
        
        # GPU Progress Bar
        self.gpu_progress = QProgressBar()
        self.gpu_progress.setRange(0, 100)
        self.gpu_progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #9c27b0;
                border-radius: 5px;
                text-align: center;
                background-color: #2e2e2e;
            }
            QProgressBar::chunk {
                background-color: #9c27b0;
                border-radius: 3px;
            }
        """)
        gpu_layout.addWidget(self.gpu_progress)
        charts_layout.addWidget(gpu_group)
        
        layout.addLayout(charts_layout)
        
        # Status labels - horizontale layout
        status_layout = QHBoxLayout()
        status_layout.setSpacing(15)  # Normale spacing
        
        self.cpu_label = QLabel("CPU: 0%")
        self.cpu_label.setStyleSheet("color: #4caf50; font-weight: bold; padding: 5px;")
        status_layout.addWidget(self.cpu_label)
        
        self.memory_label = QLabel("RAM: 0%")
        self.memory_label.setStyleSheet("color: #2196f3; font-weight: bold; padding: 5px;")
        status_layout.addWidget(self.memory_label)
        
        self.gpu_label = QLabel("GPU: N/A")
        self.gpu_label.setStyleSheet("color: #9c27b0; font-weight: bold; padding: 5px;")
        status_layout.addWidget(self.gpu_label)
        
        layout.addLayout(status_layout)
        
        self.setLayout(layout) # Set the main layout for the widget
    
    def setup_timer(self):
        """Setup de update timer"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # Update elke seconde
    
    def get_gpu_info(self):
        """Krijg GPU informatie - alleen dedicated GPU"""
        # Probeer NVIDIA GPU via pynvml (betere utilization)
        try:
            import pynvml
            pynvml.nvmlInit()
            device_count = pynvml.nvmlDeviceGetCount()
            if device_count > 0:
                handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
                return utilization.gpu # Gebruik GPU utilization voor betere weergave
        except:
            pass
        
        # Probeer PyTorch CUDA als fallback (geeft memory percent)
        try:
            import torch
            if torch.cuda.is_available():
                gpu_count = torch.cuda.device_count()
                if gpu_count > 0:
                    memory_allocated = torch.cuda.memory_allocated(0)
                    memory_total = torch.cuda.get_device_properties(0).total_memory
                    memory_percent = (memory_allocated / memory_total) * 100
                    return memory_percent
        except:
            pass
        
        return None
    
    def get_gpu_name(self):
        """Krijg dynamische GPU naam - alleen dedicated GPU"""
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
        
        # Probeer PyTorch CUDA als fallback
        try:
            import torch
            if torch.cuda.is_available():
                gpu_count = torch.cuda.device_count()
                if gpu_count > 0:
                    return torch.cuda.get_device_name(0)
        except:
            pass
        
        return "Onbekende GPU"
    
    def get_temperature(self) -> Tuple[Optional[float], Optional[str]]:
        """Krijg temperatuur informatie (uitgeschakeld op Windows)"""
        # Temperatuur uitlezen is problematisch op Windows, dus uitgeschakeld
        return None, None
    
    def update_data(self):
        """Update alle monitoring data"""
        
        # CPU data
        cpu_percent = psutil.cpu_percent(interval=0.1)
        self.cpu_chart.add_data_point(cpu_percent)
        self.cpu_label.setText(f"CPU: {cpu_percent:.1f}%")
        self.cpu_progress.setValue(int(cpu_percent))
        
        # Memory data
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        self.memory_chart.add_data_point(memory_percent)
        self.memory_label.setText(f"RAM: {memory_percent:.1f}%")
        self.memory_progress.setValue(int(memory_percent))
        
        # GPU data
        gpu_utilization = self.get_gpu_info()
        if gpu_utilization is not None:
            self.gpu_chart.add_data_point(gpu_utilization)
            # Dynamische GPU naam detectie
            gpu_name = self.get_gpu_name()
            self.gpu_label.setText(f"{gpu_name}: {gpu_utilization:.1f}%")
            self.gpu_label.setStyleSheet("color: #9c27b0; font-weight: bold;")
            self.gpu_progress.setValue(int(gpu_utilization))
        else:
            self.gpu_label.setText("GPU: N/A")
            self.gpu_label.setStyleSheet("color: #888; font-weight: bold;")
            self.gpu_progress.setValue(0)
    
    def start_monitoring(self):
        """Start monitoring"""
        if not self.timer.isActive():
            self.timer.start(1000)
    
    def stop_monitoring(self):
        """Stop monitoring"""
        if self.timer.isActive():
            self.timer.stop() 