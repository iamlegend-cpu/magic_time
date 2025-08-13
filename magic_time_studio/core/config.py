"""
Configuratie management voor Magic Time Studio
"""

import os
import sys
from pathlib import Path
import datetime

# Normale imports
try:
    # Gebruik absolute imports om import fouten te voorkomen
    import magic_time_studio.core.logging as logging_module
    import magic_time_studio.core.utils as utils_module
    
    # Setup logging
    logging_module.setup_logging()
    
    # Laad environment variabelen
    project_root = utils_module.get_project_root()
    env_file = os.path.join(project_root, 'whisper_config.env')
    utils_module.load_env_file(env_file)
    
    class ConfigManager:
        """Centrale configuratie manager"""
        
        def __init__(self):
            self.config = {}
            self.env_vars = {}
            self.panel_visibility = {
                'settings_panel': True,
                'files_panel': True,
                'processing_panel': True,
                'batch_panel': True,
                'charts_panel': True,
                'completed_files_panel': True
            }
            self._load_config()
            self._load_panel_config()
        
        def _load_config(self):
            """Laad configuratie uit verschillende bronnen"""
            # Laad environment variabelen
            self.env_vars = dict(os.environ)
            
            # Laad configuratie uit bestand als dat bestaat
            config_file = self._get_config_file_path()
            if config_file and os.path.exists(config_file):
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#'):
                                if '=' in line:
                                    key, value = line.split('=', 1)
                                    key = key.strip()
                                    value = value.strip().strip('"').strip("'")
                                    self.config[key] = value
                except Exception as e:
                    print(f"⚠️ Fout bij laden config bestand: {e}")
        
        def _get_config_file_path(self):
            """Krijg het pad naar het configuratie bestand"""
            if hasattr(sys, '_MEIPASS'):
                # PyInstaller bundle
                bundle_dir = sys._MEIPASS
                return os.path.join(bundle_dir, 'whisper_config.env')
            else:
                # Normale Python omgeving
                project_root = utils_module.get_project_root()
                return os.path.join(project_root, 'whisper_config.env')
        
        def _get_panel_config_path(self):
            """Krijg het pad naar het panel configuratie bestand"""
            if hasattr(sys, '_MEIPASS'):
                # PyInstaller bundle
                bundle_dir = sys._MEIPASS
                return os.path.join(bundle_dir, 'panel_config.json')
            else:
                # Normale Python omgeving
                project_root = utils_module.get_project_root()
                return os.path.join(project_root, 'panel_config.json')
        
        def _load_panel_config(self):
            """Laad panel configuratie uit JSON bestand"""
            import json
            panel_config_file = self._get_panel_config_path()
            if panel_config_file and os.path.exists(panel_config_file):
                try:
                    with open(panel_config_file, 'r', encoding='utf-8') as f:
                        panel_data = json.load(f)
                        if 'panel_visibility' in panel_data:
                            self.panel_visibility.update(panel_data['panel_visibility'])
                        print(f"✅ Panel configuratie geladen uit: {panel_config_file}")
                except Exception as e:
                    print(f"⚠️ Fout bij laden panel configuratie: {e}")
        
        def _save_panel_config(self):
            """Sla panel configuratie op naar JSON bestand"""
            import json
            panel_config_file = self._get_panel_config_path()
            if panel_config_file:
                try:
                    os.makedirs(os.path.dirname(panel_config_file), exist_ok=True)
                    panel_data = {
                        'panel_visibility': self.panel_visibility,
                        'last_updated': str(datetime.datetime.now())
                    }
                    with open(panel_config_file, 'w', encoding='utf-8') as f:
                        json.dump(panel_data, f, indent=2, ensure_ascii=False)
                    print(f"✅ Panel configuratie opgeslagen naar: {panel_config_file}")
                except Exception as e:
                    print(f"⚠️ Fout bij opslaan panel configuratie: {e}")
        
        def get(self, key: str, default=None):
            """Krijg een configuratie waarde"""
            return self.config.get(key, self.env_vars.get(key, default))
        
        def get_env(self, key: str, default=""):
            """Krijg een environment variabele"""
            return self.env_vars.get(key, default)
        
        def set(self, key: str, value):
            """Zet een configuratie waarde"""
            self.config[key] = value
        
        def set_env(self, key: str, value):
            """Zet een environment variabele"""
            self.env_vars[key] = value
            os.environ[key] = value
        
        def get_all(self):
            """Krijg alle configuratie"""
            return {**self.env_vars, **self.config}
        
        def save_config(self):
            """Sla configuratie op naar bestand"""
            config_file = self._get_config_file_path()
            if config_file:
                try:
                    os.makedirs(os.path.dirname(config_file), exist_ok=True)
                    with open(config_file, 'w', encoding='utf-8') as f:
                        for key, value in self.config.items():
                            f.write(f"{key}={value}\n")
                    print(f"✅ Configuratie opgeslagen naar: {config_file}")
                except Exception as e:
                    print(f"⚠️ Fout bij opslaan configuratie: {e}")
        
        def get_project_root(self):
            """Krijg project root directory"""
            if hasattr(sys, '_MEIPASS'):
                return sys._MEIPASS
            else:
                # Normale Python omgeving
                return utils_module.get_project_root()
        
        def get_assets_path(self):
            """Krijg assets directory pad"""
            if hasattr(sys, '_MEIPASS'):
                # PyInstaller bundle
                return os.path.join(sys._MEIPASS, 'assets')
            else:
                # Normale Python omgeving
                project_root = utils_module.get_project_root()
                return os.path.join(project_root, 'assets')
        
        def get_whisper_config_path(self):
            """Krijg Whisper config bestand pad"""
            if hasattr(sys, '_MEIPASS'):
                # PyInstaller bundle
                return os.path.join(sys._MEIPASS, 'whisper_config.env')
            else:
                # Normale Python omgeving
                project_root = utils_module.get_project_root()
                return os.path.join(project_root, 'whisper_config.env')
        
        # Panel management methoden
        def get_visible_panels(self):
            """Krijg lijst van zichtbare panels"""
            return [name for name, visible in self.panel_visibility.items() if visible]
        
        def is_panel_visible(self, panel_name: str):
            """Controleer of een panel zichtbaar is"""
            return self.panel_visibility.get(panel_name, True)
        
        def get_panel_visibility(self, panel_name: str):
            """Krijg panel zichtbaarheid"""
            return self.panel_visibility.get(panel_name, True)
        
        def set_panel_visibility(self, panel_name: str, visible: bool):
            """Stel panel zichtbaarheid in"""
            self.panel_visibility[panel_name] = visible
            self._save_panel_config()  # Sla direct op
        
        def get_all_panels(self):
            """Krijg alle beschikbare panels"""
            return list(self.panel_visibility.keys())
        
        # Thema en taal methoden
        def get_theme(self):
            """Krijg huidige thema"""
            return self.config.get('theme', 'dark')
        
        def set_theme(self, theme: str):
            """Stel thema in"""
            self.config['theme'] = theme
        
        def get_language(self):
            """Krijg huidige taal"""
            return self.config.get('language', 'nl')
        
        def set_language(self, language: str):
            """Stel taal in"""
            self.config['language'] = language
        
        def load_configuration(self):
            """Laad configuratie"""
            self._load_config()
            self._load_panel_config()
        
        def save_configuration(self):
            """Sla configuratie op"""
            self.save_config()
            self._save_panel_config()
    
    config_manager = ConfigManager()
    
