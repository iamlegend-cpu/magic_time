#!/usr/bin/env python3
"""
Launcher script voor Magic Time Studio v2.0 (Modulaire versie)
"""

import sys
import os

# Voeg de parent directory toe aan Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

def main():
    """Start Magic Time Studio"""
    try:
        from magic_time_studio.main import main as run_app
        run_app()
    except ImportError as e:
        print(f"❌ Import fout: {e}")
        print("Zorg ervoor dat alle modules correct zijn geïnstalleerd.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Fout bij starten: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 