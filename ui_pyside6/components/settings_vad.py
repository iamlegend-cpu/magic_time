"""
VAD (Voice Activity Detection) Instellingen voor Settings Panel
Modulaire versie volgens de project structuur
"""

from PySide6.QtWidgets import (
    QGroupBox, QFormLayout, QCheckBox, QComboBox, QSlider, QLabel, 
    QSpinBox, QDoubleSpinBox, QPushButton, QHBoxLayout, QVBoxLayout,
    QProgressBar, QTextEdit, QMessageBox, QFileDialog, QApplication
)
from PySide6.QtCore import Qt, Signal, QThread, QObject
from PySide6.QtGui import QFont

# ============================================================================
# VAD METHOD MAPPING
# ============================================================================

class VADMethodMapping:
    """Mapping van UI namen naar WhisperX methoden"""
    
    VAD_METHOD_MAPPING = {
        "Silero (snel)": "silero",
        "Pyannote (nauwkeurig)": "pyannote", 
        "Auditok (lichtgewicht)": "auditok",
        "Energie-gebaseerd": "energy",
        "Auto-selectie (aanbevolen)": "auto"
    }
    
    @classmethod
    def get_whisperx_method(cls, ui_method: str) -> str:
        """Converteer UI methode naam naar WhisperX methode"""
        return cls.VAD_METHOD_MAPPING.get(ui_method, "pyannote")
    
    @classmethod
    def get_ui_method(cls, whisperx_method: str) -> str:
        """Converteer WhisperX methode naar UI methode naam"""
        for ui_name, wx_name in cls.VAD_METHOD_MAPPING.items():
            if wx_name == whisperx_method:
                return ui_name
        return "Pyannote (nauwkeurig)"  # Fallback

# ============================================================================
# VAD SETTINGS MANAGER
# ============================================================================

class VADSettingsManager:
    """Beheert VAD instellingen en configuratie"""
    
    def __init__(self, config_mgr=None):
        self.config_mgr = config_mgr
        self._default_settings = {
            "vad_enabled": True,
            "vad_method": "Pyannote (nauwkeurig)",
            "vad_threshold": 0.5,
            "vad_onset": 0.5,
            "vad_chunk_size": 30,
            "vad_min_speech": 0.5,
            "vad_min_silence": 0.5,
        }
    
    def get_settings(self) -> dict:
        """Haal VAD instellingen op"""
        try:
            if not self.config_mgr:
                # Gebruik standaard instellingen en voeg WhisperX methode toe
                settings = self._default_settings.copy()
                settings["vad_method_whisperx"] = VADMethodMapping.get_whisperx_method(settings["vad_method"])
                return settings
            
            # Haal instellingen op uit config manager
            settings = {
                "vad_enabled": self.config_mgr.get_env("VAD_ENABLED", "true").lower() == "true",
                "vad_method": self.config_mgr.get_env("VAD_METHOD", "Pyannote (nauwkeurig)"),
                "vad_threshold": float(self.config_mgr.get_env("VAD_THRESHOLD", "0.5")),
                "vad_onset": float(self.config_mgr.get_env("VAD_ONSET", "0.5")),
                "vad_chunk_size": int(self.config_mgr.get_env("VAD_CHUNK_SIZE", "30")),
                "vad_min_speech": float(self.config_mgr.get_env("VAD_MIN_SPEECH", "0.5")),
                "vad_min_silence": float(self.config_mgr.get_env("VAD_MIN_SILENCE", "0.5")),
            }
            
            # Voeg WhisperX methode toe
            settings["vad_method_whisperx"] = VADMethodMapping.get_whisperx_method(settings["vad_method"])
            
            return settings
        except Exception as e:
            print(f"⚠️ Fout bij laden VAD instellingen: {e}")
            # Gebruik standaard instellingen en voeg WhisperX methode toe
            settings = self._default_settings.copy()
            settings["vad_method_whisperx"] = VADMethodMapping.get_whisperx_method(settings["vad_method"])
            return settings
    
    def save_settings(self, settings: dict) -> bool:
        """Sla VAD instellingen op"""
        if not self.config_mgr:
            return False
        
        try:
            # Update config manager
            self.config_mgr.set_env("VAD_ENABLED", str(settings["vad_enabled"]).lower())
            self.config_mgr.set_env("VAD_METHOD", settings["vad_method"])
            self.config_mgr.set_env("VAD_THRESHOLD", str(settings["vad_threshold"]))
            self.config_mgr.set_env("VAD_ONSET", str(settings["vad_onset"]))
            self.config_mgr.set_env("VAD_CHUNK_SIZE", str(settings["vad_chunk_size"]))
            self.config_mgr.set_env("VAD_MIN_SPEECH", str(settings["vad_min_speech"]))
            self.config_mgr.set_env("VAD_MIN_SILENCE", str(settings["vad_min_silence"]))
            
            return True
        except Exception as e:
            print(f"❌ Fout bij opslaan VAD instellingen: {e}")
            return False

