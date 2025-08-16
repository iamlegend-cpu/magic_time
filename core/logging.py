"""
Logging functionaliteit voor Magic Time Studio
"""

import os
import sys
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    """Setup logging configuratie"""
    try:
        # Maak logs directory
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Configureer logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                RotatingFileHandler(
                    log_dir / "magic_time_studio.log",
                    maxBytes=10*1024*1024,  # 10MB
                    backupCount=5,
                    encoding='utf-8'  # UTF-8 encoding voor emoji support
                ),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        print("✅ Logging geconfigureerd")
        
    except Exception as e:
        print(f"⚠️ Fout bij setup logging: {e}")

def get_logger(name: str):
    """Krijg een logger instance"""
    return logging.getLogger(name)

# Export een standaard logger voor compatibiliteit
logger = get_logger("magic_time_studio") 