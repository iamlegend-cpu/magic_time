"""
File Manager voor Magic Time Studio
Handelt bestandsoperaties en -zoekacties af
"""

import os
from typing import List, Optional

class FileManager:
    """Manager voor bestandsoperaties"""
    
    def __init__(self):
        self.completed_files = []
    
    def find_main_window(self, widget) -> Optional[object]:
        """Zoek naar de main window in de parent hierarchy"""
        parent = widget.parent()
        
        while parent:
            # Probeer verschillende methoden om main window te vinden
            if hasattr(parent, 'window') and parent.window():
                return parent.window()
            elif hasattr(parent, 'main_window'):
                return parent.main_window
            elif hasattr(parent, 'parent') and callable(parent.parent):
                parent = parent.parent()
            else:
                break
        
        return None
    
    def get_files_from_main_window(self, main_window) -> List[str]:
        """Haal bestanden op van de main window"""
        files = []
        
        if hasattr(main_window, 'get_selected_files'):
            files = main_window.get_selected_files()
        elif hasattr(main_window, 'files_panel'):
            # Probeer eerst de get_file_list methode (geeft alle bestanden)
            if hasattr(main_window.files_panel, 'get_file_list'):
                files = main_window.files_panel.get_file_list()
            # Als dat niet werkt, probeer get_selected_files
            elif hasattr(main_window.files_panel, 'get_selected_files'):
                files = main_window.files_panel.get_selected_files()
            # Als laatste optie, probeer direct uit widgets te halen
            else:
                files = self._extract_files_from_widgets(main_window)
        
        return files
    
    def _extract_files_from_widgets(self, main_window) -> List[str]:
        """Probeer bestanden direct uit UI widgets te halen"""
        try:
            files = []
            
            # Zoek naar files_panel
            if hasattr(main_window, 'files_panel'):
                files_panel = main_window.files_panel
                
                # Zoek naar list widgets of andere bestand containers
                for attr_name in dir(files_panel):
                    if not attr_name.startswith('_'):
                        attr = getattr(files_panel, attr_name)
                        if hasattr(attr, 'selectedItems') and callable(attr.selectedItems):
                            # QListWidget gevonden
                            selected_items = attr.selectedItems()
                            if selected_items:
                                for item in selected_items:
                                    if hasattr(item, 'text'):
                                        file_path = item.text()
                                        if file_path and os.path.exists(file_path):
                                            files.append(file_path)
                                if files:
                                    break
                        elif hasattr(attr, 'currentText') and callable(attr.currentText):
                            # QComboBox of QLineEdit gevonden
                            current_text = attr.currentText()
                            if current_text and os.path.exists(current_text):
                                files.append(current_text)
                                break
            
            return files
            
        except Exception:
            return []
    
    def get_settings_from_main_window(self, main_window) -> dict:
        """Haal instellingen op van de main window"""
        settings = {}
        
        try:
            # Probeer verschillende methoden om settings op te halen
            if hasattr(main_window, 'get_settings'):
                settings = main_window.get_settings()
            elif hasattr(main_window, 'settings_panel'):
                if hasattr(main_window.settings_panel, 'get_current_settings'):
                    settings = main_window.settings_panel.get_current_settings()
                elif hasattr(main_window.settings_panel, 'get_settings'):
                    settings = main_window.settings_panel.get_settings()
            elif hasattr(main_window, 'get_current_settings'):
                settings = main_window.get_current_settings()
            
            # Debug output
            print(f"🔧 [DEBUG] FileManager: Settings opgehaald: {settings}")
            
        except Exception as e:
            print(f"⚠️ [WAARSCHUWING] Fout bij ophalen settings: {e}")
        
        return settings
    
    def add_completed_file(self, file_path: str, output_path: str = None):
        """Voeg een voltooid bestand toe"""
        # Gebruik output_path als deze beschikbaar is, anders file_path
        filename = output_path if output_path else file_path
        
        if filename not in self.completed_files:
            self.completed_files.append(filename)
    
    def get_completed_files(self) -> List[str]:
        """Haal de lijst met voltooide bestanden op"""
        return self.completed_files.copy()
    
    def clear_completed_files(self):
        """Wis de lijst met voltooide bestanden"""
        self.completed_files.clear()
    
    def validate_file(self, file_path: str) -> bool:
        """Valideer of een bestand bestaat en toegankelijk is"""
        return os.path.exists(file_path) and os.path.isfile(file_path)
