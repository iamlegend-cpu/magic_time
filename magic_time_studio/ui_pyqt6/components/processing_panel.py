"""
Processing Panel component voor Magic Time Studio
Handelt verwerking en progress af
"""

import os
from datetime import datetime
from typing import List, Dict
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QProgressBar, QGroupBox, QTextEdit, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, pyqtSignal

class ProcessingPanel(QWidget):
    """Verwerking paneel"""
    
    processing_started = pyqtSignal(list, dict)
    processing_stopped = pyqtSignal()
    file_completed = pyqtSignal(str)  # Signal om bestand uit "nog te doen" lijst te verwijderen
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_processing = False
        self.completed_files = []
        self.setup_ui()
    
    def setup_ui(self):
        """Setup de UI"""
        layout = QVBoxLayout(self)
        
        # Verwerking groep
        processing_group = QGroupBox("⚙️ Verwerking")
        processing_layout = QVBoxLayout(processing_group)
        
        # Status label
        self.status_label = QLabel("Klaar voor verwerking")
        processing_layout.addWidget(self.status_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        processing_layout.addWidget(self.progress_bar)
        
        # Knoppen
        buttons_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("▶️ Start Verwerking")
        self.start_btn.setProperty("class", "primary")
        self.start_btn.clicked.connect(self.start_processing)
        buttons_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹️ Stop")
        self.stop_btn.setProperty("class", "danger")
        self.stop_btn.clicked.connect(self.stop_processing)
        self.stop_btn.setEnabled(False)
        buttons_layout.addWidget(self.stop_btn)
        
        processing_layout.addLayout(buttons_layout)
        
        # Real-time console output viewer
        console_group = QGroupBox("📊 Real-time Console Output")
        console_layout = QVBoxLayout(console_group)
        
        # Console output met progress tracking
        self.console_output = QTextEdit()
        self.console_output.setMaximumHeight(120)
        self.console_output.setReadOnly(True)
        self.console_output.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #00ff00;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
                border: 1px solid #333;
                border-radius: 4px;
            }
        """)
        console_layout.addWidget(self.console_output)
        
        # Progress indicator voor console output
        self.console_progress_label = QLabel("Console Progress: 0%")
        self.console_progress_label.setStyleSheet("""
            QLabel {
                color: #00ff00;
                font-weight: bold;
                font-size: 12px;
            }
        """)
        console_layout.addWidget(self.console_progress_label)
        
        processing_layout.addWidget(console_group)
        
        # Log output (oude versie - nu kleiner)
        self.log_output = QTextEdit()
        self.log_output.setMaximumHeight(80)
        self.log_output.setReadOnly(True)
        processing_layout.addWidget(self.log_output)
        
        layout.addWidget(processing_group)
        
        # Voltooide bestanden groep
        completed_group = QGroupBox("✅ Voltooide Bestanden")
        completed_layout = QVBoxLayout(completed_group)
        
        # Voltooide bestanden lijst
        self.completed_list = QListWidget()
        self.completed_list.setMaximumHeight(150)
        completed_layout.addWidget(self.completed_list)
        
        # Wis knop
        clear_completed_btn = QPushButton("🗑️ Wis Voltooide Lijst")
        clear_completed_btn.clicked.connect(self.clear_completed_list)
        completed_layout.addWidget(clear_completed_btn)
        
        layout.addWidget(completed_group)
    
    def start_processing(self):
        """Start verwerking (legacy methode)"""
        if self.is_processing:
            print("⚠️ Verwerking al bezig, negeer legacy start request")
            return
        
        print("🚀 ProcessingPanel.start_processing: Legacy start request")
        # Emit een signal om de hoofdapplicatie te laten weten dat verwerking moet starten
        # De hoofdapplicatie zal dan de bestanden ophalen en verwerking starten
        self.processing_started.emit([], {})
    
    def start_processing_with_settings(self, files: List[str], settings: Dict):
        """Start verwerking met bestanden en instellingen"""
        if self.is_processing:
            print("⚠️ Verwerking al bezig, negeer dubbele start request")
            return
        
        print(f"🚀 ProcessingPanel.start_processing_with_settings: Start verwerking met {len(files)} bestanden")
        self.is_processing = True
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("Verwerking gestart...")
        self.log_output.append(f"🚀 Verwerking gestart met {len(files)} bestanden")
        
        # Wis console output voor nieuwe verwerking
        self.clear_console_output()
        
        # Emit signal
        self.processing_started.emit(files, settings)
    
    def stop_processing(self):
        """Stop verwerking"""
        if not self.is_processing:
            return
        
        print("🛑 ProcessingPanel.stop_processing() aangeroepen")
        
        self.is_processing = False
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText("Verwerking gestopt")
        self.log_output.append("🛑 Verwerking gestopt door gebruiker")
        
        # Wis console output bij stoppen
        self.clear_console_output()
        
        # Emit signal naar hoofdapplicatie
        self.processing_stopped.emit()
        
        print("✅ ProcessingPanel stop signal verzonden")
    
    def update_progress(self, value: float, status: str = ""):
        """Update voortgangsbalk met real-time updates"""
        self.progress_bar.setValue(int(value))
        if status:
            # Update status label met real-time info
            self.status_label.setText(status)
            
            # Voeg alleen nieuwe status toe aan log (niet elke progress update)
            # Parse Fast Whisper progress
            if "🎤 Fast Whisper:" in status and "%" in status:
                try:
                    # Extract percentage from status message
                    percent_str = status.split("🎤 Fast Whisper:")[1].split("%")[0].strip()
                    percent = float(percent_str)
                    return percent
                except:
                    pass
            else:
                # Voor andere updates, altijd loggen
                self.log_output.append(f"📊 {status}")
            
            # Scroll naar beneden
            self.log_output.ensureCursorVisible()
    
    def add_console_output(self, message: str, progress: float = None):
        """Voeg bericht toe aan console output met optionele progress"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]  # Milliseconden
        
        # Format console entry met progress als beschikbaar
        if progress is not None:
            console_entry = f"[{timestamp}] {message} ({progress:.1%})"
        else:
            console_entry = f"[{timestamp}] {message}"
        
        # Voeg toe aan console output
        self.console_output.append(console_entry)
        
        # Scroll naar beneden
        self.console_output.ensureCursorVisible()
    
    def clear_console_output(self):
        """Wis console output"""
        self.console_output.clear()
        self.console_progress_label.setText("Console Progress: 0%")
    
    def update_console_progress(self, progress: float):
        """Update alleen de console progress indicator"""
        self.console_progress_label.setText(f"Console Progress: {progress:.1%}")
    
    def processing_finished(self):
        """Verwerking voltooid"""
        self.is_processing = False
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText("Verwerking voltooid!")
        self.log_output.append("✅ Verwerking voltooid!")
        
        # Wis console output bij voltooien
        self.clear_console_output()
    
    def add_completed_file(self, file_path: str, output_path: str = None):
        """Voeg voltooid bestand toe aan de lijst (alleen video bestanden)"""
        print(f"🔍 [DEBUG] ProcessingPanel.add_completed_file aangeroepen: {file_path}")
        
        # Controleer of het een video bestand is
        video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']
        if not any(file_path.lower().endswith(ext) for ext in video_extensions):
            print(f"🔍 [DEBUG] Skip niet-video bestand: {file_path}")
            return  # Skip niet-video bestanden
        
        print(f"🔍 [DEBUG] Video bestand gedetecteerd, voeg toe...")
        
        # Voeg toe aan interne lijst
        completed_item = {
            'file_path': file_path,
            'output_path': output_path,
            'completed_at': datetime.now().strftime("%H:%M:%S")
        }
        self.completed_files.append(completed_item)
        print(f"🔍 [DEBUG] Toegevoegd aan interne lijst: {completed_item}")
        
        # Voeg toe aan UI lijst - gebruik de volledige bestandsnaam zoals in de verwerkingslijst
        display_text = f"✅ {file_path} ({completed_item['completed_at']})"
        item = QListWidgetItem(display_text)
        item.setData(Qt.ItemDataRole.UserRole, completed_item)
        self.completed_list.addItem(item)
        print(f"🔍 [DEBUG] Toegevoegd aan UI lijst: {display_text}")
        print(f"🔍 [DEBUG] Aantal items in completed_list: {self.completed_list.count()}")
        
        # Emit signal om bestand uit "nog te doen" lijst te verwijderen
        self.file_completed.emit(file_path)
        
        # Log
        self.log_output.append(f"✅ {file_path} voltooid")
        print(f"🔍 [DEBUG] add_completed_file voltooid")
    
    def get_completed_files(self) -> List[str]:
        """Haal voltooide bestanden lijst op"""
        return [item['file_path'] for item in self.completed_files]
    
    def clear_completed_list(self):
        """Wis de voltooide bestanden lijst"""
        self.completed_list.clear()
        self.completed_files.clear()
        self.log_output.append("🗑️ Voltooide lijst gewist") 