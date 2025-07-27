"""
Utility functies voor Magic Time Studio
"""

import os
import time
import threading
import tkinter as tk
from typing import Optional, Any, Callable
from .logging import logger

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
    """Veilige widget operaties"""
    
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
    def safe_config(widget: tk.Widget, **kwargs) -> None:
        """Veilige config() aanroep"""
        try:
            if widget is not None and hasattr(widget, "config"):
                widget.config(**kwargs)
        except Exception as e:
            logger.log_debug(f"❌ Fout bij safe_config: {e}")
    
    @staticmethod
    def safe_set(var: tk.Variable, value: Any) -> None:
        """Veilige set() aanroep voor tkinter variabelen"""
        if var is not None:
            try:
                var.set(value)
            except Exception:
                pass
    
    @staticmethod
    def safe_get(var: tk.Variable) -> Any:
        """Veilige get() aanroep voor tkinter variabelen"""
        if var is not None:
            try:
                return var.get()
            except Exception:
                return None
        return None
    
    @staticmethod
    def safe_after(widget: tk.Widget, ms: int, func: Callable) -> Optional[str]:
        """Veilige after() aanroep"""
        try:
            if widget is not None and hasattr(widget, "after"):
                return widget.after(ms, func)
        except Exception as e:
            logger.log_debug(f"❌ Fout bij safe_after: {e}")
        return None
    
    @staticmethod
    def safe_update_idletasks(widget: tk.Widget) -> None:
        """Veilige update_idletasks() aanroep"""
        if widget is not None:
            try:
                widget.update_idletasks()
            except Exception:
                pass
    
    @staticmethod
    def safe_option_add(widget: tk.Widget, pattern: str, value: str) -> None:
        """Veilige option_add() aanroep"""
        if widget is not None:
            try:
                widget.option_add(pattern, value)
            except Exception:
                pass
    
    @staticmethod
    def safe_mainloop(widget: tk.Widget) -> None:
        """Veilige mainloop() aanroep"""
        if widget is not None:
            try:
                widget.mainloop()
            except Exception:
                pass
    
    @staticmethod
    def safe_deiconify(widget: tk.Widget) -> None:
        """Veilige deiconify() aanroep"""
        if widget is not None:
            try:
                widget.deiconify()
            except Exception:
                pass
    
    @staticmethod
    def safe_winfo_children(widget: tk.Widget) -> list:
        """Veilige winfo_children() aanroep"""
        if widget is not None:
            try:
                return widget.winfo_children()
            except Exception:
                return []
        return []

class GUIUpdater:
    """Beheert GUI updates voor thread-safety"""
    
    def __init__(self):
        self.update_batch = []
        self.update_timer = None
        self.root = None
    
    def set_root(self, root: tk.Tk) -> None:
        """Zet de root window"""
        self.root = root
    
    def batch_gui_update(self) -> None:
        """Voer alle gebatchte GUI updates uit"""
        global GUI_UPDATE_BATCH
        try:
            if GUI_UPDATE_BATCH:
                for update_func in GUI_UPDATE_BATCH:
                    try:
                        update_func()
                    except Exception as e:
                        logger.log_debug(f"❌ Fout bij GUI update: {e}")
                GUI_UPDATE_BATCH.clear()
        except Exception as e:
            logger.log_debug(f"❌ Fout bij batch GUI update: {e}")
        finally:
            # Plan volgende update
            if self.root:
                self.update_timer = self.root.after(UI_UPDATE_INTERVAL, self.batch_gui_update)
    
    def schedule_gui_update(self, update_func: Callable) -> None:
        """Plan een GUI update"""
        global GUI_UPDATE_BATCH
        try:
            GUI_UPDATE_BATCH.append(update_func)
            if len(GUI_UPDATE_BATCH) >= MAX_UI_UPDATE_BATCH_SIZE:
                # Force directe update bij te veel updates
                self.batch_gui_update()
            elif self.update_timer is None and self.root:
                # Start update loop als die nog niet draait
                self.update_timer = self.root.after(UI_UPDATE_INTERVAL, self.batch_gui_update)
        except Exception as e:
            logger.log_debug(f"❌ Fout bij plannen GUI update: {e}")
    
    def schedule_immediate_update(self, update_func: Callable) -> None:
        """Plan een onmiddellijke GUI update"""
        try:
            if self.root:
                self.root.after_idle(update_func)
        except Exception as e:
            logger.log_debug(f"❌ Fout bij onmiddellijke GUI update: {e}")
    
    def schedule_priority_update(self, update_func: Callable) -> None:
        """Plan een hoge prioriteit GUI update"""
        try:
            if self.root:
                self.root.after(1, update_func)
        except Exception as e:
            logger.log_debug(f"❌ Fout bij prioriteit GUI update: {e}")

# Globale instanties
safe_widget = SafeWidget()
gui_updater = GUIUpdater()

# Helper functies voor backward compatibility
def safe_basename(path: str) -> str:
    """Backward compatibility functie"""
    return safe_widget.safe_basename(path)

def safe_splitext(path: str) -> tuple:
    """Backward compatibility functie"""
    return safe_widget.safe_splitext(path)

def safe_config(widget: tk.Widget, **kwargs) -> None:
    """Backward compatibility functie"""
    safe_widget.safe_config(widget, **kwargs)

def safe_set(var: tk.Variable, value: Any) -> None:
    """Backward compatibility functie"""
    safe_widget.safe_set(var, value)

def safe_get(var: tk.Variable) -> Any:
    """Backward compatibility functie"""
    return safe_widget.safe_get(var)

def safe_after(widget: tk.Widget, ms: int, func: Callable) -> Optional[str]:
    """Backward compatibility functie"""
    return safe_widget.safe_after(widget, ms, func)

def safe_update_idletasks(widget: tk.Widget) -> None:
    """Backward compatibility functie"""
    safe_widget.safe_update_idletasks(widget)

def safe_option_add(widget: tk.Widget, pattern: str, value: str) -> None:
    """Backward compatibility functie"""
    safe_widget.safe_option_add(widget, pattern, value)

def safe_mainloop(widget: tk.Widget) -> None:
    """Backward compatibility functie"""
    safe_widget.safe_mainloop(widget)

def safe_deiconify(widget: tk.Widget) -> None:
    """Backward compatibility functie"""
    safe_widget.safe_deiconify(widget)

def safe_winfo_children(widget: tk.Widget) -> list:
    """Backward compatibility functie"""
    return safe_widget.safe_winfo_children(widget)

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