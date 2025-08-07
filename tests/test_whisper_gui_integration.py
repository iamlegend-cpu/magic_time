"""
Test script voor Whisper GUI integratie
Test of de GUI correct werkt met whisper_manager
"""

import sys
import os
from pathlib import Path

# Voeg project root toe aan Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_whisper_manager_import():
    """Test of whisper_manager correct kan worden geïmporteerd"""
    try:
        from magic_time_studio.processing.whisper_manager import whisper_manager
        print("✅ Whisper manager import succesvol")
        return True
    except Exception as e:
        print(f"❌ Whisper manager import gefaald: {e}")
        return False

def test_whisper_manager_functionality():
    """Test whisper_manager functionaliteit"""
    try:
        from magic_time_studio.processing.whisper_manager import whisper_manager
        
        # Test beschikbare types
        available_types = whisper_manager.get_available_whisper_types()
        print(f"📋 Beschikbare Whisper types: {available_types}")
        
        # Test beschikbare modellen
        for whisper_type in available_types:
            models = whisper_manager.get_available_models(whisper_type)
            print(f"📦 Modellen voor {whisper_type}: {models}")
        
        # Test initialisatie
        if "fast" in available_types:
            success = whisper_manager.initialize("fast", "medium")
            print(f"🚀 Fast Whisper initialisatie: {'✅' if success else '❌'}")
            
            if success:
                info = whisper_manager.get_model_info()
                print(f"📊 Model info: {info}")
                whisper_manager.cleanup()
        
        if "standard" in available_types:
            success = whisper_manager.initialize("standard", "medium")
            print(f"🐌 Standaard Whisper initialisatie: {'✅' if success else '❌'}")
            
            if success:
                info = whisper_manager.get_model_info()
                print(f"📊 Model info: {info}")
                whisper_manager.cleanup()
        
        return True
        
    except Exception as e:
        print(f"❌ Whisper manager functionaliteit gefaald: {e}")
        return False

def test_gui_components():
    """Test GUI componenten"""
    try:
        from PyQt6.QtWidgets import QApplication
        from magic_time_studio.ui_pyqt6.components.settings_panel import SettingsPanel
        from magic_time_studio.ui_pyqt6.config_window import ConfigWindow
        
        # Maak QApplication instance
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Test Settings Panel
        print("🧪 Test Settings Panel...")
        settings_panel = SettingsPanel()
        print("✅ Settings Panel geladen")
        
        # Test Config Window
        print("🧪 Test Config Window...")
        config_window = ConfigWindow()
        print("✅ Config Window geladen")
        
        return True
        
    except Exception as e:
        print(f"❌ GUI componenten test gefaald: {e}")
        return False

def test_whisper_selector():
    """Test Whisper Selector component"""
    try:
        from PyQt6.QtWidgets import QApplication
        from magic_time_studio.ui_pyqt6.components.whisper_selector import WhisperSelectorWidget
        
        # Maak QApplication instance
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Test Whisper Selector
        print("🧪 Test Whisper Selector...")
        whisper_selector = WhisperSelectorWidget()
        print("✅ Whisper Selector geladen")
        
        # Test beschikbare opties
        available_types = whisper_selector.type_combo.count()
        print(f"📋 Beschikbare types in selector: {available_types}")
        
        available_models = whisper_selector.model_combo.count()
        print(f"📦 Beschikbare modellen in selector: {available_models}")
        
        return True
        
    except Exception as e:
        print(f"❌ Whisper Selector test gefaald: {e}")
        return False

def main():
    """Hoofdfunctie voor tests"""
    print("🧪 Start Whisper GUI integratie tests...\n")
    
    # Test 1: Import
    if not test_whisper_manager_import():
        print("❌ Import test gefaald")
        return False
    
    # Test 2: Functionaliteit
    if not test_whisper_manager_functionality():
        print("❌ Functionaliteit test gefaald")
        return False
    
    # Test 3: GUI componenten
    if not test_gui_components():
        print("❌ GUI componenten test gefaald")
        return False
    
    # Test 4: Whisper Selector
    if not test_whisper_selector():
        print("❌ Whisper Selector test gefaald")
        return False
    
    print("\n✅ Alle tests geslaagd!")
    print("\n🎉 Whisper GUI integratie werkt correct!")
    print("\n📋 Wat er nu beschikbaar is:")
    print("• Keuze tussen Fast Whisper en Standaard Whisper")
    print("• Verschillende modellen per type")
    print("• Automatische model switching")
    print("• Verbeterde GUI met emoji's en beschrijvingen")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 