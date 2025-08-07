"""
Window Setup Mixin voor MainWindow
Bevat alle window setup en configuratie functies
"""

import os
from PyQt6.QtWidgets import QMainWindow, QApplication, QStatusBar
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIcon
from magic_time_studio.core.config import config_manager

class WindowSetupMixin:
    """Mixin voor window setup functionaliteit"""
    
    def setup_window(self):
        """Setup het hoofdvenster"""
        self.setWindowTitle("Magic Time Studio v3.0 - PyQt6")
        
        # Stel minimum grootte in
        self.setMinimumSize(1200, 800)
        
        # Probeer window state te herstellen, anders gebruik standaard
        try:
            self.restore_window_state()
        except Exception as e:
            print(f"⚠️ Kon window state niet herstellen: {e}")
            # Fallback naar standaard setup
            screen = QApplication.primaryScreen()
            screen_geometry = screen.availableGeometry()
            
            # Bereken optimale window grootte (80% van scherm)
            window_width = int(screen_geometry.width() * 0.8)
            window_height = int(screen_geometry.height() * 0.8)
            
            # Centreer window op scherm
            x = (screen_geometry.width() - window_width) // 2
            y = (screen_geometry.height() - window_height) // 2
            
            # Stel window geometrie in
            self.setGeometry(x, y, window_width, window_height)
            self.showMaximized()
        
        # Zorg ervoor dat window zichtbaar is
        self.raise_()
        self.activateWindow()
        
        # Stel taakbalk icoon in na het tonen van het venster
        QTimer.singleShot(100, self.setTaskbarIcon)
        
        # Stel icoon in voor venster
        try:
            # Bepaal project root
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            
            # Probeer verschillende icoon paden
            icon_paths = [
                os.path.join(os.path.dirname(__file__), "..", "..", "..", "assets", "Magic_Time_Studio.ico"),
                os.path.join(os.path.dirname(__file__), "..", "..", "..", "assets", "Magic_Time_Studio_wit.ico"),
                os.path.join(project_root, "assets", "Magic_Time_Studio.ico"),
                os.path.join(project_root, "assets", "Magic_Time_Studio_wit.ico"),
                os.path.join(os.getcwd(), "assets", "Magic_Time_Studio.ico"),
                os.path.join(os.getcwd(), "assets", "Magic_Time_Studio_wit.ico"),
            ]
            
            icon_set = False
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    self.setWindowIcon(QIcon(icon_path))
                    print(f"✅ Venster icoon ingesteld: {icon_path}")
                    icon_set = True
                    break
            
            if not icon_set:
                print("⚠️ Geen icoon bestand gevonden voor venster")
            
            # Stel ook taakbalk icoon in
            self.setTaskbarIcon()
                
        except Exception as e:
            print(f"❌ Fout bij instellen venster icoon: {e}")
    
    def setTaskbarIcon(self):
        """Stel taakbalk icoon in"""
        try:
            # Bepaal project root
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            
            # Probeer verschillende icoon paden voor taakbalk
            icon_paths = [
                os.path.join(project_root, "assets", "Magic_Time_Studio_wit.ico"),
                os.path.join(project_root, "assets", "Magic_Time_Studio.ico"),
                os.path.join(os.path.dirname(__file__), "..", "..", "..", "assets", "Magic_Time_Studio_wit.ico"),
                os.path.join(os.path.dirname(__file__), "..", "..", "..", "assets", "Magic_Time_Studio.ico"),
                os.path.join(os.getcwd(), "assets", "Magic_Time_Studio_wit.ico"),
                os.path.join(os.getcwd(), "assets", "Magic_Time_Studio.ico"),
            ]
            
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    # Stel icoon in voor het venster (dit beïnvloedt de taakbalk)
                    self.setWindowIcon(QIcon(icon_path))
                    print(f"✅ Taakbalk icoon ingesteld: {icon_path}")
                    return
            
            print("⚠️ Geen icoon bestand gevonden voor taakbalk")
            
        except Exception as e:
            print(f"❌ Fout bij instellen taakbalk icoon: {e}")
    
    def create_status_bar(self):
        """Maak de statusbalk"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Klaar")
    
    def setup_timers(self):
        """Setup timers voor real-time updates"""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.periodic_update)
        self.update_timer.start(1000)
    
    def periodic_update(self):
        """Periodieke update functie"""
        # Verwijderd: update_translator_status() is niet meer beschikbaar
        pass 