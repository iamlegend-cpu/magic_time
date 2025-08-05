"""
Batch Processor Plugin
Hoofdplugin klasse voor intelligente batch verwerking
"""

import os
from datetime import datetime
from typing import List, Dict, Any
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFileDialog, QGroupBox, QTextEdit,
    QCheckBox, QSpinBox, QComboBox, QProgressBar,
    QListWidget, QListWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QTimer
from PyQt6.QtGui import QFont

from magic_time_studio.ui_pyqt6.features.plugin_manager import PluginBase
from .batch_processor_thread import SmartBatchProcessorThread

class BatchProcessorPlugin(PluginBase):
    """Intelligente Batch Processor Plugin"""
    
    def __init__(self, main_window):
        super().__init__(main_window)
        self.name = "Smart Batch Processor"
        self.version = "2.0.0"
        self.description = "Intelligente batch verwerking met systeem monitoring"
        self.author = "Magic Time Studio"
        self.category = "Processing"
        
        self.batch_files = []
        self.processing_thread = None
        self.system_status = {}
    
    def initialize(self) -> bool:
        """Initialiseer de plugin"""
        print(f"🔌 Smart Batch Processor Plugin geïnitialiseerd: {self.name}")
        return True
    
    def cleanup(self):
        """Cleanup bij afsluiten"""
        print(f"🔌 Smart Batch Processor Plugin cleanup: {self.name}")
        if self.processing_thread and self.processing_thread.isRunning():
            self.processing_thread.stop()
            self.processing_thread.wait()
    
    def get_widget(self) -> QWidget:
        """Retourneer plugin widget"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Titel
        title = QLabel("🧠 Smart Batch Processor")
        title.setStyleSheet("font-weight: bold; font-size: 14px; color: #ff9800;")
        layout.addWidget(title)
        
        # Bestanden sectie
        files_group = QGroupBox("📁 Batch Bestanden")
        files_layout = QVBoxLayout(files_group)
        
        # Bestanden lijst
        self.files_list = QListWidget()
        self.files_list.setMaximumHeight(150)
        files_layout.addWidget(self.files_list)
        
        # Bestand knoppen
        file_btn_layout = QHBoxLayout()
        
        self.add_files_btn = QPushButton("📂 Voeg Bestanden Toe")
        self.add_files_btn.clicked.connect(self.add_files)
        file_btn_layout.addWidget(self.add_files_btn)
        
        self.add_folder_btn = QPushButton("📁 Voeg Map Toe")
        self.add_folder_btn.clicked.connect(self.add_folder)
        file_btn_layout.addWidget(self.add_folder_btn)
        
        self.clear_btn = QPushButton("🗑️ Wis Lijst")
        self.clear_btn.clicked.connect(self.clear_files)
        file_btn_layout.addWidget(self.clear_btn)
        
        files_layout.addLayout(file_btn_layout)
        layout.addWidget(files_group)
        
        # Intelligente instellingen sectie
        settings_group = QGroupBox("🧠 Intelligente Instellingen")
        settings_layout = QVBoxLayout(settings_group)
        
        # Auto-detectie info
        auto_info = QLabel("🔍 Systeem wordt automatisch geanalyseerd voor optimale performance")
        auto_info.setStyleSheet("color: #4caf50; font-style: italic;")
        settings_layout.addWidget(auto_info)
        
        # Verwerking opties
        options_layout = QHBoxLayout()
        
        self.parallel_check = QCheckBox("Parallel verwerken (Aanbevolen)")
        self.parallel_check.setChecked(True)
        options_layout.addWidget(self.parallel_check)
        
        self.workers_label = QLabel("Workers:")
        options_layout.addWidget(self.workers_label)
        
        self.workers_spin = QSpinBox()
        self.workers_spin.setRange(1, 4)
        self.workers_spin.setValue(2)  # Veilige default
        self.workers_spin.setSuffix(" (Auto)")
        options_layout.addWidget(self.workers_spin)
        
        settings_layout.addLayout(options_layout)
        
        # Systeem monitoring
        monitor_layout = QHBoxLayout()
        monitor_layout.addWidget(QLabel("💾 RAM:"))
        
        self.ram_label = QLabel("--")
        self.ram_label.setStyleSheet("color: #2196f3; font-weight: bold;")
        monitor_layout.addWidget(self.ram_label)
        
        monitor_layout.addWidget(QLabel("🖥️ CPU:"))
        
        self.cpu_label = QLabel("--")
        self.cpu_label.setStyleSheet("color: #ff9800; font-weight: bold;")
        monitor_layout.addWidget(self.cpu_label)
        
        settings_layout.addLayout(monitor_layout)
        
        layout.addWidget(settings_group)
        
        # Verwerking sectie
        processing_group = QGroupBox("⚡ Verwerking")
        processing_layout = QVBoxLayout(processing_group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        processing_layout.addWidget(self.progress_bar)
        
        # Status
        self.status_label = QLabel("Klaar voor intelligente batch verwerking")
        self.status_label.setStyleSheet("color: #888888;")
        processing_layout.addWidget(self.status_label)
        
        # Verwerking knoppen
        process_btn_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("🚀 Start Smart Batch")
        self.start_btn.clicked.connect(self.start_batch)
        process_btn_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹️ Stop")
        self.stop_btn.clicked.connect(self.stop_batch)
        self.stop_btn.setEnabled(False)
        process_btn_layout.addWidget(self.stop_btn)
        
        processing_layout.addLayout(process_btn_layout)
        
        layout.addWidget(processing_group)
        
        # Log sectie
        log_group = QGroupBox("📝 Smart Log")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(120)
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 4px;
                font-family: 'Consolas', monospace;
                font-size: 10px;
            }
        """)
        log_layout.addWidget(self.log_text)
        
        layout.addWidget(log_group)
        
        return widget
    
    def add_files(self):
        """Voeg bestanden toe aan batch"""
        files, _ = QFileDialog.getOpenFileNames(
            self.main_window,
            "Selecteer Bestanden voor Batch Verwerking",
            "",
            "Media bestanden (*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.mp3 *.wav *.m4a *.aac)"
        )
        
        for file_path in files:
            if file_path not in self.batch_files:
                self.batch_files.append(file_path)
                self.files_list.addItem(os.path.basename(file_path))
        
        self.update_status(f"✅ {len(files)} bestand(en) toegevoegd")
    
    def add_folder(self):
        """Voeg map toe aan batch"""
        folder = QFileDialog.getExistingDirectory(
            self.main_window,
            "Selecteer Map voor Batch Verwerking"
        )
        
        if folder:
            added_count = 0
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.lower().endswith(('.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.mp3', '.wav', '.m4a', '.aac')):
                        file_path = os.path.join(root, file)
                        if file_path not in self.batch_files:
                            self.batch_files.append(file_path)
                            self.files_list.addItem(file)
                            added_count += 1
            
            self.update_status(f"✅ {added_count} bestand(en) uit map toegevoegd")
    
    def clear_files(self):
        """Wis bestanden lijst"""
        self.batch_files.clear()
        self.files_list.clear()
        self.update_status("🗑️ Bestanden lijst gewist")
    
    def start_batch(self):
        """Start intelligente batch verwerking"""
        if not self.batch_files:
            QMessageBox.warning(self.main_window, "Waarschuwing", "Geen bestanden geselecteerd!")
            return
        
        # Maak settings
        settings = {
            "parallel": self.parallel_check.isChecked(),
            "workers": self.workers_spin.value(),
            "processing_type": "Smart Batch"
        }
        
        # Start verwerking thread
        self.processing_thread = SmartBatchProcessorThread(self.batch_files, settings)
        self.processing_thread.progress_updated.connect(self.update_progress)
        self.processing_thread.file_processed.connect(self.on_file_processed)
        self.processing_thread.batch_finished.connect(self.on_batch_finished)
        self.processing_thread.error_occurred.connect(self.on_error)
        self.processing_thread.system_status.connect(self.on_system_status)
        
        self.processing_thread.start()
        
        # Update UI
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.update_status("🧠 Intelligente batch verwerking gestart...")
        
        self.log_message(f"🚀 Smart batch gestart met {len(self.batch_files)} bestand(en)")
        self.log_message(f"🔧 Auto-detectie: {self.processing_thread.max_workers} workers")
    
    def stop_batch(self):
        """Stop batch verwerking"""
        if self.processing_thread and self.processing_thread.isRunning():
            self.processing_thread.stop()
            self.processing_thread.wait()
        
        # Update UI
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
        self.update_status("⏹️ Batch verwerking gestopt")
        
        self.log_message("⏹️ Batch verwerking gestopt door gebruiker")
    
    def update_progress(self, value: int, message: str):
        """Update progress bar"""
        self.progress_bar.setValue(value)
        self.update_status(message)
    
    def on_file_processed(self, filename: str, status: str):
        """Bestand verwerkt"""
        self.log_message(f"{status} {filename}")
    
    def on_batch_finished(self):
        """Batch verwerking voltooid"""
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
        self.update_status("✅ Intelligente batch verwerking voltooid!")
        
        self.log_message("✅ Smart batch succesvol voltooid")
    
    def on_error(self, error: str):
        """Fout tijdens verwerking"""
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
        self.update_status(f"❌ Fout: {error}")
        
        self.log_message(f"❌ Fout tijdens batch verwerking: {error}")
    
    def on_system_status(self, status: Dict[str, Any]):
        """Update systeem status"""
        self.system_status = status
        
        # Update labels
        if "memory_gb" in status:
            self.ram_label.setText(f"{status['memory_gb']:.1f}GB")
        if "cpu_percent" in status:
            self.cpu_label.setText(f"{status['cpu_percent']:.1f}%")
        
        # Kleur op basis van veiligheid
        if status.get("is_safe", True):
            self.ram_label.setStyleSheet("color: #4caf50; font-weight: bold;")
            self.cpu_label.setStyleSheet("color: #4caf50; font-weight: bold;")
        else:
            self.ram_label.setStyleSheet("color: #f44336; font-weight: bold;")
            self.cpu_label.setStyleSheet("color: #f44336; font-weight: bold;")
    
    def update_status(self, message: str):
        """Update status label"""
        self.status_label.setText(message)
    
    def log_message(self, message: str):
        """Voeg bericht toe aan log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
        
        # Scroll naar beneden
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def get_menu_items(self) -> list:
        """Retourneer menu items"""
        return [
            {
                "text": "Smart Batch Processor",
                "action": self.show_processor,
                "shortcut": "Ctrl+Shift+B"
            }
        ]
    
    def show_processor(self):
        """Toon processor widget"""
        if hasattr(self, 'widget'):
            self.widget.show()
            self.widget.raise_() 