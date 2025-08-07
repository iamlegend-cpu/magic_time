import os
from PyQt6.QtCore import QThread, pyqtSignal
from magic_time_studio.processing import translator, audio_processor, video_processor
from magic_time_studio.processing.whisper_manager import whisper_manager

# Debug mode - zet op False om debug output uit te zetten
DEBUG_MODE = False

class ProcessingThread(QThread):
    """Thread voor verwerking van bestanden"""
    progress_updated = pyqtSignal(float, str)
    status_updated = pyqtSignal(str)
    processing_finished = pyqtSignal()
    error_occurred = pyqtSignal(str)
    
    def __init__(self, files, settings):
        super().__init__()
        self.files = files
        self.settings = settings
        self.is_running = True
    
    def run(self):
        """Voer verwerking uit in aparte thread"""
        try:
            # Debug test - controleer of debug output werkt
            # if DEBUG_MODE:
            #     print("🔍 [DEBUG] ProcessingThread.run: DEBUG_MODE is actief!")
                
            
            # Gebruik de echte bestanden uit de files lijst
            if not self.files:
                self.status_updated.emit("⚠️ Geen bestanden geselecteerd voor verwerking")
                self.processing_finished.emit()
                return
            
            # Debug informatie
            # if DEBUG_MODE:
            #     print(f"🔍 [DEBUG] ProcessingThread.run: {len(self.files)} bestanden ontvangen")
            #     for i, file_path in enumerate(self.files):
            #         print(f"🔍 [DEBUG] ProcessingThread.run: Bestand {i+1}: {file_path}")
                    
            
            # Filter alleen video bestanden
            video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']
            video_files = [f for f in self.files if any(f.lower().endswith(ext) for ext in video_extensions)]
            total_files = len(video_files)
            
            # if DEBUG_MODE:
            #     print(f"🔍 [DEBUG] ProcessingThread.run: {total_files} video bestanden gevonden")
            #     for i, file_path in enumerate(video_files):
            #         print(f"🔍 [DEBUG] ProcessingThread.run: Video bestand {i+1}: {file_path}")
                    
            
            if not video_files:
                self.status_updated.emit("⚠️ Geen video bestanden gevonden om te verwerken")
                self.processing_finished.emit()
                return
            
            self.status_updated.emit(f"🚀 Start verwerking van {total_files} video bestanden")
            completed = 0
            
            for i, file_path in enumerate(video_files):
                # if DEBUG_MODE:
                #     print(f"🔍 [DEBUG] ProcessingThread.run: Start verwerking van bestand {i+1}/{total_files}: {file_path}")
                
                if not self.is_running:
                    # if DEBUG_MODE:
                    #     print(f"🔍 [DEBUG] ProcessingThread.run: Verwerking gestopt door gebruiker")
                    break
                    
                self.status_updated.emit(f"🎬 Start verwerking: {file_path}")
                
                # Update progress voor dit bestand - gebruik percentage van totaal verwerking
                # Voor elk bestand: 0-100% van de totale verwerking
                file_progress = (i / total_files) * 100
                progress_message = f"Bestand {i+1} van {total_files}: {os.path.basename(file_path)}"
                
                # Reset progress bar voor nieuw bestand
                # if DEBUG_MODE:
                #     print(f"🔍 [DEBUG] Reset progress bar voor nieuw bestand: {os.path.basename(file_path)}")
                self.progress_updated.emit(0.0, f"🎬 Start verwerking: {os.path.basename(file_path)}")
                
                # if DEBUG_MODE:
                #     print(f"🔍 [DEBUG] ProcessingThread.run: Progress voor bestand {i+1}: {file_progress:.1f}%")
                
                # Log progress update
                try:
                    from magic_time_studio.core.logging import logger
                    logger.add_log_message(f"📊 {progress_message}", "INFO")
                except ImportError:
                    pass  # Stil falen als logging niet beschikbaar is
                
                # Start gedetailleerde progress tracking
                self.status_updated.emit(f"🎬 Start verwerking: {os.path.basename(file_path)}")
                
                try:
                    # if DEBUG_MODE:
                    #     print(f"🔍 [DEBUG] ProcessingThread.run: Start audio extractie voor {file_path}")
                    
                    # Stap 1: Audio extractie
                    self.status_updated.emit(f"🎵 Audio extractie gestart: {os.path.basename(file_path)}")
                    # if DEBUG_MODE:
                    #     print(f"🔍 [DEBUG] Audio extractie gestart: {os.path.basename(file_path)}")
                    
                    # Progress callback voor FFmpeg audio extractie
                    def audio_progress_callback(msg):
                        if "FFmpeg:" in msg:
                            # Parse FFmpeg progress uit de message
                            try:
                                # Extract percentage uit FFmpeg output (bijv. "4%|███▎| 19968/544656")
                                if "%" in msg:
                                    progress_str = msg.split("%")[0].split("|")[-1].strip()
                                    progress = float(progress_str) / 100.0
                                    # Update progressbalk met FFmpeg progress (0-15% van totaal)
                                    ffmpeg_progress = progress * 15  # 0-15% voor audio extractie
                                    progress_text = f"🎵 FFmpeg: {progress:.1%} - {os.path.basename(file_path)}"
                                    
                                    self.progress_updated.emit(ffmpeg_progress, progress_text)
                            except:
                                pass  # Stil falen als parsing niet lukt
                            # Console output
                            self.status_updated.emit(f"CONSOLE_OUTPUT:{msg}")
                    
                    audio_result = audio_processor.extract_audio_from_video(
                        file_path, 
                        progress_callback=audio_progress_callback
                    )
                    if "error" in audio_result:
                        self.status_updated.emit(f"❌ Audio extractie gefaald: {audio_result['error']}")
                        # if DEBUG_MODE:
