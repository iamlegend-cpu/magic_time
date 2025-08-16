"""
Settings Panel Core - Hoofdklasse
Beheert de hoofdlogica van het settings panel
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Signal

# Import lokale modules
from .settings_translator import TranslatorSettings
from .settings_whisper import WhisperSettings
from .settings_subtitles import SubtitleSettings
from .settings_vad import VadSettings

class SettingsPanel(QWidget):
    """Quick Settings panel component - alleen essentiële instellingen voor snelle toegang"""
    
    # Signals
    translator_changed = Signal(str)
    model_changed = Signal(str)
    language_changed = Signal(str)
    preserve_subtitles_changed = Signal(bool)
    # VAD is altijd ingeschakeld, geen signal nodig
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_modules()
        self._setup_ui()
        self._connect_signals()
        self.load_current_settings()
        
        # Lijst van quick settings die altijd zichtbaar moeten zijn
        self.quick_settings = [
            self.translator_settings.translator_combo,
            self.whisper_settings.model_combo,
            self.whisper_settings.language_combo,
            self.subtitle_settings.preserve_subtitles_combo,
            self.subtitle_settings.subtitle_type_combo
        ]
    
    def _setup_modules(self):
        """Initialiseer alle settings modules"""
        self.translator_settings = TranslatorSettings(self)
        self.whisper_settings = WhisperSettings(self)
        self.subtitle_settings = SubtitleSettings(self)
        self.vad_settings = VadSettings(self)
    
    def _setup_ui(self):
        """Setup de UI - alleen essentiële quick settings"""
        layout = QVBoxLayout(self)
        
        # Voeg alle settings modules toe
        layout.addWidget(self.translator_settings.translator_group)
        layout.addWidget(self.whisper_settings.whisper_group)
        layout.addWidget(self.whisper_settings.language_group)
        layout.addWidget(self.subtitle_settings.content_group)
        layout.addWidget(self.vad_settings.vad_group)
        
        # Voeg stretch toe aan het einde
        layout.addStretch()
    
    def _connect_signals(self):
        """Verbind alle signals tussen modules"""
        # Vertaler signals
        self.translator_settings.translator_changed.connect(self.translator_changed)
        
        # WhisperX signals
        self.whisper_settings.model_changed.connect(self.model_changed)
        self.whisper_settings.language_changed.connect(self.language_changed)
        
        # Subtitle signals
        self.subtitle_settings.preserve_subtitles_changed.connect(self.preserve_subtitles_changed)
        
        # VAD is altijd ingeschakeld, geen signal connectie nodig
    
    def _is_debug_mode(self) -> bool:
        """Controleer of debug mode is ingeschakeld"""
        try:
            # Lazy import van config_manager om circulaire import te voorkomen
            from core.config import config_manager
            if config_manager:
                log_level = config_manager.get_env("LOG_LEVEL", "INFO")
                return log_level.upper() == "DEBUG"
            return False
        except:
            return False
    
    def load_current_settings(self):
        """Laad huidige instellingen in alle modules"""
        try:
            # Lazy import van config_manager om circulaire import te voorkomen
            from core.config import config_manager
            config_mgr = config_manager
        except ImportError:
            config_mgr = None
        
        # Laad instellingen in alle modules
        self.translator_settings.load_settings(config_mgr)
        self.whisper_settings.load_settings(config_mgr)
        self.subtitle_settings.load_settings(config_mgr)
        self.vad_settings.load_settings(config_mgr)
    
    def get_current_settings(self) -> dict:
        """Krijg huidige instellingen als dictionary"""
        try:
            # Lazy import van config_manager om circulaire import te voorkomen
            from core.config import config_manager
            config_mgr = config_manager
        except ImportError:
            config_mgr = None
        
        # Verzamel instellingen van alle modules
        translator_settings = self.translator_settings.get_settings(config_mgr)
        whisper_settings = self.whisper_settings.get_settings(config_mgr)
        subtitle_settings = self.subtitle_settings.get_settings(config_mgr)
        vad_settings = self.vad_settings.get_current_settings()
        
        # Combineer alle instellingen
        all_settings = {}
        all_settings.update(translator_settings)
        all_settings.update(whisper_settings)
        all_settings.update(subtitle_settings)
        all_settings.update(vad_settings)
        
        # Sla instellingen op in config manager en .env bestanden
        if config_mgr:
            self.translator_settings.save_settings(config_mgr)
            self.whisper_settings.save_settings(config_mgr)
            self.subtitle_settings.save_settings(config_mgr)
            self.vad_settings.save_settings(config_mgr)
        
        if self._is_debug_mode():
            print(f"🔧 [DEBUG] Settings panel: Huidige instellingen: {all_settings}")
        
        return all_settings
    
    def freeze_settings(self):
        """Bevries alle instellingen (maakt ze niet-wijzigbaar)"""
        if self._is_debug_mode():
            print(f"🔧 [DEBUG] Settings panel: Bevries instellingen")
        
        # Bevries alle modules
        self.translator_settings.freeze()
        self.whisper_settings.freeze()
        self.subtitle_settings.freeze()
        self.vad_settings.freeze()
        
        # VAD is altijd beschikbaar met WhisperX
        if self._is_debug_mode():
            print(f"🔧 [DEBUG] Settings panel: VAD status behouden tijdens bevriezen (WhisperX)")
    
    def unfreeze_settings(self):
        """Ontdooit alle instellingen (maakt ze weer wijzigbaar)"""
        if self._is_debug_mode():
            print(f"🔧 [DEBUG] Settings panel: Ontdooi instellingen")
        
        # Ontdooit alle modules
        self.translator_settings.unfreeze()
        self.whisper_settings.unfreeze()
        self.subtitle_settings.unfreeze()
        self.vad_settings.unfreeze()
        
        # VAD is altijd beschikbaar met WhisperX
        if self._is_debug_mode():
            print(f"🔧 [DEBUG] Settings panel: VAD ingeschakeld tijdens ontdooien (WhisperX)")
    
    def is_frozen(self) -> bool:
        """Controleer of instellingen bevroren zijn"""
        frozen = self.translator_settings.is_frozen()
        if self._is_debug_mode():
            print(f"🔧 [DEBUG] Settings panel: Instellingen bevroren: {frozen}")
        return frozen
    
    def update_translator_status(self):
        """Update de status van de vertaler"""
        if self._is_debug_mode():
            print(f"🔧 [DEBUG] Settings panel: Update vertaler status aangeroepen")
        # Deze functie kan worden gebruikt om de vertaler status te updaten
        pass
