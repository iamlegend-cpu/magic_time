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
# from magic_time_studio.ui_pyqt6.features.processing_mode_manager import processing_mode_manager # Verwijderd

class SettingsPanel(QWidget):
    """Settings panel component"""
    
    # Signals
    translator_changed = pyqtSignal(str)
    model_changed = pyqtSignal(str)
    language_changed = pyqtSignal(str)
    content_type_changed = pyqtSignal(str)
    preserve_subtitles_changed = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_current_settings()
        
        # Sla alle UI elementen op voor later gebruik
        self.ui_elements = [
            self.translator_combo,
            self.model_combo,
            self.language_combo,
            self.content_combo,
            self.preserve_subtitles_combo
        ]
        
        # Registreer bij ProcessingModeManager
        # processing_mode_manager.register_settings_panel(self) # Verwijderd
    
    def setup_ui(self):
        """Setup de UI"""
        layout = QVBoxLayout(self)
        
        # Vertaler status
        self.translator_status_label = QLabel(f"🌐 Vertaler: {translator.get_current_service().upper()}")
        self.translator_status_label.setStyleSheet("font-weight: bold; color: #4caf50;")
        layout.addWidget(self.translator_status_label)
        
        # Vertaler selectie
        translator_layout = QHBoxLayout()
        translator_layout.addWidget(QLabel("Vertaler:"))
        
        self.translator_combo = QComboBox()
        self.translator_combo.addItems([
            "Geen vertaling", "LibreTranslate"
        ])
        self.translator_combo.currentTextChanged.connect(self.on_translator_changed)
        translator_layout.addWidget(self.translator_combo)
        
        layout.addLayout(translator_layout)
        
        # Whisper model
        model_layout = QHBoxLayout()
        model_layout.addWidget(QLabel("🎤 Whisper model:"))
        
        self.model_combo = QComboBox()
        self.model_combo.addItems([
            "tiny", "base", "small", "medium", "large"
        ])
        self.model_combo.currentTextChanged.connect(self.on_model_changed)
        model_layout.addWidget(self.model_combo)
        
        layout.addLayout(model_layout)
        
        # Taal selectie (voor Whisper - gesproken taal)
        language_layout = QHBoxLayout()
        language_layout.addWidget(QLabel("Gesproken taal:"))
        
        self.language_combo = QComboBox()
        self.language_combo.addItems([
            "Engels", "Nederlands", "Duits", "Frans", "Spaans"
        ])
        self.language_combo.currentTextChanged.connect(self.on_language_changed)
        language_layout.addWidget(self.language_combo)
        
        layout.addLayout(language_layout)
        
        # Vertaling info label
        translation_info = QLabel("ℹ️ Vertaling gaat altijd naar Nederlands")
        translation_info.setStyleSheet("color: #888; font-size: 11px; font-style: italic;")
        layout.addWidget(translation_info)
        
        # Content type
        content_layout = QHBoxLayout()
        content_layout.addWidget(QLabel("Content type:"))
        
        self.content_combo = QComboBox()
        self.content_combo.addItems([
            "Auto detectie", "Video", "Audio", "Podcast", "Interview"
        ])
        self.content_combo.currentTextChanged.connect(self.on_content_type_changed)
        content_layout.addWidget(self.content_combo)
        
        layout.addLayout(content_layout)
        
        # Originele ondertitels optie
        subtitle_layout = QHBoxLayout()
        subtitle_layout.addWidget(QLabel("📝 Originele ondertitels:"))
        
        self.preserve_subtitles_combo = QComboBox()
        self.preserve_subtitles_combo.addItems([
            "Behouden", "Verwijderen"
        ])
        self.preserve_subtitles_combo.currentTextChanged.connect(self.on_preserve_subtitles_changed)
        subtitle_layout.addWidget(self.preserve_subtitles_combo)
        
        layout.addLayout(subtitle_layout)
        
        # Subtitle info label
        subtitle_info = QLabel("ℹ️ Behoud originele ondertitels in het video bestand")
        subtitle_info.setStyleSheet("color: #888; font-size: 11px; font-style: italic;")
        layout.addWidget(subtitle_info)
        
        # Voeg wat ruimte toe
        layout.addStretch()
    
    def load_current_settings(self):
        """Laad huidige instellingen"""
        # Vertaler
        current_translator = config_manager.get("default_translator", "libretranslate")
        if current_translator == "libretranslate":
            self.translator_combo.setCurrentText("LibreTranslate")
        else:
            self.translator_combo.setCurrentText("Geen vertaling")
        
        # Whisper model
        current_model = config_manager.get("default_whisper_model", "large")
        self.model_combo.setCurrentText(current_model)
        
        # Taal (standaard Engels)
        self.language_combo.setCurrentText("Engels")
        
        # Content type (standaard auto detectie)
        self.content_combo.setCurrentText("Auto detectie")
        
        # Originele ondertitels (standaard behouden)
        preserve_subtitles = config_manager.get("preserve_original_subtitles", True)
        if preserve_subtitles:
            self.preserve_subtitles_combo.setCurrentText("Behouden")
        else:
            self.preserve_subtitles_combo.setCurrentText("Verwijderen")
    
    def on_translator_changed(self, translator_name: str):
        """Vertaler gewijzigd"""
        if translator_name == "LibreTranslate":
            translator.set_service("libretranslate")
            config_manager.set("default_translator", "libretranslate")
        else:
            translator.set_service("none")
            config_manager.set("default_translator", "none")
        
        self.translator_changed.emit(translator_name)
        self.update_translator_status()
    
    def on_model_changed(self, model: str):
        """Whisper model gewijzigd"""
        config_manager.set("default_whisper_model", model)
        self.model_changed.emit(model)
    
    def on_language_changed(self, language: str):
        """Taal gewijzigd"""
        self.language_changed.emit(language)
    
    def on_content_type_changed(self, content_type: str):
        """Content type gewijzigd"""
        self.content_type_changed.emit(content_type)
    
    def on_preserve_subtitles_changed(self, preserve_text: str):
        """Originele ondertitels optie gewijzigd"""
        preserve_subtitles = preserve_text == "Behouden"
        config_manager.set("preserve_original_subtitles", preserve_subtitles)
        self.preserve_subtitles_changed.emit(preserve_subtitles)
    
    def update_translator_status(self):
        """Update vertaler status label"""
        self.translator_status_label.setText(f"🌐 Vertaler: {translator.get_current_service().upper()}")
    
    def get_current_settings(self) -> dict:
        """Haal huidige instellingen op"""
        # Map taalnamen naar taal codes voor Whisper (gesproken taal)
        language_mapping = {
            "Engels": "en",
            "Nederlands": "nl", 
            "Duits": "de",
            "Frans": "fr",
            "Spaans": "es"
        }
        
        selected_language = self.language_combo.currentText()
        whisper_language = language_mapping.get(selected_language, "en")
        
        # Target language is altijd Nederlands voor vertaling
        target_language = "nl"
        
        return {
            "translator": self.translator_combo.currentText(),
            "whisper_model": self.model_combo.currentText(),
            "language": self.language_combo.currentText(),
            "content_type": self.content_combo.currentText(),
            "enable_translation": self.translator_combo.currentText() != "Geen vertaling",
            "target_language": target_language,
            "preserve_original_subtitles": self.preserve_subtitles_combo.currentText() == "Behouden"
        } 