# ============================================================================
# VAD TEST ENGINE
# ============================================================================

class VADTestEngine(QObject):
    """Engine voor VAD testen en optimalisatie"""
    
    test_completed = Signal(dict)
    optimize_completed = Signal(dict)
    
    def __init__(self):
        super().__init__()
    
    def test_vad_settings(self, media_file: str, vad_settings: dict):
        """Test VAD instellingen op media bestand"""
        self.test_thread = VADTestThread(media_file, vad_settings)
        self.test_thread.test_completed.connect(self.test_completed.emit)
        self.test_thread.start()
    
    def optimize_vad_settings(self, media_file: str):
        """Optimaliseer VAD instellingen voor media bestand"""
        self.optimize_thread = VADOptimizeThread(media_file)
        self.optimize_thread.optimize_completed.connect(self.optimize_completed.emit)
        self.optimize_thread.start()

class VADTestThread(QThread):
    """Thread voor VAD testen"""
    
    test_completed = Signal(dict)
    
    def __init__(self, media_file: str, vad_settings: dict):
        super().__init__()
        self.media_file = media_file
        self.vad_settings = vad_settings
    
    def run(self):
        """Voer VAD test uit"""
        try:
            result = self._perform_vad_test()
            self.test_completed.emit(result)
        except Exception as e:
            self.test_completed.emit({"success": False, "error": str(e)})
    
    def _perform_vad_test(self) -> dict:
        """Voer daadwerkelijke VAD test uit"""
        # Implementatie van VAD test logica
        # Voor nu een simulatie
        return {
            "success": True,
            "vad_method": self.vad_settings.get("vad_method", "Onbekend"),
            "vad_quality": "Simulatie - geen echte analyse",
            "note": "VAD test simulatie voltooid"
        }

class VADOptimizeThread(QThread):
    """Thread voor VAD optimalisatie"""
    
    optimize_completed = Signal(dict)
    
    def __init__(self, media_file: str):
        super().__init__()
        self.media_file = media_file
    
    def run(self):
        """Voer VAD optimalisatie uit"""
        try:
            result = self._perform_vad_optimization()
            self.optimize_completed.emit(result)
        except Exception as e:
            self.optimize_completed.emit({"success": False, "error": str(e)})
    
    def _perform_vad_optimization(self) -> dict:
        """Voer daadwerkelijke VAD optimalisatie uit"""
        # Implementatie van VAD optimalisatie logica
        # Voor nu een simulatie
        return {
            "success": True,
            "recommendation": "Simulatie optimalisatie",
            "note": "VAD optimalisatie simulatie voltooid"
        }

# ============================================================================
# VAD UI COMPONENTS
# ============================================================================

class VADMethodSelector:
    """UI component voor VAD methode selectie"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.combo = QComboBox()
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup VAD methode selector UI"""
        self.combo.addItems([
            "Pyannote (nauwkeurig)", 
            "Silero (snel)", 
            "Auditok (lichtgewicht)",
            "Energie-gebaseerd",
            "Auto-selectie (aanbevolen)"
        ])
        self.combo.setToolTip("Kies VAD methode: Pyannote is nauwkeuriger, Silero is snel, Auditok is lichtgewicht")
    
    def get_current_method(self) -> str:
        """Haal huidige geselecteerde methode op"""
        return self.combo.currentText()
    
    def set_current_method(self, method: str):
        """Zet huidige methode"""
        index = self.combo.findText(method)
        if index >= 0:
            self.combo.setCurrentIndex(index)

class VADThresholdSlider:
    """UI component voor VAD threshold slider"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.label = QLabel("0.5")
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup threshold slider UI"""
        self.slider.setRange(1, 99)
        self.slider.setValue(50)
        self.slider.setToolTip("VAD threshold: hoger = minder gevoelig voor geluid")
        self.slider.valueChanged.connect(self._on_value_changed)
        
        self.label.setMinimumWidth(40)
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight)
    
    def _on_value_changed(self, value: int):
        """Handle slider waarde wijziging"""
        threshold = value / 100.0
        self.label.setText(f"{threshold:.2f}")
    
    def get_value(self) -> float:
        """Haal huidige waarde op"""
        return self.slider.value() / 100.0
    
    def set_value(self, value: float):
        """Zet waarde"""
        self.slider.setValue(int(value * 100))

