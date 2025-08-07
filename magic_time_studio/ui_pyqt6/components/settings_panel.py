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

from magic_time_studio.core.config import config_manager
from magic_time_studio.processing import translator

# Import whisper_manager
try:
    from magic_time_studio.processing.whisper_manager import whisper_manager
except ImportError:
    import sys
    sys.path.append('..')
    from processing.whisper_manager import whisper_manager

class SettingsPanel(QWidget):
    """Quick Settings panel component - alleen essentiële instellingen voor snelle toegang"""
    
    # Signals
    translator_changed = pyqtSignal(str)
    whisper_type_changed = pyqtSignal(str)
    model_changed = pyqtSignal(str)
    language_changed = pyqtSignal(str)
    preserve_subtitles_changed = pyqtSignal(bool)
    
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
            self.preserve_subtitles_combo
        ]
    
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
        
        # Whisper instellingen
        whisper_group = QGroupBox("🎤 Fast Whisper Instellingen")
        whisper_layout = QFormLayout(whisper_group)
        
        # Whisper Type (alleen Fast Whisper beschikbaar)
        self.whisper_type_combo = QComboBox()
        self.whisper_type_combo.addItems(["🚀 Fast Whisper"])
        self.whisper_type_combo.setEnabled(False)  # Uitschakelen omdat alleen Fast Whisper beschikbaar is
        self.whisper_type_combo.currentTextChanged.connect(self.on_whisper_type_changed)
        whisper_layout.addRow("Whisper Type:", self.whisper_type_combo)
        
        # Model
        self.model_combo = QComboBox()
        self.model_combo.currentTextChanged.connect(self.on_model_changed)
        whisper_layout.addRow("Model:", self.model_combo)
        
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
        self.preserve_subtitles_combo.addItems(["Behoud originele ondertitels", "Vervang originele ondertitels"])
        self.preserve_subtitles_combo.currentTextChanged.connect(self.on_preserve_subtitles_changed)
        content_layout.addRow("Originele ondertitels:", self.preserve_subtitles_combo)
        
        layout.addWidget(content_group)
        
        # Voeg stretch toe aan het einde
        layout.addStretch()
    
    def load_current_settings(self):
        """Laad huidige instellingen"""
        # Vertaler
        current_translator = config_manager.get("default_translator", "libretranslate")
        if current_translator == "libretranslate":
            self.translator_combo.setCurrentText("LibreTranslate")
        else:
            self.translator_combo.setCurrentText("Geen vertaling")
        
        # Whisper type (altijd Fast Whisper)
        self.whisper_type_combo.setCurrentText("🚀 Fast Whisper")
        
        # Update modellen voor Fast Whisper
        self.update_models_for_type("fast")
        
        # Taal (standaard Engels)
        self.language_combo.setCurrentText("Engels")
        
        # Originele ondertitels (standaard behouden)
        preserve_subtitles = config_manager.get("preserve_original_subtitles", True)
        if preserve_subtitles:
            self.preserve_subtitles_combo.setCurrentText("Behoud originele ondertitels")
        else:
            self.preserve_subtitles_combo.setCurrentText("Vervang originele ondertitels")
    
    def update_models_for_type(self, whisper_type):
        """Update beschikbare modellen voor het geselecteerde Whisper type"""
        try:
            self.model_combo.clear()
            
            if whisper_type == "fast":
                # Fast Whisper modellen
                models = [
                    "tiny", "base", "small", "medium", "large",
                    "large-v1", "large-v2", "large-v3", 
                    "large-v3-turbo", "turbo"
                ]
                default_model = config_manager.get_env("DEFAULT_FAST_WHISPER_MODEL", "large-v3-turbo")
            else:
                # Alleen Fast Whisper modellen beschikbaar
                models = [
                    "tiny", "base", "small", "medium", "large",
                    "large-v1", "large-v2", "large-v3", 
                    "large-v3-turbo", "turbo"
                ]
                default_model = config_manager.get_env("DEFAULT_FAST_WHISPER_MODEL", "large-v3-turbo")
            
            # Voeg modellen toe met display namen
            model_display_names = {
                "tiny": "Tiny (39 MB)",
                "base": "Base (74 MB)", 
                "small": "Small (244 MB)",
                "medium": "Medium (769 MB)",
                "large": "Large (1550 MB)",
                "large-v1": "Large V1 (1550 MB)",
                "large-v2": "Large V2 (1550 MB)",
                "large-v3": "Large V3 (1550 MB)",
                "large-v3-turbo": "Large V3 Turbo (1550 MB)",
                "turbo": "Turbo (1550 MB)"
            }
            
            for model in models:
                display_name = model_display_names.get(model, model)
                self.model_combo.addItem(display_name, model)
            
            # Stel default model in
            default_index = self.model_combo.findData(default_model)
            if default_index >= 0:
                self.model_combo.setCurrentIndex(default_index)
            else:
                # Fallback naar eerste model
                self.model_combo.setCurrentIndex(0)
                
        except Exception as e:
            print(f"⚠️ Fout bij updaten modellen: {e}")
            # Fallback naar basis modellen
            self.model_combo.clear()
            self.model_combo.addItems(["tiny", "base", "small", "medium", "large"])
    
    def on_translator_changed(self, translator_name: str):
        """Handle vertaler wijziging"""
        if translator_name == "LibreTranslate":
            config_manager.set("default_translator", "libretranslate")
        else:
            config_manager.set("default_translator", "none")
        
        self.translator_changed.emit(translator_name)
    
    def on_whisper_type_changed(self, type_text: str):
        """Handle whisper type wijziging (alleen Fast Whisper beschikbaar)"""
        # Forceer altijd Fast Whisper
        whisper_type = "fast"
        config_manager.set("whisper_type", whisper_type)
        self.update_models_for_type(whisper_type)
        self.whisper_type_changed.emit(type_text)
    
    def on_model_changed(self, model_text: str):
        """Handle model wijziging"""
        # Haal de echte model naam op uit de display text
        model_data = self.model_combo.currentData()
        if model_data:
            config_manager.set("whisper_model", model_data)
            self.model_changed.emit(model_data)
    
    def on_language_changed(self, language: str):
        """Handle taal wijziging"""
        config_manager.set("language", language.lower())
        self.language_changed.emit(language)
    
    def on_preserve_subtitles_changed(self, preserve_text: str):
        """Handle preserve subtitles wijziging"""
        preserve = "Behoud" in preserve_text
        config_manager.set("preserve_original_subtitles", preserve)
        self.preserve_subtitles_changed.emit(preserve)
    
    def get_current_settings(self) -> dict:
        """Haal huidige instellingen op"""
        return {
            "translator": self.translator_combo.currentText(),
            "whisper_type": self.whisper_type_combo.currentText(),
            "model": self.model_combo.currentData() or self.model_combo.currentText(),
            "language": self.language_combo.currentText(),
            "preserve_subtitles": "Behoud" in self.preserve_subtitles_combo.currentText(),
        }
    
    def freeze_settings(self):
        """Bevries alle instellingen tijdens verwerking"""
        for element in self.ui_elements:
            if hasattr(element, 'setEnabled'):
                element.setEnabled(False)
    
    def unfreeze_settings(self):
        """Ontdooi alle instellingen na verwerking"""
        for element in self.ui_elements:
            if hasattr(element, 'setEnabled'):
                element.setEnabled(True)
    
    def is_frozen(self) -> bool:
        """Controleer of settings bevroren zijn"""
        if self.ui_elements:
            return not self.ui_elements[0].isEnabled()
        return False
    
    def update_translator_status(self):
        """Update vertaler status"""
        try:
            # Test vertaler connectie
            server = config_manager.get_env("LIBRETRANSLATE_SERVER", "")
            if server:
                # Hier zou je een echte connectie test kunnen doen
                print(f"🌐 Vertaler status gecontroleerd voor server: {server}")
            else:
                print("⚠️ Geen vertaler server geconfigureerd")
        except Exception as e:
            print(f"⚠️ Fout bij updaten vertaler status: {e}") 