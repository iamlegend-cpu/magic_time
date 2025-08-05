"""
Files Panel component voor Magic Time Studio
Handelt bestanden beheer af
"""

import os
from typing import List
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, 
    QGroupBox, QTabWidget, QMessageBox, QFileDialog, QListWidgetItem
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
        self.file_list_widget.itemSelectionChanged.connect(self.on_file_selection_changed)
        files_tab_layout.addWidget(self.file_list_widget)
        
        # Knoppen
        buttons_layout = QHBoxLayout()
        
        self.add_file_btn = QPushButton("Bestand toevoegen")
        self.add_file_btn.setProperty("class", "primary")
        self.add_file_btn.clicked.connect(self.add_file)
        buttons_layout.addWidget(self.add_file_btn)
        
        self.add_folder_btn = QPushButton("Map toevoegen")
        self.add_folder_btn.setProperty("class", "secondary")
        self.add_folder_btn.clicked.connect(self.add_folder)
        buttons_layout.addWidget(self.add_folder_btn)
        
        files_tab_layout.addLayout(buttons_layout)
        
        # Verwijder knoppen
        remove_layout = QHBoxLayout()
        
        self.remove_btn = QPushButton("Verwijder geselecteerd")
        self.remove_btn.setProperty("class", "danger")
        self.remove_btn.clicked.connect(self.remove_selected)
        remove_layout.addWidget(self.remove_btn)
        
        self.clear_btn = QPushButton("Wis lijst")
        self.clear_btn.clicked.connect(self.clear_list)
        remove_layout.addWidget(self.clear_btn)
        
        files_tab_layout.addLayout(remove_layout)
        
        # Voeg files tab toe
        self.files_tab_widget.addTab(files_tab, "📋 Lijst")
        
        files_layout.addWidget(self.files_tab_widget)
        layout.addWidget(files_group)
    
    def on_files_dropped(self, files: List[str]):
        """Bestanden gedropt - automatisch laden en voorbereiden"""
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
                # Emit signal voor automatische verwerking voorbereiding
                self.files_dropped.emit(self.file_list)
                print(f"✅ {added_count} bestand(en) toegevoegd en klaar voor verwerking")
        except Exception as e:
            print(f"❌ Fout bij verwerken gedropte bestanden: {e}")
            # Emit een lege lijst om de applicatie niet te laten crashen
            self.files_dropped.emit([])
    
    def add_file(self):
        """Voeg bestand toe"""
        try:
            files, _ = QFileDialog.getOpenFileNames(
                self, "Selecteer bestanden", "",
                "Video bestanden (*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm);;Alle bestanden (*)"
            )
            
            video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']
            added_count = 0
            
            print(f"🔍 [DEBUG] FilesPanel.add_file: {len(files)} bestanden geselecteerd")
            
            for file_path in files:
                print(f"🔍 [DEBUG] FilesPanel.add_file: Controleer bestand: {file_path}")
                # Filter alleen video bestanden
                if any(file_path.lower().endswith(ext) for ext in video_extensions):
                    print(f"🔍 [DEBUG] FilesPanel.add_file: Video bestand gedetecteerd: {file_path}")
                    if file_path not in self.file_list:
                        self.file_list.append(file_path)
                        self.file_list_widget.addItem(os.path.basename(file_path))
                        added_count += 1
                        print(f"🔍 [DEBUG] FilesPanel.add_file: Bestand toegevoegd: {file_path}")
                    else:
                        print(f"🔍 [DEBUG] FilesPanel.add_file: Bestand al in lijst: {file_path}")
                else:
                    print(f"🔍 [DEBUG] FilesPanel.add_file: Niet-video bestand genegeerd: {file_path}")
            
            print(f"🔍 [DEBUG] FilesPanel.add_file: {added_count} bestanden toegevoegd")
            
            if added_count > 0:
                # Emit signal voor automatische verwerking voorbereiding
                self.files_dropped.emit(self.file_list)
                print(f"✅ {added_count} bestand(en) klaar voor verwerking")
            
            return added_count
        except Exception as e:
            print(f"❌ Fout bij toevoegen bestanden: {e}")
            return 0
    
    def add_folder(self):
        """Voeg map toe"""
        try:
            folder = QFileDialog.getExistingDirectory(self, "Selecteer map")
            if folder:
                video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']
                added_count = 0
                
                # Recursief door de map gaan
                for root, dirs, files in os.walk(folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Filter alleen op video bestanden
                        if any(file.lower().endswith(ext) for ext in video_extensions):
                            if file_path not in self.file_list:
                                self.file_list.append(file_path)
                                self.file_list_widget.addItem(os.path.basename(file_path))
                                added_count += 1
                
                if added_count > 0:
                    # Emit signal voor automatische verwerking voorbereiding
                    self.files_dropped.emit(self.file_list)
                    print(f"✅ {added_count} bestand(en) uit map toegevoegd en klaar voor verwerking")
                
                return added_count
            return 0
        except Exception as e:
            print(f"❌ Fout bij toevoegen map: {e}")
            return 0
    
    def remove_selected(self):
        """Verwijder geselecteerd bestand"""
        current_row = self.file_list_widget.currentRow()
        if current_row >= 0:
            self.file_list.pop(current_row)
            self.file_list_widget.takeItem(current_row)
    
    def clear_list(self):
        """Wis de lijst"""
        self.file_list.clear()
        self.file_list_widget.clear()
    
    def on_file_selection_changed(self):
        """Bestand selectie veranderd"""
        current_row = self.file_list_widget.currentRow()
        if current_row >= 0 and current_row < len(self.file_list):
            selected_file = self.file_list[current_row]
            self.file_selected.emit(selected_file)
    
    def get_file_list(self) -> List[str]:
        """Krijg bestandenlijst"""
        return self.file_list.copy() 