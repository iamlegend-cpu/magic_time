"""
Vertaler Instellingen voor Settings Panel
Beheert LibreTranslate en andere vertaler configuratie
"""

from PySide6.QtWidgets import QGroupBox, QFormLayout, QComboBox
from PySide6.QtCore import Signal, QObject

class TranslatorSettings(QObject):
    """Beheert vertaler instellingen in het settings panel"""
    
    # Signals - defined as class attributes
    translator_changed = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.translator_combo = None
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup vertaler UI componenten"""
        # Vertaler instellingen
        translator_group = QGroupBox("🌐 Vertaler")
        translator_layout = QFormLayout(translator_group)
        
        self.translator_combo = QComboBox()
        self.translator_combo.addItems(["LibreTranslate", "Geen vertaling"])
        self.translator_combo.currentTextChanged.connect(self._on_translator_changed)
        translator_layout.addRow("Vertaler:", self.translator_combo)
        
        translator_group.setLayout(translator_layout)
        self.translator_group = translator_group
    
    def _on_translator_changed(self, translator_name: str):
        """Handle vertaler wijziging"""
        if self.parent and hasattr(self.parent, '_is_debug_mode'):
            if self.parent._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: Vertaler gewijzigd naar {translator_name}")
        
        # Emit signal naar parent
        self.translator_changed.emit(translator_name)
    
    def load_settings(self, config_mgr):
        """Laad vertaler instellingen"""
        if not config_mgr:
            return
        
        current_translator = config_mgr.get("default_translator", "libretranslate")
        if current_translator == "libretranslate":
            self.translator_combo.setCurrentText("LibreTranslate")
        else:
            self.translator_combo.setCurrentText("Geen vertaling")
        
        # Debug output alleen in debug mode
        if self.parent and hasattr(self.parent, '_is_debug_mode'):
            if self.parent._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: Vertaler geladen: {current_translator}")
        
        # LibreTranslate server instellingen
        libretranslate_server = config_mgr.get("libretranslate_server", None)
        if not libretranslate_server:
            libretranslate_server = config_mgr.get_env("LIBRETRANSLATE_SERVER", "Niet ingesteld")
        if self.parent and hasattr(self.parent, '_is_debug_mode'):
            if self.parent._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: LibreTranslate server: {libretranslate_server}")
    
    def get_settings(self, config_mgr):
        """Krijg huidige vertaler instellingen"""
        # Haal LibreTranslate server URL op uit config manager
        libretranslate_server = "http://100.90.127.78:5000"  # Standaard fallback
        if config_mgr:
            # Eerst kijken naar GUI instellingen
            libretranslate_server = config_mgr.get("libretranslate_server", libretranslate_server)
            if not libretranslate_server:
                # Fallback naar .env instellingen
                libretranslate_server = config_mgr.get_env("LIBRETRANSLATE_SERVER", libretranslate_server)
        
        if self.parent and hasattr(self.parent, '_is_debug_mode'):
            if self.parent._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: LibreTranslate server uit config: {libretranslate_server}")
        
        # Converteer vertaler naam naar juiste waarde voor processing
        translator_value = "libretranslate" if self.translator_combo.currentText() == "LibreTranslate" else "none"
        
        if self.parent and hasattr(self.parent, '_is_debug_mode'):
            if self.parent._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: Vertaler uit UI: {translator_value}")
        
        return {
            "translator": translator_value,
            "default_translator": translator_value,
            "libretranslate_server": libretranslate_server,
            "target_language": "nl"  # ALTIJD naar Nederlands vertalen
        }
    
    def save_settings(self, config_mgr):
        """Sla vertaler instellingen op"""
        if not config_mgr:
            return
        
        settings = self.get_settings(config_mgr)
        
        # Sla alleen op in .env bestanden
        config_mgr.set_env("DEFAULT_TRANSLATOR", settings["translator"])
        config_mgr.set_env("LIBRETRANSLATE_SERVER", settings["libretranslate_server"])
        config_mgr.set_env("DEFAULT_TARGET_LANGUAGE", settings["target_language"])
    
    def freeze(self):
        """Bevries vertaler instellingen"""
        if self.translator_combo:
            self.translator_combo.setEnabled(False)
    
    def unfreeze(self):
        """Ontdooit vertaler instellingen"""
        if self.translator_combo:
            self.translator_combo.setEnabled(True)
    
    def is_frozen(self):
        """Controleer of vertaler instellingen bevroren zijn"""
        return not self.translator_combo.isEnabled() if self.translator_combo else False
