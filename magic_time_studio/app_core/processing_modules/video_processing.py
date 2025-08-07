"""
Video processing module voor Magic Time Studio
"""

import os
from magic_time_studio.processing import video_processor

class VideoProcessor:
    """Video processing functionaliteit"""
    
    def __init__(self, processing_thread):
        self.thread = processing_thread
        self.settings = processing_thread.settings
    
    def process_video(self, file_path, transcript, transcriptions, translated_transcriptions=None):
        """Process video met ondertitels"""
        if self.settings.get('subtitle_type') == 'hardcoded':
            return self._process_hardcoded_video(file_path, transcript)
        else:
            return self._process_softcoded_video(file_path, transcriptions, translated_transcriptions)
    
    def _process_hardcoded_video(self, file_path, transcript):
        """Process video met hardcoded ondertitels"""
        self.thread.status_updated.emit(f"🎬 Video verwerking gestart: {os.path.basename(file_path)}")
        
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
                        
                        self.thread.progress_updated.emit(ffmpeg_progress, progress_text)
                except:
                    pass  # Stil falen als parsing niet lukt
                # Console output
                self.thread.status_updated.emit(f"CONSOLE_OUTPUT:{msg}")
        
        video_result = video_processor.add_subtitles_to_video(
            file_path,
            transcript,
            progress_callback=video_progress_wrapper,
            settings=self.settings
        )
        
        if video_result.get("success"):
            self.thread.status_updated.emit(f"✅ Video verwerking voltooid: {os.path.basename(file_path)}")
        else:
            self.thread.status_updated.emit(f"⚠️ Video verwerking gefaald: {video_result.get('error', 'Onbekende fout')}")
        
        return video_result
    
    def _process_softcoded_video(self, file_path, transcriptions, translated_transcriptions=None):
        """Process video met softcoded ondertitels (SRT bestanden)"""
        self.thread.status_updated.emit(f"📄 SRT bestanden genereren: {os.path.basename(file_path)}")
        
        video_result = video_processor.generate_srt_files(
            file_path,
            transcriptions,
            translated_transcriptions if self.settings.get('enable_translation', False) else None,
            self.settings
        )
        
        if video_result.get("success"):
            self.thread.status_updated.emit(f"✅ SRT bestanden gegenereerd: {os.path.basename(file_path)}")
            # Log de gegenereerde SRT bestanden
            if "output_files" in video_result:
                output_files = video_result["output_files"]
                for file_type, file_path_srt in output_files.items():
                    self.thread.status_updated.emit(f"📄 {file_type.upper()} bestand gegenereerd: {os.path.basename(file_path_srt)}")
        else:
            self.thread.status_updated.emit(f"⚠️ SRT generatie gefaald: {video_result.get('error', 'Onbekende fout')}")
        
        return video_result
