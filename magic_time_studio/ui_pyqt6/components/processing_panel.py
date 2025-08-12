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
        try:
            # Emit een signal om de hoofdapplicatie te laten weten dat verwerking moet starten
            # De hoofdapplicatie zal dan de bestanden ophalen en verwerking starten
            self.processing_started.emit([], {})
        except Exception as e:
            print(f"⚠️ Fout bij start_processing: {e}")
    
    def start_processing_with_settings(self, files: List[str], settings: Dict):
        """Start verwerking met bestanden en instellingen"""
        if self.is_processing:
            print("⚠️ Verwerking al bezig, negeer dubbele start request")
            return
        
        print(f"🚀 ProcessingPanel.start_processing_with_settings: Start verwerking met {len(files)} bestanden")
        
        try:
            self.is_processing = True
            
            if hasattr(self, 'start_btn'):
                self.start_btn.setEnabled(False)
            if hasattr(self, 'stop_btn'):
                self.stop_btn.setEnabled(True)
            if hasattr(self, 'progress_bar'):
                self.progress_bar.setValue(0)
            if hasattr(self, 'status_label'):
                self.status_label.setText("Verwerking gestart...")
            if hasattr(self, 'log_output'):
                self.log_output.append(f"🚀 Verwerking gestart met {len(files)} bestanden")
            
            # Wis console output voor nieuwe verwerking
            self.clear_console_output()
            
            # Emit signal
            self.processing_started.emit(files, settings)
        except Exception as e:
            print(f"⚠️ Fout bij start_processing_with_settings: {e}")
    
    def stop_processing(self):
        """Stop verwerking"""
        if not self.is_processing:
            print("⚠️ ProcessingPanel: Verwerking is al gestopt")
            return
        
        print("🛑 ProcessingPanel.stop_processing() aangeroepen")
        
        try:
            # Zet processing status op False
            self.is_processing = False
            
            # Update UI onmiddellijk
            if hasattr(self, 'start_btn'):
                self.start_btn.setEnabled(True)
            if hasattr(self, 'stop_btn'):
                self.stop_btn.setEnabled(False)
            if hasattr(self, 'status_label'):
                self.status_label.setText("Verwerking gestopt...")
            if hasattr(self, 'log_output'):
                self.log_output.append("🛑 Verwerking gestopt door gebruiker")
            
            # Wis console output bij stoppen
            self.clear_console_output()
        except Exception as e:
            print(f"⚠️ Fout bij stop_processing: {e}")
        
        # Emit signal naar hoofdapplicatie EERST
        print("🛑 ProcessingPanel: Emit processing_stopped signal...")
        self.processing_stopped.emit()
        
        # Stop verwerking via StopManager met timeout
        try:
            # Import stop_manager voor verwerking stop
            try:
                from core.stop_manager import stop_manager
            except ImportError:
                stop_manager = None
            
            if stop_manager:
                print("🛑 ProcessingPanel: Roep stop_manager.stop_all_processes() aan...")
                
                # Start stop process in aparte thread om UI niet te blokkeren
                import threading
                def stop_processes():
                    try:
                        stop_manager.stop_all_processes()
                        print("✅ ProcessingPanel: StopManager stop_all_processes() voltooid")
                    except Exception as e:
                        print(f"⚠️ ProcessingPanel: Fout bij aanroepen StopManager: {e}")
                
                stop_thread = threading.Thread(target=stop_processes, daemon=True)
                stop_thread.start()
                
                # Wacht maximaal 2 seconden voor stop process
                stop_thread.join(timeout=2.0)
                
                if stop_thread.is_alive():
                    print("⚠️ ProcessingPanel: Stop process duurde langer dan 2 seconden, forceer stop...")
                    # Forceer stop als laatste redmiddel
                    try:
                        stop_manager.force_kill_processes()
                    except Exception as e:
                        print(f"⚠️ ProcessingPanel: Fout bij forceer stop: {e}")
            
        except Exception as e:
            print(f"⚠️ ProcessingPanel: Fout bij aanroepen StopManager: {e}")
        
        print("✅ ProcessingPanel: Stop signal verzonden")
        
        # Reset UI state
        try:
            if hasattr(self, 'progress_bar'):
                self.progress_bar.setValue(0)
            if hasattr(self, 'status_label'):
                self.status_label.setText("Klaar voor verwerking")
            
            # Reset console progress
            if hasattr(self, 'console_progress_label'):
                self.console_progress_label.setText("Console Progress: 0%")
        except Exception as e:
            print(f"⚠️ Fout bij resetten UI state: {e}")
        
        # Forceer stop van alle subprocessen als laatste redmiddel
        try:
            import psutil
            current_process = psutil.Process()
            children = current_process.children(recursive=True)
            for child in children:
                try:
                    cmdline = " ".join(child.cmdline()).lower()
                    if any(keyword in cmdline for keyword in ["ffmpeg", "whisper", "python", "faster-whisper"]):
                        print(f"💀 ProcessingPanel: Forceer stop van subproces: {child.pid} - {cmdline[:50]}")
                        child.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        except Exception as e:
            print(f"⚠️ ProcessingPanel: Fout bij forceer stop van subprocessen: {e}")
    
    def clear_console_output(self):
        """Wis console output"""
        try:
            if hasattr(self, 'console_output'):
                self.console_output.clear()
            if hasattr(self, 'console_progress_label'):
                self.console_progress_label.setText("Console Progress: 0%")
        except Exception as e:
            print(f"⚠️ Fout bij clear_console_output: {e}")
    
    def add_console_output(self, message: str, progress: float = None):
        """Voeg console output toe"""
        try:
            if hasattr(self, 'console_output'):
                # Voeg timestamp toe
                timestamp = datetime.now().strftime("%H:%M:%S")
                formatted_message = f"[{timestamp}] {message}"
                
                # Voeg message toe aan console output
                self.console_output.append(formatted_message)
                
                # Scroll naar beneden om nieuwste output te tonen
                if hasattr(self.console_output, 'verticalScrollBar'):
                    scrollbar = self.console_output.verticalScrollBar()
                    if scrollbar:
                        scrollbar.setValue(scrollbar.maximum())
                
                # Update progress als gegeven
                if progress is not None and hasattr(self, 'console_progress_label'):
                    progress_percent = int(progress * 100)
                    self.console_progress_label.setText(f"Console Progress: {progress_percent}%")
                    
                    # Update ook de hoofdprogress bar als het een whisper progress is
                    if "🎤" in message and "%" in message:
                        try:
                            # Parse percentage uit bericht (bijv. "🎤 Faster Whisper: 45.5% - filename")
                            percent_start = message.find(":") + 1
                            percent_end = message.find("%")
                            if percent_start > 0 and percent_end > percent_start:
                                percent_str = message[percent_start:percent_end].strip()
                                percent = float(percent_str)
                                # Whisper transcriptie is ongeveer 15% van de totale verwerking (50% tot 65%)
                                whisper_progress = 50.0 + (percent * 0.15)
                                if hasattr(self, 'progress_bar'):
                                    self.progress_bar.setValue(int(whisper_progress))
                        except:
                            pass
                
                # Beperk console output tot laatste 1000 regels
                max_lines = 1000
                lines = self.console_output.toPlainText().split('\n')
                if len(lines) > max_lines:
                    # Behoud alleen laatste regels
                    lines = lines[-max_lines:]
                    self.console_output.setPlainText('\n'.join(lines))
                    
        except Exception as e:
            print(f"⚠️ Fout bij add_console_output: {e}")
    
    def update_console_progress(self, progress: float):
        """Update console progress indicator"""
        try:
            if hasattr(self, 'console_progress_label'):
                progress_percent = int(progress * 100)
                self.console_progress_label.setText(f"Console Progress: {progress_percent}%")
        except Exception as e:
            print(f"⚠️ Fout bij update_console_progress: {e}")
    
    def update_progress(self, value: float, status: str = ""):
        """Update voortgangsbalk en status"""
        try:
            if hasattr(self, 'progress_bar'):
                # Update progress bar (value moet tussen 0 en 100 zijn)
                progress_value = max(0, min(100, int(value)))
                self.progress_bar.setValue(progress_value)
            
            if status and hasattr(self, 'status_label'):
                # Update status label
                self.status_label.setText(status)
            
            # Voeg ook toe aan console output voor real-time updates
            if status:
                self.add_console_output(status, value / 100.0 if value > 0 else None)
        except Exception as e:
            print(f"⚠️ Fout bij update_progress: {e}")
    
    def processing_finished(self):
        """Verwerking voltooid - reset UI state"""
        print("✅ ProcessingPanel: processing_finished aangeroepen")
        
        try:
            # Reset UI state
            self.is_processing = False
            
            if hasattr(self, 'progress_bar'):
                self.progress_bar.setValue(0)
            
            if hasattr(self, 'status_label'):
                self.status_label.setText("Klaar voor verwerking")
            
            # Reset knoppen
            if hasattr(self, 'start_btn'):
                self.start_btn.setEnabled(True)
            if hasattr(self, 'stop_btn'):
                self.stop_btn.setEnabled(False)
            
            # Reset console progress
            if hasattr(self, 'console_progress_label'):
                self.console_progress_label.setText("Console Progress: 0%")
            
            print("✅ ProcessingPanel: UI state gereset")
        except Exception as e:
            print(f"⚠️ Fout bij processing_finished: {e}")
    
    def clear_completed_list(self):
        """Wis voltooide bestanden lijst"""
        try:
            if hasattr(self, 'completed_list'):
                self.completed_list.clear()
                print("🗑️ Voltooide bestanden lijst gewist")
        except Exception as e:
            print(f"⚠️ Fout bij clear_completed_list: {e}")
    
    def add_completed_file(self, file_path: str, output_path: str = None):
        """Voeg voltooid bestand toe aan de lijst"""
        try:
            if hasattr(self, 'completed_list'):
                # Maak een mooie display naam
                from datetime import datetime
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
                
                # Maak list item
                from PyQt6.QtWidgets import QListWidgetItem
                item = QListWidgetItem(f"✅ {display_name}")
                self.completed_list.addItem(item)
                
                # Scroll naar beneden om nieuwste item te tonen
                if hasattr(self.completed_list, 'scrollToBottom'):
                    self.completed_list.scrollToBottom()
                
                print(f"✅ Voltooid bestand toegevoegd: {display_name}")
        except Exception as e:
            print(f"⚠️ Fout bij add_completed_file: {e}")
    
    def get_completed_files(self) -> List[str]:
        """Krijg lijst van voltooide bestanden"""
        try:
            completed_files = []
            if hasattr(self, 'completed_list'):
                for i in range(self.completed_list.count()):
                    item = self.completed_list.item(i)
                    if item:
                        completed_files.append(item.text())
            return completed_files
        except Exception as e:
            print(f"⚠️ Fout bij get_completed_files: {e}")
            return [] 