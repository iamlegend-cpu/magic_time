"""
Plugin Manager voor Magic Time Studio
Beheert plugins en extensies
"""

import os
import sys
import importlib
import importlib.util
from typing import Dict, List, Any, Optional
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGroupBox, QTextEdit, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt, Signal

class PluginBase:
    """Basis klasse voor alle plugins"""
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.name = "Unknown Plugin"
        self.version = "1.0.0"
        self.description = "No description"
        self.author = "Unknown"
        self.category = "General"
        self.enabled = True
    
    def initialize(self) -> bool:
        """Initialiseer de plugin"""
        return True
    
    def cleanup(self):
        """Cleanup bij afsluiten"""
        pass
    
    def get_widget(self) -> QWidget:
        """Retourneer plugin widget"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel(f"Plugin: {self.name}"))
        return widget
    
    def get_menu_items(self) -> list:
        """Retourneer menu items"""
        return []

class PluginManager:
    """Beheert plugins en extensies"""
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.plugins = {}
        self.plugin_widgets = {}
        self.plugin_directories = [
            os.path.join(os.path.dirname(__file__), "plugins"),
            os.path.join(os.path.dirname(__file__), "..", "..", "plugins")
        ]
    
    def scan_plugins(self) -> List[Dict[str, Any]]:
        """Scan voor beschikbare plugins"""
        print("🔍 Plugins scannen...")
        
        found_plugins = []
        
        # Scan plugin directories
        for plugin_dir in self.plugin_directories:
            if os.path.exists(plugin_dir):
                for filename in os.listdir(plugin_dir):
                    if filename.endswith('.py') and not filename.startswith('__'):
                        plugin_path = os.path.join(plugin_dir, filename)
                        plugin_info = self.load_plugin_info(plugin_path)
                        if plugin_info:
                            found_plugins.append(plugin_info)
        
        # Laad ingebouwde plugins
        self.load_builtin_plugins()
        
        print(f"✅ {len(found_plugins)} plugin(s) gevonden")
        return found_plugins
    
    def load_builtin_plugins(self):
        """Laad ingebouwde plugins"""
        try:
            # Audio Analyzer Plugin
            from .plugins.audio_analyzer_plugin import AudioAnalyzerPlugin
            self.register_plugin("audio_analyzer", AudioAnalyzerPlugin(self.main_window))
            
            # Batch Processor Plugin
            from .plugins.batch_processor_plugin import BatchProcessorPlugin
            self.register_plugin("batch_processor", BatchProcessorPlugin(self.main_window))
            
            # System Monitor Plugin (uitgeschakeld - dubbele GPU monitoring)
            # from .plugins.system_monitor_plugin import EnhancedSystemMonitorPlugin
            # self.register_plugin("system_monitor", EnhancedSystemMonitorPlugin(self.main_window))
            
            print("✅ Ingebouwde plugins geladen")
            
        except Exception as e:
            print(f"❌ Fout bij laden ingebouwde plugins: {e}")
    
    def load_plugin_info(self, plugin_path: str) -> Optional[Dict[str, Any]]:
        """Laad plugin informatie"""
        try:
            spec = importlib.util.spec_from_file_location("plugin", plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Zoek naar PluginBase subclasses
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    issubclass(attr, PluginBase) and 
                    attr != PluginBase):
                    
                    plugin_instance = attr(self.main_window)
                    return {
                        "name": plugin_instance.name,
                        "version": plugin_instance.version,
                        "description": plugin_instance.description,
                        "author": plugin_instance.author,
                        "category": plugin_instance.category,
                        "path": plugin_path,
                        "class": attr
                    }
            
        except Exception as e:
            print(f"❌ Fout bij laden plugin {plugin_path}: {e}")
        
        return None
    
    def register_plugin(self, plugin_id: str, plugin_instance: PluginBase):
        """Registreer een plugin"""
        self.plugins[plugin_id] = plugin_instance
        print(f"🔌 Plugin geregistreerd: {plugin_instance.name}")
    
    def get_plugin(self, plugin_id: str) -> Optional[PluginBase]:
        """Krijg plugin instance"""
        return self.plugins.get(plugin_id)
    
    def get_all_plugins(self) -> Dict[str, PluginBase]:
        """Krijg alle plugins"""
        return self.plugins
    
    def enable_plugin(self, plugin_id: str) -> bool:
        """Enable een plugin"""
        plugin = self.get_plugin(plugin_id)
        if plugin:
            plugin.enabled = True
            print(f"✅ Plugin enabled: {plugin.name}")
            return True
        return False
    
    def disable_plugin(self, plugin_id: str) -> bool:
        """Disable een plugin"""
        plugin = self.get_plugin(plugin_id)
        if plugin:
            plugin.enabled = False
            print(f"❌ Plugin disabled: {plugin.name}")
            return True
        return False
    
    def get_plugin_widget(self, plugin_id: str) -> Optional[QWidget]:
        """Krijg plugin widget"""
        plugin = self.get_plugin(plugin_id)
        if plugin and plugin.enabled:
            if plugin_id not in self.plugin_widgets:
                self.plugin_widgets[plugin_id] = plugin.get_widget()
            return self.plugin_widgets[plugin_id]
        return None
    
    def cleanup_plugins(self):
        """Cleanup alle plugins"""
        for plugin in self.plugins.values():
            try:
                plugin.cleanup()
            except Exception as e:
                print(f"❌ Fout bij cleanup plugin {plugin.name}: {e}")
    
    def get_plugin_info(self) -> List[Dict[str, Any]]:
        """Krijg informatie over alle plugins"""
        info = []
        for plugin_id, plugin in self.plugins.items():
            info.append({
                "id": plugin_id,
                "name": plugin.name,
                "version": plugin.version,
                "description": plugin.description,
                "author": plugin.author,
                "category": plugin.category,
                "enabled": plugin.enabled
            })
        return info

class PluginPanel(QWidget):
    """Plugin management panel"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.plugin_manager = None
        self.setup_ui()
    
    def setup_ui(self):
        """Setup de UI"""
        layout = QVBoxLayout(self)
        
        # Titel
        title = QLabel("🔌 Plugin Manager")
        title.setStyleSheet("font-weight: bold; font-size: 14px; color: #9c27b0;")
        layout.addWidget(title)
        
        # Plugin lijst
        plugins_group = QGroupBox("📦 Beschikbare Plugins")
        plugins_layout = QVBoxLayout(plugins_group)
        
        self.plugins_list = QListWidget()
        self.plugins_list.setMaximumHeight(200)
        plugins_layout.addWidget(self.plugins_list)
        
        # Plugin knoppen
        plugin_btn_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("🔄 Vernieuwen")
        self.refresh_btn.clicked.connect(self.refresh_plugins)
        plugin_btn_layout.addWidget(self.refresh_btn)
        
        self.enable_btn = QPushButton("✅ Enable")
        self.enable_btn.clicked.connect(self.enable_selected)
        plugin_btn_layout.addWidget(self.enable_btn)
        
        self.disable_btn = QPushButton("❌ Disable")
        self.disable_btn.clicked.connect(self.disable_selected)
        plugin_btn_layout.addWidget(self.disable_btn)
        
        plugins_layout.addLayout(plugin_btn_layout)
        layout.addWidget(plugins_group)
        
        # Plugin info
        info_group = QGroupBox("ℹ️ Plugin Informatie")
        info_layout = QVBoxLayout(info_group)
        
        self.info_text = QTextEdit()
        self.info_text.setMaximumHeight(150)
        self.info_text.setReadOnly(True)
        self.info_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 4px;
                font-family: 'Consolas', monospace;
                font-size: 10px;
            }
        """)
        info_layout.addWidget(self.info_text)
        
        layout.addWidget(info_group)
        
        # Connect signals
        self.plugins_list.itemClicked.connect(self.on_plugin_selected)
    
    def set_plugin_manager(self, plugin_manager: PluginManager):
        """Stel plugin manager in"""
        self.plugin_manager = plugin_manager
        self.refresh_plugins()
    
    def refresh_plugins(self):
        """Vernieuw plugin lijst"""
        if not self.plugin_manager:
            return
        
        self.plugins_list.clear()
        plugin_info = self.plugin_manager.get_plugin_info()
        
        for info in plugin_info:
            status = "✅" if info["enabled"] else "❌"
            item_text = f"{status} {info['name']} v{info['version']}"
            
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, info)
            self.plugins_list.addItem(item)
    
    def on_plugin_selected(self, item):
        """Plugin geselecteerd"""
        info = item.data(Qt.ItemDataRole.UserRole)
        if info:
            info_text = f"""
Plugin: {info['name']}
Versie: {info['version']}
Auteur: {info['author']}
Categorie: {info['category']}
Status: {'Enabled' if info['enabled'] else 'Disabled'}

Beschrijving:
{info['description']}
            """
            self.info_text.setText(info_text)
    
    def enable_selected(self):
        """Enable geselecteerde plugin"""
        current_item = self.plugins_list.currentItem()
        if current_item and self.plugin_manager:
            info = current_item.data(Qt.ItemDataRole.UserRole)
            if info:
                self.plugin_manager.enable_plugin(info['id'])
                self.refresh_plugins()
    
    def disable_selected(self):
        """Disable geselecteerde plugin"""
        current_item = self.plugins_list.currentItem()
        if current_item and self.plugin_manager:
            info = current_item.data(Qt.ItemDataRole.UserRole)
            if info:
                self.plugin_manager.disable_plugin(info['id'])
                self.refresh_plugins() 