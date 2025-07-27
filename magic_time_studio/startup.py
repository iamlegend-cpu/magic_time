#!/usr/bin/env python3
"""
Magic Time Studio v2.0 - Startup Script
Eenvoudige launcher voor de applicatie
"""

import sys
import os

# Voeg de parent directory toe aan Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

def main():
    """Start Magic Time Studio"""
    try:
        from magic_time_studio.main import main as app_main
        app_main()
    except ImportError as e:
        print(f"❌ Import fout: {e}")
        print("Zorg ervoor dat alle dependencies geïnstalleerd zijn:")
        print("pip install openai-whisper requests")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Kritieke fout: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 