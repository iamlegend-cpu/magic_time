"""
Interface instellingen tab
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QGroupBox, QComboBox, QSpinBox, QCheckBox
)

from magic_time_studio.core.config import config_manager

class InterfaceTab(QWidget):
    """Interface instellingen tab"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup de UI"""
        layout = QVBoxLayout(self)
        
        # Panel zichtbaarheid
        panels_group = QGroupBox("👁️ Panel Zichtbaarheid")
        panels_layout = QVBoxLayout(panels_group)
        
        self.settings_panel_check = QCheckBox("⚙️ Instellingen Panel")
        panels_layout.addWidget(self.settings_panel_check)
        
        self.files_panel_check = QCheckBox("📁 Bestanden Panel")
        panels_layout.addWidget(self.files_panel_check)
        
        self.processing_panel_check = QCheckBox("⚙️ Verwerking Panel")
        panels_layout.addWidget(self.processing_panel_check)
        
        self.charts_panel_check = QCheckBox("📊 Grafieken Panel")
        panels_layout.addWidget(self.charts_panel_check)
        
        self.batch_panel_check = QCheckBox("📦 Batch Panel")
        panels_layout.addWidget(self.batch_panel_check)
        
        layout.addWidget(panels_group)
        
        # UI instellingen
        ui_group = QGroupBox("🎨 UI Instellingen")
        ui_layout = QVBoxLayout(ui_group)
        
        # Window grootte (gebruiksvriendelijk)
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("🖥️ Standaard Window Grootte:"))
        
        self.window_size_combo = QComboBox()
        self.window_size_combo.addItems([
            "Klein (800×600)",
            "Gemiddeld (1200×800)", 
            "Groot (1600×900)",
            "Extra Groot (1920×1080)",
            "Automatisch (aanpassen aan scherm)"
        ])
        self.window_size_combo.currentTextChanged.connect(self.on_window_size_changed)
        size_layout.addWidget(self.window_size_combo)
        
        ui_layout.addLayout(size_layout)
        
        # Splitter posities
        splitter_layout = QHBoxLayout()
        splitter_layout.addWidget(QLabel("✂️ Splitter Posities:"))
        
        self.splitter1_spin = QSpinBox()
        self.splitter1_spin.setRange(100, 800)
        self.splitter1_spin.setValue(300)
        self.splitter1_spin.setSuffix(" px")
        splitter_layout.addWidget(self.splitter1_spin)
        
        self.splitter2_spin = QSpinBox()
        self.splitter2_spin.setRange(100, 800)
        self.splitter2_spin.setValue(600)
        self.splitter2_spin.setSuffix(" px")
        splitter_layout.addWidget(self.splitter2_spin)
        
        ui_layout.addLayout(splitter_layout)
        
        layout.addWidget(ui_group)
    
    def on_window_size_changed(self, size_text: str):
        """Handle window size change"""
        print(f"🖥️ Window grootte gewijzigd naar: {size_text}")
        
        # Map size text naar pixel waarden
        size_mapping = {
            "Klein (800×600)": (800, 600),
            "Gemiddeld (1200×800)": (1200, 800),
            "Groot (1600×900)": (1600, 900),
            "Extra Groot (1920×1080)": (1920, 1080),
            "Automatisch (aanpassen aan scherm)": (0, 0)  # 0 betekent automatisch
        }
        
        width, height = size_mapping.get(size_text, (1200, 800))
        config_manager.set("window_width", width)
        config_manager.set("window_height", height)
    
    def load_configuration(self):
        """Laad configuratie"""
        try:
            # Panel zichtbaarheid
            visible_panels = config_manager.get_visible_panels()
            self.settings_panel_check.setChecked(visible_panels.get("settings", True))
            self.files_panel_check.setChecked(visible_panels.get("files", True))
            self.processing_panel_check.setChecked(visible_panels.get("processing", True))
            self.charts_panel_check.setChecked(visible_panels.get("charts", True))
            self.batch_panel_check.setChecked(visible_panels.get("batch", True))
            
            # UI instellingen
            default_window_size = config_manager.get("DEFAULT_WINDOW_SIZE", "Gemiddeld (1200×800)")
            self.window_size_combo.setCurrentText(default_window_size)
            self.splitter1_spin.setValue(int(config_manager.get("SPLITTER1_POS", "300")))
            self.splitter2_spin.setValue(int(config_manager.get("SPLITTER2_POS", "600")))
            
        except Exception as e:
            print(f"❌ Fout bij laden interface configuratie: {e}")
    
    def save_configuration(self):
        """Sla configuratie op"""
        try:
            # Panel zichtbaarheid
            config_manager.set_panel_visibility("settings", self.settings_panel_check.isChecked())
            config_manager.set_panel_visibility("files", self.files_panel_check.isChecked())
            config_manager.set_panel_visibility("processing", self.processing_panel_check.isChecked())
            config_manager.set_panel_visibility("charts", self.charts_panel_check.isChecked())
            config_manager.set_panel_visibility("batch", self.batch_panel_check.isChecked())
            
            # Window grootte (gebruiksvriendelijk)
            window_size_text = self.window_size_combo.currentText()
            size_mapping = {
                "Klein (800×600)": (800, 600),
                "Gemiddeld (1200×800)": (1200, 800),
                "Groot (1600×900)": (1600, 900),
                "Extra Groot (1920×1080)": (1920, 1080),
                "Automatisch (aanpassen aan scherm)": (0, 0)
            }
            width, height = size_mapping.get(window_size_text, (1200, 800))
            config_manager.set("window_width", width)
            config_manager.set("window_height", height)
            config_manager.set("DEFAULT_WINDOW_SIZE", window_size_text)
            
            # Splitter posities
            config_manager.set("SPLITTER1_POS", str(self.splitter1_spin.value()))
            config_manager.set("SPLITTER2_POS", str(self.splitter2_spin.value()))
            
        except Exception as e:
            print(f"❌ Fout bij opslaan interface configuratie: {e}")
