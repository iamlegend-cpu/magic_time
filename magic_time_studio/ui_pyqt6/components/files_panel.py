"""
Files Panel component voor Magic Time Studio
Handelt bestanden beheer af
"""

import os
from typing import List
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QListWidget, 
    QGroupBox, QTabWidget, QMessageBox, QFileDialog, QListWidgetItem, QLabel
)
from PyQt6.QtCore import Qt, pyqtSignal

from ..features.drag_drop import DragDropZone

class FilesPanel(QWidget):
    """Bestanden paneel met preview"""
    
    files_dropped = pyqtSignal(list)
    file_selected = pyqtSignal(str)
    
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
        
        # Drag & drop zone
        self.drag_drop_zone = DragDropZone("📁 Sleep bestanden hierheen")
        self.drag_drop_zone.files_dropped.connect(self.on_files_dropped)
        files_tab_layout.addWidget(self.drag_drop_zone)
        
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
        
        # Tab 2: Preview
        preview_tab = QWidget()
        preview_layout = QVBoxLayout(preview_tab)
        
        # Preview label
        self.preview_label = QLabel("Selecteer een bestand om preview te zien")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet("""
            QLabel {
                color: #888888;
                font-size: 14px;
                padding: 20px;
            }
        """)
        preview_layout.addWidget(self.preview_label)
        
        # Voeg tabs toe aan tab widget
        self.files_tab_widget.addTab(files_tab, "📁 Bestanden")
        self.files_tab_widget.addTab(preview_tab, "👁️ Preview")
        
        files_layout.addWidget(self.files_tab_widget)
        layout.addWidget(files_group)
        
        # Update button states
        self.update_button_states()
    
    def on_files_dropped(self, files: List[str]):
        """Bestanden gedropt - automatisch laden en voorbereiden"""
        # Voorkom drag & drop tijdens verwerking
        if self.processing_active:
            print("⚠️ Kan geen bestanden toevoegen via drag & drop tijdens verwerking")
            return
        
        try:
            video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']
            added_count = 0
            
            # Voeg bestanden toe en bereid verwerking voor
            for file_path in files:
                if os.path.exists(file_path):
                    file_ext = os.path.splitext(file_path)[1].lower()
                    if file_ext in video_extensions:
                        if file_path not in self.file_list:
                            self.file_list.append(file_path)
                            added_count += 1
                            
                            # Voeg toe aan lijst widget
                            item = QListWidgetItem(os.path.basename(file_path))
                            item.setData(Qt.ItemDataRole.UserRole, file_path)
                            self.file_list_widget.addItem(item)
            
            if added_count > 0:
                # Update remove button state na toevoegen bestanden
                self.update_button_states()
                # Emit signal voor automatische verwerking voorbereiding
                self.files_dropped.emit(self.file_list)
                print(f"✅ {added_count} bestand(en) toegevoegd en klaar voor verwerking")
        except Exception as e:
            print(f"❌ Fout bij verwerken gedropte bestanden: {e}")
            # Emit een lege lijst om de applicatie niet te laten crashen
            self.files_dropped.emit([])
    
    def on_selection_changed(self):
        """Handle bestand selectie wijziging"""
        current_row = self.file_list_widget.currentRow()
        if current_row >= 0 and current_row < len(self.file_list):
            selected_file = self.file_list[current_row]
            print(f"📁 Bestand geselecteerd: {selected_file}")
            
            # Emit signal voor hoofdapplicatie
            self.file_selected.emit(selected_file)
            
            # Update preview (toekomstig)
            self.update_preview(selected_file)
        else:
            print("📁 Geen bestand geselecteerd")
        
        # Update button states
        self.update_button_states()
    
    def update_preview(self, file_path: str):
        """Update preview van geselecteerd bestand"""
        # Toekomstig: implementeer video preview
        self.preview_label.setText(f"Preview van: {os.path.basename(file_path)}")
    
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
                print(f"✅ {added_count} bestand(en) uit map toegevoegd")
            else:
                print("⚠️ Geen video bestanden gevonden in map")
    
    def remove_selected(self):
        """Verwijder geselecteerd bestand"""
        current_row = self.file_list_widget.currentRow()
        if current_row >= 0:
            # Voorkom verwijdering van het eerste bestand (index 0)
            if current_row == 0:
                print("⚠️ Kan het eerste bestand niet verwijderen")
                QMessageBox.warning(self, "Waarschuwing", "Het eerste bestand kan niet worden verwijderd!")
                return
            
            removed_file = self.file_list.pop(current_row)
            self.file_list_widget.takeItem(current_row)
            
            # Update button states op basis van verwerking status
            if hasattr(self, 'processing_active') and self.processing_active:
                self.update_button_states_during_processing()
            else:
                self.update_button_states()
            
            print(f"🗑️ Bestand verwijderd: {os.path.basename(removed_file)}")
        else:
            QMessageBox.information(self, "Informatie", "Selecteer eerst een bestand om te verwijderen.")
    
    def clear_list(self):
        """Wis de hele lijst"""
        # Vraag bevestiging voordat lijst wordt gewist
        from PyQt6.QtWidgets import QMessageBox
        reply = QMessageBox.question(
            self, "🗑️ Wis Lijst", 
            "Weet je zeker dat je alle bestanden uit de lijst wilt wissen?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.file_list.clear()
            self.file_list_widget.clear()
            
            # Update button states op basis van verwerking status
            if hasattr(self, 'processing_active') and self.processing_active:
                self.update_button_states_during_processing()
            else:
                self.update_button_states()
            
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