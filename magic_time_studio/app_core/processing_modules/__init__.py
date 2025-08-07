"""
Processing modules voor Magic Time Studio
"""

from .audio_processing import AudioProcessor
from .whisper_processing import WhisperProcessor
from .translation_processing import TranslationProcessor
from .video_processing import VideoProcessor

__all__ = [
    'AudioProcessor',
    'WhisperProcessor', 
    'TranslationProcessor',
    'VideoProcessor'
]
