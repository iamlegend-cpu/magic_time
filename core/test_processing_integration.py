"""
Test bestand voor Processing integratie
Controleert of ProcessingCore en ProcessingThread correct samenwerken
"""

import sys
import os

def test_processing_core_creation():
    """Test of ProcessingCore correct wordt aangemaakt"""
    print("🔍 Test ProcessingCore creatie...")
    
    try:
        # Test import van ProcessingCore
        from ui_pyside6.components.processing.processing_core import ProcessingCore
        
        print("✅ ProcessingCore geïmporteerd")
        
        # Test of ProcessingCore kan worden aangemaakt
        # We maken een mock FileManager
        class MockFileManager:
            def __init__(self):
                self.completed_files = []
            
            def add_completed_file(self, file_path):
                self.completed_files.append(file_path)
        
        file_manager = MockFileManager()
        processing_core = ProcessingCore(file_manager)
        
        print("✅ ProcessingCore aangemaakt")
        
        # Test of alle benodigde methoden bestaan
        required_methods = [
            'start_processing',
            'update_progress', 
            'update_status',
            'handle_error',
            'handle_completion',
            'get_processing_status'
        ]
        
        for method in required_methods:
            if hasattr(processing_core, method):
                print(f"   ✅ Methode {method} bestaat")
            else:
                print(f"   ❌ Methode {method} ontbreekt")
                return False
        
        print("✅ Alle benodigde methoden aanwezig")
        return True
        
    except ImportError as e:
        print(f"❌ Import fout: {e}")
        return False
    except Exception as e:
        print(f"❌ Onverwachte fout: {e}")
        return False

def test_processing_thread_integration():
    """Test of ProcessingThread correct integreert met ProcessingCore"""
    print("\n🔍 Test ProcessingThread integratie...")
    
    try:
        # Test import van ProcessingThread
        from app_core.processing_thread_new import ProcessingThread
        
        print("✅ ProcessingThread geïmporteerd")
        
        # Test of ProcessingThread kan worden aangemaakt
        # We maken een mock ProcessingCore
        class MockProcessingCore:
            def __init__(self):
                self.settings = {'language': 'en', 'whisper_model': 'large-v3'}
            
            def update_progress(self, progress, message):
                print(f"Mock Progress: {progress}% - {message}")
            
            def update_status(self, message):
                print(f"Mock Status: {message}")
        
        processing_core = MockProcessingCore()
        files = ["test_audio.wav"]
        settings = {'language': 'en', 'whisper_model': 'large-v3'}
        
        # Test constructor
        processing_thread = ProcessingThread(files, processing_core, settings)
        
        print("✅ ProcessingThread aangemaakt")
        
        # Test of instellingen correct worden doorgegeven
        if hasattr(processing_thread, 'settings') and processing_thread.settings:
            language = processing_thread.settings.get('language', 'en')
            model = processing_thread.settings.get('whisper_model', 'large-v3')
            print(f"   ✅ Taal instelling: {language}")
            print(f"   ✅ Model instelling: {model}")
        else:
            print("   ❌ Instellingen niet correct doorgegeven")
            return False
        
        print("✅ ProcessingThread integratie werkt correct")
        return True
        
    except ImportError as e:
        print(f"❌ Import fout: {e}")
        return False
    except Exception as e:
        print(f"❌ Onverwachte fout: {e}")
        return False

def main():
    """Hoofdfunctie voor het testen"""
    print("🚀 Start Processing integratie test...\n")
    
    # Test ProcessingCore
    core_test = test_processing_core_creation()
    
    # Test ProcessingThread integratie
    thread_test = test_processing_thread_integration()
    
    # Samenvatting
    print("\n📊 Test resultaten samenvatting:")
    print(f"   - ProcessingCore: {'✅' if core_test else '❌'}")
    print(f"   - ProcessingThread integratie: {'✅' if thread_test else '❌'}")
    
    if all([core_test, thread_test]):
        print("\n🎉 Alle tests geslaagd! Processing integratie werkt correct.")
        return True
    else:
        print("\n⚠️ Sommige tests gefaald. Controleer de implementatie.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
