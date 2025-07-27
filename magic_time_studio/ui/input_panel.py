"""
Input panel voor Magic Time Studio
Beheert bestandsinvoer en lijst management
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import List, Callable, Optional
from ..core.logging import logger
from ..core.utils import safe_basename
from .themes import theme_manager

class InputPanel:
    """Panel voor bestandsinvoer en lijst management"""
    
    def __init__(self, parent: tk.Widget):
        self.parent = parent
        self.file_list = []
        self.selected_index = -1
        
        # Callbacks
        self.on_file_added: Optional[Callable] = None
        self.on_file_removed: Optional[Callable] = None
        self.on_file_selected: Optional[Callable] = None
        
        self.create_panel()
    
    def create_panel(self):
        """Maak het input panel"""
        # Hoofdframe
        self.frame = theme_manager.create_styled_frame(
            self.parent,
            relief=tk.RAISED,
            borderwidth=2
        )
        self.frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Titel
        title_label = theme_manager.create_styled_label(
            self.frame,
            "📁 Bestanden",
            font=("Arial", 12, "bold")
        )
        title_label.pack(pady=(5, 10))
        
        # Knoppen frame
        buttons_frame = theme_manager.create_styled_frame(self.frame)
        buttons_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Bestand toevoegen knop
        self.add_file_btn = theme_manager.create_styled_button(
            buttons_frame,
            "📁 Bestand toevoegen",
            self.add_file
        )
        self.add_file_btn.pack(side=tk.LEFT, padx=2)
        
        # Map toevoegen knop
        self.add_folder_btn = theme_manager.create_styled_button(
            buttons_frame,
            "📂 Map toevoegen",
            self.add_folder
        )
        self.add_folder_btn.pack(side=tk.LEFT, padx=2)
        
        # Verwijder knop
        self.remove_btn = theme_manager.create_styled_button(
            buttons_frame,
            "🗑️ Verwijder",
            self.remove_selected
        )
        self.remove_btn.pack(side=tk.LEFT, padx=2)
        
        # Verwijder alles knop
        self.clear_btn = theme_manager.create_styled_button(
            buttons_frame,
            "🗑️ Verwijder alles",
            self.clear_list
        )
        self.clear_btn.pack(side=tk.LEFT, padx=2)
        
        # Lijst frame
        list_frame = theme_manager.create_styled_frame(self.frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bestandenlijst
        self.file_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            bg=theme_manager.colors["frame"],
            fg=theme_manager.colors["fg"],
            selectbackground=theme_manager.colors["accent"],
            selectforeground=theme_manager.colors["fg"],
            font=("Consolas", 9),
            height=15
        )
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.file_listbox.yview)
        
        # Bind events
        self.file_listbox.bind('<<ListboxSelect>>', self.on_listbox_select)
        self.file_listbox.bind('<Double-Button-1>', self.on_double_click)
        
        # Status label
        self.status_label = theme_manager.create_styled_label(
            self.frame,
            "Klaar voor bestanden",
            font=("Arial", 9)
        )
        self.status_label.pack(pady=5)
        
        logger.log_debug("📁 Input panel aangemaakt")
    
    def add_file(self):
        """Voeg een bestand toe"""
        file_path = filedialog.askopenfilename(
            title="Selecteer video bestand",
            filetypes=[
                ("Video bestanden", "*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm"),
                ("Audio bestanden", "*.mp3 *.wav *.flac *.m4a *.aac"),
                ("Alle bestanden", "*.*")
            ]
        )
        
        if file_path:
            self.add_file_path(file_path)
    
    def add_folder(self):
        """Voeg een map toe"""
        folder_path = filedialog.askdirectory(title="Selecteer map met video's")
        if folder_path:
            self.add_folder_path(folder_path)
    
    def add_file_path(self, file_path: str):
        """Voeg een bestandspad toe aan de lijst"""
        if file_path in self.file_list:
            logger.log_debug(f"⚠️ Bestand al in lijst: {safe_basename(file_path)}")
            return
        
        self.file_list.append(file_path)
        self.update_listbox()
        self.update_status()
        
        logger.log_debug(f"📁 Bestand toegevoegd: {safe_basename(file_path)}")
        
        if self.on_file_added:
            self.on_file_added(file_path)
    
    def add_folder_path(self, folder_path: str):
        """Voeg alle video bestanden uit een map toe"""
        video_extensions = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'}
        added_count = 0
        
        try:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    _, ext = os.path.splitext(filename.lower())
                    if ext in video_extensions:
                        self.add_file_path(file_path)
                        added_count += 1
            
            logger.log_debug(f"📂 {added_count} bestanden toegevoegd uit map: {folder_path}")
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij toevoegen map: {e}")
            messagebox.showerror("Fout", f"Fout bij toevoegen map: {e}")
    
    def remove_selected(self):
        """Verwijder geselecteerd bestand"""
        if self.selected_index >= 0 and self.selected_index < len(self.file_list):
            removed_file = self.file_list.pop(self.selected_index)
            self.update_listbox()
            self.update_status()
            
            logger.log_debug(f"🗑️ Bestand verwijderd: {safe_basename(removed_file)}")
            
            if self.on_file_removed:
                self.on_file_removed(removed_file)
    
    def clear_list(self):
        """Verwijder alle bestanden"""
        if not self.file_list:
            return
        
        if messagebox.askyesno("Bevestig", "Weet je zeker dat je alle bestanden wilt verwijderen?"):
            removed_files = self.file_list.copy()
            self.file_list.clear()
            self.update_listbox()
            self.update_status()
            
            logger.log_debug(f"🗑️ {len(removed_files)} bestanden verwijderd")
            
            if self.on_file_removed:
                for file_path in removed_files:
                    self.on_file_removed(file_path)
    
    def update_listbox(self):
        """Update de listbox met huidige bestanden"""
        self.file_listbox.delete(0, tk.END)
        
        for i, file_path in enumerate(self.file_list):
            filename = safe_basename(file_path)
            # Voeg bestandsgrootte toe als beschikbaar
            try:
                size = os.path.getsize(file_path)
                size_str = self.format_file_size(size)
                display_text = f"{filename} ({size_str})"
            except:
                display_text = filename
            
            self.file_listbox.insert(tk.END, display_text)
    
    def update_status(self):
        """Update status label"""
        count = len(self.file_list)
        if count == 0:
            status_text = "Geen bestanden geselecteerd"
        elif count == 1:
            status_text = "1 bestand geselecteerd"
        else:
            status_text = f"{count} bestanden geselecteerd"
        
        self.status_label.config(text=status_text)
    
    def on_listbox_select(self, event):
        """Handle listbox selectie"""
        selection = self.file_listbox.curselection()
        if selection:
            self.selected_index = selection[0]
            if self.on_file_selected and self.selected_index < len(self.file_list):
                self.on_file_selected(self.file_list[self.selected_index])
        else:
            self.selected_index = -1
    
    def on_double_click(self, event):
        """Handle double click op bestand"""
        if self.selected_index >= 0 and self.selected_index < len(self.file_list):
            file_path = self.file_list[self.selected_index]
            # Open bestand in standaard applicatie
            try:
                import subprocess
                import platform
                
                if platform.system() == "Windows":
                    os.startfile(file_path)
                elif platform.system() == "Darwin":  # macOS
                    subprocess.run(["open", file_path])
                else:  # Linux
                    subprocess.run(["xdg-open", file_path])
                    
                logger.log_debug(f"🎬 Bestand geopend: {safe_basename(file_path)}")
            except Exception as e:
                logger.log_debug(f"❌ Fout bij openen bestand: {e}")
    
    def format_file_size(self, size_bytes: int) -> str:
        """Format bestandsgrootte in leesbare vorm"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    def get_file_list(self) -> List[str]:
        """Krijg de lijst van bestanden"""
        return self.file_list.copy()
    
    def get_selected_file(self) -> Optional[str]:
        """Krijg het geselecteerde bestand"""
        if self.selected_index >= 0 and self.selected_index < len(self.file_list):
            return self.file_list[self.selected_index]
        return None
    
    def get_selected_files(self) -> List[str]:
        """Krijg lijst van geselecteerde bestanden"""
        if self.selected_index >= 0 and self.selected_index < len(self.file_list):
            return [self.file_list[self.selected_index]]
        return []
    
    def get_all_files(self) -> List[str]:
        """Krijg lijst van alle bestanden"""
        return self.file_list.copy()
    
    def set_callbacks(self, on_file_added=None, on_file_removed=None, on_file_selected=None):
        """Zet callbacks voor events"""
        self.on_file_added = on_file_added
        self.on_file_removed = on_file_removed
        self.on_file_selected = on_file_selected
    
    def clear_selection(self):
        """Wis de selectie"""
        self.file_listbox.selection_clear(0, tk.END)
        self.selected_index = -1
    
    def is_empty(self) -> bool:
        """Controleer of de lijst leeg is"""
        return len(self.file_list) == 0
    
    def get_count(self) -> int:
        """Krijg het aantal bestanden"""
        return len(self.file_list) 