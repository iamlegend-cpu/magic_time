"""
Plugin beheer tab
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QGroupBox, QLineEdit, QCheckBox, QPushButton,
    QListWidget, QListWidgetItem, QTextEdit
)
from PyQt6.QtCore import Qt

from core.config import config_manager

class PluginsTab(QWidget):
    """Plugin beheer tab"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup de UI"""
        layout = QVBoxLayout(self)
        
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
        """Laad configuratie"""
        try:
            # Plugin instellingen
            self.plugin_dir_edit.setText(config_manager.get("PLUGIN_DIR", ""))
            self.load_on_startup_check.setChecked(config_manager.get("LOAD_PLUGINS_ON_STARTUP", "true").lower() == "true")
            self.auto_scan_check.setChecked(config_manager.get("AUTO_SCAN_PLUGINS", "true").lower() == "true")
            
        except Exception as e:
            print(f"❌ Fout bij laden plugin configuratie: {e}")
    
    def save_configuration(self):
        """Sla configuratie op"""
        try:
            # Plugin instellingen
            config_manager.set("PLUGIN_DIR", self.plugin_dir_edit.text())
            config_manager.set("LOAD_PLUGINS_ON_STARTUP", str(self.load_on_startup_check.isChecked()).lower())
            config_manager.set("AUTO_SCAN_PLUGINS", str(self.auto_scan_check.isChecked()).lower())
            
        except Exception as e:
            print(f"❌ Fout bij opslaan plugin configuratie: {e}")
