"""
Charts Panel component voor Magic Time Studio
Handelt grafieken en monitoring af
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QTabWidget, QLabel
)
from PySide6.QtCore import Qt, QTimer

from ..features.progress_charts import PerformanceChart
from ..features.system_monitor import SystemMonitorWidget
from ..features.gpu_monitor import GPUMonitor

class ChartsPanel(QWidget):
    """Grafieken paneel"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup de UI"""
        layout = QVBoxLayout(self)
        
        # Titel
        title = QLabel("📊 Grafieken & Monitoring")
        title.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff;")
        layout.addWidget(title)
        
        # Tab widget voor verschillende grafieken
        self.tab_widget = QTabWidget()
        
        # Tab 1: Systeem Monitoring
        system_tab = QWidget()
        system_layout = QVBoxLayout(system_tab)
        
        self.system_monitor = SystemMonitorWidget()
        system_layout.addWidget(self.system_monitor)
        
        # Maak alleen GPU monitor aan (FFmpeg en LibreTranslate alleen als status labels)
        self.gpu_monitor = GPUMonitor(self)
        
        # Koppel alleen GPU chart aan monitor
        self.gpu_monitor.gpu_chart = self.system_monitor.gpu_chart
        
        # Koppel GPU monitor aan hoofdvenster (wordt later gedaan na initialisatie)
        self.gpu_monitor.main_window = None
        
        # Start timer om later te proberen te koppelen
        self.connection_timer = QTimer()
        self.connection_timer.timeout.connect(self._try_connect_monitors)
        self.connection_timer.start(1000)  # Probeer elke seconde te koppelen
        
        self.tab_widget.addTab(system_tab, "🖥️ Systeem")
        
        # Tab 2: Performance Metrics
        performance_tab = QWidget()
        performance_layout = QVBoxLayout(performance_tab)
        
        self.performance_chart = PerformanceChart()
        performance_layout.addWidget(self.performance_chart)
        
        self.tab_widget.addTab(performance_tab, "⚡ Performance")
        
        layout.addWidget(self.tab_widget)
    
    def start_processing_monitoring(self):
        """Start snelle monitoring tijdens verwerking"""
        if hasattr(self, 'system_monitor'):
            self.system_monitor.start_processing_monitoring()
        
        if hasattr(self, 'gpu_monitor'):
            # Geef verwerkingsstatus door aan GPU monitor
            self.gpu_monitor.set_processing_status(True, True)  # Processing + WhisperX
            self.gpu_monitor.start_processing_monitoring()
        else:
            print("⚠️ Charts Panel: GPU monitor niet beschikbaar")
        
        if hasattr(self, 'performance_chart'):
            self.performance_chart.start_processing_monitoring()
    
    def stop_processing_monitoring(self):
        """Stop snelle monitoring na verwerking"""
        if hasattr(self, 'system_monitor'):
            self.system_monitor.stop_processing_monitoring()
        
        if hasattr(self, 'gpu_monitor'):
            # Reset verwerkingsstatus in GPU monitor
            self.gpu_monitor.set_processing_status(False, False)
            self.gpu_monitor.stop_processing_monitoring()
        else:
            print("⚠️ Charts Panel: GPU monitor niet beschikbaar")
        
        if hasattr(self, 'performance_chart'):
            self.performance_chart.stop_processing_monitoring()
    
    def _try_connect_monitors(self):
        """Probeert de GPU monitor te koppelen aan het hoofdvenster na initialisatie."""
        main_window = self._find_main_window()
        if main_window:
            self.gpu_monitor.main_window = main_window
            self.connection_timer.stop()
            
            # Force een onmiddellijke update van de GPU status
            if hasattr(self, 'gpu_monitor'):
                self.gpu_monitor._update_gpu_status_display()
                # Start ook de GPU monitoring timer
                if hasattr(self.gpu_monitor, 'gpu_timer') and self.gpu_monitor.gpu_timer:
                    self.gpu_monitor.gpu_timer.start(500)  # Normale snelheid
        else:
            print("⚠️ GPU Monitor kon nog niet gekoppeld worden aan hoofdvenster. Probeer opnieuw...")
    
    def _find_main_window(self):
        """Zoek naar het hoofdvenster om statusbalk labels bij te werken"""
        parent = self.parent()
        while parent:
            if (hasattr(parent, 'gpu_status_label') and 
                hasattr(parent, 'gpu_memory_label')):
                return parent
            parent = parent.parent()
        
        print("⚠️ Charts Panel: Hoofdvenster niet gevonden")
        return None 