"""
Bestand zoeken en directory functies voor Magic Time Studio
Bevat functies voor het zoeken en doorlopen van directories
"""

import os
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

def get_directory_files(directory_path: str, recursive: bool = False,
                       file_types: Optional[List[str]] = None) -> List[str]:
    """
    Haal alle bestanden op uit een directory
    
    Args:
        directory_path: Pad naar de directory
        recursive: Of recursief door subdirectories moet worden gezocht
        file_types: Lijst van bestand extensies om te filteren (optioneel)
    
    Returns:
        Lijst van bestand paden
    """
    try:
        if not os.path.exists(directory_path):
            logger.error(f"Directory bestaat niet: {directory_path}")
            return []
        
        if not os.path.isdir(directory_path):
            logger.error(f"Pad is geen directory: {directory_path}")
            return []
        
        file_paths = []
        
        if recursive:
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file_types:
                        if any(file.lower().endswith(ext) for ext in file_types):
                            file_paths.append(file_path)
                    else:
                        file_paths.append(file_path)
        else:
            for item in os.listdir(directory_path):
                item_path = os.path.join(directory_path, item)
                if os.path.isfile(item_path):
                    if file_types:
                        if any(item.lower().endswith(ext) for ext in file_types):
                            file_paths.append(item_path)
                    else:
                        file_paths.append(item_path)
        
        return sorted(file_paths)
        
    except Exception as e:
        logger.error(f"Fout bij ophalen directory bestanden: {e}")
        return []

def get_video_files(directory_path: str, recursive: bool = False) -> List[str]:
    """Haal alle video bestanden op uit een directory"""
    from .file_validation import VIDEO_EXTENSIONS
    return get_directory_files(directory_path, recursive, list(VIDEO_EXTENSIONS))

def get_audio_files(directory_path: str, recursive: bool = False) -> List[str]:
    """Haal alle audio bestanden op uit een directory"""
    from .file_validation import AUDIO_EXTENSIONS
    return get_directory_files(directory_path, recursive, list(AUDIO_EXTENSIONS))

def get_subtitle_files(directory_path: str, recursive: bool = False) -> List[str]:
    """Haal alle ondertitel bestanden op uit een directory"""
    from .file_validation import SUBTITLE_EXTENSIONS
    return get_directory_files(directory_path, recursive, list(SUBTITLE_EXTENSIONS))

def find_files_by_pattern(directory_path: str, pattern: str, recursive: bool = True) -> List[str]:
    """
    Zoek bestanden op basis van een patroon
    
    Args:
        directory_path: Pad naar de directory om te zoeken
        pattern: Patroon om te zoeken (bijv. "*.mp4")
        recursive: Of recursief door subdirectories moet worden gezocht
    
    Returns:
        Lijst van gevonden bestand paden
    """
    try:
        import glob
        search_pattern = os.path.join(directory_path, "**" if recursive else "", pattern)
        return glob.glob(search_pattern, recursive=recursive)
        
    except Exception as e:
        logger.error(f"Fout bij zoeken naar bestanden met patroon: {e}")
        return []
