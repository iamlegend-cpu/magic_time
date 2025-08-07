"""
Script om Fast Whisper te installeren in de PyQt6 virtual environment
"""

import subprocess
import sys
import os
from pathlib import Path

def install_fast_whisper():
    """Installeer Fast Whisper in de PyQt6 virtual environment"""
    
    # Bepaal het pad naar de PyQt6 virtual environment
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    venv_path = project_root / "pyqt6_env"
    
    # Controleer of virtual environment bestaat
    if not venv_path.exists():
        print("❌ PyQt6 virtual environment niet gevonden!")
        print(f"💡 Verwacht pad: {venv_path}")
        return False
    
    # Bepaal het pad naar pip in de virtual environment
    if os.name == 'nt':  # Windows
        pip_path = venv_path / "Scripts" / "pip.exe"
        python_path = venv_path / "Scripts" / "python.exe"
    else:  # Linux/Mac
        pip_path = venv_path / "bin" / "pip"
        python_path = venv_path / "bin" / "python"
    
    if not pip_path.exists():
        print(f"❌ Pip niet gevonden in virtual environment: {pip_path}")
        return False
    
    print("🚀 Installeer Fast Whisper...")
    print(f"📁 Virtual environment: {venv_path}")
    print(f"🔧 Pip pad: {pip_path}")
    
    try:
        # Installeer Fast Whisper
        print("\n📦 Installeer Fast Whisper...")
        result = subprocess.run([
            str(pip_path), "install", "fast-whisper"
        ], capture_output=True, text=True, check=True)
        
        print("✅ Fast Whisper succesvol geïnstalleerd!")
        print(result.stdout)
        
        # Test de installatie
        print("\n🧪 Test Fast Whisper installatie...")
        test_result = subprocess.run([
            str(python_path), "-c", 
            "from fast_whisper import WhisperModel; print('✅ Fast Whisper import succesvol!')"
        ], capture_output=True, text=True, check=True)
        
        print(test_result.stdout)
        
        # Toon beschikbare modellen
        print("\n📋 Beschikbare Fast Whisper modellen:")
        print("• tiny")
        print("• base") 
        print("• small")
        print("• medium")
        print("• large")
        print("• large-v1")
        print("• large-v2")
        print("• large-v3")
        print("• large-v3-turbo (nieuwste en snelste)")
        print("• turbo")
        
        print("\n🎯 Aanbevolen model: large-v3-turbo")
        print("💡 Dit is het nieuwste en snelste model van OpenAI Whisper")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Fout bij installeren Fast Whisper: {e}")
        print(f"🔍 Error output: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Onverwachte fout: {e}")
        return False

def main():
    """Hoofdfunctie"""
    print("🤖 Fast Whisper Installatie Script")
    print("=" * 50)
    
    success = install_fast_whisper()
    
    if success:
        print("\n🎉 Fast Whisper installatie voltooid!")
        print("💡 Je kunt nu Fast Whisper gebruiken in Magic Time Studio")
        print("💡 Stel DEFAULT_FAST_WHISPER_MODEL=large-v3-turbo in voor beste prestaties")
    else:
        print("\n❌ Fast Whisper installatie gefaald!")
        print("💡 Controleer je internetverbinding en probeer opnieuw")
        sys.exit(1)

if __name__ == "__main__":
    main() 