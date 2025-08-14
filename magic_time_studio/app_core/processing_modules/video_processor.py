"""
Video Processor Module voor Magic Time Studio
Handelt video verwerking en ondertiteling af
"""

import os
import subprocess
from typing import Optional, Dict, Any, List

# Import WhisperX SRT functies voor betere accuracy
try:
    from magic_time_studio.core.whisperx_srt_functions import (
        create_whisperx_srt_content,
        validate_whisperx_transcriptions,
        get_whisperx_statistics
    )
    WHISPERX_SRT_AVAILABLE = True
except ImportError:
    WHISPERX_SRT_AVAILABLE = False
    print("⚠️ WhisperX SRT functies niet beschikbaar, gebruik standaard SRT generatie")

class VideoProcessor:
    """Video verwerking module met FFmpeg"""
    
    def __init__(self, processing_thread):
        self.processing_thread = processing_thread
        self.settings = None  # Instellingen worden later ingesteld
    
    def set_settings(self, settings: dict):
        """Stel instellingen in voor de video processor"""
        print(f"🔍 [DEBUG] VideoProcessor.set_settings: Ontvangen instellingen = {settings}")
        print(f"🔍 [DEBUG] VideoProcessor.set_settings: subtitle_type = {settings.get('subtitle_type', 'NIET_GEVONDEN')}")
        print(f"🔍 [DEBUG] VideoProcessor.set_settings: preserve_subtitles = {settings.get('preserve_subtitles', 'NIET_GEVONDEN')}")
        self.settings = settings
        print(f"🔍 [DEBUG] VideoProcessor.set_settings: self.settings ingesteld = {self.settings}")
    
    def process_video(self, file_path: str, transcript: str, transcriptions: List[Dict[str, Any]], 
                     translated_transcriptions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Verwerk video - maak alleen SRT bestanden"""
        try:
            print(f"🎬 Start video verwerking: {file_path}")
            print(f"🔍 [DEBUG] VideoProcessor.process_video: self.settings = {self.settings}")
            print(f"🔍 [DEBUG] VideoProcessor.process_video: transcript lengte = {len(transcript) if transcript else 0}")
            print(f"🔍 [DEBUG] VideoProcessor.process_video: transcriptions count = {len(transcriptions) if transcriptions else 0}")
            print(f"🔍 [DEBUG] VideoProcessor.process_video: translated_transcriptions count = {len(translated_transcriptions) if translated_transcriptions else 0}")
            
            # Update status
            self.processing_thread.status_updated.emit("🎬 SRT bestanden worden gemaakt...")
            self.processing_thread.progress_updated.emit(70.0, "SRT bestanden maken...")
            
            # Haal instellingen op
            preserve_subtitles = self._get_preserve_subtitles_setting()
            print(f"🔍 [DEBUG] VideoProcessor.process_video: preserve_subtitles = {preserve_subtitles}")
            
            # Maak alleen SRT bestanden - geen video verwerking
            print("📝 Maak alleen SRT bestanden - geen video verwerking")
            
            # Maak SRT bestand voor ondertiteling
            srt_path = self._create_srt_file(translated_transcriptions, file_path)
            if not srt_path:
                return {"error": "Kon SRT bestand niet maken"}
            
            # Maak ook SRT bestand met alleen originele tekst (zonder vertaling) - alleen als preserve_subtitles is ingeschakeld
            original_srt_path = None
            if preserve_subtitles:
                original_srt_path = self._create_original_srt_file(transcriptions, file_path)
                if not original_srt_path:
                    print("⚠️ Kon origineel SRT bestand niet maken")
                else:
                    print(f"✅ Origineel SRT bestand gemaakt: {original_srt_path}")
            else:
                print("📝 Origineel SRT bestand wordt niet gemaakt (instelling: verwijder originele SRT)")
                # Verwijder bestaand origineel SRT bestand als het bestaat
                self._remove_existing_original_srt(file_path)
            
            print(f"✅ SRT bestanden gemaakt: {srt_path}")
            
            # Retourneer het originele video bestand als output (geen wijziging)
            return {"output_path": file_path, "srt_path": srt_path, "original_srt_path": original_srt_path}
            
        except Exception as e:
            print(f"❌ Fout bij video verwerking: {e}")
            return {"error": str(e)}
    
    def _create_srt_file(self, transcriptions: List[Dict[str, Any]], video_path: str) -> Optional[str]:
        """Maak SRT bestand van transcripties (vertaald)"""
        try:
            print(f"🔍 [DEBUG] VideoProcessor._create_srt_file: Start met {len(transcriptions)} transcripties")
            
            # Genereer SRT bestandsnaam - gebruik _NL voor vertaalde versie
            base_name = os.path.splitext(os.path.basename(video_path))[0]
            srt_path = os.path.join(os.path.dirname(video_path), f"{base_name}_NL.srt")
            print(f"🔍 [DEBUG] VideoProcessor._create_srt_file: SRT pad = {srt_path}")
            
            # Gebruik WhisperX SRT functies voor betere accuracy als beschikbaar
            if WHISPERX_SRT_AVAILABLE:
                print("🎯 Gebruik WhisperX SRT generatie voor betere accuracy")
                # Valideer transcripties eerst
                if validate_whisperx_transcriptions(transcriptions):
                    # Genereer SRT met WhisperX functies
                    srt_content = create_whisperx_srt_content(transcriptions)
                    # Schrijf SRT bestand
                    with open(srt_path, 'w', encoding='utf-8') as f:
                        f.write(srt_content)
                else:
                    print("⚠️ WhisperX validatie gefaald, gebruik standaard SRT generatie")
                    srt_content = self._create_standard_srt_content(transcriptions)
                    with open(srt_path, 'w', encoding='utf-8') as f:
                        f.write(srt_content)
            else:
                # Fallback naar standaard SRT generatie
                print("📝 Gebruik standaard SRT generatie")
                srt_content = self._create_standard_srt_content(transcriptions)
                with open(srt_path, 'w', encoding='utf-8') as f:
                    f.write(srt_content)
            
            print(f"✅ SRT bestand gemaakt: {srt_path}")
            print(f"🔍 [DEBUG] VideoProcessor._create_srt_file: SRT bestand grootte = {os.path.getsize(srt_path)} bytes")
            return srt_path
            
        except Exception as e:
            print(f"❌ Fout bij maken SRT bestand: {e}")
            return None
    
    def _create_standard_srt_content(self, transcriptions: List[Dict[str, Any]]) -> str:
        """Maak standaard SRT content als fallback"""
        srt_content = ""
        for i, segment in enumerate(transcriptions, 1):
            start_time = self._format_time(segment["start"])
            end_time = self._format_time(segment["end"])
            text = segment.get("text", "")
            srt_content += f"{i}\n{start_time} --> {end_time}\n{text}\n\n"
        return srt_content
    
    def _create_original_srt_file(self, transcriptions: List[Dict[str, Any]], video_path: str) -> Optional[str]:
        """Maak SRT bestand van originele transcripties (zonder vertaling)"""
        try:
            print(f"🔍 [DEBUG] VideoProcessor._create_original_srt_file: Start met {len(transcriptions)} transcripties")
            
            # Genereer SRT bestandsnaam - gebruik originele bestandsnaam zonder toevoegingen
            base_name = os.path.splitext(os.path.basename(video_path))[0]
            srt_path = os.path.join(os.path.dirname(video_path), f"{base_name}.srt")
            print(f"🔍 [DEBUG] VideoProcessor._create_original_srt_file: SRT pad = {srt_path}")
            
            # Gebruik WhisperX SRT functies voor betere accuracy als beschikbaar
            if WHISPERX_SRT_AVAILABLE:
                print("🎯 Gebruik WhisperX SRT generatie voor originele transcripties")
                # Valideer transcripties eerst
                if validate_whisperx_transcriptions(transcriptions):
                    # Genereer SRT met WhisperX functies
                    srt_content = create_whisperx_srt_content(transcriptions)
                    # Schrijf SRT bestand
                    with open(srt_path, 'w', encoding='utf-8') as f:
                        f.write(srt_content)
                else:
                    print("⚠️ WhisperX validatie gefaald, gebruik standaard SRT generatie")
                    srt_content = self._create_standard_srt_content(transcriptions)
                    with open(srt_path, 'w', encoding='utf-8') as f:
                        f.write(srt_content)
            else:
                # Fallback naar standaard SRT generatie
                print("📝 Gebruik standaard SRT generatie voor originele transcripties")
                srt_content = self._create_standard_srt_content(transcriptions)
                with open(srt_path, 'w', encoding='utf-8') as f:
                    f.write(srt_content)
            
            print(f"✅ Origineel SRT bestand gemaakt: {srt_path}")
            print(f"🔍 [DEBUG] VideoProcessor._create_original_srt_file: SRT bestand grootte = {os.path.getsize(srt_path)} bytes")
            return srt_path
            
        except Exception as e:
            print(f"❌ Fout bij maken origineel SRT bestand: {e}")
            return None
    
    def _add_subtitles_to_video(self, video_path: str, srt_path: str) -> Optional[str]:
        """Voeg ondertiteling toe aan video met FFmpeg"""
        try:
            print(f"🔍 [DEBUG] VideoProcessor._add_subtitles_to_video: Start met video_path = {video_path}")
            print(f"🔍 [DEBUG] VideoProcessor._add_subtitles_to_video: srt_path = {srt_path}")
            
            # Genereer output bestandsnaam
            base_name = os.path.splitext(os.path.basename(video_path))[0]
            output_path = os.path.join(os.path.dirname(video_path), f"{base_name}_subtitled.mp4")
            print(f"🔍 [DEBUG] VideoProcessor._add_subtitles_to_video: output_path = {output_path}")
            
            # Haal subtitle type instelling op
            subtitle_type = self._get_subtitle_type_setting()
            print(f"🔍 [DEBUG] VideoProcessor._add_subtitles_to_video: subtitle_type = {subtitle_type}")
            
            # Altijd softcoded ondertiteling (hardcoded wordt niet meer ondersteund)
            print("📝 Softcoded ondertiteling - voeg SRT toe als externe track")
            print(f"🔍 [DEBUG] VideoProcessor: FFmpeg commando voor softcoded (replace):")
            
            # FFmpeg commando voor softcoded ondertiteling
            cmd = [
                "ffmpeg", "-i", video_path,
                "-i", srt_path,  # Voeg SRT toe als tweede input
                "-c:v", "copy",  # Kopieer video stream
                "-c:a", "copy",  # Kopieer audio stream
                "-c:s", "mov_text",  # Converteer SRT naar mov_text formaat
                "-metadata:s:s:0", "language=nld",  # Stel taal in
                "-y",  # Overschrijf bestaand bestand
                output_path
            ]
            print(f"🔍 [DEBUG] VideoProcessor: FFmpeg commando: {' '.join(cmd)}")
            
            # Voer FFmpeg uit
            print(f"🔍 [DEBUG] VideoProcessor: Start FFmpeg uitvoering...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            print(f"🔍 [DEBUG] VideoProcessor: FFmpeg returncode: {result.returncode}")
            
            if result.returncode == 0 and os.path.exists(output_path):
                print(f"✅ Ondertiteling toegevoegd: {output_path}")
                return output_path
            else:
                print(f"❌ FFmpeg gefaald: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print("❌ FFmpeg timeout - video te lang")
            return None
        except Exception as e:
            print(f"❌ Fout bij toevoegen ondertiteling: {e}")
            return None
    
    def _format_time(self, seconds: float) -> str:
        """Converteer seconden naar SRT timestamp formaat"""
        try:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = int(seconds % 60)
            millisecs = int((seconds % 1) * 1000)
            return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"
        except:
            return "00:00:00,000"
    
    def _get_preserve_subtitles_setting(self) -> bool:
        """Haal preserve_subtitles instelling op"""
        try:
            if self.settings:
                preserve_subtitles = self.settings.get("preserve_subtitles", False)
                print(f"🔍 [DEBUG] VideoProcessor._get_preserve_subtitles_setting: {preserve_subtitles}")
                return preserve_subtitles
            else:
                print("⚠️ VideoProcessor._get_preserve_subtitles_setting: self.settings is None")
                return False
        except Exception as e:
            print(f"❌ Fout bij ophalen preserve_subtitles instelling: {e}")
            return False
    
    def _get_subtitle_type_setting(self) -> str:
        """Haal subtitle_type instelling op"""
        try:
            if self.settings:
                subtitle_type = self.settings.get("subtitle_type", "softcoded")
                print(f"🔍 [DEBUG] VideoProcessor._get_subtitle_type_setting: {subtitle_type}")
                return subtitle_type
            else:
                print("⚠️ VideoProcessor._get_subtitle_type_setting: self.settings is None")
                return "softcoded"
        except Exception as e:
            print(f"❌ Fout bij ophalen subtitle_type instelling: {e}")
            return "softcoded"

    def _remove_existing_original_srt(self, video_path: str):
        """Verwijder bestaand origineel SRT bestand als het bestaat"""
        try:
            # Genereer pad naar origineel SRT bestand
            base_name = os.path.splitext(os.path.basename(video_path))[0]
            original_srt_path = os.path.join(os.path.dirname(video_path), f"{base_name}.srt")
            
            # Controleer of het bestand bestaat
            if os.path.exists(original_srt_path):
                print(f"🗑️ Verwijder bestaand origineel SRT bestand: {original_srt_path}")
                
                # Verwijder het bestand
                os.remove(original_srt_path)
                
                if os.path.exists(original_srt_path):
                    print(f"⚠️ Kon origineel SRT bestand niet verwijderen: {original_srt_path}")
                else:
                    print(f"✅ Origineel SRT bestand succesvol verwijderd: {original_srt_path}")
            else:
                print(f"ℹ️ Geen bestaand origineel SRT bestand gevonden om te verwijderen: {original_srt_path}")
                
        except Exception as e:
            print(f"⚠️ Fout bij verwijderen origineel SRT bestand: {e}")
            import traceback
            traceback.print_exc()
