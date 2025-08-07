"""
Translation processing module voor Magic Time Studio
"""

import os
from magic_time_studio.processing import translator

class TranslationProcessor:
    """Translation processing functionaliteit"""
    
    def __init__(self, processing_thread):
        self.thread = processing_thread
        self.settings = processing_thread.settings
    
    def translate_content(self, transcript, transcriptions, source_language="en"):
        """Vertaal transcript en transcriptions"""
        if not self.settings.get('enable_translation', False):
            return transcript, transcriptions
        
        self.thread.status_updated.emit(f"🌐 Vertaling gestart: {os.path.basename(self.thread.current_file) if hasattr(self.thread, 'current_file') and self.thread.current_file else 'onbekend bestand'}")
        
        target_language = self.settings.get('target_language', 'nl')
        
        # Vertaal de transcript tekst
        translation_result = translator.translate_text(
            transcript, 
            source_language, 
            target_language
        )
        
        if translation_result and "error" not in translation_result:
            transcript = translation_result.get("translated_text", transcript)
            self.thread.status_updated.emit(f"✅ Vertaling voltooid: {source_language} -> {target_language}")
            
            # Vertaal ook de transcriptions lijst voor SRT generatie
            if transcriptions:
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
                
                return transcript, translated_transcriptions
        else:
            error_msg = translation_result.get("error", "Onbekende fout") if translation_result else "Geen resultaat"
            self.thread.status_updated.emit(f"⚠️ Vertaling gefaald: {error_msg}")
            # Gebruik originele transcriptie als fallback
            return transcript, transcriptions
        
        return transcript, transcriptions
