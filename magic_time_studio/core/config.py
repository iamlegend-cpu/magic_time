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
    "default_translator": "libretranslate",
    "libretranslate_server": "http://100.90.127.78:5000",
    "target_language": "nl",
    "subtitle_type": "softcoded",  # Altijd softcoded, hardcoded wordt niet meer ondersteund (alleen SRT bestanden)
    "hardcoded_language": "dutch_only",
    "font_size": 9,
    "worker_count": 4,
    "theme": "dark",
    "debug_mode": False,  # Zet debug mode uit standaard (alleen aan in debug mode)
    "preserve_subtitles": False,  # Maak alleen SRT bestanden, voeg geen ondertiteling toe aan video (geen MP4 verwerking of generatie, origineel blijft ongewijzigd)
    "logging_config": {
        "debug": False,  # Zet debug logging uit standaard
        "info": True,
        "warning": True,
        "error": True
    },
    "visible_panels": {
        "settings": True,
        "files": True,
        "processing": True,
        "charts": True,
        "batch": True,
        "plugins": True,
        "completed": True
    }
}

# Voeg timeout instellingen toe
DEFAULT_TIMEOUTS = {
    "whisper_transcription": 3600,  # 1 uur
    "audio_extraction": 300,        # 5 minuten
    "video_processing": 1800,       # 30 minuten
    "translation": 600              # 10 minuten
}

# Thema kleuren
THEMA_KLEUREN = {
    "light": {
        "bg": "#2a2a2a",
        "fg": "#ffffff",
        "accent": "#404040",
        "frame": "#353535",
        "knop": "#505050",
        "knop_fg": "#ffffff",
        "main_bg": "#252525",
        "panel_bg": "#303030",
        "knop_start": "#4caf50",
        "knop_stop": "#d32f2f",
        "knop_delete_all": "#d32f2f",
        "knop_special_fg": "#ffffff"
    },
    "dark": {
        "bg": "#2a2a2a",
        "fg": "#ffffff",
        "accent": "#404040",
        "frame": "#353535",
        "knop": "#505050",
        "knop_fg": "#ffffff",
        "main_bg": "#252525",
        "panel_bg": "#303030",
        "knop_start": "#4caf50",
        "knop_stop": "#d32f2f",
        "knop_delete_all": "#d32f2f",
        "knop_special_fg": "#ffffff"
    },
    "blue": {
        "bg": "#1a237e",
        "fg": "#ffffff",
        "accent": "#3949ab",
        "frame": "#283593",
        "knop": "#3f51b5",
        "knop_fg": "#ffffff",
        "main_bg": "#0d47a1",
        "panel_bg": "#1565c0",
        "knop_start": "#4caf50",
        "knop_stop": "#d32f2f",
        "knop_delete_all": "#d32f2f",
        "knop_special_fg": "#ffffff"
    },
    "green": {
        "bg": "#1b5e20",
        "fg": "#ffffff",
        "accent": "#2e7d32",
        "frame": "#388e3c",
        "knop": "#4caf50",
        "knop_fg": "#ffffff",
        "main_bg": "#0d4f14",
        "panel_bg": "#1565c0",
        "knop_start": "#4caf50",
        "knop_stop": "#d32f2f",
        "knop_delete_all": "#d32f2f",
        "knop_special_fg": "#ffffff"
    },
}

