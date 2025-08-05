"""
Completed Files Panel component voor Magic Time Studio
Handelt voltooide bestanden af
"""

import os
from typing import List
from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QListWidget, QGroupBox, QListWidgetItem, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt

class CompletedFilesPanel(QWidget):
    """Voltooide bestanden paneel"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.completed_files = []
        self.setup_ui()
    
    def setup_ui(self):
        """Setup de UI"""
        layout = QVBoxLayout(self)
        
        completed_group = QGroupBox("✅ Voltooide Bestanden")
        completed_layout = QVBoxLayout(completed_group)
        
        # Styling voor de group box
        completed_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
                background-color: #1a1a1a;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #4CAF50;
                font-size: 14px;
            }
        """)
        
        # Voltooide bestanden lijst
        self.completed_list_widget = QListWidget()
        self.completed_list_widget.setMaximumHeight(200)
        self.completed_list_widget.setMinimumHeight(150)
        
        # Styling voor de list widget
        self.completed_list_widget.setStyleSheet("""
            QListWidget {
                background-color: #2a2a2a;
                border: 1px solid #4CAF50;
                border-radius: 5px;
                color: #ffffff;
                font-size: 12px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #3a3a3a;
                background-color: #2a2a2a;
            }
            QListWidget::item:selected {
                background-color: #4CAF50;
                color: #ffffff;
            }
            QListWidget::item:hover {
                background-color: #3a3a3a;
            }
        """)
        
        completed_layout.addWidget(self.completed_list_widget)
        
        # Knoppen
        buttons_layout = QHBoxLayout()
        
        self.clear_btn = QPushButton("Wis Lijst")
        self.clear_btn.setProperty("class", "danger")
        self.clear_btn.clicked.connect(self.clear_completed)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
            QPushButton:pressed {
                background-color: #b71c1c;
            }
        """)
        buttons_layout.addWidget(self.clear_btn)
        
        self.export_btn = QPushButton("Exporteer Lijst")
        self.export_btn.setProperty("class", "secondary")
        self.export_btn.clicked.connect(self.export_completed_list)
        self.export_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        buttons_layout.addWidget(self.export_btn)
        
        # Test knop voor development
        self.test_btn = QPushButton("Test Voltooide Bestanden")
        self.test_btn.setProperty("class", "info")
        self.test_btn.clicked.connect(self.add_test_files)
        self.test_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
            QPushButton:pressed {
                background-color: #E65100;
            }
        """)
        buttons_layout.addWidget(self.test_btn)
        
        completed_layout.addLayout(buttons_layout)
        
        # Status label
        self.status_label = QLabel("0 bestanden voltooid")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #4CAF50;
                font-size: 11px;
                font-style: italic;
                padding: 5px;
            }
        """)
        completed_layout.addWidget(self.status_label)
        
        layout.addWidget(completed_group)
    
    def add_test_files(self):
        """Voeg test bestanden toe voor development"""
        test_files = [
            "test_video_1.mp4",
            "test_audio_1.mp3", 
            "test_video_2.avi",
            "test_audio_2.wav",
            "test_document.pdf"
        ]
        
        for test_file in test_files:
            self.add_completed_file(test_file, f"output_{test_file}")
    
    def add_completed_file(self, file_path: str, output_path: str = None):
        """Voeg voltooid bestand toe"""
        if file_path not in self.completed_files:
            self.completed_files.append(file_path)
            
            # Maak een mooiere display naam
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            # Bepaal bestandstype
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext in ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv']:
                file_type = "🎬 Video"
            elif file_ext in ['.mp3', '.wav', '.m4a', '.aac']:
                file_type = "🎵 Audio"
            else:
                file_type = "📄 Bestand"
            
            # Maak display tekst
            display_name = f"{file_type} {os.path.basename(file_path)}"
            if output_path:
                display_name += f" → {os.path.basename(output_path)}"
            
            # Voeg timestamp toe
            display_name += f" ({timestamp})"
            
            # Maak list item met icon
            item = QListWidgetItem(f"✅ {display_name}")
            item.setData(Qt.ItemDataRole.UserRole, file_path)  # Sla origineel pad op
            
            self.completed_list_widget.addItem(item)
            
            # Scroll naar beneden om nieuwste item te tonen
            self.completed_list_widget.scrollToBottom()
            
            self.update_status()
    
    def clear_completed(self):
        """Wis voltooide bestanden lijst"""
        self.completed_files.clear()
        self.completed_list_widget.clear()
        self.update_status()
    
    def export_completed_list(self):
        """Exporteer voltooide bestanden lijst"""
        if not self.completed_files:
            QMessageBox.information(self, "Export", "Geen voltooide bestanden om te exporteren.")
            return
        
        # Maak timestamp voor bestandsnaam
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"voltooide_bestanden_{timestamp}.txt"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Exporteer voltooide bestanden",
            default_filename,
            "Tekst bestanden (*.txt);;CSV bestanden (*.csv);;Alle bestanden (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"Voltooide Bestanden - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 50 + "\n\n")
                    
                    for i, file_path in enumerate(self.completed_files, 1):
                        # Krijg bestandsinfo
                        try:
                            file_size = os.path.getsize(file_path)
                            file_size_mb = file_size / (1024 * 1024)
                            file_ext = os.path.splitext(file_path)[1].lower()
                            
                            f.write(f"{i}. {os.path.basename(file_path)}\n")
                            f.write(f"   Pad: {file_path}\n")
                            f.write(f"   Type: {file_ext}\n")
                            f.write(f"   Grootte: {file_size_mb:.2f} MB\n")
                            f.write(f"   Voltooid: {datetime.now().strftime('%H:%M:%S')}\n\n")
                        except Exception as e:
                            f.write(f"{i}. {os.path.basename(file_path)} (fout bij lezen: {e})\n\n")
                
                QMessageBox.information(self, "Export", f"Voltooide bestanden geëxporteerd naar:\n{file_path}")
                
            except Exception as e:
                QMessageBox.critical(self, "Export Fout", f"Fout bij exporteren:\n{str(e)}")
    
    def update_status(self):
        """Update status label"""
        count = len(self.completed_files)
        if count == 0:
            self.status_label.setText("Geen voltooide bestanden")
        elif count == 1:
            self.status_label.setText("1 bestand voltooid")
        else:
            self.status_label.setText(f"{count} bestanden voltooid")
    
    def get_completed_files(self) -> List[str]:
        """Krijg lijst van voltooide bestanden"""
        return self.completed_files.copy() 