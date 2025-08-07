"""
ProcessingThread - Modulaire versie voor Magic Time Studio
"""

import os
from PyQt6.QtCore import QThread, pyqtSignal
from .processing_modules import AudioProcessor, WhisperProcessor, TranslationProcessor, VideoProcessor

# Debug mode - zet op False om debug output uit te zetten
DEBUG_MODE = False

# Alle debug prints uitcommentariëren voor schonere output
def debug_print(*args, **kwargs):
    """Debug print functie die niets doet"""
    pass

class ProcessingThread(QThread):
    """Thread voor verwerking van bestanden - Modulaire versie"""
    progress_updated = pyqtSignal(float, str)
    status_updated = pyqtSignal(str)
    processing_finished = pyqtSignal()
    error_occurred = pyqtSignal(str)
    
    def __init__(self, files, settings):
        super().__init__()
        self.files = files
        self.settings = settings
        self.is_running = True
        self.current_file = None
        
        # Initialiseer processing modules
        self.audio_processor = AudioProcessor(self)
        self.whisper_processor = WhisperProcessor(self)
        self.translation_processor = TranslationProcessor(self)
        self.video_processor = VideoProcessor(self)
    
    def run(self):
        """Voer verwerking uit in aparte thread"""
        try:
            # Gebruik de echte bestanden uit de files lijst
            if not self.files:
                self.status_updated.emit("⚠️ Geen bestanden geselecteerd voor verwerking")
                self.processing_finished.emit()
                return
            
            # Filter alleen video bestanden
            video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']
            video_files = [f for f in self.files if any(f.lower().endswith(ext) for ext in video_extensions)]
            total_files = len(video_files)
            
            if not video_files:
                self.status_updated.emit("⚠️ Geen video bestanden gevonden om te verwerken")
                self.processing_finished.emit()
                return
            
            self.status_updated.emit(f"🚀 Start verwerking van {total_files} video bestanden")
            completed = 0
            
            for i, file_path in enumerate(video_files):
                self.current_file = file_path
                
                if not self.is_running:
                    break
                    
                self.status_updated.emit(f"🎬 Start verwerking: {file_path}")
                
                # Update progress voor dit bestand
                file_progress = (i / total_files) * 100
                progress_message = f"Bestand {i+1} van {total_files}: {os.path.basename(file_path)}"
                
                # Reset progress bar voor nieuw bestand
                self.progress_updated.emit(0.0, f"🎬 Start verwerking: {os.path.basename(file_path)}")
                
                try:
                    # Stap 1: Audio extractie
                    audio_path = self.audio_processor.extract_audio(file_path)
                    if not audio_path:
                        continue
                    
                    # Check of verwerking gestopt moet worden
                    if not self.is_running:
                        self.status_updated.emit("🛑 Verwerking gestopt door gebruiker")
                        break
                    
                    # Stap 2: Fast Whisper transcriptie
                    whisper_result = self.whisper_processor.transcribe_audio(audio_path, file_path)
                    if not whisper_result:
                        continue
                    
                    transcript = whisper_result["transcript"]
                    transcriptions = whisper_result["transcriptions"]
                    source_language = whisper_result["language"]
                    
                    # Check of verwerking gestopt moet worden
                    if not self.is_running:
                        self.status_updated.emit("🛑 Verwerking gestopt door gebruiker")
                        break
                    
                    # Update progress na transcriptie
                    self.progress_updated.emit(file_progress + 65, f"🌐 Vertaling: {os.path.basename(file_path)}")
                    
                    # Stap 3: Vertaling (als ingesteld)
                    transcript, translated_transcriptions = self.translation_processor.translate_content(
                        transcript, transcriptions, source_language
                    )
                    
                    # Check of verwerking gestopt moet worden
                    if not self.is_running:
                        self.status_updated.emit("🛑 Verwerking gestopt door gebruiker")
                        break
                    
                    # Stap 4: Video verwerking
                    video_result = self.video_processor.process_video(
                        file_path, transcript, transcriptions, translated_transcriptions
                    )
                    
                    # Bepaal output pad
                    if "error" in video_result:
                        self.status_updated.emit(f"⚠️ Video verwerking gefaald: {video_result['error']}")
                        output_path = file_path
                    else:
                        output_path = file_path
                    
                    # Ruim tijdelijke bestanden op
                    try:
                        if os.path.exists(audio_path):
                            os.remove(audio_path)
                    except Exception as e:
                        pass  # Stil falen bij cleanup
                    
                    completed += 1
                    self.status_updated.emit(f"✅ {file_path} voltooid")
                    
                    # Voeg toe aan completed files via signal
                    completed_signal = f"COMPLETED_FILE:{file_path}:{output_path}"
                    self.status_updated.emit(completed_signal)
                    
                    # Emit ook een direct signal om het bestand uit de "nog te doen" lijst te verwijderen
                    self.status_updated.emit(f"FILE_COMPLETED_REMOVE:{file_path}")
                    
                    # Update progress naar 100% voor dit bestand
                    self.progress_updated.emit(100.0, f"✅ {os.path.basename(file_path)} voltooid")
                    
                except Exception as e:
                    self.status_updated.emit(f"❌ Fout bij verwerken {file_path}: {str(e)}")
                    continue
            
            if self.is_running:
                self.progress_updated.emit(100.0, "Verwerking voltooid!")
                self.processing_finished.emit()
            
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            # Zorg ervoor dat de verwerking altijd als voltooid wordt gemarkeerd
            self.progress_updated.emit(100.0, "Verwerking voltooid!")
            self.processing_finished.emit()
    
    def stop(self):
        """Stop de verwerking"""
        self.is_running = False
        
        # Wacht tot de thread stopt
        if self.isRunning():
            self.wait(5000)  # Wacht maximaal 5 seconden
    
    def set_file_list_callback(self, callback):
        """Stel een callback in om de actuele file list op te halen"""
        self._file_list_callback = callback
