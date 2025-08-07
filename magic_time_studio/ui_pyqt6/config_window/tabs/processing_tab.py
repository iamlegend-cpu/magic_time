"""
Verwerking instellingen tab
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QGroupBox, QComboBox, QSpinBox
)

from magic_time_studio.core.config import config_manager

class ProcessingTab(QWidget):
    """Verwerking instellingen tab"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup de UI"""
        layout = QVBoxLayout(self)
        
        # Whisper instellingen
        whisper_group = QGroupBox("🎤 Whisper Instellingen")
        whisper_layout = QVBoxLayout(whisper_group)
        
        # Whisper Type (alleen Fast Whisper beschikbaar)
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("🤖 Type:"))
        
        self.whisper_type_combo = QComboBox()
        self.whisper_type_combo.addItems(["🚀 Fast Whisper"])
        self.whisper_type_combo.setEnabled(False)  # Niet wijzigbaar
        type_layout.addWidget(self.whisper_type_combo)
        
        whisper_layout.addLayout(type_layout)
        
        # Model
        model_layout = QHBoxLayout()
        model_layout.addWidget(QLabel("📦 Model:"))
        
        self.model_combo = QComboBox()
        self.model_combo.currentTextChanged.connect(self.on_model_changed)
        model_layout.addWidget(self.model_combo)
        
        whisper_layout.addLayout(model_layout)
        
        # Device
        device_layout = QHBoxLayout()
        device_layout.addWidget(QLabel("💻 Device:"))
        
        self.device_combo = QComboBox()
        self.device_combo.addItems(["cpu", "cuda"])
        device_layout.addWidget(self.device_combo)
        
        whisper_layout.addLayout(device_layout)
        
        # Worker count
        workers_layout = QHBoxLayout()
        workers_layout.addWidget(QLabel("⚙️ Worker Count:"))
        
        self.workers_spin = QSpinBox()
        self.workers_spin.setRange(1, 8)
        self.workers_spin.setValue(4)
        workers_layout.addWidget(self.workers_spin)
        
        whisper_layout.addLayout(workers_layout)
        
        layout.addWidget(whisper_group)
        
        # Systeem limieten
        limits_group = QGroupBox("⚡ Systeem Limieten")
        limits_layout = QVBoxLayout(limits_group)
        
        # CPU limiet
        cpu_layout = QHBoxLayout()
        cpu_layout.addWidget(QLabel("🖥️ CPU Limiet (%):"))
        
        self.cpu_limit_spin = QSpinBox()
        self.cpu_limit_spin.setRange(10, 100)
        self.cpu_limit_spin.setValue(80)
        cpu_layout.addWidget(self.cpu_limit_spin)
        
        limits_layout.addLayout(cpu_layout)
        
        # Memory limiet (gebruiksvriendelijk)
        memory_layout = QHBoxLayout()
        memory_layout.addWidget(QLabel("💾 Memory Limiet:"))
        
        self.memory_limit_combo = QComboBox()
        self.memory_limit_combo.addItems([
            "2 GB (2048 MB)",
            "4 GB (4096 MB)", 
            "6 GB (6144 MB)",
            "8 GB (8192 MB)",
            "12 GB (12288 MB)",
            "16 GB (16384 MB)",
            "Automatisch (aanpassen aan systeem)"
        ])
        self.memory_limit_combo.currentTextChanged.connect(self.on_memory_limit_changed)
        memory_layout.addWidget(self.memory_limit_combo)
        
        limits_layout.addLayout(memory_layout)
        
        layout.addWidget(limits_group)
        
        # Subtitle instellingen
        subtitle_group = QGroupBox("📺 Subtitle Instellingen")
        subtitle_layout = QVBoxLayout(subtitle_group)
        
        # Subtitle type
        subtitle_type_layout = QHBoxLayout()
        subtitle_type_layout.addWidget(QLabel("📝 Type:"))
        
        self.subtitle_type_combo = QComboBox()
        self.subtitle_type_combo.addItems(["softcoded", "hardcoded"])
        subtitle_type_layout.addWidget(self.subtitle_type_combo)
        
        subtitle_layout.addLayout(subtitle_type_layout)
        
        # Hardcoded language
        hardcoded_layout = QHBoxLayout()
        hardcoded_layout.addWidget(QLabel("🌍 Hardcoded Taal:"))
        
        self.hardcoded_combo = QComboBox()
        self.hardcoded_combo.addItems(["dutch_only", "english_only", "both"])
        hardcoded_layout.addWidget(self.hardcoded_combo)
        
        subtitle_layout.addLayout(hardcoded_layout)
        
        layout.addWidget(subtitle_group)
    
    def on_whisper_type_changed(self, type_text: str):
        """Whisper type gewijzigd (alleen Fast Whisper beschikbaar)"""
        # Forceer altijd Fast Whisper
        whisper_type = "fast"
        config_manager.set_env("WHISPER_TYPE", "fast")
        
        # Update modellen voor Fast Whisper
        self.update_models_for_type(whisper_type)
    
    def update_models_for_type(self, whisper_type):
        """Update beschikbare modellen voor het geselecteerde Whisper type"""
        try:
            self.model_combo.clear()
            
            # Alleen Fast Whisper modellen beschikbaar
            models = [
                "tiny", "base", "small", "medium", "large",
                "large-v1", "large-v2", "large-v3", 
                "large-v3-turbo", "turbo"
            ]
            default_model = config_manager.get_env("DEFAULT_FAST_WHISPER_MODEL", "large-v3-turbo")
            
            # Voeg modellen toe met display namen
            for model in models:
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
            index = self.model_combo.findData(default_model)
            if index >= 0:
                self.model_combo.setCurrentIndex(index)
            
        except Exception as e:
            print(f"❌ Fout bij updaten modellen: {e}")
    
    def on_model_changed(self):
        """Handle model change"""
        model = self.model_combo.currentText()
        print(f"🎤 Model gewijzigd naar: {model}")
    
    def on_memory_limit_changed(self, memory_text: str):
        """Handle memory limit change"""
        print(f"💾 Memory limiet gewijzigd naar: {memory_text}")
        
        # Map user-friendly text naar bytes
        memory_mapping = {
            "2 GB (2048 MB)": 2048 * 1024 * 1024,
            "4 GB (4096 MB)": 4096 * 1024 * 1024,
            "6 GB (6144 MB)": 6144 * 1024 * 1024,
            "8 GB (8192 MB)": 8192 * 1024 * 1024,
            "12 GB (12288 MB)": 12288 * 1024 * 1024,
            "16 GB (16384 MB)": 16384 * 1024 * 1024,
            "Automatisch (aanpassen aan systeem)": 0 # 0 betekent automatisch
        }
        
        memory_bytes = memory_mapping.get(memory_text, 8192 * 1024 * 1024) # Standaard 8GB
        config_manager.set("MEMORY_LIMIT_MB", str(memory_bytes // (1024 * 1024))) # Opslaan in MB
    
    def load_configuration(self):
        """Laad configuratie"""
        try:
            # Whisper instellingen (alleen Fast Whisper)
            self.whisper_type_combo.setCurrentText("🚀 Fast Whisper")
            
            # Update modellen voor Fast Whisper
            self.update_models_for_type("fast")
            
            self.device_combo.setCurrentText(config_manager.get("WHISPER_DEVICE", "cuda"))
            self.workers_spin.setValue(int(config_manager.get("DEFAULT_WORKER_COUNT", "4")))
            
            # Systeem limieten
            self.cpu_limit_spin.setValue(int(config_manager.get("CPU_LIMIT_PERCENTAGE", "80")))
            
            # Memory limit (gebruiksvriendelijk)
            memory_mb = int(config_manager.get("MEMORY_LIMIT_MB", "8192"))
            memory_mapping_reverse = {
                2048: "2 GB (2048 MB)",
                4096: "4 GB (4096 MB)", 
                6144: "6 GB (6144 MB)",
                8192: "8 GB (8192 MB)",
                12288: "12 GB (12288 MB)",
                16384: "16 GB (16384 MB)",
                0: "Automatisch (aanpassen aan systeem)"
            }
            memory_text = memory_mapping_reverse.get(memory_mb, "8 GB (8192 MB)")
            self.memory_limit_combo.setCurrentText(memory_text)
            
            # Subtitle instellingen
            self.subtitle_type_combo.setCurrentText(config_manager.get("DEFAULT_SUBTITLE_TYPE", "softcoded"))
            self.hardcoded_combo.setCurrentText(config_manager.get("DEFAULT_HARDCODED_LANGUAGE", "dutch_only"))
            
        except Exception as e:
            print(f"❌ Fout bij laden verwerking configuratie: {e}")
    
    def save_configuration(self):
        """Sla configuratie op"""
        try:
            # Whisper instellingen (alleen Fast Whisper)
            config_manager.set_env("WHISPER_TYPE", "fast")
            
            # Model instellingen (alleen Fast Whisper)
            model_data = self.model_combo.currentData()
            if model_data:
                config_manager.set_env("DEFAULT_FAST_WHISPER_MODEL", model_data)
            
            config_manager.set("WHISPER_DEVICE", self.device_combo.currentText())
            config_manager.set("DEFAULT_WORKER_COUNT", str(self.workers_spin.value()))
            
            # Systeem limieten
            config_manager.set("CPU_LIMIT_PERCENTAGE", str(self.cpu_limit_spin.value()))
            
            # Memory limit (gebruiksvriendelijk)
            memory_text = self.memory_limit_combo.currentText()
            memory_mapping = {
                "2 GB (2048 MB)": 2048 * 1024 * 1024,
                "4 GB (4096 MB)": 4096 * 1024 * 1024,
                "6 GB (6144 MB)": 6144 * 1024 * 1024,
                "8 GB (8192 MB)": 8192 * 1024 * 1024,
                "12 GB (12288 MB)": 12288 * 1024 * 1024,
                "16 GB (16384 MB)": 16384 * 1024 * 1024,
                "Automatisch (aanpassen aan systeem)": 0
            }
            memory_bytes = memory_mapping.get(memory_text, 8192 * 1024 * 1024) # Standaard 8GB
            config_manager.set("MEMORY_LIMIT_MB", str(memory_bytes // (1024 * 1024))) # Opslaan in MB
            
            # Subtitle instellingen
            config_manager.set("DEFAULT_SUBTITLE_TYPE", self.subtitle_type_combo.currentText())
            config_manager.set("DEFAULT_HARDCODED_LANGUAGE", self.hardcoded_combo.currentText())
            
        except Exception as e:
            print(f"❌ Fout bij opslaan verwerking configuratie: {e}")
