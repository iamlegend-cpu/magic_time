"""
Processing modules voor Magic Time Studio
Bevat video/audio verwerking en transcriptie functionaliteit
"""

# Processing modules
from .whisper_processor import WhisperProcessor, whisper_processor
from .translator import Translator, translator
from .audio_processor import AudioProcessor, audio_processor
from .video_processor import VideoProcessor, video_processor
from .batch_processor import BatchProcessor, batch_processor 