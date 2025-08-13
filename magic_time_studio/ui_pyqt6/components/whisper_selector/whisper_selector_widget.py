"""
Whisper Selector Widget Component voor Magic Time Studio
UI component voor het kiezen tussen standaard Whisper en Fast Whisper
Met automatische model selectie en laden
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QComboBox, QGroupBox, QGridLayout, QFrame, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QPalette, QColor
import time # Added for time.time()

# Absolute imports
try:
    from core.logging import logger
    # Lazy import van config_manager om circulaire import te voorkomen
    def _get_config_manager():
        """Lazy config manager import om circulaire import te voorkomen"""
        try:
            from core.config import config_manager
            return config_manager
        except ImportError:
            return None
    from .model_load_thread import ModelLoadThread
except ImportError:
    # Fallback - maak dummy imports
    logger = None
    def _get_config_manager():
        return None
    class ModelLoadThread:
        def __init__(self):
            pass


class WhisperSelectorWidget(QWidget):
    """Widget voor het selecteren van Whisper type en model met automatische selectie"""
    
    # Signals
    whisper_changed = pyqtSignal(str, str)  # type, model
    model_loaded = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # Gebruik configuratie voor defaults
        config_mgr = _get_config_manager()
        self.current_whisper_type = config_mgr.get("whisper_type", "fast") if config_mgr else "fast"
        if self.current_whisper_type == "fast":
            self.current_model = config_mgr.get("default_fast_whisper_model", "medium") if config_mgr else "medium"
        else:
            self.current_model = config_mgr.get("default_whisper_model", "medium") if config_mgr else "medium"
        
        # GPU instellingen
        self.current_device = config_mgr.get_env("WHISPER_DEVICE", "cuda") if config_mgr else "cuda"
        self.current_compute_type = config_mgr.get_env("WHISPER_COMPUTE_TYPE", "float16") if config_mgr else "float16"
        
        self.is_loading = False
        # Automatische loading uitgeschakeld om vastlopen te voorkomen
        # self.auto_load_timer = QTimer()
        # self.auto_load_timer.setSingleShot(True)
        # self.auto_load_timer.timeout.connect(self._auto_load_model)
        
        self.setup_ui()
        self.load_available_options()
        # self.load_gpu_settings()  # Deze methode bestaat niet, commentaar uit
    
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
        
        model_group.setLayout(model_layout)
        layout.addWidget(model_group)
        
        # GPU Device Selector (alleen voor Fast Whisper)
        self.gpu_group = QGroupBox("🎮 GPU Device")
        gpu_layout = QVBoxLayout()
        
        # Device selector
        device_selector_layout = QHBoxLayout()
        device_selector_layout.addWidget(QLabel("Device:"))
        
        self.device_combo = QComboBox()
        self.device_combo.addItem("🚀 CUDA (GPU)", "cuda")
        self.device_combo.addItem("🖥️ CPU", "cpu")
        self.device_combo.currentTextChanged.connect(self.on_device_changed)
        device_selector_layout.addWidget(self.device_combo)
        
        gpu_layout.addLayout(device_selector_layout)
        
        # Compute Type selector
        compute_selector_layout = QHBoxLayout()
        compute_selector_layout.addWidget(QLabel("Compute Type:"))
        
        self.compute_combo = QComboBox()
        self.compute_combo.addItem("⚡ Float16 (Snel)", "float16")
        self.compute_combo.addItem("📊 Float32 (Accuraat)", "float32")
        self.compute_combo.addItem("💾 Int8 (Compact)", "int8")
        self.compute_combo.currentTextChanged.connect(self.on_compute_type_changed)
        compute_selector_layout.addWidget(self.compute_combo)
        
        gpu_layout.addLayout(compute_selector_layout)
        
        # GPU Status
        self.gpu_status_label = QLabel("GPU Status: Controleer...")
        self.gpu_status_label.setStyleSheet("color: #FF9800; font-size: 10px;")
        gpu_layout.addWidget(self.gpu_status_label)
        
        # GPU Test Button
        test_button_layout = QHBoxLayout()
        self.test_gpu_button = QPushButton("🧪 Test GPU")
        self.test_gpu_button.clicked.connect(self.test_gpu)
        self.test_gpu_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
            QPushButton:pressed {
                background-color: #E65100;
            }
        """)
        test_button_layout.addWidget(self.test_gpu_button)
        gpu_layout.addLayout(test_button_layout)
        
        self.gpu_group.setLayout(gpu_layout)
        layout.addWidget(self.gpu_group)
        
        self.setLayout(layout)
        
        # Update GPU status
        self.update_gpu_status()
    
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
            config_mgr = _get_config_manager()
            default_type = config_mgr.get("whisper_type", "fast") if config_mgr else "fast"
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
            config_mgr = _get_config_manager()
            if self.current_whisper_type == "fast":
                default_model = config_mgr.get("default_fast_whisper_model", "medium") if config_mgr else "medium"
            else:
                default_model = config_mgr.get("default_whisper_model", "medium") if config_mgr else "medium"
            
            index = self.model_combo.findData(default_model)
            if index >= 0:
                self.model_combo.setCurrentIndex(index)
                self.current_model = default_model
            
            # Start automatisch laden uitgeschakeld om vastlopen te voorkomen
            # self.auto_load_timer.start(2000)  # Uitgeschakeld
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij updaten modellen: {e}")
    
    def on_type_changed(self, text):
        """Callback voor type wijziging"""
        try:
            # Haal data op uit combo box
            current_data = self.type_combo.currentData()
            if current_data:
                self.current_whisper_type = current_data
                if self._is_debug_mode():
                    print(f"🔧 [DEBUG] Whisper type gewijzigd naar: {self.current_whisper_type}")
                
                # Update modellen
                self.update_models()
                
                # Toon/verberg GPU opties op basis van type
                self.gpu_group.setVisible(current_data == "fast")
                
                # Sla type op in configuratie
                config_mgr = _get_config_manager()
                if config_mgr:
                    config_mgr.set("whisper_type", self.current_whisper_type)
                    
                    # Sla ook op in environment configuratie
                    config_mgr.set_env("WHISPER_TYPE", self.current_whisper_type)
                
                # Emit signal voor type wijziging
                self.whisper_changed.emit(self.current_whisper_type, self.current_model)
                
        except Exception as e:
            logger.log_debug(f"❌ Fout bij type wijziging: {e}")
    
    def on_model_changed(self, text):
        """Callback voor model wijziging"""
        try:
            # Haal data op uit combo box
            current_data = self.model_combo.currentData()
            if current_data:
                self.current_model = current_data
                if self._is_debug_mode():
                    print(f"🔧 [DEBUG] Whisper model gewijzigd naar: {self.current_model}")
                
                # Sla model op in configuratie
                config_mgr = _get_config_manager()
                if config_mgr:
                    if self.current_whisper_type == "fast":
                        config_mgr.set("default_fast_whisper_model", self.current_model)
                    else:
                        config_mgr.set("whisper_model", self.current_model)
                
                # Start automatisch laden uitgeschakeld om vastlopen te voorkomen
                # self.auto_load_timer.start(2000)  # Uitgeschakeld
                
                # Emit signal voor model wijziging
                self.whisper_changed.emit(self.current_whisper_type, self.current_model)
                
        except Exception as e:
            logger.log_debug(f"❌ Fout bij model wijziging: {e}")
    
    def on_device_changed(self, text):
        """Callback voor device wijziging"""
        try:
            current_data = self.device_combo.currentData()
            if current_data:
                self.current_device = current_data
                if self._is_debug_mode():
                    print(f"🔧 [DEBUG] GPU device gewijzigd naar: {current_data}")
                
                # Update whisper manager
                try:
                    from app_core.whisper_manager import whisper_manager
                    if whisper_manager:
                        whisper_manager.set_gpu_device(current_data)
                except ImportError:
                    pass
                
                # Sla op in configuratie
                config_mgr = _get_config_manager()
                if config_mgr:
                    config_mgr.set_env("WHISPER_DEVICE", current_data)
                
                # Update GPU status
                self.update_gpu_status()
                
        except Exception as e:
            if self._is_debug_mode():
                print(f"❌ Fout bij device wijziging: {e}")
    
    def on_compute_type_changed(self, text):
        """Callback voor compute type wijziging"""
        try:
            current_data = self.compute_combo.currentData()
            if current_data:
                self.current_compute_type = current_data
                if self._is_debug_mode():
                    print(f"🔧 [DEBUG] Compute type gewijzigd naar: {current_data}")
                
                # Update whisper manager
                try:
                    from app_core.whisper_manager import whisper_manager
                    if whisper_manager:
                        whisper_manager.set_compute_type(current_data)
                except ImportError:
                    pass
                
                # Sla op in configuratie
                config_mgr = _get_config_manager()
                if config_mgr:
                    config_mgr.set_env("WHISPER_COMPUTE_TYPE", current_data)
                
        except Exception as e:
            if self._is_debug_mode():
                print(f"❌ Fout bij compute type wijziging: {e}")
    
    def update_gpu_status(self):
        """Update GPU status informatie"""
        try:
            # Probeer whisper manager te gebruiken
            try:
                from app_core.whisper_manager import whisper_manager
                if whisper_manager:
                    gpu_status = whisper_manager.check_gpu_status()
                    
                    if gpu_status and gpu_status.get('available'):
                        device_name = gpu_status.get('name', 'N/A')
                        memory_total = gpu_status.get('memory_total', 0)
                        
                        if memory_total > 0:
                            self.gpu_status_label.setText(f"✅ GPU: {device_name} ({memory_total:.1f}GB VRAM)")
                            self.gpu_status_label.setStyleSheet("color: #4CAF50; font-size: 10px;")
                        else:
                            self.gpu_status_label.setText(f"✅ GPU: {device_name}")
                            self.gpu_status_label.setStyleSheet("color: #4CAF50; font-size: 10px;")
                    else:
                        self.gpu_status_label.setText("❌ GPU niet beschikbaar")
                        self.gpu_status_label.setStyleSheet("color: #f44336; font-size: 10px;")
                        
                        # Schakel over naar CPU
                        cpu_index = self.device_combo.findData("cpu")
                        if cpu_index >= 0:
                            self.device_combo.setCurrentIndex(cpu_index)
                    
                    return
            except ImportError:
                pass
            except Exception as e:
                # print(f"⚠️ Fout bij whisper manager GPU status: {e}")  # Uitgeschakeld
                pass
            
            # Fallback - probeer direct GPU check
            try:
                import torch
                if torch.cuda.is_available():
                    device_name = torch.cuda.get_device_name(0)
                    memory_total = torch.cuda.get_device_properties(0).total_memory / (1024**3)
                    
                    self.gpu_status_label.setText(f"✅ GPU: {device_name} ({memory_total:.1f}GB VRAM)")
                    self.gpu_status_label.setStyleSheet("color: #4CAF50; font-size: 10px;")
                else:
                    self.gpu_status_label.setText("❌ CUDA niet beschikbaar")
                    self.gpu_status_label.setStyleSheet("color: #f44336; font-size: 10px;")
                    
                    # Schakel over naar CPU
                    cpu_index = self.device_combo.findData("cpu")
                    if cpu_index >= 0:
                        self.device_combo.setCurrentIndex(cpu_index)
                        
            except ImportError:
                self.gpu_status_label.setText("⚠️ PyTorch niet beschikbaar")
                self.gpu_status_label.setStyleSheet("color: #FF9800; font-size: 10px;")
            except Exception as e:
                self.gpu_status_label.setText(f"❌ Fout: {str(e)[:30]}...")
                self.gpu_status_label.setStyleSheet("color: #f44336; font-size: 10px;")
                
        except Exception as e:
            self.gpu_status_label.setText(f"❌ Fout bij GPU status: {str(e)[:30]}...")
            self.gpu_status_label.setStyleSheet("color: #f44336; font-size: 10px;")
    
    def test_gpu(self):
        """Test GPU functionaliteit"""
        try:
            self.test_gpu_button.setEnabled(False)
            self.test_gpu_button.setText("🧪 Testen...")
            
            # Voer GPU test uit
            try:
                from app_core.whisper_manager import whisper_manager
                if whisper_manager:
                    gpu_status = whisper_manager.check_gpu_status()
                    
                    if gpu_status and gpu_status.get('available'):
                        device_name = gpu_status.get('name', 'N/A')
                        memory_total = gpu_status.get('memory_total', 0)
                        
                        if memory_total > 0:
                            self.gpu_status_label.setText(f"✅ Test geslaagd: {device_name} ({memory_total:.1f}GB VRAM)")
                            self.gpu_status_label.setStyleSheet("color: #4CAF50; font-size: 10px;")
                        else:
                            self.gpu_status_label.setText(f"✅ Test geslaagd: {device_name}")
                            self.gpu_status_label.setStyleSheet("color: #4CAF50; font-size: 10px;")
                    else:
                        self.gpu_status_label.setText("❌ GPU test gefaald")
                        self.gpu_status_label.setStyleSheet("color: #f44336; font-size: 10px;")
                        
            except ImportError:
                self.gpu_status_label.setText("⚠️ Whisper manager niet beschikbaar")
                self.gpu_status_label.setStyleSheet("color: #FF9800; font-size: 10px;")
            except Exception as e:
                self.gpu_status_label.setText(f"❌ Test gefaald: {str(e)[:30]}...")
                self.gpu_status_label.setStyleSheet("color: #f44336; font-size: 10px;")
                
        except Exception as e:
            self.gpu_status_label.setText(f"❌ Test fout: {str(e)[:30]}...")
            self.gpu_status_label.setStyleSheet("color: #f44336; font-size: 10px;")
        finally:
            self.test_gpu_button.setEnabled(True)
            self.test_gpu_button.setText("🧪 Test GPU")
    
    def _auto_load_model(self):
        """Automatisch laden van het geselecteerde model - UITGESCHAKELD"""
        # Automatisch laden is uitgeschakeld om vastlopen te voorkomen
        # Gebruiker moet handmatig model laden via UI
        pass
    
    def _start_loading(self):
        """Start het laden van het model"""
        try:
            if self.is_loading:
                print("⚠️ Model wordt al geladen, wacht...")
                return
            
            print(f"🔄 Start laden van {self.current_whisper_type} model: {self.current_model}")
            self.is_loading = True
            
            # Start loading in background thread met GPU instellingen
            self.load_thread = ModelLoadThread(
                self.current_whisper_type, 
                self.current_model,
                device=self.current_device,
                compute_type=self.current_compute_type
            )
            self.load_thread.finished.connect(self.on_model_loaded)
            self.load_thread.start()
            

            
        except Exception as e:
            print(f"❌ Fout bij starten laden: {e}")
            logger.log_debug(f"❌ Fout bij starten laden: {e}")
            self.reset_loading_state()
    

    
    def on_model_loaded(self, success):
        """Callback voor model geladen"""
        try:
            self.is_loading = False
            
            if success:
                print(f"✅ Model {self.current_model} succesvol geladen")
                self.model_loaded.emit(True)
            else:
                print(f"❌ Model {self.current_model} laden gefaald")
                self.model_loaded.emit(False)
                
        except Exception as e:
            print(f"❌ Fout bij model geladen callback: {e}")
            logger.log_debug(f"❌ Fout bij model geladen callback: {e}")
            self.reset_loading_state()
            self.model_loaded.emit(False)
    

    
    def reset_loading_state(self):
        """Reset loading state"""
        self.is_loading = False
    

    

    
    def get_current_settings(self):
        """Haal huidige instellingen op"""
        return {
            'whisper_type': self.current_whisper_type,
            'model': self.current_model,
            'device': self.device_combo.currentData() if hasattr(self, 'device_combo') else 'cuda',
            'compute_type': self.compute_combo.currentData() if hasattr(self, 'compute_combo') else 'float16'
        }
    
    def set_settings(self, whisper_type, model):
        """Stel instellingen in"""
        try:
            # Update type
            index = self.type_combo.findData(whisper_type)
            if index >= 0:
                self.type_combo.setCurrentIndex(index)
                self.current_whisper_type = whisper_type
            
            # Update model (wordt automatisch gedaan door type change)
            # De model update gebeurt automatisch in on_type_changed
            
            # Sla instellingen op in configuratie
            config_mgr = _get_config_manager()
            if config_mgr:
                config_mgr.set("whisper_type", whisper_type)
                if whisper_type == "fast":
                    config_mgr.set("default_fast_whisper_model", model)
                else:
                    config_mgr.set("default_whisper_model", model)
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij instellen instellingen: {e}")
