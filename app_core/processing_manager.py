"""
Processing Manager voor Magic Time Studio PySide6
Beheert alle verwerking en thread management
"""

class ProcessingManager:
    """Beheert alle verwerking en thread management"""
    
    def __init__(self, main_app):
        self.main_app = main_app
        self.processing_thread = None
        
    def start_processing(self, files: list, settings: dict):
        """Start verwerking van bestanden"""
        print(f"🚀 Hoofdapplicatie: _on_start_processing aangeroepen met {len(files)} bestanden")
        print(f"🔧 Instellingen: {settings}")
        
        # Stop bestaande thread
        self._stop_existing_thread()
        
        # Maak nieuwe thread
        if not self._create_processing_thread(files, settings):
            return 1
        
        # Verbind signals
        self._connect_processing_thread_signals()
        
        # Start thread
        if not self._start_processing_thread():
            return 1
    
    def _stop_existing_thread(self):
        """Stop bestaande verwerking thread"""
        if self.processing_thread and self.processing_thread.isRunning():
            print("🛑 Stop bestaande verwerking thread...")
            try:
                # Gebruik de juiste methode om de thread te stoppen
                if hasattr(self.processing_thread, 'is_running'):
                    self.processing_thread.is_running = False
                    if hasattr(self.processing_thread, 'wait'):
                        self.processing_thread.wait(5000)  # Wacht maximaal 5 seconden
                    print("✅ Bestaande thread gestopt")
                else:
                    print("⚠️ processing_thread.is_running niet gevonden, geen thread gestopt")
            except Exception as e:
                print(f"⚠️ Fout bij stoppen bestaande thread: {e}")
    
    def _create_processing_thread(self, files: list, settings: dict):
        """Maak nieuwe ProcessingThread aan"""
        print("🧵 Maak ProcessingThread aan...")
        if self.main_app.ProcessingThread:
            try:
                # Maak ProcessingThread aan met files, processing_core en settings
                self.processing_thread = self.main_app.ProcessingThread(files, self, settings)
                print("✅ ProcessingThread aangemaakt")
                return True
            except Exception as e:
                print(f"❌ Fout bij aanmaken ProcessingThread: {e}")
                return False
        else:
            print("❌ ProcessingThread niet geïnitialiseerd, verwerking zal niet starten")
            return False
    
    def _connect_processing_thread_signals(self):
        """Verbind ProcessingThread signalen"""
        if not self.processing_thread:
            return
        
        # Verbind progress signal
        self._connect_progress_signal()
        
        # Verbind status signalen
        self._connect_status_signals()
        
        # StopManager configuratie verwijderd - geen stop functionaliteit meer
    
    def _connect_progress_signal(self):
        """Verbind progress signal"""
        try:
            if self.main_app.ui_manager.main_window and hasattr(self.main_app.ui_manager.main_window, 'update_progress'):
                self.processing_thread.progress_updated.connect(self.main_app.ui_manager.main_window.update_progress)
                print("✅ progress_updated signal verbonden")
            else:
                print("⚠️ update_progress methode niet gevonden in main_window of main_window is None")
        except Exception as e:
            print(f"⚠️ Fout bij verbinden progress_updated signal: {e}")
    
    def _connect_status_signals(self):
        """Verbind status signalen"""
        try:
            self.processing_thread.status_updated.connect(self._on_status_updated)
            print("✅ status_updated signal verbonden")
        except Exception as e:
            print(f"⚠️ Fout bij verbinden status_updated signal: {e}")
        
        try:
            self.processing_thread.processing_finished.connect(self._on_processing_finished)
            print("✅ processing_finished signal verbonden")
        except Exception as e:
            print(f"⚠️ Fout bij verbinden processing_finished signal: {e}")
        
        try:
            self.processing_thread.error_occurred.connect(self._on_processing_error)
            print("✅ error_occurred signal verbonden")
        except Exception as e:
            print(f"⚠️ Fout bij verbinden error_occurred signal: {e}")
    

    
    def _start_processing_thread(self):
        """Start de ProcessingThread"""
        print("▶️ Start ProcessingThread...")
        try:
            self.processing_thread.start()
            print("✅ ProcessingThread gestart")
            return True
        except Exception as e:
            print(f"❌ Fout bij starten ProcessingThread: {e}")
            return False
    
    def _on_status_updated(self, message: str):
        """Handle status updates van processing thread"""
        # Debug logging
        self._log_debug_status(message)
        
        # Verwerk verschillende soorten berichten
        if message.startswith("COMPLETED_FILE:"):
            self._handle_completed_file(message)
        elif message.startswith("FILE_COMPLETED_REMOVE:"):
            self._handle_file_completed_remove(message)
        elif message.startswith("CONSOLE_OUTPUT:"):
            self._handle_console_output(message)
        else:
            self._handle_normal_status_update(message)
    
    def _log_debug_status(self, message: str):
        """Log status updates in debug mode"""
        if self.main_app.DEBUG_MODE and any(keyword in message for keyword in ["COMPLETED_FILE:", "FILE_COMPLETED_REMOVE:", "CONSOLE_OUTPUT:", "❌", "⚠️", "✅"]):
            try:
                # Probeer verschillende import methoden
                try:
                    from ...core.logging import logger
                except ImportError:
                    try:
                        from magic_time_studio.core.logging import logger
                    except ImportError:
                        logger = None
                
                if logger:
                    logger.debug(f"Status update: {message}")
            except ImportError:
                pass
    
    def _handle_completed_file(self, message: str):
        """Verwerk completed file bericht"""
        try:
            # Verwijder "COMPLETED_FILE:" prefix
            content = message[len("COMPLETED_FILE:"):]
            
            # Zoek naar de laatste ":" om output_path te scheiden
            last_colon_index = content.rfind(":")
            if last_colon_index != -1:
                file_path = content[:last_colon_index]
                output_path = content[last_colon_index + 1:]
                
                # Voeg toe aan completed files
                if self.main_app.ui_manager.main_window:
                    self.main_app.ui_manager.main_window.add_completed_file(file_path, output_path)
                    # Update status met normale bericht
                    self.main_app.ui_manager.main_window.update_status(f"✅ {file_path} voltooid")
                else:
                    print(f"⚠️ main_window is None, geen completed_file toegevoegd: {file_path}")
            else:
                if self.main_app.DEBUG_MODE:
                    try:
                        from magic_time_studio.core.logging import logger
                        logger.debug("Signal parsing gefaald - geen colon gevonden")
                    except ImportError:
                        pass
        except Exception as e:
            if self.main_app.DEBUG_MODE:
                try:
                    from magic_time_studio.core.logging import logger
                    logger.debug(f"Signal parsing error: {e}")
                except ImportError:
                    pass
    
    def _handle_file_completed_remove(self, message: str):
        """Verwerk file completed remove bericht"""
        file_path = message[len("FILE_COMPLETED_REMOVE:"):]
        
        # Voeg eerst toe aan voltooide lijst
        if self.main_app.ui_manager.main_window:
            try:
                self.main_app.ui_manager.main_window.add_completed_file(file_path, file_path)  # Gebruik file_path als output_path
                print(f"✅ Bestand toegevoegd aan voltooide lijst: {file_path}")
            except Exception as e:
                print(f"⚠️ Fout bij toevoegen aan voltooide lijst: {e}")
            
            try:
                # Roep de on_file_completed methode aan om het bestand te verwijderen uit "nog te doen" lijst
                self.main_app.ui_manager.main_window.on_file_completed(file_path)
                print(f"✅ Bestand verwijderd uit te verwerken lijst: {file_path}")
            except Exception as e:
                print(f"⚠️ Fout bij verwijderen uit te verwerken lijst: {e}")
        else:
            print(f"⚠️ main_window is None, geen FILE_COMPLETED_REMOVE verwerkt: {file_path}")
    
    def _handle_console_output(self, message: str):
        """Verwerk console output bericht"""
        parts = message.split(":", 2)
        if len(parts) >= 3:
            console_message = parts[1]
            try:
                progress = float(parts[2])
                # Progress is al een decimale waarde (0.0-1.0), dus geen conversie nodig
            except ValueError:
                progress = None
            
            # Update alleen de console progress indicator (geen dubbele console output)
            if self.main_app.ui_manager.main_window and hasattr(self.main_app.ui_manager.main_window, 'processing_panel'):
                if progress is not None:
                    self.main_app.ui_manager.main_window.processing_panel.update_console_progress(progress)
            else:
                print("⚠️ main_window of processing_panel is None, geen CONSOLE_OUTPUT verwerkt")
    
    def _handle_normal_status_update(self, message: str):
        """Verwerk normale status update"""
        if self.main_app.ui_manager.main_window:
            # Update alleen de hoofdstatus (geen dubbele logging)
            self.main_app.ui_manager.main_window.update_status(message)
            
            # Voeg toe aan processing panel log (alleen voor belangrijke berichten)
            if hasattr(self.main_app.ui_manager.main_window, 'processing_panel'):
                self._update_processing_panel(message)
            else:
                print("⚠️ main_window of processing_panel is None, geen status update verwerkt")
        
        # Voeg toe aan logging systeem voor log viewer (alleen voor belangrijke berichten)
        if any(keyword in message for keyword in ["✅", "❌", "⚠️", "🚀", "🎬", "🎤", "⏱️"]):
            self._log_status_message(message)
    
    def _update_processing_panel(self, message: str):
        """Update processing panel met status bericht"""
        try:
            # Voeg toe aan processing panel log (alleen voor belangrijke berichten, geen duplicaten)
            if any(keyword in message for keyword in ["✅", "❌", "⚠️", "🚀", "🎬", "🎤", "⏱️"]):
                # Controleer of bericht al in log staat om duplicaten te voorkomen
                log_output = self.main_app.ui_manager.main_window.processing_panel.log_output
                if not log_output.toPlainText().endswith(message):
                    log_output.append(message)
                    log_output.ensureCursorVisible()
            
            # WhisperX progress parsing
            if "WhisperX:" in message or "whisperx" in message.lower():
                self._parse_whisperx_progress(message)
            elif "transcriptie" in message.lower() or "transcription" in message.lower():
                self._parse_whisperx_progress(message)
            elif "alignment" in message.lower():
                self._parse_whisperx_progress(message)
        except Exception as e:
            print(f"⚠️ Fout bij updaten processing panel: {e}")
    
    def _parse_whisperx_progress(self, message: str):
        """Parse WhisperX progress uit bericht"""
        try:
            # Controleer of het bericht WhisperX progress bevat
            if "WhisperX:" not in message:
                return  # Geen WhisperX progress bericht
            
            # Zoek naar percentage in het bericht (bijv. "WhisperX: 45.5% - filename")
            # of "whisperx: 45.5% - filename")
            parts = message.split("WhisperX:")
            if len(parts) < 2:
                return  # Niet genoeg delen
                
            percent_part = parts[1].split("%")[0].strip()
            if ":" in percent_part:
                percent_str = percent_part.split(":")[1].strip()
                try:
                    percent = float(percent_str)
                    # Update console met WhisperX progress
                    print(f"🔍 [DEBUG] WhisperX progress: {percent:.1f}% - {message}")
                    
                    # Update ook de hoofdprogress bar als mogelijk
                    if self.main_app.ui_manager.main_window and hasattr(self.main_app.ui_manager.main_window, 'processing_panel'):
                        try:
                            # WhisperX progress is ongeveer 15% van de totale verwerking (50% tot 65%)
                            whisper_progress = 50.0 + (percent * 0.15)
                            self.main_app.ui_manager.main_window.processing_panel.progress_bar.setValue(int(whisper_progress))
                        except Exception as e:
                            print(f"⚠️ Fout bij updaten hoofdprogress bar: {e}")
                except ValueError:
                    # Kon percentage niet parsen
                    pass
        except Exception as e:
            print(f"⚠️ Fout bij parsen WhisperX progress: {e}")
            pass
    
    def _log_status_message(self, message: str):
        """Log status bericht in logging systeem"""
        try:
            # Probeer verschillende import methoden
            try:
                from ...core.logging import logger
            except ImportError:
                try:
                    from magic_time_studio.core.logging import logger
                except ImportError:
                    logger = None
            
            if logger:
                # Use the standard logging methods instead of add_log_message
                logger.info(message)
        except ImportError:
            pass  # Stil falen als logging niet beschikbaar is
    
    def _on_processing_finished(self):
        """Verwerking voltooid"""
        print("✅ Verwerking voltooid")
        if self.main_app.ui_manager.main_window and hasattr(self.main_app.ui_manager.main_window, 'processing_finished'):
            try:
                self.main_app.ui_manager.main_window.processing_finished()
                print("✅ processing_finished aangeroepen")
            except Exception as e:
                print(f"⚠️ Fout bij aanroepen processing_finished: {e}")
        else:
            print("⚠️ processing_finished methode niet gevonden in main_window")
    
    def _on_processing_error(self, error: str):
        """Fout tijdens verwerking"""
        print(f"❌ Verwerking fout: {error}")
        if self.main_app.ui_manager.main_window:
            self._reset_processing_on_error()
            self._show_error_message(error)
        else:
            print("⚠️ main_window is None, geen foutmelding weergegeven")
    
    def _reset_processing_on_error(self):
        """Reset processing state bij fout"""
        try:
            self.main_app.ui_manager.main_window.processing_active = False
            print("✅ processing_active flag gereset")
        except Exception as e:
            print(f"⚠️ Fout bij resetten processing_active flag: {e}")
        
        try:
            if hasattr(self.main_app.ui_manager.main_window, 'processing_finished'):
                self.main_app.ui_manager.main_window.processing_finished()
                print("✅ processing_finished aangeroepen")
            else:
                print("⚠️ processing_finished methode niet gevonden in main_window")
        except Exception as e:
            print(f"⚠️ Fout bij aanroepen processing_finished: {e}")
    
    def _show_error_message(self, error: str):
        """Toon foutmelding aan gebruiker"""
        try:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.critical(self.main_app.ui_manager.main_window, "Fout", f"Verwerking fout: {error}")
            print("✅ Foutmelding weergegeven")
        except Exception as e:
            print(f"⚠️ Fout bij weergeven foutmelding: {e}")
    

    
    def _reset_processing_ui(self):
        """Reset processing UI"""
        if self.main_app.ui_manager.main_window:
            try:
                self.main_app.ui_manager.main_window.processing_active = False
                print("✅ processing_active flag gereset")
            except Exception as e:
                print(f"⚠️ Fout bij resetten processing_active flag: {e}")
            
            try:
                if hasattr(self.main_app.ui_manager.main_window, 'processing_finished'):
                    self.main_app.ui_manager.main_window.processing_finished()
                    print("✅ processing_finished aangeroepen")
                else:
                    print("⚠️ processing_finished methode niet gevonden in main_window")
            except Exception as e:
                print(f"⚠️ Fout bij aanroepen processing_finished: {e}")
    

