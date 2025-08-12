"""
Processing Modules voor Magic Time Studio
Bevat alle verwerking modules voor audio, video, whisper en vertaling
"""

from .audio_processor import AudioProcessor
from .whisper_processor import WhisperProcessor
from .translation_processor import TranslationProcessor
from .video_processor import VideoProcessor

__all__ = [
    'AudioProcessor',
    'WhisperProcessor', 
    'TranslationProcessor',
    'VideoProcessor'
]
