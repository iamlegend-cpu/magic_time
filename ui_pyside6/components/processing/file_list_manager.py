"""
File List Manager component voor Magic Time Studio
Bevat alle file list beheer logica
"""

import os
from PySide6.QtCore import QObject

class FileListManager(QObject):
    """Beheert alle file list operaties"""
    
    def __init__(self, ui_component, file_manager):
        super().__init__()
        self.ui = ui_component
        self.file_manager = file_manager
    
    def find_file_path_in_list(self, filename: str) -> str:
        """Zoek naar volledig bestandspad in files lijst"""
        try:
            # Zoek naar main window en files panel
            parent = self.ui.parent()
            while parent:
                if hasattr(parent, 'files_panel'):
                    files_panel = parent.files_panel
                    if hasattr(files_panel, 'get_file_list'):
                        files = files_panel.get_file_list()
                        # Zoek naar bestand met dezelfde naam
                        for file_path in files:
                            if os.path.basename(file_path) == filename:
                                print(f"🔧 [DEBUG] Bestandspad gevonden: {file_path}")
                                return file_path
                        
                        print(f"⚠️ [DEBUG] Bestand niet gevonden in files lijst: {filename}")
                        return None
                    else:
                        print(f"⚠️ [DEBUG] Files panel heeft geen get_file_list methode")
                        return None
                parent = parent.parent()
            
            print(f"⚠️ [DEBUG] Kan files panel niet vinden voor zoeken bestand")
            return None
                
        except Exception as e:
            print(f"⚠️ [WAARSCHUWING] Fout bij zoeken bestandspad: {e}")
            return None
    
    def remove_completed_file_from_list(self, filename: str):
        """Verwijder een voltooid bestand uit de files lijst"""
        try:
            print(f"🔍 Zoek bestand in files lijst: {filename}")
            
            # Zoek naar main window en files panel
            parent = self.ui.parent()
            while parent:
                if hasattr(parent, 'files_panel'):
                    files_panel = parent.files_panel
                    
                    if hasattr(files_panel, 'remove_file'):
                        # Controleer eerst of er überhaupt bestanden in de lijst staan
                        if hasattr(files_panel, 'get_file_list'):
                            current_files = files_panel.get_file_list()
                            print(f"📁 {len(current_files)} bestanden gevonden in files panel")
                            
                            # Als er geen bestanden zijn, is er niets om te verwijderen
                            if len(current_files) == 0:
                                print(f"ℹ️ Files panel is leeg, geen bestanden om te verwijderen")
                                return True  # Geen fout, gewoon lege lijst
                            
                            # Debug: toon alle bestanden voor vergelijking
                            print("🔍 Huidige bestanden in files panel:")
                            for i, file_path in enumerate(current_files):
                                file_basename = os.path.basename(file_path)
                                print(f"  {i+1}: {file_basename}")
                            
                            # Zoek naar bestand met dezelfde naam
                            for file_path in current_files:
                                file_basename = os.path.basename(file_path)
                                if file_basename == filename:
                                    print(f"✅ Exacte match gevonden: {file_path}")
                                    files_panel.remove_file(file_path)
                                    print(f"🗑️ Bestand verwijderd uit files lijst: {filename}")
                                    return True
                            
                            # Als geen exacte match, probeer bestandsnaam zonder extensie
                            filename_no_ext = os.path.splitext(filename)[0]
                            for file_path in current_files:
                                file_basename = os.path.basename(file_path)
                                file_basename_no_ext = os.path.splitext(file_basename)[0]
                                if file_basename_no_ext == filename_no_ext:
                                    print(f"✅ Match zonder extensie gevonden: {file_path}")
                                    files_panel.remove_file(file_path)
                                    print(f"🗑️ Bestand verwijderd uit files lijst: {filename}")
                                    return True
                            
                            # Als nog steeds geen match, probeer case-insensitive
                            for file_path in current_files:
                                file_basename = os.path.basename(file_path)
                                if file_basename.lower() == filename.lower():
                                    print(f"✅ Case-insensitive match gevonden: {file_path}")
                                    files_panel.remove_file(file_path)
                                    print(f"🗑️ Bestand verwijderd uit files lijst: {filename}")
                                    return True
                            
                            # Als nog steeds geen match, probeer gedeeltelijke match
                            for file_path in current_files:
                                file_basename = os.path.basename(file_path)
                                # Controleer of de bestandsnaam de zoekterm bevat
                                if filename.lower() in file_basename.lower() or file_basename.lower() in filename.lower():
                                    print(f"✅ Gedeeltelijke match gevonden: {file_path}")
                                    files_panel.remove_file(file_path)
                                    print(f"🗑️ Bestand verwijderd uit files lijst: {filename}")
                                    return True
                            
                            # Als nog steeds geen match, probeer bestandsnaam zonder seizoen/episode info
                            # Bijvoorbeeld: "Foundation.2021.S01E01.The.Emperors.Peace.mp4" -> "Foundation.mp4"
                            for file_path in current_files:
                                file_basename = os.path.basename(file_path)
                                # Verwijder seizoen/episode info voor vergelijking
                                clean_filename = self._clean_filename_for_comparison(filename)
                                clean_file_basename = self._clean_filename_for_comparison(file_basename)
                                
                                if clean_filename == clean_file_basename:
                                    print(f"✅ Clean match gevonden: {file_path}")
                                    files_panel.remove_file(file_path)
                                    print(f"🗑️ Bestand verwijderd uit files lijst: {filename}")
                                    return True
                            
                            print(f"❌ Bestand niet gevonden in files lijst: {filename}")
                            return False
                        else:
                            print(f"⚠️ Files panel heeft geen get_file_list methode")
                            return False
                    else:
                        print(f"⚠️ Files panel heeft geen remove_file methode")
                        return False
                parent = parent.parent()
            
            print(f"❌ Kan files panel niet vinden voor verwijderen bestand")
            return False
                
        except Exception as e:
            print(f"⚠️ Fout bij verwijderen bestand uit files lijst: {e}")
            return False
    
    def _clean_filename_for_comparison(self, filename: str) -> str:
        """Maak bestandsnaam schoon voor vergelijking door seizoen/episode info te verwijderen"""
        try:
            # Verwijder extensie
            name_without_ext = os.path.splitext(filename)[0]
            
            # Verwijder seizoen/episode patronen (S01E01, S1E1, etc.)
            import re
            # Patronen: S01E01, S1E1, Season 1 Episode 1, etc.
            patterns = [
                r'S\d{1,2}E\d{1,2}',  # S01E01, S1E1
                r'Season\s+\d+\s+Episode\s+\d+',  # Season 1 Episode 1
                r'\d{4}',  # Jaar (2021)
            ]
            
            clean_name = name_without_ext
            for pattern in patterns:
                clean_name = re.sub(pattern, '', clean_name, flags=re.IGNORECASE)
            
            # Verwijder dubbele spaties en trim
            clean_name = ' '.join(clean_name.split())
            
            # Verwijder lege delen
            clean_name = clean_name.strip(' .-_')
            
            print(f"🔧 Clean filename: '{filename}' -> '{clean_name}'")
            return clean_name
            
        except Exception as e:
            print(f"⚠️ Fout bij cleanen bestandsnaam: {e}")
            return filename
    
    def add_completed_file(self, file_path: str, output_path: str = None):
        """Voeg een voltooid bestand toe aan de lijst"""
        try:
            from datetime import datetime
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            # Gebruik output_path als deze beschikbaar is, anders file_path
            filename = output_path if output_path else file_path
            
            # Gebruik alleen de bestandsnaam, niet het volledige pad
            basename = os.path.basename(filename) if os.path.sep in filename else filename
            formatted_message = f"[{timestamp}] ✅ {basename}"
            
            print(f"🔍 Voeg voltooid bestand toe: {basename}")
            
            # Voeg toe aan QTextEdit
            current_text = self.ui.completed_list.toPlainText()
            if current_text:
                new_text = current_text + "\n" + formatted_message
            else:
                new_text = formatted_message
            
            self.ui.completed_list.setPlainText(new_text)
            
            # Auto-scroll naar beneden
            scrollbar = self.ui.completed_list.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
            
            # Voeg ook toe aan file manager
            self.file_manager.add_completed_file(filename)
            
            # Verwijder bestand uit files lijst
            print(f"🔍 Probeer bestand te verwijderen uit files lijst: {basename}")
            removal_success = self.remove_completed_file_from_list(basename)
            
            if removal_success:
                print(f"✅ Bestand succesvol verplaatst: {basename}")
            else:
                print(f"⚠️ Kon bestand niet verwijderen uit files lijst: {basename}")
                # Probeer alternatieve methode via main window
                self._try_remove_via_main_window(basename)
            
            print(f"🔍 Voltooid bestand toegevoegd aan completed list: {basename}")
            
        except Exception as e:
            print(f"⚠️ Fout bij toevoegen voltooid bestand: {e}")
    
    def _try_remove_via_main_window(self, filename: str):
        """Probeer bestand te verwijderen via main window als fallback"""
        try:
            print(f"🔍 Probeer alternatieve verwijdering via main window: {filename}")
            
            # Zoek naar main window
            parent = self.ui.parent()
            while parent:
                if hasattr(parent, 'files_panel'):
                    files_panel = parent.files_panel
                    
                    # Controleer of het bestand nog steeds in de lijst staat
                    if hasattr(files_panel, 'get_file_list'):
                        current_files = files_panel.get_file_list()
                        print(f"📁 Huidige bestanden in files panel: {len(current_files)}")
                        
                        # Debug: toon alle bestanden
                        print("🔍 Huidige bestanden in files panel:")
                        for i, file_path in enumerate(current_files):
                            file_basename = os.path.basename(file_path)
                            print(f"  {i+1}: {file_basename}")
                        
                        # Zoek naar bestand
                        for file_path in current_files:
                            file_basename = os.path.basename(file_path)
                            if file_basename == filename:
                                print(f"✅ Bestand gevonden in files panel: {file_path}")
                                if hasattr(files_panel, 'remove_file'):
                                    files_panel.remove_file(file_path)
                                    print(f"🗑️ Bestand verwijderd via main window: {filename}")
                                    return True
                                else:
                                    print(f"⚠️ Files panel heeft geen remove_file methode")
                                    return False
                        
                        print(f"❌ Bestand niet meer gevonden in files panel: {filename}")
                        return False
                    else:
                        print(f"⚠️ Files panel heeft geen get_file_list methode")
                        return False
                parent = parent.parent()
            
            print(f"❌ Kan main window niet vinden")
            return False
            
        except Exception as e:
            print(f"⚠️ Fout bij alternatieve verwijdering: {e}")
            return False
    
    def clear_completed_files(self):
        """Wis de voltooide bestanden lijst"""
        try:
            self.ui.completed_list.clear()
        except Exception:
            pass
    
    def get_completed_files(self):
        """Haal de lijst met voltooide bestanden op"""
        return self.file_manager.get_completed_files()
