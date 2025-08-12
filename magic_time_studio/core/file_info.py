"""
Bestand informatie en metadata voor Magic Time Studio
Bevat functies voor het ophalen van bestand informatie
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

def get_file_info(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Haal informatie op over een bestand
    
    Args:
        file_path: Pad naar het bestand
    
    Returns:
        Dictionary met bestand informatie of None bij fout
    """
    try:
        if not os.path.exists(file_path):
            logger.error(f"Bestand bestaat niet: {file_path}")
            return None
        
        stat_info = os.stat(file_path)
        path_obj = Path(file_path)
        
        # Import hier om circulaire import te voorkomen
        from .file_validation import is_video_file, is_audio_file, is_subtitle_file
        
        file_info = {
            "name": path_obj.name,
            "stem": path_obj.stem,
            "suffix": path_obj.suffix.lower(),
            "parent": str(path_obj.parent),
            "absolute_path": str(path_obj.absolute()),
            "size_bytes": stat_info.st_size,
            "size_mb": round(stat_info.st_size / (1024 * 1024), 2),
            "created_time": stat_info.st_ctime,
            "modified_time": stat_info.st_mtime,
            "accessed_time": stat_info.st_atime,
            "is_file": path_obj.is_file(),
            "is_dir": path_obj.is_dir(),
            "is_video": is_video_file(file_path),
            "is_audio": is_audio_file(file_path),
            "is_subtitle": is_subtitle_file(file_path)
        }
        
        return file_info
        
    except Exception as e:
        logger.error(f"Fout bij ophalen bestand informatie: {e}")
        return None

def get_file_size_formatted(file_path: str) -> str:
    """
    Krijg de bestandsgrootte in een leesbaar formaat
    
    Args:
        file_path: Pad naar het bestand
    
    Returns:
        Geformatteerde bestandsgrootte string
    """
    try:
        if not os.path.exists(file_path):
            return "0 B"
        
        size_bytes = os.path.getsize(file_path)
        
        # Converteer naar leesbaar formaat
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        
        return f"{size_bytes:.1f} PB"
        
    except Exception as e:
        logger.error(f"Fout bij formatteren bestandsgrootte: {e}")
        return "0 B"

def get_file_hash(file_path: str, algorithm: str = "md5") -> Optional[str]:
    """
    Bereken de hash van een bestand
    
    Args:
        file_path: Pad naar het bestand
        algorithm: Hash algoritme (md5, sha1, sha256)
    
    Returns:
        Hash string of None bij fout
    """
    try:
        if not os.path.exists(file_path):
            logger.error(f"Bestand bestaat niet: {file_path}")
            return None
        
        import hashlib
        hash_obj = hashlib.new(algorithm)
        
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)
        
        return hash_obj.hexdigest()
        
    except Exception as e:
        logger.error(f"Fout bij berekenen bestand hash: {e}")
        return None

def get_relative_path(file_path: str, base_directory: str) -> Optional[str]:
    """
    Krijg het relatieve pad van een bestand ten opzichte van een basis directory
    
    Args:
        file_path: Pad naar het bestand
        base_directory: Basis directory
    
    Returns:
        Relatief pad of None bij fout
    """
    try:
        file_path = os.path.abspath(file_path)
        base_directory = os.path.abspath(base_directory)
        
        if not file_path.startswith(base_directory):
            return None
        
        relative_path = os.path.relpath(file_path, base_directory)
        return relative_path
        
    except Exception as e:
        logger.error(f"Fout bij berekenen relatief pad: {e}")
        return None