class VADOnsetSlider:
    """UI component voor VAD onset slider"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.label = QLabel("0.5")
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup onset slider UI"""
        self.slider.setRange(1, 99)
        self.slider.setValue(50)
        self.slider.setToolTip("VAD onset: wanneer spraak begint te detecteren")
        self.slider.valueChanged.connect(self._on_value_changed)
        
        self.label.setMinimumWidth(40)
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight)
    
    def _on_value_changed(self, value: int):
        """Handle slider waarde wijziging"""
        onset = value / 100.0
        self.label.setText(f"{onset:.2f}")
    
    def get_value(self) -> float:
        """Haal huidige waarde op"""
        return self.slider.value() / 100.0
    
    def set_value(self, value: float):
        """Zet waarde"""
        self.slider.setValue(int(value * 100))

class VADParameterSpinner:
    """UI component voor VAD parameter spinners"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.chunk_size_spin = QSpinBox()
        self.min_speech_spin = QDoubleSpinBox()
        self.min_silence_spin = QDoubleSpinBox()
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup parameter spinners UI"""
        # Chunk size
        self.chunk_size_spin.setRange(5, 60)
        self.chunk_size_spin.setValue(30)
        self.chunk_size_spin.setSuffix(" sec")
        self.chunk_size_spin.setToolTip("Chunk grootte voor VAD verwerking")
        
        # Min speech duration
        self.min_speech_spin.setRange(0.1, 5.0)
        self.min_speech_spin.setValue(0.5)
        self.min_speech_spin.setSuffix(" sec")
        self.min_speech_spin.setToolTip("Minimale spraak duur")
        
        # Min silence duration
        self.min_silence_spin.setRange(0.1, 5.0)
        self.min_silence_spin.setValue(0.5)
        self.min_silence_spin.setSuffix(" sec")
        self.min_silence_spin.setToolTip("Minimale stilte duur")
    
    def get_values(self) -> dict:
        """Haal alle waarden op"""
        return {
            "vad_chunk_size": self.chunk_size_spin.value(),
            "vad_min_speech": self.min_speech_spin.value(),
            "vad_min_silence": self.min_silence_spin.value(),
        }
    
    def set_values(self, values: dict):
        """Zet alle waarden"""
        if "vad_chunk_size" in values:
            self.chunk_size_spin.setValue(values["vad_chunk_size"])
        if "vad_min_speech" in values:
            self.min_speech_spin.setValue(values["vad_min_speech"])
        if "vad_min_silence" in values:
            self.min_silence_spin.setValue(values["vad_min_silence"])

class VADToolButtons:
    """UI component voor VAD tool knoppen"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.test_button = QPushButton("🧪 Test VAD")
        self.optimize_button = QPushButton("🔧 Optimaliseer VAD")
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup tool knoppen UI"""
        self.test_button.setToolTip("Test huidige VAD instellingen op een kort audio fragment")
        self.optimize_button.setToolTip("Vind beste VAD instellingen voor jouw audio")
    
    def set_testing_state(self, is_testing: bool):
        """Zet test status"""
        if is_testing:
            self.test_button.setText("⏳ Test bezig...")
            self.test_button.setEnabled(False)
        else:
            self.test_button.setText("🧪 Test VAD")
            self.test_button.setEnabled(True)
    
    def set_optimizing_state(self, is_optimizing: bool):
        """Zet optimalisatie status"""
        if is_optimizing:
            self.optimize_button.setText("⏳ Optimalisatie bezig...")
            self.optimize_button.setEnabled(False)
        else:
            self.optimize_button.setText("🔧 Optimaliseer VAD")
            self.optimize_button.setEnabled(True)

# ============================================================================
# MAIN VAD SETTINGS CLASS
# ============================================================================