except ImportError as e:
    print(f"⚠️ Config import gefaald: {e}")
    # Fallback naar dummy config manager
    class DummyConfigManager:
        def __init__(self):
            self.config = {}
            self.env_vars = {}
            self.panel_visibility = {
                'settings_panel': True,
                'files_panel': True,
                'processing_panel': True,
                'batch_panel': True,
                'charts_panel': True,
                'completed_files_panel': True
            }
            self._load_panel_config()
        
        def _get_panel_config_path(self):
            """Krijg het pad naar het panel configuratie bestand"""
            if hasattr(sys, '_MEIPASS'):
                return sys._MEIPASS
            else:
                return os.path.join(os.getcwd(), 'panel_config.json')
        
        def _load_panel_config(self):
            """Laad panel configuratie uit JSON bestand (dummy implementatie)"""
            import json
            panel_config_file = self._get_panel_config_path()
            if panel_config_file and os.path.exists(panel_config_file):
                try:
                    with open(panel_config_file, 'r', encoding='utf-8') as f:
                        panel_data = json.load(f)
                        if 'panel_visibility' in panel_data:
                            self.panel_visibility.update(panel_data['panel_visibility'])
                        print(f"✅ Panel configuratie geladen uit: {panel_config_file}")
                except Exception as e:
                    print(f"⚠️ Fout bij laden panel configuratie: {e}")
        
        def _save_panel_config(self):
            """Sla panel configuratie op naar JSON bestand (dummy implementatie)"""
            import json
            import datetime
            panel_config_file = self._get_panel_config_path()
            if panel_config_file:
                try:
                    os.makedirs(os.path.dirname(panel_config_file), exist_ok=True)
                    panel_data = {
                        'panel_visibility': self.panel_visibility,
                        'last_updated': str(datetime.datetime.now())
                    }
                    with open(panel_config_file, 'w', encoding='utf-8') as f:
                        json.dump(panel_data, f, indent=2, ensure_ascii=False)
                    print(f"✅ Panel configuratie opgeslagen naar: {panel_config_file}")
                except Exception as e:
                    print(f"⚠️ Fout bij opslaan panel configuratie: {e}")
        
        def get(self, key: str, default=None):
            return default
        
        def get_env(self, key: str, default=""):
            return os.environ.get(key, default)
        
        def set(self, key: str, value):
            pass
        
        def set_env(self, key: str, value):
            os.environ[key] = value
        
        def get_all(self):
            return {}
        
        def save_config(self):
            pass
        
        def get_project_root(self):
            if hasattr(sys, '_MEIPASS'):
                return sys._MEIPASS
            else:
                return os.getcwd()
        
        def get_assets_path(self):
            if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, 'assets')
            else:
                return os.path.join(os.getcwd(), 'assets')
        
        def get_whisper_config_path(self):
            if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, 'whisper_config.env')
            else:
                return os.path.join(os.getcwd(), 'whisper_config.env')
        
        # Voeg ontbrekende methoden toe
        def load_configuration(self):
            """Laad configuratie (dummy implementatie)"""
            self._load_panel_config()
        
        def save_configuration(self):
            """Sla configuratie op (dummy implementatie)"""
            self._save_panel_config()
        
        def get_visible_panels(self):
            """Krijg lijst van zichtbare panels (dummy implementatie)"""
            return [name for name, visible in self.panel_visibility.items() if visible]
        
        def is_panel_visible(self, panel_name: str):
            """Controleer of een panel zichtbaar is (dummy implementatie)"""
            return self.panel_visibility.get(panel_name, True)
        
        def get_panel_visibility(self, panel_name: str):
            """Krijg panel zichtbaarheid (dummy implementatie)"""
            return self.panel_visibility.get(panel_name, True)
        
        def set_panel_visibility(self, panel_name: str, visible: bool):
            """Stel panel zichtbaarheid in (dummy implementatie)"""
            self.panel_visibility[panel_name] = visible
            self._save_panel_config()  # Sla direct op
        
        def get_all_panels(self):
            """Krijg alle beschikbare panels (dummy implementatie)"""
            return list(self.panel_visibility.keys())
        
        def get_theme(self):
            """Krijg huidige thema (dummy implementatie)"""
            return "dark"  # Standaard donker thema
        
        def set_theme(self, theme: str):
            """Stel thema in (dummy implementatie)"""
            pass
        
        def get_language(self):
            """Krijg huidige taal (dummy implementatie)"""
            return "nl"  # Standaard Nederlands
        
        def set_language(self, language: str):
            """Stel taal in (dummy implementatie)"""
            pass 