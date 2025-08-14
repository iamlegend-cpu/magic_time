"""
Processing Panel component voor Magic Time Studio
Handelt verwerking en progress af
"""

import os
from datetime import datetime
from typing import List, Dict
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QProgressBar, QGroupBox, QTextEdit, QListWidget, QListWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal

class ProcessingPanel(QWidget):
    """Verwerking paneel"""
    
    processing_started = pyqtSignal(list, dict)
    file_completed = pyqtSignal(str)  # Signal om bestand uit "nog te doen" lijst te verwijderen
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_processing = False
        self.completed_files = []
        self.setup_ui()
    
    def setup_ui(self):
        """Setup de UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Verwerking groep
        processing_group = QGroupBox("⚙️ Verwerking")
        processing_layout = QVBoxLayout(processing_group)
        processing_layout.setSpacing(10)
        
        # Status label
        self.status_label = QLabel("Klaar voor verwerking")
        processing_layout.addWidget(self.status_label)
        
        # Progress bar met moderne styling
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #4a5568;
                border-radius: 8px;
                text-align: center;
                font-weight: bold;
                font-size: 12px;
                color: #ffffff;
                background: #1a202c;
                height: 25px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a90e2, stop:1 #63b3ed);
                border-radius: 6px;
                margin: 2px;
            }
        """)
        processing_layout.addWidget(self.progress_bar)
        
        # Dunne progress lijn (behouden voor subtiele voortgang)
        self.progress_line = QProgressBar()
        self.progress_line.setRange(0, 100)
        self.progress_line.setValue(0)
        self.progress_line.setStyleSheet("""
            QProgressBar {
                border: 1px solid #4a5568;
                border-radius: 4px;
                text-align: center;
                font-size: 10px;
                color: #a0aec0;
                background: #1a202c;
                height: 12px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #48bb78, stop:1 #38a169);
                border-radius: 3px;
                margin: 1px;
            }
        """)
        processing_layout.addWidget(self.progress_line)
        
        # Knoppen
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        self.start_btn = QPushButton("▶️ Start Verwerking")
        self.start_btn.setProperty("class", "primary")
        self.start_btn.clicked.connect(self.start_processing_direct)
        buttons_layout.addWidget(self.start_btn)
        
        processing_layout.addLayout(buttons_layout)
        
        # Log output
        log_label = QLabel("📋 Verwerking Log")
        processing_layout.addWidget(log_label)
        
        self.log_output = QTextEdit()
        self.log_output.setMaximumHeight(100)
        self.log_output.setReadOnly(True)
        processing_layout.addWidget(self.log_output)
        
        layout.addWidget(processing_group)
        
        # Voltooide bestanden groep
        completed_group = QGroupBox("✅ Voltooide Bestanden")
        completed_layout = QVBoxLayout(completed_group)
        completed_layout.setSpacing(10)
        
        # Voltooide bestanden lijst
        self.completed_list = QListWidget()
        self.completed_list.setMaximumHeight(150)
        completed_layout.addWidget(self.completed_list)
        
        # Wis knop
        clear_completed_btn = QPushButton("🗑️ Wis Voltooide Lijst")
        clear_completed_btn.clicked.connect(self.clear_completed_list)
        completed_layout.addWidget(clear_completed_btn)
        
        layout.addWidget(completed_group)
    
    def start_processing_direct(self):
        """Start verwerking direct met bestanden uit files panel"""
        try:
            # Zoek naar het hoofdvenster om bij de bestanden te komen
            main_window = self._find_main_window()
            if main_window and hasattr(main_window, 'files_panel'):
                files = main_window.files_panel.get_file_list()
                if not files:
                    QMessageBox.warning(self, "Waarschuwing", "Geen bestanden geselecteerd!")
                    return
                
                # Haal instellingen op uit settings panel
                if hasattr(main_window, 'settings_panel'):
                    settings = main_window.settings_panel.settings_panel.get_current_settings()
                else:
                    settings = {}
                
                print(f"🚀 ProcessingPanel.start_processing_direct: Snelle start request")
                self.start_processing_with_settings(files, settings)
            else:
                print("⚠️ Hoofdvenster of files panel niet beschikbaar")
                # Fallback naar legacy methode
                self.start_processing()
                
        except Exception as e:
            print(f"❌ Fout bij start_processing_direct: {e}")
            # Fallback naar legacy methode
            self.start_processing()
    
    def _find_main_window(self):
        """Zoek naar het hoofdvenster"""
        parent = self.parent()
        while parent:
            if hasattr(parent, 'start_processing_from_panel'):
                return parent
            parent = parent.parent()
        return None
    
    def start_processing(self):
        """Start verwerking (legacy methode)"""
        if self.is_processing:
            print("⚠️ Verwerking al bezig, negeer legacy start request")
            return
        
        print("🚀 ProcessingPanel.start_processing: Legacy start request")
        try:
            # Emit een signal om de hoofdapplicatie te laten weten dat verwerking moet starten
            # De hoofdapplicatie zal dan de bestanden ophalen en verwerking starten
            main_window = self._find_main_window()
            if main_window and hasattr(main_window, 'main_processing_started'):
                # Emit met lege bestanden en instellingen voor legacy mode
                main_window.main_processing_started.emit([], {})
                print("✅ Legacy main_processing_started signal geëmit")
            else:
                print("⚠️ main_processing_started signal niet beschikbaar")
                # Fallback naar oude methode
                self.processing_started.emit([], {})
        except Exception as e:
            print(f"⚠️ Fout bij start_processing: {e}")
            # Fallback naar oude methode
            self.processing_started.emit([], {})
    
    def start_processing_with_settings(self, files: List[str], settings: Dict):
        """Start verwerking met bestanden en instellingen"""
        try:
            if not files:
                QMessageBox.warning(self, "Waarschuwing", "Geen bestanden geselecteerd!")
                return
            
            print(f"🚀 Start verwerking met {len(files)} bestanden...")
            
            # Update UI voor start
            self.is_processing = True
            self.start_btn.setEnabled(False)
            
            # UITGESCHAKELD: Status label updates zijn overbodig
            # self.status_label.setText("Verwerking gestart...")
            
            # Emit signal naar main window via main_processing_started
            main_window = self._find_main_window()
            if main_window and hasattr(main_window, 'main_processing_started'):
                main_window.main_processing_started.emit(files, settings)
                print("✅ main_processing_started signal geëmit")
            else:
                print("⚠️ main_processing_started signal niet beschikbaar")
                # Fallback naar legacy methode
                self.start_processing()
                
        except Exception as e:
            print(f"❌ Fout bij start_processing_with_settings: {e}")
            # Reset UI bij fout
            self.is_processing = False
            self.start_btn.setEnabled(True)
    

    
    def clear_console_output(self):
        """Wis console output"""
        try:
            if hasattr(self, 'log_output'):
                self.log_output.clear()
            # if hasattr(self, 'console_progress_label'): # Removed as per edit hint
            #     self.console_progress_label.setText("Console Progress: 0%")
        except Exception as e:
            print(f"⚠️ Fout bij clear_console_output: {e}")
    
    def add_console_output(self, message: str, progress: float = None):
        """Voeg console output toe"""
        try:
            if hasattr(self, 'log_output'):
                # Voeg timestamp toe
                timestamp = datetime.now().strftime("%H:%M:%S")
                formatted_message = f"[{timestamp}] {message}"
                
                # Voeg message toe aan console output
                self.log_output.append(formatted_message)
                
                # Scroll naar beneden om nieuwste output te tonen
                if hasattr(self.log_output, 'verticalScrollBar'):
                    scrollbar = self.log_output.verticalScrollBar()
                    if scrollbar:
                        scrollbar.setValue(scrollbar.maximum())
                
                # Update progress als gegeven
                if progress is not None and hasattr(self, 'console_progress_label'):
                    # UITGESCHAKELD: Console progress updates zijn overbodig
                    # progress_percent = int(progress * 100)
                    # self.console_progress_label.setText(f"Console Progress: {progress_percent}%")
                    
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
                lines = self.log_output.toPlainText().split('\n')
                if len(lines) > max_lines:
                    # Behoud alleen laatste regels
                    lines = lines[-max_lines:]
                    self.log_output.setPlainText('\n'.join(lines))
                    
        except Exception as e:
            print(f"⚠️ Fout bij add_console_output: {e}")
    
    def update_console_progress(self, progress: float):
        """Update console progress indicator - UITGESCHAKELD"""
        # UITGESCHAKELD: Console progress updates zijn overbodig
        # try:
        #     if hasattr(self, 'console_progress_label'):
        #         progress_percent = int(progress * 100)
        #         self.console_progress_label.setText(f"Console Progress: {progress_percent}%")
        # except Exception as e:
        #     print(f"⚠️ Fout bij update_console_progress: {e}")
        pass
    
    def update_progress(self, value: float, status: str = ""):
        """Update voortgangsbalk en status"""
        try:
            if hasattr(self, 'progress_bar'):
                # Update hoofdprogress bar (value moet tussen 0 en 100 zijn)
                progress_value = max(0, min(100, int(value)))
                self.progress_bar.setValue(progress_value)
            
            if hasattr(self, 'progress_line'):
                # Update dunne progress lijn
                progress_value = max(0, min(100, int(value)))
                self.progress_line.setValue(progress_value)
            
            # UITGESCHAKELD: Status label updates zijn overbodig
            # if status and hasattr(self, 'status_label'):
            #     self.status_label.setText(status)
            
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
            if hasattr(self, 'progress_line'):
                self.progress_line.setValue(0)
            
            # UITGESCHAKELD: Status label updates zijn overbodig
            # if hasattr(self, 'status_label'):
            #     self.status_label.setText("Klaar voor verwerking")
            
            # Reset knoppen
            if hasattr(self, 'start_btn'):
                self.start_btn.setEnabled(True)
            
            # Reset console progress
            # if hasattr(self, 'console_progress_label'): # Removed as per edit hint
            #     self.console_progress_label.setText("Console Progress: 0%")
            
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