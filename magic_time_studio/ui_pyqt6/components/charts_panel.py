"""
Charts Panel component voor Magic Time Studio
Handelt grafieken en monitoring af
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QTabWidget, QLabel
)
from PyQt6.QtCore import Qt

from ..features.progress_charts import PerformanceChart
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
        
        # Tab 2: Performance Metrics
        performance_tab = QWidget()
        performance_layout = QVBoxLayout(performance_tab)
        
        self.performance_chart = PerformanceChart()
        performance_layout.addWidget(self.performance_chart)
        
        self.tab_widget.addTab(performance_tab, "⚡ Performance")
        
        layout.addWidget(self.tab_widget) 