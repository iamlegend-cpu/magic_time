"""
Processing Tab voor Config Window
Beheert verwerkingsinstellingen inclusief Whisper configuratie
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, 
    QComboBox, QGroupBox, QFormLayout
)
from PyQt6.QtCore import Qt

# Import whisper selector
try:
    from ...components.whisper_selector import WhisperSelectorWidget
    from core.config import config_manager
except ImportError:
    from core.config import config_manager
    # Fallback - maak dummy WhisperSelectorWidget
    class WhisperSelectorWidget:
        def __init__(self):
            pass

class ProcessingTab(QWidget):
    """Tab voor verwerkingsinstellingen"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_configuration()
    
    def setup_ui(self):
        """Setup de UI"""
        layout = QVBoxLayout(self)
        
        # Whisper instellingen - gebruik de volledige WhisperSelectorWidget
        whisper_group = QGroupBox("🎤 Whisper Instellingen")
        whisper_layout = QVBoxLayout(whisper_group)
        
        # Voeg de volledige whisper selector toe
        self.whisper_selector = WhisperSelectorWidget()
        whisper_layout.addWidget(self.whisper_selector)
        
        whisper_group.setLayout(whisper_layout)
        layout.addWidget(whisper_group)
        
        # Device instellingen
        device_group = QGroupBox("💻 Device Instellingen")
        device_layout = QFormLayout(device_group)
        
        self.device_combo = QComboBox()
        self.device_combo.addItems(["cpu", "cuda"])
        device_layout.addRow("Device:", self.device_combo)
        
        device_group.setLayout(device_layout)
        layout.addWidget(device_group)
        
        # Worker count
        workers_group = QGroupBox("⚙️ Worker Instellingen")
        workers_layout = QFormLayout(workers_group)
        
        self.workers_spin = QSpinBox()
        self.workers_spin.setRange(1, 8)
        self.workers_spin.setValue(4)
        workers_layout.addRow("Worker Count:", self.workers_spin)
        
        workers_group.setLayout(workers_layout)
        layout.addWidget(workers_group)
        
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
        
        limits_group.setLayout(limits_layout)
        layout.addWidget(limits_group)
        
        # Subtitle instellingen
        subtitle_group = QGroupBox("📺 Subtitle Instellingen")
        subtitle_layout = QVBoxLayout(subtitle_group)
        
        # Subtitle type
        subtitle_type_layout = QHBoxLayout()
        subtitle_type_layout.addWidget(QLabel("📝 Type:"))
        
        self.subtitle_type_combo = QComboBox()
        self.subtitle_type_combo.addItems(["softcoded"])
        self.subtitle_type_combo.setEnabled(False)  # Uitgeschakeld omdat alleen softcoded beschikbaar is
        subtitle_type_layout.addWidget(self.subtitle_type_combo)
        
        subtitle_layout.addLayout(subtitle_type_layout)
        
        subtitle_group.setLayout(subtitle_layout)
        layout.addWidget(subtitle_group)
        
        # Voeg stretch toe
        layout.addStretch()
    
    def on_memory_limit_changed(self, memory_text: str):
        """Handle memory limit wijziging"""
        # Converteer tekst naar MB waarde
        memory_mapping = {
            "2 GB (2048 MB)": 2048,
            "4 GB (4096 MB)": 4096,
            "6 GB (6144 MB)": 6144,
            "8 GB (8192 MB)": 8192,
            "12 GB (12288 MB)": 12288,
            "16 GB (16384 MB)": 16384,
            "Automatisch (aanpassen aan systeem)": 0
        }
        
        memory_mb = memory_mapping.get(memory_text, 8192)
        config_manager.set("memory_limit_mb", memory_mb)
    
    def load_configuration(self):
        """Laad configuratie"""
        try:
            # Device instellingen
            device = config_manager.get("WHISPER_DEVICE", "cuda")
            self.device_combo.setCurrentText(device)
            
            # Worker count
            workers = config_manager.get("worker_count", 4)
            self.workers_spin.setValue(workers)
            
            # CPU limiet
            cpu_limit = config_manager.get("cpu_limit_percentage", 80)
            self.cpu_limit_spin.setValue(cpu_limit)
            
            # Memory limiet
            memory_mb = config_manager.get("memory_limit_mb", 8192)
            memory_text = self._get_memory_display_text(memory_mb)
            self.memory_limit_combo.setCurrentText(memory_text)
            
            # Subtitle type (altijd softcoded)
            subtitle_type = "softcoded"  # Altijd softcoded, hardcoded wordt niet meer ondersteund
            self.subtitle_type_combo.setCurrentText(subtitle_type)
            
        except Exception as e:
            print(f"⚠️ Fout bij laden configuratie: {e}")
    
    def _get_memory_display_text(self, memory_mb: int) -> str:
        """Converteer memory MB naar display tekst"""
        if memory_mb == 0:
            return "Automatisch (aanpassen aan systeem)"
        
        memory_mapping = {
            2048: "2 GB (2048 MB)",
            4096: "4 GB (4096 MB)",
            6144: "6 GB (6144 MB)",
            8192: "8 GB (8192 MB)",
            12288: "12 GB (12288 MB)",
            16384: "16 GB (16384 MB)"
        }
        
        return memory_mapping.get(memory_mb, "8 GB (8192 MB)")
    
    def save_configuration(self):
        """Sla configuratie op"""
        try:
            # Device instellingen
            config_manager.set("WHISPER_DEVICE", self.device_combo.currentText())
            
            # Worker count
            config_manager.set("worker_count", self.workers_spin.value())
            
            # CPU limiet
            config_manager.set("cpu_limit_percentage", self.cpu_limit_spin.value())
            
            # Subtitle type (altijd softcoded)
            config_manager.set("subtitle_type", "softcoded")  # Altijd softcoded, hardcoded wordt niet meer ondersteund
            
            # Whisper instellingen worden automatisch opgeslagen door de WhisperSelectorWidget
            
            print("✅ Processing configuratie opgeslagen")
            
        except Exception as e:
            print(f"❌ Fout bij opslaan configuratie: {e}")
    
    def get_current_settings(self) -> dict:
        """Krijg huidige instellingen als dictionary"""
        return {
            "whisper_type": self.whisper_selector.current_whisper_type,
            "whisper_model": self.whisper_selector.current_model,
            "device": self.device_combo.currentText(),
            "worker_count": self.workers_spin.value(),
            "cpu_limit_percentage": self.cpu_limit_spin.value(),
            "memory_limit_mb": self._get_memory_mb_from_display(),
            "subtitle_type": "softcoded"  # Altijd softcoded, hardcoded wordt niet meer ondersteund
        }
    
    def _get_memory_mb_from_display(self) -> int:
        """Converteer display tekst naar memory MB"""
        memory_text = self.memory_limit_combo.currentText()
        memory_mapping = {
            "2 GB (2048 MB)": 2048,
            "4 GB (4096 MB)": 4096,
            "6 GB (6144 MB)": 6144,
            "8 GB (8192 MB)": 8192,
            "12 GB (12288 MB)": 12288,
            "16 GB (16384 MB)": 16384,
            "Automatisch (aanpassen aan systeem)": 0
        }
        
        return memory_mapping.get(memory_text, 8192)
