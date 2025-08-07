"""
Test of de UI alleen Fast Whisper toont en geen Standard Whisper opties meer heeft
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from magic_time_studio.ui_pyqt6.config_window import ConfigWindow
from magic_time_studio.ui_pyqt6.components.settings_panel import SettingsPanel

def test_fast_whisper_only_ui():
    """Test of de UI alleen Fast Whisper opties toont"""
    app = QApplication(sys.argv)
    
    print("🧪 Test Fast Whisper Only UI...")
    
    # Test config window
    print("\n📋 Test Config Window Processing Tab:")
    config_window = ConfigWindow()
    
    # Zoek de processing tab
    processing_tab = None
    for i in range(config_window.tab_widget.count()):
        tab = config_window.tab_widget.widget(i)
        if hasattr(tab, 'whisper_type_combo'):
            processing_tab = tab
            break
    
    if processing_tab:
        # Controleer whisper type combo
        whisper_combo = processing_tab.whisper_type_combo
        print(f"  • Whisper Type Combo items: {[whisper_combo.itemText(i) for i in range(whisper_combo.count())]}")
        print(f"  • Whisper Type Combo enabled: {whisper_combo.isEnabled()}")
        print(f"  • Huidige selectie: {whisper_combo.currentText()}")
        
        # Controleer of alleen Fast Whisper beschikbaar is
        fast_whisper_only = (
            whisper_combo.count() == 1 and
            "Fast Whisper" in whisper_combo.itemText(0) and
            not whisper_combo.isEnabled()
        )
        
        if fast_whisper_only:
            print("  ✅ Config Window: Alleen Fast Whisper beschikbaar")
        else:
            print("  ❌ Config Window: Nog Standard Whisper opties aanwezig")
    
    # Test settings panel
    print("\n⚙️ Test Settings Panel:")
    settings_panel = SettingsPanel()
    
    # Controleer whisper type combo in settings panel
    whisper_combo = settings_panel.whisper_type_combo
    print(f"  • Whisper Type Combo items: {[whisper_combo.itemText(i) for i in range(whisper_combo.count())]}")
    print(f"  • Huidige selectie: {whisper_combo.currentText()}")
    
    # Controleer of alleen Fast Whisper beschikbaar is
    fast_whisper_only_settings = (
        whisper_combo.count() == 1 and
        "Fast Whisper" in whisper_combo.itemText(0)
    )
    
    if fast_whisper_only_settings:
        print("  ✅ Settings Panel: Alleen Fast Whisper beschikbaar")
    else:
        print("  ❌ Settings Panel: Nog Standard Whisper opties aanwezig")
    
    # Test model lijst
    print("\n📦 Test Model Lijst:")
    model_combo = settings_panel.model_combo
    models = [model_combo.itemText(i) for i in range(model_combo.count())]
    print(f"  • Beschikbare modellen: {models}")
    
    # Controleer of alleen Fast Whisper modellen beschikbaar zijn
    fast_models = ["large-v3-turbo", "large-v3", "large-v2", "large-v1", "turbo"]
    has_fast_models = any("Large V3 Turbo" in model or "Turbo" in model for model in models)
    
    if has_fast_models:
        print("  ✅ Fast Whisper modellen beschikbaar")
    else:
        print("  ❌ Geen Fast Whisper modellen gevonden")
    
    # Test whisper manager
    print("\n🔧 Test Whisper Manager:")
    try:
        from magic_time_studio.processing.whisper_manager import whisper_manager
        
        # Test initialisatie
        success = whisper_manager.initialize("fast", "large-v3-turbo")
        if success:
            print("  ✅ Whisper Manager: Fast Whisper geïnitialiseerd")
        else:
            print("  ❌ Whisper Manager: Fast Whisper initialisatie gefaald")
        
        # Test beschikbare types
        available_types = whisper_manager.get_available_whisper_types()
        print(f"  • Beschikbare types: {available_types}")
        
        if "fast" in available_types and "standard" not in available_types:
            print("  ✅ Whisper Manager: Alleen Fast Whisper beschikbaar")
        else:
            print("  ❌ Whisper Manager: Nog Standard Whisper beschikbaar")
            
    except Exception as e:
        print(f"  ❌ Fout bij testen Whisper Manager: {e}")
    
    # Samenvatting
    print("\n📊 Samenvatting:")
    if fast_whisper_only and fast_whisper_only_settings and has_fast_models:
        print("  ✅ Alle UI componenten tonen alleen Fast Whisper")
        print("  ✅ Standard Whisper is volledig verwijderd uit de interface")
    else:
        print("  ❌ Nog Standard Whisper opties gevonden in de UI")
    
    app.quit()

if __name__ == "__main__":
    test_fast_whisper_only_ui()
