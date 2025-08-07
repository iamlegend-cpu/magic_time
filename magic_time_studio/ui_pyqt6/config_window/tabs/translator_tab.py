"""
Vertaler instellingen tab
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QGroupBox, QLineEdit, QSpinBox
)

from magic_time_studio.core.config import config_manager

class TranslatorTab(QWidget):
    """Vertaler instellingen tab"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup de UI"""
        layout = QVBoxLayout(self)
        
        # LibreTranslate instellingen
        libretranslate_group = QGroupBox("🌐 LibreTranslate Instellingen")
        libretranslate_layout = QVBoxLayout(libretranslate_group)
        
        # Server URL
        server_layout = QHBoxLayout()
        server_layout.addWidget(QLabel("🌍 Server URL:"))
        
        self.server_edit = QLineEdit()
        self.server_edit.setPlaceholderText("bijv. localhost:5000")
        server_layout.addWidget(self.server_edit)
        
        libretranslate_layout.addLayout(server_layout)
        
        # Timeout
        timeout_layout = QHBoxLayout()
        timeout_layout.addWidget(QLabel("⏱️ Timeout (seconden):"))
        
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(5, 120)
        self.timeout_spin.setValue(30)
        timeout_layout.addWidget(self.timeout_spin)
        
        libretranslate_layout.addLayout(timeout_layout)
        
        # Rate limit
        rate_layout = QHBoxLayout()
        rate_layout.addWidget(QLabel("🚦 Rate Limit (0 = uit):"))
        
        self.rate_limit_spin = QSpinBox()
        self.rate_limit_spin.setRange(0, 1000)
        self.rate_limit_spin.setValue(0)
        rate_layout.addWidget(self.rate_limit_spin)
        
        libretranslate_layout.addLayout(rate_layout)
        
        # Max characters
        max_chars_layout = QHBoxLayout()
        max_chars_layout.addWidget(QLabel("📏 Max Karakters:"))
        
        self.max_chars_spin = QSpinBox()
        self.max_chars_spin.setRange(1000, 50000)
        self.max_chars_spin.setValue(10000)
        max_chars_layout.addWidget(self.max_chars_spin)
        
        libretranslate_layout.addLayout(max_chars_layout)
        
        layout.addWidget(libretranslate_group)
    
    def load_configuration(self):
        """Laad configuratie"""
        try:
            # LibreTranslate instellingen
            self.server_edit.setText(config_manager.get("LIBRETRANSLATE_SERVER", ""))
            self.timeout_spin.setValue(int(config_manager.get("LIBRETRANSLATE_TIMEOUT", "30")))
            self.rate_limit_spin.setValue(int(config_manager.get("LIBRETRANSLATE_RATE_LIMIT", "0")))
            self.max_chars_spin.setValue(int(config_manager.get("LIBRETRANSLATE_MAX_CHARS", "10000")))
            
        except Exception as e:
            print(f"❌ Fout bij laden vertaler configuratie: {e}")
    
    def save_configuration(self):
        """Sla configuratie op"""
        try:
            # LibreTranslate instellingen
            config_manager.set("LIBRETRANSLATE_SERVER", self.server_edit.text())
            config_manager.set("LIBRETRANSLATE_TIMEOUT", str(self.timeout_spin.value()))
            config_manager.set("LIBRETRANSLATE_RATE_LIMIT", str(self.rate_limit_spin.value()))
            config_manager.set("LIBRETRANSLATE_MAX_CHARS", str(self.max_chars_spin.value()))
            
        except Exception as e:
            print(f"❌ Fout bij opslaan vertaler configuratie: {e}")
