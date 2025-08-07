#!/usr/bin/env python3
"""
Test voor Server Consistency - Magic Time Studio
Test of het LibreTranslate server IP consistent is tussen GUI en config
"""

import sys
import os

# Voeg project root toe aan Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_server_consistency():
    """Test of server IP consistent is tussen GUI en config"""
    try:
        from PyQt6.QtWidgets import QApplication
        from magic_time_studio.ui_pyqt6.components.settings_panel import SettingsPanel
        from magic_time_studio.core.config import config_manager
        
        # Maak QApplication aan
        app = QApplication(sys.argv)
        
        # Maak SettingsPanel aan
        settings_panel = SettingsPanel()
        print("✅ SettingsPanel aangemaakt")
        
        # Test server IP consistentie
        print("\n🔍 Test server IP consistentie:")
        
        # Haal server IP op uit config
        config_server = config_manager.get_env("LIBRETRANSLATE_SERVER", "NIET GEVONDEN")
        print(f"  - Config server IP: {config_server}")
        
        # Haal server IP op uit GUI
        gui_server = settings_panel.translate_server_edit.text()
        print(f"  - GUI server IP: {gui_server}")
        
        # Controleer of ze hetzelfde zijn (accepteer lege waarden als consistent)
        if config_server == gui_server or (config_server == "NIET GEVONDEN" and gui_server == ""):
            print("✅ Server IP is consistent tussen GUI en config")
            return True
        else:
            print("❌ Server IP is NIET consistent tussen GUI en config")
            print(f"  - Verschil: Config='{config_server}' vs GUI='{gui_server}'")
            return False
        
    except Exception as e:
        print(f"❌ Fout bij testen server consistentie: {e}")
        return False

def test_server_sync():
    """Test of server IP correct wordt gesynchroniseerd"""
    try:
        from PyQt6.QtWidgets import QApplication
        from magic_time_studio.ui_pyqt6.components.settings_panel import SettingsPanel
        from magic_time_studio.core.config import config_manager
        
        # Maak QApplication aan
        app = QApplication(sys.argv)
        
        # Maak SettingsPanel aan
        settings_panel = SettingsPanel()
        print("✅ SettingsPanel aangemaakt")
        
        # Test server IP synchronisatie
        print("\n🔄 Test server IP synchronisatie:")
        
        # Stel een nieuwe server IP in via GUI
        new_server = "localhost:5000"
        settings_panel.translate_server_edit.setText(new_server)
        print(f"  - Nieuwe server IP ingesteld in GUI: {new_server}")
        
        # Trigger de change event
        settings_panel.on_translate_server_changed()
        print("  - Change event getriggerd")
        
        # Controleer of config is bijgewerkt
        config_server = config_manager.get_env("LIBRETRANSLATE_SERVER", "NIET GEVONDEN")
        print(f"  - Config server IP na wijziging: {config_server}")
        
        if config_server == new_server:
            print("✅ Server IP correct gesynchroniseerd")
            return True
        else:
            print("❌ Server IP niet correct gesynchroniseerd")
            return False
        
    except Exception as e:
        print(f"❌ Fout bij testen server synchronisatie: {e}")
        return False

def test_load_current_settings():
    """Test of load_current_settings correct werkt"""
    try:
        from PyQt6.QtWidgets import QApplication
        from magic_time_studio.ui_pyqt6.components.settings_panel import SettingsPanel
        from magic_time_studio.core.config import config_manager
        
        # Maak QApplication aan
        app = QApplication(sys.argv)
        
        # Maak SettingsPanel aan
        settings_panel = SettingsPanel()
        print("✅ SettingsPanel aangemaakt")
        
        # Test load_current_settings
        print("\n📥 Test load_current_settings:")
        
        # Stel een test server IP in via config
        test_server = "localhost:5000"
        config_manager.set_env("LIBRETRANSLATE_SERVER", test_server)
        print(f"  - Test server IP ingesteld in config: {test_server}")
        
        # Herlaad instellingen
        settings_panel.load_current_settings()
        print("  - Instellingen herladen")
        
        # Controleer of GUI is bijgewerkt
        gui_server = settings_panel.translate_server_edit.text()
        print(f"  - GUI server IP na herladen: {gui_server}")
        
        if gui_server == test_server:
            print("✅ GUI correct bijgewerkt vanuit config")
            return True
        else:
            print("❌ GUI niet correct bijgewerkt vanuit config")
            return False
        
    except Exception as e:
        print(f"❌ Fout bij testen load_current_settings: {e}")
        return False

def main():
    """Voer alle tests uit"""
    print("🧪 Test Server Consistency...")
    print("=" * 50)
    
    tests = [
        ("Server Consistency Test", test_server_consistency),
        ("Server Sync Test", test_server_sync),
        ("Load Settings Test", test_load_current_settings)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}...")
        if test_func():
            print(f"✅ {test_name} geslaagd")
            passed += 1
        else:
            print(f"❌ {test_name} gefaald")
    
    print("\n" + "=" * 50)
    print(f"📊 Resultaat: {passed}/{total} tests geslaagd")
    
    if passed == total:
        print("🎉 Alle tests geslaagd! Server IP is consistent.")
        return True
    else:
        print("⚠️ Sommige tests gefaald. Er is een inconsistentie in server IP.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
