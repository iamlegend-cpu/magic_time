"""
PyQt6 Thema management voor Magic Time Studio UI
"""

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt
from typing import Dict, Any, Optional
# Lazy import van config_manager om circulaire import te voorkomen
def _get_config_manager():
    """Lazy config manager import om circulaire import te voorkomen"""
    try:
        from core.config import config_manager
        return config_manager
    except ImportError:
        return None

class ThemeManager:
    """Beheert thema's en styling voor de PyQt6 UI"""
    
    def __init__(self):
        config_mgr = _get_config_manager()
        self.current_theme = config_mgr.get("theme", "dark") if config_mgr else "dark"
        self.colors = self._get_theme_colors(self.current_theme)
    
    def _get_theme_colors(self, theme_name: str) -> Dict[str, str]:
        """Krijg kleuren voor een thema"""
        if theme_name == "dark":
            return {
                "main_bg": "#2b2b2b",
                "bg": "#3c3c3c",
                "fg": "#ffffff",
                "accent": "#007acc",
                "knop": "#4c4c4c",
                "knop_fg": "#ffffff",
                "knop_start": "#4caf50",
                "knop_stop": "#d32f2f",
                "knop_delete_all": "#d32f2f",
                "knop_special_fg": "#ffffff",
                "border": "#555555",
                "text": "#ffffff",
                "text_secondary": "#cccccc"
            }
        else:  # light theme
            return {
                "main_bg": "#f5f5f5",
                "bg": "#ffffff",
                "fg": "#000000",
                "accent": "#007acc",
                "knop": "#e0e0e0",
                "knop_fg": "#000000",
                "knop_start": "#4caf50",
                "knop_stop": "#d32f2f",
                "knop_delete_all": "#d32f2f",
                "knop_special_fg": "#ffffff",
                "border": "#cccccc",
                "text": "#000000",
                "text_secondary": "#666666"
            }
    
    def apply_theme(self, app: QApplication, theme_name: str) -> None:
        """Pas een thema toe op de hele applicatie"""
        self.current_theme = theme_name
        self.colors = self._get_theme_colors(theme_name)
        
        # Sla thema op in configuratie
        config_mgr = _get_config_manager()
        if config_mgr:
            config_mgr.set("theme", theme_name)
            config_mgr.save_configuration()
        
        # Pas thema toe op applicatie
        self._apply_theme_to_app(app)
        
        print(f"🎨 PyQt6 Thema '{theme_name}' toegepast")
    
    def _apply_theme_to_app(self, app: QApplication) -> None:
        """Pas thema toe op QApplication"""
        palette = QPalette()
        
        if self.current_theme == "dark":
            # Dark theme kleuren
            palette.setColor(QPalette.ColorRole.Window, QColor(self.colors["main_bg"]))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(self.colors["fg"]))
            palette.setColor(QPalette.ColorRole.Base, QColor(self.colors["bg"]))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(self.colors["main_bg"]))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(self.colors["bg"]))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor(self.colors["fg"]))
            palette.setColor(QPalette.ColorRole.Text, QColor(self.colors["text"]))
            palette.setColor(QPalette.ColorRole.Button, QColor(self.colors["knop"]))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(self.colors["knop_fg"]))
            palette.setColor(QPalette.ColorRole.Link, QColor(self.colors["accent"]))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(self.colors["accent"]))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(self.colors["knop_special_fg"]))
        else:
            # Light theme kleuren
            palette.setColor(QPalette.ColorRole.Window, QColor(self.colors["main_bg"]))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(self.colors["fg"]))
            palette.setColor(QPalette.ColorRole.Base, QColor(self.colors["bg"]))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(self.colors["main_bg"]))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(self.colors["bg"]))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor(self.colors["fg"]))
            palette.setColor(QPalette.ColorRole.Text, QColor(self.colors["text"]))
            palette.setColor(QPalette.ColorRole.Button, QColor(self.colors["knop"]))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(self.colors["knop_fg"]))
            palette.setColor(QPalette.ColorRole.Link, QColor(self.colors["accent"]))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(self.colors["accent"]))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(self.colors["knop_special_fg"]))
        
        app.setPalette(palette)
    
    def get_colors(self, theme_name: Optional[str] = None) -> Dict[str, str]:
        """Krijg kleuren voor een thema"""
        if theme_name is None:
            theme_name = self.current_theme
        return self._get_theme_colors(theme_name)
    
    def get_available_themes(self) -> list:
        """Krijg beschikbare thema's"""
        return ["dark", "light"]
    
    def get_current_theme(self) -> str:
        """Krijg huidige thema"""
        return self.current_theme 