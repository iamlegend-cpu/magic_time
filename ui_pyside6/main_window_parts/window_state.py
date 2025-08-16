"""
Window State Mixin voor MainWindow
Bevat alle window state gerelateerde functies
"""

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMainWindow, QMessageBox, QApplication
from PySide6.QtGui import QIcon
import os

# Lazy import van config_manager om circulaire import te voorkomen
def _get_config_manager():
    """Lazy config manager import om circulaire import te voorkomen"""
    try:
        from ...core.config import config_manager
        return config_manager
    except ImportError:
        try:
            from core.config import config_manager
            return config_manager
        except ImportError:
            return None

class WindowStateMixin:
    """Mixin voor window state functionaliteit"""
    
    def closeEvent(self, event):
        """Venster sluiten"""
        if self.processing_active:
            reply = QMessageBox.question(
                self, "Bevestig afsluiten",
                "Verwerking is nog actief. Weet je zeker dat je wilt afsluiten?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                event.ignore()
                return
        
        # Sla window state op voordat we sluiten
        try:
            self.save_window_state()
        except Exception as e:
            print(f"⚠️ Kon window state niet opslaan: {e}")
        
        event.accept()
    
    def changeEvent(self, event):
        """Handle window state changes"""
        if event.type() == event.Type.WindowStateChange:
            # Als window wordt gerestaureerd, zorg ervoor dat het binnen scherm blijft
            if not self.isMaximized():
                self.ensure_window_on_screen()
        # Let op: super().changeEvent(event) wordt niet aangeroepen in mixin context
        # De hoofdklasse zal dit zelf afhandelen
    
    def ensure_window_on_screen(self):
        """Zorg ervoor dat window binnen scherm blijft"""
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.geometry()
        
        # Controleer of window buiten scherm is
        if window_geometry.right() > screen_geometry.right():
            window_geometry.moveRight(screen_geometry.right())
        if window_geometry.bottom() > screen_geometry.bottom():
            window_geometry.moveBottom(screen_geometry.bottom())
        if window_geometry.left() < screen_geometry.left():
            window_geometry.moveLeft(screen_geometry.left())
        if window_geometry.top() < screen_geometry.top():
            window_geometry.moveTop(screen_geometry.top())
        
        # Als window te groot is, pas grootte aan
        if window_geometry.width() > screen_geometry.width():
            window_geometry.setWidth(screen_geometry.width())
        if window_geometry.height() > screen_geometry.height():
            window_geometry.setHeight(screen_geometry.height())
        
        # Pas geometrie toe als er iets is veranderd
        if window_geometry != self.geometry():
            self.setGeometry(window_geometry)
    
    def save_window_state(self):
        """Sla window state op"""
        geometry = self.geometry()
        is_maximized = self.isMaximized()
        
        config_mgr = _get_config_manager()
        if config_mgr:
            config_mgr.set_json("window_geometry", {
                "x": geometry.x(),
                "y": geometry.y(),
                "width": geometry.width(),
                "height": geometry.height(),
                "maximized": is_maximized
            })
            config_mgr.save_configuration()
    
    def restore_window_state(self):
        """Herstel window state"""
        try:
            config_mgr = _get_config_manager()
            geometry_data = config_mgr.get_json("window_geometry", {}) if config_mgr else {}
            if geometry_data:
                x = geometry_data.get("x", 100)
                y = geometry_data.get("y", 100)
                width = geometry_data.get("width", 1200)
                height = geometry_data.get("height", 800)
                maximized = geometry_data.get("maximized", True)
                
                # Controleer of window binnen scherm past
                screen = QApplication.primaryScreen()
                screen_geometry = screen.availableGeometry()
                
                # Pas positie aan als nodig
                if x + width > screen_geometry.right():
                    x = screen_geometry.right() - width
                if y + height > screen_geometry.bottom():
                    y = screen_geometry.bottom() - height
                if x < screen_geometry.left():
                    x = screen_geometry.left()
                if y < screen_geometry.top():
                    y = screen_geometry.top()
                
                self.setGeometry(x, y, width, height)
                
                if maximized:
                    self.showMaximized()
                else:
                    self.showNormal()
        except Exception as e:
            print(f"❌ Fout bij herstellen window state: {e}")
            # Fallback naar standaard gedrag
            self.showMaximized() 