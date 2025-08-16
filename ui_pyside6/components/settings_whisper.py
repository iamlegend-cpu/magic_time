"""
WhisperX Instellingen voor Settings Panel
Beheert WhisperX model en taal configuratie
"""

from PySide6.QtWidgets import QGroupBox, QFormLayout, QComboBox, QLabel
from PySide6.QtCore import Signal, QObject
from PySide6.QtGui import QFont

class WhisperSettings(QObject):
    """Beheert WhisperX instellingen in het settings panel"""
    
    # Signals - defined as class attributes
    model_changed = Signal(str)
    language_changed = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.model_combo = None
        self.language_combo = None
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup WhisperX UI componenten"""
        # Whisper instellingen - alleen WhisperX
        whisper_group = QGroupBox("🎤 WhisperX Instellingen")
        whisper_layout = QFormLayout(whisper_group)
        
        # WhisperX type label (niet meer selecteerbaar)
        whisper_type_label = QLabel("WhisperX")
        whisper_type_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        whisper_layout.addRow("Whisper Type:", whisper_type_label)
        
        # Model selector
        self.model_combo = QComboBox()
        self.model_combo.addItems(["tiny", "base", "small", "medium", "large", "large-v3", "large-v3-turbo"])
        self.model_combo.currentTextChanged.connect(self._on_model_changed)
        whisper_layout.addRow("Model:", self.model_combo)
        
        whisper_group.setLayout(whisper_layout)
        self.whisper_group = whisper_group
        
        # Taal instellingen
        language_group = QGroupBox("🗣️ Taal")
        language_layout = QFormLayout(language_group)
        
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Engels", "Nederlands", "Duits", "Frans", "Spaans"])
        self.language_combo.currentTextChanged.connect(self._on_language_changed)
        language_layout.addRow("Taal:", self.language_combo)
        
        language_group.setLayout(language_layout)
        self.language_group = language_group
    
    def _on_model_changed(self, model: str):
        """Handle WhisperX model wijziging"""
        if self.parent and hasattr(self.parent, '_is_debug_mode'):
            if self.parent._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: WhisperX model gewijzigd naar {model}")
        
        # Emit signal naar parent
        self.model_changed.emit(model)
    
    def _on_language_changed(self, language_text: str):
        """Handle taal wijziging"""
        if self.parent and hasattr(self.parent, '_is_debug_mode'):
            if self.parent._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: Taal gewijzigd naar {language_text}")
        
        # Emit signal naar parent
        self.language_changed.emit(language_text)
    
    def load_settings(self, config_mgr):
        """Laad WhisperX instellingen"""
        if not config_mgr:
            return
        
        # WhisperX instellingen - altijd WhisperX
        current_whisper_type = "whisperx"  # Altijd WhisperX
        
        # Model instellingen
        current_model = config_mgr.get("default_whisperx_model", None)
        if current_model is None:
            # Fallback naar .env of default
            current_model = config_mgr.get_env("DEFAULT_WHISPERX_MODEL", "large-v3")
        
        # Zet het juiste model
        model_index = self.model_combo.findText(current_model)
        if model_index >= 0:
            self.model_combo.setCurrentIndex(model_index)
        
        if self.parent and hasattr(self.parent, '_is_debug_mode'):
            if self.parent._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: Whisper type geladen: {current_whisper_type}, model: {current_model}")
        
        # Taal - laad uit configuratie
        current_language = config_mgr.get("default_language", "en")
        language_mapping = {
            "en": "Engels",
            "nl": "Nederlands", 
            "de": "Duits",
            "fr": "Frans",
            "es": "Spaans"
        }
        language_display = language_mapping.get(current_language, "Engels")
        self.language_combo.setCurrentText(language_display)
        
        if self.parent and hasattr(self.parent, '_is_debug_mode'):
            if self.parent._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: Taal geladen: {current_language} -> {language_display}")
    
    def get_settings(self, config_mgr):
        """Krijg huidige WhisperX instellingen"""
        # WhisperX instellingen - altijd WhisperX
        whisper_type = "whisperx"
        whisper_model = self.model_combo.currentText()
        
        if self.parent and hasattr(self.parent, '_is_debug_mode'):
            if self.parent._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: WhisperX type uit UI: {whisper_type}, model: {whisper_model}")
        
        # Converteer taal naar juiste waarde voor processing
        language_mapping = {
            "Engels": "en",
            "Nederlands": "nl", 
            "Duits": "de",
            "Frans": "fr",
            "Spaans": "es",
            "Auto detectie": "auto"
        }
        language_code = language_mapping.get(self.language_combo.currentText(), "en")
        
        if self.parent and hasattr(self.parent, '_is_debug_mode'):
            if self.parent._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: Taal uit UI: {language_code}")
        
        return {
            "whisper_type": whisper_type,
            "whisper_model": whisper_model,
            "language": language_code
        }
    
    def save_settings(self, config_mgr):
        """Sla WhisperX instellingen op"""
        if not config_mgr:
            return
        
        settings = self.get_settings(config_mgr)
        
        # Update config manager - sla alleen op in .env
        config_mgr.set_env("DEFAULT_WHISPERX_MODEL", settings["whisper_model"])
        config_mgr.set_env("DEFAULT_LANGUAGE", settings["language"])
        
        if self.parent and hasattr(self.parent, '_is_debug_mode'):
            if self.parent._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: WhisperX model opgeslagen in config: {settings['whisper_model']}")
                print(f"🔧 [DEBUG] Settings panel: Taal opgeslagen in config: {settings['language']}")
    
    def freeze(self):
        """Bevries WhisperX instellingen"""
        if self.model_combo:
            self.model_combo.setEnabled(False)
        if self.language_combo:
            self.language_combo.setEnabled(False)
    
    def unfreeze(self):
        """Ontdooit WhisperX instellingen"""
        if self.model_combo:
            self.model_combo.setEnabled(True)
        if self.language_combo:
            self.language_combo.setEnabled(True)
    
    def is_frozen(self):
        """Controleer of WhisperX instellingen bevroren zijn"""
        return (not self.model_combo.isEnabled() if self.model_combo else False) or \
               (not self.language_combo.isEnabled() if self.language_combo else False)
