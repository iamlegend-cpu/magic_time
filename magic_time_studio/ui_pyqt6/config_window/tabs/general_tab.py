"""
Algemene instellingen tab
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QGroupBox, QComboBox, QSpinBox, QCheckBox
)

from core.config import config_manager

class GeneralTab(QWidget):
    """Algemene instellingen tab"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup de UI"""
        layout = QVBoxLayout(self)
        
        # Basis instellingen
        general_group = QGroupBox("🔧 Algemene Instellingen")
        general_layout = QVBoxLayout(general_group)
        
        # Thema
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("🎨 Thema:"))
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["dark", "light", "blue", "green", "purple", "orange", "cyber"])
        theme_layout.addWidget(self.theme_combo)
        
        general_layout.addLayout(theme_layout)
        
        # Font grootte
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("📝 Font Grootte:"))
        
        self.font_spin = QSpinBox()
        self.font_spin.setRange(8, 16)
        self.font_spin.setValue(9)
        font_layout.addWidget(self.font_spin)
        
        general_layout.addLayout(font_layout)
        
        # Auto cleanup
        self.auto_cleanup_check = QCheckBox("🧹 Automatisch opschonen van tijdelijke bestanden")
        general_layout.addWidget(self.auto_cleanup_check)
        
        # Auto output directory
        self.auto_output_check = QCheckBox("📁 Automatisch output directory aanmaken")
        general_layout.addWidget(self.auto_output_check)
        
        layout.addWidget(general_group)
        
        # Logging instellingen
        logging_group = QGroupBox("📝 Logging Instellingen")
        logging_layout = QVBoxLayout(logging_group)
        
        # Log level
        log_level_layout = QHBoxLayout()
        log_level_layout.addWidget(QLabel("📊 Log Level:"))
        
        self.log_level_combo = QComboBox()
        self.log_level_combo.addItems(["DEBUG", "INFO", "WARNING", "ERROR"])
        log_level_layout.addWidget(self.log_level_combo)
        
        logging_layout.addLayout(log_level_layout)
        
        # Log naar bestand
        self.log_to_file_check = QCheckBox("📄 Log naar bestand")
        logging_layout.addWidget(self.log_to_file_check)
        
        layout.addWidget(logging_group)
    
    def load_configuration(self):
        """Laad configuratie"""
        try:
            # Algemene instellingen
            self.theme_combo.setCurrentText(config_manager.get("DEFAULT_THEME", "dark"))
            
            # Font grootte
            font_size = config_manager.get_int("DEFAULT_FONT_SIZE", 9)
            self.font_spin.setValue(font_size)
            
            # Boolean instellingen
            auto_cleanup = config_manager.get_bool("AUTO_CLEANUP_TEMP", True)
            self.auto_cleanup_check.setChecked(auto_cleanup)
            
            auto_output = config_manager.get_bool("AUTO_CREATE_OUTPUT_DIR", True)
            self.auto_output_check.setChecked(auto_output)
            
            # Logging
            self.log_level_combo.setCurrentText(config_manager.get("LOG_LEVEL", "INFO"))
            self.log_to_file_check.setChecked(config_manager.get("LOG_TO_FILE", "false").lower() == "true")
            
        except Exception as e:
            print(f"❌ Fout bij laden algemene configuratie: {e}")
    
    def save_configuration(self):
        """Sla configuratie op"""
        try:
            # Algemene instellingen
            config_manager.set("DEFAULT_THEME", self.theme_combo.currentText())
            config_manager.set("DEFAULT_FONT_SIZE", str(self.font_spin.value()))
            config_manager.set("AUTO_CLEANUP_TEMP", str(self.auto_cleanup_check.isChecked()).lower())
            config_manager.set("AUTO_CREATE_OUTPUT_DIR", str(self.auto_output_check.isChecked()).lower())
            
            # Logging
            config_manager.set("LOG_LEVEL", self.log_level_combo.currentText())
            config_manager.set("LOG_TO_FILE", str(self.log_to_file_check.isChecked()).lower())
            
        except Exception as e:
            print(f"❌ Fout bij opslaan algemene configuratie: {e}")
