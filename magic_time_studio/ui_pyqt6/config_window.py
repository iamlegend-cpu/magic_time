"""
Configuratie venster voor Magic Time Studio
"""

import os
from PyQt6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QGroupBox, QTextEdit, QComboBox, QSpinBox,
    QCheckBox, QLineEdit, QTabWidget, QMessageBox, QFileDialog,
    QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from magic_time_studio.core.config import config_manager
from magic_time_studio.ui_pyqt6.features.modern_styling import ModernStyling
# from magic_time_studio.ui_pyqt6.features.processing_mode_manager import processing_mode_manager # Verwijderd

class ConfigWindow(QDialog):
    """Configuratie venster"""
    
    config_saved = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("⚙️ Magic Time Studio - Configuratie")
        
        # Start in een redelijke grootte, maar niet te groot
        self.setGeometry(200, 200, 900, 700)
        self.setMinimumSize(800, 600)
        
        self.callback = None
        
        # Sla alle verwerking-gerelateerde UI elementen op (moet voor setup_ui)
        self.processing_ui_elements = []
        
        self.setup_ui()
        self.load_configuration()
        
        # Registreer bij ProcessingModeManager
        # processing_mode_manager.register_config_window(self) # Verwijderd
    
    def set_callback(self, callback):
        """Stel callback functie in voor configuratie opslaan"""
        self.callback = callback
    
    def setup_ui(self):
        """Setup de UI"""
        layout = QVBoxLayout(self)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Tab 1: Algemene instellingen
        self.create_general_tab()
        
        # Tab 2: Verwerking instellingen
        self.create_processing_tab()
        
        # Tab 3: Vertaler instellingen
        self.create_translator_tab()
        
        # Tab 4: Interface instellingen
        self.create_interface_tab()
        
        # Tab 5: Thema instellingen
        self.create_theme_tab()
        
        # Tab 6: Geavanceerde instellingen
        self.create_advanced_tab()
        
        # Tab 7: Plugin beheer
        self.create_plugins_tab()
        
        # Knoppen
        button_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("💾 Opslaan")
        self.save_btn.clicked.connect(self.save_configuration)
        button_layout.addWidget(self.save_btn)
        
        self.cancel_btn = QPushButton("❌ Annuleren")
        self.cancel_btn.clicked.connect(self.close)
        button_layout.addWidget(self.cancel_btn)
        
        self.reset_btn = QPushButton("🔄 Reset naar Standaard")
        self.reset_btn.clicked.connect(self.reset_to_defaults)
        button_layout.addWidget(self.reset_btn)
        
        layout.addLayout(button_layout)
    
    def create_general_tab(self):
        """Maak algemene instellingen tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Basis instellingen
        general_group = QGroupBox("🔧 Algemene Instellingen")
        general_layout = QVBoxLayout(general_group)
        
        # Thema
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("🎨 Thema:"))
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["dark", "light", "blue", "green", "purple", "orange", "cyber"])
        theme_layout.addWidget(self.theme_combo)
        
        general_layout.addLayout(theme_layout)
        
        # Font grootte
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("📝 Font Grootte:"))
        
        self.font_spin = QSpinBox()
        self.font_spin.setRange(8, 16)
        self.font_spin.setValue(9)
        font_layout.addWidget(self.font_spin)
        
        general_layout.addLayout(font_layout)
        
        # Auto cleanup
        self.auto_cleanup_check = QCheckBox("🧹 Automatisch opschonen van tijdelijke bestanden")
        general_layout.addWidget(self.auto_cleanup_check)
        
        # Auto output directory
        self.auto_output_check = QCheckBox("📁 Automatisch output directory aanmaken")
        general_layout.addWidget(self.auto_output_check)
        
        layout.addWidget(general_group)
        
        # Logging instellingen
        logging_group = QGroupBox("📝 Logging Instellingen")
        logging_layout = QVBoxLayout(logging_group)
        
        # Log level
        log_level_layout = QHBoxLayout()
        log_level_layout.addWidget(QLabel("📊 Log Level:"))
        
        self.log_level_combo = QComboBox()
        self.log_level_combo.addItems(["DEBUG", "INFO", "WARNING", "ERROR"])
        log_level_layout.addWidget(self.log_level_combo)
        
        logging_layout.addLayout(log_level_layout)
        
        # Log naar bestand
        self.log_to_file_check = QCheckBox("📄 Log naar bestand")
        logging_layout.addWidget(self.log_to_file_check)
        
        layout.addWidget(logging_group)
        
        self.tab_widget.addTab(tab, "🔧 Algemeen")
    
    def create_processing_tab(self):
        """Maak verwerking instellingen tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Whisper instellingen
        whisper_group = QGroupBox("🎤 Whisper Instellingen")
        whisper_layout = QVBoxLayout(whisper_group)
        
        # Model
        model_layout = QHBoxLayout()
        model_layout.addWidget(QLabel("🤖 Model:"))
        
        self.model_combo = QComboBox()
        self.model_combo.addItems(["tiny", "base", "small", "medium", "large"])
        model_layout.addWidget(self.model_combo)
        self.processing_ui_elements.append(self.model_combo)
        
        whisper_layout.addLayout(model_layout)
        
        # Device
        device_layout = QHBoxLayout()
        device_layout.addWidget(QLabel("💻 Device:"))
        
        self.device_combo = QComboBox()
        self.device_combo.addItems(["cpu", "cuda"])
        device_layout.addWidget(self.device_combo)
        self.processing_ui_elements.append(self.device_combo)
        
        whisper_layout.addLayout(device_layout)
        
        # Worker count
        workers_layout = QHBoxLayout()
        workers_layout.addWidget(QLabel("⚙️ Worker Count:"))
        
        self.workers_spin = QSpinBox()
        self.workers_spin.setRange(1, 8)
        self.workers_spin.setValue(4)
        workers_layout.addWidget(self.workers_spin)
        self.processing_ui_elements.append(self.workers_spin)
        
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
        self.processing_ui_elements.append(self.cpu_limit_spin)
        
        limits_layout.addLayout(cpu_layout)
        
        # Memory limiet
        memory_layout = QHBoxLayout()
        memory_layout.addWidget(QLabel("💾 Memory Limiet (MB):"))
        
        self.memory_limit_spin = QSpinBox()
        self.memory_limit_spin.setRange(1024, 32768)
        self.memory_limit_spin.setValue(8192)
        self.memory_limit_spin.setSuffix(" MB")
        memory_layout.addWidget(self.memory_limit_spin)
        self.processing_ui_elements.append(self.memory_limit_spin)
        
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
        self.processing_ui_elements.append(self.subtitle_type_combo)
        
        subtitle_layout.addLayout(subtitle_type_layout)
        
        # Hardcoded language
        hardcoded_layout = QHBoxLayout()
        hardcoded_layout.addWidget(QLabel("🌍 Hardcoded Taal:"))
        
        self.hardcoded_combo = QComboBox()
        self.hardcoded_combo.addItems(["dutch_only", "english_only", "both"])
        hardcoded_layout.addWidget(self.hardcoded_combo)
        self.processing_ui_elements.append(self.hardcoded_combo)
        
        subtitle_layout.addLayout(hardcoded_layout)
        
        layout.addWidget(subtitle_group)
        
        self.tab_widget.addTab(tab, "⚙️ Verwerking")
    
    def create_translator_tab(self):
        """Maak vertaler instellingen tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # LibreTranslate instellingen
        libretranslate_group = QGroupBox("🌐 LibreTranslate Instellingen")
        libretranslate_layout = QVBoxLayout(libretranslate_group)
        
        # Server URL
        server_layout = QHBoxLayout()
        server_layout.addWidget(QLabel("🌍 Server URL:"))
        
        self.server_edit = QLineEdit()
        self.server_edit.setPlaceholderText("bijv. 192.168.1.100:5000")
        server_layout.addWidget(self.server_edit)
        
        libretranslate_layout.addLayout(server_layout)
        
        # Timeout
        timeout_layout = QHBoxLayout()
        timeout_layout.addWidget(QLabel("⏱️ Timeout (seconden):"))
        
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(5, 120)
        self.timeout_spin.setValue(30)
        timeout_layout.addWidget(self.timeout_spin)
        
        libretranslate_layout.addLayout(timeout_layout)
        
        # Rate limit
        rate_layout = QHBoxLayout()
        rate_layout.addWidget(QLabel("🚦 Rate Limit (0 = uit):"))
        
        self.rate_limit_spin = QSpinBox()
        self.rate_limit_spin.setRange(0, 1000)
        self.rate_limit_spin.setValue(0)
        rate_layout.addWidget(self.rate_limit_spin)
        
        libretranslate_layout.addLayout(rate_layout)
        
        # Max characters
        max_chars_layout = QHBoxLayout()
        max_chars_layout.addWidget(QLabel("📏 Max Karakters:"))
        
        self.max_chars_spin = QSpinBox()
        self.max_chars_spin.setRange(1000, 50000)
        self.max_chars_spin.setValue(10000)
        max_chars_layout.addWidget(self.max_chars_spin)
        
        libretranslate_layout.addLayout(max_chars_layout)
        
        layout.addWidget(libretranslate_group)
        
        self.tab_widget.addTab(tab, "🌐 Vertaler")
    
    def create_interface_tab(self):
        """Maak interface instellingen tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Panel zichtbaarheid
        panels_group = QGroupBox("👁️ Panel Zichtbaarheid")
        panels_layout = QVBoxLayout(panels_group)
        
        self.settings_panel_check = QCheckBox("⚙️ Instellingen Panel")
        panels_layout.addWidget(self.settings_panel_check)
        
        self.files_panel_check = QCheckBox("📁 Bestanden Panel")
        panels_layout.addWidget(self.files_panel_check)
        
        self.processing_panel_check = QCheckBox("⚙️ Verwerking Panel")
        panels_layout.addWidget(self.processing_panel_check)
        
        self.charts_panel_check = QCheckBox("📊 Grafieken Panel")
        panels_layout.addWidget(self.charts_panel_check)
        
        self.batch_panel_check = QCheckBox("📦 Batch Panel")
        panels_layout.addWidget(self.batch_panel_check)
        
        layout.addWidget(panels_group)
        
        # UI instellingen
        ui_group = QGroupBox("🎨 UI Instellingen")
        ui_layout = QVBoxLayout(ui_group)
        
        # Window grootte
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("�� Standaard Window Grootte:"))
        
        self.width_spin = QSpinBox()
        self.width_spin.setRange(800, 1920)
        self.width_spin.setValue(1200)
        self.width_spin.setSuffix(" px")
        size_layout.addWidget(self.width_spin)
        
        self.height_spin = QSpinBox()
        self.height_spin.setRange(600, 1080)
        self.height_spin.setValue(800)
        self.height_spin.setSuffix(" px")
        size_layout.addWidget(self.height_spin)
        
        ui_layout.addLayout(size_layout)
        
        # Splitter posities
        splitter_layout = QHBoxLayout()
        splitter_layout.addWidget(QLabel("✂️ Splitter Posities:"))
        
        self.splitter1_spin = QSpinBox()
        self.splitter1_spin.setRange(100, 800)
        self.splitter1_spin.setValue(300)
        self.splitter1_spin.setSuffix(" px")
        splitter_layout.addWidget(self.splitter1_spin)
        
        self.splitter2_spin = QSpinBox()
        self.splitter2_spin.setRange(100, 800)
        self.splitter2_spin.setValue(600)
        self.splitter2_spin.setSuffix(" px")
        splitter_layout.addWidget(self.splitter2_spin)
        
        ui_layout.addLayout(splitter_layout)
        
        layout.addWidget(ui_group)
        
        self.tab_widget.addTab(tab, "👁️ Interface")
    
    def create_theme_tab(self):
        """Maak thema instellingen tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Thema preview
        preview_group = QGroupBox("🎨 Thema Preview")
        preview_layout = QVBoxLayout(preview_group)
        
        self.theme_preview_label = QLabel("Selecteer een thema om een preview te zien")
        self.theme_preview_label.setStyleSheet("""
            QLabel {
                padding: 20px;
                border: 2px dashed #555555;
                border-radius: 8px;
                background-color: #1e1e1e;
                color: #ffffff;
                font-size: 12px;
            }
        """)
        preview_layout.addWidget(self.theme_preview_label)
        
        layout.addWidget(preview_group)
        
        # Thema opties
        theme_options_group = QGroupBox("🎨 Thema Opties")
        theme_options_layout = QVBoxLayout(theme_options_group)
        
        # Beschikbare thema's
        themes_layout = QHBoxLayout()
        themes_layout.addWidget(QLabel("🎨 Beschikbare Thema's:"))
        
        self.theme_selector_combo = QComboBox()
        self.theme_selector_combo.addItems([
            "dark", "light", "blue", "green", "purple", "orange", "cyber"
        ])
        self.theme_selector_combo.currentTextChanged.connect(self.preview_theme)
        themes_layout.addWidget(self.theme_selector_combo)
        
        theme_options_layout.addLayout(themes_layout)
        
        # Thema beschrijvingen
        self.theme_description = QTextEdit()
        self.theme_description.setMaximumHeight(100)
        self.theme_description.setReadOnly(True)
        self.theme_description.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 4px;
                font-size: 10px;
            }
        """)
        theme_options_layout.addWidget(self.theme_description)
        
        layout.addWidget(theme_options_group)
        
        # Thema aanpassingen
        custom_group = QGroupBox("🎨 Aangepaste Kleuren")
        custom_layout = QVBoxLayout(custom_group)
        
        # Accent kleur
        accent_layout = QHBoxLayout()
        accent_layout.addWidget(QLabel("🎨 Accent Kleur:"))
        
        self.accent_color_edit = QLineEdit()
        self.accent_color_edit.setPlaceholderText("#4caf50")
        accent_layout.addWidget(self.accent_color_edit)
        
        custom_layout.addLayout(accent_layout)
        
        # Tekst kleur
        text_layout = QHBoxLayout()
        text_layout.addWidget(QLabel("📝 Tekst Kleur:"))
        
        self.text_color_edit = QLineEdit()
        self.text_color_edit.setPlaceholderText("#ffffff")
        text_layout.addWidget(self.text_color_edit)
        
        custom_layout.addLayout(text_layout)
        
        layout.addWidget(custom_group)
        
        self.tab_widget.addTab(tab, "🎨 Thema")
    
    def create_advanced_tab(self):
        """Maak geavanceerde instellingen tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
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
        
        self.tab_widget.addTab(tab, "🔧 Geavanceerd")
    
    def create_plugins_tab(self):
        """Maak plugin beheer tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Plugin instellingen
        plugin_group = QGroupBox("🔌 Plugin Instellingen")
        plugin_layout = QVBoxLayout(plugin_group)
        
        # Plugin directory
        plugin_dir_layout = QHBoxLayout()
        plugin_dir_layout.addWidget(QLabel("📁 Plugin Directory:"))
        
        self.plugin_dir_edit = QLineEdit()
        self.plugin_dir_edit.setPlaceholderText("bijv. /path/naar/plugins")
        plugin_dir_layout.addWidget(self.plugin_dir_edit)
        
        plugin_layout.addLayout(plugin_dir_layout)
        
        # Load on startup
        self.load_on_startup_check = QCheckBox("🚀 Laad Plugins op Start")
        plugin_layout.addWidget(self.load_on_startup_check)
        
        # Auto scan plugins
        self.auto_scan_check = QCheckBox("🔍 Automatisch scannen voor nieuwe plugins")
        plugin_layout.addWidget(self.auto_scan_check)
        
        layout.addWidget(plugin_group)
        
        # Plugin lijst
        plugins_list_group = QGroupBox("📦 Beschikbare Plugins")
        plugins_list_layout = QVBoxLayout(plugins_list_group)
        
        # Plugin lijst widget
        self.plugins_list = QListWidget()
        self.plugins_list.setMaximumHeight(200)
        plugins_list_layout.addWidget(self.plugins_list)
        
        # Plugin knoppen
        plugin_btn_layout = QHBoxLayout()
        
        self.refresh_plugins_btn = QPushButton("🔄 Vernieuwen")
        self.refresh_plugins_btn.clicked.connect(self.refresh_plugins_list)
        plugin_btn_layout.addWidget(self.refresh_plugins_btn)
        
        self.enable_plugin_btn = QPushButton("✅ Enable")
        self.enable_plugin_btn.clicked.connect(self.enable_selected_plugin)
        plugin_btn_layout.addWidget(self.enable_plugin_btn)
        
        self.disable_plugin_btn = QPushButton("❌ Disable")
        self.disable_plugin_btn.clicked.connect(self.disable_selected_plugin)
        plugin_btn_layout.addWidget(self.disable_plugin_btn)
        
        plugins_list_layout.addLayout(plugin_btn_layout)
        layout.addWidget(plugins_list_group)
        
        # Plugin info
        plugin_info_group = QGroupBox("ℹ️ Plugin Informatie")
        plugin_info_layout = QVBoxLayout(plugin_info_group)
        
        self.plugin_info_text = QTextEdit()
        self.plugin_info_text.setMaximumHeight(150)
        self.plugin_info_text.setReadOnly(True)
        self.plugin_info_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 4px;
                font-family: 'Consolas', monospace;
                font-size: 10px;
            }
        """)
        plugin_info_layout.addWidget(self.plugin_info_text)
        
        layout.addWidget(plugin_info_group)
        
        # Connect signals
        self.plugins_list.itemClicked.connect(self.on_plugin_selected)
        
        # Laad initiële plugin lijst
        self.refresh_plugins_list()
        
        self.tab_widget.addTab(tab, "🔌 Plugins")
    
    def refresh_plugins_list(self):
        """Vernieuw plugin lijst"""
        self.plugins_list.clear()
        
        # Voeg ingebouwde plugins toe
        builtin_plugins = [
            {"name": "Enhanced System Monitor", "version": "2.1.0", "enabled": True, "description": "Uitgebreide systeem monitoring met GPU, verwerkingsvoortgang, ETA en performance metrics"},
            {"name": "Audio Analyzer", "version": "1.0.0", "enabled": True, "description": "Audio analyse en visualisatie tools"},
            {"name": "Batch Processor", "version": "1.0.0", "enabled": True, "description": "Batch verwerking van meerdere bestanden"}
        ]
        
        for plugin in builtin_plugins:
            status = "✅" if plugin["enabled"] else "❌"
            item_text = f"{status} {plugin['name']} v{plugin['version']}"
            
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, plugin)
            self.plugins_list.addItem(item)
    
    def on_plugin_selected(self, item):
        """Plugin geselecteerd"""
        plugin_data = item.data(Qt.ItemDataRole.UserRole)
        if plugin_data:
            info_text = f"""
