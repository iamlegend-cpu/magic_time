"""
Logging functionaliteit voor Magic Time Studio
"""

import os
import sys
from pathlib import Path

# Normale imports
try:
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
                        backupCount=5
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
        
except ImportError as e:
    print(f"⚠️ Logging import gefaald: {e}")
    
    # Fallback naar dummy logging functies
    def setup_logging():
        """Dummy logging setup"""
        print("✅ Logging geconfigureerd (dummy mode)")
    
    def get_logger(name: str):
        """Dummy logger"""
        class DummyLogger:
            def __init__(self):
                self.name = name
            def debug(self, msg): pass
            def info(self, msg): print(f"[INFO] {msg}")
            def warning(self, msg): print(f"[WARNING] {msg}")
            def error(self, msg): print(f"[ERROR] {msg}")
            def critical(self, msg): print(f"[CRITICAL] {msg}")
        return DummyLogger()

# Injecteer logging module in sys.modules voor compatibiliteit
if 'logging' not in sys.modules:
    import types
    logging_module = types.ModuleType('logging')
    logging_module.getLogger = get_logger
    logging_module.get_logger = get_logger
    logging_module.info = lambda msg: print(f"[INFO] {msg}")
    logging_module.warning = lambda msg: print(f"[WARNING] {msg}")
    logging_module.error = lambda msg: print(f"[ERROR] {msg}")
    logging_module.debug = lambda msg: print(f"[DEBUG] {msg}")
    logging_module.critical = lambda msg: print(f"[CRITICAL] {msg}")
    logging_module.basicConfig = lambda **kwargs: None
    logging_module.INFO = 20
    logging_module.WARNING = 30
    logging_module.ERROR = 40
    logging_module.CRITICAL = 50
    logging_module.DEBUG = 10
    sys.modules['logging'] = logging_module
    print("✅ Logging module geïnjecteerd in sys.modules") 