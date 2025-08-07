"""
Audio processing module voor Magic Time Studio
"""

import os
from magic_time_studio.processing import audio_processor

class AudioProcessor:
    """Audio processing functionaliteit"""
    
    def __init__(self, processing_thread):
        self.thread = processing_thread
        self.settings = processing_thread.settings
    
    def extract_audio(self, file_path):
        """Extract audio van video bestand"""
        self.thread.status_updated.emit(f"🎵 Audio extractie gestart: {os.path.basename(file_path)}")
        
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
                        
                        self.thread.progress_updated.emit(ffmpeg_progress, progress_text)
                except:
                    pass  # Stil falen als parsing niet lukt
                # Console output
                self.thread.status_updated.emit(f"CONSOLE_OUTPUT:{msg}")
        
        audio_result = audio_processor.extract_audio_from_video(
            file_path, 
            progress_callback=audio_progress_callback
        )
        
        if "error" in audio_result:
            self.thread.status_updated.emit(f"❌ Audio extractie gefaald: {audio_result['error']}")
            return None
        
        audio_path = audio_result.get("audio_path")
        if not audio_path or not os.path.exists(audio_path):
            self.thread.status_updated.emit(f"❌ Audio bestand niet gevonden: {audio_path}")
            return None
        
        self.thread.status_updated.emit(f"✅ Audio extractie voltooid: {os.path.basename(file_path)}")
        return audio_path
