"""
Plugin system voor Magic Time Studio
"""

from magic_time_studio.ui_pyqt6.features.plugins.audio_analyzer_plugin import AudioAnalyzerPlugin
from magic_time_studio.ui_pyqt6.features.plugins.batch_processor_plugin import BatchProcessorPlugin

__all__ = [
    'AudioAnalyzerPlugin',
    'BatchProcessorPlugin'
] 