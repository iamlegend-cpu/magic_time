"""
Logging functionaliteit voor Magic Time Studio
"""

import os
import datetime
import queue
import threading
import tkinter as tk
from typing import Optional, Tuple
from .config import config_manager

# Globale variabelen
log_queue = queue.Queue()
log_text_widget: Optional[tk.Text] = None
USER_OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "MagicTime_Output")

class Logger:
    """Centrale logging klasse"""
    
    def __init__(self):
        self.log_queue = queue.Queue()
        self.log_text_widget = None
        
        # Laad logging configuratie uit environment variables
        self.log_to_file = config_manager.get_env("LOG_TO_FILE", "false").lower() == "true"
        self.log_level = config_manager.get_env("LOG_LEVEL", "INFO").upper()
        
        # Log bestand pad
        if self.log_to_file:
            log_file_path = config_manager.get_env("LOG_FILE_PATH", "")
            if log_file_path:
                self.log_path = log_file_path
            else:
                self.log_path = os.path.join(USER_OUTPUT_DIR, "MagicTime_debug_log.txt")
        else:
            self.log_path = None
        
        # Zorg ervoor dat output directory bestaat
        os.makedirs(USER_OUTPUT_DIR, exist_ok=True)
    
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
        logging_config = config_manager.get("logging_config", {})
        
        # Controleer of deze categorie gelogd moet worden
        if category in logging_config and not logging_config[category]:
            return
        
        # Voeg timestamp toe
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] {msg}"

        # Print naar terminal
        print(formatted_msg)

        # Voeg toe aan GUI log queue voor real-time updates (alleen voor belangrijke berichten)
        if category in ["error", "success", "warning"] or "Fout" in msg or "✅" in msg or "❌" in msg:
            self.add_log_message(msg, "INFO")

        # Ook direct naar live log viewer als die open is (alleen voor belangrijke berichten)
        if self.log_text_widget is not None and (category in ["error", "success", "warning"] or "Fout" in msg or "✅" in msg or "❌" in msg):
            try:
                self.log_text_widget.insert(tk.END, f"{formatted_msg}\n")
                self.log_text_widget.see(tk.END)
            except:
                pass
    
    def set_log_widget(self, widget: tk.Text) -> None:
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