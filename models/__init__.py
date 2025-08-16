"""
Models module voor Magic Time Studio
"""

# Import alleen de ProgressTracker die geen circulaire imports heeft
from .progress_tracker import ProgressTracker

__all__ = ['ProgressTracker'] 