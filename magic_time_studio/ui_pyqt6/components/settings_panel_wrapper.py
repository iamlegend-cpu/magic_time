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