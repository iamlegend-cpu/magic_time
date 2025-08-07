"""
Script om eenvoudig tussen Whisper types te wisselen
Gebruik: python scripts/switch_whisper_type.py [standard|fast]
"""

import sys
import os
from pathlib import Path

def switch_whisper_type(whisper_type: str):
    """Wissel naar specifiek Whisper type"""
    
    # Valideer input
    if whisper_type not in ["standard", "fast"]:
        print("❌ Ongeldig Whisper type. Gebruik 'standard' of 'fast'")
        return False
    
    # Zoek naar .env bestanden
    env_files = [
        Path(".env"),
        Path("magic_time_studio/.env"),
        Path("magic_time_studio/whisper_config.env")
    ]
    
    target_env_file = None
    
    # Zoek bestaand .env bestand
    for env_file in env_files:
        if env_file.exists():
            target_env_file = env_file
            break
    
    # Maak nieuw bestand als geen bestaand gevonden
    if target_env_file is None:
        target_env_file = Path("magic_time_studio/.env")
    
    # Lees bestaande configuratie
    existing_config = {}
    if target_env_file.exists():
        with open(target_env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    existing_config[key] = value
    
    # Update Whisper configuratie
    existing_config['WHISPER_TYPE'] = whisper_type
    
    # Voeg andere standaard instellingen toe als ze niet bestaan
    defaults = {
        'DEFAULT_WHISPER_MODEL': 'large',
        'WHISPER_DEVICE': 'cuda',
        'DEFAULT_FAST_WHISPER_MODEL': 'large-v3-turbo',
        'FAST_WHISPER_DEVICE': 'cuda',
        'DEFAULT_THEME': 'dark',
        'DEFAULT_FONT_SIZE': '9',
        'DEFAULT_WORKER_COUNT': '4',
        'DEFAULT_SUBTITLE_TYPE': 'softcoded',
        'DEFAULT_HARDCODED_LANGUAGE': 'dutch_only',
        'LOG_LEVEL': 'INFO',
        'LOG_TO_FILE': 'false',
        'AUTO_CREATE_OUTPUT_DIR': 'true',
        'CPU_LIMIT_PERCENTAGE': '80',
        'MEMORY_LIMIT_MB': '8192',
        'AUTO_CLEANUP_TEMP': 'true'
    }
    
    for key, value in defaults.items():
        if key not in existing_config:
            existing_config[key] = value
    
    # Schrijf nieuwe configuratie
    with open(target_env_file, 'w', encoding='utf-8') as f:
        f.write(f"# Whisper Type Configuratie\n")
        f.write(f"# Kies tussen 'standard' en 'fast'\n")
        f.write(f"WHISPER_TYPE={whisper_type}\n\n")
        
        f.write(f"# Standaard Whisper instellingen\n")
        f.write(f"DEFAULT_WHISPER_MODEL={existing_config.get('DEFAULT_WHISPER_MODEL', 'large')}\n")
        f.write(f"WHISPER_DEVICE={existing_config.get('WHISPER_DEVICE', 'cuda')}\n\n")
        
        f.write(f"# Fast Whisper instellingen\n")
        f.write(f"DEFAULT_FAST_WHISPER_MODEL={existing_config.get('DEFAULT_FAST_WHISPER_MODEL', 'large-v3-turbo')}\n")
        f.write(f"FAST_WHISPER_DEVICE={existing_config.get('FAST_WHISPER_DEVICE', 'cuda')}\n\n")
        
        f.write(f"# Andere instellingen\n")
        for key, value in existing_config.items():
            if key not in ['WHISPER_TYPE', 'DEFAULT_WHISPER_MODEL', 'WHISPER_DEVICE', 
                          'DEFAULT_FAST_WHISPER_MODEL', 'FAST_WHISPER_DEVICE']:
                f.write(f"{key}={value}\n")
    
    print(f"✅ Whisper type gewisseld naar: {whisper_type}")
    print(f"📁 Configuratie opgeslagen in: {target_env_file}")
    
    # Toon aanbevelingen
    if whisper_type == "fast":
        print("\n💡 Fast Whisper aanbevelingen:")
        print("  • Model: large-v3-turbo (snelste)")
        print("  • Device: cuda (voor GPU versnelling)")
        print("  • 6.8x sneller dan standaard Whisper")
    else:
        print("\n💡 Standaard Whisper aanbevelingen:")
        print("  • Model: large (beste kwaliteit)")
        print("  • Device: cuda (voor GPU versnelling)")
        print("  • Zeer stabiel en goed getest")
    
    return True

def show_current_config():
    """Toon huidige Whisper configuratie"""
    print("🔍 Huidige Whisper configuratie:")
    
    # Zoek naar .env bestanden
    env_files = [
        Path(".env"),
        Path("magic_time_studio/.env"),
        Path("magic_time_studio/whisper_config.env")
    ]
    
    config_found = False
    for env_file in env_files:
        if env_file.exists():
            print(f"\n📁 Configuratie bestand: {env_file}")
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        if 'WHISPER' in key:
                            print(f"  {key}={value}")
            config_found = True
            break
    
    if not config_found:
        print("❌ Geen configuratie bestand gevonden")
        print("💡 Maak een .env bestand aan of gebruik het switch script")

def main():
    """Hoofdfunctie"""
    if len(sys.argv) < 2:
        print("🤖 Whisper Type Switcher")
        print("=" * 30)
        print("Gebruik:")
        print("  python scripts/switch_whisper_type.py standard")
        print("  python scripts/switch_whisper_type.py fast")
        print("  python scripts/switch_whisper_type.py status")
        print("\n💡 Opties:")
        print("  • standard: Originele OpenAI Whisper")
        print("  • fast: Geoptimaliseerde Fast Whisper (6.8x sneller)")
        print("  • status: Toon huidige configuratie")
        return
    
    command = sys.argv[1].lower()
    
    if command == "status":
        show_current_config()
    elif command in ["standard", "fast"]:
        switch_whisper_type(command)
    else:
        print(f"❌ Onbekend commando: {command}")
        print("💡 Gebruik 'standard', 'fast', of 'status'")

if __name__ == "__main__":
    main() 