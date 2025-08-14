"""
ProcessingThread - Modulaire versie voor Magic Time Studio
Gebruikt de nieuwe modulaire functies
"""

import os
from PyQt6.QtCore import QThread, pyqtSignal

# Import processing modules
try:
    from .processing_modules import AudioProcessor, WhisperProcessor, TranslationProcessor, VideoProcessor
except ImportError:
    # Fallback als imports falen
    AudioProcessor = None
    WhisperProcessor = None
    TranslationProcessor = None
    VideoProcessor = None

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
        print(f"🔍 [DEBUG] ProcessingThread.__init__: Ontvangen instellingen: {self.settings}")
        self.is_running = True
        self.current_file = None
        
        # Initialiseer processing modules (gebruiken nu modulaire functies)
        self.audio_processor = AudioProcessor(self) if AudioProcessor else None
        self.whisper_processor = WhisperProcessor(self) if WhisperProcessor else None
        self.translation_processor = TranslationProcessor(self) if TranslationProcessor else None
        self.video_processor = VideoProcessor(self) if VideoProcessor else None
        
        # Debug: toon status van alle modules
        print(f"🔍 [DEBUG] ProcessingThread: Audio processor: {self.audio_processor}")
        print(f"🔍 [DEBUG] ProcessingThread: Whisper processor: {self.whisper_processor}")
        print(f"🔍 [DEBUG] ProcessingThread: Translation processor: {self.translation_processor}")
        print(f"🔍 [DEBUG] ProcessingThread: Video processor: {self.video_processor}")
        
        # Controleer of alle modules beschikbaar zijn
        if not all([self.audio_processor, self.whisper_processor, self.translation_processor, self.video_processor]):
            print("⚠️ Niet alle processing modules zijn beschikbaar")
    

    
    def run(self):
        """Voer verwerking uit in aparte thread - gebruikt modulaire functies"""
        try:
            print(f"🔍 [DEBUG] ProcessingThread.run: Start met instellingen: {self.settings}")
            
            # Controleer of alle modules beschikbaar zijn
            if not all([self.audio_processor, self.whisper_processor, self.translation_processor, self.video_processor]):
                self.error_occurred.emit("Niet alle processing modules zijn beschikbaar")
                self.processing_finished.emit()
                return
            
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
                    
                # Update progress voor dit bestand
                file_progress = (i / total_files) * 100
                progress_message = f"Bestand {i+1} van {total_files}: {os.path.basename(file_path)}"
                
                # Reset progress bar voor nieuw bestand
                self.progress_updated.emit(0.0, f"🎬 Start verwerking: {os.path.basename(file_path)}")
                
                try:
                    # Stap 1: Audio extractie (gebruikt modulaire functie)
                    print(f"🔍 [DEBUG] ProcessingThread: Start stap 1 - Audio extractie")
                    self.status_updated.emit(f"🎵 Audio extractie gestart: {os.path.basename(file_path)}")
                    self.progress_updated.emit(10.0, f"🎵 Audio extractie...")
                    
                    # Geef instellingen door aan audio processor
                    if hasattr(self, 'settings') and self.settings:
                        print(f"🔍 [DEBUG] ProcessingThread: Geef instellingen door aan audio processor: {self.settings}")
                        self.audio_processor.set_settings(self.settings)
                    
                    audio_path = self.audio_processor.extract_audio(file_path)
                    if not audio_path:
                        print(f"🔍 [DEBUG] ProcessingThread: Audio extractie gefaald")
                        continue
                    
                    # Controleer of audio bestand nog bestaat en wacht even
                    import time
                    time.sleep(0.5)  # Wacht 0.5 seconde om zeker te zijn dat bestand is geschreven
                    
                    if not os.path.exists(audio_path):
                        print(f"❌ Audio bestand verdwenen na extractie: {audio_path}")
                        continue
                    
                    print(f"🔍 [DEBUG] ProcessingThread: Audio extractie voltooid: {audio_path}")
                    print(f"🔍 [DEBUG] ProcessingThread: Audio bestand grootte: {os.path.getsize(audio_path)} bytes")
                    
                    # Update progress na audio extractie (geen dubbele status update)
                    self.progress_updated.emit(25.0, f"✅ Audio extractie voltooid: {os.path.basename(file_path)}")
                    
                    # Check of verwerking gestopt moet worden
                    if not self.is_running:
                        self.status_updated.emit("🛑 Verwerking gestopt door gebruiker")
                        break
                    
                    # Stap 2: Whisper transcriptie (gebruikt modulaire functie)
                    print(f"🔍 [DEBUG] ProcessingThread: Start stap 2 - Whisper transcriptie")
                    
                    # Geef instellingen door aan whisper processor
                    if hasattr(self, 'settings') and self.settings:
                        print(f"🔍 [DEBUG] ProcessingThread: Geef instellingen door aan whisper processor: {self.settings}")
                        self.whisper_processor.set_settings(self.settings)
                    
                    # Update status voor whisper transcriptie (geen dubbele status update)
                    self.progress_updated.emit(30.0, f"🎤 Whisper transcriptie gestart...")
                    
                    # Geef de settings door aan transcribe_audio
                    whisper_result = self.whisper_processor.transcribe_audio(audio_path, self.settings)
                    if not whisper_result:
                        print(f"🔍 [DEBUG] ProcessingThread: Whisper transcriptie gefaald")
                        continue
                    
                    print(f"🔍 [DEBUG] ProcessingThread: Whisper transcriptie voltooid")
                    print(f"🔍 [DEBUG] ProcessingThread: whisper_result type: {type(whisper_result)}")
                    
                    # Update progress na transcriptie (geen dubbele status update)
                    self.progress_updated.emit(65.0, f"✅ Whisper transcriptie voltooid: {os.path.basename(file_path)}")
                    
                    transcript = whisper_result.get("transcript", "")
                    
                    # Check of transcriptions of segments beschikbaar zijn
                    if "transcriptions" in whisper_result:
                        transcriptions = whisper_result["transcriptions"]
                    elif "segments" in whisper_result:
                        # Converteer segments naar transcriptions formaat
                        transcriptions = []
                        for segment in whisper_result["segments"]:
                            transcriptions.append({
                                "start": segment.get("start", 0.0),
                                "end": segment.get("end", 0.0),
                                "text": segment.get("text", "")
                            })
                    else:
                        # Fallback: maak een enkele transcriptie
                        transcriptions = [{
                            "start": 0.0,
                            "end": 5.0,
                            "text": transcript
                        }]
                    
                    source_language = whisper_result.get("language", "auto")
                    
                    print(f"🔍 [DEBUG] ProcessingThread: transcript type: {type(transcript)}, lengte: {len(transcript) if transcript else 0}")
                    print(f"🔍 [DEBUG] ProcessingThread: transcriptions type: {type(transcriptions)}, count: {len(transcriptions) if transcriptions else 0}")
                    
                    # Check of verwerking gestopt moet worden
                    if not self.is_running:
                        self.status_updated.emit("🛑 Verwerking gestopt door gebruiker")
                        break
                    
                    # Update progress na transcriptie
                    self.progress_updated.emit(file_progress + 65, f"🌐 Vertaling: {os.path.basename(file_path)}")
                    
                    # Stap 3: Vertaling (als ingesteld) - gebruikt modulaire functie
                    print(f"🔍 [DEBUG] ProcessingThread: Start stap 3 - Vertaling")
                    print(f"🔍 [DEBUG] ProcessingThread: Vertaling instellingen: {self.settings}")
                    print(f"🔍 [DEBUG] ProcessingThread: Translation processor: {self.translation_processor}")
                    print(f"🔍 [DEBUG] ProcessingThread: Translation processor type: {type(self.translation_processor)}")
                    print(f"🔍 [DEBUG] ProcessingThread: Translation processor methods: {dir(self.translation_processor) if self.translation_processor else 'None'}")
                    
                    # Controleer of vertaling is ingeschakeld
                    translator_enabled = self.settings.get("translator", "none") == "libretranslate" if self.settings else False
                    print(f"🔍 [DEBUG] ProcessingThread: Vertaling ingeschakeld: {translator_enabled}")
                    
                    if translator_enabled:
                        print(f"🔍 [DEBUG] ProcessingThread: Vertaling stap wordt uitgevoerd!")
                        self.status_updated.emit(f"🌐 Start vertaling: {os.path.basename(file_path)}")
                        self.progress_updated.emit(70.0, f"🌐 Vertaling...")
                        
                        try:
                            # Geef instellingen door aan translation processor
                            if hasattr(self, 'settings') and self.settings:
                                print(f"🔍 [DEBUG] ProcessingThread: Geef instellingen door aan translation processor: {self.settings}")
                                self.translation_processor.set_settings(self.settings)
                            
                            transcript, translated_transcriptions = self.translation_processor.translate_content(
                                transcript, transcriptions, source_language
                            )
                            print(f"🔍 [DEBUG] ProcessingThread: Vertaling voltooid")
                            print(f"🔍 [DEBUG] ProcessingThread: translated_transcriptions type: {type(translated_transcriptions)}, count: {len(translated_transcriptions) if translated_transcriptions else 0}")
                            
                            self.progress_updated.emit(75.0, f"✅ Vertaling voltooid: {os.path.basename(file_path)}")
                            self.status_updated.emit(f"✅ Vertaling voltooid: {os.path.basename(file_path)}")
                            
                        except Exception as e:
                            print(f"🔍 [DEBUG] ProcessingThread: Vertaling gefaald: {e}")
                            import traceback
                            print(f"🔍 [DEBUG] ProcessingThread: Vertaling traceback: {traceback.format_exc()}")
                            # Gebruik originele transcriptie als vertaling faalt
                            translated_transcriptions = transcriptions
                            self.status_updated.emit(f"⚠️ Vertaling gefaald, gebruik originele transcriptie")
                    else:
                        print(f"🔍 [DEBUG] ProcessingThread: Vertaling uitgeschakeld, gebruik originele transcriptie")
                        translated_transcriptions = transcriptions
                        self.progress_updated.emit(75.0, f"⏭️ Vertaling overgeslagen: {os.path.basename(file_path)}")
                    
                    # Check of verwerking gestopt moet worden
                    if not self.is_running:
                        self.status_updated.emit("🛑 Verwerking gestopt door gebruiker")
                        break
                    
                    # Stap 4: Video verwerking (gebruikt modulaire functie)
                    print(f"🔍 [DEBUG] ProcessingThread: Start stap 4 - Video verwerking")
                    print(f"🔍 [DEBUG] ProcessingThread: Memory check - transcriptions count: {len(transcriptions) if transcriptions else 0}")
                    
                    self.status_updated.emit(f"🎬 Start video verwerking: {os.path.basename(file_path)}")
                    self.progress_updated.emit(80.0, f"🎬 Video verwerking...")
                    
                    # Memory check
                    try:
                        import psutil
                        process = psutil.Process()
                        memory_info = process.memory_info()
                        print(f"🔍 [DEBUG] ProcessingThread: Memory gebruik: {memory_info.rss / 1024 / 1024:.1f} MB")
                    except Exception as e:
                        print(f"🔍 [DEBUG] ProcessingThread: Memory check gefaald: {e}")
                    
                    try:
                        # Geef instellingen door aan video processor
                        if hasattr(self, 'settings') and self.settings:
                            # Stel instellingen in voor video processor
                            print(f"🔍 [DEBUG] ProcessingThread: Geef instellingen door aan video processor: {self.settings}")
                            self.video_processor.set_settings(self.settings)
                        
                        video_result = self.video_processor.process_video(
                            file_path, transcript, transcriptions, translated_transcriptions
                        )
                        print(f"🔍 [DEBUG] ProcessingThread: Video verwerking voltooid")
                        
                        self.progress_updated.emit(90.0, f"✅ Video verwerking voltooid: {os.path.basename(file_path)}")
                        self.status_updated.emit(f"✅ Video verwerking voltooid: {os.path.basename(file_path)}")
                        
                    except Exception as e:
                        print(f"🔍 [DEBUG] ProcessingThread: CRASH in video_processor.process_video: {e}")
                        print(f"🔍 [DEBUG] ProcessingThread: Exception type: {type(e)}")
                        import traceback
                        print(f"🔍 [DEBUG] ProcessingThread: Traceback: {traceback.format_exc()}")
                        raise  # Re-raise de exception
                    
                    # Bepaal output pad
                    if "error" in video_result:
                        self.status_updated.emit(f"⚠️ Video verwerking gefaald: {video_result['error']}")
                        output_path = file_path
                    else:
                        output_path = file_path
                    
                    # Ruim tijdelijke bestanden op
                    try:
                        self.progress_updated.emit(95.0, f"🧹 Ruim tijdelijke bestanden op...")
                        self.status_updated.emit(f"🧹 Ruim tijdelijke bestanden op: {os.path.basename(file_path)}")
                        
                        if self.audio_processor:
                            self.audio_processor.cleanup_audio_by_video(file_path)
                        else:
                            # Fallback cleanup
                            if os.path.exists(audio_path):
                                os.remove(audio_path)
                        
                        self.progress_updated.emit(98.0, f"✅ Cleanup voltooid: {os.path.basename(file_path)}")
                        
                    except Exception as e:
                        print(f"⚠️ Kon audio bestand niet opruimen: {e}")
                        self.status_updated.emit(f"⚠️ Cleanup gefaald: {e}")
                    
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
    

    
    def set_file_list_callback(self, callback):
        """Stel een callback in om de actuele file list op te halen"""
        self._file_list_callback = callback
