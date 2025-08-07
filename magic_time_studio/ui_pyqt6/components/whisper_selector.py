"""
Whisper Selector Component voor Magic Time Studio
UI component voor het kiezen tussen standaard Whisper en Fast Whisper
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QComboBox, QPushButton, QGroupBox, QGridLayout,
    QProgressBar, QTextEdit, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QTimer
from PyQt6.QtGui import QFont, QPalette, QColor

# Absolute imports
try:
    from magic_time_studio.processing.whisper_manager import whisper_manager
    from magic_time_studio.core.logging import logger
    from magic_time_studio.core.config import config_manager
except ImportError:
    # Fallback voor directe import
    import sys
    sys.path.append('..')
    from processing.whisper_manager import whisper_manager
    from core.logging import logger
    from core.config import config_manager

class WhisperSelectorWidget(QWidget):
    """Widget voor het selecteren van Whisper type en model"""
    
    # Signals
    whisper_changed = pyqtSignal(str, str)  # type, model
    model_loaded = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_whisper_type = "fast"
        self.current_model = "large-v3-turbo"
        self.is_loading = False
        
        self.setup_ui()
        self.load_available_options()
        self.update_status()
    
    def setup_ui(self):
        """Setup de UI componenten"""
        layout = QVBoxLayout()
        
        # Hoofdtitel
        title = QLabel("🤖 Whisper Configuratie")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Whisper Type Selector
        type_group = QGroupBox("Whisper Type")
        type_layout = QVBoxLayout()
        
        # Type selector
        type_selector_layout = QHBoxLayout()
        type_selector_layout.addWidget(QLabel("Type:"))
        
        self.type_combo = QComboBox()
        self.type_combo.currentTextChanged.connect(self.on_type_changed)
        type_selector_layout.addWidget(self.type_combo)
        
        type_layout.addLayout(type_selector_layout)
        
        # Type beschrijving
        self.type_description = QLabel()
        self.type_description.setWordWrap(True)
        self.type_description.setStyleSheet("color: #888888; font-style: italic;")
        type_layout.addWidget(self.type_description)
        
        type_group.setLayout(type_layout)
        layout.addWidget(type_group)
        
        # Model Selector
        model_group = QGroupBox("Model Selectie")
        model_layout = QVBoxLayout()
        
        # Model selector
        model_selector_layout = QHBoxLayout()
        model_selector_layout.addWidget(QLabel("Model:"))
        
        self.model_combo = QComboBox()
        self.model_combo.currentTextChanged.connect(self.on_model_changed)
        model_selector_layout.addWidget(self.model_combo)
        
        model_layout.addLayout(model_selector_layout)
        
        # Model beschrijving
        self.model_description = QLabel()
        self.model_description.setWordWrap(True)
        self.model_description.setStyleSheet("color: #888888; font-style: italic;")
        model_layout.addWidget(self.model_description)
        
        model_group.setLayout(model_layout)
        layout.addWidget(model_group)
        
        # Control Buttons
        button_layout = QHBoxLayout()
        
        self.load_button = QPushButton("🔄 Laad Model")
        self.load_button.clicked.connect(self.load_model)
        button_layout.addWidget(self.load_button)
        
        self.switch_button = QPushButton("🔄 Wissel Type")
        self.switch_button.clicked.connect(self.switch_whisper_type)
        button_layout.addWidget(self.switch_button)
        
        layout.addLayout(button_layout)
        
        # Status
        status_group = QGroupBox("Status")
        status_layout = QVBoxLayout()
        
        self.status_label = QLabel("Niet geladen")
        self.status_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")
        status_layout.addWidget(self.status_label)
        
        # Progress bar voor laden
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        status_layout.addWidget(self.progress_bar)
        
        # Model info
        self.model_info = QTextEdit()
        self.model_info.setMaximumHeight(100)
        self.model_info.setReadOnly(True)
        self.model_info.setStyleSheet("""
            QTextEdit {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 1px solid #404040;
                border-radius: 4px;
                padding: 8px;
            }
        """)
        status_layout.addWidget(self.model_info)
        
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        # Performance vergelijking
        perf_group = QGroupBox("Performance Vergelijking")
        perf_layout = QVBoxLayout()
        
        self.perf_text = QLabel()
        self.perf_text.setWordWrap(True)
        self.perf_text.setStyleSheet("color: #4caf50;")
        perf_layout.addWidget(self.perf_text)
        
        perf_group.setLayout(perf_layout)
        layout.addWidget(perf_group)
        
        self.setLayout(layout)
    
    def load_available_options(self):
        """Laad beschikbare Whisper types en modellen"""
        try:
            # Laad beschikbare types
            available_types = whisper_manager.get_available_whisper_types()
            self.type_combo.clear()
            
            for whisper_type in available_types:
                if whisper_type == "standard":
                    self.type_combo.addItem("🐌 Standaard Whisper", "standard")
                elif whisper_type == "fast":
                    self.type_combo.addItem("🚀 Fast Whisper", "fast")
            
            # Stel default type in
            default_type = config_manager.get_env("WHISPER_TYPE", "fast")
            index = self.type_combo.findData(default_type)
            if index >= 0:
                self.type_combo.setCurrentIndex(index)
                self.current_whisper_type = default_type
            
            # Update modellen voor huidig type
            self.update_models()
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij laden Whisper opties: {e}")
    
    def update_models(self):
        """Update beschikbare modellen voor huidig type"""
        try:
            self.model_combo.clear()
            
            available_models = whisper_manager.get_available_models(self.current_whisper_type)
            
            for model in available_models:
                display_name = model
                if model == "large-v3-turbo":
                    display_name = "🚀 Large V3 Turbo (Aanbevolen)"
                elif model == "large":
                    display_name = "📊 Large"
                elif model == "medium":
                    display_name = "📈 Medium"
                elif model == "small":
                    display_name = "📉 Small"
                elif model == "base":
                    display_name = "📋 Base"
                elif model == "tiny":
                    display_name = "⚡ Tiny"
                
                self.model_combo.addItem(display_name, model)
            
            # Stel default model in
            if self.current_whisper_type == "fast":
                default_model = config_manager.get_env("DEFAULT_FAST_WHISPER_MODEL", "large-v3-turbo")
            else:
                default_model = config_manager.get_env("DEFAULT_WHISPER_MODEL", "large")
            
            index = self.model_combo.findData(default_model)
            if index >= 0:
                self.model_combo.setCurrentIndex(index)
                self.current_model = default_model
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij updaten modellen: {e}")
    
    def on_type_changed(self, text):
        """Callback voor type wijziging"""
        try:
            # Haal data op uit combo box
            current_data = self.type_combo.currentData()
            if current_data:
                self.current_whisper_type = current_data
                
                # Update beschrijving
                if self.current_whisper_type == "fast":
                    self.type_description.setText(
                        "🚀 Fast Whisper: 2-4x sneller dan standaard Whisper, "
                        "minder geheugengebruik, betere GPU ondersteuning"
                    )
                else:
                    self.type_description.setText(
                        "🐌 Standaard Whisper: Originele OpenAI Whisper, "
                        "stabiel en goed getest"
                    )
                
                # Update modellen
                self.update_models()
                
                # Update performance vergelijking
                self.update_performance_comparison()
                
        except Exception as e:
            logger.log_debug(f"❌ Fout bij type wijziging: {e}")
    
    def on_model_changed(self, text):
        """Callback voor model wijziging"""
        try:
            # Haal data op uit combo box
            current_data = self.model_combo.currentData()
            if current_data:
                self.current_model = current_data
                
                # Update beschrijving
                self.update_model_description()
                
        except Exception as e:
            logger.log_debug(f"❌ Fout bij model wijziging: {e}")
    
    def update_model_description(self):
        """Update model beschrijving"""
        try:
            if self.current_model == "large-v3-turbo":
                self.model_description.setText(
                    "🚀 Nieuwste en snelste model van OpenAI Whisper. "
                    "Beste kwaliteit en snelheid combinatie."
                )
            elif self.current_model == "large":
                self.model_description.setText(
                    "📊 Groot model met beste transcriptie kwaliteit. "
                    "Langzamer maar zeer accuraat."
                )
            elif self.current_model == "medium":
                self.model_description.setText(
                    "📈 Gemiddeld model met goede balans tussen "
                    "snelheid en kwaliteit."
                )
            elif self.current_model == "small":
                self.model_description.setText(
                    "📉 Klein model voor snelle transcriptie. "
                    "Acceptabele kwaliteit."
                )
            elif self.current_model == "base":
                self.model_description.setText(
                    "📋 Basis model voor snelle transcriptie. "
                    "Basis kwaliteit."
                )
            elif self.current_model == "tiny":
                self.model_description.setText(
                    "⚡ Zeer klein model voor ultieme snelheid. "
                    "Lage kwaliteit."
                )
            else:
                self.model_description.setText(f"Model: {self.current_model}")
                
        except Exception as e:
            logger.log_debug(f"❌ Fout bij updaten model beschrijving: {e}")
    
    def load_model(self):
        """Laad het geselecteerde model"""
        try:
            if self.is_loading:
                return
            
            self.is_loading = True
            self.load_button.setEnabled(False)
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # Indeterminate progress
            self.status_label.setText("Model laden...")
            self.status_label.setStyleSheet("color: #ffa726; font-weight: bold;")
            
            # Start loading in background thread
            self.load_thread = ModelLoadThread(self.current_whisper_type, self.current_model)
            self.load_thread.finished.connect(self.on_model_loaded)
            self.load_thread.start()
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij laden model: {e}")
            self.reset_loading_state()
    
    def on_model_loaded(self, success):
        """Callback voor model geladen"""
        try:
            self.reset_loading_state()
            
            if success:
                self.status_label.setText("✅ Model geladen")
                self.status_label.setStyleSheet("color: #4caf50; font-weight: bold;")
                self.update_model_info()
                self.model_loaded.emit(True)
            else:
                self.status_label.setText("❌ Model laden gefaald")
                self.status_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")
                self.model_loaded.emit(False)
                
        except Exception as e:
            logger.log_debug(f"❌ Fout bij model geladen callback: {e}")
            self.reset_loading_state()
    
    def reset_loading_state(self):
        """Reset loading state"""
        self.is_loading = False
        self.load_button.setEnabled(True)
        self.progress_bar.setVisible(False)
    
    def switch_whisper_type(self):
        """Wissel naar ander Whisper type"""
        try:
            if self.is_loading:
                return
            
            # Bepaal nieuw type
            current_types = whisper_manager.get_available_whisper_types()
            if self.current_whisper_type == "fast" and "standard" in current_types:
                new_type = "standard"
                new_model = "large"
            elif self.current_whisper_type == "standard" and "fast" in current_types:
                new_type = "fast"
                new_model = "large-v3-turbo"
            else:
                return
            
            # Update UI
            index = self.type_combo.findData(new_type)
            if index >= 0:
                self.type_combo.setCurrentIndex(index)
            
            # Laad nieuw model
            self.load_model()
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij wisselen Whisper type: {e}")
    
    def update_model_info(self):
        """Update model informatie display"""
        try:
            info = whisper_manager.get_model_info()
            
            if "error" in info:
                self.model_info.setText(f"❌ Fout: {info['error']}")
                return
            
            info_text = f"🤖 Type: {info.get('whisper_type', 'unknown')}\n"
            info_text += f"📦 Model: {info.get('model_name', 'unknown')}\n"
            info_text += f"💻 Device: {info.get('device', 'unknown')}\n"
            
            if 'compute_type' in info:
                info_text += f"⚙️ Compute: {info['compute_type']}\n"
            
            info_text += f"🌍 Multilingual: {'Ja' if info.get('is_multilingual', False) else 'Nee'}"
            
            self.model_info.setText(info_text)
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij updaten model info: {e}")
    
    def update_performance_comparison(self):
        """Update performance vergelijking"""
        try:
            comparison = whisper_manager.get_performance_comparison()
            
            perf_text = "📊 Performance Vergelijking:\n\n"
            
            if comparison["fast_available"]:
                perf_text += "🚀 Fast Whisper:\n"
                perf_text += "  • 2-4x sneller dan standaard\n"
                perf_text += "  • 50-70% minder geheugen\n"
                perf_text += "  • Betere GPU optimalisatie\n\n"
            
            if comparison["standard_available"]:
                perf_text += "🐌 Standaard Whisper:\n"
                perf_text += "  • Stabiel en goed getest\n"
                perf_text += "  • Originele OpenAI implementatie\n"
                perf_text += "  • Breed ondersteund\n\n"
            
            if comparison["current_type"] != "none":
                perf_text += f"🎯 Huidig type: {comparison['current_type']}"
            
            self.perf_text.setText(perf_text)
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij updaten performance vergelijking: {e}")
    
    def update_status(self):
        """Update status display"""
        try:
            if whisper_manager.is_model_loaded():
                self.status_label.setText("✅ Model geladen")
                self.status_label.setStyleSheet("color: #4caf50; font-weight: bold;")
                self.update_model_info()
            else:
                self.status_label.setText("❌ Geen model geladen")
                self.status_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")
                self.model_info.setText("Geen model geladen")
            
            self.update_performance_comparison()
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij updaten status: {e}")


class ModelLoadThread(QThread):
    """Thread voor het laden van Whisper modellen"""
    
    def __init__(self, whisper_type, model_name):
        super().__init__()
        self.whisper_type = whisper_type
        self.model_name = model_name
        self.success = False
    
    def run(self):
        """Voer model loading uit"""
        try:
            self.success = whisper_manager.initialize(self.whisper_type, self.model_name)
        except Exception as e:
            logger.log_debug(f"❌ Fout in model load thread: {e}")
            self.success = False
    
    def finished(self):
        """Thread finished callback"""
        pass 