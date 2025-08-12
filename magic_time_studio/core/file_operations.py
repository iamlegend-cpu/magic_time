"""
Bestand operaties voor Magic Time Studio
Bevat functies voor het kopiëren, verplaatsen en verwijderen van bestanden
"""

import os
import shutil
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def copy_file(source_path: str, destination_path: str, overwrite: bool = False) -> bool:
    """Kopieer een bestand"""
    try:
        if not os.path.exists(source_path):
            logger.error(f"Bron bestand bestaat niet: {source_path}")
            return False
        
        if os.path.exists(destination_path) and not overwrite:
            logger.error(f"Doel bestand bestaat al: {destination_path}")
            return False
        
        dest_dir = os.path.dirname(destination_path)
        if dest_dir and not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        
        shutil.copy2(source_path, destination_path)
        logger.info(f"Bestand gekopieerd: {source_path} -> {destination_path}")
        return True
        
    except Exception as e:
        logger.error(f"Fout bij kopiëren bestand: {e}")
        return False

def move_file(source_path: str, destination_path: str, overwrite: bool = False) -> bool:
    """Verplaats een bestand"""
    try:
        if not os.path.exists(source_path):
            logger.error(f"Bron bestand bestaat niet: {source_path}")
            return False
        
        if os.path.exists(destination_path) and not overwrite:
            logger.error(f"Doel bestand bestaat al: {destination_path}")
            return False
        
        dest_dir = os.path.dirname(destination_path)
        if dest_dir and not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        
        shutil.move(source_path, destination_path)
        logger.info(f"Bestand verplaatst: {source_path} -> {destination_path}")
        return True
        
    except Exception as e:
        logger.error(f"Fout bij verplaatsen bestand: {e}")
        return False

def delete_file(file_path: str) -> bool:
    """Verwijder een bestand"""
    try:
        if not os.path.exists(file_path):
            logger.warning(f"Bestand bestaat niet: {file_path}")
            return True
        
        os.remove(file_path)
        logger.info(f"Bestand verwijderd: {file_path}")
        return True
        
    except Exception as e:
        logger.error(f"Fout bij verwijderen bestand: {e}")
        return False

def delete_directory(directory_path: str, recursive: bool = True) -> bool:
    """Verwijder een directory"""
    try:
        if not os.path.exists(directory_path):
            logger.warning(f"Directory bestaat niet: {directory_path}")
            return True
        
        if not os.path.isdir(directory_path):
            logger.error(f"Pad is geen directory: {directory_path}")
            return False
        
        if recursive:
            shutil.rmtree(directory_path)
        else:
            os.rmdir(directory_path)
        
        logger.info(f"Directory verwijderd: {directory_path}")
        return True
        
    except Exception as e:
        logger.error(f"Fout bij verwijderen directory: {e}")
        return False

def rename_file(old_path: str, new_name: str) -> bool:
    """Hernoem een bestand"""
    try:
        if not os.path.exists(old_path):
            logger.error(f"Bestand bestaat niet: {old_path}")
            return False
        
        old_dir = os.path.dirname(old_path)
        new_path = os.path.join(old_dir, new_name)
        
        if os.path.exists(new_path):
            logger.error(f"Nieuw bestand bestaat al: {new_path}")
            return False
        
        os.rename(old_path, new_path)
        logger.info(f"Bestand hernoemd: {old_path} -> {new_path}")
        return True
        
    except Exception as e:
        logger.error(f"Fout bij hernoemen bestand: {e}")
        return False

def ensure_directory_exists(directory_path: str) -> bool:
    """Zorg ervoor dat een directory bestaat"""
    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path, exist_ok=True)
            logger.info(f"Directory aangemaakt: {directory_path}")
        return True
        
    except Exception as e:
        logger.error(f"Fout bij aanmaken directory: {e}")
        return False
