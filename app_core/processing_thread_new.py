"""
ProcessingThread - Modulaire versie voor Magic Time Studio
Gebruikt de nieuwe modulaire functies
"""

import os
from PySide6.QtCore import QThread, Signal
from typing import List, Dict

class ProcessingThread(QThread):
    """Processing thread voor Magic Time Studio"""
    
    # Definieer signals als class variabelen (moet buiten __init__ staan)
    progress_updated = Signal(float, str)
    status_updated = Signal(str)
    error_occurred = Signal(str)
    processing_completed = Signal()
    processing_finished = Signal()  # Alias voor processing_completed voor backward compatibility
    
    def __init__(self, files: List[str], processing_core, settings: Dict = None):
        super().__init__()
        self.files = files
        self.processing_core = processing_core
        self.settings = settings or {}
        self.whisperx_processor = None
        self.is_running = True
        self._should_stop = False
        
        # Debug: toon instellingen
        print(f"🔧 [DEBUG] ProcessingThread: Instellingen ontvangen: {self.settings}")
        if self.settings:
            language = self.settings.get('language', 'en')
            model = self.settings.get('whisper_model', 'large-v3')
            print(f"🌍 [DEBUG] ProcessingThread: Taal: {language}, Model: {model}")
        else:
            print("⚠️ [DEBUG] ProcessingThread: Geen instellingen ontvangen, gebruik standaardwaarden")
        
        # Initialiseer WhisperX processor
        try:
            # Gebruik absolute import in plaats van relatief
            from app_core.whisperx.whisperx_processor import WhisperXProcessor
            self.whisperx_processor = WhisperXProcessor()
            print(f"✅ [INFO] WhisperX processor geïnitialiseerd")
        except Exception as e:
            print(f"❌ [FOUT] Kon WhisperX processor niet initialiseren: {e}")
            # Probeer alternatieve import
            try:
                import sys
                sys.path.append(os.path.dirname(os.path.dirname(__file__)))
                from whisperx.whisperx_processor import WhisperXProcessor
                self.whisperx_processor = WhisperXProcessor()
                print(f"✅ [INFO] WhisperX processor geïnitialiseerd via alternatief pad")
            except Exception as e2:
                print(f"❌ [FOUT] Ook alternatieve import gefaald: {e2}")
    
    def cleanup(self):
        """Veilige cleanup van de thread"""
        print(f"🧹 [CLEANUP] ProcessingThread: Start cleanup")
        self._should_stop = True
        self.is_running = False
        
        # Wacht tot thread natuurlijk stopt
        if self.isRunning():
            print(f"⏳ [CLEANUP] Wacht tot thread natuurlijk stopt...")
            self.wait(3000)  # Wacht maximaal 3 seconden
    
    def _progress_callback(self, progress: float, message: str):
        """Progress callback voor WhisperX"""
        try:
            print(f"🔧 [DEBUG] Progress callback ontvangen: {progress:.1f}% - {message}")
            
            # Bereken totale progress op basis van huidige bestand en WhisperX progress
            if hasattr(self, 'current_file_index') and self.current_file_index is not None:
                file_progress = (self.current_file_index - 1) / len(self.files) * 100
                whisperx_progress = progress / len(self.files)
                total_progress = file_progress + whisperx_progress
                
                # Stuur progress update
                self.progress_updated.emit(total_progress, f"Bestand {self.current_file_index}: {message}")
                print(f"🔧 [DEBUG] Progress callback verwerkt: {total_progress:.1f}% - {message}")
            else:
                # Fallback naar basis progress
                self.progress_updated.emit(progress, message)
                print(f"🔧 [DEBUG] Progress callback (fallback): {progress:.1f}% - {message}")
                
        except Exception as e:
            print(f"⚠️ [WAARSCHUWING] Fout in progress callback: {e}")
    
    def run(self):
        """Voer verwerking uit in aparte thread"""
        try:
            print(f"🔧 [START] Processing thread gestart voor {len(self.files)} bestand(en)")
            
            for i, file_path in enumerate(self.files, 1):
                # Controleer of verwerking moet stoppen
                if self._should_stop:
                    print(f"🛑 [STOP] Verwerking gestopt door gebruiker")
                    break
                
                # Stel huidige bestand index in voor progress callback
                self.current_file_index = i
                
                try:
                    print(f"📁 [START] Start verwerking van bestand {i}/{len(self.files)}: {os.path.basename(file_path)}")
                    
                    # Update status
                    self.status_updated.emit(f"Verwerking bestand {i}/{len(self.files)}: {os.path.basename(file_path)}")
                    
                    # Start WhisperX verwerking
                    print(f"🎤 [START] Start WhisperX verwerking van {os.path.basename(file_path)}...")
                    
                    # Laad model als dat nog niet is gebeurd
                    if not self.whisperx_processor.model_manager.is_loaded:
                        print(f"🔧 [BEZIG] Laad WhisperX model...")
                        
                        # Haal VAD instellingen op uit settings
                        vad_settings = None
                        if self.settings:
                            vad_settings = {
                                "vad_enabled": self.settings.get("vad_enabled", True),
                                "vad_method": self.settings.get("vad_method", "Pyannote (nauwkeurig)"),
                                "vad_method_whisperx": "pyannote",  # Altijd pyannote voor WhisperX
                                "vad_threshold": self.settings.get("vad_threshold", 0.5),
                                "vad_onset": self.settings.get("vad_onset", 0.5),
                                "vad_chunk_size": self.settings.get("vad_chunk_size", 30),
                                "vad_min_speech": self.settings.get("vad_min_speech", 0.5),
                                "vad_min_silence": self.settings.get("vad_min_silence", 0.5),
                                "whisper_model": self.settings.get("whisper_model", "large-v3"),  # Voeg model toe voor ETA berekening
                            }
                            print(f"🔧 [DEBUG] VAD instellingen voor model loading: {vad_settings}")
                        
                        # Haal het geselecteerde model op uit de UI instellingen
                        selected_model = self.settings.get('whisper_model', 'large-v3')
                        print(f"🔧 [DEBUG] ProcessingThread: Gebruik geselecteerd model: {selected_model}")
                        
                        self.whisperx_processor.load_model(
                            model_name=selected_model,
                            vad_settings=vad_settings
                        )
                        print(f"✅ [VOLTOOID] WhisperX model geladen met VAD instellingen")
                    
                    # Start transcriptie
                    print(f"🎯 [START] Start transcriptie van {os.path.basename(file_path)}...")
                    
                    # Start transcriptie met betere progress tracking
                    print(f"🎯 [START] Start transcriptie van {os.path.basename(file_path)}...")
                    
                    # Voer transcriptie uit
                    language = self.settings.get('language', 'en')  # Standaard Engels
                    print(f"🌍 [INFO] Gebruik taal: {language}")
                    
                    # Haal VAD instellingen op voor transcriptie
                    vad_settings = None
                    if self.settings:
                        vad_settings = {
                            "vad_enabled": self.settings.get("vad_enabled", True),
                            "vad_method": self.settings.get("vad_method", "Pyannote (nauwkeurig)"),
                            "vad_method_whisperx": "pyannote",  # Altijd pyannote voor WhisperX
                            "vad_threshold": self.settings.get("vad_threshold", 0.5),
                            "vad_onset": self.settings.get("vad_onset", 0.5),
                            "vad_chunk_size": self.settings.get("vad_chunk_size", 30),
                            "vad_min_speech": self.settings.get("vad_min_speech", 0.5),
                            "vad_min_silence": self.settings.get("vad_min_silence", 0.5),
                            "whisper_model": self.settings.get("whisper_model", "large-v3"),  # Voeg model toe voor ETA berekening
                        }
                        print(f"🔧 [DEBUG] VAD instellingen voor transcriptie: {vad_settings}")
                    
                    # Start transcriptie met progress callback
                    print(f"🎯 [DEBUG] Start transcriptie met progress callback")
                    result = self.whisperx_processor.transcribe_with_alignment(
                        file_path,
                        language=language,
                        progress_callback=self._progress_callback,
                        vad_settings=vad_settings
                    )
                    
                    # Update progress na voltooiing van bestand
                    progress = (i / len(self.files)) * 100
                    filename = os.path.basename(file_path)
                    self.progress_updated.emit(progress, f"Bestand {i}/{len(self.files)} voltooid: {filename}")
                    print(f"🔧 [DEBUG] Progress bijgewerkt: {progress:.1f}%")
                    
                    if result:
                        print(f"✅ [VOLTOOID] Transcriptie succesvol voor {filename}")
                    else:
                        print(f"❌ [FOUT] Transcriptie gefaald voor {filename}")
                    
                except Exception as e:
                    print(f"❌ [FOUT] Fout tijdens transcriptie van {os.path.basename(file_path)}: {e}")
                    self.error_occurred.emit(f"Fout tijdens transcriptie van {os.path.basename(file_path)}: {e}")
            
            print(f"🎉 [VOLTOOID] Alle bestanden verwerkt!")
            self.processing_completed.emit()
            self.processing_finished.emit()  # Emit beide signals voor backward compatibility
            
            # Reset status
            self.is_running = False
            
        except Exception as e:
            print(f"❌ [FOUT] Fout in processing thread: {e}")
            self.error_occurred.emit(f"Fout in processing thread: {e}")
        finally:
            print(f"🔧 [INFO] Processing thread gestopt")
            self.is_running = False
    
    def get_current_file(self):
        """Krijg het huidige bestand dat wordt verwerkt"""
        return self.current_file
