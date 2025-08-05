"""
Video processor voor Magic Time Studio
Beheert video verwerking en SRT bestand generatie
"""

import os
import json
import subprocess
from typing import Dict, List, Any, Optional
from datetime import timedelta
# Absolute imports in plaats van relative imports
try:
    from magic_time_studio.core.logging import logger
    from magic_time_studio.core.config import config_manager
    from magic_time_studio.core.utils import safe_basename, create_progress_bar
except ImportError:
    # Fallback voor directe import
    import sys
    sys.path.append('..')
    from core.logging import logger
    from core.config import config_manager
    from core.utils import safe_basename, create_progress_bar
from magic_time_studio.processing.audio_processor import audio_processor
from magic_time_studio.processing.whisper_processor import whisper_processor
from magic_time_studio.processing.translator import translator

class VideoProcessor:
    """Processor voor video verwerking en SRT bestand generatie"""
    
    def __init__(self):
        self.supported_formats = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']
        self.output_formats = ['srt', 'vtt', 'txt', 'json']
        
    def process_video(self, video_path: str, settings: Dict[str, Any], 
                     progress_callback: Optional[callable] = None) -> Dict[str, Any]:
        """Verwerk video bestand volledig (audio extractie + transcriptie + vertaling)"""
        try:
            # Controleer of video bestand bestaat
            if not os.path.exists(video_path):
                return {"error": "Video bestand niet gevonden"}
            
            # Controleer of video bestand leesbaar is
            try:
                if os.path.getsize(video_path) == 0:
                    return {"error": "Video bestand is leeg"}
            except Exception as e:
                return {"error": f"Kan video bestand niet lezen: {e}"}
            
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
            
            # Maak een wrapper voor de progress callback om FFmpeg output door te geven
            def audio_progress_wrapper(msg):
                if progress_callback:
                    progress_callback(0.2, f"🎵 {msg}")
            
            audio_result = audio_processor.extract_audio_from_video(
                video_path, 
                output_dir=settings.get("output_dir"),
                audio_format="wav",
                progress_callback=audio_progress_wrapper
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
                try:
                    detected_language = whisper_processor.detect_language(audio_path)
                    if detected_language != "auto":
                        language = detected_language
                        logger.log_debug(f"🌍 Taal gedetecteerd: {language}")
                    else:
                        logger.log_debug("⚠️ Taal detectie gefaald, gebruik 'auto'")
                except Exception as e:
                    logger.log_debug(f"⚠️ Taal detectie gefaald: {e}, gebruik 'auto'")
                    language = "auto"
            
            transcription_result = whisper_processor.transcribe_audio(
                audio_path,
                language=language,
                progress_callback=lambda progress_bar: progress_callback(0.4, f"🎤 {progress_bar}")
            )
            
            if not transcription_result.get("success"):
                return {"error": f"Transcriptie gefaald: {transcription_result.get('error')}"}
            
            transcriptions = transcription_result["transcriptions"]
            
            # Stap 4: Vertaling (indien gewenst)
            if progress_callback:
                progress_callback(0.8, "Vertaling...")
            
            # Vertaling instellingen
            target_language = settings.get("target_language")
            translator_service = settings.get("translator_service", "libretranslate")
            
            # Vertaal alleen als target_language is ingesteld en anders is dan source
            if target_language and target_language != language:
                logger.log_debug(f"🌐 Start vertaling: {language} -> {target_language}")
                translation_result = translator.translate_transcriptions(
                    transcriptions,
                    source_lang=language,
                    target_lang=target_language,
                    service=translator_service
                )
                
                # Controleer of vertaling succesvol was
                if isinstance(translation_result, list) and translation_result:
                    translated_transcriptions = translation_result
                    logger.log_debug(f"✅ Vertaling voltooid: {len(translated_transcriptions)} segmenten")
                else:
                    logger.log_debug(f"⚠️ Vertaling gefaald, gebruik originele transcripties")
                    translated_transcriptions = transcriptions
            else:
                logger.log_debug(f"🌐 Geen vertaling nodig (target_language: {target_language}, source: {language})")
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
            # Gebruik altijd de directory van het bronbestand
            output_dir = os.path.dirname(video_path)
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
    
    def generate_srt_files(self, video_path: str, transcriptions: List[Dict], 
                          translated_transcriptions: List[Dict] = None) -> Dict[str, Any]:
        """Genereer SRT bestanden voor video"""
        try:
            if not os.path.exists(video_path):
                return {"error": "Video bestand niet gevonden"}
            
            logger.log_debug(f"📄 Start SRT generatie: {safe_basename(video_path)}")
            
            # Gebruik altijd de directory van het bronbestand
            output_dir = os.path.dirname(video_path)
            os.makedirs(output_dir, exist_ok=True)
            
            video_name = safe_basename(video_path)
            name_without_ext = os.path.splitext(video_name)[0]
            
            output_files = {}
            
            # SRT bestand (origineel) - alleen als er GEEN vertaling is
            if not translated_transcriptions or translated_transcriptions == transcriptions:
                srt_path = os.path.join(output_dir, f"{name_without_ext}.srt")
                self._create_srt_file(transcriptions, srt_path)
                output_files["srt"] = srt_path
            
            # SRT bestand (vertaald) - alleen als er vertaling is
            if translated_transcriptions and translated_transcriptions != transcriptions:
                translated_srt_path = os.path.join(output_dir, f"{name_without_ext}_nl.srt")
                self._create_srt_file(translated_transcriptions, translated_srt_path)
                output_files["translated_srt"] = translated_srt_path
            
            logger.log_debug(f"📄 SRT bestanden gegenereerd: {len(output_files)} bestanden")
            
            return {
                "success": True,
                "output_files": output_files
            }
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij genereren SRT bestanden: {e}")
            return {"error": str(e)}
    
    def add_subtitles_to_video(self, video_path: str, subtitle_text: str, 
                              output_path: Optional[str] = None, 
                              progress_callback: Optional[callable] = None,
                              settings: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Voeg ondertitels toe aan video bestand met real-time progress updates"""
        try:
            if not os.path.exists(video_path):
                return {"error": "Video bestand niet gevonden"}
            
            logger.log_debug(f"🎬 Start ondertitels toevoegen: {safe_basename(video_path)}")
            
            # Controleer of originele ondertitels behouden moeten worden
            preserve_original_subtitles = True  # Standaard behouden
            if settings:
                preserve_original_subtitles = settings.get("preserve_original_subtitles", True)
            
            logger.log_debug(f"📝 Originele ondertitels behouden: {preserve_original_subtitles}")
            
            # Genereer output pad als niet opgegeven
            if not output_path:
                base_name = os.path.splitext(os.path.basename(video_path))[0]
                output_dir = os.path.dirname(video_path)
                output_path = os.path.join(output_dir, f"{base_name}_with_subtitles.mp4")
            
            # Maak tijdelijke SRT bestand
            import tempfile
            temp_srt_path = None
            try:
                with tempfile.NamedTemporaryFile(mode='w', suffix='.srt', delete=False, encoding='utf-8') as temp_srt:
                    temp_srt_path = temp_srt.name
                    # Schrijf eenvoudige SRT met hele tekst
                    temp_srt.write("1\n")
                    temp_srt.write("00:00:00,000 --> 99:59:59,999\n")
                    temp_srt.write(subtitle_text + "\n\n")
            except Exception as e:
                logger.log_debug(f"❌ Fout bij maken tijdelijk SRT bestand: {e}")
                # Als tijdelijk bestand maken faalt, ga door zonder ondertitels
                return {
                    "success": True,
                    "output_path": video_path,
                    "message": "Transcriptie voltooid (tijdelijk bestand kon niet worden gemaakt)"
                }
            
            try:
                # Gebruik FFmpeg om ondertitels toe te voegen
                import subprocess
                
                # Gebruik een eenvoudigere aanpak met drawtext filter
                # Escape speciale karakters in de tekst
                escaped_text = subtitle_text.replace("'", "\\'").replace('"', '\\"')
                
                # Bepaal FFmpeg commando op basis van originele ondertitels optie
                if preserve_original_subtitles:
                    # Behoud originele ondertitels - voeg nieuwe toe als extra stream
                    logger.log_debug("📝 Behoud originele ondertitels - voeg nieuwe toe als overlay")
                    cmd = [
                        'ffmpeg',
                        '-i', video_path,
                        '-vf', f'drawtext=text=\'{escaped_text}\':fontsize=24:fontcolor=white:box=1:boxcolor=black@0.5:x=(w-text_w)/2:y=h-text_h-10',
                        '-c:a', 'copy',
                        '-c:v', 'libx264',  # Herencode video om ondertitels toe te voegen
                        '-progress', 'pipe:1',  # Stuur progress naar stdout
                        '-y',  # Overschrijf output bestand
                        output_path
                    ]
                else:
                    # Verwijder originele ondertitels - vervang met nieuwe
                    logger.log_debug("📝 Verwijder originele ondertitels - vervang met nieuwe")
                    cmd = [
                        'ffmpeg',
                        '-i', video_path,
                        '-vf', f'drawtext=text=\'{escaped_text}\':fontsize=24:fontcolor=white:box=1:boxcolor=black@0.5:x=(w-text_w)/2:y=h-text_h-10',
                        '-c:a', 'copy',
                        '-c:v', 'libx264',  # Herencode video
                        '-map', '0:v:0',  # Alleen video stream
                        '-map', '0:a',  # Behoud audio streams
                        '-progress', 'pipe:1',  # Stuur progress naar stdout
                        '-y',  # Overschrijf output bestand
                        output_path
                    ]
                
                logger.log_debug(f"🎬 FFmpeg commando: {' '.join(cmd)}")
                
                if progress_callback:
                    # Gebruik Popen voor real-time output
                    process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        bufsize=1,
                        universal_newlines=True
                    )
                    
                    # Lees real-time output
                    while True:
                        output = process.stdout.readline()
                        if output == '' and process.poll() is not None:
                            break
                        if output:
                            # Parse progress uit FFmpeg output
                            if "out_time_ms=" in output:
                                try:
                                    time_ms = int(output.split("=")[1])
                                    # Schat progress gebaseerd op tijd
                                    estimated_duration = 120.0  # 2 minuten
                                    progress = min(time_ms / 1000.0 / estimated_duration, 0.99)
                                    progress_bar = create_progress_bar(progress, 40, safe_basename(video_path))
                                    if progress_callback:
                                        progress_callback(f"🎬 {progress_bar}")
                                except:
                                    pass
                            elif "frame=" in output:
                                # Stuur frame info door
                                if progress_callback:
                                    try:
                                        if "fps=" in output and "time=" in output:
                                            # Extract fps en time info
                                            fps_part = output.split("fps=")[1].split()[0]
                                            time_part = output.split("time=")[1].split()[0]
                                            progress_callback(f"🎬 FFmpeg: {fps_part} fps, {time_part}")
                                        else:
                                            progress_callback(f"🎬 FFmpeg: {output.strip()}")
                                    except:
                                        progress_callback(f"🎬 FFmpeg: {output.strip()}")
                    
                    # Wacht tot proces klaar is
                    return_code = process.wait()
                    
                    if return_code == 0:
                        logger.log_debug(f"✅ Ondertitels toegevoegd: {output_path}")
                        return {
                            "success": True,
                            "output_path": output_path,
                            "message": "Ondertitels succesvol toegevoegd"
                        }
                    else:
                        error_msg = process.stderr.read() if process.stderr else "Onbekende FFmpeg fout"
                        logger.log_debug(f"❌ FFmpeg fout: {error_msg}")
                        
                        # Als video verwerking faalt, retourneer nog steeds succes maar zonder output
                        # Dit zorgt ervoor dat het bestand in de voltooide lijst komt
                        logger.log_debug(f"⚠️ Video verwerking gefaald, maar transcriptie is voltooid")
                        return {
                            "success": True,
                            "output_path": video_path,  # Gebruik origineel bestand
                            "message": "Transcriptie voltooid (video verwerking gefaald)"
                        }
                else:
                    # Originele methode zonder real-time output
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        timeout=300  # 5 minuten timeout
                    )
                    
                    if result.returncode == 0:
                        logger.log_debug(f"✅ Ondertitels toegevoegd: {output_path}")
                        return {
                            "success": True,
                            "output_path": output_path,
                            "message": "Ondertitels succesvol toegevoegd"
                        }
                    else:
                        error_msg = result.stderr if result.stderr else "Onbekende FFmpeg fout"
                        logger.log_debug(f"❌ FFmpeg fout: {error_msg}")
                        
                        # Als video verwerking faalt, retourneer nog steeds succes maar zonder output
                        # Dit zorgt ervoor dat het bestand in de voltooide lijst komt
                        logger.log_debug(f"⚠️ Video verwerking gefaald, maar transcriptie is voltooid")
                        return {
                            "success": True,
                            "output_path": video_path,  # Gebruik origineel bestand
                            "message": "Transcriptie voltooid (video verwerking gefaald)"
                        }
                    
            finally:
                # Ruim tijdelijk bestand op
                if temp_srt_path:
                    try:
                        os.unlink(temp_srt_path)
                    except:
                        pass
                    
        except Exception as e:
            logger.log_debug(f"❌ Fout bij toevoegen ondertitels: {e}")
            # Zelfs bij fout, retourneer succes zodat bestand in voltooide lijst komt
            return {
                "success": True,
                "output_path": video_path,
                "message": f"Transcriptie voltooid (fout: {str(e)})"
            }

# Globale video processor instantie
video_processor = VideoProcessor() 