#     print(f"🔍 [DEBUG] ProcessingThread.run: Audio extractie gefaald voor {file_path}")
                        continue
                    
                    audio_path = audio_result.get("audio_path")
                    if not audio_path or not os.path.exists(audio_path):
                        self.status_updated.emit(f"❌ Audio bestand niet gevonden: {audio_path}")
                        # if DEBUG_MODE:
#     print(f"🔍 [DEBUG] ProcessingThread.run: Audio bestand niet gevonden: {audio_path}")
                        continue
                    
                    # Debug informatie voor audio bestand
                    if DEBUG_MODE:
                        try:
                            from magic_time_studio.core.logging import logger
                            logger.log_debug(f"Audio bestand gevonden: {os.path.basename(audio_path)}, grootte: {os.path.getsize(audio_path)} bytes")
                        except ImportError:
                            pass  # Stil falen als logging niet beschikbaar is
                    
                    # if DEBUG_MODE:
#     pass
                    self.status_updated.emit(f"✅ Audio extractie voltooid: {os.path.basename(file_path)}")
                    
                    # Check of verwerking gestopt moet worden
                    if not self.is_running:
                        self.status_updated.emit("🛑 Verwerking gestopt door gebruiker")
                        if DEBUG_MODE:
                            try:
                                from magic_time_studio.core.logging import logger
                                logger.log_debug("Verwerking gestopt na audio extractie")
                            except ImportError:
                                pass
                        break
                    
                    # Update progress na audio extractie
                    
                    if DEBUG_MODE:
                        try:
                            from magic_time_studio.core.logging import logger
                            logger.log_debug(f"Start Fast Whisper transcriptie voor {os.path.basename(file_path)}")
                        except ImportError:
                            pass
                    
                    # Stap 2: Fast Whisper transcriptie
                    whisper_type = self.settings.get('whisper_type', 'fast')
                    whisper_model = self.settings.get('whisper_model', 'large-v3-turbo')
                    self.status_updated.emit(f"🎤 Fast Whisper transcriptie ({whisper_type} {whisper_model}): {os.path.basename(file_path)}")
                    
                    # Gebruik progress na audio extractie voor console
                    whisper_start_progress = (file_progress + 15) / 100.0
                    # Verwijder console output voor Fast Whisper start
                    
                    # Initialiseer Fast Whisper als nog niet gedaan
                    if not whisper_manager.is_model_loaded():
                        if not whisper_manager.initialize(whisper_type, whisper_model):
                            self.status_updated.emit(f"❌ Fast Whisper initialisatie gefaald")
                            # if DEBUG_MODE:
#     pass
                            continue
                    
                    # Check of verwerking gestopt moet worden
                    if not self.is_running:
                        self.status_updated.emit("🛑 Verwerking gestopt door gebruiker")
                        # if DEBUG_MODE:
