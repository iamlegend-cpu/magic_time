"""
Video processor voor Magic Time Studio
Beheert video verwerking en SRT bestand generatie
"""

import os
import json
import tempfile
from typing import Dict, Any, List, Optional
from datetime import timedelta
from ..core.logging import logger
from ..core.config import config_manager
from ..core.utils import safe_basename
from .audio_processor import audio_processor
from .whisper_processor import whisper_processor
from .translator import translator

class VideoProcessor:
    """Processor voor video verwerking en SRT bestand generatie"""
    
    def __init__(self):
        self.supported_formats = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']
        self.output_formats = ['srt', 'vtt', 'txt', 'json']
        
    def process_video(self, video_path: str, settings: Dict[str, Any], 
                     progress_callback: Optional[callable] = None) -> Dict[str, Any]:
        """Verwerk video bestand volledig (audio extractie + transcriptie + vertaling)"""
        try:
            if not os.path.exists(video_path):
                return {"error": "Video bestand niet gevonden"}
            
            logger.log_debug(f"🎬 Start video verwerking: {safe_basename(video_path)}")
            
            # Stap 1: Haal video informatie op
            if progress_callback:
                progress_callback(0.1, "Video informatie ophalen...")
            
            video_info = audio_processor.get_video_info(video_path)
            if not video_info.get("success"):
                return {"error": f"Kan video info niet ophalen: {video_info.get('error')}"}
            
            # Stap 2: Extracteer audio
            if progress_callback:
                progress_callback(0.2, "Audio extractie...")
            
            audio_result = audio_processor.extract_audio_from_video(
                video_path, 
                output_dir=settings.get("output_dir"),
                audio_format="wav"
            )
            
            if not audio_result.get("success"):
                return {"error": f"Audio extractie gefaald: {audio_result.get('error')}"}
            
            audio_path = audio_result["audio_path"]
            
            # Stap 3: Transcriptie
            if progress_callback:
                progress_callback(0.4, "Transcriptie...")
            
            whisper_settings = settings.get("whisper", {})
            language = whisper_settings.get("language", "auto")
            
            # Detecteer taal als auto
            if language == "auto" and settings.get("auto_detect", True):
                detected_language = whisper_processor.detect_language(audio_path)
                if detected_language != "auto":
                    language = detected_language
                    logger.log_debug(f"🌍 Taal gedetecteerd: {language}")
            
            transcription_result = whisper_processor.transcribe_audio(
                audio_path,
                language=language,
                progress_callback=lambda p: progress_callback(0.4 + p * 0.4, f"Transcriptie {p:.1%}")
            )
            
            if not transcription_result.get("success"):
                return {"error": f"Transcriptie gefaald: {transcription_result.get('error')}"}
            
            transcriptions = transcription_result["transcriptions"]
            
            # Stap 4: Vertaling (indien gewenst)
            if progress_callback:
                progress_callback(0.8, "Vertaling...")
            
            translator_settings = settings.get("translator", {})
            target_language = translator_settings.get("target_language")
            translator_service = translator_settings.get("service", "libretranslate")
            
            if target_language and target_language != language:
                translated_transcriptions = translator.translate_transcriptions(
                    transcriptions,
                    source_lang=language,
                    target_lang=target_language,
                    service=translator_service
                )
            else:
                translated_transcriptions = transcriptions
            
            # Stap 5: Genereer output bestanden
            if progress_callback:
                progress_callback(0.9, "Output bestanden genereren...")
            
            output_result = self._generate_output_files(
                video_path, transcriptions, translated_transcriptions, settings
            )
            
            if progress_callback:
                progress_callback(1.0, "Voltooid!")
            
            # Ruim tijdelijke audio op
            try:
                if os.path.exists(audio_path):
                    os.remove(audio_path)
                    logger.log_debug("🧹 Tijdelijke audio opgeruimd")
            except Exception as e:
                logger.log_debug(f"⚠️ Kon tijdelijke audio niet opruimen: {e}")
            
            logger.log_debug(f"✅ Video verwerking voltooid: {safe_basename(video_path)}")
            
            return {
                "success": True,
                "video_path": video_path,
                "transcriptions": transcriptions,
                "translated_transcriptions": translated_transcriptions,
                "output_files": output_result.get("output_files", {}),
                "video_info": video_info.get("info", {}),
                "processing_time": output_result.get("processing_time", 0)
            }
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij video verwerking: {e}")
            return {"error": str(e)}
    
    def _generate_output_files(self, video_path: str, transcriptions: List[Dict], 
                             translated_transcriptions: List[Dict], 
                             settings: Dict[str, Any]) -> Dict[str, Any]:
        """Genereer output bestanden (SRT, VTT, etc.)"""
        try:
            output_dir = settings.get("output_dir", os.path.dirname(video_path))
            os.makedirs(output_dir, exist_ok=True)
            
            video_name = safe_basename(video_path)
            name_without_ext = os.path.splitext(video_name)[0]
            
            output_files = {}
            
            # SRT bestand (origineel)
            if settings.get("generate_srt", True):
                srt_path = os.path.join(output_dir, f"{name_without_ext}.srt")
                self._create_srt_file(transcriptions, srt_path)
                output_files["srt"] = srt_path
            
            # SRT bestand (vertaald)
            if settings.get("generate_translated_srt", True) and translated_transcriptions != transcriptions:
                translated_srt_path = os.path.join(output_dir, f"{name_without_ext}_translated.srt")
                self._create_srt_file(translated_transcriptions, translated_srt_path)
                output_files["translated_srt"] = translated_srt_path
            
            # VTT bestand
            if settings.get("generate_vtt", False):
                vtt_path = os.path.join(output_dir, f"{name_without_ext}.vtt")
                self._create_vtt_file(transcriptions, vtt_path)
                output_files["vtt"] = vtt_path
            
            # JSON bestand
            if settings.get("generate_json", False):
                json_path = os.path.join(output_dir, f"{name_without_ext}.json")
                self._create_json_file(transcriptions, translated_transcriptions, json_path)
                output_files["json"] = json_path
            
            # TXT bestand
            if settings.get("generate_txt", False):
                txt_path = os.path.join(output_dir, f"{name_without_ext}.txt")
                self._create_txt_file(transcriptions, txt_path)
                output_files["txt"] = txt_path
            
            logger.log_debug(f"📄 Output bestanden gegenereerd: {len(output_files)} bestanden")
            
            return {
                "success": True,
                "output_files": output_files
            }
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij genereren output bestanden: {e}")
            return {"error": str(e)}
    
    def _create_srt_file(self, transcriptions: List[Dict], output_path: str):
        """Maak SRT bestand"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for i, segment in enumerate(transcriptions, 1):
                    start_time = self._format_timestamp(segment["start"])
                    end_time = self._format_timestamp(segment["end"])
                    text = segment.get("translated_text", segment["text"])
                    
                    f.write(f"{i}\n")
                    f.write(f"{start_time} --> {end_time}\n")
                    f.write(f"{text}\n\n")
            
            logger.log_debug(f"📄 SRT bestand gemaakt: {safe_basename(output_path)}")
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij maken SRT bestand: {e}")
            raise
    
    def _create_vtt_file(self, transcriptions: List[Dict], output_path: str):
        """Maak VTT bestand"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("WEBVTT\n\n")
                
                for i, segment in enumerate(transcriptions, 1):
                    start_time = self._format_timestamp_vtt(segment["start"])
                    end_time = self._format_timestamp_vtt(segment["end"])
                    text = segment.get("translated_text", segment["text"])
                    
                    f.write(f"{start_time} --> {end_time}\n")
                    f.write(f"{text}\n\n")
            
            logger.log_debug(f"📄 VTT bestand gemaakt: {safe_basename(output_path)}")
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij maken VTT bestand: {e}")
            raise
    
    def _create_json_file(self, transcriptions: List[Dict], translated_transcriptions: List[Dict], 
                         output_path: str):
        """Maak JSON bestand"""
        try:
            data = {
                "original_transcriptions": transcriptions,
                "translated_transcriptions": translated_transcriptions,
                "metadata": {
                    "total_segments": len(transcriptions),
                    "has_translations": transcriptions != translated_transcriptions
                }
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.log_debug(f"📄 JSON bestand gemaakt: {safe_basename(output_path)}")
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij maken JSON bestand: {e}")
            raise
    
    def _create_txt_file(self, transcriptions: List[Dict], output_path: str):
        """Maak TXT bestand"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for segment in transcriptions:
                    text = segment.get("translated_text", segment["text"])
                    f.write(f"{text}\n")
            
            logger.log_debug(f"📄 TXT bestand gemaakt: {safe_basename(output_path)}")
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij maken TXT bestand: {e}")
            raise
    
    def _format_timestamp(self, seconds: float) -> str:
        """Format timestamp voor SRT"""
        td = timedelta(seconds=seconds)
        hours = int(td.total_seconds() // 3600)
        minutes = int((td.total_seconds() % 3600) // 60)
        secs = td.total_seconds() % 60
        return f"{hours:02d}:{minutes:02d}:{secs:06.3f}".replace('.', ',')
    
    def _format_timestamp_vtt(self, seconds: float) -> str:
        """Format timestamp voor VTT"""
        td = timedelta(seconds=seconds)
        hours = int(td.total_seconds() // 3600)
        minutes = int((td.total_seconds() % 3600) // 60)
        secs = td.total_seconds() % 60
        return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"
    
    def is_video_file(self, file_path: str) -> bool:
        """Controleer of bestand een video is"""
        if not file_path:
            return False
        
        _, ext = os.path.splitext(file_path.lower())
        return ext in self.supported_formats
    
    def get_supported_formats(self) -> List[str]:
        """Krijg ondersteunde video formaten"""
        return self.supported_formats.copy()
    
    def get_output_formats(self) -> List[str]:
        """Krijg beschikbare output formaten"""
        return self.output_formats.copy()

# Globale video processor instantie
video_processor = VideoProcessor() 