"""
Features module voor Magic Time Studio UI
"""

from .modern_styling import ModernStyling
from .file_preview import FilePreviewWidget
from .batch_queue import BatchQueueManager
from .progress_charts import RealTimeChart, PerformanceChart
from .subtitle_preview import SubtitlePreviewWidget
from .system_monitor import SystemMonitorWidget
from .plugin_manager import PluginManager

__all__ = [
    'ModernStyling',
    'FilePreviewWidget',
    'BatchQueueManager',
    'RealTimeChart',
    'SystemMonitorWidget',
    'PerformanceChart',
    'SubtitlePreviewWidget',
    'PluginManager'
] 