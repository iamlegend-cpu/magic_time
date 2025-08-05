"""
Performance monitoring chart voor Magic Time Studio
Toon I/O, netwerk en uptime informatie
"""

import psutil
from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QGroupBox
)
from PyQt6.QtCore import Qt, QTimer
from .real_time_chart import RealTimeChart


class PerformanceChart(QWidget):
    """Performance monitoring chart"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_timer()
    
    def setup_ui(self):
        """Setup de UI"""
        layout = QVBoxLayout(self)
        
        # Titel
        title = QLabel("⚡ Performance Metrics")
        title.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff;")
        layout.addWidget(title)
        
        # Charts container - verticale layout met horizontale grafieken
        charts_layout = QVBoxLayout()
        charts_layout.setSpacing(10)  # Spacing tussen grafieken
        
        # I/O Chart
        io_group = QGroupBox("💾 I/O Activiteit")
        io_layout = QVBoxLayout(io_group)
        io_layout.setContentsMargins(10, 10, 10, 10)  # Normale margins
        self.io_chart = RealTimeChart("I/O Activiteit", max_points=30)
        self.io_chart.setMinimumHeight(80)  # Kleinere hoogte voor horizontale layout
        io_layout.addWidget(self.io_chart)
        charts_layout.addWidget(io_group)
        
        # Network Chart
        network_group = QGroupBox("🌐 Netwerk")
        network_layout = QVBoxLayout(network_group)
        network_layout.setContentsMargins(10, 10, 10, 10)
        self.network_chart = RealTimeChart("Netwerk", max_points=30)
        self.network_chart.setMinimumHeight(80)
        network_layout.addWidget(self.network_chart)
        charts_layout.addWidget(network_group)
        
        layout.addLayout(charts_layout)
        
        # Performance info - horizontale layout
        info_layout = QHBoxLayout()
        info_layout.setSpacing(15)  # Normale spacing
        
        self.io_label = QLabel("I/O: 0 MB/s")
        self.io_label.setStyleSheet("color: #ff9800; font-weight: bold; padding: 5px;")
        info_layout.addWidget(self.io_label)
        
        self.network_label = QLabel("Netwerk: 0 MB/s")
        self.network_label.setStyleSheet("color: #2196f3; font-weight: bold; padding: 5px;")
        info_layout.addWidget(self.network_label)
        
        self.uptime_label = QLabel("Uptime: -")
        self.uptime_label.setStyleSheet("color: #4caf50; font-weight: bold; padding: 5px;")
        info_layout.addWidget(self.uptime_label)
        
        layout.addLayout(info_layout)
    
    def setup_timer(self):
        """Setup timer voor updates"""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_performance_stats)
        self.update_timer.start(2000)  # Elke 2 seconden
        
        # Initialiseer vorige waarden
        self.prev_io_read = 0
        self.prev_io_write = 0
        self.prev_network_sent = 0
        self.prev_network_recv = 0
    
    def update_performance_stats(self):
        """Update performance statistieken"""
        try:
            # I/O statistieken
            io_counters = psutil.disk_io_counters()
            if io_counters:
                io_read_mb = io_counters.read_bytes / (1024**2)
                io_write_mb = io_counters.write_bytes / (1024**2)
                
                # Bereken snelheid (verschil met vorige meting)
                if hasattr(self, 'prev_io_read'):
                    io_read_speed = (io_read_mb - self.prev_io_read) / 2  # MB/s
                    io_write_speed = (io_write_mb - self.prev_io_write) / 2  # MB/s
                    total_io_speed = io_read_speed + io_write_speed
                    
                    self.io_chart.add_data_point(total_io_speed)
                    self.io_label.setText(f"I/O: {total_io_speed:.1f} MB/s")
                
                self.prev_io_read = io_read_mb
                self.prev_io_write = io_write_mb
            
            # Netwerk statistieken
            network_counters = psutil.net_io_counters()
            if network_counters:
                network_sent_mb = network_counters.bytes_sent / (1024**2)
                network_recv_mb = network_counters.bytes_recv / (1024**2)
                
                # Bereken snelheid
                if hasattr(self, 'prev_network_sent'):
                    network_sent_speed = (network_sent_mb - self.prev_network_sent) / 2
                    network_recv_speed = (network_recv_mb - self.prev_network_recv) / 2
                    total_network_speed = network_sent_speed + network_recv_speed
                    
                    self.network_chart.add_data_point(total_network_speed)
                    self.network_label.setText(f"Netwerk: {total_network_speed:.1f} MB/s")
                
                self.prev_network_sent = network_sent_mb
                self.prev_network_recv = network_recv_mb
            
            # Uptime
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            uptime_str = str(uptime).split('.')[0]  # Verwijder microseconden
            self.uptime_label.setText(f"Uptime: {uptime_str}")
            
        except Exception as e:
            print(f"❌ Fout bij performance monitoring: {e}")
    
    def update_whisper_speed(self, speed: float):
        """Update Whisper snelheid (seconden per minuut audio)"""
        # Deze methode kan later worden uitgebreid
        pass
    
    def update_translation_speed(self, speed: float):
        """Update vertaling snelheid (woorden per seconde)"""
        # Deze methode kan later worden uitgebreid
        pass 