"""
Features module voor Magic Time Studio UI
"""

from .system_monitor import SystemMonitorWidget
from .gpu_monitor import GPUMonitor
from .cpu_ram_monitor import CPURAMMonitor
from .real_time_chart import RealTimeChart
from .performance_chart import PerformanceChart
from .batch_queue import BatchQueueManager
from .file_preview import FilePreviewWidget
from .modern_styling import ModernStyling
from .plugin_manager import PluginManager
from .processing_progress import ProcessingProgressChart
from .subtitle_preview import SubtitlePreviewWidget

__all__ = [
    'SystemMonitorWidget',
    'GPUMonitor',
    'CPURAMMonitor',
    'RealTimeChart',
    'PerformanceChart',
    'BatchQueueManager',
    'FilePreviewWidget',
    'ModernStyling',
    'PluginManager',
    'ProcessingProgressChart',
    'SubtitlePreviewWidget',
] 