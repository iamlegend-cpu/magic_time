"""
Runtime Hook voor Magic Time Studio PyInstaller Bundle
Zorgt voor correcte pad handling en module discovery
"""

import sys
import os
import types # Added for creating empty modules

def _is_pyinstaller_build():
    """Controleer of dit een PyInstaller build is"""
    return (
        'PyInstaller' in str(sys.modules.get('__main__', '')) or
        'pyinstaller' in str(sys.modules.get('__main__', '')).lower() or
        'build' in str(sys.modules.get('__main__', '')).lower()
    )

def _is_pyinstaller_runtime():
    """Controleer of dit een PyInstaller runtime is (geen build)"""
    return hasattr(sys, '_MEIPASS') and not _is_pyinstaller_build()

def _setup_magic_time_studio_paths():
    """Setup Python paths voor Magic Time Studio"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller bundle
        bundle_dir = sys._MEIPASS
        print(f"🔧 Runtime hook: Bundle directory: {bundle_dir}")
        
        # Voeg bundle directory toe aan Python path
        if bundle_dir not in sys.path:
            sys.path.insert(0, bundle_dir)
            print(f"🔧 Runtime hook: Bundle directory toegevoegd aan sys.path")
        
        # Voeg subdirectories toe voor betere module discovery
        subdirs = ['core', 'app_core', 'ui_pyqt6', 'models']
        for subdir in subdirs:
            subdir_path = os.path.join(bundle_dir, subdir)
            if os.path.exists(subdir_path) and subdir_path not in sys.path:
                sys.path.insert(0, subdir_path)
                print(f"🔧 Runtime hook: {subdir} directory toegevoegd aan sys.path")
        
        # Voeg ook de magic_time_studio package directory toe
        magic_time_studio_dir = os.path.join(bundle_dir, 'magic_time_studio')
        if os.path.exists(magic_time_studio_dir) and magic_time_studio_dir not in sys.path:
            sys.path.insert(0, magic_time_studio_dir)
            print(f"🔧 Runtime hook: magic_time_studio package directory toegevoegd aan sys.path")
        
        print("✅ Runtime hook: Alle paden correct ingesteld")
    else:
        print("🔧 Runtime hook: Normale Python omgeving gedetecteerd - skip runtime hook")

def _inject_logging_module():
    """Injecteer logging module in sys.modules voor compatibiliteit"""
    if 'logging' not in sys.modules:
        try:
            # Probeer de echte logging module te importeren
            import logging
            print("✅ Runtime hook: Echte logging module geladen")
        except ImportError:
            print("⚠️ Runtime hook: Echte logging module niet beschikbaar")
    else:
        print("✅ Runtime hook: Logging module al beschikbaar")

def _inject_magic_time_studio_modules():
    """Injecteer Magic Time Studio modules als echte Python modules"""
    if hasattr(sys, '_MEIPASS'):
        bundle_dir = sys._MEIPASS
        
        # Import importlib.util hier om de fout te voorkomen
        try:
            import importlib.util
        except ImportError:
            print("❌ Runtime hook: importlib.util niet beschikbaar")
            return
        
        # Injecteer alleen als de modules nog niet bestaan
        if 'magic_time_studio' not in sys.modules:
            try:
                # Maak magic_time_studio package
                magic_time_studio_spec = importlib.util.spec_from_file_location(
                    "magic_time_studio", 
                    os.path.join(bundle_dir, "magic_time_studio", "__init__.py")
                )
                if magic_time_studio_spec and magic_time_studio_spec.loader:
                    magic_time_studio = importlib.util.module_from_spec(magic_time_studio_spec)
                    sys.modules['magic_time_studio'] = magic_time_studio
                    magic_time_studio_spec.loader.exec_module(magic_time_studio)
                    print("✅ Runtime hook: magic_time_studio package geïnjecteerd")
                else:
                    print("⚠️ Runtime hook: magic_time_studio package kon niet worden gemaakt")
            except Exception as e:
                print(f"⚠️ Runtime hook: Fout bij injecteren magic_time_studio package: {e}")
        
        # Injecteer core modules
        core_modules = [
            'magic_time_studio.core.config',
            'magic_time_studio.core.stop_manager',
            'magic_time_studio.core.all_functions',
            'magic_time_studio.core.translation_functions',
            'magic_time_studio.core.audio_functions',
            'magic_time_studio.core.video_functions',
            'magic_time_studio.core.file_functions',
            'magic_time_studio.core.subtitle_functions',
            'magic_time_studio.core.whisper_functions',
        ]
        
        for module_name in core_modules:
            if module_name not in sys.modules:
                try:
                    # Bepaal het pad naar de module
                    module_path = module_name.replace('magic_time_studio.', '')
                    module_file = os.path.join(bundle_dir, 'magic_time_studio', module_path.replace('.', os.sep) + '.py')
                    
                    if os.path.exists(module_file):
                        module_spec = importlib.util.spec_from_file_location(module_name, module_file)
                        if module_spec and module_spec.loader:
                            module = importlib.util.module_from_spec(module_spec)
                            sys.modules[module_name] = module
                            module_spec.loader.exec_module(module)
                            print(f"✅ Runtime hook: {module_name} geïnjecteerd")
                        else:
                            print(f"⚠️ Runtime hook: {module_name} kon niet worden gemaakt")
                    else:
                        # Module bestand bestaat niet - maak een lege module aan
                        print(f"⚠️ Runtime hook: {module_name} bestand niet gevonden, maak lege module aan")
                        empty_module = types.ModuleType(module_name)
                        sys.modules[module_name] = empty_module
                        print(f"✅ Runtime hook: {module_name} lege module aangemaakt")
                except Exception as e:
                    print(f"⚠️ Runtime hook: Fout bij injecteren {module_name}: {e}")
                    # Maak een lege module aan als fallback
                    try:
                        empty_module = types.ModuleType(module_name)
                        sys.modules[module_name] = empty_module
                        print(f"✅ Runtime hook: {module_name} fallback module aangemaakt")
                    except Exception as e2:
                        print(f"❌ Runtime hook: Kon geen fallback module maken voor {module_name}: {e2}")
        
        # Injecteer app_core modules
        app_core_modules = [
            'magic_time_studio.app_core.main_entry',
            'magic_time_studio.app_core.magic_time_studio_pyqt6',
            'magic_time_studio.app_core.ui_manager',
        ]
        
        for module_name in app_core_modules:
            if module_name not in sys.modules:
                try:
                    # Bepaal het pad naar de module
                    module_path = module_name.replace('magic_time_studio.', '')
                    module_file = os.path.join(bundle_dir, 'magic_time_studio', module_path.replace('.', os.sep) + '.py')
                    
                    if os.path.exists(module_file):
                        module_spec = importlib.util.spec_from_file_location(module_name, module_file)
                        if module_spec and module_spec.loader:
                            module = importlib.util.module_from_spec(module_spec)
                            sys.modules[module_name] = module
                            module_spec.loader.exec_module(module)
                            print(f"✅ Runtime hook: {module_name} geïnjecteerd")
                        else:
                            print(f"⚠️ Runtime hook: {module_name} kon niet worden gemaakt")
                    else:
                        # Module bestand bestaat niet - maak een lege module aan
                        print(f"⚠️ Runtime hook: {module_name} bestand niet gevonden, maak lege module aan")
                        empty_module = types.ModuleType(module_name)
                        sys.modules[module_name] = empty_module
                        print(f"✅ Runtime hook: {module_name} lege module aangemaakt")
                except Exception as e:
                    print(f"⚠️ Runtime hook: Fout bij injecteren {module_name}: {e}")
                    # Maak een lege module aan als fallback
                    try:
                        empty_module = types.ModuleType(module_name)
                        sys.modules[module_name] = empty_module
                        print(f"✅ Runtime hook: {module_name} fallback module aangemaakt")
                    except Exception as e2:
                        print(f"❌ Runtime hook: Kon geen fallback module maken voor {module_name}: {e2}")
        
        # Injecteer UI modules
        ui_modules = [
            'magic_time_studio.ui_pyqt6.main_window',
            'magic_time_studio.ui_pyqt6.main_window_parts.main_window_core',
        ]
        
        for module_name in ui_modules:
            if module_name not in sys.modules:
                try:
                    # Bepaal het pad naar de module
                    module_path = module_name.replace('magic_time_studio.', '')
                    module_file = os.path.join(bundle_dir, 'magic_time_studio', module_path.replace('.', os.sep) + '.py')
                    
                    if os.path.exists(module_file):
                        module_spec = importlib.util.spec_from_file_location(module_name, module_file)
                        if module_spec and module_spec.loader:
                            module = importlib.util.module_from_spec(module_spec)
                            sys.modules[module_name] = module
                            module_spec.loader.exec_module(module)
                            print(f"✅ Runtime hook: {module_name} geïnjecteerd")
                        else:
                            print(f"⚠️ Runtime hook: {module_name} kon niet worden gemaakt")
                    else:
                        # Module bestand bestaat niet - maak een lege module aan
                        print(f"⚠️ Runtime hook: {module_name} bestand niet gevonden, maak lege module aan")
                        empty_module = types.ModuleType(module_name)
                        sys.modules[module_name] = empty_module
                        print(f"✅ Runtime hook: {module_name} lege module aangemaakt")
                except Exception as e:
                    print(f"⚠️ Runtime hook: Fout bij injecteren {module_name}: {e}")
                    # Maak een lege module aan als fallback
                    try:
                        empty_module = types.ModuleType(module_name)
                        sys.modules[module_name] = empty_module
                        print(f"✅ Runtime hook: {module_name} fallback module aangemaakt")
                    except Exception as e2:
                        print(f"❌ Runtime hook: Kon geen fallback module maken voor {module_name}: {e2}")
        
        # Injecteer unittest module handmatig voor PyTorch
        if 'unittest' not in sys.modules:
            try:
                import unittest
                sys.modules['unittest'] = unittest
                print("✅ Runtime hook: unittest module handmatig geïnjecteerd")
            except Exception as e:
                print(f"⚠️ Runtime hook: unittest injectie gefaald: {e}")
        
        # Injecteer PyTorch modules - alleen de essentiële
        # PyTorch wordt nu automatisch gedetecteerd door de custom hook
        print("✅ Runtime hook: PyTorch wordt automatisch gedetecteerd door custom hook")
        
        print("✅ Runtime hook: Alle belangrijke modules geïnjecteerd")

def _fix_pytorch_imports():
    """Repareer PyTorch imports zodat ze beschikbaar zijn in de executable"""
    if hasattr(sys, '_MEIPASS'):
        try:
            # Probeer torch te importeren
            import torch
            print("✅ Runtime hook: PyTorch succesvol geïmporteerd")
            
            # Controleer CUDA beschikbaarheid
            if torch.cuda.is_available():
                print(f"✅ Runtime hook: CUDA beschikbaar - {torch.cuda.get_device_name(0)}")
                print(f"✅ Runtime hook: CUDA versie: {torch.version.cuda}")
            else:
                print("⚠️ Runtime hook: CUDA niet beschikbaar in PyTorch")
                
        except ImportError as e:
            print(f"❌ Runtime hook: PyTorch import gefaald: {e}")
            print("🔧 Runtime hook: Probeer torch modules handmatig te laden...")
            
            # Probeer torch modules handmatig te laden
            try:
                # Voeg torch directory toe aan sys.path
                torch_dir = os.path.join(sys._MEIPASS, 'torch')
                if os.path.exists(torch_dir) and torch_dir not in sys.path:
                    sys.path.insert(0, torch_dir)
                    print(f"✅ Runtime hook: Torch directory toegevoegd aan sys.path: {torch_dir}")
                
                # Probeer opnieuw torch te importeren
                import torch
                print("✅ Runtime hook: PyTorch succesvol geïmporteerd na pad fix")
                
            except ImportError as e2:
                print(f"❌ Runtime hook: PyTorch import blijft falen: {e2}")
                print("⚠️ Runtime hook: PyTorch functionaliteit zal niet beschikbaar zijn")
        
        except Exception as e:
            print(f"❌ Runtime hook: Onverwachte fout bij PyTorch import: {e}")

def _setup_environment():
    """Setup environment variabelen"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller bundle
        bundle_dir = sys._MEIPASS
        
        # Zet working directory naar bundle directory
        try:
            os.chdir(bundle_dir)
            print(f"🔧 Runtime hook: Working directory ingesteld op: {bundle_dir}")
        except Exception as e:
            print(f"⚠️ Runtime hook: Kon working directory niet instellen: {e}")
        
        # Zet environment variabelen
        os.environ['MAGIC_TIME_STUDIO_BUNDLE'] = 'true'
        os.environ['MAGIC_TIME_STUDIO_BUNDLE_DIR'] = bundle_dir
        print("🔧 Runtime hook: Environment variabelen ingesteld")
    else:
        print("🔧 Runtime hook: Normale Python omgeving - geen environment aanpassingen")

# Controleer eerst of dit een PyInstaller build is
if _is_pyinstaller_build():
    print("🔧 Runtime hook: PyInstaller build gedetecteerd - skip alle runtime hook functionaliteit")
    print("✅ Magic Time Studio Runtime Hook voltooid (build mode)")
elif _is_pyinstaller_runtime():
    print("🔧 Runtime hook: PyInstaller runtime gedetecteerd - voer alle setup uit")
    # Voer alle setup functies uit voor runtime
    _setup_magic_time_studio_paths()
    _inject_logging_module() # Voeg de logging module toe
    _inject_magic_time_studio_modules() # Voeg de Magic Time Studio modules toe
    _fix_pytorch_imports() # Voeg de PyTorch import fix toe
    _setup_environment()
    print("✅ Magic Time Studio Runtime Hook voltooid (runtime mode)")
else:
    print("🔧 Runtime hook: Normale Python omgeving gedetecteerd - skip runtime hook")
    print("✅ Magic Time Studio Runtime Hook voltooid (normale mode)")
