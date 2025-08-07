#!/usr/bin/env python3
"""
Script om syntax errors in processing_thread.py te repareren
"""

import re

def fix_debug_syntax():
    """Repareer syntax errors door debug prints uit te commentariëren"""
    
    file_path = "magic_time_studio/app_core/processing_thread.py"
    
    # Lees het bestand
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vervang alle lege if DEBUG_MODE: blokken
    content = re.sub(r'if DEBUG_MODE:\s*\n\s*\n', '# if DEBUG_MODE:\n#     pass\n', content)
    
    # Vervang alle if DEBUG_MODE: gevolgd door een lege regel
    content = re.sub(r'if DEBUG_MODE:\s*\n\s*print\(', '# if DEBUG_MODE:\n#     print(', content)
    
    # Schrijf het bestand terug
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Syntax errors gerepareerd!")

if __name__ == "__main__":
    fix_debug_syntax()
