"""
Log Manager component voor Magic Time Studio
Bevat alle log beheer logica
"""

from datetime import datetime
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication

class LogManager(QObject):
    """Beheert alle log operaties"""
    
    def __init__(self, ui_component):
        super().__init__()
        self.ui = ui_component
    
    def log_message(self, message: str):
        """Voeg een bericht toe aan de log"""
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            formatted_message = f"[{timestamp}] {message}"
            self.ui.log_text.append(formatted_message)
            
            # Auto-scroll naar beneden
            scrollbar = self.ui.log_text.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
        except Exception:
            pass
    
    def clear_log(self):
        """Wis de log"""
        try:
            self.ui.log_text.clear()
        except Exception:
            pass
    
    def copy_log(self):
        """Kopieer de log naar klembord"""
        try:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.ui.log_text.toPlainText())
            self.log_message("📋 Log gekopieerd naar klembord")
        except Exception as e:
            self.log_message(f"❌ Fout bij kopiëren: {e}")
    
    def update_progress(self, value, step_progress=None):
        """Update de progress bar"""
        try:
            # Zorg ervoor dat value een integer is
            if isinstance(value, str):
                try:
                    value = int(value)
                except ValueError:
                    value = 0
            elif isinstance(value, (int, float)):
                value = int(value)
            else:
                value = 0
            
            # Update de hoofdprogress bar
            self.ui.progress_bar.setValue(value)
            
            # Log de progress update
            if value > 0:
                self.log_message(f"📊 Progress: {value}%")
        except Exception:
            # Stil falen bij fouten
            pass
    
    def update_status(self, status):
        """Update de status label"""
        try:
            if isinstance(status, str):
                self.ui.status_label.setText(status)
            elif status is not None:
                self.ui.status_label.setText(str(status))
        except Exception:
            pass
