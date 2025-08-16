"""
Real-time grafieken voor Magic Time Studio
Hoofdbestand dat alle chart componenten samenbrengt
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QLabel

# Import alle refactored componenten
from .real_time_chart import RealTimeChart
from .performance_chart import PerformanceChart
from .subtitle_preview import SubtitlePreviewWidget


# ChartsPanel is verplaatst naar components/charts_panel.py
# Deze file bevat alleen nog de individuele componenten 