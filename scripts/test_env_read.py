from magic_time_studio.core.config import ConfigManager

print("[TEST] Start .env test")
cm = ConfigManager()
print(f"[TEST] Gevonden env_vars: {cm.env_vars}")
print(f"[TEST] config['default_whisper_model']: {cm.get('default_whisper_model', 'large')}")
print(f"[TEST] config dict: {cm.config}") 