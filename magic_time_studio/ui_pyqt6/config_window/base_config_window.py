"""
Basis configuratie venster voor Magic Time Studio
"""

import os
from PyQt6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QTabWidget, QMessageBox
)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QShowEvent

from core.config import config_manager

# Import alle tab modules
from .tabs.general_tab import GeneralTab
from .tabs.processing_tab import ProcessingTab
from .tabs.translator_tab import TranslatorTab
from .tabs.interface_tab import InterfaceTab
from .tabs.theme_tab import ThemeTab
from .tabs.advanced_tab import AdvancedTab
from .tabs.plugins_tab import PluginsTab

class ConfigWindow(QDialog):
    """Configuratie venster"""
    
    config_saved = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("⚙️ Magic Time Studio - Configuratie")
        
        # Start in een redelijke grootte, maar niet te groot
        self.setGeometry(200, 200, 900, 700)
        self.setMinimumSize(800, 600)
        
        self.callback = None
        
        # Sla alle verwerking-gerelateerde UI elementen op
        self.processing_ui_elements = []
        
        # Maak tab instances
        self.tabs = {}
        
        self.setup_ui()
        # Laad configuratie niet automatisch - wordt gedaan wanneer venster wordt getoond
    
    def set_callback(self, callback):
        """Stel callback functie in voor configuratie opslaan"""
        self.callback = callback
    
    def setup_ui(self):
        """Setup de UI"""
        layout = QVBoxLayout(self)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Maak alle tabs aan
        self.create_tabs()
        
        # Knoppen
        button_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("💾 Opslaan")
        self.save_btn.clicked.connect(self.save_configuration)
        button_layout.addWidget(self.save_btn)
        
        self.cancel_btn = QPushButton("❌ Annuleren")
        self.cancel_btn.clicked.connect(self.close)
        button_layout.addWidget(self.cancel_btn)
        
        self.reset_btn = QPushButton("🔄 Reset naar Standaard")
        self.reset_btn.clicked.connect(self.reset_to_defaults)
        button_layout.addWidget(self.reset_btn)
        
        layout.addLayout(button_layout)
    
    def create_tabs(self):
        """Maak alle tabs aan"""
        # Tab 1: Algemene instellingen
        self.tabs['general'] = GeneralTab()
        self.tab_widget.addTab(self.tabs['general'], "🔧 Algemeen")
        
        # Tab 2: Verwerking instellingen
        self.tabs['processing'] = ProcessingTab()
        self.tab_widget.addTab(self.tabs['processing'], "⚙️ Verwerking")
        
        # Tab 3: Vertaler instellingen
        self.tabs['translator'] = TranslatorTab()
        self.tab_widget.addTab(self.tabs['translator'], "🌐 Vertaler")
        
        # Tab 4: Interface instellingen
        self.tabs['interface'] = InterfaceTab()
        self.tab_widget.addTab(self.tabs['interface'], "👁️ Interface")
        
        # Tab 5: Thema instellingen
        self.tabs['theme'] = ThemeTab()
        self.tab_widget.addTab(self.tabs['theme'], "🎨 Thema")
        
        # Tab 6: Geavanceerde instellingen
        self.tabs['advanced'] = AdvancedTab()
        self.tab_widget.addTab(self.tabs['advanced'], "🔧 Geavanceerd")
        
        # Tab 7: Plugin beheer
        self.tabs['plugins'] = PluginsTab()
        self.tab_widget.addTab(self.tabs['plugins'], "🔌 Plugins")
    
    def load_configuration(self):
        """Laad huidige configuratie"""
        try:
            # Laad configuratie voor alle tabs
            for tab_name, tab in self.tabs.items():
                if hasattr(tab, 'load_configuration'):
                    tab.load_configuration()
            
            print("✅ Configuratie geladen")
            
        except Exception as e:
            print(f"❌ Fout bij laden configuratie: {e}")
    
    def showEvent(self, event: QShowEvent):
        """Event dat wordt aangeroepen wanneer het venster wordt getoond"""
        super().showEvent(event)
        # Laad configuratie wanneer venster wordt getoond
        self.load_configuration()
    
    def save_configuration(self):
        """Sla configuratie op"""
        try:
            # Sla configuratie op voor alle tabs
            for tab_name, tab in self.tabs.items():
                tab.save_configuration()
            
            # Sla configuratie op
            config_manager.save_configuration()
            
            # Emit signal
            self.config_saved.emit()
            
            # Roep callback aan als deze is ingesteld
            if self.callback:
                self.callback()
            
            QMessageBox.information(self, "✅ Succes", "Configuratie opgeslagen!")
            print("✅ Configuratie opgeslagen")
            
        except Exception as e:
            QMessageBox.critical(self, "❌ Fout", f"Fout bij opslaan configuratie: {e}")
            print(f"❌ Fout bij opslaan configuratie: {e}")
    
    def reset_to_defaults(self):
        """Reset naar standaard instellingen"""
        reply = QMessageBox.question(
            self, "🔄 Reset", 
            "Weet je zeker dat je alle instellingen wilt resetten naar standaard?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            config_manager.reset_to_defaults()
            self.load_configuration()
            QMessageBox.information(self, "✅ Reset", "Instellingen gereset naar standaard!")
