"""
Whisper Selector Component voor Magic Time Studio
Backward compatibility import voor bestaande code
"""

# Import van de nieuwe modulaire structuur
from .whisper_selector.whisper_selector_widget import WhisperSelectorWidget
from .whisper_selector.model_load_thread import ModelLoadThread

# Behoud backward compatibility
__all__ = ['WhisperSelectorWidget', 'ModelLoadThread'] 