class VadSettings(QObject):
    """Hoofdklasse voor VAD instellingen - modulaire versie"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        # Initialiseer componenten
        self.settings_manager = VADSettingsManager()
        self.test_engine = VADTestEngine()
        
        # UI componenten
        self.method_selector = VADMethodSelector(parent)
        self.threshold_slider = VADThresholdSlider(parent)
        self.onset_slider = VADOnsetSlider(parent)
        self.parameter_spinner = VADParameterSpinner(parent)
        self.tool_buttons = VADToolButtons(parent)
        
        # Verbind signals
        self._connect_signals()
        
        # Setup UI
        self.vad_group = self._create_ui()
    
    def _connect_signals(self):
        """Verbind alle signals"""
        self.test_engine.test_completed.connect(self._on_vad_test_completed)
        self.test_engine.optimize_completed.connect(self._on_vad_optimize_completed)
        
        self.tool_buttons.test_button.clicked.connect(self._on_vad_test_clicked)
        self.tool_buttons.optimize_button.clicked.connect(self._on_vad_optimize_clicked)
    
    def _create_ui(self) -> QGroupBox:
        """Maak VAD UI aan"""
        vad_group = QGroupBox("🎯 Voice Activity Detection (Altijd ingeschakeld)")
        vad_layout = QFormLayout(vad_group)
        
        # VAD methode selectie
        vad_layout.addRow("VAD Methode:", self.method_selector.combo)
        
        # VAD threshold instellingen
        threshold_layout = QHBoxLayout()
        threshold_layout.addWidget(self.threshold_slider.slider)
        threshold_layout.addWidget(self.threshold_slider.label)
        vad_layout.addRow("VAD Threshold:", threshold_layout)
        
        # VAD onset instellingen
        onset_layout = QHBoxLayout()
        onset_layout.addWidget(self.onset_slider.slider)
        onset_layout.addWidget(self.onset_slider.label)
        vad_layout.addRow("VAD Onset:", onset_layout)
        
        # VAD parameters
        vad_layout.addRow("Chunk Grootte:", self.parameter_spinner.chunk_size_spin)
        vad_layout.addRow("Min Spraak Duur:", self.parameter_spinner.min_speech_spin)
        vad_layout.addRow("Min Stilte Duur:", self.parameter_spinner.min_silence_spin)
        
        # VAD tools
        vad_tools_layout = QHBoxLayout()
        vad_tools_layout.addWidget(self.tool_buttons.test_button)
        vad_tools_layout.addWidget(self.tool_buttons.optimize_button)
        vad_layout.addRow("VAD Tools:", vad_tools_layout)
        
        vad_group.setLayout(vad_layout)
        return vad_group
    
    def _on_vad_test_clicked(self):
        """Handle VAD test knop klik"""
        try:
            print("🧪 Start VAD test...")
            
            # Haal huidige instellingen op
            vad_settings = self.get_current_settings()
            print(f"🔧 Test VAD instellingen: {vad_settings}")
            
            # Vraag gebruiker om media bestand te selecteren
            media_file, _ = QFileDialog.getOpenFileName(
                self.parent,
                "Selecteer video of audio bestand voor VAD test",
                "",
                "Media bestanden (*.mp4 *.avi *.mkv *.mov *.mp3 *.wav *.m4a *.flac *.ogg);;Alle bestanden (*.*)"
            )
            
            if not media_file:
                print("❌ Geen bestand geselecteerd")
                return
            
            print(f"🎵 Geselecteerd bestand: {media_file}")
            
            # Start VAD test
            self.tool_buttons.set_testing_state(True)
            self.test_engine.test_vad_settings(media_file, vad_settings)
            
        except Exception as e:
            print(f"❌ Fout bij starten VAD test: {e}")
            import traceback
            traceback.print_exc()
    
    def _on_vad_optimize_clicked(self):
        """Handle VAD optimalisatie knop klik"""
        try:
            print("🔧 Start VAD optimalisatie...")
            
            # Vraag gebruiker om media bestand te selecteren
            media_file, _ = QFileDialog.getOpenFileName(
                self.parent,
                "Selecteer video of audio bestand voor VAD optimalisatie",
                "",
                "Media bestanden (*.mp4 *.avi *.mkv *.mov *.mp3 *.wav *.m4a *.flac *.ogg);;Alle bestanden (*.*)"
            )
            
            if not media_file:
                print("❌ Geen bestand geselecteerd")
                return
            
            print(f"🎵 Geselecteerd bestand: {media_file}")
            
            # Start VAD optimalisatie
            self.tool_buttons.set_optimizing_state(True)
            self.test_engine.optimize_vad_settings(media_file)
            
        except Exception as e:
            print(f"❌ Fout bij starten VAD optimalisatie: {e}")
            import traceback
            traceback.print_exc()
    
    def _on_vad_test_completed(self, result: dict):
        """VAD test voltooid"""
        try:
            # Herstel knop status
            self.tool_buttons.set_testing_state(False)
            
            if result.get("success"):
                print("✅ VAD test voltooid!")
                self._show_test_results(result)
            else:
                print(f"❌ VAD test gefaald: {result.get('error')}")
                self._show_error("VAD Test Fout", f"VAD test gefaald:\n{result.get('error')}")
                
        except Exception as e:
            print(f"❌ Fout bij verwerken VAD test resultaten: {e}")
    
    def _on_vad_optimize_completed(self, result: dict):
        """VAD optimalisatie voltooid"""
        try:
            # Herstel knop status
            self.tool_buttons.set_optimizing_state(False)
            
            if result.get("success"):
                print("✅ VAD optimalisatie voltooid!")
                self._apply_optimized_settings(result)
                self._show_optimization_results(result)
            else:
                print(f"❌ VAD optimalisatie gefaald: {result.get('error')}")
                self._show_error("VAD Optimalisatie Fout", f"VAD optimalisatie gefaald:\n{result.get('error')}")
                
        except Exception as e:
            print(f"❌ Fout bij verwerken VAD optimalisatie resultaten: {e}")
    
    def _show_test_results(self, result: dict):
        """Toon VAD test resultaten"""
        message = f"""VAD Test Resultaten:

