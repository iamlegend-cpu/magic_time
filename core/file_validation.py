"""
Bestand validatie en type detectie voor Magic Time Studio
Bevat functies voor het controleren van bestandstypes en validatie
"""

import os
from pathlib import Path
from typing import Optional

# Ondersteunde video extensies
VIDEO_EXTENSIONS = {
    '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', 
    '.m4v', '.3gp', '.ogv', '.ts', '.mts', '.m2ts'
}

# Ondersteunde audio extensies
AUDIO_EXTENSIONS = {
    '.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', '.opus'
}

# Ondersteunde ondertitel extensies
SUBTITLE_EXTENSIONS = {
    '.srt', '.vtt', '.ass', '.ssa', '.sub', '.txt'
}

def is_video_file(file_path: str) -> bool:
    """
    Controleer of een bestand een video bestand is
    
    Args:
        file_path: Pad naar het bestand
    
    Returns:
        True als het een video bestand is, False anders
    """
    if not file_path:
        return False
    
    file_ext = Path(file_path).suffix.lower()
    return file_ext in VIDEO_EXTENSIONS

def is_audio_file(file_path: str) -> bool:
    """
    Controleer of een bestand een audio bestand is
    
    Args:
        file_path: Pad naar het bestand
    
    Returns:
        True als het een audio bestand is, False anders
    """
    if not file_path:
        return False
    
    file_ext = Path(file_path).suffix.lower()
    return file_ext in AUDIO_EXTENSIONS

def is_subtitle_file(file_path: str) -> bool:
    """
    Controleer of een bestand een ondertitel bestand is
    
    Args:
        file_path: Pad naar het bestand
    
    Returns:
        True als het een ondertitel bestand is, False anders
    """
    if not file_path:
        return False
    
    file_ext = Path(file_path).suffix.lower()
    return file_ext in SUBTITLE_EXTENSIONS

def get_file_type(file_path: str) -> Optional[str]:
    """
    Bepaal het type van een bestand
    
    Args:
        file_path: Pad naar het bestand
    
    Returns:
        Bestandstype ('video', 'audio', 'subtitle', 'unknown') of None bij fout
    """
    if not file_path:
        return None
    
    if is_video_file(file_path):
        return 'video'
    elif is_audio_file(file_path):
        return 'audio'
    elif is_subtitle_file(file_path):
        return 'subtitle'
    else:
        return 'unknown'

def validate_file_exists(file_path: str) -> bool:
    """
    Valideer of een bestand bestaat
    
    Args:
        file_path: Pad naar het bestand
    
    Returns:
        True als het bestand bestaat, False anders
    """
    return os.path.exists(file_path) if file_path else False

def validate_file_readable(file_path: str) -> bool:
    """
    Valideer of een bestand leesbaar is
    
    Args:
        file_path: Pad naar het bestand
    
    Returns:
        True als het bestand leesbaar is, False anders
    """
    try:
        return os.access(file_path, os.R_OK) if file_path else False
    except Exception:
        return False

def validate_file_writable(file_path: str) -> bool:
    """
    Valideer of een bestand schrijfbaar is
    
    Args:
        file_path: Pad naar het bestand
    
    Returns:
        True als het bestand schrijfbaar is, False anders
    """
    try:
        return os.access(file_path, os.W_OK) if file_path else False
    except Exception:
        return False
