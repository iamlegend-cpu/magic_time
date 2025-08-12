"""
Runtime hook voor Magic Time Studio
Zorgt ervoor dat alle modules correct worden geladen tijdens runtime
"""

import os
import sys
import importlib

def _setup_magic_time_studio_paths():
    """Setup de juiste paths voor Magic Time Studio modules"""
    
    # Voeg de huidige directory toe aan Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(current_dir)
    
    # Voeg alle benodigde paths toe
    paths_to_add = [
        base_dir,
        os.path.join(base_dir, 'magic_time_studio'),
        os.path.join(base_dir, 'magic_time_studio', 'core'),
        os.path.join(base_dir, 'magic_time_studio', 'app_core'),
        os.path.join(base_dir, 'magic_time_studio', 'processing'),
        os.path.join(base_dir, 'magic_time_studio', 'ui_pyqt6'),
        os.path.join(base_dir, 'magic_time_studio', 'ui_pyqt6', 'components'),
    ]
    
    for path in paths_to_add:
        if path not in sys.path and os.path.exists(path):
            sys.path.insert(0, path)
            print(f"🔧 Runtime hook: Path toegevoegd: {path}")

def _preload_critical_modules():
    """Preload kritieke modules om import problemen te voorkomen"""
    
    critical_modules = [
        'magic_time_studio.core.config',
        'magic_time_studio.core.logging',
        'magic_time_studio.processing.whisper_manager',
        'magic_time_studio.processing.translator',
        'magic_time_studio.app_core.processing_modules.whisper_processing',
        'magic_time_studio.app_core.processing_modules.translation_processing',
        'magic_time_studio.app_core.processing_modules.video_processing',
        'magic_time_studio.app_core.processing_modules.audio_processing',
    ]
    
    for module_name in critical_modules:
        try:
            importlib.import_module(module_name)
            print(f"✅ Runtime hook: Module geladen: {module_name}")
        except ImportError as e:
            print(f"⚠️ Runtime hook: Module laden gefaald: {module_name} - {e}")

def _setup_environment():
    """Setup environment variabelen en configuratie"""
    
    # Zorg ervoor dat de whisper_config.env wordt geladen
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(current_dir)
    env_file = os.path.join(base_dir, 'magic_time_studio', 'whisper_config.env')
    
    if os.path.exists(env_file):
        print(f"🔧 Runtime hook: Environment file gevonden: {env_file}")
        
        # Laad environment variabelen
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
                        print(f"🔧 Runtime hook: Environment variabele ingesteld: {key.strip()}")
        except Exception as e:
            print(f"⚠️ Runtime hook: Fout bij laden environment: {e}")
    else:
        print(f"⚠️ Runtime hook: Environment file niet gevonden: {env_file}")

# Voer alle setup functies uit
print("🚀 Magic Time Studio Runtime Hook wordt uitgevoerd...")

_setup_magic_time_studio_paths()
_setup_environment()
_preload_critical_modules()

print("✅ Magic Time Studio Runtime Hook voltooid!")
