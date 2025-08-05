"""
Utility functies voor Magic Time Studio
"""

import os
import sys
import time
import threading
from typing import Optional, Any, Callable
from magic_time_studio.core.logging import logger

# GUI update optimalisaties
GUI_UPDATE_BATCH = []
GUI_UPDATE_TIMER = None
UI_UPDATE_INTERVAL = 16  # 60 FPS (1000ms / 60)
MAX_UI_UPDATE_BATCH_SIZE = 10

# PIL LANCZOS fix
try:
    from PIL import Image
    LANCZOS_RESAMPLE = getattr(Image, "LANCZOS", getattr(Image, "BICUBIC", 3))
except ImportError:
    LANCZOS_RESAMPLE = 3

class SafeWidget:
    """Veilige widget operaties voor PyQt6"""
    
    @staticmethod
    def safe_basename(path: str) -> str:
        """Veilige basename() aanroep"""
        try:
            if path is not None:
                return os.path.basename(path)
        except Exception as e:
            logger.log_debug(f"❌ Fout bij safe_basename: {e}")
        return "onbekend_bestand"
    
    @staticmethod
    def safe_splitext(path: str) -> tuple:
        """Veilige splitext() aanroep"""
        return os.path.splitext(path) if path else ("onbekend", "")
    
    @staticmethod
    def safe_config(widget: object, **kwargs) -> None:
        """Veilige config() aanroep voor PyQt6 widgets"""
        try:
            if widget is not None and hasattr(widget, "setProperty"):
                for key, value in kwargs.items():
                    widget.setProperty(key, value)
        except Exception as e:
            logger.log_debug(f"❌ Fout bij safe_config: {e}")
    
    @staticmethod
    def safe_set(var: object, value: Any) -> None:
        """Veilige set() aanroep voor PyQt6 variabelen"""
        if var is not None:
            try:
                if hasattr(var, "setValue"):
                    var.setValue(value)
                elif hasattr(var, "setText"):
                    var.setText(str(value))
            except Exception:
                pass
    
    @staticmethod
    def safe_get(var: object) -> Any:
        """Veilige get() aanroep voor PyQt6 variabelen"""
        if var is not None:
            try:
                if hasattr(var, "value"):
                    return var.value()
                elif hasattr(var, "text"):
                    return var.text()
            except Exception:
                return None
        return None
    
    @staticmethod
    def safe_after(widget: object, ms: int, func: Callable) -> Optional[int]:
        """Veilige timer aanroep voor PyQt6"""
        try:
            if widget is not None and hasattr(widget, "startTimer"):
                return widget.startTimer(ms)
        except Exception as e:
            logger.log_debug(f"❌ Fout bij safe_after: {e}")
        return None
    
    @staticmethod
    def safe_update_idletasks(widget: object) -> None:
        """Veilige update aanroep voor PyQt6"""
        if widget is not None:
            try:
                if hasattr(widget, "update"):
                    widget.update()
            except Exception:
                pass
    
    @staticmethod
    def safe_option_add(widget: object, pattern: str, value: str) -> None:
        """Veilige option_add() aanroep - niet nodig voor PyQt6"""
        # PyQt6 gebruikt stylesheets in plaats van options
        pass
    
    @staticmethod
    def safe_mainloop(widget: object) -> None:
        """Veilige mainloop() aanroep - niet nodig voor PyQt6"""
        # PyQt6 gebruikt QApplication.exec()
        pass
    
    @staticmethod
    def safe_deiconify(widget: object) -> None:
        """Veilige deiconify() aanroep voor PyQt6"""
        if widget is not None:
            try:
                if hasattr(widget, "show"):
                    widget.show()
            except Exception:
                pass
    
    @staticmethod
    def safe_winfo_children(widget: object) -> list:
        """Veilige children ophalen voor PyQt6"""
        if widget is not None:
            try:
                if hasattr(widget, "children"):
                    return list(widget.children())
                elif hasattr(widget, "findChildren"):
                    return widget.findChildren()
            except Exception:
                pass
        return []

