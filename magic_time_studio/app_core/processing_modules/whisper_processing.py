"""
Whisper processing module voor Magic Time Studio
"""

import os
import re
from magic_time_studio.processing.whisper_manager import whisper_manager

class WhisperProcessor:
    """Whisper processing functionaliteit"""
    
    def __init__(self, processing_thread):
        self.thread = processing_thread
        self.settings = processing_thread.settings
    
    def transcribe_audio(self, audio_path, file_path):
        """Transcribe audio met Fast Whisper"""
        whisper_type = self.settings.get('whisper_type', 'fast')
        whisper_model = self.settings.get('whisper_model', 'large-v3-turbo')
        self.thread.status_updated.emit(f"🎤 Fast Whisper transcriptie ({whisper_type} {whisper_model}): {os.path.basename(file_path)}")
        
        # Initialiseer Fast Whisper als nog niet gedaan
        if not whisper_manager.is_model_loaded():
            if not whisper_manager.initialize(whisper_type, whisper_model):
                self.thread.status_updated.emit(f"❌ Fast Whisper initialisatie gefaald")
                return None
        
        # Fast Whisper progress callback functie
        def whisper_progress_callback(progress_bar):
            # Parse progress uit de voortgangsbalk string
            try:
                # Zoek naar percentage in de progress bar string
                if isinstance(progress_bar, str):
                    # Probeer percentage te extraheren uit string zoals "50.0%"
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
            self.thread.progress_updated.emit(whisper_progress, progress_text)
            
            # Alleen status update bij start (0%) en voltooiing (100%)
            if progress <= 0.01:  # Start
                self.thread.status_updated.emit(f"🎤 Fast Whisper transcriptie gestart: {os.path.basename(file_path)}")
            elif progress >= 0.99:  # Voltooid
                self.thread.status_updated.emit(f"✅ Fast Whisper transcriptie voltooid: {os.path.basename(file_path)}")
            
            # Console output voor Fast Whisper progress
            console_progress = (15 + (progress * 50)) / 100.0
            # Alleen voortgangsbalk tonen, geen andere berichten
            self.thread.status_updated.emit(f"CONSOLE_OUTPUT:🎤 {progress_bar}")
            
            # Check of verwerking gestopt moet worden
            if not self.thread.is_running:
                return False  # Stop Fast Whisper processing
            return True  # Ga door met processing
        
        # Fast Whisper stop callback functie
        def whisper_stop_callback():
            # Alleen loggen als er daadwerkelijk een stop wordt gevraagd
            if not self.thread.is_running:
                return True
            return False
        
        # Voer Fast Whisper transcriptie uit
        transcript_result = whisper_manager.transcribe_audio(
            audio_path, 
            progress_callback=whisper_progress_callback,
            stop_callback=whisper_stop_callback
        )
        
        # Check of transcript_result geldig is
        if not transcript_result:
            self.thread.status_updated.emit(f"❌ Fast Whisper transcriptie gefaald: Geen resultaat")
            return None
        
        if not isinstance(transcript_result, dict):
            self.thread.status_updated.emit(f"❌ Fast Whisper transcriptie gefaald: Ongeldig resultaat")
            return None
        
        if "error" in transcript_result:
            self.thread.status_updated.emit(f"❌ Fast Whisper transcriptie gefaald: {transcript_result['error']}")
            return None
        
        # Check voor transcript
        transcript = transcript_result.get("transcript", "")
        transcriptions = transcript_result.get("transcriptions", [])
        if not transcript:
            self.thread.status_updated.emit(f"⚠️ Geen transcriptie gegenereerd voor {file_path}")
            # Maak een placeholder transcriptie voor bestanden zonder spraak
            transcript = "[Geen spraak gedetecteerd in deze video]"
            self.thread.status_updated.emit(f"ℹ️ Placeholder transcriptie gemaakt voor {file_path}")
            # Maak ook placeholder transcriptions
            transcriptions = [{
                "start": 0.0,
                "end": 10.0,
                "text": transcript,
                "language": "en"
            }]
        
        return {
            "transcript": transcript,
            "transcriptions": transcriptions,
            "language": transcript_result.get("language", "en")
        }
