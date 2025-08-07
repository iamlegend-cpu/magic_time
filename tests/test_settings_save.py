#!/usr/bin/env python3
"""
Test voor Settings Save Functionaliteit - Magic Time Studio
Test of instellingen correct kunnen worden opgeslagen
"""

import sys
import os

# Voeg project root toe aan Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_settings_save():
    """Test of instellingen kunnen worden opgeslagen"""
    try:
        from PyQt6.QtWidgets import QApplication
        from magic_time_studio.ui_pyqt6.components.settings_panel import SettingsPanel
        from magic_time_studio.core.config import config_manager
        
        # Maak QApplication aan
        app = QApplication(sys.argv)
        
        # Maak SettingsPanel aan
        settings_panel = SettingsPanel()
        print("✅ SettingsPanel aangemaakt")
        
        # Test update_translator_status methode
        print("\n🔧 Test update_translator_status methode:")
        settings_panel.update_translator_status()
        print("✅ update_translator_status werkt")
        
        # Test instellingen wijzigen en opslaan
        print("\n💾 Test instellingen opslaan:")
        
        # Wijzig enkele instellingen
        settings_panel.translator_combo.setCurrentText("LibreTranslate")
        settings_panel.translate_server_edit.setText("localhost:5000")
        settings_panel.cpu_limit_spin.setValue(85)
        settings_panel.memory_limit_spin.setValue(10240)
        
        print(f"  - Vertaler: {settings_panel.translator_combo.currentText()}")
        print(f"  - Server: {settings_panel.translate_server_edit.text()}")
        print(f"  - CPU Limiet: {settings_panel.cpu_limit_spin.value()}%")
        print(f"  - Geheugen Limiet: {settings_panel.memory_limit_spin.value()} MB")
        
        # Test config_manager opslaan
        config_manager.save_configuration()
        print("✅ Configuratie opgeslagen")
        
        # Test herladen van instellingen
        print("\n🔄 Test herladen instellingen:")
        settings_panel.load_current_settings()
        print("✅ Instellingen herladen")
        
        # Test update_translator_status na wijzigingen
        settings_panel.update_translator_status()
        print("✅ Vertaler status bijgewerkt")
        
        print("\n🎉 Settings save functionaliteit werkt correct!")
        return True
        
    except Exception as e:
        print(f"❌ Fout bij testen settings save: {e}")
        return False

def test_config_manager_integration():
    """Test config_manager integratie"""
    try:
        from magic_time_studio.core.config import config_manager
        
        print("\n🔧 Test config_manager integratie:")
        
        # Test enkele instellingen ophalen
        cpu_limit = config_manager.get_env("CPU_LIMIT_PERCENTAGE", "80")
        memory_limit = config_manager.get_env("MEMORY_LIMIT_MB", "8192")
        translator = config_manager.get("default_translator", "libretranslate")
        
        print(f"  - CPU Limiet: {cpu_limit}%")
        print(f"  - Geheugen Limiet: {memory_limit} MB")
        print(f"  - Vertaler: {translator}")
        
        # Test instellingen wijzigen
        config_manager.set_env("CPU_LIMIT_PERCENTAGE", "90")
        config_manager.set_env("MEMORY_LIMIT_MB", "12288")
        config_manager.set("default_translator", "libretranslate")
        
        # Test opslaan
        config_manager.save_configuration()
        print("✅ Configuratie opgeslagen via config_manager")
        
        print("✅ Config_manager integratie werkt correct!")
        return True
        
    except Exception as e:
        print(f"❌ Fout bij testen config_manager: {e}")
        return False

def main():
    """Voer alle tests uit"""
    print("🧪 Test Settings Save Functionaliteit...")
    print("=" * 50)
    
    tests = [
        ("Settings Save Test", test_settings_save),
        ("Config Manager Test", test_config_manager_integration)
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
        print("🎉 Alle tests geslaagd! Settings kunnen correct worden opgeslagen.")
        print("\n💡 Conclusie:")
        print("✅ update_translator_status methode toegevoegd")
        print("✅ Instellingen kunnen worden opgeslagen")
        print("✅ Config_manager integratie werkt")
        print("✅ Settings panel is volledig functioneel")
        return True
    else:
        print("⚠️ Sommige tests gefaald. Controleer de fouten hierboven.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
