"""
Files Panel component voor Magic Time Studio
Handelt bestanden beheer af
"""

import os
from typing import List
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QListWidget, 
    QGroupBox, QTabWidget, QMessageBox, QFileDialog, QListWidgetItem, QLabel,
    QFormLayout, QSizePolicy
)
from PySide6.QtCore import Qt, Signal

class FilesPanel(QWidget):
    """Bestanden paneel met info tab voor status en model informatie"""
    
    file_selected = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_list = []
        self.processing_active = False  # Flag voor verwerking status
        self.setup_ui()
    
    def setup_ui(self):
        """Setup de UI"""
        layout = QVBoxLayout(self)
        
        files_group = QGroupBox("📁 Bestanden")
        files_layout = QVBoxLayout(files_group)
        
        # Tab widget voor bestanden en preview
        self.files_tab_widget = QTabWidget()
        
        # Tab 1: Bestandenlijst
        files_tab = QWidget()
        files_tab_layout = QVBoxLayout(files_tab)
        
        # Grote knop bovenaan is verwijderd - gebruik knoppen onderaan
        
        # Bestanden lijst
        self.file_list_widget = QListWidget()
        self.file_list_widget.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.file_list_widget.itemSelectionChanged.connect(self.on_selection_changed)
        files_tab_layout.addWidget(self.file_list_widget)
        
        # Knoppen layout - 2x2 grid
        buttons_layout = QGridLayout()
        
        # Voeg bestand knop (linksboven)
        self.add_file_btn = QPushButton("📁 Bestand")
        self.add_file_btn.setMinimumWidth(120)  # Minimum breedte voor tekst
        self.add_file_btn.setMinimumHeight(35)  # Iets hoger voor betere leesbaarheid
        self.add_file_btn.clicked.connect(self.add_file)
        buttons_layout.addWidget(self.add_file_btn, 0, 0)
        
        # Verwijder knop (rechtsboven)
        self.remove_btn = QPushButton("🗑️ Verwijder")
        self.remove_btn.setMinimumWidth(120)  # Minimum breedte voor tekst
        self.remove_btn.setMinimumHeight(35)  # Iets hoger voor betere leesbaarheid
        self.remove_btn.clicked.connect(self.remove_selected)
        self.remove_btn.setEnabled(False)  # Standaard uitgeschakeld
        buttons_layout.addWidget(self.remove_btn, 0, 1)
        
        # Voeg map knop (linksonder)
        self.add_folder_btn = QPushButton("📂 Map")
        self.add_folder_btn.setMinimumWidth(120)  # Minimum breedte voor tekst
        self.add_folder_btn.setMinimumHeight(35)  # Iets hoger voor betere leesbaarheid
        self.add_folder_btn.clicked.connect(self.add_folder)
        buttons_layout.addWidget(self.add_folder_btn, 1, 0)
        
        # Wis lijst knop (rechtsonder)
        self.clear_btn = QPushButton("🗑️ Wis lijst")
        self.clear_btn.setMinimumWidth(120)  # Minimum breedte voor tekst
        self.clear_btn.setMinimumHeight(35)  # Iets hoger voor betere leesbaarheid
        self.clear_btn.clicked.connect(self.clear_list)
        self.clear_btn.setEnabled(False)  # Standaard uitgeschakeld
        buttons_layout.addWidget(self.clear_btn, 1, 1)
        
        files_tab_layout.addLayout(buttons_layout)
        
        # Tab 2: Info (Status & Model)
        info_tab = QWidget()
        info_layout = QVBoxLayout(info_tab)
        
        # Status informatie
        status_group = QGroupBox("📊 Status")
        status_layout = QFormLayout(status_group)
        
        self.processing_status_label = QLabel("Inactief")
        self.processing_status_label.setStyleSheet("color: #28a745; font-weight: bold;")
        status_layout.addRow("Verwerking:", self.processing_status_label)
        
        self.files_count_label = QLabel("0 bestanden")
        status_layout.addRow("Bestanden:", self.files_count_label)
        
        self.current_file_label = QLabel("Geen bestand geselecteerd")
        self.current_file_label.setStyleSheet("color: #888888;")
        status_layout.addRow("Huidig:", self.current_file_label)
        
        status_group.setLayout(status_layout)
        info_layout.addWidget(status_group)
        
        # Model informatie
        model_group = QGroupBox("🎤 Model Info")
        model_layout = QFormLayout(model_group)
        
        self.whisper_type_label = QLabel("Niet geladen")
        self.whisper_type_label.setStyleSheet("color: #888888;")
        model_layout.addRow("Whisper Type:", self.whisper_type_label)
        
        self.model_name_label = QLabel("Niet geladen")
        self.model_name_label.setStyleSheet("color: #888888;")
        model_layout.addRow("Model:", self.model_name_label)
        
        self.language_label = QLabel("Engels")
        model_layout.addRow("Taal:", self.language_label)
        
        self.translator_label = QLabel("Geen vertaling")
        model_layout.addRow("Vertaler:", self.translator_label)
        
        model_group.setLayout(model_layout)
        info_layout.addWidget(model_group)
        
        # Systeem informatie
        system_group = QGroupBox("💻 Systeem")
        system_layout = QFormLayout(system_group)
        
        self.gpu_status_label = QLabel("Niet gedetecteerd")
        self.gpu_status_label.setStyleSheet("color: #888888;")
        system_layout.addRow("GPU:", self.gpu_status_label)
        
        self.vad_status_label = QLabel("Uitgeschakeld")
        self.vad_status_label.setStyleSheet("color: #888888;")
        system_layout.addRow("VAD:", self.vad_status_label)
        
        system_group.setLayout(system_layout)
        info_layout.addWidget(system_group)
        
        # Voeg tabs toe aan tab widget
        self.files_tab_widget.addTab(files_tab, "📁 Bestanden")
        self.files_tab_widget.addTab(info_tab, "ℹ️ Info")
        
        files_layout.addWidget(self.files_tab_widget)
        layout.addWidget(files_group)
        
        # Update button states
        self.update_button_states()
        
        # Initialiseer info labels
        self.refresh_all_info()
    
    def on_selection_changed(self):
        """Handle bestand selectie wijziging"""
        current_row = self.file_list_widget.currentRow()
        if current_row >= 0 and current_row < len(self.file_list):
            selected_file = self.file_list[current_row]
            print(f"📁 Bestand geselecteerd: {selected_file}")
            
            # Emit signal voor hoofdapplicatie
            self.file_selected.emit(selected_file)
            
            # Update info
            self.update_info(selected_file)
        else:
            print("📁 Geen bestand geselecteerd")
            # Update info voor geen selectie
            self.update_info(None)
        
        # Update button states
        self.update_button_states()
    
    def update_info(self, file_path: str):
        """Update info van geselecteerd bestand"""
        if file_path:
            self.current_file_label.setText(os.path.basename(file_path))
            self.current_file_label.setStyleSheet("color: #007bff; font-weight: bold;")
        else:
            self.current_file_label.setText("Geen bestand geselecteerd")
            self.current_file_label.setStyleSheet("color: #888888;")
        
        # Update bestanden teller
        self.update_files_count()
    
    def add_file(self):
        """Voeg bestand toe via file dialog"""
        files, _ = QFileDialog.getOpenFileNames(
            self, "Selecteer bestanden", "",
            "Video bestanden (*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm)"
        )
        
        added_count = 0
        video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']
        
        for file_path in files:
            # Filter alleen video bestanden
            if any(file_path.lower().endswith(ext) for ext in video_extensions):
                if file_path not in self.file_list:
                    self.file_list.append(file_path)
                    self.file_list_widget.addItem(os.path.basename(file_path))
                    added_count += 1
        
        if added_count > 0:
            self.update_button_states()
            self.update_files_count()
            print(f"✅ {added_count} bestand(en) toegevoegd")
        else:
            print("⚠️ Geen video bestanden toegevoegd")
    
    def add_folder(self):
        """Voeg map toe via folder dialog"""
        folder = QFileDialog.getExistingDirectory(self, "Selecteer map")
        if folder:
            added_count = 0
            video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']
            
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    if any(file.lower().endswith(ext) for ext in video_extensions):
                        if file_path not in self.file_list:
                            self.file_list.append(file_path)
                            self.file_list_widget.addItem(os.path.basename(file_path))
                            added_count += 1
            
            if added_count > 0:
                self.update_button_states()
                self.update_files_count()
                print(f"✅ {added_count} bestand(en) uit map toegevoegd")
            else:
                print("⚠️ Geen video bestanden gevonden in map")
    
    def remove_selected(self):
        """Verwijder geselecteerd bestand"""
        current_row = self.file_list_widget.currentRow()
        if current_row >= 0 and current_row < len(self.file_list):
            # Controleer of verwerking actief is
            if hasattr(self, 'processing_active') and self.processing_active:
                # Tijdens verwerking: alleen bestanden na het eerste kunnen verwijderd worden
                if current_row == 0:
                    print("⚠️ Kan het eerste bestand niet verwijderen tijdens verwerking")
                    QMessageBox.warning(self, "Waarschuwing", "Het eerste bestand kan niet worden verwijderd tijdens verwerking!")
                    return
            else:
                # Normale modus: alle bestanden kunnen verwijderd worden
                pass
            
            # Verwijder het bestand
            removed_file = self.file_list.pop(current_row)
            self.file_list_widget.takeItem(current_row)
            
            # Update button states
            self.update_button_states()
            
            # Update bestanden teller
            self.update_files_count()
            
            print(f"🗑️ Bestand verwijderd: {os.path.basename(removed_file)}")
        else:
            QMessageBox.information(self, "Informatie", "Selecteer eerst een bestand om te verwijderen.")
    
    def clear_list(self):
        """Wis de hele lijst"""
        # Controleer of verwerking actief is
        if hasattr(self, 'processing_active') and self.processing_active:
            QMessageBox.warning(self, "Waarschuwing", "Kan lijst niet wissen tijdens verwerking!")
            return
        
        # Vraag bevestiging voordat lijst wordt gewist
        from PySide6.QtWidgets import QMessageBox
        reply = QMessageBox.question(
            self, "🗑️ Wis Lijst", 
            "Weet je zeker dat je alle bestanden uit de lijst wilt wissen?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.file_list.clear()
            self.file_list_widget.clear()
            
            # Update button states
            self.update_button_states()
            
            # Update bestanden teller
            self.update_files_count()
            
            print("🗑️ Lijst gewist")
    
    def update_button_states(self):
        """Update de button states op basis van lijst inhoud en verwerking status"""
        # Als verwerking actief is, gebruik de speciale methode
        if hasattr(self, 'processing_active') and self.processing_active:
            self.update_button_states_during_processing()
            return
        
        # Normale button states (geen verwerking)
        # Controleer of er bestanden in de lijst zijn
        has_files = len(self.file_list) > 0
        
        # Controleer of er een bestand is geselecteerd
        current_row = self.file_list_widget.currentRow()
        has_selection = current_row >= 0
        
        # Alle knoppen beschikbaar
        self.add_file_btn.setEnabled(True)
        self.add_folder_btn.setEnabled(True)
        self.file_list_widget.setEnabled(True)
        
        # Remove button: alleen enabled als er een bestand is geselecteerd (behalve eerste)
        if has_selection and current_row > 0:  # Niet het eerste bestand
            self.remove_btn.setEnabled(True)
            self.remove_btn.setToolTip("Verwijder geselecteerd bestand")
        else:
            self.remove_btn.setEnabled(False)
            if current_row == 0:
                self.remove_btn.setToolTip("Kan het eerste bestand niet verwijderen")
            else:
                self.remove_btn.setToolTip("Selecteer een bestand om te verwijderen")
        
        # Clear button: alleen enabled als er bestanden in de lijst zijn
        if has_files:
            self.clear_btn.setEnabled(True)
            self.clear_btn.setToolTip("Wis alle bestanden uit de lijst")
        else:
            self.clear_btn.setEnabled(False)
            self.clear_btn.setToolTip("Geen bestanden om te wissen")
    
    def update_remove_button_state(self):
        """Update alleen de remove button state (voor backward compatibility)"""
        self.update_button_states()
    
    def update_button_states_during_processing(self):
        """Update button states specifiek voor tijdens verwerking"""
        # Controleer of er bestanden in de lijst zijn
        has_files = len(self.file_list) > 0
        
        # Controleer of er een bestand is geselecteerd
        current_row = self.file_list_widget.currentRow()
        has_selection = current_row >= 0
        
        # Toevoegen knoppen blijven beschikbaar tijdens verwerking
        self.add_file_btn.setEnabled(True)
        self.add_folder_btn.setEnabled(True)
        self.file_list_widget.setEnabled(True)
        
        # Remove button: alleen enabled als er een bestand is geselecteerd (behalve eerste)
        if has_selection and current_row > 0:  # Niet het eerste bestand
            self.remove_btn.setEnabled(True)
            self.remove_btn.setToolTip("Verwijder geselecteerd bestand")
        else:
            self.remove_btn.setEnabled(False)
            if current_row == 0:
                self.remove_btn.setToolTip("Kan het eerste bestand niet verwijderen (wordt verwerkt)")
            else:
                self.remove_btn.setToolTip("Selecteer een bestand om te verwijderen")
        
        # Clear button: UITGESCHAKELD tijdens verwerking (omdat eerste bestand niet verwijderd mag worden)
        self.clear_btn.setEnabled(False)
        self.clear_btn.setToolTip("Kan lijst niet wissen tijdens verwerking (eerste bestand wordt verwerkt)")
    
    def remove_file(self, file_path: str):
        """Verwijder specifiek bestand uit lijst"""
        try:
            if file_path in self.file_list:
                index = self.file_list.index(file_path)
                self.file_list.pop(index)
                self.file_list_widget.takeItem(index)
                print(f"🗑️ Bestand verwijderd uit lijst: {file_path}")
                return True
            else:
                print(f"⚠️ Bestand niet gevonden in lijst: {file_path}")
                return False
        except Exception as e:
            print(f"❌ Fout bij verwijderen bestand: {e}")
            return False
    
    def on_file_selection_changed(self):
        """Bestand selectie veranderd"""
        current_row = self.file_list_widget.currentRow()
        if current_row >= 0 and current_row < len(self.file_list):
            selected_file = self.file_list[current_row]
            self.file_selected.emit(selected_file)
        
        # Update de remove button state
        self.update_remove_button_state()
    
    def get_file_list(self) -> List[str]:
        """Krijg bestandenlijst"""
        return self.file_list.copy()
    
    def update_processing_status(self, is_active: bool):
        """Update verwerking status"""
        if is_active:
            self.processing_status_label.setText("Actief")
            self.processing_status_label.setStyleSheet("color: #dc3545; font-weight: bold;")
        else:
            self.processing_status_label.setText("Inactief")
            self.processing_status_label.setStyleSheet("color: #28a745; font-weight: bold;")
    
    def update_files_count(self):
        """Update bestanden teller"""
        count = len(self.file_list)
        self.files_count_label.setText(f"{count} bestand{'en' if count != 1 else ''}")
    
    def update_whisper_info(self, whisper_type: str, model: str):
        """Update whisper type en model informatie"""
        if whisper_type:
            self.whisper_type_label.setText(whisper_type)
            self.whisper_type_label.setStyleSheet("color: #007bff; font-weight: bold;")
        if model:
            self.model_name_label.setText(model)
            self.model_name_label.setStyleSheet("color: #007bff; font-weight: bold;")
    
    def update_language_info(self, language: str):
        """Update taal informatie"""
        if language:
            self.language_label.setText(language)
    
    def update_translator_info(self, translator: str):
        """Update vertaler informatie"""
        if translator:
            self.translator_label.setText(translator)
    
    def update_gpu_status(self, has_gpu: bool):
        """Update GPU status"""
        if has_gpu:
            self.gpu_status_label.setText("Beschikbaar")
            self.gpu_status_label.setStyleSheet("color: #28a745; font-weight: bold;")
        else:
            self.gpu_status_label.setText("Niet gedetecteerd")
            self.gpu_status_label.setStyleSheet("color: #888888;")
    
    def update_vad_status(self, enabled: bool):
        """Update VAD status"""
        if enabled:
            self.vad_status_label.setText("Ingeschakeld")
            self.vad_status_label.setStyleSheet("color: #28a745; font-weight: bold;")
        else:
            self.vad_status_label.setText("Uitgeschakeld")
            self.vad_status_label.setStyleSheet("color: #888888;")
    
    def refresh_all_info(self):
        """Ververs alle info labels"""
        self.update_files_count()
        # Andere info wordt bijgewerkt door externe componenten 