#     pass
                        break
                    
                    # Fast Whisper progress callback functie
                    def whisper_progress_callback(progress_bar):
                        # Parse progress uit de voortgangsbalk string
                        try:
                            # Zoek naar percentage in de progress bar string
                            if isinstance(progress_bar, str):
                                # Probeer percentage te extraheren uit string zoals "50.0%"
                                import re
                                match = re.search(r'(\d+(?:\.\d+)?)%', progress_bar)
                                if match:
                                    progress = float(match.group(1)) / 100.0
                                else:
                                    progress = 0.5  # Fallback
                            else:
                                progress = float(progress_bar)
                        except (ValueError, TypeError):
                            progress = 0.5  # Fallback
                        
                        # Update progress voor Fast Whisper (15-65% van totaal)
                        whisper_progress = 15 + (progress * 50)  # 15-65% voor Fast Whisper transcriptie
                        progress_text = f"🎤 Fast Whisper: {progress:.1%} - {os.path.basename(file_path)}"
                        
                        # Update GUI progress bar (zonder debug output)
                        self.progress_updated.emit(whisper_progress, progress_text)
                        
                        # Alleen status update bij start (0%) en voltooiing (100%)
                        if progress <= 0.01:  # Start
                            self.status_updated.emit(f"🎤 Fast Whisper transcriptie gestart: {os.path.basename(file_path)}")
                        elif progress >= 0.99:  # Voltooid
                            self.status_updated.emit(f"✅ Fast Whisper transcriptie voltooid: {os.path.basename(file_path)}")
                        
                        # Console output voor Fast Whisper progress
                        console_progress = (15 + (progress * 50)) / 100.0
                        # Alleen voortgangsbalk tonen, geen andere berichten
                        self.status_updated.emit(f"CONSOLE_OUTPUT:🎤 {progress_bar}")
                        
                        # Check of verwerking gestopt moet worden
                        if not self.is_running:
                            return False  # Stop Fast Whisper processing
                        return True  # Ga door met processing
                    
                    # Fast Whisper stop callback functie
                    def whisper_stop_callback():
                        # Alleen loggen als er daadwerkelijk een stop wordt gevraagd
                        if not self.is_running:
                            # if DEBUG_MODE:
#     pass
                            return True
                        return False
                    
                    # Voer Fast Whisper transcriptie uit
                    transcript_result = whisper_manager.transcribe_audio(
                        audio_path, 
                        progress_callback=whisper_progress_callback,
                        stop_callback=whisper_stop_callback
                    )
                    
                    # Eenvoudige debug output direct na transcriptie
                    
                    
                    
                    
                    
                    # Check of transcript_result geldig is
                    if not transcript_result:
                        
                        self.status_updated.emit(f"❌ Fast Whisper transcriptie gefaald: Geen resultaat")
                        continue
                    
                    if not isinstance(transcript_result, dict):
                        
                        self.status_updated.emit(f"❌ Fast Whisper transcriptie gefaald: Ongeldig resultaat")
                        continue
                    
                    # Extra debug output om te zien wat er gebeurt
                    
                    
                    # Extra debug output om te zien wat er gebeurt
                    
                    
                    # Debug informatie
                    if transcript_result and "error" not in transcript_result:
                        transcript = transcript_result.get("transcript", "")
                        transcriptions = transcript_result.get("transcriptions", [])
                        
                        
                        
                        
                        
                        # Test vertaling sectie
                        
                        enable_translation = self.settings.get("enable_translation", False)
                        
                        
                        if enable_translation:
                            
                            # Vertaal transcripties
                            translated_transcriptions = []
                            for segment in transcriptions:
                                try:
                                    translated_text = self.translator.translate_text(segment["text"], "nl")
                                    translated_segment = segment.copy()
                                    translated_segment["text"] = translated_text
                                    translated_transcriptions.append(translated_segment)
                                except Exception as e:
                                    
                                    translated_transcriptions.append(segment)
                            
                            
                        else:
                            
                            translated_transcriptions = transcriptions
                        
                        # Test video verwerking sectie
                        
                        
                        
                        # Video verwerking
                        if self.settings.get("subtitle_type") == "softcoded":
                            
                            video_result = video_processor.generate_srt_files(
                                file_path,
                                transcriptions,
                                translated_transcriptions if enable_translation else None,
                                self.settings
                            )
                            
                            
                            if "error" in video_result:
                                
                                error_message = f"SRT generatie gefaald: {video_result['error']}"
                                self.progress_updated.emit(0, f"❌ {error_message}")
                                return
                            else:
                                
                        else:
                            
                        
                        
                    else:
                        
                        if transcript_result and "error" in transcript_result:
                            error_message = f"Fast Whisper transcriptie gefaald: {transcript_result['error']}"
                            
                            self.progress_updated.emit(0, f"❌ {error_message}")
                            return
                    
                    # Debug informatie
                    if DEBUG_MODE:
                        try:
                            from magic_time_studio.core.logging import logger
                            logger.log_debug(f"Fast Whisper result voor {os.path.basename(file_path)}: Keys={list(transcript_result.keys())}, Success={transcript_result.get('success', False)}, Transcript length={len(transcript_result.get('transcript', ''))}")
                        except ImportError:
                            pass  # Stil falen als logging niet beschikbaar is
                    
                    if "error" in transcript_result:
                        self.status_updated.emit(f"❌ Fast Whisper transcriptie gefaald: {transcript_result['error']}")
                        # if DEBUG_MODE:
#     print(f"🔍 [DEBUG] ProcessingThread.run: Fast Whisper transcriptie gefaald voor {file_path}")
                        continue
                    
                    # Check voor transcript
                    transcript = transcript_result.get("transcript", "")
                    transcriptions = transcript_result.get("transcriptions", [])
                    if not transcript:
                        self.status_updated.emit(f"⚠️ Geen transcriptie gegenereerd voor {file_path}")
                        # if DEBUG_MODE:
#     pass
                        # if DEBUG_MODE:
#     pass
                        # if DEBUG_MODE:
#     pass
                        # Maak een placeholder transcriptie voor bestanden zonder spraak
                        transcript = "[Geen spraak gedetecteerd in deze video]"
                        self.status_updated.emit(f"ℹ️ Placeholder transcriptie gemaakt voor {file_path}")
                        # if DEBUG_MODE:
#     pass
                        # Maak ook placeholder transcriptions
                        transcriptions = [{
                            "start": 0.0,
                            "end": 10.0,
                            "text": transcript,
                            "language": "en"
                        }]
                    
                    # if DEBUG_MODE:
#     pass
                        if transcriptions:
                            
                        
                        
                    
                    # Check of verwerking gestopt moet worden
                    if not self.is_running:
                        self.status_updated.emit("🛑 Verwerking gestopt door gebruiker")
                        # if DEBUG_MODE:
#     pass
                        break
                    
                    # if DEBUG_MODE:
#     pass
                    # Update progress na transcriptie
                    self.progress_updated.emit(file_progress + 65, f"🌐 Vertaling: {os.path.basename(file_path)}")
                    
                    # if DEBUG_MODE:
#     pass
                    # Stap 3: Vertaling (als ingesteld)
                    translated_transcriptions = None
                    if self.settings.get('enable_translation', False):
                        # if DEBUG_MODE:
#     pass
                        self.status_updated.emit(f"🌐 Vertaling gestart: {os.path.basename(file_path)}")
                        # Gebruik progress na transcriptie voor console
                        translation_start_progress = (file_progress + 65) / 100.0
                        # Verwijder console output voor vertaling
                        
                        # Vertaal transcriptie
                        target_language = self.settings.get('target_language', 'nl')
                        source_language = transcript_result.get("language", "en")
                        
                        # if DEBUG_MODE:
#     pass
                        # Vertaal de transcript tekst
                        translation_result = translator.translate_text(
                            transcript, 
                            source_language, 
                            target_language
                        )
                        
                        # if DEBUG_MODE:
#     pass
                        if translation_result and "error" not in translation_result:
                            transcript = translation_result.get("translated_text", transcript)
                            self.status_updated.emit(f"✅ Vertaling voltooid: {source_language} -> {target_language}")
                            # if DEBUG_MODE:
#     pass
                            # Vertaal ook de transcriptions lijst voor SRT generatie
                            if transcriptions:
                                # if DEBUG_MODE:
