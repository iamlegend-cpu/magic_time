"""
Whisper Selector Components Package
UI components voor het kiezen tussen standaard Whisper en Fast Whisper
"""

from .whisper_selector_widget import WhisperSelectorWidget
from .model_load_thread import ModelLoadThread

__all__ = ['WhisperSelectorWidget', 'ModelLoadThread']
