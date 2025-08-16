"""
Systeem monitoring widget voor Magic Time Studio
Alleen WhisperX wordt ondersteund
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QGroupBox, QProgressBar
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from .gpu_monitor import GPUMonitor
from .cpu_ram_monitor import CPURAMMonitor

class SystemMonitorWidget(QWidget):
    """Widget voor real-time systeem monitoring - alleen WhisperX"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_timer()
        
        # WhisperX status
        self.whisperx_available = False
        self.whisperx_device = None
    
    def setup_ui(self):
        """Setup de UI componenten"""
        layout = QVBoxLayout()
        
        # Charts container
        charts_layout = QVBoxLayout()
        charts_layout.setSpacing(15)  # Meer ruimte tussen charts
        
        # CPU en RAM monitoring
        self.cpu_ram_monitor = CPURAMMonitor(self)
        self.cpu_ram_monitor.setup_ui(charts_layout)
        
        # GPU monitoring (WhisperX)
        gpu_group = QGroupBox("🎮 GPU (WhisperX)")
        gpu_layout = QVBoxLayout(gpu_group)
        gpu_layout.setContentsMargins(10, 15, 10, 15)  # Meer ruimte boven/onder
        gpu_layout.setSpacing(8)  # Meer ruimte tussen elementen
        
        # GPU Chart
        from .real_time_chart import RealTimeChart
        self.gpu_chart = RealTimeChart("GPU Gebruik", max_points=50)
        gpu_layout.addWidget(self.gpu_chart)
        
        # Voeg GPU groep toe aan charts layout
        charts_layout.addWidget(gpu_group)
        
        layout.addLayout(charts_layout)
        self.setLayout(layout)
    
    def setup_timer(self):
        """Setup timer voor real-time updates"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_monitoring)
        self.timer.start(1000)  # Update elke seconde
    
    def update_monitoring(self):
        """Update alle monitoring data"""
        try:
            # Update CPU en RAM
            self.cpu_ram_monitor.update_monitoring()
            
            # GPU wordt automatisch bijgewerkt door de GPU monitor timer
            
        except Exception as e:
            print(f"⚠️ Fout bij monitoring update: {e}")
    
    def start_processing_monitoring(self):
        """Start snellere monitoring tijdens verwerking"""
        # The GPU monitor is now managed by the charts panel, so no direct call here.
        pass
    
    def stop_processing_monitoring(self):
        """Stop snellere monitoring na verwerking"""
        # The GPU monitor is now managed by the charts panel, so no direct call here.
        pass 

    def _find_main_window(self):
        """Zoek naar het hoofdvenster om statusbalk labels bij te werken"""
        parent = self.parent()
        while parent:
            if hasattr(parent, 'gpu_status_label') and hasattr(parent, 'gpu_memory_label'):
                return parent
            parent = parent.parent()
        return None 