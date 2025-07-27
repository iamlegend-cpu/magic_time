"""
Configuratie management voor Magic Time Studio
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path

# Standaard configuratie waarden (worden overschreven door .env)
DEFAULT_CONFIG = {
    "translator": "libretranslate",
    "subtitle_type": "softcoded",
    "hardcoded_language": "dutch_only",
    "font_size": 9,
    "worker_count": 4,
    "theme": "dark",
    "logging_config": {
        "debug": True,
        "info": True,
        "warning": True,
        "error": True
    }
}

# Thema kleuren
THEMA_KLEUREN = {
    "light": {
        "bg": "#f5f5f5",
        "fg": "#2c2c2c",
        "accent": "#e8e8e8",
        "frame": "#fafafa",
        "knop": "#e8e8e8",
        "knop_fg": "#2c2c2c",
        "main_bg": "#f0f8f0",
        "panel_bg": "#f5faf5",
    },
    "dark": {
        "bg": "#2a2a2a",
        "fg": "#e0e0e0",
        "accent": "#404040",
        "frame": "#353535",
        "knop": "#505050",
        "knop_fg": "#e0e0e0",
        "main_bg": "#252525",
        "panel_bg": "#303030",
    },
    "blue": {
        "bg": "#e3f2fd",
        "fg": "#1565c0",
        "accent": "#bbdefb",
        "frame": "#e1f5fe",
        "knop": "#2196f3",
        "knop_fg": "#ffffff",
        "main_bg": "#ffffff",
        "panel_bg": "#f0f8ff",
    },
    "green": {
        "bg": "#e8f5e8",
        "fg": "#2e7d32",
        "accent": "#c8e6c9",
        "frame": "#e8f5e8",
        "knop": "#4caf50",
        "knop_fg": "#ffffff",
        "main_bg": "#ffffff",
        "panel_bg": "#f1f8e9",
    },
}

class ConfigManager:
    """Beheert de configuratie van de applicatie"""
    
    def __init__(self):
        self.config_path = os.path.join(self.get_user_data_dir(), "config.json")
        self.config = self.load_configuration()
        self.env_vars = self.load_env_variables()
        
    def get_user_data_dir(self) -> str:
        """Krijg de gebruiker data directory"""
        app_name = "MagicTimeStudio"
        if os.name == 'nt':  # Windows
            app_data = os.getenv('APPDATA')
            if app_data:
                return os.path.join(app_data, app_name)
            else:
                return os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', app_name)
        else:  # Linux/Mac
            return os.path.join(os.path.expanduser('~'), '.config', app_name)
    
    def load_configuration(self) -> Dict[str, Any]:
        """Laad configuratie uit bestand en .env"""
        try:
            # Start met standaard configuratie
            config = DEFAULT_CONFIG.copy()
            
            # Laad .env variabelen
            env_config = self._load_config_from_env()
            config.update(env_config)
            
            # Laad JSON configuratie (overschrijft .env)
            if os.path.exists(self.config_path):
                with open(self.config_path, "r", encoding="utf-8") as f:
                    json_config = json.load(f)
                config.update(json_config)
            
            return config
        except Exception as e:
            print(f"❌ Fout bij laden configuratie: {e}")
            return DEFAULT_CONFIG.copy()
    
    def _load_config_from_env(self) -> Dict[str, Any]:
        """Laad configuratie uit environment variables"""
        config = {}
        
        # Whisper configuratie
        config["default_whisper_model"] = self.get_env("DEFAULT_WHISPER_MODEL", "base")
        config["whisper_device"] = self.get_env("WHISPER_DEVICE", "cpu")
        
        # Applicatie configuratie
        config["theme"] = self.get_env("DEFAULT_THEME", "dark")
        config["font_size"] = int(self.get_env("DEFAULT_FONT_SIZE", "9"))
        config["worker_count"] = int(self.get_env("DEFAULT_WORKER_COUNT", "4"))
        config["subtitle_type"] = self.get_env("DEFAULT_SUBTITLE_TYPE", "softcoded")
        config["hardcoded_language"] = self.get_env("DEFAULT_HARDCODED_LANGUAGE", "dutch_only")
        
        # Logging configuratie
        log_level = self.get_env("LOG_LEVEL", "INFO").upper()
        config["logging_config"] = {
            "debug": log_level in ["DEBUG"],
            "info": log_level in ["DEBUG", "INFO"],
            "warning": log_level in ["DEBUG", "INFO", "WARNING"],
            "error": log_level in ["DEBUG", "INFO", "WARNING", "ERROR"]
        }
        
        # Performance configuratie
        config["cpu_limit_percentage"] = int(self.get_env("CPU_LIMIT_PERCENTAGE", "80"))
        config["memory_limit_mb"] = int(self.get_env("MEMORY_LIMIT_MB", "2048"))
        
        # Output configuratie
        config["auto_create_output_dir"] = self.get_env("AUTO_CREATE_OUTPUT_DIR", "true").lower() == "true"
        
        # Security configuratie
        config["auto_cleanup_temp"] = self.get_env("AUTO_CLEANUP_TEMP", "true").lower() == "true"
        
        return config
    
    def load_env_variables(self) -> Dict[str, str]:
        """Laad environment variables uit .env bestanden"""
        env_vars = {}
        
        # Zoek naar .env bestanden in verschillende locaties
        env_paths = [
            Path(__file__).parent.parent / ".env",  # magic_time_studio/.env
            Path.cwd() / ".env",  # Huidige directory
            Path.home() / ".env",  # Home directory
        ]
        
        for env_path in env_paths:
            if env_path.exists():
                try:
                    with open(env_path, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            # Skip comments en lege regels
                            if line and not line.startswith("#"):
                                if "=" in line:
                                    key, value = line.split("=", 1)
                                    key = key.strip()
                                    value = value.strip().strip('"').strip("'")
                                    env_vars[key] = value
                    logging.debug(f"✅ Environment variables geladen van: {env_path}")
                except Exception as e:
                    logging.warning(f"⚠️ Kon .env bestand niet laden: {env_path} - {e}")
        
        return env_vars
    
    def save_configuration(self) -> bool:
        """Sla configuratie op naar bestand"""
        try:
            # Zorg ervoor dat de directory bestaat
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"❌ Fout bij opslaan configuratie: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Krijg een configuratie waarde"""
        return self.config.get(key, default)
    
    def get_env(self, key: str, default: str = "") -> str:
        """Krijg een environment variable"""
        return self.env_vars.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Zet een configuratie waarde"""
        self.config[key] = value
    
    def get_theme_colors(self, theme_name: str) -> Dict[str, str]:
        """Krijg kleuren voor een thema"""
        return THEMA_KLEUREN.get(theme_name, THEMA_KLEUREN["dark"])
    
    def get_available_themes(self) -> list:
        """Krijg lijst van beschikbare thema's"""
        return list(THEMA_KLEUREN.keys())

# Globale configuratie instantie
config_manager = ConfigManager()

# Helper functies voor backward compatibility
def load_configuration():
    """Backward compatibility functie"""
    return config_manager.load_configuration()

def sla_config_op():
    """Backward compatibility functie"""
    return config_manager.save_configuration()

def laad_thema_uit_config():
    """Laad thema uit configuratie"""
    return config_manager.get("theme", "dark")

def sla_thema_op(gekozen_thema: str):
    """Sla thema op in configuratie"""
    config_manager.set("theme", gekozen_thema)
    config_manager.save_configuration() 