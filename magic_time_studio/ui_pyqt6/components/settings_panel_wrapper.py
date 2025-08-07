"""
Settings Panel Wrapper voor Magic Time Studio
"""

import os
import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QScrollArea, QGroupBox
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor

from magic_time_studio.ui_pyqt6.components.settings_panel import SettingsPanel

class SettingsPanelWrapper(QWidget):
    """Wrapper voor settings panel"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings_panel = SettingsPanel()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup de UI"""
        layout = QVBoxLayout(self)
        
        settings_group = QGroupBox("⚙️ Instellingen")
        settings_layout = QVBoxLayout(settings_group)
        settings_layout.addWidget(self.settings_panel)
        layout.addWidget(settings_group)
    
    def freeze_settings(self):
        """Bevries alle instellingen tijdens verwerking"""
        self.settings_panel.freeze_settings()
    
    def unfreeze_settings(self):
        """Ontdooi alle instellingen na verwerking"""
        self.settings_panel.unfreeze_settings()
    
    def is_frozen(self) -> bool:
        """Controleer of settings bevroren zijn"""
        return self.settings_panel.is_frozen()
    
    def get_current_settings(self) -> dict:
        """Haal huidige instellingen op"""
        return self.settings_panel.get_current_settings()
    
    def update_translator_status(self):
        """Update vertaler status"""
        self.settings_panel.update_translator_status() 