"""
Progress Handler component voor Magic Time Studio
Bevat alle progress en status update logica
"""

from PySide6.QtCore import QObject
import os

class ProgressHandler(QObject):
    """Handelt alle progress en status updates af"""
    
    def __init__(self, ui_component, progress_tracker):
        super().__init__()
        self.ui = ui_component
        self.progress_tracker = progress_tracker
        self.current_file_index = 0
        self.total_files = 0
        self.processing_files = []  # Lijst van bestanden die worden verwerkt
    
    def handle_progress_update(self, progress: float, message: str):
        """Handle progress updates van de processing thread"""
        try:
            # Update progress bar voor huidige bestand (0-100% per bestand)
            if self.progress_tracker:
                self.progress_tracker.update_file_progress(progress)
            
            # Update status label
            if message:
                self.ui.status_label.setText(f"🔄 {message}")
            
            # Controleer of een bestand is voltooid
            if self._is_file_completed_message(message):
                print(f"🔍 Voltooid bestand gedetecteerd in message: {message}")
                
                # Haal bestandsnaam op
                filename = self._extract_filename_from_message(message)
                if filename:
                    print(f"✅ Bestandsnaam geëxtraheerd: '{filename}'")
                    
                    # Markeer bestand als voltooid in progress tracker
                    if self.progress_tracker:
                        self.progress_tracker.complete_file(filename)
                    
                    # Emit signal voor completed file
                    if hasattr(self, 'file_completed_signal'):
                        self.file_completed_signal.emit(filename, filename)  # file_path, output_path
                        print(f"📤 File completed signal geëmit voor: {filename}")
                    
                    # Ga naar volgend bestand
                    self._move_to_next_file()
                else:
                    print(f"⚠️ Kon bestandsnaam niet extraheren uit message: {message}")
            
            # Controleer of alle bestanden zijn voltooid (100% progress)
            if progress >= 100.0:
                print(f"🎉 100% progress bereikt, start cleanup")
                # Direct cleanup aanroepen in plaats van signal
                if hasattr(self, 'cleanup_callback'):
                    self.cleanup_callback()
                else:
                    print(f"⚠️ Geen cleanup_callback gevonden")
                
        except Exception as e:
            print(f"⚠️ Fout in progress update handler: {e}")
    
    def _is_file_completed_message(self, message: str) -> bool:
        """Controleer of een message aangeeft dat een bestand is voltooid"""
        message_lower = message.lower()
        
        # Controleer op voltooiing indicatoren
        completion_indicators = [
            "voltooid",
            "klaar", 
            "afgerond",
            "gereed",
            "completed",
            "finished",
            "done",
            "succesvol",
            "klaar met",
            "verwerkt",
            "bestand"
        ]
        
        # Controleer op bestandsextensies
        file_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wav', '.mp3', '.m4a', '.flac', '.srt']
        
        # Controleer of message een voltooiing indicator bevat EN een bestandsextensie
        has_completion = any(indicator in message_lower for indicator in completion_indicators)
        has_extension = any(ext in message_lower for ext in file_extensions)
        
        # Speciale controle voor berichten met "Bestand X/Y voltooid:"
        has_file_completion_format = "bestand" in message_lower and "voltooid" in message_lower and ":" in message
        
        # Voorkom dubbele verwerking van dezelfde message
        if hasattr(self, '_last_processed_message') and self._last_processed_message == message:
            return False
        
        result = (has_completion and has_extension) or has_file_completion_format
        
        if result:
            self._last_processed_message = message
        
        return result
    
    def _extract_filename_from_message(self, message: str) -> str:
        """Haal bestandsnaam op uit een voltooiing message"""
        try:
            # Eerst proberen om bestandsnaam uit message te halen met ':'
            if ":" in message:
                parts = message.split(":")
                if len(parts) >= 2:
                    potential_filename = parts[-1].strip()
                    # Verwijder eventuele extra tekst
                    if "(" in potential_filename:
                        potential_filename = potential_filename.split("(")[0].strip()
                    if ")" in potential_filename:
                        potential_filename = potential_filename.split(")")[0].strip()
                    
                    # Controleer of dit een geldige bestandsnaam is
                    if potential_filename and len(potential_filename) > 0 and "." in potential_filename:
                        print(f"🔍 Bestandsnaam gevonden via ':' methode: '{potential_filename}'")
                        return potential_filename
            
            # Als geen ':' methode werkt, zoek naar bestandsextensies
            file_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wav', '.mp3', '.m4a', '.flac', '.srt']
            
            for ext in file_extensions:
                if ext in message.lower():
                    # Zoek naar bestandsnaam rond de extensie
                    ext_pos = message.lower().find(ext)
                    if ext_pos > 0:
                        # Zoek naar begin van bestandsnaam (na spatie, punt, of pad separator)
                        start_pos = ext_pos
                        while start_pos > 0 and message[start_pos-1] not in [' ', '.', '/', '\\', ':', '(', ')']:
                            start_pos -= 1
                        
                        # Als start_pos nog steeds op een punt staat, ga verder naar links
                        while start_pos > 0 and message[start_pos-1] == '.':
                            start_pos -= 1
                            # Ga verder naar links tot je een spatie of separator tegenkomt
                            while start_pos > 0 and message[start_pos-1] not in [' ', '/', '\\', ':', '(', ')']:
                                start_pos -= 1
                        
                        filename = message[start_pos:ext_pos + len(ext)]
                        if filename and "." in filename and len(filename) > 3:
                            # Verwijder eventuele extra tekst na de extensie
                            if "(" in filename:
                                filename = filename.split("(")[0].strip()
                            if ")" in filename:
                                filename = filename.split(")")[0].strip()
                            
                            print(f"🔍 Bestandsnaam gevonden via extensie methode: '{filename}'")
                            return filename.strip()
            
            print(f"⚠️ Kon geen bestandsnaam extraheren uit message: {message}")
            return None
            
        except Exception as e:
            print(f"⚠️ Fout bij extraheren bestandsnaam: {e}")
            return None
    
    def _move_to_next_file(self):
        """Ga naar het volgende bestand"""
        try:
            if self.progress_tracker:
                self.progress_tracker.reset_for_next_file()
                
                # Reset progress bar naar 0% voor nieuw bestand
                if hasattr(self.ui, 'progress_bar') and self.ui.progress_bar:
                    self.ui.progress_bar.setValue(0)
                    print(f"🔄 Progress bar gereset naar 0% voor nieuw bestand")
                
                # Update status label
                if hasattr(self.ui, 'status_label') and self.ui.status_label:
                    if hasattr(self.progress_tracker, 'total_files') and hasattr(self.progress_tracker, 'current_file_index'):
                        current_file = self.progress_tracker.current_file_index + 1
                        total_files = self.progress_tracker.total_files
                        self.ui.status_label.setText(f"🔄 Bestand {current_file}/{total_files} wordt verwerkt...")
                    else:
                        self.ui.status_label.setText("🔄 Volgend bestand wordt verwerkt...")
                        
        except Exception as e:
            print(f"⚠️ Fout bij naar volgend bestand gaan: {e}")
    
    def set_processing_files(self, files: list):
        """Stel de lijst van te verwerken bestanden in"""
        self.processing_files = files
        self.total_files = len(files)
        self.current_file_index = 0
        print(f"🔧 [DEBUG] ProgressHandler: {self.total_files} bestanden ingesteld voor verwerking")
    
    def handle_status_update(self, status: str):
        """Handle status updates van de processing thread"""
        try:
            print(f"🔧 [DEBUG] Status update: {status}")
            
            # Update status label
            if status:
                self.ui.status_label.setText(f"ℹ️ {status}")
                
        except Exception as e:
            print(f"⚠️ [DEBUG] Fout in status update handler: {e}")
    
    def update_progress_display(self, is_processing: bool):
        """Update de progress display real-time"""
        try:
            if self.progress_tracker and is_processing:
                # Gebruik ETA voor huidige bestand en resterende bestanden
                current_file_eta = self.progress_tracker.get_eta_for_current_file()
                remaining_files_eta = self.progress_tracker.get_eta_for_remaining_files()
                elapsed_str = self.progress_tracker.get_elapsed_time()
                
                # Update timing label
                if current_file_eta and current_file_eta != "--:--":
                    if remaining_files_eta and remaining_files_eta != "--:--":
                        self.ui.timing_label.setText(f"⏱️ Huidig: {current_file_eta} | Totaal: {remaining_files_eta} | Verstreken: {elapsed_str}")
                    else:
                        self.ui.timing_label.setText(f"⏱️ Huidig: {current_file_eta} | Verstreken: {elapsed_str}")
                else:
                    self.ui.timing_label.setText(f"⏱️ ETA: --:-- | Verstreken: {elapsed_str}")
                
        except Exception as e:
            print(f"⚠️ [DEBUG] Fout in progress display update: {e}")
            self.ui.timing_label.setText("⏱️ ETA: --:-- | Verstreken: --:--")
    
    def set_signals(self, file_completed_signal, cleanup_callback):
        """Stel de benodigde signals in"""
        self.file_completed_signal = file_completed_signal
        self.cleanup_callback = cleanup_callback
