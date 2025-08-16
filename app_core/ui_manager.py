"""
UI Manager voor Magic Time Studio PySide6
Beheert alle UI-gerelateerde functionaliteit
"""

import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon

class UIManager:
    """Beheert alle UI-gerelateerde functionaliteit"""
    
    def __init__(self, main_app):
        self.main_app = main_app
        self.app = None
        self.main_window = None
        self.theme_manager = None
        
    def create_ui(self):
        """Maak de PySide6 gebruikersinterface"""
        print("🎨 PySide6 UI wordt aangemaakt...")
        
        # Maak QApplication
        self._create_qapplication()
        
        # Stel icoon in
        self._set_application_icon()
        
        # Pas thema toe
        self._apply_theme()
        
        # Maak hoofdvenster
        if not self._create_main_window():
            return 1  # Stop de applicatie
        
        # Connect signals
        self._connect_signals()
        
        # Stel taakbalk icoon in
        self.setTaskbarIcon()
        
        print("✅ PySide6 UI aangemaakt")
    
    def _create_qapplication(self):
        """Maak QApplication aan"""
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Magic Time Studio v3.0")
        self.app.setApplicationVersion("3.0")
        print("✅ QApplication aangemaakt")
    
    def _set_application_icon(self):
        """Stel applicatie icoon in"""
        try:
            # Bepaal project root (magic_time directory)
            project_root = r"d:\project\magic_time"
            possible_roots = [
                project_root,  # magic_time directory
            ]
            
            # Probeer verschillende icoon paden
            icon_paths = []
            for root in possible_roots:
                icon_paths.extend([
                    os.path.join(root, "assets", "Magic_Time_Studio_wit.ico"),
                    os.path.join(root, "assets", "Magic_Time_Studio.ico"),
                    os.path.join(root, "assets", "Magic_Time_Studio_wit.png"),
                ])
            
            # Debug: toon alle paden
            print(f"🔍 Zoek naar icoon bestanden in:")
            for path in icon_paths:
                print(f"   {path} - {'✅ Bestaat' if os.path.exists(path) else '❌ Niet gevonden'}")
            
            icon_set = False
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    self.app.setWindowIcon(QIcon(icon_path))
                    print(f"✅ Icoon ingesteld: {icon_path}")
                    icon_set = True
                    break
            
            if not icon_set:
                print("⚠️ Geen icoon bestand gevonden")
                
        except Exception as e:
            print(f"❌ Fout bij instellen icoon: {e}")
    
    def _apply_theme(self):
        """Pas thema toe"""
        if self.main_app.config_manager and self.main_app.theme_manager:
            try:
                theme = self.main_app.config_manager.get("theme", "dark")
                self.main_app.theme_manager.apply_theme(self.app, theme)
                print(f"✅ Thema toegepast: {theme}")
            except Exception as e:
                print(f"⚠️ Fout bij toepassen thema: {e}")
        else:
            print("⚠️ Configuratie of ThemeManager niet beschikbaar, geen thema toegepast")
    
    def _create_main_window(self):
        """Maak hoofdvenster aan"""
        if self.main_app.MainWindow:
            try:
                self.main_window = self.main_app.MainWindow()
                print("✅ Hoofdvenster aangemaakt")
                return True
            except Exception as e:
                print(f"❌ Fout bij aanmaken hoofdvenster: {e}")
                import traceback
                traceback.print_exc()
                return False
        else:
            print("❌ MainWindow niet geïnitialiseerd, applicatie zal niet werken")
            return False
    
    def _connect_signals(self):
        """Verbind alle signalen"""
        if self.main_window:
            self._connect_processing_signals()
            self._connect_file_signals()
        else:
            print("⚠️ main_window is None, geen signal connecties mogelijk")
    
    def _connect_processing_signals(self):
        """Verbind processing signalen"""
        try:
            self.main_window.main_processing_started.connect(self.main_app._on_start_processing)
            print("✅ main_processing_started signal verbonden")
        except Exception as e:
            print(f"⚠️ Fout bij verbinden main_processing_started: {e}")
    
    def _connect_file_signals(self):
        """Verbind bestand signalen"""
        try:
            self.main_window.main_file_selected.connect(self.main_app._on_file_selected)
            print("✅ main_file_selected signal verbonden")
        except Exception as e:
            print(f"⚠️ Fout bij verbinden main_file_selected: {e}")
    
    def setTaskbarIcon(self):
        """Stel taakbalk icoon in"""
        try:
            # Bepaal project root (magic_time directory)
            project_root = r"d:\project\magic_time"
            
            # Probeer verschillende icoon paden voor taakbalk
            icon_paths = [
                os.path.join(project_root, "assets", "Magic_Time_Studio_wit.ico"),  # magic_time/assets
                os.path.join(project_root, "assets", "Magic_Time_Studio.ico"),     # magic_time/assets
                os.path.join(project_root, "assets", "Magic_Time_Studio_wit.png"), # magic_time/assets
            ]
            
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    try:
                        # Stel icoon in voor de applicatie (dit beïnvloedt de taakbalk)
                        self.app.setWindowIcon(QIcon(icon_path))
                        print(f"✅ Taakbalk icoon ingesteld: {icon_path}")
                        return
                    except Exception as e:
                        print(f"⚠️ Fout bij instellen taakbalk icoon {icon_path}: {e}")
                        continue
            
            print("⚠️ Geen werkend icoon bestand gevonden voor taakbalk")
            
        except Exception as e:
            print(f"❌ Fout bij instellen taakbalk icoon: {e}")
    
    def show_main_window(self):
        """Toon hoofdvenster"""
        if self.main_window:
            try:
                self.main_window.show()
                print("✅ Hoofdvenster getoond")
                
                # Koppel monitors na het tonen van het venster
                self._connect_monitors()
                
                return True
            except Exception as e:
                print(f"❌ Fout bij tonen hoofdvenster: {e}")
                return False
        else:
            print("❌ main_window is None, applicatie zal niet tonen")
            return False
    
    def _connect_monitors(self):
        """Verbind monitors aan het hoofdvenster"""
        try:
            if hasattr(self.main_window, 'connect_monitors'):
                self.main_window.connect_monitors()
            else:
                print("⚠️ connect_monitors methode niet beschikbaar in main_window")
        except Exception as e:
            print(f"⚠️ Fout bij koppelen GPU monitor: {e}")
