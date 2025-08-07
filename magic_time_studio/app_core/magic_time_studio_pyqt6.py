import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIcon
from magic_time_studio.core.config import config_manager
from magic_time_studio.core.stop_manager import stop_manager
from magic_time_studio.ui_pyqt6.main_window import MainWindow
from magic_time_studio.ui_pyqt6.themes import ThemeManager
from magic_time_studio.processing import translator, audio_processor, video_processor
from magic_time_studio.processing.whisper_manager import whisper_manager
from magic_time_studio.app_core.processing_thread import ProcessingThread
from magic_time_studio.app_core.single_instance import release_single_instance_lock

# Import whisper_manager
try:
    from magic_time_studio.processing.whisper_manager import whisper_manager
except ImportError:
    import sys
    sys.path.append('..')
    from processing.whisper_manager import whisper_manager

# Debug mode - zet op False om debug output uit te zetten
DEBUG_MODE = False

class MagicTimeStudioPyQt6:
    """Hoofdapplicatie klasse voor PyQt6"""
    
    def __init__(self):
        self.app = None
        self.main_window = None
        self.processing_thread = None
        self.theme_manager = ThemeManager()
        self.socket = None  # Socket voor single instance controle
        
        # Initialiseer modules
        self._init_modules()
    
    def _init_modules(self):
        """Initialiseer alle modules"""
        print("🚀 Magic Time Studio PyQt6 wordt geïnitialiseerd...")
        
        # Laad configuratie
        config_manager.load_configuration()
        
        # Log systeem informatie
        print("💾 RAM: 33.7% gebruikt (18.5GB vrij)")
        print("💻 CPU: 0.0% gebruikt")
        
        # Initialiseer processing modules
        self._init_processing_modules()
        
        print("✅ Modules geïnitialiseerd")
    
    def _init_processing_modules(self):
        """Initialiseer processing modules"""
        print("🔧 Processing modules initialiseren...")
        
        # Initialiseer Whisper Manager
        default_whisper_type = config_manager.get_env("WHISPER_TYPE", "fast")
        if default_whisper_type == "fast":
            default_model = config_manager.get_env("DEFAULT_FAST_WHISPER_MODEL", "large-v3-turbo")
        else:
            default_model = config_manager.get_env("DEFAULT_WHISPER_MODEL", "large")
        
        print(f"[DEBUG] Gekozen Whisper type: {default_whisper_type}, model: {default_model}")
        
        if whisper_manager.initialize(default_whisper_type, default_model):
            print(f"✅ Whisper Manager geïnitialiseerd met {default_whisper_type} model: {default_model}")
        else:
            print("⚠️ Whisper Manager initialisatie gefaald")
        
        # Controleer FFmpeg
        if audio_processor.is_ffmpeg_available():
            print("✅ FFmpeg beschikbaar")
        else:
            print("⚠️ FFmpeg niet gevonden")
        
        # Zet vertaler service
        default_translator = config_manager.get("default_translator", "libretranslate")
        translator.set_service(default_translator)
        print(f"✅ Translator geïnitialiseerd: {default_translator}")
    
    def create_ui(self):
        """Maak de PyQt6 gebruikersinterface"""
        print("🎨 PyQt6 UI wordt aangemaakt...")
        
        # Maak QApplication
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Magic Time Studio v2.0")
        self.app.setApplicationVersion("2.0")
        
        # Stel icoon in voor applicatie en taakbalk
        try:
            # Bepaal project root
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            # Probeer verschillende icoon paden
            icon_paths = [
                os.path.join(os.path.dirname(__file__), "..", "assets", "Magic_Time_Studio.ico"),
                os.path.join(os.path.dirname(__file__), "..", "assets", "Magic_Time_Studio_wit.ico"),
                os.path.join(project_root, "assets", "Magic_Time_Studio.ico"),
                os.path.join(project_root, "assets", "Magic_Time_Studio_wit.ico"),
            ]
            
            icon_set = False
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    self.app.setWindowIcon(QIcon(icon_path))
                    print(f"✅ Icoon ingesteld: {icon_path}")
                    icon_set = True
                    break
            
            if not icon_set:
                print("⚠️ Geen icoon bestand gevonden")
                
        except Exception as e:
            print(f"❌ Fout bij instellen icoon: {e}")
        
        # Pas thema toe
        theme = config_manager.get("theme", "dark")
        self.theme_manager.apply_theme(self.app, theme)
        
        # Maak hoofdvenster
        self.main_window = MainWindow()
        
        # Connect signals
        self.main_window.processing_started.connect(self._on_start_processing)
        self.main_window.processing_stopped.connect(self._on_stop_processing)
        self.main_window.file_selected.connect(self._on_file_selected)
        
        # Stel taakbalk icoon in
        self.setTaskbarIcon()
        
        print("✅ PyQt6 UI aangemaakt")
    
    def setTaskbarIcon(self):
        """Stel taakbalk icoon in"""
        try:
            # Bepaal project root
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            # Probeer verschillende icoon paden voor taakbalk
            icon_paths = [
                os.path.join(project_root, "assets", "Magic_Time_Studio_wit.ico"),
                os.path.join(project_root, "assets", "Magic_Time_Studio.ico"),
                os.path.join(os.path.dirname(__file__), "..", "assets", "Magic_Time_Studio_wit.ico"),
                os.path.join(os.path.dirname(__file__), "..", "assets", "Magic_Time_Studio.ico"),
            ]
            
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    # Stel icoon in voor de applicatie (dit beïnvloedt de taakbalk)
                    self.app.setWindowIcon(QIcon(icon_path))
                    print(f"✅ Taakbalk icoon ingesteld: {icon_path}")
                    return
            
            print("⚠️ Geen icoon bestand gevonden voor taakbalk")
            
        except Exception as e:
            print(f"❌ Fout bij instellen taakbalk icoon: {e}")
    
    def _on_file_selected(self, file_path: str):
        """Callback voor geselecteerd bestand"""
        print(f"📁 Bestand geselecteerd: {file_path}")
    
    def _on_start_processing(self, files: list, settings: dict):
        print(f"🚀 Hoofdapplicatie: _on_start_processing aangeroepen met {len(files)} bestanden")
        print(f"🔧 Instellingen: {settings}")
        
        # Check of er al een thread draait
        if self.processing_thread and self.processing_thread.isRunning():
            print("🛑 Stop bestaande verwerking thread...")
            self.processing_thread.stop()
            self.processing_thread.wait(5000)  # Wacht maximaal 5 seconden
            print("✅ Bestaande thread gestopt")
        
        print("🧵 Maak ProcessingThread aan...")
        self.processing_thread = ProcessingThread(files, settings)
        # Stel de file list callback in zodat de thread altijd de actuele lijst kan ophalen
        self.processing_thread.set_file_list_callback(lambda: self.main_window.files_panel.get_file_list())
        self.processing_thread.progress_updated.connect(self.main_window.update_progress)
        self.processing_thread.status_updated.connect(self._on_status_updated)
        self.processing_thread.processing_finished.connect(self._on_processing_finished)
        self.processing_thread.error_occurred.connect(self._on_processing_error)
        stop_manager.set_processing_thread(self.processing_thread)
        stop_manager.set_main_window(self.main_window)
        print("▶️ Start ProcessingThread...")
        self.processing_thread.start()
    
    def _on_status_updated(self, message: str):
        """Handle status updates van processing thread"""
        # Alleen debug loggen voor belangrijke berichten als debug mode aan staat
        if DEBUG_MODE and any(keyword in message for keyword in ["COMPLETED_FILE:", "FILE_COMPLETED_REMOVE:", "CONSOLE_OUTPUT:", "❌", "⚠️", "✅"]):
            try:
                from magic_time_studio.core.logging import logger
                logger.log_debug(f"Status update: {message}")
            except ImportError:
                pass
        
        # Check of dit een completed file signal is
        if message.startswith("COMPLETED_FILE:"):
            # Parse het signal - gebruik een betere methode voor paden met spaties
            try:
                # Verwijder "COMPLETED_FILE:" prefix
                content = message[len("COMPLETED_FILE:"):]
                
                # Zoek naar de laatste ":" om output_path te scheiden
                # Voorbeeld: "D:/Films & Serie/Film/file.mp4:D:/Films & Serie/Film/file.mp4"
                last_colon_index = content.rfind(":")
                if last_colon_index != -1:
                    file_path = content[:last_colon_index]
                    output_path = content[last_colon_index + 1:]
                    
                    # Voeg toe aan completed files
                    self.main_window.add_completed_file(file_path, output_path)
                    # Update status met normale bericht
                    self.main_window.update_status(f"✅ {file_path} voltooid")
                else:
                    if DEBUG_MODE:
                        try:
                            from magic_time_studio.core.logging import logger
                            logger.log_debug("Signal parsing gefaald - geen colon gevonden")
                        except ImportError:
                            pass
            except Exception as e:
                if DEBUG_MODE:
                    try:
                        from magic_time_studio.core.logging import logger
                        logger.log_debug(f"Signal parsing error: {e}")
                    except ImportError:
                        pass
        elif message.startswith("FILE_COMPLETED_REMOVE:"):
            # Handle direct signal om bestand uit "nog te doen" lijst te verwijderen
            file_path = message[len("FILE_COMPLETED_REMOVE:"):]
            
            # Voeg eerst toe aan voltooide lijst
            self.main_window.add_completed_file(file_path, file_path)  # Gebruik file_path als output_path
            
            # Roep de on_file_completed methode aan om het bestand te verwijderen uit "nog te doen" lijst
            self.main_window.on_file_completed(file_path)
        elif message.startswith("CONSOLE_OUTPUT:"):
            # Parse console output signal
            parts = message.split(":", 2)
            if len(parts) >= 3:
                console_message = parts[1]
                try:
                    progress = float(parts[2])
                    # Progress is al een decimale waarde (0.0-1.0), dus geen conversie nodig
                except ValueError:
                    progress = None
                
                # Voeg toe aan console output in GUI
                if hasattr(self.main_window, 'processing_panel'):
                    self.main_window.processing_panel.add_console_output(console_message, progress)
                    # Update ook de console progress indicator
                    if progress is not None:
                        self.main_window.processing_panel.update_console_progress(progress)
        else:
            # Normale status update
            self.main_window.update_status(message)
            # Voeg ook toe aan processing panel log
            if hasattr(self.main_window, 'processing_panel'):
                self.main_window.processing_panel.log_output.append(message)
                self.main_window.processing_panel.log_output.ensureCursorVisible()
                
                # Voeg ook toe aan console output voor real-time updates
                self.main_window.processing_panel.add_console_output(message)
                
                # Update console progress indicator voor Fast Whisper progress updates
                if "🎤 Fast Whisper:" in message and "%" in message:
                    # Parse Fast Whisper progress uit bericht
                    try:
                        # Zoek naar percentage in het bericht (bijv. "🎤 Fast Whisper: 45.5% - filename")
                        percent_str = message.split("🎤 Fast Whisper:")[1].split("%")[0].strip()
                        percent = float(percent_str)
                        # Update console met Fast Whisper progress
                        print(f"🔍 [DEBUG] Fast Whisper progress: {percent:.1f}% - {message}")
                    except:
                        pass
            
            # Voeg ook toe aan logging systeem voor log viewer
            try:
                from magic_time_studio.core.logging import logger
                logger.add_log_message(message, "INFO")
            except ImportError:
                pass  # Stil falen als logging niet beschikbaar is
    
    def _on_stop_processing(self):
        """Stop verwerking via StopManager"""
        print("🛑 Stop verwerking via StopManager...")
        stop_manager.stop_all_processes()
    
    def _on_processing_finished(self):
        """Verwerking voltooid"""
        print("✅ Verwerking voltooid")
        self.main_window.processing_finished()
    
    def _on_processing_error(self, error: str):
        """Fout tijdens verwerking"""
        print(f"❌ Verwerking fout: {error}")
        self.main_window.processing_active = False
        self.main_window.processing_finished()
        QMessageBox.critical(self.main_window, "Fout", f"Verwerking fout: {error}")
    
    def run(self):
        """Start de applicatie"""
        print("🚀 Magic Time Studio PyQt6 wordt gestart...")
        
        try:
            # Maak UI
            self.create_ui()
            
            # Toon hoofdvenster
            self.main_window.show()
            
            # Stel taakbalk icoon in na het tonen van het venster
            QTimer.singleShot(200, self.setTaskbarIcon)
            
            # Start event loop
            return self.app.exec()
            
        except Exception as e:
            print(f"❌ Fout bij starten applicatie: {e}")
            return 1
    
    def quit_app(self):
        """Sluit de applicatie"""
        print("👋 Magic Time Studio wordt afgesloten...")
        
        # Stop verwerking als actief via StopManager
        if self.processing_thread and self.processing_thread.isRunning():
            print("🛑 Stop verwerking bij afsluiten...")
            stop_manager.stop_all_processes()
        
        # Release single instance lock
        if hasattr(self, 'lock_file'):
            release_single_instance_lock(self.lock_file)
        
        # Probeer ook oude lock files op te ruimen
        try:
            import tempfile
            old_lock_file = os.path.join(tempfile.gettempdir(), "magic_time_studio.lock")
            if os.path.exists(old_lock_file):
                os.remove(old_lock_file)
                print(f"🗑️ Oude lock file verwijderd: {old_lock_file}")
        except Exception as e:
            print(f"⚠️ Kon oude lock file niet verwijderen: {e}")
        
        # Sluit applicatie
        if self.app:
            self.app.quit()