class GUIUpdater:
    """GUI update manager voor PyQt6"""
    
    def __init__(self):
        self.root = None
        self.update_batch = []
        self.update_timer = None
    
    def set_root(self, root: object) -> None:
        """Zet de root widget"""
        self.root = root
    
    def batch_gui_update(self) -> None:
        """Voer batch GUI updates uit"""
        if self.update_batch:
            try:
                for update_func in self.update_batch:
                    update_func()
            except Exception as e:
                logger.log_debug(f"❌ Fout bij batch GUI update: {e}")
            finally:
                self.update_batch.clear()
    
    def schedule_gui_update(self, update_func: Callable) -> None:
        """Plan een GUI update"""
        if len(self.update_batch) < MAX_UI_UPDATE_BATCH_SIZE:
            self.update_batch.append(update_func)
    
    def schedule_immediate_update(self, update_func: Callable) -> None:
        """Plan een directe GUI update"""
        try:
            update_func()
        except Exception as e:
            logger.log_debug(f"❌ Fout bij immediate update: {e}")
    
    def schedule_priority_update(self, update_func: Callable) -> None:
        """Plan een prioriteit GUI update"""
        try:
            update_func()
        except Exception as e:
            logger.log_debug(f"❌ Fout bij priority update: {e}")

# Globale GUI updater
gui_updater = GUIUpdater()

def create_progress_bar(progress: float, width: int = 50, filename: str = "") -> str:
    """Maak een voortgangsbalk voor console output"""
    filled = int(width * progress)
    bar = "█" * filled + "░" * (width - filled)
    percentage = int(progress * 100)
    return f"{percentage:3d}%|{bar}| {filename}"

# Helper functies voor backward compatibility
def safe_basename(path: str) -> str:
    """Backward compatibility functie"""
    return SafeWidget.safe_basename(path)

def safe_splitext(path: str) -> tuple:
    """Backward compatibility functie"""
    return SafeWidget.safe_splitext(path)

def safe_config(widget: object, **kwargs) -> None:
    """Backward compatibility functie"""
    SafeWidget.safe_config(widget, **kwargs)

def safe_set(var: object, value: Any) -> None:
    """Backward compatibility functie"""
    SafeWidget.safe_set(var, value)

def safe_get(var: object) -> Any:
    """Backward compatibility functie"""
    return SafeWidget.safe_get(var)

def safe_after(widget: object, ms: int, func: Callable) -> Optional[int]:
    """Backward compatibility functie"""
    return SafeWidget.safe_after(widget, ms, func)

def safe_update_idletasks(widget: object) -> None:
    """Backward compatibility functie"""
    SafeWidget.safe_update_idletasks(widget)

def safe_option_add(widget: object, pattern: str, value: str) -> None:
    """Backward compatibility functie"""
    SafeWidget.safe_option_add(widget, pattern, value)

def safe_mainloop(widget: object) -> None:
    """Backward compatibility functie"""
    SafeWidget.safe_mainloop(widget)

def safe_deiconify(widget: object) -> None:
    """Backward compatibility functie"""
    SafeWidget.safe_deiconify(widget)

def safe_winfo_children(widget: object) -> list:
    """Backward compatibility functie"""
    return SafeWidget.safe_winfo_children(widget)

def batch_gui_update():
    """Backward compatibility functie"""
    gui_updater.batch_gui_update()

def schedule_gui_update(update_func: Callable) -> None:
    """Backward compatibility functie"""
    gui_updater.schedule_gui_update(update_func)

def schedule_immediate_update(update_func: Callable) -> None:
    """Backward compatibility functie"""
    gui_updater.schedule_immediate_update(update_func)

def schedule_priority_update(update_func: Callable) -> None:
    """Backward compatibility functie"""
    gui_updater.schedule_priority_update(update_func)

def get_bundle_dir() -> str:
    """Krijg de bundle directory voor PyInstaller"""
    if getattr(sys, 'frozen', False):
        # PyInstaller bundle
        return os.path.dirname(sys.executable)
    else:
        # Normale Python omgeving
        return os.path.dirname(os.path.abspath(__file__))

def find_executable_in_bundle(executable_name: str) -> Optional[str]:
    """Zoek een executable in de bundle directory"""
    bundle_dir = get_bundle_dir()
    executable_path = os.path.join(bundle_dir, executable_name)
    
    if os.path.exists(executable_path):
        return executable_path
    
    # Zoek in subdirectories
    for root, dirs, files in os.walk(bundle_dir):
        if executable_name in files:
            return os.path.join(root, executable_name)
    
    return None 