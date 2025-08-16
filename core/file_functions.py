"""
Bestand functies voor Magic Time Studio
Hoofdmodule die alle bestand-gerelateerde functionaliteit importeert
"""

# Import alle functies uit de gesplitste modules
from .file_validation import (
    is_video_file, is_audio_file, is_subtitle_file, get_file_type,
    validate_file_exists, validate_file_readable, validate_file_writable,
    VIDEO_EXTENSIONS, AUDIO_EXTENSIONS, SUBTITLE_EXTENSIONS
)

from .file_info import (
    get_file_info, get_file_size_formatted, get_file_hash, get_relative_path
)

from .file_operations import (
    copy_file, move_file, delete_file, delete_directory, rename_file, ensure_directory_exists
)

from .file_search import (
    get_directory_files, get_video_files, get_audio_files, 
    get_subtitle_files, find_files_by_pattern
)

from .file_utilities import (
    create_temp_file, create_temp_directory, compare_files, backup_file, restore_backup
)

# Export alle functies voor backward compatibility
__all__ = [
    # File validation
    'is_video_file', 'is_audio_file', 'is_subtitle_file', 'get_file_type',
    'validate_file_exists', 'validate_file_readable', 'validate_file_writable',
    'VIDEO_EXTENSIONS', 'AUDIO_EXTENSIONS', 'SUBTITLE_EXTENSIONS',
    
    # File info
    'get_file_info', 'get_file_size_formatted', 'get_file_hash', 'get_relative_path',
    
    # File operations
    'copy_file', 'move_file', 'delete_file', 'delete_directory', 'rename_file', 'ensure_directory_exists',
    
    # File search
    'get_directory_files', 'get_video_files', 'get_audio_files', 
    'get_subtitle_files', 'find_files_by_pattern',
    
    # File utilities
    'create_temp_file', 'create_temp_directory', 'compare_files', 'backup_file', 'restore_backup'
]

# Backward compatibility - alle functies zijn beschikbaar via imports hierboven
# Dit zorgt ervoor dat bestaande code blijft werken
