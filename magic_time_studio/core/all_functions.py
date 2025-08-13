"""
Alle functies voor Magic Time Studio
Dit bestand brengt alle functionaliteit samen in één overzicht
"""

# Import alle functie modules
from .audio_functions import *
from .video_functions import *
from .whisper_functions import *
from .translation_functions import *
from .subtitle_functions import *

# Import bestand functies uit de nieuwe gesplitste modules
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

# Maak alle functies beschikbaar
__all__ = [
    # Audio functies
    'extract_audio_from_video',
    'get_audio_duration',
    'convert_audio_format',
    'normalize_audio',
    'split_audio_by_silence',
    
    # Video functies
    'get_video_info',
    'get_video_duration',
    'get_video_resolution',
    'extract_video_frame',
    'create_video_thumbnail',
    'merge_video_audio',
    'convert_video_format',
    'compress_video',
    
    # Whisper functies
    'load_whisper_model',
    'transcribe_audio_fast_whisper',
    'transcribe_audio_standard_whisper',
    'detect_language',
    'transcribe_with_timestamps',
    'save_transcription_to_srt',
    'format_timestamp',
    'get_whisper_model_info',
    
    # Vertaling functies
    'translate_text_libretranslate',
    'translate_text_google',
    'translate_text_deepl',
    'translate_text',
    'translate_transcriptions',
    'batch_translate_texts',
    'detect_language_from_text',
    'get_supported_languages',
    'validate_language_code',
    'get_language_name',
    
    # Ondertitel functies
    'create_srt_content',
    'create_vtt_content',
    'create_ass_content',
    'format_timestamp',
    'format_vtt_timestamp',
    'format_ass_timestamp',
    'escape_ass_text',
    'merge_subtitle_files',
    'read_subtitle_file',
    'read_srt_file',
    'read_vtt_file',
    'read_ass_file',
    
    # Bestand functies
    'is_video_file',
    'is_audio_file',
    'is_subtitle_file',
    'get_file_type',
    'validate_file_exists',
    'validate_file_readable',
    'validate_file_writable',
    'VIDEO_EXTENSIONS',
    'AUDIO_EXTENSIONS',
    'SUBTITLE_EXTENSIONS',
    'get_file_info',
    'get_file_size_formatted',
    'get_file_hash',
    'get_relative_path',
    'copy_file',
    'move_file',
    'delete_file',
    'delete_directory',
    'rename_file',
    'ensure_directory_exists',
    'get_directory_files',
    'get_video_files',
    'get_audio_files',
    'get_subtitle_files',
    'find_files_by_pattern',
    'create_temp_file',
    'create_temp_directory',
    'compare_files',
    'backup_file',
    'restore_backup'
]

# Debug: toon alle beschikbare functies
if __name__ == "__main__":
    print("🔍 Beschikbare functies in all_functions:")
    for func in __all__:
        print(f"  - {func}")
