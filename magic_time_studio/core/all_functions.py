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
    'get_directory_files',
    'get_video_files',
    'get_audio_files',
    'get_subtitle_files',
    'find_files_by_pattern',
    'create_temp_file',
    'create_temp_directory',
    'copy_file',
    'move_file',
    'delete_file',
    'delete_directory',
    'rename_file',
    'compare_files',
    'backup_file',
    'restore_backup',
    'ensure_directory_exists'
]

# Constanten
__version__ = "2.0.0"
__author__ = "Magic Time Studio Team"
__description__ = "Alle functies voor Magic Time Studio in één overzicht"

# Functie categorieën voor gemakkelijke navigatie
FUNCTION_CATEGORIES = {
    "Audio": [
        'extract_audio_from_video',
        'get_audio_duration',
        'convert_audio_format',
        'normalize_audio',
        'split_audio_by_silence'
    ],
    "Video": [
        'get_video_info',
        'get_video_duration',
        'get_video_resolution',
        'extract_video_frame',
        'create_video_thumbnail',
        'merge_video_audio',
        'convert_video_format',
        'compress_video'
    ],
    "Whisper": [
        'load_whisper_model',
        'transcribe_audio_fast_whisper',
        'transcribe_audio_standard_whisper',
        'detect_language',
        'transcribe_with_timestamps',
        'save_transcription_to_srt',
        'format_timestamp',
        'get_whisper_model_info'
    ],
    "Vertaling": [
        'translate_text_libretranslate',
        'translate_text_google',
        'translate_text_deepl',
        'translate_text',
        'translate_transcriptions',
        'batch_translate_texts',
        'detect_language_from_text',
        'get_supported_languages',
        'validate_language_code',
        'get_language_name'
    ],
    "Ondertitels": [
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
        'read_ass_file'
    ],
    "Bestanden": [
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
        'get_directory_files',
        'get_video_files',
        'get_audio_files',
        'get_subtitle_files',
        'find_files_by_pattern',
        'create_temp_file',
        'create_temp_directory',
        'copy_file',
        'move_file',
        'delete_file',
        'delete_directory',
        'rename_file',
        'compare_files',
        'backup_file',
        'restore_backup',
        'ensure_directory_exists'
    ]
}

def get_functions_by_category(category: str) -> list:
    """
    Krijg alle functies van een bepaalde categorie
    
    Args:
        category: Naam van de categorie
    
    Returns:
        Lijst van functie namen in die categorie
    """
    return FUNCTION_CATEGORIES.get(category, [])

def get_all_categories() -> list:
    """
    Krijg alle beschikbare categorieën
    
    Returns:
        Lijst van alle categorie namen
    """
    return list(FUNCTION_CATEGORIES.keys())

def search_functions(search_term: str) -> list:
    """
    Zoek functies op basis van een zoekterm
    
    Args:
        search_term: Zoekterm om te zoeken
    
    Returns:
        Lijst van functie namen die matchen
    """
    search_term = search_term.lower()
    matching_functions = []
    
    for category, functions in FUNCTION_CATEGORIES.items():
        for func_name in functions:
            if search_term in func_name.lower() or search_term in category.lower():
                matching_functions.append(func_name)
    
    return matching_functions

def get_function_info(function_name: str) -> dict:
    """
    Krijg informatie over een specifieke functie
    
    Args:
        function_name: Naam van de functie
    
    Returns:
        Dictionary met functie informatie
    """
    # Zoek in welke categorie de functie hoort
    for category, functions in FUNCTION_CATEGORIES.items():
        if function_name in functions:
            return {
                "name": function_name,
                "category": category,
                "available": True
            }
    
    return {
        "name": function_name,
        "category": "Onbekend",
        "available": False
    }

def list_all_functions() -> dict:
    """
    Krijg een overzicht van alle functies per categorie
    
    Returns:
        Dictionary met alle functies per categorie
    """
    return FUNCTION_CATEGORIES.copy()

# Voorbeeld gebruik
if __name__ == "__main__":
    print(f"Magic Time Studio v{__version__}")
    print(f"Beschikbare categorieën: {get_all_categories()}")
    print(f"Totaal aantal functies: {len(__all__)}")
    
    # Toon functies per categorie
    for category, functions in FUNCTION_CATEGORIES.items():
        print(f"\n{category} ({len(functions)} functies):")
        for func in functions:
            print(f"  - {func}")
