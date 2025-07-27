"""
Thema management voor Magic Time Studio UI
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Optional
from ..core.config import config_manager
from ..core.logging import logger

class ThemeManager:
    """Beheert thema's en styling voor de UI"""
    
    def __init__(self):
        self.current_theme = config_manager.get("theme", "dark")
        self.colors = config_manager.get_theme_colors(self.current_theme)
    
    def get_colors(self, theme_name: Optional[str] = None) -> Dict[str, str]:
        """Krijg kleuren voor een thema"""
        if theme_name is None:
            theme_name = self.current_theme
        return config_manager.get_theme_colors(theme_name)
    
    def apply_theme(self, root: tk.Tk, theme_name: str) -> None:
        """Pas een thema toe op de hele applicatie"""
        self.current_theme = theme_name
        self.colors = self.get_colors(theme_name)
        
        # Sla thema op in configuratie
        config_manager.set("theme", theme_name)
        config_manager.save_configuration()
        
        # Pas thema toe op root window
        root.configure(bg=self.colors["main_bg"])
        
        # Pas thema toe op alle widgets
        self._apply_theme_to_widgets(root)
        
        logger.log_debug(f"🎨 Thema '{theme_name}' toegepast")
    
    def _apply_theme_to_widgets(self, parent_widget: tk.Widget) -> None:
        """Pas thema toe op alle widgets recursief"""
        try:
            # Pas thema toe op huidige widget
            self._apply_theme_to_widget(parent_widget)
            
            # Pas thema toe op alle child widgets
            for child in parent_widget.winfo_children():
                self._apply_theme_to_widgets(child)
        except Exception as e:
            logger.log_debug(f"❌ Fout bij toepassen thema op widget: {e}")
    
    def _apply_theme_to_widget(self, widget: tk.Widget) -> None:
        """Pas thema toe op een specifieke widget"""
        try:
            widget_class = widget.winfo_class()
            
            if widget_class == "Frame" or widget_class == "TFrame":
                widget.configure(
                    bg=self.colors["bg"],
                    fg=self.colors["fg"]
                )
            elif widget_class == "Label" or widget_class == "TLabel":
                widget.configure(
                    bg=self.colors["bg"],
                    fg=self.colors["fg"]
                )
            elif widget_class == "Button" or widget_class == "TButton":
                widget.configure(
                    bg=self.colors["knop"],
                    fg=self.colors["knop_fg"],
                    activebackground=self.colors["accent"],
                    activeforeground=self.colors["knop_fg"]
                )
            elif widget_class == "Entry" or widget_class == "TEntry":
                widget.configure(
                    bg=self.colors["frame"],
                    fg=self.colors["fg"],
                    insertbackground=self.colors["fg"]
                )
            elif widget_class == "Text":
                widget.configure(
                    bg=self.colors["frame"],
                    fg=self.colors["fg"],
                    insertbackground=self.colors["fg"],
                    selectbackground=self.colors["accent"]
                )
            elif widget_class == "Listbox":
                widget.configure(
                    bg=self.colors["frame"],
                    fg=self.colors["fg"],
                    selectbackground=self.colors["accent"],
                    selectforeground=self.colors["fg"]
                )
            elif widget_class == "Combobox":
                widget.configure(
                    background=self.colors["frame"],
                    foreground=self.colors["fg"],
                    selectbackground=self.colors["accent"],
                    selectforeground=self.colors["fg"]
                )
            elif widget_class == "Scale" or widget_class == "TScale":
                widget.configure(
                    bg=self.colors["bg"],
                    fg=self.colors["fg"],
                    troughcolor=self.colors["frame"],
                    highlightbackground=self.colors["bg"]
                )
            elif widget_class == "Progressbar":
                widget.configure(
                    background=self.colors["accent"],
                    troughcolor=self.colors["frame"]
                )
            elif widget_class == "Notebook":
                widget.configure(
                    background=self.colors["bg"]
                )
            elif widget_class == "PanedWindow":
                widget.configure(
                    bg=self.colors["bg"]
                )
                
        except Exception as e:
            # Stil falen voor widgets die geen configuratie ondersteunen
            pass
    
    def create_styled_button(self, parent: tk.Widget, text: str, command: callable, **kwargs) -> tk.Button:
        """Maak een gestylede knop"""
        # Verwijder font, bg, fg uit kwargs als ze al bestaan
        font = kwargs.pop("font", ("Arial", 10))
        bg = kwargs.pop("bg", self.colors["knop"])
        fg = kwargs.pop("fg", self.colors["knop_fg"])
        
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=self.colors["accent"],
            activeforeground=self.colors["knop_fg"],
            relief=tk.RAISED,
            borderwidth=2,
            font=font,
            **kwargs
        )
        return button
    
    def create_styled_label(self, parent: tk.Widget, text: str = "", **kwargs) -> tk.Label:
        """Maak een gestylede label"""
        # Verwijder font en fg uit kwargs als ze al bestaan
        font = kwargs.pop("font", ("Arial", 10))
        fg = kwargs.pop("fg", self.colors["fg"])
        
        label = tk.Label(
            parent,
            text=text,
            bg=self.colors["bg"],
            fg=fg,
            font=font,
            **kwargs
        )
        return label
    
    def create_styled_frame(self, parent: tk.Widget, **kwargs) -> tk.Frame:
        """Maak een gestylede frame"""
        # Verwijder relief en borderwidth uit kwargs als ze al bestaan
        relief = kwargs.pop("relief", tk.RAISED)
        borderwidth = kwargs.pop("borderwidth", 1)
        
        frame = tk.Frame(
            parent,
            bg=self.colors["bg"],
            relief=relief,
            borderwidth=borderwidth,
            **kwargs
        )
        return frame
    
    def create_styled_entry(self, parent: tk.Widget, **kwargs) -> tk.Entry:
        """Maak een gestylede entry"""
        # Verwijder font uit kwargs als het al bestaat
        font = kwargs.pop("font", ("Arial", 10))
        
        entry = tk.Entry(
            parent,
            bg=self.colors["frame"],
            fg=self.colors["fg"],
            insertbackground=self.colors["fg"],
            relief=tk.SUNKEN,
            borderwidth=2,
            font=font,
            **kwargs
        )
        return entry
    
    def create_styled_combobox(self, parent: tk.Widget, values: list, **kwargs) -> ttk.Combobox:
        """Maak een gestylede combobox"""
        # Verwijder font uit kwargs als het al bestaat
        font = kwargs.pop("font", ("Arial", 10))
        
        combobox = ttk.Combobox(
            parent,
            values=values,
            state="readonly",
            font=font,
            **kwargs
        )
        return combobox
    
    def create_styled_progressbar(self, parent: tk.Widget, **kwargs) -> ttk.Progressbar:
        """Maak een gestylede progressbar"""
        progressbar = ttk.Progressbar(
            parent,
            mode="determinate",
            **kwargs
        )
        return progressbar
    
    def get_available_themes(self) -> list:
        """Krijg lijst van beschikbare thema's"""
        return config_manager.get_available_themes()
    
    def get_current_theme(self) -> str:
        """Krijg het huidige thema"""
        return self.current_theme

# Globale theme manager instantie
theme_manager = ThemeManager() 