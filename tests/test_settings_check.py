#!/usr/bin/env python3
"""
Test om de settings te controleren
"""

import sys
import os
from pathlib import Path

# Voeg project root toe aan Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_settings():
    """Test of de settings correct zijn"""
    print("🔍 [DEBUG] Settings Test")
    print("=" * 50)
    
    try:
        from magic_time_studio.ui_pyqt6.components.settings_panel import SettingsPanel
        from PyQt6.QtWidgets import QApplication
        
        # Maak een QApplication instance
        app = QApplication([])
        
        # Maak settings panel
        settings_panel = SettingsPanel()
        
        # Laad huidige settings
        settings_panel.load_current_settings()
        
        # Haal settings op
        settings = settings_panel.get_current_settings()
        
        print(f"📊 Settings: {settings}")
        
        # Controleer belangrijke settings
        print(f"\n🔍 Belangrijke settings:")
        print(f"  whisper_type: {settings.get('whisper_type')}")
        print(f"  whisper_model: {settings.get('whisper_model')}")
        print(f"  enable_translation: {settings.get('enable_translation')}")
        print(f"  subtitle_type: {settings.get('subtitle_type')}")
        print(f"  preserve_original_subtitles: {settings.get('preserve_original_subtitles')}")
        
        # Controleer of subtitle_type correct is
        if settings.get('subtitle_type') == 'softcoded':
            print("  ✅ subtitle_type is correct (softcoded)")
        else:
            print(f"  ❌ subtitle_type is incorrect: {settings.get('subtitle_type')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Fout in settings test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 [DEBUG] Settings Check Test")
    print("=" * 50)
    
    success = test_settings()
    
    if success:
        print("\n🎉 Settings test geslaagd!")
    else:
        print("\n⚠️ Settings test gefaald.") 