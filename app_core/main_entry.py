import sys
import threading
import time

# Schakel TF32 in voordat andere modules worden geladen
try:
    from app_core.import_utils import setup_tf32
    setup_tf32()
except Exception as e:
    print(f"⚠️ Kon TF32 niet inschakelen: {e}")

# Import de benodigde modules
try:
    from app_core.magic_time_studio_pyside6 import MagicTimeStudioPySide6
    from app_core.single_instance import acquire_single_instance_lock, release_single_instance_lock
    print("✅ Imports succesvol via app_core.*")
except ImportError as e:
    print(f"❌ Import mislukt: {e}")
    raise

def main():
    """Hoofdfunctie"""
    print("🚀 Magic Time Studio PySide6 v2.0")
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
    app = MagicTimeStudioPySide6()
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