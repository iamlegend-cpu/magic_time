"""
Moderne styling voor PyQt6 applicatie
"""

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QTimer
from PyQt6.QtGui import QPalette, QColor, QFont

class ModernStyling:
    """Moderne styling manager"""
    
    def __init__(self):
        self.current_theme = "dark"
        self.available_themes = {
            "dark": self.get_dark_theme(),
            "light": self.get_light_theme(),
            "blue": self.get_blue_theme(),
            "green": self.get_green_theme(),
            "purple": self.get_purple_theme(),
            "orange": self.get_orange_theme(),
            "cyber": self.get_cyber_theme()
        }
    
    def get_dark_theme(self) -> dict:
        """Dark theme kleuren"""
        return {
            "bg": "#1e1e1e",
            "fg": "#ffffff",
            "accent": "#404040",
            "frame": "#2d2d2d",
            "knop": "#505050",
            "knop_fg": "#ffffff",
            "main_bg": "#252525",
            "panel_bg": "#303030",
            "knop_start": "#4caf50",
            "knop_stop": "#d32f2f",
            "knop_delete_all": "#d32f2f",
            "knop_special_fg": "#ffffff",
            "text_primary": "#ffffff",
            "text_secondary": "#b0b0b0",
            "border": "#555555",
            "hover": "#404040",
            "selection": "#2196f3"
        }
    
    def get_light_theme(self) -> dict:
        """Light theme kleuren"""
        return {
            "bg": "#f5f5f5",
            "fg": "#000000",
            "accent": "#e0e0e0",
            "frame": "#ffffff",
            "knop": "#f0f0f0",
            "knop_fg": "#000000",
            "main_bg": "#ffffff",
            "panel_bg": "#fafafa",
            "knop_start": "#4caf50",
            "knop_stop": "#d32f2f",
            "knop_delete_all": "#d32f2f",
            "knop_special_fg": "#ffffff",
            "text_primary": "#000000",
            "text_secondary": "#666666",
            "border": "#cccccc",
            "hover": "#e0e0e0",
            "selection": "#2196f3"
        }
    
    def get_blue_theme(self) -> dict:
        """Blue theme kleuren"""
        return {
            "bg": "#1a237e",
            "fg": "#ffffff",
            "accent": "#3949ab",
            "frame": "#283593",
            "knop": "#3f51b5",
            "knop_fg": "#ffffff",
            "main_bg": "#0d47a1",
            "panel_bg": "#1565c0",
            "knop_start": "#4caf50",
            "knop_stop": "#d32f2f",
            "knop_delete_all": "#d32f2f",
            "knop_special_fg": "#ffffff",
            "text_primary": "#ffffff",
            "text_secondary": "#b3e5fc",
            "border": "#3949ab",
            "hover": "#3949ab",
            "selection": "#64b5f6"
        }
    
    def get_green_theme(self) -> dict:
        """Green theme kleuren"""
        return {
            "bg": "#1b5e20",
            "fg": "#ffffff",
            "accent": "#2e7d32",
            "frame": "#388e3c",
            "knop": "#4caf50",
            "knop_fg": "#ffffff",
            "main_bg": "#0d4f14",
            "panel_bg": "#1565c0",
            "knop_start": "#4caf50",
            "knop_stop": "#d32f2f",
            "knop_delete_all": "#d32f2f",
            "knop_special_fg": "#ffffff",
            "text_primary": "#ffffff",
            "text_secondary": "#a5d6a7",
            "border": "#2e7d32",
            "hover": "#2e7d32",
            "selection": "#66bb6a"
        }
    
    def get_purple_theme(self) -> dict:
        """Purple theme kleuren"""
        return {
            "bg": "#4a148c",
            "fg": "#ffffff",
            "accent": "#6a1b9a",
            "frame": "#7b1fa2",
            "knop": "#8e24aa",
            "knop_fg": "#ffffff",
            "main_bg": "#311b92",
            "panel_bg": "#4527a0",
            "knop_start": "#4caf50",
            "knop_stop": "#d32f2f",
            "knop_delete_all": "#d32f2f",
            "knop_special_fg": "#ffffff",
            "text_primary": "#ffffff",
            "text_secondary": "#ce93d8",
            "border": "#6a1b9a",
            "hover": "#6a1b9a",
            "selection": "#ab47bc"
        }
    
    def get_orange_theme(self) -> dict:
        """Orange theme kleuren"""
        return {
            "bg": "#e65100",
            "fg": "#ffffff",
            "accent": "#f57c00",
            "frame": "#ff8f00",
            "knop": "#ff9800",
            "knop_fg": "#ffffff",
            "main_bg": "#bf360c",
            "panel_bg": "#d84315",
            "knop_start": "#4caf50",
            "knop_stop": "#d32f2f",
            "knop_delete_all": "#d32f2f",
            "knop_special_fg": "#ffffff",
            "text_primary": "#ffffff",
            "text_secondary": "#ffcc02",
            "border": "#f57c00",
            "hover": "#f57c00",
            "selection": "#ffb74d"
        }
    
    def get_cyber_theme(self) -> dict:
        """Cyber theme kleuren"""
        return {
            "bg": "#0a0a0a",
            "fg": "#00ff00",
            "accent": "#1a1a1a",
            "frame": "#2a2a2a",
            "knop": "#3a3a3a",
            "knop_fg": "#00ff00",
            "main_bg": "#000000",
            "panel_bg": "#1a1a1a",
            "knop_start": "#00ff00",
            "knop_stop": "#ff0000",
            "knop_delete_all": "#ff0000",
            "knop_special_fg": "#000000",
            "text_primary": "#00ff00",
            "text_secondary": "#00cc00",
            "border": "#00ff00",
            "hover": "#00cc00",
            "selection": "#00ff00"
        }
    
    def apply_theme(self, app: QApplication, theme_name: str):
        """Pas thema toe op applicatie"""
        if theme_name not in self.available_themes:
            theme_name = "dark"
        
        self.current_theme = theme_name
        theme = self.available_themes[theme_name]
        
        # Stel palette in
        palette = QPalette()
        
        # Window
        palette.setColor(QPalette.ColorRole.Window, QColor(theme["bg"]))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(theme["fg"]))
        
        # Base
        palette.setColor(QPalette.ColorRole.Base, QColor(theme["main_bg"]))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(theme["panel_bg"]))
        
        # Text
        palette.setColor(QPalette.ColorRole.Text, QColor(theme["text_primary"]))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(theme["text_secondary"]))
        
        # Button
        palette.setColor(QPalette.ColorRole.Button, QColor(theme["knop"]))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(theme["knop_fg"]))
        
        # Highlight
        palette.setColor(QPalette.ColorRole.Highlight, QColor(theme["selection"]))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(theme["fg"]))
        
        # Link
        palette.setColor(QPalette.ColorRole.Link, QColor(theme["knop_start"]))
        palette.setColor(QPalette.ColorRole.LinkVisited, QColor(theme["knop_stop"]))
        
        app.setPalette(palette)
        
        # CSS styling
        css = self.get_css_style(theme)
        app.setStyleSheet(css)
        
        print(f"🎨 Thema '{theme_name}' toegepast")
    
    def get_css_style(self, theme: dict) -> str:
        """Genereer CSS styling"""
        return f"""
        /* Main Window */
        QMainWindow {{
            background-color: {theme["bg"]};
            color: {theme["fg"]};
        }}
        
        /* Widgets */
        QWidget {{
            background-color: {theme["bg"]};
            color: {theme["fg"]};
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 9pt;
        }}
        
        /* Buttons */
        QPushButton {{
            background-color: {theme["knop"]};
            color: {theme["knop_fg"]};
            border: 1px solid {theme["border"]};
            border-radius: 4px;
            padding: 6px 12px;
            font-weight: bold;
        }}
        
        QPushButton:hover {{
            background-color: {theme["hover"]};
        }}
        
        QPushButton:pressed {{
            background-color: {theme["accent"]};
        }}
        
        QPushButton[class="primary"] {{
            background-color: {theme["knop_start"]};
            color: {theme["knop_special_fg"]};
        }}
        
        QPushButton[class="danger"] {{
            background-color: {theme["knop_stop"]};
            color: {theme["knop_special_fg"]};
        }}
        
        /* Group Boxes */
        QGroupBox {{
            background-color: {theme["panel_bg"]};
            border: 2px solid {theme["border"]};
            border-radius: 6px;
            margin-top: 8px;
            padding-top: 8px;
            font-weight: bold;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 8px;
            padding: 0 4px 0 4px;
            color: {theme["text_primary"]};
        }}
        
        /* Labels */
        QLabel {{
            color: {theme["text_primary"]};
        }}
        
        /* Text Edit */
        QTextEdit {{
            background-color: {theme["main_bg"]};
            color: {theme["text_primary"]};
            border: 1px solid {theme["border"]};
            border-radius: 4px;
            padding: 4px;
        }}
        
        /* List Widget */
        QListWidget {{
            background-color: {theme["main_bg"]};
            color: {theme["text_primary"]};
            border: 1px solid {theme["border"]};
            border-radius: 4px;
            padding: 4px;
        }}
        
        QListWidget::item {{
            padding: 4px;
            border-radius: 2px;
        }}
        
        QListWidget::item:selected {{
            background-color: {theme["selection"]};
            color: {theme["fg"]};
        }}
        
        QListWidget::item:hover {{
            background-color: {theme["hover"]};
        }}
        
        /* Progress Bar */
        QProgressBar {{
            border: 1px solid {theme["border"]};
            border-radius: 4px;
            text-align: center;
            background-color: {theme["main_bg"]};
        }}
        
        QProgressBar::chunk {{
            background-color: {theme["knop_start"]};
            border-radius: 3px;
        }}
        
        /* Combo Box */
        QComboBox {{
            background-color: {theme["main_bg"]};
            color: {theme["text_primary"]};
            border: 1px solid {theme["border"]};
            border-radius: 4px;
            padding: 4px;
        }}
        
        QComboBox::drop-down {{
            border: none;
        }}
        
        QComboBox::down-arrow {{
            image: none;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 4px solid {theme["text_primary"]};
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {theme["main_bg"]};
            color: {theme["text_primary"]};
            border: 1px solid {theme["border"]};
            selection-background-color: {theme["selection"]};
        }}
        
        /* Spin Box */
        QSpinBox {{
            background-color: {theme["main_bg"]};
            color: {theme["text_primary"]};
            border: 1px solid {theme["border"]};
            border-radius: 4px;
            padding: 4px;
        }}
        
        /* Check Box */
        QCheckBox {{
            color: {theme["text_primary"]};
            spacing: 8px;
        }}
        
        QCheckBox::indicator {{
            width: 16px;
            height: 16px;
            border: 1px solid {theme["border"]};
            border-radius: 2px;
            background-color: {theme["main_bg"]};
        }}
        
        QCheckBox::indicator:checked {{
            background-color: {theme["knop_start"]};
        }}
        
        /* Tab Widget */
        QTabWidget::pane {{
            border: 1px solid {theme["border"]};
            background-color: {theme["bg"]};
        }}
        
        QTabBar::tab {{
            background-color: {theme["panel_bg"]};
            color: {theme["text_primary"]};
            padding: 8px 16px;
            margin-right: 2px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }}
        
        QTabBar::tab:selected {{
            background-color: {theme["bg"]};
            border-bottom: 2px solid {theme["knop_start"]};
        }}
        
        QTabBar::tab:hover {{
            background-color: {theme["hover"]};
        }}
        
        /* Table Widget */
        QTableWidget {{
            background-color: {theme["main_bg"]};
            color: {theme["text_primary"]};
            border: 1px solid {theme["border"]};
            gridline-color: {theme["border"]};
        }}
        
        QTableWidget::item {{
            padding: 4px;
        }}
        
        QTableWidget::item:selected {{
            background-color: {theme["selection"]};
        }}
        
        QHeaderView::section {{
            background-color: {theme["panel_bg"]};
            color: {theme["text_primary"]};
            padding: 4px;
            border: 1px solid {theme["border"]};
        }}
        
        /* Scroll Bar */
        QScrollBar:vertical {{
            background-color: {theme["main_bg"]};
            width: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {theme["knop"]};
            border-radius: 6px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {theme["hover"]};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        /* Menu Bar */
        QMenuBar {{
            background-color: {theme["panel_bg"]};
            color: {theme["text_primary"]};
            border-bottom: 1px solid {theme["border"]};
        }}
        
        QMenuBar::item {{
            padding: 6px 12px;
        }}
        
        QMenuBar::item:selected {{
            background-color: {theme["selection"]};
        }}
        
        QMenu {{
            background-color: {theme["main_bg"]};
            color: {theme["text_primary"]};
            border: 1px solid {theme["border"]};
            padding: 4px;
        }}
        
        QMenu::item {{
            padding: 6px 24px;
        }}
        
        QMenu::item:selected {{
            background-color: {theme["selection"]};
        }}
        
        /* Status Bar */
        QStatusBar {{
            background-color: {theme["panel_bg"]};
            color: {theme["text_primary"]};
            border-top: 1px solid {theme["border"]};
        }}
        
        /* Splitter */
        QSplitter::handle {{
            background-color: {theme["border"]};
        }}
        
        QSplitter::handle:horizontal {{
            width: 2px;
        }}
        
        QSplitter::handle:vertical {{
            height: 2px;
        }}
        """
    
    def add_hover_animation(self, widget, duration: int = 200):
        """Voeg hover animatie toe aan widget"""
        animation = QPropertyAnimation(widget, b"geometry")
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        return animation
    
    def add_fade_animation(self, widget, start_opacity: float = 0.0, end_opacity: float = 1.0, duration: int = 300):
        """Voeg fade animatie toe aan widget"""
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setStartValue(start_opacity)
        animation.setEndValue(end_opacity)
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        return animation
    
    def add_slide_animation(self, widget, start_pos: tuple, end_pos: tuple, duration: int = 300):
        """Voeg slide animatie toe aan widget"""
        animation = QPropertyAnimation(widget, b"pos")
        animation.setStartValue(start_pos)
        animation.setEndValue(end_pos)
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.Type.OutBack)
        return animation
    
    def get_available_themes(self) -> list:
        """Krijg beschikbare thema's"""
        return list(self.available_themes.keys())
    
    def get_current_theme(self) -> str:
        """Krijg huidige thema"""
        return self.current_theme 