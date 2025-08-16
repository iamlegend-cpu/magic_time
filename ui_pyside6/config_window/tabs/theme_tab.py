"""
Thema instellingen tab
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QGroupBox, QComboBox, QTextEdit, QLineEdit
)

from core.config import config_manager
from ...features.modern_styling import ModernStyling

class ThemeTab(QWidget):
    """Thema instellingen tab"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup de UI"""
        layout = QVBoxLayout(self)
        
        # Thema preview
        preview_group = QGroupBox("🎨 Thema Preview")
        preview_layout = QVBoxLayout(preview_group)
        
        self.theme_preview_label = QLabel("Selecteer een thema om een preview te zien")
        self.theme_preview_label.setStyleSheet("""
            QLabel {
                padding: 20px;
                border: 2px dashed #555555;
                border-radius: 8px;
                background-color: #1e1e1e;
                color: #ffffff;
                font-size: 12px;
            }
        """)
        preview_layout.addWidget(self.theme_preview_label)
        
        layout.addWidget(preview_group)
        
        # Thema opties
        theme_options_group = QGroupBox("🎨 Thema Opties")
        theme_options_layout = QVBoxLayout(theme_options_group)
        
        # Beschikbare thema's
        themes_layout = QHBoxLayout()
        themes_layout.addWidget(QLabel("🎨 Beschikbare Thema's:"))
        
        self.theme_selector_combo = QComboBox()
        self.theme_selector_combo.addItems([
            "dark", "light", "blue", "green", "purple", "orange", "cyber"
        ])
        self.theme_selector_combo.currentTextChanged.connect(self.preview_theme)
        themes_layout.addWidget(self.theme_selector_combo)
        
        theme_options_layout.addLayout(themes_layout)
        
        # Thema beschrijvingen
        self.theme_description = QTextEdit()
        self.theme_description.setMaximumHeight(100)
        self.theme_description.setReadOnly(True)
        self.theme_description.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 4px;
                font-size: 10px;
            }
        """)
        theme_options_layout.addWidget(self.theme_description)
        
        layout.addWidget(theme_options_group)
        
        # Thema aanpassingen
        custom_group = QGroupBox("🎨 Aangepaste Kleuren")
        custom_layout = QVBoxLayout(custom_group)
        
        # Accent kleur
        accent_layout = QHBoxLayout()
        accent_layout.addWidget(QLabel("🎨 Accent Kleur:"))
        
        self.accent_color_edit = QLineEdit()
        self.accent_color_edit.setPlaceholderText("#4caf50")
        accent_layout.addWidget(self.accent_color_edit)
        
        custom_layout.addLayout(accent_layout)
        
        # Tekst kleur
        text_layout = QHBoxLayout()
        text_layout.addWidget(QLabel("📝 Tekst Kleur:"))
        
        self.text_color_edit = QLineEdit()
        self.text_color_edit.setPlaceholderText("#ffffff")
        text_layout.addWidget(self.text_color_edit)
        
        custom_layout.addLayout(text_layout)
        
        layout.addWidget(custom_group)
    
    def preview_theme(self):
        """Preview het geselecteerde thema"""
        theme_name = self.theme_selector_combo.currentText()
        
        # Thema beschrijvingen
        theme_descriptions = {
            "dark": "🌙 Donker thema - Perfect voor nachtelijk gebruik",
            "light": "☀️ Licht thema - Helder en duidelijk",
            "blue": "🌊 Blauw thema - Professioneel en rustig",
            "green": "🌿 Groen thema - Natuurlijk en ontspannend",
            "purple": "🔮 Paars thema - Creatief en mysterieus",
            "orange": "🔥 Oranje thema - Energiek en warm",
            "cyber": "🤖 Cyber thema - Futuristisch en technisch"
        }
        
        description = theme_descriptions.get(theme_name, "Onbekend thema")
        self.theme_description.setText(description)
        
        # Update preview label styling
        modern_styling = ModernStyling()
        theme = modern_styling.available_themes.get(theme_name, modern_styling.available_themes["dark"])
        
        self.theme_preview_label.setStyleSheet(f"""
            QLabel {{
                padding: 20px;
                border: 2px dashed {theme["border"]};
                border-radius: 8px;
                background-color: {theme["bg"]};
                color: {theme["fg"]};
                font-size: 12px;
            }}
        """)
        
        self.theme_preview_label.setText(f"Preview van '{theme_name}' thema")
    
    def load_configuration(self):
        """Laad configuratie"""
        try:
            # Thema
            self.theme_selector_combo.setCurrentText(config_manager.get("DEFAULT_THEME", "dark"))
            self.preview_theme()
            
        except Exception as e:
            print(f"❌ Fout bij laden thema configuratie: {e}")
    
    def save_configuration(self):
        """Sla configuratie op"""
        try:
            # Thema instellingen worden opgeslagen in de general tab
            pass
            
        except Exception as e:
            print(f"❌ Fout bij opslaan thema configuratie: {e}")