Methode: {result.get('vad_method', 'Onbekend')}
Kwaliteit: {result.get('vad_quality', 'Onbekend')}

{result.get('note', '')}"""
        
        QMessageBox.information(self.parent, "VAD Test Resultaten", message)
    
    def _show_optimization_results(self, result: dict):
        """Toon VAD optimalisatie resultaten"""
        message = f"""VAD Optimalisatie Voltooid!

{result.get('recommendation', 'Optimalisatie voltooid')}

{result.get('note', '')}"""
        
        QMessageBox.information(self.parent, "VAD Optimalisatie Voltooid", message)
    
    def _show_error(self, title: str, message: str):
        """Toon fout melding"""
        QMessageBox.warning(self.parent, title, message)
    
    def _apply_optimized_settings(self, result: dict):
        """Pas geoptimaliseerde instellingen toe"""
        # Implementatie voor het toepassen van geoptimaliseerde instellingen
        # Kan worden uitgebreid op basis van de optimalisatie resultaten
        pass
    
    def load_settings(self, config_mgr):
        """Laad VAD instellingen"""
        self.settings_manager.config_mgr = config_mgr
        settings = self.settings_manager.get_settings()
        
        # Pas instellingen toe op UI componenten
        self.method_selector.set_current_method(settings["vad_method"])
        self.threshold_slider.set_value(settings["vad_threshold"])
        self.onset_slider.set_value(settings["vad_onset"])
        self.parameter_spinner.set_values(settings)
        
        if self.parent and hasattr(self.parent, '_is_debug_mode'):
            if self.parent._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: VAD instellingen geladen")
    
    def get_current_settings(self) -> dict:
        """Haal huidige VAD instellingen op uit UI"""
        settings = {
            "vad_enabled": True,  # VAD is altijd ingeschakeld
            "vad_method": self.method_selector.get_current_method(),
            "vad_threshold": self.threshold_slider.get_value(),
            "vad_onset": self.onset_slider.get_value(),
            **self.parameter_spinner.get_values()
        }
        
        # Voeg WhisperX methode toe
        settings["vad_method_whisperx"] = VADMethodMapping.get_whisperx_method(settings["vad_method"])
        
        return settings
    
    def save_settings(self, config_mgr):
        """Sla VAD instellingen op"""
        self.settings_manager.config_mgr = config_mgr
        settings = self.get_current_settings()
        
        success = self.settings_manager.save_settings(settings)
        
        if self.parent and hasattr(self.parent, '_is_debug_mode'):
            if self.parent._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: VAD instellingen opgeslagen: {success}")
        
        return success
    
    def freeze(self):
        """Bevries VAD instellingen"""
        self.method_selector.combo.setEnabled(False)
        self.threshold_slider.slider.setEnabled(False)
        self.onset_slider.slider.setEnabled(False)
        self.parameter_spinner.chunk_size_spin.setEnabled(False)
        self.parameter_spinner.min_speech_spin.setEnabled(False)
        self.parameter_spinner.min_silence_spin.setEnabled(False)
        self.tool_buttons.test_button.setEnabled(False)
        self.tool_buttons.optimize_button.setEnabled(False)
    
    def unfreeze(self):
        """Ontdooit VAD instellingen"""
        self.method_selector.combo.setEnabled(True)
        self.threshold_slider.slider.setEnabled(True)
        self.onset_slider.slider.setEnabled(True)
        self.parameter_spinner.chunk_size_spin.setEnabled(True)
        self.parameter_spinner.min_speech_spin.setEnabled(True)
        self.parameter_spinner.min_silence_spin.setEnabled(True)
        self.tool_buttons.test_button.setEnabled(True)
        self.tool_buttons.optimize_button.setEnabled(True)
    
    def is_frozen(self) -> bool:
        """Controleer of VAD instellingen bevroren zijn"""
        return not self.method_selector.combo.isEnabled()
