"""
Geavanceerde instellingen tab
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QGroupBox, QSpinBox, QCheckBox
)

from core.config import config_manager

class AdvancedTab(QWidget):
    """Geavanceerde instellingen tab"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup de UI"""
        layout = QVBoxLayout(self)
        
        # Debug instellingen
        debug_group = QGroupBox("🐛 Debug Instellingen")
        debug_layout = QVBoxLayout(debug_group)
        
        self.debug_mode_check = QCheckBox("🐛 Debug Mode")
        debug_layout.addWidget(self.debug_mode_check)
        
        self.verbose_logging_check = QCheckBox("📝 Verbose Logging")
        debug_layout.addWidget(self.verbose_logging_check)
        
        self.show_system_info_check = QCheckBox("💻 Toon Systeem Informatie")
        debug_layout.addWidget(self.show_system_info_check)
        
        layout.addWidget(debug_group)
        
        # Performance instellingen
        performance_group = QGroupBox("⚡ Performance Instellingen")
        performance_layout = QVBoxLayout(performance_group)
        
        # Cache grootte
        cache_layout = QHBoxLayout()
        cache_layout.addWidget(QLabel("💾 Cache Grootte (MB):"))
        
        self.cache_size_spin = QSpinBox()
        self.cache_size_spin.setRange(100, 5000)
        self.cache_size_spin.setValue(1000)
        cache_layout.addWidget(self.cache_size_spin)
        
        performance_layout.addLayout(cache_layout)
        
        # Thread pool grootte
        thread_layout = QHBoxLayout()
        thread_layout.addWidget(QLabel("🧵 Thread Pool Grootte:"))
        
        self.thread_pool_spin = QSpinBox()
        self.thread_pool_spin.setRange(2, 16)
        self.thread_pool_spin.setValue(4)
        thread_layout.addWidget(self.thread_pool_spin)
        
        performance_layout.addLayout(thread_layout)
        
        layout.addWidget(performance_group)
        
        # Backup instellingen
        backup_group = QGroupBox("💾 Backup Instellingen")
        backup_layout = QVBoxLayout(backup_group)
        
        self.auto_backup_check = QCheckBox("💾 Automatische Backup")
        backup_layout.addWidget(self.auto_backup_check)
        
        # Backup interval
        backup_interval_layout = QHBoxLayout()
        backup_interval_layout.addWidget(QLabel("⏰ Backup Interval (dagen):"))
        
        self.backup_interval_spin = QSpinBox()
        self.backup_interval_spin.setRange(1, 30)
        self.backup_interval_spin.setValue(7)
        backup_interval_layout.addWidget(self.backup_interval_spin)
        
        backup_layout.addLayout(backup_interval_layout)
        
        layout.addWidget(backup_group)
    
    def load_configuration(self):
        """Laad configuratie"""
        try:
            # Debug instellingen
            self.debug_mode_check.setChecked(config_manager.get("DEBUG_MODE", "false").lower() == "true")
            self.verbose_logging_check.setChecked(config_manager.get("VERBOSE_LOGGING", "false").lower() == "true")
            self.show_system_info_check.setChecked(config_manager.get("SHOW_SYSTEM_INFO", "false").lower() == "true")
            
            # Performance instellingen
            self.cache_size_spin.setValue(int(config_manager.get("CACHE_SIZE_MB", "1000")))
            self.thread_pool_spin.setValue(int(config_manager.get("THREAD_POOL_SIZE", "4")))
            
            # Backup instellingen
            self.auto_backup_check.setChecked(config_manager.get("AUTO_BACKUP", "false").lower() == "true")
            self.backup_interval_spin.setValue(int(config_manager.get("BACKUP_INTERVAL_DAYS", "7")))
            
        except Exception as e:
            print(f"❌ Fout bij laden geavanceerde configuratie: {e}")
    
    def save_configuration(self):
        """Sla configuratie op"""
        try:
            # Debug instellingen
            config_manager.set("DEBUG_MODE", str(self.debug_mode_check.isChecked()).lower())
            config_manager.set("VERBOSE_LOGGING", str(self.verbose_logging_check.isChecked()).lower())
            config_manager.set("SHOW_SYSTEM_INFO", str(self.show_system_info_check.isChecked()).lower())
            
            # Performance instellingen
            config_manager.set("CACHE_SIZE_MB", str(self.cache_size_spin.value()))
            config_manager.set("THREAD_POOL_SIZE", str(self.thread_pool_spin.value()))
            
            # Backup instellingen
            config_manager.set("AUTO_BACKUP", str(self.auto_backup_check.isChecked()).lower())
            config_manager.set("BACKUP_INTERVAL_DAYS", str(self.backup_interval_spin.value()))
            
        except Exception as e:
            print(f"❌ Fout bij opslaan geavanceerde configuratie: {e}")