Plugin: {plugin_data['name']}
Versie: {plugin_data['version']}
Status: {'Enabled' if plugin_data['enabled'] else 'Disabled'}

Beschrijving:
{plugin_data['description']}
"""
            self.plugin_info_text.setText(info_text)
    
    def enable_selected_plugin(self):
        """Enable geselecteerde plugin"""
        current_item = self.plugins_list.currentItem()
        if current_item:
            plugin_data = current_item.data(Qt.ItemDataRole.UserRole)
            if plugin_data and not plugin_data["enabled"]:
                plugin_data["enabled"] = True
                status = "✅"
                item_text = f"{status} {plugin_data['name']} v{plugin_data['version']}"
                current_item.setText(item_text)
                current_item.setData(Qt.ItemDataRole.UserRole, plugin_data)
    
    def disable_selected_plugin(self):
        """Disable geselecteerde plugin"""
        current_item = self.plugins_list.currentItem()
        if current_item:
            plugin_data = current_item.data(Qt.ItemDataRole.UserRole)
            if plugin_data and plugin_data["enabled"]:
                plugin_data["enabled"] = False
                status = "❌"
                item_text = f"{status} {plugin_data['name']} v{plugin_data['version']}"
                current_item.setText(item_text)
                current_item.setData(Qt.ItemDataRole.UserRole, plugin_data)
    
    def load_configuration(self):
        """Laad huidige configuratie"""
        try:
            # Algemene instellingen
            self.theme_combo.setCurrentText(config_manager.get("DEFAULT_THEME", "dark"))
            self.font_spin.setValue(int(config_manager.get("DEFAULT_FONT_SIZE", "9")))
            self.auto_cleanup_check.setChecked(config_manager.get("AUTO_CLEANUP_TEMP", "true").lower() == "true")
            self.auto_output_check.setChecked(config_manager.get("AUTO_CREATE_OUTPUT_DIR", "true").lower() == "true")
            
            # Logging
            self.log_level_combo.setCurrentText(config_manager.get("LOG_LEVEL", "INFO"))
            self.log_to_file_check.setChecked(config_manager.get("LOG_TO_FILE", "false").lower() == "true")
            
            # Whisper instellingen
            self.model_combo.setCurrentText(config_manager.get("DEFAULT_WHISPER_MODEL", "large"))
            self.device_combo.setCurrentText(config_manager.get("WHISPER_DEVICE", "cuda"))
            self.workers_spin.setValue(int(config_manager.get("DEFAULT_WORKER_COUNT", "4")))
            
            # Systeem limieten
            self.cpu_limit_spin.setValue(int(config_manager.get("CPU_LIMIT_PERCENTAGE", "80")))
            self.memory_limit_spin.setValue(int(config_manager.get("MEMORY_LIMIT_MB", "8192")))
            
            # Subtitle instellingen
            self.subtitle_type_combo.setCurrentText(config_manager.get("DEFAULT_SUBTITLE_TYPE", "softcoded"))
            self.hardcoded_combo.setCurrentText(config_manager.get("DEFAULT_HARDCODED_LANGUAGE", "dutch_only"))
            
            # LibreTranslate instellingen
            self.server_edit.setText(config_manager.get("LIBRETRANSLATE_SERVER", ""))
            self.timeout_spin.setValue(int(config_manager.get("LIBRETRANSLATE_TIMEOUT", "30")))
            self.rate_limit_spin.setValue(int(config_manager.get("LIBRETRANSLATE_RATE_LIMIT", "0")))
            self.max_chars_spin.setValue(int(config_manager.get("LIBRETRANSLATE_MAX_CHARS", "10000")))
            
            # Panel zichtbaarheid
            visible_panels = config_manager.get_visible_panels()
            self.settings_panel_check.setChecked(visible_panels.get("settings", True))
            self.files_panel_check.setChecked(visible_panels.get("files", True))
            self.processing_panel_check.setChecked(visible_panels.get("processing", True))
            self.charts_panel_check.setChecked(visible_panels.get("charts", True))
            self.batch_panel_check.setChecked(visible_panels.get("batch", True))
            
            # UI instellingen
            self.width_spin.setValue(1200)
            self.height_spin.setValue(800)
            self.splitter1_spin.setValue(300)
            self.splitter2_spin.setValue(600)
            
            # Thema
            self.theme_selector_combo.setCurrentText(config_manager.get("DEFAULT_THEME", "dark"))
            self.preview_theme()
            
            # Plugin instellingen
            self.plugin_dir_edit.setText(config_manager.get("PLUGIN_DIR", ""))
            self.load_on_startup_check.setChecked(config_manager.get("LOAD_PLUGINS_ON_STARTUP", "true").lower() == "true")
            self.auto_scan_check.setChecked(config_manager.get("AUTO_SCAN_PLUGINS", "true").lower() == "true")
            
            # Laad initiële plugin lijst
            self.refresh_plugins_list()
            
            print("✅ Configuratie geladen")
            
        except Exception as e:
            print(f"❌ Fout bij laden configuratie: {e}")
    
    def save_configuration(self):
        """Sla configuratie op"""
        try:
            # Algemene instellingen
            config_manager.set("DEFAULT_THEME", self.theme_combo.currentText())
            config_manager.set("DEFAULT_FONT_SIZE", str(self.font_spin.value()))
            config_manager.set("AUTO_CLEANUP_TEMP", str(self.auto_cleanup_check.isChecked()).lower())
            config_manager.set("AUTO_CREATE_OUTPUT_DIR", str(self.auto_output_check.isChecked()).lower())
            
            # Logging
            config_manager.set("LOG_LEVEL", self.log_level_combo.currentText())
            config_manager.set("LOG_TO_FILE", str(self.log_to_file_check.isChecked()).lower())
            
            # Whisper instellingen
            config_manager.set("DEFAULT_WHISPER_MODEL", self.model_combo.currentText())
            config_manager.set("WHISPER_DEVICE", self.device_combo.currentText())
            config_manager.set("DEFAULT_WORKER_COUNT", str(self.workers_spin.value()))
            
            # Systeem limieten
            config_manager.set("CPU_LIMIT_PERCENTAGE", str(self.cpu_limit_spin.value()))
            config_manager.set("MEMORY_LIMIT_MB", str(self.memory_limit_spin.value()))
            
            # Subtitle instellingen
            config_manager.set("DEFAULT_SUBTITLE_TYPE", self.subtitle_type_combo.currentText())
            config_manager.set("DEFAULT_HARDCODED_LANGUAGE", self.hardcoded_combo.currentText())
            
            # LibreTranslate instellingen
            config_manager.set("LIBRETRANSLATE_SERVER", self.server_edit.text())
            config_manager.set("LIBRETRANSLATE_TIMEOUT", str(self.timeout_spin.value()))
            config_manager.set("LIBRETRANSLATE_RATE_LIMIT", str(self.rate_limit_spin.value()))
            config_manager.set("LIBRETRANSLATE_MAX_CHARS", str(self.max_chars_spin.value()))
            
            # Panel zichtbaarheid
            config_manager.set_panel_visibility("settings", self.settings_panel_check.isChecked())
            config_manager.set_panel_visibility("files", self.files_panel_check.isChecked())
            config_manager.set_panel_visibility("processing", self.processing_panel_check.isChecked())
            config_manager.set_panel_visibility("charts", self.charts_panel_check.isChecked())
            config_manager.set_panel_visibility("batch", self.batch_panel_check.isChecked())
            
            # Plugin instellingen
            config_manager.set("PLUGIN_DIR", self.plugin_dir_edit.text())
            config_manager.set("LOAD_PLUGINS_ON_STARTUP", str(self.load_on_startup_check.isChecked()).lower())
            config_manager.set("AUTO_SCAN_PLUGINS", str(self.auto_scan_check.isChecked()).lower())
            
            # Sla configuratie op
            config_manager.save_configuration()
            
            # Emit signal
            self.config_saved.emit()
            
            # Roep callback aan als deze is ingesteld
            if self.callback:
                self.callback()
            
            QMessageBox.information(self, "✅ Succes", "Configuratie opgeslagen!")
            print("✅ Configuratie opgeslagen")
            
        except Exception as e:
            QMessageBox.critical(self, "❌ Fout", f"Fout bij opslaan configuratie: {e}")
            print(f"❌ Fout bij opslaan configuratie: {e}")
    
    def reset_to_defaults(self):
        """Reset naar standaard instellingen"""
        reply = QMessageBox.question(
            self, "🔄 Reset", 
            "Weet je zeker dat je alle instellingen wilt resetten naar standaard?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            config_manager.reset_to_defaults()
            self.load_configuration()
            QMessageBox.information(self, "✅ Reset", "Instellingen gereset naar standaard!")
    
    def preview_theme(self):
        """Preview het geselecteerde thema"""
        theme_name = self.theme_selector_combo.currentText()
        
        # Thema beschrijvingen
        theme_descriptions = {
            "dark": "🌙 Donker thema - Perfect voor nachtelijk gebruik",
            "light": "☀️ Licht thema - Helder en duidelijk",
            "blue": "🌊 Blauw thema - Professioneel en rustig",
            "green": "🌿 Groen thema - Natuurlijk en ontspannend",
            "purple": "🔮 Paars thema - Creatief en mysterieus",
            "orange": "🔥 Oranje thema - Energiek en warm",
            "cyber": "🤖 Cyber thema - Futuristisch en technisch"
        }
        
        description = theme_descriptions.get(theme_name, "Onbekend thema")
        self.theme_description.setText(description)
        
        # Update preview label styling
        modern_styling = ModernStyling()
        theme = modern_styling.available_themes.get(theme_name, modern_styling.available_themes["dark"])
        
        self.theme_preview_label.setStyleSheet(f"""
            QLabel {{
                padding: 20px;
                border: 2px dashed {theme["border"]};
                border-radius: 8px;
                background-color: {theme["bg"]};
                color: {theme["fg"]};
                font-size: 12px;
            }}
        """)
        
        self.theme_preview_label.setText(f"Preview van '{theme_name}' thema") 