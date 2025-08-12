"""
Video Processor Module voor Magic Time Studio
Handelt video verwerking en ondertiteling af
"""

import os
import subprocess
from typing import Optional, Dict, Any, List

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
            
            # Maak ook SRT bestand met alleen originele tekst (zonder vertaling)
            original_srt_path = self._create_original_srt_file(transcriptions, file_path)
            if not original_srt_path:
                print("⚠️ Kon origineel SRT bestand niet maken")
            
            print(f"✅ SRT bestanden gemaakt: {srt_path}")
            if original_srt_path:
                print(f"✅ Origineel SRT bestand gemaakt: {original_srt_path}")
            
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
            
            # Maak SRT content
            srt_content = ""
            for i, segment in enumerate(transcriptions, 1):
                start_time = self._format_time(segment["start"])
                end_time = self._format_time(segment["end"])
                
                            # Toon alleen vertaling (origineel komt in apart SRT bestand)
                text = segment.get("text", "")
                print(f"🔍 [DEBUG] VideoProcessor._create_srt_file: Segment {i}: vertaalde tekst")
                
                srt_content += f"{i}\n{start_time} --> {end_time}\n{text}\n\n"
            
            # Schrijf SRT bestand
            with open(srt_path, 'w', encoding='utf-8') as f:
                f.write(srt_content)
            
            print(f"✅ SRT bestand gemaakt: {srt_path}")
            print(f"🔍 [DEBUG] VideoProcessor._create_srt_file: SRT bestand grootte = {os.path.getsize(srt_path)} bytes")
            return srt_path
            
        except Exception as e:
            print(f"❌ Fout bij maken SRT bestand: {e}")
            return None
    
    def _create_original_srt_file(self, transcriptions: List[Dict[str, Any]], video_path: str) -> Optional[str]:
        """Maak SRT bestand van originele transcripties (zonder vertaling)"""
        try:
            print(f"🔍 [DEBUG] VideoProcessor._create_original_srt_file: Start met {len(transcriptions)} transcripties")
            
            # Genereer SRT bestandsnaam - gebruik originele bestandsnaam zonder toevoegingen
            base_name = os.path.splitext(os.path.basename(video_path))[0]
            srt_path = os.path.join(os.path.dirname(video_path), f"{base_name}.srt")
            print(f"🔍 [DEBUG] VideoProcessor._create_original_srt_file: SRT pad = {srt_path}")
            
            # Maak SRT content met alleen originele tekst
            srt_content = ""
            for i, segment in enumerate(transcriptions, 1):
                start_time = self._format_time(segment["start"])
                end_time = self._format_time(segment["end"])
                
                # Gebruik originele tekst als die beschikbaar is, anders fallback naar text
                original_text = segment.get("original_text", segment.get("text", ""))
                text = original_text
                
                srt_content += f"{i}\n{start_time} --> {end_time}\n{text}\n\n"
            
            # Schrijf SRT bestand
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
            # Converteer SRT naar mov_text (ondersteund door MP4) en voeg toe als externe track
            cmd = [
                "ffmpeg", "-i", video_path,
                "-i", srt_path,  # Voeg SRT toe als tweede input toe
                "-c:v", "copy",  # Kopieer video stream
                "-c:a", "copy",  # Kopieer audio stream
                "-c:s", "mov_text",  # Converteer SRT naar mov_text formaat
                "-metadata:s:s:0", "language=nld",  # Stel taal in
                "-y",  # Overschrijf bestaand bestand
                output_path
            ]
            print(f"🔍 [DEBUG] VideoProcessor: FFmpeg commando: {' '.join(cmd)}")
            
            # Voer FFmpeg uit
            print(f"🔍 [DEBUG] VideoProcessor: Start FFmpeg uitvoering (replace)...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            print(f"🔍 [DEBUG] VideoProcessor: FFmpeg returncode (replace): {result.returncode}")
            print(f"🔍 [DEBUG] VideoProcessor: FFmpeg stdout (replace): {result.stdout}")
            print(f"🔍 [DEBUG] VideoProcessor: FFmpeg stderr (replace): {result.stderr}")
            
            if result.returncode == 0 and os.path.exists(output_path):
                print(f"✅ Ondertiteling toegevoegd ({subtitle_type}): {output_path}")
                return output_path
            else:
                print(f"❌ FFmpeg fout: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print("❌ Video verwerking timeout (10 minuten)")
            return None
        except Exception as e:
            print(f"❌ Fout bij toevoegen ondertiteling: {e}")
            return None
    
    def _format_time(self, seconds: float) -> str:
        """Converteer seconden naar SRT tijdformaat (HH:MM:SS,mmm)"""
        try:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = int(seconds % 60)
            millisecs = int((seconds % 1) * 1000)
            
            formatted_time = f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"
            print(f"🔍 [DEBUG] VideoProcessor._format_time: {seconds}s -> {formatted_time}")
            return formatted_time
        except Exception as e:
            print(f"🔍 [DEBUG] VideoProcessor._format_time: Fout bij formatteren tijd {seconds}: {e}")
            return "00:00:00,000"
    
    def create_thumbnail(self, video_path: str, output_path: str, time_position: str = "00:00:05") -> bool:
        """Maak thumbnail van video op specifieke tijd"""
        try:
            cmd = [
                "ffmpeg", "-i", video_path,
                "-ss", time_position,  # Tijd positie
                "-vframes", "1",  # Eén frame
                "-q:v", "2",  # Hoge kwaliteit
                "-y",  # Overschrijf bestaand bestand
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0 and os.path.exists(output_path):
                print(f"✅ Thumbnail gemaakt: {output_path}")
                return True
            else:
                print(f"❌ Thumbnail fout: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Fout bij maken thumbnail: {e}")
            return False
    
    def _get_preserve_subtitles_setting(self) -> bool:
        """Haal preserve_subtitles instelling op (altijd False)"""
        # Er worden altijd alleen SRT bestanden gemaakt - geen video verwerking
        print(f"🔍 [DEBUG] VideoProcessor._get_preserve_subtitles_setting: Altijd alleen SRT bestanden maken")
        return False
    
    def _get_subtitle_type_setting(self) -> str:
        """Haal subtitle_type instelling op (altijd softcoded)"""
        # Hardcoded ondertiteling wordt niet meer ondersteund - altijd softcoded
        print(f"🔍 [DEBUG] VideoProcessor: Subtitle type instelling: altijd softcoded (hardcoded niet meer ondersteund)")
        return 'softcoded'
    
    def _add_subtitles_preserve_original(self, video_path: str, transcriptions: List[Dict[str, Any]]) -> Optional[str]:
        """Voeg ondertiteling toe aan video terwijl originele ondertitels behouden blijven"""
        try:
            print(f"🔍 [DEBUG] VideoProcessor._add_subtitles_preserve_original: Start met video_path = {video_path}")
            print(f"🔍 [DEBUG] VideoProcessor._add_subtitles_preserve_original: transcriptions count = {len(transcriptions) if transcriptions else 0}")
            
            # Genereer output bestandsnaam
            base_name = os.path.splitext(os.path.basename(video_path))[0]
            output_path = os.path.join(os.path.dirname(video_path), f"{base_name}_with_subtitles.mp4")
            print(f"🔍 [DEBUG] VideoProcessor._add_subtitles_preserve_original: output_path = {output_path}")
            
            # Maak eerst SRT bestand
            srt_path = self._create_srt_file(transcriptions, video_path)
            if not srt_path:
                return None
            
            # Haal subtitle type instelling op
            subtitle_type = self._get_subtitle_type_setting()
            print(f"🔍 [DEBUG] VideoProcessor._add_subtitles_preserve_original: subtitle_type = {subtitle_type}")
            
            # Altijd softcoded ondertiteling (hardcoded wordt niet meer ondersteund)
            print("📝 Softcoded ondertiteling - voeg SRT toe als externe track")
            print(f"🔍 [DEBUG] VideoProcessor: FFmpeg commando voor softcoded (preserve):")
            # FFmpeg commando voor softcoded ondertiteling
            # Converteer SRT naar mov_text (ondersteund door MP4) en voeg toe als externe track
            cmd = [
                "ffmpeg", "-i", video_path,
                "-i", srt_path,  # Voeg SRT als tweede input toe
                "-c:v", "copy",  # Kopieer video stream
                "-c:a", "copy",  # Kopieer audio stream
                "-c:s", "mov_text",  # Converteer SRT naar mov_text formaat
                "-metadata:s:s:0", "language=nld",  # Stel taal in
                "-y",  # Overschrijf bestaand bestand
                output_path
            ]
            print(f"🔍 [DEBUG] VideoProcessor: FFmpeg commando: {' '.join(cmd)}")
            
            # Voer FFmpeg uit
            print(f"🔍 [DEBUG] VideoProcessor: Start FFmpeg uitvoering (preserve)...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            print(f"🔍 [DEBUG] VideoProcessor: FFmpeg returncode (preserve): {result.returncode}")
            print(f"🔍 [DEBUG] VideoProcessor: FFmpeg stdout (preserve): {result.stdout}")
            print(f"🔍 [DEBUG] VideoProcessor: FFmpeg stderr (preserve): {result.stderr}")
            
            # Ruim SRT bestand op
            try:
                if os.path.exists(srt_path):
                    os.remove(srt_path)
            except:
                pass
            
            if result.returncode == 0 and os.path.exists(output_path):
                print(f"✅ Ondertiteling toegevoegd ({subtitle_type}, originele behouden): {output_path}")
                return output_path
            else:
                print(f"❌ FFmpeg fout: {result.stderr}")
                # Probeer alternatieve methode met overlay filter
                return self._add_subtitles_overlay_method(video_path, transcriptions)
                
        except subprocess.TimeoutExpired:
            print("❌ Video verwerking timeout (10 minuten)")
            return None
        except Exception as e:
            print(f"❌ Fout bij toevoegen ondertiteling: {e}")
            return None
    
    def _add_subtitles_overlay_method(self, video_path: str, transcriptions: List[Dict[str, Any]]) -> Optional[str]:
        """Alternatieve methode om ondertiteling toe te voegen met overlay filter"""
        try:
            print(f"🔍 [DEBUG] VideoProcessor._add_subtitles_overlay_method: Start met video_path = {video_path}")
            print(f"🔍 [DEBUG] VideoProcessor._add_subtitles_overlay_method: transcriptions count = {len(transcriptions) if transcriptions else 0}")
            
            # Genereer output bestandsnaam
            base_name = os.path.splitext(os.path.basename(video_path))[0]
            output_path = os.path.join(os.path.dirname(video_path), f"{base_name}_with_subtitles.mp4")
            print(f"🔍 [DEBUG] VideoProcessor._add_subtitles_overlay_method: output_path = {output_path}")
            
            # Maak eerst SRT bestand
            srt_path = self._create_srt_file(transcriptions, video_path)
            if not srt_path:
                return None
            
            # Haal subtitle type instelling op
            subtitle_type = self._get_subtitle_type_setting()
            print(f"🔍 [DEBUG] VideoProcessor._add_subtitles_overlay_method: subtitle_type = {subtitle_type}")
            
            # Altijd softcoded ondertiteling (hardcoded wordt niet meer ondersteund)
            print("📝 Softcoded ondertiteling (overlay methode) - voeg SRT toe als externe track")
            print(f"🔍 [DEBUG] VideoProcessor: FFmpeg commando voor softcoded (overlay):")
            # FFmpeg commando voor softcoded ondertiteling
            # Converteer SRT naar mov_text (ondersteund door MP4) en voeg toe als externe track
            cmd = [
                "ffmpeg", "-i", video_path,
                "-i", srt_path,  # Voeg SRT als tweede input toe
                "-c:v", "copy",  # Kopieer video stream
                "-c:a", "copy",  # Kopieer audio stream
                "-c:s", "mov_text",  # Converteer SRT naar mov_text formaat
                "-metadata:s:s:0", "language=nld",  # Stel taal in
                "-y",  # Overschrijf bestaand bestand
                output_path
            ]
            print(f"🔍 [DEBUG] VideoProcessor: FFmpeg commando: {' '.join(cmd)}")
            
            # Voer FFmpeg uit
            print(f"🔍 [DEBUG] VideoProcessor: Start FFmpeg uitvoering (overlay)...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            print(f"🔍 [DEBUG] VideoProcessor: FFmpeg returncode (overlay): {result.returncode}")
            print(f"🔍 [DEBUG] VideoProcessor: FFmpeg stdout (overlay): {result.stdout}")
            print(f"🔍 [DEBUG] VideoProcessor: FFmpeg stderr (overlay): {result.stderr}")
            
            # Ruim SRT bestand op
            try:
                if os.path.exists(srt_path):
                    os.remove(srt_path)
            except:
                pass
            
            if result.returncode == 0 and os.path.exists(output_path):
                print(f"✅ Ondertiteling toegevoegd ({subtitle_type}, overlay methode): {output_path}")
                return output_path
            else:
                print(f"❌ FFmpeg overlay methode gefaald: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"❌ Fout bij overlay methode: {e}")
            return None
