import os
from PyQt6.QtCore import QThread, pyqtSignal
from magic_time_studio.processing import whisper_processor, translator, audio_processor, video_processor

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
            # Gebruik de echte bestanden uit de files lijst
            if not self.files:
                self.status_updated.emit("⚠️ Geen bestanden geselecteerd voor verwerking")
                self.processing_finished.emit()
                return
            
            # Debug informatie
            if DEBUG_MODE:
                print(f"🔍 [DEBUG] ProcessingThread.run: {len(self.files)} bestanden ontvangen")
                for i, file_path in enumerate(self.files):
                    print(f"🔍 [DEBUG] ProcessingThread.run: Bestand {i+1}: {file_path}")
            
            # Filter alleen video bestanden
            video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']
            video_files = [f for f in self.files if any(f.lower().endswith(ext) for ext in video_extensions)]
            total_files = len(video_files)
            
            if DEBUG_MODE:
                print(f"🔍 [DEBUG] ProcessingThread.run: {total_files} video bestanden gevonden")
                for i, file_path in enumerate(video_files):
                    print(f"🔍 [DEBUG] ProcessingThread.run: Video bestand {i+1}: {file_path}")
            
            if not video_files:
                self.status_updated.emit("⚠️ Geen video bestanden gevonden om te verwerken")
                self.processing_finished.emit()
                return
            
            self.status_updated.emit(f"🚀 Start verwerking van {total_files} video bestanden")
            completed = 0
            
            for i, file_path in enumerate(video_files):
                if DEBUG_MODE:
                    print(f"🔍 [DEBUG] ProcessingThread.run: Start verwerking van bestand {i+1}/{total_files}: {file_path}")
                
                if not self.is_running:
                    if DEBUG_MODE:
                        print(f"🔍 [DEBUG] ProcessingThread.run: Verwerking gestopt door gebruiker")
                    break
                    
                self.status_updated.emit(f"🎬 Start verwerking: {file_path}")
                
                # Update progress voor dit bestand - verwijder deze regel zodat alleen FFmpeg progress wordt getoond
                file_progress = (i / total_files) * 100
                progress_message = f"Bestand {i+1} van {total_files}: {os.path.basename(file_path)}"
                # self.progress_updated.emit(file_progress, progress_message)  # Verwijderd - alleen FFmpeg progress
                
                if DEBUG_MODE:
                    print(f"🔍 [DEBUG] ProcessingThread.run: Progress voor bestand {i+1}: {file_progress:.1f}%")
                
                # Log progress update
                try:
                    from magic_time_studio.core.logging import logger
                    logger.add_log_message(f"📊 {progress_message}", "INFO")
                except ImportError:
                    pass  # Stil falen als logging niet beschikbaar is
                
                # Start gedetailleerde progress tracking
                self.status_updated.emit(f"🎬 Start verwerking: {os.path.basename(file_path)}")
                
                try:
                    if DEBUG_MODE:
                        print(f"🔍 [DEBUG] ProcessingThread.run: Start audio extractie voor {file_path}")
                    
                    # Stap 1: Audio extractie
                    self.status_updated.emit(f"🎵 Audio extractie gestart: {os.path.basename(file_path)}")
                    
                    # Progress callback voor FFmpeg audio extractie
                    def audio_progress_callback(msg):
                        if "FFmpeg:" in msg:
                            # Parse FFmpeg progress uit de message
                            try:
                                # Extract percentage uit FFmpeg output (bijv. "4%|███▎| 19968/544656")
                                if "%" in msg:
                                    progress_str = msg.split("%")[0].split("|")[-1].strip()
                                    progress = float(progress_str) / 100.0
                                    # Update progressbalk met FFmpeg progress
                                    ffmpeg_progress = file_progress + (progress * 15)  # 15% van totaal voor audio
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
                        if DEBUG_MODE:
                            print(f"🔍 [DEBUG] ProcessingThread.run: Audio extractie gefaald voor {file_path}")
                        continue
                    
                    audio_path = audio_result.get("audio_path")
                    if not audio_path or not os.path.exists(audio_path):
                        self.status_updated.emit(f"❌ Audio bestand niet gevonden: {audio_path}")
                        if DEBUG_MODE:
                            print(f"🔍 [DEBUG] ProcessingThread.run: Audio bestand niet gevonden: {audio_path}")
                        continue
                    
                    # Debug informatie voor audio bestand
                    if DEBUG_MODE:
                        try:
                            from magic_time_studio.core.logging import logger
                            logger.log_debug(f"Audio bestand gevonden: {os.path.basename(audio_path)}, grootte: {os.path.getsize(audio_path)} bytes")
                        except ImportError:
                            pass  # Stil falen als logging niet beschikbaar is
                    
                    if DEBUG_MODE:
                        print(f"🔍 [DEBUG] ProcessingThread.run: Audio extractie voltooid voor {file_path}")
                    
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
                            logger.log_debug(f"Start Whisper transcriptie voor {os.path.basename(file_path)}")
                        except ImportError:
                            pass
                    
                    # Stap 2: Whisper transcriptie
                    whisper_model = self.settings.get('whisper_model', 'large')
                    self.status_updated.emit(f"🎤 Whisper transcriptie ({whisper_model}): {os.path.basename(file_path)}")
                    # Gebruik progress na audio extractie voor console
                    whisper_start_progress = (file_progress + 15) / 100.0
                    # Verwijder console output voor Whisper start
                    
                    # Initialiseer Whisper als nog niet gedaan
                    if not whisper_processor.is_initialized:
                        if not whisper_processor.initialize(whisper_model):
                            self.status_updated.emit(f"❌ Whisper initialisatie gefaald")
                            if DEBUG_MODE:
                                print(f"🔍 [DEBUG] ProcessingThread.run: Whisper initialisatie gefaald")
                            continue
                    
                    # Check of verwerking gestopt moet worden
                    if not self.is_running:
                        self.status_updated.emit("🛑 Verwerking gestopt door gebruiker")
                        if DEBUG_MODE:
                            print(f"🔍 [DEBUG] ProcessingThread.run: Verwerking gestopt voor Whisper")
                        break
                    
                    # Whisper progress callback functie
                    def whisper_progress_callback(progress_bar):
                        # Parse progress uit de voortgangsbalk string
                        try:
                            # Extract percentage uit voortgangsbalk (bijv. "50%|████████████████████░░░░░░░░░░░░| filename")
                            if "%" in progress_bar:
                                progress_str = progress_bar.split("%")[0].strip()
                                progress = float(progress_str) / 100.0
                            else:
                                progress = 0.5  # Fallback
                        except:
                            progress = 0.5  # Fallback
                        
                        # Update progress voor Whisper (15-65% van totaal)
                        whisper_progress = file_progress + 15 + (progress * 50)
                        progress_text = f"🎤 Whisper: {progress:.1%} - {os.path.basename(file_path)}"
                        # Verwijder progress update - alleen console output
                        
                        # Alleen status update bij start (0%) en voltooiing (100%)
                        if progress <= 0.01:  # Start
                            self.status_updated.emit(f"🎤 Whisper transcriptie gestart: {os.path.basename(file_path)}")
                        elif progress >= 0.99:  # Voltooid
                            self.status_updated.emit(f"✅ Whisper transcriptie voltooid: {os.path.basename(file_path)}")
                        
                        # Console output voor Whisper progress
                        console_progress = (file_progress + 15 + (progress * 50)) / 100.0
                        # Alleen voortgangsbalk tonen, geen andere berichten
                        self.status_updated.emit(f"CONSOLE_OUTPUT:🎤 {progress_bar}")
                        
                        # Check of verwerking gestopt moet worden
                        if not self.is_running:
                            return False  # Stop Whisper processing
                        return True  # Ga door met processing
                    
                    # Whisper stop callback functie
                    def whisper_stop_callback():
                        if DEBUG_MODE:
                            print(f"🔍 [DEBUG] ProcessingThread.run: Whisper stop callback aangeroepen voor {file_path}")
                        return not self.is_running
                    
                    # Voer Whisper transcriptie uit
                    transcript_result = whisper_processor.transcribe_audio(
                        audio_path, 
                        progress_callback=whisper_progress_callback,
                        stop_callback=whisper_stop_callback
                    )
                    
                    # Debug informatie
                    if DEBUG_MODE:
                        try:
                            from magic_time_studio.core.logging import logger
                            logger.log_debug(f"Whisper result voor {os.path.basename(file_path)}: Keys={list(transcript_result.keys())}, Success={transcript_result.get('success', False)}, Transcript length={len(transcript_result.get('transcript', ''))}")
                        except ImportError:
                            pass  # Stil falen als logging niet beschikbaar is
                    
                    if "error" in transcript_result:
                        self.status_updated.emit(f"❌ Whisper transcriptie gefaald: {transcript_result['error']}")
                        if DEBUG_MODE:
                            print(f"🔍 [DEBUG] ProcessingThread.run: Whisper transcriptie gefaald voor {file_path}")
                        continue
                    
                    # Check voor transcript
                    transcript = transcript_result.get("transcript", "")
                    transcriptions = transcript_result.get("transcriptions", [])
                    if not transcript:
                        self.status_updated.emit(f"⚠️ Geen transcriptie gegenereerd voor {file_path}")
                        if DEBUG_MODE:
                            print(f"🔍 [DEBUG] ProcessingThread.run: Geen transcriptie gegenereerd voor {file_path}")
                        if DEBUG_MODE:
                            print(f"🔍 [DEBUG] ProcessingThread.run: transcript_result keys: {list(transcript_result.keys())}")
                        if DEBUG_MODE:
                            print(f"🔍 [DEBUG] ProcessingThread.run: transcript_result: {transcript_result}")
                        
                        # Maak een placeholder transcriptie voor bestanden zonder spraak
                        transcript = "[Geen spraak gedetecteerd in deze video]"
                        self.status_updated.emit(f"ℹ️ Placeholder transcriptie gemaakt voor {file_path}")
                        if DEBUG_MODE:
                            print(f"🔍 [DEBUG] ProcessingThread.run: Placeholder transcriptie gemaakt: {transcript}")
                        
                        # Maak ook placeholder transcriptions
                        transcriptions = [{
                            "start": 0.0,
                            "end": 10.0,
                            "text": transcript,
                            "language": "en"
                        }]
                    
                    if DEBUG_MODE:
                        print(f"🔍 [DEBUG] ProcessingThread.run: Whisper transcriptie voltooid voor {file_path}")
                    
                    # Check of verwerking gestopt moet worden
                    if not self.is_running:
                        self.status_updated.emit("🛑 Verwerking gestopt door gebruiker")
                        if DEBUG_MODE:
                            print(f"🔍 [DEBUG] ProcessingThread.run: Verwerking gestopt na Whisper")
                        break
                    
                    # Update progress na transcriptie
                    self.progress_updated.emit(file_progress + 65, f"🌐 Vertaling: {os.path.basename(file_path)}")
                    
                    # Stap 3: Vertaling (als ingesteld)
                    translated_transcriptions = None
                    if self.settings.get('enable_translation', False):
                        if DEBUG_MODE:
                            print(f"🔍 [DEBUG] ProcessingThread.run: Start vertaling voor {file_path}")
                        self.status_updated.emit(f"🌐 Vertaling gestart: {os.path.basename(file_path)}")
                        # Gebruik progress na transcriptie voor console
                        translation_start_progress = (file_progress + 65) / 100.0
                        # Verwijder console output voor vertaling
                        
                        # Vertaal transcriptie
                        target_language = self.settings.get('target_language', 'nl')
                        source_language = transcript_result.get("language", "en")
                        
                        translation_result = translator.translate_text(
                            transcript, 
                            source_language, 
                            target_language
                        )
                        
                        if translation_result and "error" not in translation_result:
                            transcript = translation_result.get("translated_text", transcript)
                            self.status_updated.emit(f"✅ Vertaling voltooid: {source_language} -> {target_language}")
                            if DEBUG_MODE:
                                print(f"🔍 [DEBUG] ProcessingThread.run: Vertaling voltooid voor {file_path}")
                        else:
                            error_msg = translation_result.get("error", "Onbekende fout") if translation_result else "Geen resultaat"
                            self.status_updated.emit(f"⚠️ Vertaling gefaald: {error_msg}")
                            if DEBUG_MODE:
                                print(f"🔍 [DEBUG] ProcessingThread.run: Vertaling gefaald voor {file_path}: {error_msg}")
                            # Gebruik originele transcriptie als fallback
                        
                        # Check of verwerking gestopt moet worden
                        if not self.is_running:
                            self.status_updated.emit("🛑 Verwerking gestopt door gebruiker")
                            if DEBUG_MODE:
                                print(f"🔍 [DEBUG] ProcessingThread.run: Verwerking gestopt na vertaling")
                            break
                    
                    # Stap 4: Video verwerking (hardcoded ondertitels)
                    if self.settings.get('subtitle_type') == 'hardcoded':
                        if DEBUG_MODE:
                            print(f"🔍 [DEBUG] ProcessingThread.run: Start hardcoded video verwerking voor {file_path}")
                        
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
                                        # Update progressbalk met FFmpeg progress
                                        ffmpeg_progress = file_progress + 75 + (progress * 25)  # 25% van totaal voor video
                                        progress_text = f"🎬 FFmpeg: {progress:.1%} - {os.path.basename(file_path)}"
                                        self.progress_updated.emit(ffmpeg_progress, progress_text)
                                except:
                                    pass  # Stil falen als parsing niet lukt
                                # Console output
                                self.status_updated.emit(f"CONSOLE_OUTPUT:{msg}")
                        
                        video_result = video_processor.add_subtitles_to_video(
                            file_path,
                            transcript,
                            progress_callback=video_progress_wrapper
                        )
                        
                        if video_result.get("success"):
                            self.status_updated.emit(f"✅ Video verwerking voltooid: {os.path.basename(file_path)}")
                        else:
                            self.status_updated.emit(f"⚠️ Video verwerking gefaald: {video_result.get('error', 'Onbekende fout')}")
                    else:
                        # Softcoded ondertitels - genereer alleen SRT bestanden
                        if DEBUG_MODE:
                            print(f"🔍 [DEBUG] ProcessingThread.run: Start SRT bestanden genereren voor {file_path}")
                        
                        self.status_updated.emit(f"📄 SRT bestanden genereren: {os.path.basename(file_path)}")
                        
                        video_result = video_processor.generate_srt_files(
                            file_path,
                            transcriptions,
                            translated_transcriptions if self.settings.get('enable_translation', False) else None
                        )
                        
                        if video_result.get("success"):
                            self.status_updated.emit(f"✅ SRT bestanden gegenereerd: {os.path.basename(file_path)}")
                        else:
                            self.status_updated.emit(f"⚠️ SRT generatie gefaald: {video_result.get('error', 'Onbekende fout')}")
                    
                    # Bepaal output pad
                    if "error" in video_result:
                        self.status_updated.emit(f"⚠️ Video verwerking gefaald: {video_result['error']}")
                        if DEBUG_MODE:
                            print(f"🔍 [DEBUG] ProcessingThread.run: Video verwerking gefaald voor {file_path}")
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
                                if DEBUG_MODE:
                                    print(f"🔍 [DEBUG] ProcessingThread.run: {file_type.upper()} bestand gegenereerd: {file_path_srt}")
                    
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
                    
                    completed += 1
                    self.status_updated.emit(f"✅ {file_path} voltooid")
                    if DEBUG_MODE:
                        print(f"🔍 [DEBUG] ProcessingThread.run: Bestand {i+1}/{total_files} voltooid: {file_path}")
                    # Gebruik voltooide progress voor console
                    completed_progress = (file_progress + 100) / 100.0
                    # Verwijder console output voor voltooiing
                    
                    # Voeg toe aan completed files via signal
                    completed_signal = f"COMPLETED_FILE:{file_path}:{output_path}"
                    if DEBUG_MODE:
                        print(f"🔍 [DEBUG] Signal uitgezonden: {completed_signal}")
                    self.status_updated.emit(completed_signal)
                    
                    # Emit ook een direct signal om het bestand uit de "nog te doen" lijst te verwijderen
                    self.status_updated.emit(f"FILE_COMPLETED_REMOVE:{file_path}")
                    
                except Exception as e:
                    self.status_updated.emit(f"❌ Fout bij verwerken {file_path}: {str(e)}")
                    if DEBUG_MODE:
                        print(f"🔍 [DEBUG] ProcessingThread.run: Fout bij verwerken {file_path}: {str(e)}")
                    continue
            
            if DEBUG_MODE:
                print(f"🔍 [DEBUG] ProcessingThread.run: Loop voltooid. Completed: {completed}/{total_files}")
            
            if self.is_running:
                self.progress_updated.emit(100.0, "Verwerking voltooid!")
                self.processing_finished.emit()
                if DEBUG_MODE:
                    print(f"🔍 [DEBUG] ProcessingThread.run: Verwerking voltooid!")
            else:
                if DEBUG_MODE:
                    print(f"🔍 [DEBUG] ProcessingThread.run: Verwerking gestopt door gebruiker")
                
        except Exception as e:
            if DEBUG_MODE:
                print(f"🔍 [DEBUG] ProcessingThread.run: Kritieke fout: {str(e)}")
            self.error_occurred.emit(str(e))
    
    def stop(self):
        """Stop de verwerking"""
        if DEBUG_MODE:
            print("🛑 ProcessingThread.stop() aangeroepen - zet is_running = False")
        self.is_running = False
        if DEBUG_MODE:
            print("✅ ProcessingThread gestopt - is_running = False")

    def set_file_list_callback(self, callback):
        """Stel een callback in om de actuele file list op te halen"""
        self._file_list_callback = callback