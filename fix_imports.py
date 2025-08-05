#!/usr/bin/env python3
"""
Script om relative imports te vervangen door absolute imports voor PyInstaller compatibiliteit
"""

import os
import re
import glob

def fix_relative_imports(file_path):
    """Vervang relative imports door absolute imports in een bestand"""
    print(f"🔍 Processing: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return
    
    # Vervang relative imports
    # from .module import -> from magic_time_studio.module import
    # from ..module import -> from magic_time_studio.module import
    # from ...module import -> from magic_time_studio.module import
    
    # Patroon voor relative imports
    patterns = [
        (r'from \.\.\.([a-zA-Z_][a-zA-Z0-9_]*) import', r'from magic_time_studio.\1 import'),
        (r'from \.\.([a-zA-Z_][a-zA-Z0-9_]*) import', r'from magic_time_studio.\1 import'),
        (r'from \.([a-zA-Z_][a-zA-Z0-9_]*) import', r'from magic_time_studio.\1 import'),
    ]
    
    modified = False
    for pattern, replacement in patterns:
        if re.search(pattern, content):
            print(f"  🔧 Found pattern: {pattern}")
            content = re.sub(pattern, replacement, content)
            modified = True
    
    if modified:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed imports in: {file_path}")
        except Exception as e:
            print(f"❌ Error writing {file_path}: {e}")
    else:
        print(f"ℹ️  No relative imports found in: {file_path}")

def main():
    """Main functie om alle Python bestanden te verwerken"""
    # Zoek alle Python bestanden in magic_time_studio
    python_files = glob.glob('magic_time_studio/**/*.py', recursive=True)
    
    print(f"🔍 Found {len(python_files)} Python files to process")
    
    for file_path in python_files:
        fix_relative_imports(file_path)
    
    print("✅ All relative imports have been converted to absolute imports!")

if __name__ == "__main__":
    main() 