#     pass
                                translated_transcriptions = []
                                for segment in transcriptions:
                                    # Vertaal de tekst van elk segment
                                    segment_translation = translator.translate_text(
                                        segment["text"],
                                        source_language,
                                        target_language
                                    )
                                    
                                    if segment_translation and "error" not in segment_translation:
                                        translated_segment = segment.copy()
                                        translated_segment["text"] = segment_translation.get("translated_text", segment["text"])
                                        translated_segment["translated_text"] = segment_translation.get("translated_text", segment["text"])
                                        translated_transcriptions.append(translated_segment)
                                    else:
                                        # Fallback naar origineel segment als vertaling faalt
                                        translated_segment = segment.copy()
                                        translated_segment["translated_text"] = segment["text"]
                                        translated_transcriptions.append(translated_segment)
                                
                                # if DEBUG_MODE:
#     pass
                        else:
                            error_msg = translation_result.get("error", "Onbekende fout") if translation_result else "Geen resultaat"
                            self.status_updated.emit(f"⚠️ Vertaling gefaald: {error_msg}")
                            # if DEBUG_MODE:
#     print(f"🔍 [DEBUG] ProcessingThread.run: Vertaling gefaald voor {file_path}: {error_msg}")
                            # Gebruik originele transcriptie als fallback
                            translated_transcriptions = transcriptions
                        
                        # Check of verwerking gestopt moet worden
                        if not self.is_running:
                            self.status_updated.emit("🛑 Verwerking gestopt door gebruiker")
                            # if DEBUG_MODE:
#     pass
                            break
                    else:
                        # if DEBUG_MODE:
#     pass
                        # Geen vertaling - gebruik originele transcriptions
                        translated_transcriptions = transcriptions
                    
                    # if DEBUG_MODE:
#     pass
                    # Stap 4: Video verwerking (hardcoded ondertitels)
                    if self.settings.get('subtitle_type') == 'hardcoded':
                        # if DEBUG_MODE:
#     pass
                        self.status_updated.emit(f"🎬 Video verwerking gestart: {os.path.basename(file_path)}")
                        
                        # Maak een wrapper voor de progress callback
                        def video_progress_wrapper(msg):
                            # Alleen FFmpeg progress bars tonen
                            if "FFmpeg:" in msg:
                                # Parse FFmpeg progress uit de message
                                try:
                                    # Extract percentage uit FFmpeg output (bijv. "4%|███▎| 19968/544656")
                                    if "%" in msg:
                                        progress_str = msg.split("%")[0].split("|")[-1].strip()
                                        progress = float(progress_str) / 100.0
                                        # Update progressbalk met FFmpeg progress (65-100% van totaal)
                                        ffmpeg_progress = 65 + (progress * 35)  # 65-100% voor video verwerking
                                        progress_text = f"🎬 FFmpeg: {progress:.1%} - {os.path.basename(file_path)}"
                                        
                                        self.progress_updated.emit(ffmpeg_progress, progress_text)
                                except:
                                    pass  # Stil falen als parsing niet lukt
                                # Console output
                                self.status_updated.emit(f"CONSOLE_OUTPUT:{msg}")
                        
                        video_result = video_processor.add_subtitles_to_video(
                            file_path,
                            transcript,
                            progress_callback=video_progress_wrapper,
                            settings=self.settings
                        )
                        
                        if video_result.get("success"):
                            self.status_updated.emit(f"✅ Video verwerking voltooid: {os.path.basename(file_path)}")
                        else:
                            self.status_updated.emit(f"⚠️ Video verwerking gefaald: {video_result.get('error', 'Onbekende fout')}")
                    else:
                        # Softcoded ondertitels - genereer alleen SRT bestanden
                        # if DEBUG_MODE:
#     pass
                        self.status_updated.emit(f"📄 SRT bestanden genereren: {os.path.basename(file_path)}")
                        
                        # if DEBUG_MODE:
#     pass
                        video_result = video_processor.generate_srt_files(
                            file_path,
                            transcriptions,
                            translated_transcriptions if self.settings.get('enable_translation', False) else None,
                            self.settings
                        )
                        
                        # if DEBUG_MODE:
#     pass
                        if video_result.get("success"):
                            self.status_updated.emit(f"✅ SRT bestanden gegenereerd: {os.path.basename(file_path)}")
                            # if DEBUG_MODE:
#     pass
                                if "output_files" in video_result:
                                    
                        else:
                            self.status_updated.emit(f"⚠️ SRT generatie gefaald: {video_result.get('error', 'Onbekende fout')}")
                            # if DEBUG_MODE:
#     pass
                    # if DEBUG_MODE:
#     pass
                    # Bepaal output pad
                    if "error" in video_result:
                        self.status_updated.emit(f"⚠️ Video verwerking gefaald: {video_result['error']}")
                        # if DEBUG_MODE:
