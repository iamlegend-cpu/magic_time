#!/usr/bin/env python3
"""
Test voor No Hardcoded IPs - Magic Time Studio
Test of er geen hardcoded IP adressen meer in de code staan
"""

import sys
import os
import re

# Voeg project root toe aan Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_no_hardcoded_ips():
    """Test of er geen hardcoded IP adressen in de code staan"""
    try:
        print("🔍 Zoek naar hardcoded IP adressen...")
        
        # Zoek naar hardcoded IP adressen in relevante bestanden
        hardcoded_ips = []
        
        # Controleer settings_panel.py
        settings_panel_path = "magic_time_studio/ui_pyqt6/components/settings_panel.py"
        if os.path.exists(settings_panel_path):
            with open(settings_panel_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Zoek naar IP adressen (192.168.x.x, 10.x.x.x, etc.)
                ip_pattern = r'\b(?:192\.168\.|10\.|172\.(?:1[6-9]|2[0-9]|3[0-1])\.)\d+\.\d+'
                matches = re.findall(ip_pattern, content)
                if matches:
                    hardcoded_ips.append(f"settings_panel.py: {matches}")
        
        # Controleer config_window.py
        config_window_path = "magic_time_studio/ui_pyqt6/config_window.py"
        if os.path.exists(config_window_path):
            with open(config_window_path, 'r', encoding='utf-8') as f:
                content = f.read()
                ip_pattern = r'\b(?:192\.168\.|10\.|172\.(?:1[6-9]|2[0-9]|3[0-1])\.)\d+\.\d+'
                matches = re.findall(ip_pattern, content)
                if matches:
                    hardcoded_ips.append(f"config_window.py: {matches}")
        
        # Controleer stop_manager.py
        stop_manager_path = "magic_time_studio/core/stop_manager.py"
        if os.path.exists(stop_manager_path):
            with open(stop_manager_path, 'r', encoding='utf-8') as f:
                content = f.read()
                ip_pattern = r'\b(?:192\.168\.|10\.|172\.(?:1[6-9]|2[0-9]|3[0-1])\.)\d+\.\d+'
                matches = re.findall(ip_pattern, content)
                if matches:
                    hardcoded_ips.append(f"stop_manager.py: {matches}")
        
        if hardcoded_ips:
            print("❌ Hardcoded IP adressen gevonden:")
            for ip in hardcoded_ips:
                print(f"  - {ip}")
            return False
        else:
            print("✅ Geen hardcoded IP adressen gevonden in code bestanden")
            return True
        
    except Exception as e:
        print(f"❌ Fout bij testen hardcoded IPs: {e}")
        return False

def test_placeholder_texts():
    """Test of placeholder teksten geen hardcoded IPs bevatten"""
    try:
        print("\n📝 Test placeholder teksten...")
        
        # Test settings_panel.py placeholder
        from PyQt6.QtWidgets import QApplication
        from magic_time_studio.ui_pyqt6.components.settings_panel import SettingsPanel
        
        app = QApplication(sys.argv)
        settings_panel = SettingsPanel()
        
        placeholder = settings_panel.translate_server_edit.placeholderText()
        print(f"  - Settings panel placeholder: '{placeholder}'")
        
        # Controleer of placeholder geen hardcoded IP bevat
        ip_pattern = r'\b(?:192\.168\.|10\.|172\.(?:1[6-9]|2[0-9]|3[0-1])\.)\d+\.\d+'
        if re.search(ip_pattern, placeholder):
            print("❌ Placeholder bevat hardcoded IP adres")
            return False
        else:
            print("✅ Placeholder bevat geen hardcoded IP adres")
            return True
        
    except Exception as e:
        print(f"❌ Fout bij testen placeholder teksten: {e}")
        return False

def test_default_values():
    """Test of default waarden geen hardcoded IPs bevatten"""
    try:
        print("\n🔧 Test default waarden...")
        
        from magic_time_studio.core.config import config_manager
        
        # Test of config_manager geen hardcoded IP gebruikt
        server_value = config_manager.get_env("LIBRETRANSLATE_SERVER", "")
        print(f"  - Config manager default: '{server_value}'")
        
        if server_value == "":
            print("✅ Config manager gebruikt geen hardcoded IP")
            return True
        else:
            print("❌ Config manager gebruikt nog steeds hardcoded IP")
            return False
        
    except Exception as e:
        print(f"❌ Fout bij testen default waarden: {e}")
        return False

def main():
    """Voer alle tests uit"""
    print("🧪 Test No Hardcoded IPs...")
    print("=" * 50)
    
    tests = [
        ("No Hardcoded IPs Test", test_no_hardcoded_ips),
        ("Placeholder Texts Test", test_placeholder_texts),
        ("Default Values Test", test_default_values)
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
        print("🎉 Alle tests geslaagd! Geen hardcoded IP adressen meer.")
        print("\n💡 Conclusie:")
        print("✅ Geen hardcoded IP adressen in code")
        print("✅ Placeholder teksten gebruiken generieke voorbeelden")
        print("✅ Gebruiker moet eigen server IP invoeren")
        print("✅ Config manager gebruikt geen default IP")
        return True
    else:
        print("⚠️ Sommige tests gefaald. Er zijn nog hardcoded IP adressen.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
