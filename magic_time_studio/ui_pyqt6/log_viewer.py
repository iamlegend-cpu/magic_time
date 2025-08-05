"""
Log Viewer voor Magic Time Studio
"""

import os
import sys
import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTextEdit, QScrollArea, QSplitter, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QThread, pyqtSlot
from PyQt6.QtGui import QFont, QPalette, QColor, QTextCursor, QTextCharFormat

from magic_time_studio.core.logging import logger
from magic_time_studio.ui_pyqt6.themes import ThemeManager

class LogViewer(QWidget):
    """PyQt6 Log viewer venster voor live log weergave"""
    
    # Signals
    log_updated = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.theme_manager = ThemeManager()
        self.auto_scroll = True
        self.is_running = False
        self.update_timer = None
        
        self.setup_window()
        self.create_interface()
        self.start_log_monitoring()
        
        print("📋 PyQt6 Log viewer aangemaakt")
    
    def setup_window(self):
        """Setup het log viewer venster"""
        self.setWindowTitle("📋 Log Viewer - Magic Time Studio")
        # setModal is niet beschikbaar voor QWidget, alleen voor QDialog
        
        # Start in een redelijke grootte
        self.setGeometry(300, 300, 1000, 700)
        self.setMinimumSize(800, 600)
        
        # Pas thema toe
        self.theme_manager.apply_theme(self, self.theme_manager.get_current_theme())
    
    def create_interface(self):
        """Maak de interface"""
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        
        # Titel
        title_label = QLabel("📋 Live Log Viewer")
        title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Knoppen
        clear_button = QPushButton("🗑️ Wissen")
        clear_button.clicked.connect(self.clear_log)
        clear_button.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f;
                color: white;
                border: none;
                padding: 8px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #c62828;
            }
        """)
        header_layout.addWidget(clear_button)
        
        self.auto_scroll_button = QPushButton("📌 Auto Scroll: AAN")
        self.auto_scroll_button.clicked.connect(self.toggle_auto_scroll)
        self.auto_scroll_button.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: white;
                border: none;
                padding: 8px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        header_layout.addWidget(self.auto_scroll_button)
        
        refresh_button = QPushButton("🔄 Ververs")
        refresh_button.clicked.connect(self.refresh_log)
        refresh_button.setStyleSheet("""
            QPushButton {
                background-color: #2196f3;
                color: white;
                border: none;
                padding: 8px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1976d2;
            }
        """)
        header_layout.addWidget(refresh_button)
        
        layout.addLayout(header_layout)
        
        # Log viewer
        log_group = QFrame() # Changed from QGroupBox to QFrame
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 9))
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 4px;
            }
        """)
        log_layout.addWidget(self.log_text)
        
        layout.addWidget(log_group)
        
        # Status bar
        self.status_label = QLabel("Klaar")
        self.status_label.setStyleSheet("color: #4caf50; font-weight: bold;")
        layout.addWidget(self.status_label)
        
        # Verbind signals
        self.log_updated.connect(self.add_log_message)
    
    def start_log_monitoring(self):
        """Start log monitoring"""
        self.is_running = True
        
        # Timer voor log updates
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_log)
        self.update_timer.start(1000)  # Elke seconde
        
        print("📋 Log monitoring gestart")
    
    def update_log(self):
        """Update log berichten"""
        try:
            # Haal echte log berichten op van de applicatie
            sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            from magic_time_studio.core.logging import logger
            
            # Probeer nieuwe log berichten op te halen
            if hasattr(logger, 'log_queue') and not logger.log_queue.empty():
                try:
                    message, color = logger.log_queue.get_nowait()
                    self.log_updated.emit(message)
                except:
                    pass
            
            # Voeg een heartbeat bericht toe om te laten zien dat de log viewer actief is
            if self.is_running and datetime.datetime.now().second % 10 < 1:  # Elke 10 seconden
                self.log_updated.emit(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 📋 Log viewer actief - wacht op berichten...")
                
        except Exception as e:
            print(f"❌ Fout bij log update: {e}")
    
    def add_log_message(self, message: str):
        """Voeg log bericht toe"""
        try:
            # Voeg bericht toe aan text edit
            self.log_text.append(message)
            
            # Auto scroll naar beneden
            if self.auto_scroll:
                cursor = self.log_text.textCursor()
                cursor.movePosition(QTextCursor.MoveOperation.End)
                self.log_text.setTextCursor(cursor)
            
            # Update status
            self.update_status()
            
        except Exception as e:
            print(f"❌ Fout bij toevoegen log bericht: {e}")
    
    def clear_log(self):
        """Wis alle log berichten"""
        try:
            self.log_text.clear()
            self.update_status()
            print("🗑️ Log gewist")
        except Exception as e:
            print(f"❌ Fout bij wissen log: {e}")
    
    def refresh_log(self):
        """Ververs log berichten"""
        try:
            # Hier zou je de log opnieuw kunnen laden
            self.add_log_message(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Log verversd")
            print("🔄 Log verversd")
        except Exception as e:
            print(f"❌ Fout bij verversen log: {e}")
    
    def toggle_auto_scroll(self):
        """Toggle auto scroll"""
        self.auto_scroll = not self.auto_scroll
        
        if self.auto_scroll:
            self.auto_scroll_button.setText("📌 Auto Scroll: AAN")
            self.auto_scroll_button.setStyleSheet("""
                QPushButton {
                    background-color: #4caf50;
                    color: white;
                    border: none;
                    padding: 8px;
                    font-weight: bold;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
        else:
            self.auto_scroll_button.setText("📌 Auto Scroll: UIT")
            self.auto_scroll_button.setStyleSheet("""
                QPushButton {
                    background-color: #ff9800;
                    color: white;
                    border: none;
                    padding: 8px;
                    font-weight: bold;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #f57c00;
                }
            """)
        
        print(f"📌 Auto scroll: {'AAN' if self.auto_scroll else 'UIT'}")
    
    def update_status(self):
        """Update status informatie"""
        try:
            # Tel aantal regels
            line_count = self.log_text.document().lineCount()
            
            # Update status label
            self.status_label.setText(f"Regels: {line_count} | Auto Scroll: {'AAN' if self.auto_scroll else 'UIT'}")
            
        except Exception as e:
            print(f"❌ Fout bij update status: {e}")
    
    def closeEvent(self, event):
        """Handle venster sluiten"""
        try:
            self.is_running = False
            
            if self.update_timer:
                self.update_timer.stop()
            
            print("📋 Log viewer gesloten")
            event.accept()
            
        except Exception as e:
            print(f"❌ Fout bij sluiten log viewer: {e}")
            event.accept()
    
    def show(self):
        """Toon het log viewer venster"""
        super().show()
        print("📋 Log viewer getoond")
    
    def add_test_message(self, message: str):
        """Voeg test bericht toe"""
        self.add_log_message(f"[TEST] {message}") 