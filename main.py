#!/usr/bin/env python3
"""
Magic Time Studio - Hoofd Entry Point
Dit is het centrale startpunt voor het hele programma
"""

import sys
import os

def main():
    """Hoofdfunctie van Magic Time Studio"""
    print("🚀 Magic Time Studio wordt gestart...")
    
    try:
        # Import de hoofdapplicatie - probeer verschillende import methoden
        try:
            # Methode 1: Directe import
            from app_core.main_entry import main as app_main
            print("✅ Hoofdapplicatie geladen via directe import")
        except ImportError:
            try:
                # Methode 2: Via magic_time_studio namespace
                from magic_time_studio.app_core.main_entry import main as app_main
                print("✅ Hoofdapplicatie geladen via magic_time_studio namespace")
            except ImportError:
                # Methode 3: Via relatieve import
                from .app_core.main_entry import main as app_main
                print("✅ Hoofdapplicatie geladen via relatieve import")
        
        # Start de applicatie
        print("✅ Hoofdapplicatie geladen - start Magic Time Studio")
        app_main()
        
    except ImportError as e:
        print(f"❌ Fout bij laden hoofdapplicatie: {e}")
        print("🔍 Controleer of alle modules correct zijn geïnstalleerd")
        return 1
        
    except Exception as e:
        print(f"❌ Onverwachte fout: {e}")
        return 1
    
    print("👋 Magic Time Studio wordt afgesloten")
    return 0

if __name__ == "__main__":
    # Start het programma
    exit_code = main()
    sys.exit(exit_code)
