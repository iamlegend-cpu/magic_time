"""
Vertaler instellingen tab
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QGroupBox, QLineEdit, QSpinBox, QPushButton
)

from core.config import config_manager

class TranslatorTab(QWidget):
    """Vertaler instellingen tab"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        # Laad configuratie niet automatisch - wordt gedaan door config window
    
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
        self.server_edit.setPlaceholderText("bijv. https://translate.argosopentech.com of localhost:5000")
        self.server_edit.setToolTip("Voer de URL van je LibreTranslate server in. Laat leeg voor standaard server.")
        server_layout.addWidget(self.server_edit)
        
        # Standaard server knop
        self.default_server_btn = QPushButton("Standaard Server")
        self.default_server_btn.setToolTip("Gebruik standaard LibreTranslate server (https://translate.argosopentech.com)")
        self.default_server_btn.clicked.connect(self.use_default_server)
        server_layout.addWidget(self.default_server_btn)
        
        # Voeg server layout toe
        libretranslate_layout.addLayout(server_layout)
        
        # Info label
        info_label = QLabel("💡 Tip: Gebruik de 'Standaard Server' knop als je geen eigen LibreTranslate server hebt.")
        info_label.setStyleSheet("color: #666; font-size: 10px;")
        libretranslate_layout.addWidget(info_label)
        
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
        self.max_chars_spin.setRange(1000, 500000)
        self.max_chars_spin.setValue(100000)
        max_chars_layout.addWidget(self.max_chars_spin)
        
        libretranslate_layout.addLayout(max_chars_layout)
        
        layout.addWidget(libretranslate_group)
    
    def load_configuration(self):
        """Laad configuratie"""
        try:
            # LibreTranslate instellingen
            server_url = config_manager.get("LIBRETRANSLATE_SERVER", "")
            if not server_url:
                # Als er geen server is ingesteld, gebruik standaard (maar sla niet automatisch op)
                server_url = "https://translate.argosopentech.com"
                print(f"🌐 Geen LibreTranslate server ingesteld, gebruik standaard: {server_url}")
            
            self.server_edit.setText(server_url)
            # Timeout en rate limiting
            timeout = config_manager.get_int("LIBRETRANSLATE_TIMEOUT", 30)
            self.timeout_spin.setValue(timeout)
            
            rate_limit = config_manager.get_int("LIBRETRANSLATE_RATE_LIMIT", 0)
            self.rate_limit_spin.setValue(rate_limit)
            
            max_chars = config_manager.get_int("LIBRETRANSLATE_MAX_CHARS", 100000)
            self.max_chars_spin.setValue(max_chars)
            
            # Toon status van server instelling
            if server_url == "https://translate.argosopentech.com":
                print(f"✅ LibreTranslate server ingesteld: {server_url}")
            else:
                print(f"🌐 LibreTranslate server ingesteld: {server_url}")
            
        except Exception as e:
            print(f"❌ Fout bij laden vertaler configuratie: {e}")
    
    def save_configuration(self):
        """Sla configuratie op"""
        try:
            # LibreTranslate instellingen
            server_url = self.server_edit.text().strip()
            if not server_url:
                # Als het veld leeg is, gebruik standaard
                server_url = "https://translate.argosopentech.com"
                print(f"🌐 Server URL veld leeg, gebruik standaard: {server_url}")
                self.server_edit.setText(server_url)
            
            config_manager.set("LIBRETRANSLATE_SERVER", server_url)
            config_manager.set("LIBRETRANSLATE_TIMEOUT", str(self.timeout_spin.value()))
            config_manager.set("LIBRETRANSLATE_RATE_LIMIT", str(self.rate_limit_spin.value()))
            config_manager.set("LIBRETRANSLATE_MAX_CHARS", str(self.max_chars_spin.value()))
            
            print(f"✅ LibreTranslate configuratie opgeslagen: {server_url}")
            
            # Toon status van server instelling
            if server_url == "https://translate.argosopentech.com":
                print(f"✅ Standaard LibreTranslate server actief: {server_url}")
            else:
                print(f"🌐 Custom LibreTranslate server actief: {server_url}")
            
        except Exception as e:
            print(f"❌ Fout bij opslaan vertaler configuratie: {e}")
    
    def use_default_server(self):
        """Gebruik standaard LibreTranslate server"""
        default_server = "https://translate.argosopentech.com"
        self.server_edit.setText(default_server)
        print(f"🌐 Standaard LibreTranslate server ingesteld: {default_server}")
        
        # Sla niet automatisch op - gebruiker moet zelf opslaan
        print(f"💡 Gebruik 'Opslaan' om de standaard server te activeren")
