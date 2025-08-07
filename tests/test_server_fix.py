#!/usr/bin/env python3
"""
Test voor Server Fix - Magic Time Studio
Test of de server IP inconsistentie is opgelost
"""

import sys
import os

# Voeg project root toe aan Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_server_default_fix():
    """Test of de default waarde fix werkt"""
    try:
        from PyQt6.QtWidgets import QApplication
        from magic_time_studio.ui_pyqt6.components.settings_panel import SettingsPanel
        from magic_time_studio.core.config import config_manager
        
        # Maak QApplication aan
        app = QApplication(sys.argv)
        
        # Maak SettingsPanel aan
        settings_panel = SettingsPanel()
        print("✅ SettingsPanel aangemaakt")
        
        # Test server IP zonder config
        print("\n🔍 Test server IP zonder config:")
        
        # Verwijder eventuele bestaande server config
        config_manager.env_vars.pop("LIBRETRANSLATE_SERVER", None)
        
        # Herlaad instellingen
        settings_panel.load_current_settings()
        
        # Controleer of GUI leeg is (geen default waarde)
        gui_server = settings_panel.translate_server_edit.text()
        print(f"  - GUI server IP zonder config: '{gui_server}'")
        
        if gui_server == "":
            print("✅ GUI toont geen default waarde (correct)")
        else:
            print(f"❌ GUI toont nog steeds default waarde: '{gui_server}'")
            return False
        
        # Test met expliciete config
        print("\n🔧 Test met expliciete config:")
        test_server = "localhost:5000"
        config_manager.set_env("LIBRETRANSLATE_SERVER", test_server)
        
        # Herlaad instellingen
        settings_panel.load_current_settings()
        
        # Controleer of GUI de juiste waarde toont
        gui_server = settings_panel.translate_server_edit.text()
        print(f"  - GUI server IP met config: '{gui_server}'")
        
        if gui_server == test_server:
            print("✅ GUI toont correcte config waarde")
        else:
            print(f"❌ GUI toont verkeerde waarde: '{gui_server}' vs '{test_server}'")
            return False
        
        print("\n🎉 Server default fix werkt correct!")
        return True
        
    except Exception as e:
        print(f"❌ Fout bij testen server fix: {e}")
        return False

def test_placeholder_text():
    """Test of de placeholder tekst is aangepast"""
    try:
        from PyQt6.QtWidgets import QApplication
        from magic_time_studio.ui_pyqt6.components.settings_panel import SettingsPanel
        
        # Maak QApplication aan
        app = QApplication(sys.argv)
        
        # Maak SettingsPanel aan
        settings_panel = SettingsPanel()
        print("✅ SettingsPanel aangemaakt")
        
        # Test placeholder tekst
        print("\n📝 Test placeholder tekst:")
        placeholder = settings_panel.translate_server_edit.placeholderText()
        print(f"  - Placeholder tekst: '{placeholder}'")
        
        if "localhost:5000" in placeholder:
            print("✅ Placeholder tekst is aangepast")
        else:
            print("❌ Placeholder tekst is niet aangepast")
            return False
        
        print("\n🎉 Placeholder tekst fix werkt correct!")
        return True
        
    except Exception as e:
        print(f"❌ Fout bij testen placeholder tekst: {e}")
        return False

def main():
    """Voer alle tests uit"""
    print("🧪 Test Server Fix...")
    print("=" * 50)
    
    tests = [
        ("Server Default Fix Test", test_server_default_fix),
        ("Placeholder Text Test", test_placeholder_text)
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
        print("🎉 Alle tests geslaagd! Server IP inconsistentie is opgelost.")
        print("\n💡 Conclusie:")
        print("✅ Geen default waarde meer in GUI")
        print("✅ Placeholder tekst aangepast")
        print("✅ Gebruiker moet expliciet server IP invoeren")
        return True
    else:
        print("⚠️ Sommige tests gefaald. Server IP inconsistentie nog niet opgelost.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
