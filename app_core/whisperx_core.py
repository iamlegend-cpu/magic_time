"""
WhisperX Core Processor - Modulaire versie
Import van de nieuwe modulaire structuur
"""

# Import van de nieuwe modulaire versie
from .whisperx.whisperx_processor import WhisperXProcessor

# Behoud backward compatibility
__all__ = ['WhisperXProcessor']
