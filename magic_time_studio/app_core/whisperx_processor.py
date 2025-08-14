"""
WhisperX Processor - Import Wrapper
Dit bestand is opgesplitst in modulaire componenten voor betere onderhoudbaarheid
"""

# Import alle functionaliteit uit de modulaire structuur
from .whisperx_core import WhisperXProcessor
from .whisperx_vad import VADManager, VADTester, VADOptimizer
from .whisperx_time_estimator import TimeEstimator
from .whisperx_utils import (
    convert_to_standard_format,
    create_accurate_srt,
    seconds_to_srt_timestamp,
    get_model_info,
    cleanup_cuda_context,
    setup_tf32
)

# Export alle klassen en functies voor backward compatibility
__all__ = [
    'WhisperXProcessor',
    'VADManager',
    'VADTester', 
    'VADOptimizer',
    'TimeEstimator',
    'convert_to_standard_format',
    'create_accurate_srt',
    'seconds_to_srt_timestamp',
    'get_model_info',
    'cleanup_cuda_context',
    'setup_tf32'
]
