#!/usr/bin/env python3
"""
Quick fix voor debug print issues in processing_thread.py
"""

import re

def quick_fix_debug():
    """Quick fix voor debug print issues"""
    
    file_path = "magic_time_studio/app_core/processing_thread.py"
    
    # Lees het bestand
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vervang alle print statements met debug_print
    content = re.sub(r'print\(', 'debug_print(', content)
    
    # Voeg debug_print functie toe aan het begin
    content = content.replace(
        '# Debug mode - zet op False om debug output uit te zetten\nDEBUG_MODE = False',
        '# Debug mode - zet op False om debug output uit te zetten\nDEBUG_MODE = False\n\n# Alle debug prints uitcommentariëren voor schonere output\ndef debug_print(*args, **kwargs):\n    """Debug print functie die niets doet"""\n    pass'
    )
    
    # Schrijf het bestand terug
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Quick fix toegepast!")

if __name__ == "__main__":
    quick_fix_debug()
