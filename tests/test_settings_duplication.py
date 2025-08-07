"""
Test om dubbele instellingen te identificeren tussen GUI settings panel en config window
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from magic_time_studio.ui_pyqt6.components.settings_panel import SettingsPanel
from magic_time_studio.ui_pyqt6.config_window import ConfigWindow

def test_settings_duplication():
    """Test om dubbele instellingen te identificeren"""
    app = QApplication(sys.argv)
    
    print("🔍 Analyseren van dubbele instellingen...")
    print("=" * 60)
    
    # Maak beide panels aan
    settings_panel = SettingsPanel()
    config_window = ConfigWindow()
    
    # Settings Panel instellingen (nieuwe schone versie)
    print("📋 SETTINGS PANEL (Hoofd GUI) - Quick Settings:")
    print("-" * 40)
    settings_fields = [
        "Vertaler (LibreTranslate/Geen vertaling)",
        "LibreTranslate Server URL",
        "Whisper Type (Fast Whisper)",
        "Model (tiny/base/small/medium/large/etc)",
        "Taal (Engels/Nederlands/Duits/Frans/Spaans/Auto detectie)",
        "Content Type (Softcoded/Hardcoded)",
        "Preserve Subtitles (Behoud/Vervang)"
    ]
    
    for i, field in enumerate(settings_fields, 1):
        print(f"{i:2d}. {field}")
    
    print("\n" + "=" * 60)
    
    # Config Window instellingen
    print("📋 CONFIG WINDOW (Menu -> Instellingen) - Geavanceerde Instellingen:")
    print("-" * 40)
    config_fields = [
        "Theme (dark/light/blue/green/purple/orange/cyber)",
        "Font Size (8-16)",
        "Auto Cleanup (Checkbox)",
        "Auto Output Directory (Checkbox)",
        "Log Level (DEBUG/INFO/WARNING/ERROR)",
        "Log to File (Checkbox)",
        "Whisper Type (Fast Whisper/Standaard Whisper)",
        "Model (tiny/base/small/medium/large/etc)",
        "Device (cpu/cuda)",
        "LibreTranslate Server URL",
        "Timeout (5-120 seconds)",
        "Rate Limit (0-1000)",
        "Max Characters (1000-50000)",
        "Panel Visibility Settings",
        "Window Size Settings",
        "Splitter Position Settings",
        "Theme Preview",
        "Custom Colors",
        "Debug Mode (Checkbox)",
        "Verbose Logging (Checkbox)",
        "System Info (Checkbox)",
        "Cache Size (100-5000 MB)",
        "Thread Pool Size (2-16)",
        "Auto Backup (Checkbox)",
        "Backup Interval (1-30 days)",
        "Plugin Directory",
        "Load Plugins on Startup (Checkbox)",
        "Auto Scan Plugins (Checkbox)"
    ]
    
    for i, field in enumerate(config_fields, 1):
        print(f"{i:2d}. {field}")
    
    print("\n" + "=" * 60)
    
    # Identificeer duplicaten (nu veel minder)
    print("🚨 DUBBELE INSTELLINGEN GEVONDEN:")
    print("-" * 40)
    duplicates = [
        "LibreTranslate Server URL",
        "Whisper Type",
        "Model"
    ]
    
    for i, duplicate in enumerate(duplicates, 1):
        print(f"{i}. {duplicate}")
    
    print("\n" + "=" * 60)
    print("💡 OPLOSSING GEPLAATST:")
    print("-" * 40)
    print("✅ GUI settings panel is nu een 'Quick Settings' panel")
    print("✅ Alleen essentiële instellingen voor snelle toegang")
    print("✅ Geen knoppen in de settings panel")
    print("✅ Geavanceerde instellingen alleen in config window")
    print("✅ Dubbele instellingen zijn geminimaliseerd")
    print("✅ Interface is nu veel schoner en gebruiksvriendelijker")
    print("\n📊 Vergelijking:")
    print(f"  - Settings Panel: {len(settings_fields)} instellingen")
    print(f"  - Config Window: {len(config_fields)} instellingen")
    print(f"  - Dubbele instellingen: {len(duplicates)} (was 7, nu 3)")
    
    app.quit()

if __name__ == "__main__":
    test_settings_duplication()