#     print(f"🔍 [DEBUG] ProcessingThread.run: Video verwerking gefaald voor {file_path}")
                        # Gebruik origineel bestand als output
                        output_path = file_path
                    else:
                        # Process_video retourneert geen output_path, gebruik origineel bestand
                        output_path = file_path
                        
                        # Log de gegenereerde SRT bestanden
                        if "output_files" in video_result:
                            output_files = video_result["output_files"]
                            for file_type, file_path_srt in output_files.items():
                                self.status_updated.emit(f"📄 {file_type.upper()} bestand gegenereerd: {os.path.basename(file_path_srt)}")
                                # if DEBUG_MODE:
#     pass
                    # if DEBUG_MODE:
#     pass
                    # Ruim tijdelijke bestanden op
                    try:
                        if os.path.exists(audio_path):
                            os.remove(audio_path)
                            if DEBUG_MODE:
                                try:
                                    from magic_time_studio.core.logging import logger
                                    logger.log_debug(f"🗑️ Tijdelijk audio bestand verwijderd: {audio_path}")
                                except ImportError:
                                    pass
                    except Exception as e:
                        if DEBUG_MODE:
                            try:
                                from magic_time_studio.core.logging import logger
                                logger.log_debug(f"⚠️ Kon tijdelijk audio bestand niet verwijderen: {e}")
                            except ImportError:
                                pass
                    
                    # if DEBUG_MODE:
#     pass
                    completed += 1
                    self.status_updated.emit(f"✅ {file_path} voltooid")
                    # if DEBUG_MODE:
#     pass
                    # Gebruik voltooide progress voor console
                    completed_progress = (file_progress + 100) / 100.0
                    # Verwijder console output voor voltooiing
                    
                    # Voeg toe aan completed files via signal
                    completed_signal = f"COMPLETED_FILE:{file_path}:{output_path}"
                    # if DEBUG_MODE:
#     pass
                    self.status_updated.emit(completed_signal)
                    
                    # Emit ook een direct signal om het bestand uit de "nog te doen" lijst te verwijderen
                    self.status_updated.emit(f"FILE_COMPLETED_REMOVE:{file_path}")
                    
                    # Update progress naar 100% voor dit bestand
                    self.progress_updated.emit(100.0, f"✅ {os.path.basename(file_path)} voltooid")
                    
                    # if DEBUG_MODE:
#     pass
                except Exception as e:
                    self.status_updated.emit(f"❌ Fout bij verwerken {file_path}: {str(e)}")
                    # if DEBUG_MODE:
#     print(f"🔍 [DEBUG] ProcessingThread.run: Fout bij verwerken {file_path}: {str(e)}")
                        import traceback
                        traceback.print_exc()
                    continue
            
            # if DEBUG_MODE:
#     pass
            if self.is_running:
                self.progress_updated.emit(100.0, "Verwerking voltooid!")
                self.processing_finished.emit()
                # if DEBUG_MODE:
#     pass
            else:
                # if DEBUG_MODE:
#     pass
        except Exception as e:
            # if DEBUG_MODE:
#     print(f"🔍 [DEBUG] ProcessingThread.run: Kritieke fout: {str(e)}")
            self.error_occurred.emit(str(e))
        finally:
            # Zorg ervoor dat de verwerking altijd als voltooid wordt gemarkeerd
            # if DEBUG_MODE:
#     print(f"🔍 [DEBUG] ProcessingThread.run: Finally block - markeer verwerking als voltooid")
            self.progress_updated.emit(100.0, "Verwerking voltooid!")
            self.processing_finished.emit()
    
    def stop(self):
        """Stop de verwerking"""
        # if DEBUG_MODE:
#     print("🛑 ProcessingThread.stop() aangeroepen - zet is_running = False")
        self.is_running = False
        
        # Wacht tot de thread stopt
        if self.isRunning():
            # if DEBUG_MODE:
#     print("🛑 ProcessingThread.stop() - wacht tot thread stopt...")
            self.wait(5000)  # Wacht maximaal 5 seconden
        
        # if DEBUG_MODE:
#     print("✅ ProcessingThread gestopt - is_running = False")

    def set_file_list_callback(self, callback):
        """Stel een callback in om de actuele file list op te halen"""
        self._file_list_callback = callback