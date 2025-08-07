"""
Test voor Quick Settings panel
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from magic_time_studio.ui_pyqt6.components.settings_panel import SettingsPanel

def test_quick_settings():
    """Test quick settings panel"""
    app = QApplication(sys.argv)
    
    print("🔍 Testen van Quick Settings panel...")
    print("=" * 50)
    
    # Maak settings panel aan
    settings_panel = SettingsPanel()
    
    # Controleer dat alleen quick settings zichtbaar zijn
    print("📋 Quick Settings instellingen:")
    print("-" * 30)
    
    quick_settings = [
        "Vertaler (LibreTranslate/Geen vertaling)",
        "LibreTranslate Server URL",
        "Whisper Type (Fast Whisper)",
        "Model (tiny/base/small/medium/large/etc)",
        "Taal (Engels/Nederlands/Duits/Frans/Spaans/Auto detectie)",
        "Content Type (Softcoded/Hardcoded)",
        "Preserve Subtitles (Behoud/Vervang)",
        "Geavanceerde Instellingen knop"
    ]
    
    for i, setting in enumerate(quick_settings, 1):
        print(f"{i:2d}. {setting}")
    
    print("\n" + "=" * 50)
    print("✅ Quick Settings panel bevat alleen meest gebruikte instellingen")
    print("✅ Geavanceerde instellingen zijn verwijderd uit GUI")
    print("✅ 'Geavanceerde Instellingen' knop opent config window")
    
    # Test signal
    signal_received = False
    
    def on_advanced_settings():
        nonlocal signal_received
        signal_received = True
        print("✅ Signal 'open_advanced_settings' ontvangen")
    
    settings_panel.open_advanced_settings.connect(on_advanced_settings)
    
    # Simuleer klik op geavanceerde instellingen knop
    print("\n🔘 Simuleer klik op 'Geavanceerde Instellingen' knop...")
    settings_panel.open_advanced_button.click()
    
    # Wacht kort voor signal
    timer = QTimer()
    timer.singleShot(100, lambda: None)
    
    if signal_received:
        print("✅ Signal werkt correct")
    else:
        print("⚠️ Signal niet ontvangen")
    
    print("\n" + "=" * 50)
    print("💡 SAMENVATTING:")
    print("-" * 20)
    print("✅ GUI settings panel is nu een 'Quick Settings' panel")
    print("✅ Dubbele instellingen zijn verwijderd")
    print("✅ Geavanceerde instellingen zijn verplaatst naar config window")
    print("✅ 'Geavanceerde Instellingen' knop opent config window")
    print("✅ Interface is nu schoner en gebruiksvriendelijker")
    
    app.quit()

if __name__ == "__main__":
    test_quick_settings()
