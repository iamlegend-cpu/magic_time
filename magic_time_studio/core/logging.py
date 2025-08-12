"""
Logging functionaliteit voor Magic Time Studio
"""

import os
import datetime
import queue
import threading
from typing import Optional, Tuple, Any

# Globale variabelen
log_queue = queue.Queue()
log_text_widget: Optional[object] = None  # PyQt6 QTextEdit widget
USER_OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "MagicTime_Output")

class Logger:
    """Centrale logging klasse"""
    
    def __init__(self):
        self.log_queue = queue.Queue()
        self.log_text_widget = None
        
        # Lazy import van config_manager om circulaire import te voorkomen
        self._config_manager = None
        
        # Laad logging configuratie uit environment variables
        self.log_to_file = self._get_config("LOG_TO_FILE", "false").lower() == "true"
        self.log_level = self._get_config("LOG_LEVEL", "INFO").upper()
        
        # Debug output voor logging configuratie (alleen in debug mode)
        if self.log_level == "DEBUG":
            print(f"🔧 [DEBUG] Logger configuratie:")
            print(f"🔧 [DEBUG] LOG_TO_FILE: {self.log_to_file}")
            print(f"🔧 [DEBUG] LOG_LEVEL: {self.log_level}")
        
        # Log bestand pad
        if self.log_to_file:
            log_file_path = self._get_config("LOG_FILE_PATH", "")
            if log_file_path:
                self.log_path = log_file_path
            else:
                self.log_path = os.path.join(USER_OUTPUT_DIR, "logs")
        else:
            self.log_path = None
        
        # Zorg ervoor dat output directory bestaat
        os.makedirs(USER_OUTPUT_DIR, exist_ok=True)
    
    def _get_config(self, key: str, default: Any = "") -> Any:
        """Lazy config manager import om circulaire import te voorkomen"""
        if self._config_manager is None:
            try:
                from .config import config_manager
                self._config_manager = config_manager
            except ImportError:
                # Fallback naar environment variables
                if key == "logging_config":
                    return {"debug": True, "info": True, "warning": True, "error": True}
                return os.getenv(key, default)
        
        if self._config_manager:
            if key == "logging_config":
                return self._config_manager.get("logging_config", {"debug": True, "info": True, "warning": True, "error": True})
            return self._config_manager.get_env(key, default)
        else:
            if key == "logging_config":
                return {"debug": True, "info": True, "warning": True, "error": True}
            return os.getenv(key, default)

    def add_log_message(self, msg: str, level: str = "INFO") -> None:
        """Voeg een bericht toe aan de log queue voor real-time updates"""
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        
        # Kleur codering voor verschillende levels
        if level == "ERROR":
            full_msg = f"{timestamp} ❌ {msg}"
            color = "red"
        elif level == "SUCCESS":
            full_msg = f"{timestamp} ✅ {msg}"
            color = "green"
        elif level == "WARNING":
            full_msg = f"{timestamp} ⚠️ {msg}"
            color = "orange"
        else:
            full_msg = f"{timestamp} ℹ️ {msg}"
            color = "black"
        
        # Schrijf naar bestand (alleen als logging naar bestand is ingeschakeld)
        if self.log_to_file and self.log_path:
            try:
                # Zorg ervoor dat de directory bestaat
                os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
                with open(self.log_path, "a", encoding="utf-8") as f:
                    f.write(full_msg + "\n")
            except Exception as e:
                pass  # Stil falen in productie
        
        # Voeg toe aan queue voor real-time updates
        try:
            self.log_queue.put((full_msg, color))
        except Exception as e:
            pass  # Stil falen in productie
    
    def log_debug(self, msg: str, category: str = "debug") -> None:
        """Log een bericht met debug level en categorie filtering"""
        # Controleer of deze categorie gelogd moet worden
        # Forceer debug mode als LOG_LEVEL=DEBUG
        if self.log_level == "DEBUG":
            # Toon alle berichten in debug mode
            pass
        else:
            # Eenvoudige categorie filtering zonder complexe config
            if category in ["error", "success", "warning"]:
                pass  # Toon belangrijke berichten
            else:
                # Voor andere categorieën, toon alleen in debug mode
                if self.log_level != "DEBUG":
                    return
        
        # Voeg timestamp toe
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] {msg}"

        # Print naar terminal (met None check voor PyInstaller)
        try:
            import sys
            if sys.stdout is not None:
                print(formatted_msg)
        except:
            pass  # Stil falen als stdout niet beschikbaar is

        # Voeg toe aan GUI log queue voor real-time updates (alleen voor belangrijke berichten)
        if category in ["error", "success", "warning"] or "Fout" in msg or "✅" in msg or "❌" in msg:
            self.add_log_message(msg, "INFO")

        # Ook direct naar live log viewer als die open is (alleen voor belangrijke berichten)
        if self.log_text_widget is not None and (category in ["error", "success", "warning"] or "Fout" in msg or "✅" in msg or "❌" in msg):
            try:
                # PyQt6 QTextEdit append methode
                self.log_text_widget.append(f"{formatted_msg}")
            except:
                pass
        
        # Schrijf naar debug log bestand als LOG_TO_FILE=true
        if self.log_to_file and self.log_path:
            try:
                os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
                with open(self.log_path, "a", encoding="utf-8") as f:
                    f.write(f"{formatted_msg}\n")
            except Exception as e:
                pass  # Stil falen in productie
    
    def set_log_widget(self, widget: object) -> None:
        """Zet de log text widget"""
        self.log_text_widget = widget
    
    def get_log_queue(self) -> queue.Queue:
        """Krijg de log queue"""
        return self.log_queue
    
    def log_system_info(self) -> None:
        """Log systeem informatie"""
        try:
            import psutil
            memory = psutil.virtual_memory()
            cpu_percent = psutil.cpu_percent()
            self.log_debug(
                f"💾 RAM: {memory.percent}% gebruikt ({memory.available/1024/1024/1024:.1f}GB vrij)",
                "log_system_info"
            )
            self.log_debug(f"💻 CPU: {cpu_percent}% gebruikt", "log_system_info")
        except ImportError:
            self.log_debug("💻 Systeem monitoring niet beschikbaar (psutil niet geïnstalleerd)", "log_system_info")

# Globale logger instantie
logger = Logger()

# Helper functies voor backward compatibility
def add_log_message(msg: str, level: str = "INFO") -> None:
    """Backward compatibility functie"""
    logger.add_log_message(msg, level)

def log_debug(msg: str, category: str = "debug") -> None:
    """Backward compatibility functie"""
    logger.log_debug(msg, category)

def update_log_viewer(viewer, message, color):
    """Update een log viewer met gekleurde tekst - UITGESCHAKELD voor stabiliteit"""
    # Log viewer is uitgeschakeld om fouten te voorkomen
    pass

def start_log_monitor():
    """Start de log monitor thread - UITGESCHAKELD voor stabiliteit"""
    # Log monitor is uitgeschakeld om oneindige loops te voorkomen
    pass

def log_system_info():
    """Backward compatibility functie"""
    logger.log_system_info() 