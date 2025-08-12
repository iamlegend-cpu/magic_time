"""
Settings Panel voor Magic Time Studio
"""

import os
import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTextEdit, QScrollArea, QGroupBox, QCheckBox, QSpinBox,
    QComboBox, QLineEdit, QFormLayout, QTabWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor

# Lazy import van config_manager om circulaire import te voorkomen
def _get_config_manager():
    """Lazy config manager import om circulaire import te voorkomen"""
    try:
        from core.config import config_manager
        return config_manager
    except ImportError:
        return None
# Import processing modules
from core.all_functions import *

# Import whisper_manager (alleen voor fallback)
try:
    from processing.whisper_manager import whisper_manager
except ImportError:
    # Fallback - maak dummy whisper_manager
    class DummyWhisperManager:
        def __init__(self):
            self.whisper_type = "fast"
            self.model = "medium"
            self.is_initialized = False
        
        def initialize(self, whisper_type, model):
            self.whisper_type = whisper_type
            self.model = model
            self.is_initialized = True
            return True
    
    whisper_manager = DummyWhisperManager()

class SettingsPanel(QWidget):
    """Quick Settings panel component - alleen essentiële instellingen voor snelle toegang"""
    
    # Signals
    translator_changed = pyqtSignal(str)
    whisper_type_changed = pyqtSignal(str)
    model_changed = pyqtSignal(str)
    language_changed = pyqtSignal(str)
    preserve_subtitles_changed = pyqtSignal(bool)
    vad_enabled_changed = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_current_settings()
        
        # Sla alle UI elementen op voor later gebruik
        self.ui_elements = [
            self.translator_combo,
            self.whisper_type_combo,
            self.model_combo,
            self.language_combo,
            self.preserve_subtitles_combo,
            self.subtitle_type_combo,
            self.vad_checkbox
        ]
    
    def _is_debug_mode(self) -> bool:
        """Controleer of debug mode is ingeschakeld"""
        try:
            config_mgr = _get_config_manager()
            if config_mgr:
                log_level = config_mgr.get_env("LOG_LEVEL", "INFO")
                return log_level.upper() == "DEBUG"
            return False
        except:
            return False
    
    def setup_ui(self):
        """Setup de UI - alleen essentiële quick settings"""
        layout = QVBoxLayout(self)
        
        # Vertaler instellingen
        translator_group = QGroupBox("🌐 Vertaler")
        translator_layout = QFormLayout(translator_group)
        
        self.translator_combo = QComboBox()
        self.translator_combo.addItems(["LibreTranslate", "Geen vertaling"])
        self.translator_combo.currentTextChanged.connect(self.on_translator_changed)
        translator_layout.addRow("Vertaler:", self.translator_combo)
        
        layout.addWidget(translator_group)
        
        # Whisper instellingen - directe implementatie
        whisper_group = QGroupBox("🎤 Whisper Instellingen")
        whisper_layout = QFormLayout(whisper_group)
        
        # Whisper type selector
        self.whisper_type_combo = QComboBox()
        self.whisper_type_combo.addItems(["Fast Whisper", "Standaard Whisper"])
        self.whisper_type_combo.currentTextChanged.connect(self.on_whisper_type_changed)
        whisper_layout.addRow("Whisper Type:", self.whisper_type_combo)
        
        # Model selector
        self.model_combo = QComboBox()
        self.model_combo.addItems(["tiny", "base", "small", "medium", "large", "large-v3-turbo"])
        self.model_combo.currentTextChanged.connect(self.on_model_changed)
        whisper_layout.addRow("Model:", self.model_combo)
        
        whisper_group.setLayout(whisper_layout)
        layout.addWidget(whisper_group)
        
        # Taal instellingen
        language_group = QGroupBox("🗣️ Taal")
        language_layout = QFormLayout(language_group)
        
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Engels", "Nederlands", "Duits", "Frans", "Spaans", "Auto detectie"])
        self.language_combo.currentTextChanged.connect(self.on_language_changed)
        language_layout.addRow("Taal:", self.language_combo)
        
        layout.addWidget(language_group)
        
        # Preserve original subtitles
        content_group = QGroupBox("📺 Ondertitels")
        content_layout = QFormLayout(content_group)
        
        self.preserve_subtitles_combo = QComboBox()
        self.preserve_subtitles_combo.addItems([
            "Alleen SRT bestanden maken"
        ])
        self.preserve_subtitles_combo.setEnabled(False)  # Altijd alleen SRT bestanden
        content_layout.addRow("Ondertitels:", self.preserve_subtitles_combo)
        
        # Subtitle type instelling (alleen softcoded beschikbaar)
        self.subtitle_type_combo = QComboBox()
        self.subtitle_type_combo.addItems([
            "Softcoded (externe track)"
        ])
        self.subtitle_type_combo.setEnabled(False)  # Uitgeschakeld omdat alleen softcoded beschikbaar is
        content_layout.addRow("Subtitle type:", self.subtitle_type_combo)
        
        content_group.setLayout(content_layout)
        layout.addWidget(content_group)
        
        # VAD instellingen
        vad_group = QGroupBox("🎯 Voice Activity Detection")
        vad_layout = QFormLayout(vad_group)
        
        self.vad_checkbox = QCheckBox("VAD inschakelen voor betere transcriptie")
        self.vad_checkbox.setToolTip("VAD inschakelen voor betere transcriptie (alleen beschikbaar met Fast Whisper)")
        self.vad_checkbox.stateChanged.connect(self.on_vad_enabled_changed)
        vad_layout.addRow(self.vad_checkbox)
        
        vad_group.setLayout(vad_layout)
        layout.addWidget(vad_group)
        
        # Voeg stretch toe aan het einde
        layout.addStretch()
    
    def load_current_settings(self):
        """Laad huidige instellingen"""
        # Vertaler
        config_mgr = _get_config_manager()
        current_translator = config_mgr.get("default_translator", "libretranslate") if config_mgr else "libretranslate"
        if current_translator == "libretranslate":
            self.translator_combo.setCurrentText("LibreTranslate")
        else:
            self.translator_combo.setCurrentText("Geen vertaling")
        # Debug output alleen in debug mode
        if self._is_debug_mode():
            print(f"🔧 [DEBUG] Settings panel: Vertaler geladen: {current_translator}")
        
        # LibreTranslate server instellingen
        if config_mgr:
            libretranslate_server = config_mgr.get("libretranslate_server", None)
            if not libretranslate_server:
                libretranslate_server = config_mgr.get_env("LIBRETRANSLATE_SERVER", "Niet ingesteld")
            if self._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: LibreTranslate server: {libretranslate_server}")
        else:
            if self._is_debug_mode():
                print(f"⚠️ [DEBUG] Settings panel: Config manager niet beschikbaar voor LibreTranslate instellingen")
        
        # Whisper instellingen - lees uit GUI configuratie (niet uit .env)
        current_whisper_type = config_mgr.get("whisper_type", None) if config_mgr else None
        if current_whisper_type is None:
            # Fallback naar .env
            current_whisper_type = config_mgr.get_env("WHISPER_TYPE", "fast") if config_mgr else "fast"
        
        if current_whisper_type == "fast":
            self.whisper_type_combo.setCurrentText("Fast Whisper")
            current_model = config_mgr.get("default_fast_whisper_model", None) if config_mgr else None
            if current_model is None:
                # Fallback naar .env
                current_model = config_mgr.get_env("DEFAULT_FAST_WHISPER_MODEL", "medium") if config_mgr else "medium"
        else:
            self.whisper_type_combo.setCurrentText("Standaard Whisper")
            current_model = config_mgr.get("default_whisper_model", None) if config_mgr else None
            if current_model is None:
                # Fallback naar .env
                current_model = config_mgr.get_env("DEFAULT_WHISPER_MODEL", "medium") if config_mgr else "medium"
        
        # Zet het juiste model
        model_index = self.model_combo.findText(current_model)
        if model_index >= 0:
            self.model_combo.setCurrentIndex(model_index)
        if self._is_debug_mode():
            print(f"🔧 [DEBUG] Settings panel: Whisper type geladen: {current_whisper_type}, model: {current_model}")
        
        # Taal - laad uit configuratie
        current_language = config_mgr.get("default_language", "en") if config_mgr else "en"
        language_mapping = {
            "en": "Engels",
            "nl": "Nederlands", 
            "de": "Duits",
            "fr": "Frans",
            "es": "Spaans",
            "auto": "Auto detectie"
        }
        language_display = language_mapping.get(current_language, "Engels")
        self.language_combo.setCurrentText(language_display)
        if self._is_debug_mode():
            print(f"🔧 [DEBUG] Settings panel: Taal geladen: {current_language} -> {language_display}")
        
        # Originele ondertitels (altijd alleen SRT bestanden)
        self.preserve_subtitles_combo.setCurrentText("Alleen SRT bestanden maken")
        if self._is_debug_mode():
            print(f"🔧 [DEBUG] Settings panel: Preserve subtitles geladen: altijd alleen SRT bestanden")
        
        # Subtitle type instelling (altijd softcoded)
        subtitle_type = "softcoded"  # Altijd softcoded, hardcoded wordt niet meer ondersteund
        self.subtitle_type_combo.setCurrentText("Softcoded (externe track)")
        if self._is_debug_mode():
            print(f"🔧 [DEBUG] Settings panel: Subtitle type geladen: {subtitle_type} (altijd softcoded)")
        
        # VAD instelling - controleer eerst het huidige whisper type
        # Gebruik de al geladen whisper type variabele
        if current_whisper_type == "standard":
            # Standaard Whisper ondersteunt geen VAD
            self.vad_checkbox.setChecked(False)
            self.vad_checkbox.setEnabled(False)
            self.vad_checkbox.setToolTip("VAD wordt niet ondersteund door standaard Whisper. Schakel over naar Fast Whisper om VAD te gebruiken.")
            if self._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: VAD uitgeschakeld (standaard Whisper)")
        else:
            # Fast Whisper ondersteunt VAD
            vad_enabled = config_mgr.get("vad_enabled", False) if config_mgr else False
            self.vad_checkbox.setChecked(vad_enabled)
            self.vad_checkbox.setEnabled(True)
            self.vad_checkbox.setToolTip("VAD inschakelen voor betere transcriptie (alleen beschikbaar met Fast Whisper)")
            if self._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: VAD geladen: {vad_enabled}")
        
        # Debug: toon huidige LibreTranslate instellingen
        if config_mgr:
            libretranslate_server = config_mgr.get("LIBRETRANSLATE_SERVER", None)
            if not libretranslate_server:
                libretranslate_server = config_mgr.get_env("LIBRETRANSLATE_SERVER", "Niet ingesteld")
            if self._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: LibreTranslate server: {libretranslate_server}")
                print(f"🔧 [DEBUG] Settings panel: Huidige vertaler: {current_translator}")
            
            # Als er geen LibreTranslate server is ingesteld, toon waarschuwing
            if not libretranslate_server or libretranslate_server == "Niet ingesteld":
                print("⚠️ Waarschuwing: LibreTranslate server niet ingesteld! Ga naar Configuratie > Vertaler om dit in te stellen.")
        else:
            if self._is_debug_mode():
                print(f"⚠️ [DEBUG] Settings panel: Config manager niet beschikbaar voor LibreTranslate instellingen")
    
    def on_translator_changed(self, translator_name: str):
        """Handle vertaler wijziging"""
        if self._is_debug_mode():
            print(f"🔧 [DEBUG] Settings panel: Vertaler gewijzigd naar {translator_name}")
        
        config_mgr = _get_config_manager()
        if config_mgr:
            if translator_name == "LibreTranslate":
                config_mgr.set("default_translator", "libretranslate")
                config_mgr.set("translator", "libretranslate")
                # Sla ook op in .env bestanden
                config_mgr.set_env("DEFAULT_TRANSLATOR", "libretranslate")
                if self._is_debug_mode():
                    print(f"🔧 [DEBUG] Settings panel: Vertaler opgeslagen in config: libretranslate")
            else:
                config_mgr.set("default_translator", "none")
                config_mgr.set("translator", "none")
                # Sla ook op in .env bestanden
                config_mgr.set_env("DEFAULT_TRANSLATOR", "none")
                if self._is_debug_mode():
                    print(f"🔧 [DEBUG] Settings panel: Vertaler opgeslagen in config: none")
        else:
            if self._is_debug_mode():
                print(f"⚠️ [DEBUG] Settings panel: Config manager niet beschikbaar voor vertaler")
        
        self.translator_changed.emit(translator_name)
    
    def on_whisper_type_changed(self, whisper_type_text: str):
        """Handle Whisper type wijziging"""
        whisper_type = "fast" if whisper_type_text == "Fast Whisper" else "standard"
        if self._is_debug_mode():
            print(f"🔧 [DEBUG] Settings panel: Whisper type gewijzigd naar {whisper_type}")
        
        # Update config manager - sla op in GUI configuratie (niet in .env)
        config_mgr = _get_config_manager()
        if config_mgr:
            config_mgr.set("whisper_type", whisper_type)
            # Sla ook op in .env als backup
            config_mgr.set_env("WHISPER_TYPE", whisper_type)
            if self._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: Whisper type opgeslagen in config: {whisper_type}")
        else:
            if self._is_debug_mode():
                print(f"⚠️ [DEBUG] Settings panel: Config manager niet beschikbaar voor whisper type")
        
        # Emit signal
        self.whisper_type_changed.emit(whisper_type)
        
        # Update VAD status op basis van whisper type
        if whisper_type == "standard":
            # Standaard Whisper ondersteunt geen VAD
            self.vad_checkbox.setChecked(False)
            self.vad_checkbox.setEnabled(False)
            self.vad_checkbox.setToolTip("VAD wordt niet ondersteund door standaard Whisper. Schakel over naar Fast Whisper om VAD te gebruiken.")
        else:
            # Fast Whisper ondersteunt VAD
            self.vad_checkbox.setEnabled(True)
            self.vad_checkbox.setToolTip("VAD inschakelen voor betere transcriptie (alleen beschikbaar met Fast Whisper)")
    
    def on_model_changed(self, model: str):
        """Handle Whisper model wijziging"""
        if self._is_debug_mode():
            print(f"🔧 [DEBUG] Settings panel: Whisper model gewijzigd naar {model}")
        
        # Update config manager - sla op in GUI configuratie (niet in .env)
        config_mgr = _get_config_manager()
        if config_mgr:
            current_whisper_type = "fast" if self.whisper_type_combo.currentText() == "Fast Whisper" else "standard"
            if current_whisper_type == "fast":
                config_mgr.set("default_fast_whisper_model", model)
                # Sla ook op in .env als backup
                config_mgr.set_env("DEFAULT_FAST_WHISPER_MODEL", model)
                if self._is_debug_mode():
                    print(f"🔧 [DEBUG] Settings panel: Fast Whisper model opgeslagen in config: {model}")
            else:
                config_mgr.set("default_whisper_model", model)
                # Sla ook op in .env als backup
                config_mgr.set_env("DEFAULT_WHISPER_MODEL", model)
                if self._is_debug_mode():
                    print(f"🔧 [DEBUG] Settings panel: Standaard Whisper model opgeslagen in config: {model}")
        else:
            if self._is_debug_mode():
                print(f"⚠️ [DEBUG] Settings panel: Config manager niet beschikbaar voor whisper model")
        
        # Emit signal
        self.model_changed.emit(model)
    

    
    def on_language_changed(self, language_text: str):
        """Handle taal wijziging"""
        if self._is_debug_mode():
            print(f"🔧 [DEBUG] Settings panel: Taal gewijzigd naar {language_text}")
        
        # Update config manager - sla op in GUI configuratie (niet in .env)
        config_mgr = _get_config_manager()
        if config_mgr:
            # Converteer taal naar code
            language_mapping = {
                "Engels": "en",
                "Nederlands": "nl", 
                "Duits": "de",
                "Frans": "fr",
                "Spaans": "es",
                "Auto detectie": "auto"
            }
            language_code = language_mapping.get(language_text, "en")
            config_mgr.set("default_language", language_code)
            if self._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: Taal opgeslagen in config: {language_code}")
        else:
            if self._is_debug_mode():
                print(f"⚠️ [DEBUG] Settings panel: Config manager niet beschikbaar voor taal")
        
        # Emit signal
        self.language_changed.emit(language_text)
    
    def on_preserve_subtitles_changed(self, preserve_text: str):
        """Handle preserve subtitles wijziging"""
        preserve = preserve_text == "Behoud originele ondertitels"
        if self._is_debug_mode():
            print(f"🔧 [DEBUG] Settings panel: Preserve subtitles gewijzigd naar {preserve}")
        
        config_mgr = _get_config_manager()
        if config_mgr:
            config_mgr.set("preserve_subtitles", preserve)
            if self._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: Preserve subtitles opgeslagen in config: {preserve}")
        else:
            if self._is_debug_mode():
                print(f"⚠️ [DEBUG] Settings panel: Config manager niet beschikbaar voor preserve subtitles")
        
        self.preserve_subtitles_changed.emit(preserve)
    
    def on_vad_enabled_changed(self, state: int):
        """Handle VAD wijziging"""
        vad_enabled = state == Qt.CheckState.Checked
        if self._is_debug_mode():
            print(f"🔧 [DEBUG] Settings panel: VAD gewijzigd naar {vad_enabled}")
        
        config_mgr = _get_config_manager()
        if config_mgr:
            config_mgr.set("vad_enabled", vad_enabled)
            if self._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: VAD opgeslagen in config: {vad_enabled}")
        else:
            if self._is_debug_mode():
                print(f"⚠️ [DEBUG] Settings panel: Config manager niet beschikbaar voor VAD")
        
        self.vad_enabled_changed.emit(vad_enabled)
    
    def on_subtitle_type_changed(self, subtitle_type_text: str):
        """Handle subtitle type wijziging"""
        subtitle_type = "softcoded" if subtitle_type_text == "Softcoded (externe track)" else "hardcoded"
        if self._is_debug_mode():
            print(f"🔧 [DEBUG] Settings panel: Subtitle type gewijzigd naar {subtitle_type}")
        
        # Update config manager - sla op in GUI configuratie (niet in .env)
        config_mgr = _get_config_manager()
        if config_mgr:
            config_mgr.set("subtitle_type", subtitle_type)
            # Sla ook op in .env als backup
            config_mgr.set_env("DEFAULT_SUBTITLE_TYPE", subtitle_type)
            if self._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: Subtitle type opgeslagen in config: {subtitle_type}")
        else:
            if self._is_debug_mode():
                print(f"⚠️ [DEBUG] Settings panel: Config manager niet beschikbaar voor subtitle type")
    

    

    
    def get_current_settings(self) -> dict:
        """Krijg huidige instellingen als dictionary"""
        # Haal LibreTranslate server URL op uit config manager
        config_mgr = _get_config_manager()
        libretranslate_server = "http://100.90.127.78:5000"  # Standaard fallback
        if config_mgr:
            # Eerst kijken naar GUI instellingen
            libretranslate_server = config_mgr.get("libretranslate_server", libretranslate_server)
            if not libretranslate_server:
                # Fallback naar .env instellingen
                libretranslate_server = config_mgr.get_env("LIBRETRANSLATE_SERVER", libretranslate_server)
        if self._is_debug_mode():
            print(f"🔧 [DEBUG] Settings panel: LibreTranslate server uit config: {libretranslate_server}")
        
        # Converteer vertaler naam naar juiste waarde voor processing
        translator_value = "libretranslate" if self.translator_combo.currentText() == "LibreTranslate" else "none"
        if self._is_debug_mode():
            print(f"🔧 [DEBUG] Settings panel: Vertaler uit UI: {translator_value}")
        
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
        if self._is_debug_mode():
            print(f"🔧 [DEBUG] Settings panel: Taal uit UI: {language_code}")
        
        # Whisper instellingen direct van de combo boxes
        whisper_type = "fast" if self.whisper_type_combo.currentText() == "Fast Whisper" else "standard"
        whisper_model = self.model_combo.currentText()
        if self._is_debug_mode():
            print(f"🔧 [DEBUG] Settings panel: Whisper type uit UI: {whisper_type}, model: {whisper_model}")
        
        # Subtitle type instelling (altijd softcoded)
        subtitle_type = "softcoded"  # Altijd softcoded, hardcoded wordt niet meer ondersteund
        if self._is_debug_mode():
            print(f"🔧 [DEBUG] Settings panel: Subtitle type uit UI: {subtitle_type} (altijd softcoded)")
        
        # Preserve subtitles instelling
        preserve_subtitles = False  # Altijd alleen SRT bestanden maken
        if self._is_debug_mode():
            print(f"🔧 [DEBUG] Settings panel: Preserve subtitles uit UI: {preserve_subtitles} (altijd alleen SRT bestanden)")
        
        # VAD instelling
        vad_enabled = self.vad_checkbox.isChecked()
        if self._is_debug_mode():
            print(f"🔧 [DEBUG] Settings panel: VAD uit UI: {vad_enabled}")
        
        settings = {
            "translator": translator_value,
            "default_translator": translator_value,
            "whisper_type": whisper_type,
            "whisper_model": whisper_model,
            "language": language_code,
            "preserve_subtitles": preserve_subtitles,
            "subtitle_type": subtitle_type,
            "vad_enabled": vad_enabled,
            "libretranslate_server": libretranslate_server,
            "target_language": "nl"  # ALTIJD naar Nederlands vertalen
        }
        
        # Sla instellingen op in config manager en .env bestanden
        if config_mgr:
            config_mgr.set("translator", translator_value)
            config_mgr.set("default_translator", translator_value)
            config_mgr.set("libretranslate_server", libretranslate_server)
            config_mgr.set("target_language", "nl")
            # Sla ook op in .env bestanden
            config_mgr.set_env("DEFAULT_TRANSLATOR", translator_value)
            config_mgr.set_env("LIBRETRANSLATE_SERVER", libretranslate_server)
            config_mgr.set_env("DEFAULT_TARGET_LANGUAGE", "nl")
        
        if self._is_debug_mode():
            print(f"🔧 [DEBUG] Settings panel: Huidige instellingen: {settings}")
        return settings
    
    def freeze_settings(self):
        """Bevries alle instellingen (maakt ze niet-wijzigbaar)"""
        if self._is_debug_mode():
            print(f"🔧 [DEBUG] Settings panel: Bevries instellingen")
        for element in self.ui_elements:
            if hasattr(element, 'setEnabled'):
                element.setEnabled(False)
        
        # Behoud VAD status op basis van whisper type
        config_mgr = _get_config_manager()
        current_whisper_type = config_mgr.get_env("WHISPER_TYPE", "fast") if config_mgr else "fast"
        if current_whisper_type == "standard":
            # Standaard Whisper ondersteunt geen VAD, houd uitgeschakeld
            self.vad_checkbox.setChecked(False)
            self.vad_checkbox.setEnabled(False)
            if self._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: VAD uitgeschakeld tijdens bevriezen (standaard Whisper)")
    
    def unfreeze_settings(self):
        """Ontdooit alle instellingen (maakt ze weer wijzigbaar)"""
        if self._is_debug_mode():
            print(f"🔧 [DEBUG] Settings panel: Ontdooi instellingen")
        for element in self.ui_elements:
            if hasattr(element, 'setEnabled'):
                element.setEnabled(True)
        
        # Herstel VAD status op basis van whisper type
        config_mgr = _get_config_manager()
        current_whisper_type = config_mgr.get_env("WHISPER_TYPE", "fast") if config_mgr else "fast"
        if current_whisper_type == "standard":
            # Standaard Whisper ondersteunt geen VAD
            self.vad_checkbox.setChecked(False)
            self.vad_checkbox.setEnabled(False)
            self.vad_checkbox.setToolTip("VAD wordt niet ondersteund door standaard Whisper. Schakel over naar Fast Whisper om VAD te gebruiken.")
            if self._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: VAD uitgeschakeld tijdens ontdooien (standaard Whisper)")
        else:
            # Fast Whisper ondersteunt VAD
            self.vad_checkbox.setEnabled(True)
            self.vad_checkbox.setToolTip("VAD inschakelen voor betere transcriptie (alleen beschikbaar met Fast Whisper)")
            if self._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: VAD ingeschakeld tijdens ontdooien (Fast Whisper)")
    
    def is_frozen(self) -> bool:
        """Controleer of instellingen bevroren zijn"""
        frozen = not self.translator_combo.isEnabled()
        if self._is_debug_mode():
            print(f"🔧 [DEBUG] Settings panel: Instellingen bevroren: {frozen}")
        return frozen
    
    def update_translator_status(self):
        """Update de status van de vertaler"""
        if self._is_debug_mode():
            print(f"🔧 [DEBUG] Settings panel: Update vertaler status aangeroepen")
        # Deze functie kan worden gebruikt om de vertaler status te updaten
        pass 