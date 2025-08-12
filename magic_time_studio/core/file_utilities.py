"""
Bestand utility functies voor Magic Time Studio
Bevat functies voor temp bestanden, backup en bestand vergelijking
"""

import os
import tempfile
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def create_temp_file(prefix: str = "magic_time_", suffix: str = ".tmp",
                    directory: Optional[str] = None) -> Optional[str]:
    """Maak een tijdelijk bestand aan"""
    try:
        temp_file = tempfile.NamedTemporaryFile(
            prefix=prefix,
            suffix=suffix,
            dir=directory,
            delete=False
        )
        temp_file.close()
        return temp_file.name
        
    except Exception as e:
        logger.error(f"Fout bij aanmaken tijdelijk bestand: {e}")
        return None

def create_temp_directory(prefix: str = "magic_time_",
                         directory: Optional[str] = None) -> Optional[str]:
    """Maak een tijdelijke directory aan"""
    try:
        temp_dir = tempfile.mkdtemp(prefix=prefix, dir=directory)
        return temp_dir
        
    except Exception as e:
        logger.error(f"Fout bij aanmaken tijdelijke directory: {e}")
        return None

def compare_files(file1_path: str, file2_path: str) -> bool:
    """Vergelijk twee bestanden"""
    try:
        if not os.path.exists(file1_path) or not os.path.exists(file2_path):
            return False
        
        if os.path.getsize(file1_path) != os.path.getsize(file2_path):
            return False
        
        with open(file1_path, 'rb') as f1, open(file2_path, 'rb') as f2:
            while True:
                chunk1 = f1.read(4096)
                chunk2 = f2.read(4096)
                
                if chunk1 != chunk2:
                    return False
                
                if not chunk1:
                    break
        
        return True
        
    except Exception as e:
        logger.error(f"Fout bij vergelijken bestanden: {e}")
        return False

def backup_file(file_path: str, backup_suffix: str = ".backup") -> Optional[str]:
    """Maak een backup van een bestand"""
    try:
        if not os.path.exists(file_path):
            logger.error(f"Bestand bestaat niet: {file_path}")
            return None
        
        backup_path = file_path + backup_suffix
        counter = 1
        while os.path.exists(backup_path):
            backup_path = f"{file_path}{backup_suffix}.{counter}"
            counter += 1
        
        from .file_operations import copy_file
        if copy_file(file_path, backup_path, overwrite=False):
            logger.info(f"Backup gemaakt: {backup_path}")
            return backup_path
        else:
            return None
        
    except Exception as e:
        logger.error(f"Fout bij maken backup: {e}")
        return None

def restore_backup(backup_path: str, original_path: str) -> bool:
    """Herstel een bestand vanuit een backup"""
    try:
        if not os.path.exists(backup_path):
            logger.error(f"Backup bestand bestaat niet: {backup_path}")
            return False
        
        # Maak backup van origineel bestand als het bestaat
        if os.path.exists(original_path):
            backup_original = backup_file(original_path, ".restore_backup")
            if not backup_original:
                logger.warning("Kon geen backup maken van origineel bestand")
        
        from .file_operations import copy_file
        if copy_file(backup_path, original_path, overwrite=True):
            logger.info(f"Backup hersteld: {backup_path} -> {original_path}")
            return True
        else:
            return False
        
    except Exception as e:
        logger.error(f"Fout bij herstellen backup: {e}")
        return False
