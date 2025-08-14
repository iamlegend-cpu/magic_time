"""
CPU en RAM Monitoring module voor Magic Time Studio
"""

import psutil
from PyQt6.QtWidgets import QLabel, QSpacerItem, QSizePolicy, QGroupBox, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer
from .real_time_chart import RealTimeChart

class CPURAMMonitor:
    """CPU en RAM Monitoring klasse"""
    
    def __init__(self, parent_widget):
        self.parent = parent_widget
        
        # UI componenten
        self.cpu_chart = None
        self.cpu_progress = None
        self.ram_chart = None
        self.ram_progress = None
    
    def setup_ui(self, parent_layout):
        """Setup de CPU en RAM monitoring UI"""
        # CPU monitoring groep
        cpu_group = QGroupBox("🖥️ CPU")
        cpu_layout = QVBoxLayout(cpu_group)
        cpu_layout.setContentsMargins(10, 15, 10, 15)  # Meer ruimte boven/onder
        cpu_layout.setSpacing(8)  # Meer ruimte tussen elementen
        
        # CPU Chart
        self.cpu_chart = RealTimeChart("CPU Gebruik", max_points=50)
        cpu_layout.addWidget(self.cpu_chart)
        
        # Voeg CPU groep toe aan parent layout
        parent_layout.addWidget(cpu_group)
        
        # Spacer tussen CPU en RAM
        spacer_cpu_ram = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        parent_layout.addItem(spacer_cpu_ram)
        
        # RAM monitoring groep
        ram_group = QGroupBox("💾 RAM")
        ram_layout = QVBoxLayout(ram_group)
        ram_layout.setContentsMargins(10, 15, 10, 15)  # Meer ruimte boven/onder
        ram_layout.setSpacing(8)  # Meer ruimte tussen elementen
        
        # RAM Chart
        self.ram_chart = RealTimeChart("RAM Gebruik", max_points=50)
        ram_layout.addWidget(self.ram_chart)
        
        # Voeg RAM groep toe aan parent layout
        parent_layout.addWidget(ram_group)
        
        # Zoek naar hoofdvenster voor statusbalk updates
        self.main_window = self._find_main_window()
    
    def _find_main_window(self):
        """Zoek naar het hoofdvenster om statusbalk labels bij te werken"""
        current = self.parent
        while current:
            if hasattr(current, 'gpu_status_label') and hasattr(current, 'gpu_memory_label'):
                return current
            current = current.parent()
        return None

    def update_monitoring(self):
        """Update CPU en RAM monitoring data"""
        try:
            # Update CPU
            cpu_percent = psutil.cpu_percent(interval=0.1)
            if self.cpu_chart and hasattr(self.cpu_chart, 'add_data_point'):
                self.cpu_chart.add_data_point(cpu_percent)
            
            # Update RAM
            memory = psutil.virtual_memory()
            ram_percent = memory.percent
            if self.ram_chart and hasattr(self.ram_chart, 'add_data_point'):
                self.ram_chart.add_data_point(ram_percent)
            
        except Exception as e:
            print(f"⚠️ Fout bij CPU/RAM monitoring update: {e}")
