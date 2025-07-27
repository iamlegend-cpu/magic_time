"""
Configuratie management voor Magic Time Studio
"""

import os
import json
import logging
from typing import Dict, Any, Optional

# Standaard configuratie waarden
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
        """Laad configuratie uit bestand"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                # Merge met standaard waarden
                merged_config = DEFAULT_CONFIG.copy()
                merged_config.update(config)
                return merged_config
            else:
                return DEFAULT_CONFIG.copy()
        except Exception as e:
            print(f"❌ Fout bij laden configuratie: {e}")
            return DEFAULT_CONFIG.copy()
    
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