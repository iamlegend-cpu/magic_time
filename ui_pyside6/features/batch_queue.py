"""
Batch Processing Queue voor Magic Time Studio
Beheer meerdere bestanden tegelijk
"""

import os
import time
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QListWidget, QListWidgetItem,
    QGroupBox, QSpinBox, QCheckBox, QProgressBar,
    QMessageBox, QFrame
)
from PySide6.QtCore import Qt, Signal, QThread, QTimer
from PySide6.QtGui import QFont, QColor, QBrush

class ProcessingStatus(Enum):
    """Status van batch items"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class BatchItem:
    """Batch item data"""
    file_path: str
    status: ProcessingStatus
    progress: float = 0.0
    error_message: str = ""
    start_time: Optional[float] = None
    end_time: Optional[float] = None

class BatchQueueManager(QWidget):
    """Manager voor batch processing queue"""
    
    # Signals
    item_started = Signal(str)  # file_path
    item_completed = Signal(str)  # file_path
    item_failed = Signal(str, str)  # file_path, error
    queue_completed = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.queue: List[BatchItem] = []
        self.current_item: Optional[BatchItem] = None
        self.processing = False
        self.max_concurrent = 1
        self.auto_start = False
        self.continue_on_error = True
        
        self.setup_ui()
        self.setup_timer()
    
    def setup_ui(self):
        """Setup de UI"""
        layout = QVBoxLayout(self)
        
        # Titel
        title = QLabel("📋 Batch Processing Queue")
        title.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff;")
        layout.addWidget(title)
        
        # Settings
        settings_group = QGroupBox("⚙️ Instellingen")
        settings_layout = QVBoxLayout(settings_group)
        
        # Max concurrent processes
        concurrent_layout = QHBoxLayout()
        concurrent_layout.addWidget(QLabel("Max gelijktijdig:"))
        self.max_concurrent_spin = QSpinBox()
        self.max_concurrent_spin.setRange(1, 10)
        self.max_concurrent_spin.setValue(1)
        self.max_concurrent_spin.valueChanged.connect(self.on_max_concurrent_changed)
        concurrent_layout.addWidget(self.max_concurrent_spin)
        settings_layout.addLayout(concurrent_layout)
        
        # Auto start checkbox
        self.auto_start_check = QCheckBox("Auto-start na toevoegen")
        self.auto_start_check.setChecked(False)
        self.auto_start_check.toggled.connect(self.on_auto_start_changed)
        settings_layout.addWidget(self.auto_start_check)
        
        # Continue on error checkbox
        self.continue_on_error_check = QCheckBox("Doorgaan bij fouten")
        self.continue_on_error_check.setChecked(True)
        self.continue_on_error_check.toggled.connect(self.on_continue_on_error_changed)
        settings_layout.addWidget(self.continue_on_error_check)
        
        layout.addWidget(settings_group)
        
        # Queue controls
        controls_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("Start Queue")
        self.start_btn.setProperty("class", "primary")
        self.start_btn.clicked.connect(self.start_queue)
        controls_layout.addWidget(self.start_btn)
        
        self.pause_btn = QPushButton("Pause")
        self.pause_btn.setProperty("class", "secondary")
        self.pause_btn.clicked.connect(self.pause_queue)
        self.pause_btn.setEnabled(False)
        controls_layout.addWidget(self.pause_btn)
        
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setProperty("class", "danger")
        self.stop_btn.clicked.connect(self.stop_queue)
        self.stop_btn.setEnabled(False)
        controls_layout.addWidget(self.stop_btn)
        
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_queue)
        controls_layout.addWidget(self.clear_btn)
        
        layout.addLayout(controls_layout)
        
        # Queue list
        queue_group = QGroupBox("📋 Wachtrij")
        queue_layout = QVBoxLayout(queue_group)
        
        self.queue_list = QListWidget()
        self.queue_list.setMaximumHeight(200)
        queue_layout.addWidget(self.queue_list)
        
        # Queue progress
        self.queue_progress = QProgressBar()
        self.queue_progress.setRange(0, 100)
        self.queue_progress.setValue(0)
        queue_layout.addWidget(self.queue_progress)
        
        # Status label
        self.queue_status_label = QLabel("Wachtrij leeg")
        self.queue_status_label.setStyleSheet("color: #ff9800; font-weight: bold;")
        queue_layout.addWidget(self.queue_status_label)
        
        layout.addWidget(queue_group)
    
    def setup_timer(self):
        """Setup timer voor updates"""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_queue_display)
        self.update_timer.start(500)  # Elke halve seconde
    
    def add_files(self, file_paths: List[str]):
        """Voeg bestanden toe aan de queue"""
        for file_path in file_paths:
            if not any(item.file_path == file_path for item in self.queue):
                batch_item = BatchItem(
                    file_path=file_path,
                    status=ProcessingStatus.PENDING
                )
                self.queue.append(batch_item)
        
        self.update_queue_display()
        self.update_queue_progress()
        
        # Auto-start indien ingeschakeld
        if self.auto_start and not self.processing:
            self.start_queue()
        
        print(f"📋 {len(file_paths)} bestand(en) toegevoegd aan batch queue")
    
    def start_queue(self):
        """Start de batch queue"""
        if not self.queue:
            QMessageBox.warning(self, "Waarschuwing", "Geen bestanden in de wachtrij!")
            return
        
        self.processing = True
        self.start_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.stop_btn.setEnabled(True)
        
        # Start processing thread
        self.process_next_item()
        
        print("🚀 Batch queue gestart")
    
    def pause_queue(self):
        """Pause de batch queue"""
        self.processing = False
        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        
        print("⏸️ Batch queue gepauzeerd")
    
    def stop_queue(self):
        """Stop de batch queue"""
        self.processing = False
        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        
        # Reset current item
        if self.current_item:
            self.current_item.status = ProcessingStatus.CANCELLED
            self.current_item = None
        
        print("⏹️ Batch queue gestopt")
    
    def clear_queue(self):
        """Wis de batch queue"""
        self.queue.clear()
        self.current_item = None
        self.update_queue_display()
        self.update_queue_progress()
        
        print("🗑️ Batch queue gewist")
    
    def process_next_item(self):
        """Verwerk het volgende item"""
        if not self.processing:
            return
        
        # Zoek naar pending items
        pending_items = [item for item in self.queue if item.status == ProcessingStatus.PENDING]
        
        if not pending_items:
            # Geen pending items meer
            self.queue_completed.emit()
            self.processing = False
            self.start_btn.setEnabled(True)
            self.pause_btn.setEnabled(False)
            self.stop_btn.setEnabled(False)
            return
        
        # Start het volgende item
        self.current_item = pending_items[0]
        self.current_item.status = ProcessingStatus.PROCESSING
        self.current_item.start_time = time.time()
        
        self.item_started.emit(self.current_item.file_path)
        
        # Simuleer processing (in echte implementatie zou dit de echte processing zijn)
        self.simulate_processing()
    
    def simulate_processing(self):
        """Simuleer processing van een item"""
        if not self.current_item:
            return
        
        # Simuleer progress
        progress = 0
        while progress < 100 and self.current_item.status == ProcessingStatus.PROCESSING:
            progress += 10
            self.current_item.progress = progress
            time.sleep(0.5)  # Simuleer werk
        
        # Markeer als voltooid
        self.current_item.status = ProcessingStatus.COMPLETED
        self.current_item.end_time = time.time()
        
        self.item_completed.emit(self.current_item.file_path)
        
        # Ga naar volgende item
        self.current_item = None
        self.process_next_item()
    
    def update_queue_display(self):
        """Update de queue display"""
        self.queue_list.clear()
        
        for item in self.queue:
            # Maak status icoon
            status_icons = {
                ProcessingStatus.PENDING: "⏳",
                ProcessingStatus.PROCESSING: "🔄",
                ProcessingStatus.COMPLETED: "✅",
                ProcessingStatus.FAILED: "❌",
                ProcessingStatus.CANCELLED: "⏹️"
            }
            
            icon = status_icons.get(item.status, "❓")
            filename = os.path.basename(item.file_path)
            
            if item.status == ProcessingStatus.PROCESSING:
                item_text = f"{icon} {filename} ({item.progress:.0f}%)"
            else:
                item_text = f"{icon} {filename}"
            
            list_item = QListWidgetItem(item_text)
            
            # Stel kleur in gebaseerd op status
            if item.status == ProcessingStatus.COMPLETED:
                list_item.setForeground(QBrush(QColor(76, 175, 80)))  # Groen
            elif item.status == ProcessingStatus.FAILED:
                list_item.setForeground(QBrush(QColor(244, 67, 54)))  # Rood
            elif item.status == ProcessingStatus.PROCESSING:
                list_item.setForeground(QBrush(QColor(255, 193, 7)))  # Geel
            else:
                list_item.setForeground(QBrush(QColor(158, 158, 158)))  # Grijs
            
            self.queue_list.addItem(list_item)
    
    def update_queue_progress(self):
        """Update queue progress"""
        if not self.queue:
            self.queue_progress.setValue(0)
            self.queue_status_label.setText("Wachtrij leeg")
            return
        
        # Bereken totale progress
        total_items = len(self.queue)
        completed_items = len([item for item in self.queue if item.status == ProcessingStatus.COMPLETED])
        failed_items = len([item for item in self.queue if item.status == ProcessingStatus.FAILED])
        
        total_progress = ((completed_items + failed_items) / total_items) * 100
        self.queue_progress.setValue(int(total_progress))
        
        # Update status label
        if self.processing:
            status_text = f"Verwerking: {completed_items}/{total_items} voltooid"
        else:
            status_text = f"Gepauzeerd: {completed_items}/{total_items} voltooid"
        
        self.queue_status_label.setText(status_text)
    
    def on_max_concurrent_changed(self, value: int):
        """Max concurrent processes gewijzigd"""
        self.max_concurrent = value
        print(f"⚙️ Max gelijktijdige processen: {value}")
    
    def on_auto_start_changed(self, checked: bool):
        """Auto-start gewijzigd"""
        self.auto_start = checked
        print(f"⚙️ Auto-start: {'Aan' if checked else 'Uit'}")
    
    def on_continue_on_error_changed(self, checked: bool):
        """Continue on error gewijzigd"""
        self.continue_on_error = checked
        print(f"⚙️ Doorgaan bij fouten: {'Aan' if checked else 'Uit'}")
    
    def get_queue_status(self) -> Dict:
        """Haal queue status op"""
        return {
            "total": len(self.queue),
            "pending": len([item for item in self.queue if item.status == ProcessingStatus.PENDING]),
            "processing": len([item for item in self.queue if item.status == ProcessingStatus.PROCESSING]),
            "completed": len([item for item in self.queue if item.status == ProcessingStatus.COMPLETED]),
            "failed": len([item for item in self.queue if item.status == ProcessingStatus.FAILED]),
            "cancelled": len([item for item in self.queue if item.status == ProcessingStatus.CANCELLED])
        } 