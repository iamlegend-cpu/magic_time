import sys
import threading
import time
from app_core.magic_time_studio_pyqt6 import MagicTimeStudioPyQt6
from app_core.single_instance import acquire_single_instance_lock, release_single_instance_lock

def main():
    """Hoofdfunctie"""
    print("🚀 Magic Time Studio PyQt6 v2.0")
    print("=" * 50)
    
    # Controleer single instance met atomische lock operatie
    print("🔍 Controleer single instance...")
    
    # Probeer lock te verkrijgen (atomische operatie)
    lock_file = acquire_single_instance_lock()
    if not lock_file:
        print("⚠️ Er draait al een instance van Magic Time Studio")
        print("🔄 Sluit de bestaande applicatie en probeer opnieuw")
        return 1
    
    print("✅ Single instance controle succesvol")
    
    # Maak applicatie
    app = MagicTimeStudioPyQt6()
    app.lock_file = lock_file
    
    try:

        
        # Start applicatie direct in de hoofdthread
        print("🎬 Start applicatie direct in hoofdthread...")
        try:
            result = app.run()
            return result
        except Exception as e:
            print(f"❌ Fout bij starten applicatie: {e}")
            app.quit_app()
            return 1
            
    except KeyboardInterrupt:
        print("\n👋 Applicatie wordt afgesloten...")
        app.quit_app()
        return 0
    except Exception as e:
        print(f"❌ Onverwachte fout: {e}")
        app.quit_app()
        return 1