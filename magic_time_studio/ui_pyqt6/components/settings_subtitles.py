"""
Ondertitel Instellingen voor Settings Panel
Beheert SRT behoud en subtitle type configuratie
"""

from PyQt6.QtWidgets import QGroupBox, QFormLayout, QComboBox
from PyQt6.QtCore import pyqtSignal, QObject

class SubtitleSettings(QObject):
    """Beheert ondertitel instellingen in het settings panel"""
    
    # Signals - defined as class attributes
    preserve_subtitles_changed = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.preserve_subtitles_combo = None
        self.subtitle_type_combo = None
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup ondertitel UI componenten"""
        # Preserve original subtitles
        content_group = QGroupBox("📺 Ondertitels")
        content_layout = QFormLayout(content_group)
        
        self.preserve_subtitles_combo = QComboBox()
        self.preserve_subtitles_combo.addItems([
            "Behoud originele SRT (in brontaal)",
            "Verwijder originele SRT (alleen vertaalde behouden)"
        ])
        self.preserve_subtitles_combo.setCurrentText("Verwijder originele SRT (alleen vertaalde behouden)")  # Standaard: verwijder originele SRT
        self.preserve_subtitles_combo.currentTextChanged.connect(self._on_preserve_subtitles_changed)
        content_layout.addRow("Ondertitels:", self.preserve_subtitles_combo)
        
        # Subtitle type instelling (alleen softcoded beschikbaar)
        self.subtitle_type_combo = QComboBox()
        self.subtitle_type_combo.addItems([
            "Softcoded (externe track)"
        ])
        self.subtitle_type_combo.setEnabled(False)  # Uitgeschakeld omdat alleen softcoded beschikbaar is
        content_layout.addRow("Subtitle type:", self.subtitle_type_combo)
        
        content_group.setLayout(content_layout)
        self.content_group = content_group
    
    def _on_preserve_subtitles_changed(self, preserve_text: str):
        """Handle preserve subtitles wijziging"""
        preserve = preserve_text == "Behoud originele SRT (in brontaal)"
        
        if self.parent and hasattr(self.parent, '_is_debug_mode'):
            if self.parent._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: Preserve subtitles gewijzigd naar {preserve}")
        
        # Emit signal naar parent
        self.preserve_subtitles_changed.emit(preserve)
    
    def load_settings(self, config_mgr):
        """Laad ondertitel instellingen"""
        if not config_mgr:
            return
        
        # Originele ondertitels - laad uit configuratie
        preserve_subtitles = config_mgr.get("preserve_subtitles", False)  # Default: verwijder originele SRT
        if preserve_subtitles:
            self.preserve_subtitles_combo.setCurrentText("Behoud originele SRT (in brontaal)")
        else:
            self.preserve_subtitles_combo.setCurrentText("Verwijder originele SRT (alleen vertaalde behouden)")
        
        if self.parent and hasattr(self.parent, '_is_debug_mode'):
            if self.parent._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: Preserve subtitles geladen: {preserve_subtitles}")
        
        # Subtitle type instelling (altijd softcoded)
        subtitle_type = "softcoded"  # Altijd softcoded, hardcoded wordt niet meer ondersteund
        self.subtitle_type_combo.setCurrentText("Softcoded (externe track)")
        
        if self.parent and hasattr(self.parent, '_is_debug_mode'):
            if self.parent._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: Subtitle type geladen: {subtitle_type} (altijd softcoded)")
    
    def get_settings(self, config_mgr):
        """Krijg huidige ondertitel instellingen"""
        # Subtitle type instelling (altijd softcoded)
        subtitle_type = "softcoded"  # Altijd softcoded, hardcoded wordt niet meer ondersteund
        
        if self.parent and hasattr(self.parent, '_is_debug_mode'):
            if self.parent._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: Subtitle type uit UI: {subtitle_type} (altijd softcoded)")
        
        # Preserve subtitles instelling - lees uit UI
        preserve_subtitles = self.preserve_subtitles_combo.currentText() == "Behoud originele SRT (in brontaal)"
        
        if self.parent and hasattr(self.parent, '_is_debug_mode'):
            if self.parent._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: Preserve subtitles uit UI: {preserve_subtitles}")
        
        return {
            "preserve_subtitles": preserve_subtitles,
            "subtitle_type": subtitle_type
        }
    
    def save_settings(self, config_mgr):
        """Sla ondertitel instellingen op"""
        if not config_mgr:
            return
        
        settings = self.get_settings(config_mgr)
        
        # Update config manager - sla op in .env
        config_mgr.set_env("PRESERVE_SUBTITLES", str(settings["preserve_subtitles"]).lower())
        
        if self.parent and hasattr(self.parent, '_is_debug_mode'):
            if self.parent._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: Preserve subtitles opgeslagen in config: {settings['preserve_subtitles']}")
    
    def freeze(self):
        """Bevries ondertitel instellingen"""
        if self.preserve_subtitles_combo:
            self.preserve_subtitles_combo.setEnabled(False)
        if self.subtitle_type_combo:
            self.subtitle_type_combo.setEnabled(False)
    
    def unfreeze(self):
        """Ontdooit ondertitel instellingen"""
        if self.preserve_subtitles_combo:
            self.preserve_subtitles_combo.setEnabled(True)
        if self.subtitle_type_combo:
            self.subtitle_type_combo.setEnabled(False)  # Altijd uitgeschakeld
    
    def is_frozen(self):
        """Controleer of ondertitel instellingen bevroren zijn"""
        return (not self.preserve_subtitles_combo.isEnabled() if self.preserve_subtitles_combo else False) or \
               (not self.subtitle_type_combo.isEnabled() if self.subtitle_type_combo else False)