class ConfigManager:
    """Beheert de configuratie van de applicatie"""
    
    def __init__(self):
        # Plaats config.json in de hoofdfolder van het programma
        self.config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
        
        # Zoek naar .env bestand
        env_paths = [
            Path(__file__).parent.parent / ".env",  # magic_time_studio/.env
            Path.cwd() / ".env",  # Huidige directory
            Path.home() / ".env",  # Home directory
        ]
        
        self.env_file_path = None
        for env_path in env_paths:
            if env_path.exists():
                self.env_file_path = env_path
                break
        
        self.env_vars = self.load_env_variables()
        self.config = self.load_configuration()
        
    def _is_debug_mode(self) -> bool:
        """Controleer of debug mode is ingeschakeld"""
        try:
            log_level = self.get_env("LOG_LEVEL", "INFO")
            return log_level.upper() == "DEBUG"
        except:
            return False
        
    def get_user_data_dir(self) -> str:
        """Krijg de gebruiker data directory (niet meer gebruikt voor config.json)"""
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
            
            # Laad .env variabelen via _load_config_from_env (zorgt voor juiste mapping)
            env_config = self._load_config_from_env()
            config.update(env_config)
            # Forceer juiste mapping voor Whisper type, model en device
            if "WHISPER_TYPE" in self.env_vars:
                config["whisper_type"] = self.env_vars["WHISPER_TYPE"]
            if "DEFAULT_WHISPER_MODEL" in self.env_vars:
                config["default_whisper_model"] = self.env_vars["DEFAULT_WHISPER_MODEL"]
            if "DEFAULT_FAST_WHISPER_MODEL" in self.env_vars:
                config["default_fast_whisper_model"] = self.env_vars["DEFAULT_FAST_WHISPER_MODEL"]
            if "WHISPER_DEVICE" in self.env_vars:
                config["whisper_device"] = self.env_vars["WHISPER_DEVICE"]
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
        config["whisper_type"] = self.get_env("WHISPER_TYPE", "fast")
        config["default_whisper_model"] = self.get_env("DEFAULT_WHISPER_MODEL", "large")
        config["default_fast_whisper_model"] = self.get_env("DEFAULT_FAST_WHISPER_MODEL", "large-v3-turbo")
        config["whisper_device"] = self.get_env("WHISPER_DEVICE", "cuda")
        
        # Vertaling configuratie
        config["default_translator"] = self.get_env("DEFAULT_TRANSLATOR", "libretranslate")
        config["libretranslate_server"] = self.get_env("LIBRETRANSLATE_SERVER", "http://100.90.127.78:5000")
        config["target_language"] = self.get_env("DEFAULT_TARGET_LANGUAGE", "nl")
        
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
        config["memory_limit_mb"] = int(self.get_env("MEMORY_LIMIT_MB", "8192"))
        
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
            Path(__file__).parent.parent / "whisper_config.env",  # magic_time_studio/whisper_config.env
            Path.cwd() / ".env",  # Huidige directory
            Path.cwd() / "whisper_config.env",  # Huidige directory whisper_config.env
            Path.home() / ".env",  # Home directory
        ]
        # Debug output alleen in debug mode
        if self._is_debug_mode():
            print(f"[DEBUG] Zoek naar .env op: {env_paths}")
        
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
                    if self._is_debug_mode():
                        print(f"[DEBUG] Environment variables geladen van: {env_path}")
                except Exception as e:
                    if self._is_debug_mode():
                        print(f"[DEBUG] ⚠️ Kon .env bestand niet laden: {env_path} - {e}")
        
        if self._is_debug_mode():
            print(f"[DEBUG] Gevonden env_vars: {env_vars}")
        
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
        """Haal environment variable op"""
        return self.env_vars.get(key, default)
    
    def set_env(self, key: str, value: str) -> None:
        """Zet environment variable (wordt opgeslagen in .env bestand)"""
        self.env_vars[key] = value
        # Sla op in .env bestand
        self._save_env_to_file()
    
    def _save_env_to_file(self) -> None:
        """Sla environment variables op in .env bestand"""
        try:
            env_path = self.env_file_path
            if env_path and env_path.exists():
                # Lees bestaande .env bestand
                existing_vars = {}
                with open(env_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            existing_vars[key] = value
                
                # Update met nieuwe waarden
                existing_vars.update(self.env_vars)
                
                # Schrijf terug naar .env bestand
                with open(env_path, 'w', encoding='utf-8') as f:
                    for key, value in existing_vars.items():
                        f.write(f"{key}={value}\n")
                        
        except Exception as e:
            print(f"⚠️ Kon .env bestand niet opslaan: {e}")
            
        # Probeer ook op te slaan in whisper_config.env als dat bestaat
        try:
            whisper_env_path = Path(__file__).parent.parent / "whisper_config.env"
            if whisper_env_path.exists():
                # Lees bestaande whisper_config.env bestand
                existing_vars = {}
                with open(whisper_env_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            existing_vars[key] = value
                
                # Update met nieuwe waarden (alleen LibreTranslate gerelateerde)
                libretranslate_keys = ["LIBRETRANSLATE_SERVER", "DEFAULT_TRANSLATOR", "DEFAULT_TARGET_LANGUAGE"]
                for key in libretranslate_keys:
                    if key in self.env_vars:
                        existing_vars[key] = self.env_vars[key]
                
                # Schrijf terug naar whisper_config.env bestand
                with open(whisper_env_path, 'w', encoding='utf-8') as f:
                    for key, value in existing_vars.items():
                        f.write(f"{key}={value}\n")
                        
        except Exception as e:
            print(f"⚠️ Kon whisper_config.env bestand niet opslaan: {e}")
    
    def set(self, key: str, value: Any) -> None:
        """Zet een configuratie waarde"""
        self.config[key] = value
    
    def get_theme_colors(self, theme_name: str) -> Dict[str, str]:
        """Krijg kleuren voor een thema"""
        return THEMA_KLEUREN.get(theme_name, THEMA_KLEUREN["dark"])
    
    def get_available_themes(self) -> list:
        """Krijg lijst van beschikbare thema's"""
        return list(THEMA_KLEUREN.keys())
    
    def is_debug_mode(self) -> bool:
        """Controleer of debug mode aan staat"""
        return self.get("debug_mode", False)
    
    def is_panel_visible(self, panel_name: str) -> bool:
        """Controleer of een panel zichtbaar is"""
        visible_panels = self.get("visible_panels", {})
        return visible_panels.get(panel_name, True)
    
    def set_panel_visibility(self, panel_name: str, visible: bool) -> None:
        """Stel panel zichtbaarheid in"""
        visible_panels = self.get("visible_panels", {})
        visible_panels[panel_name] = visible
        self.set("visible_panels", visible_panels)
    
    def get_visible_panels(self) -> Dict[str, bool]:
        """Krijg alle panel zichtbaarheid instellingen"""
        return self.get("visible_panels", {})

    def is_memory_within_limit(self) -> bool:
        """Controleer of het geheugengebruik binnen de limiet blijft"""
        try:
            import psutil
            limit_mb = self.config.get("memory_limit_mb", 8192)
            process = psutil.Process()
            mem_mb = process.memory_info().rss / 1024 / 1024
            return mem_mb < limit_mb
        except ImportError:
            return True  # Kan niet controleren zonder psutil
        except Exception:
            return True

    def get_timeout(self, timeout_type: str, default: int = None) -> int:
        """Krijg timeout instelling voor specifiek type"""
        if default is None:
            default = DEFAULT_TIMEOUTS.get(timeout_type, 3600)  # Standaard 1 uur
        
        # Probeer eerst uit environment variables
        env_key = f"{timeout_type.upper()}_TIMEOUT"
        env_value = self.get_env(env_key)
        if env_value:
            try:
                return int(env_value)
            except ValueError:
                pass
        
        # Fallback naar config bestand
        config_value = self.get(f"{timeout_type}_timeout")
        if config_value:
            try:
                return int(config_value)
            except ValueError:
                pass
        
        # Fallback naar default
        return default

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

if __name__ == "__main__":
    print("[TEST] Start .env test")
    cm = ConfigManager()
    print(f"[TEST] Gevonden env_vars: {cm.env_vars}")
    print(f"[TEST] config['default_whisper_model']: {cm.get('default_whisper_model', 'large')}") 