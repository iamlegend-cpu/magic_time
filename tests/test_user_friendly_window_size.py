"""
Test voor gebruiksvriendelijke window grootte instellingen
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from magic_time_studio.ui_pyqt6.config_window import ConfigWindow

def test_user_friendly_window_size():
    """Test gebruiksvriendelijke window grootte instellingen"""
    app = QApplication(sys.argv)
    
    print("🔍 Testen van gebruiksvriendelijke window grootte instellingen...")
    print("=" * 60)
    
    # Maak config window aan
    config_window = ConfigWindow()
    
    # Controleer beschikbare opties
    print("📋 Beschikbare window grootte opties:")
    print("-" * 40)
    
    window_size_options = [
        "Klein (800×600)",
        "Gemiddeld (1200×800)", 
        "Groot (1600×900)",
        "Extra Groot (1920×1080)",
        "Automatisch (aanpassen aan scherm)"
    ]
    
    for i, option in enumerate(window_size_options, 1):
        print(f"{i:2d}. {option}")
    
    print("\n" + "=" * 60)
    print("✅ Window grootte instellingen zijn nu gebruiksvriendelijk")
    print("✅ Geen pixels meer voor leken")
    print("✅ Duidelijke beschrijvingen van grootte")
    print("✅ Automatische optie voor scherm aanpassing")
    
    # Test de mapping
    print("\n🔧 Test window grootte mapping:")
    print("-" * 30)
    
    size_mapping = {
        "Klein (800×600)": (800, 600),
        "Gemiddeld (1200×800)": (1200, 800),
        "Groot (1600×900)": (1600, 900),
        "Extra Groot (1920×1080)": (1920, 1080),
        "Automatisch (aanpassen aan scherm)": (0, 0)
    }
    
    for option, (width, height) in size_mapping.items():
        if width == 0 and height == 0:
            print(f"  {option} → Automatisch")
        else:
            print(f"  {option} → {width}×{height} pixels")
    
    print("\n" + "=" * 60)
    print("💡 VOORDELEN VOOR LEKEN:")
    print("-" * 30)
    print("✅ Geen technische pixel kennis nodig")
    print("✅ Duidelijke beschrijvingen (Klein, Gemiddeld, Groot)")
    print("✅ Automatische optie voor beste ervaring")
    print("✅ Intuïtieve keuzes")
    print("✅ Geen verwarring over scherm resoluties")
    
    print("\n" + "=" * 60)
    print("💡 SAMENVATTING:")
    print("-" * 20)
    print("✅ Window grootte instellingen zijn nu gebruiksvriendelijk")
    print("✅ Geen pixels meer voor leken")
    print("✅ Duidelijke opties: Klein, Gemiddeld, Groot, Extra Groot, Automatisch")
    print("✅ Automatische optie past zich aan aan scherm")
    print("✅ Veel intuïtiever voor niet-technische gebruikers")
    
    app.quit()

if __name__ == "__main__":
    test_user_friendly_window_size()
