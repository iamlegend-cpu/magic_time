"""
Charts Panel component voor Magic Time Studio
Handelt grafieken en monitoring af
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QTabWidget, QLabel
)
from PyQt6.QtCore import Qt

from ..features.progress_charts import ProcessingProgressChart, PerformanceChart
from ..features.system_monitor import SystemMonitorWidget

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
        
        self.tab_widget.addTab(system_tab, "🖥️ Systeem")
        
        # Tab 2: Verwerkingsvoortgang
        progress_tab = QWidget()
        progress_layout = QVBoxLayout(progress_tab)
        
        self.progress_chart = ProcessingProgressChart()
        progress_layout.addWidget(self.progress_chart)
        
        self.tab_widget.addTab(progress_tab, "🎬 Verwerking")
        
        # Tab 3: Performance Metrics
        performance_tab = QWidget()
        performance_layout = QVBoxLayout(performance_tab)
        
        self.performance_chart = PerformanceChart()
        performance_layout.addWidget(self.performance_chart)
        
        self.tab_widget.addTab(performance_tab, "⚡ Performance")
        
        layout.addWidget(self.tab_widget)
    
    def update_progress_chart(self, value: float):
        """Update progress chart"""
        if hasattr(self, 'progress_chart'):
            self.progress_chart.update_progress(value)
    
    def start_processing(self, total_files: int):
        """Start verwerking tracking"""
        if hasattr(self, 'progress_chart'):
            self.progress_chart.start_processing(total_files)
    
    def file_completed(self):
        """Bestand voltooid"""
        if hasattr(self, 'progress_chart'):
            self.progress_chart.file_completed()
    
    def reset_progress(self):
        """Reset voortgang"""
        if hasattr(self, 'progress_chart'):
            self.progress_chart.reset_progress() 