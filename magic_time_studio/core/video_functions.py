"""
Video functies voor Magic Time Studio
Bevat alle video-gerelateerde functionaliteit
"""

import os
import subprocess
import tempfile
from typing import Optional, Tuple, List, Dict, Any
import logging

logger = logging.getLogger(__name__)

def get_video_info(video_path: str) -> Optional[Dict[str, Any]]:
    """
    Haal video informatie op
    
    Args:
        video_path: Pad naar het video bestand
    
    Returns:
        Dictionary met video informatie of None bij fout
    """
    try:
        if not os.path.exists(video_path):
            logger.error(f"Video bestand bestaat niet: {video_path}")
            return None
        
        cmd = [
            "ffprobe", "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            video_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            import json
            info = json.loads(result.stdout)
            return info
        else:
            logger.error(f"FFprobe fout: {result.stderr}")
            return None
            
    except Exception as e:
        logger.error(f"Fout bij ophalen video informatie: {e}")
        return None

def get_video_duration(video_path: str) -> Optional[float]:
    """
    Bepaal de duur van een video bestand
    
    Args:
        video_path: Pad naar het video bestand
    
    Returns:
        Duur in seconden of None bij fout
    """
    try:
        cmd = [
            "ffprobe", "-v", "quiet",
            "-show_entries", "format=duration",
            "-of", "csv=p=0",
            video_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            duration = float(result.stdout.strip())
            return duration
        else:
            logger.error(f"FFprobe fout: {result.stderr}")
            return None
            
    except Exception as e:
        logger.error(f"Fout bij bepalen video duur: {e}")
        return None

def get_video_resolution(video_path: str) -> Optional[Tuple[int, int]]:
    """
    Bepaal de resolutie van een video bestand
    
    Args:
        video_path: Pad naar het video bestand
    
    Returns:
        Tuple met (width, height) of None bij fout
    """
    try:
        cmd = [
            "ffprobe", "-v", "quiet",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height",
            "-of", "csv=p=0",
            video_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if ',' in line:
                    width, height = map(int, line.split(','))
                    return (width, height)
            return None
        else:
            logger.error(f"FFprobe fout: {result.stderr}")
            return None
            
    except Exception as e:
        logger.error(f"Fout bij bepalen video resolutie: {e}")
        return None

def extract_video_frame(video_path: str, output_path: str, time_position: float = 0.0) -> bool:
    """
    Extraheer een frame uit een video op een specifieke tijd
    
    Args:
        video_path: Pad naar het video bestand
        output_path: Pad naar het output frame bestand
        time_position: Tijd in seconden
    
    Returns:
        True bij succes, False bij fout
    """
    try:
        cmd = [
            "ffmpeg", "-i", video_path,
            "-ss", str(time_position),
            "-vframes", "1",
            "-y",
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0 and os.path.exists(output_path):
            logger.info(f"Frame succesvol geëxtraheerd: {output_path}")
            return True
        else:
            logger.error(f"FFmpeg frame extractie fout: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"Fout bij frame extractie: {e}")
        return False

def create_video_thumbnail(video_path: str, output_path: str, time_position: float = 10.0) -> bool:
    """
    Maak een thumbnail van een video
    
    Args:
        video_path: Pad naar het video bestand
        output_path: Pad naar het output thumbnail bestand
        time_position: Tijd in seconden voor de thumbnail
    
    Returns:
        True bij succes, False bij fout
    """
    try:
        cmd = [
            "ffmpeg", "-i", video_path,
            "-ss", str(time_position),
            "-vframes", "1",
            "-vf", "scale=320:240",  # Kleine thumbnail
            "-y",
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0 and os.path.exists(output_path):
            logger.info(f"Thumbnail succesvol aangemaakt: {output_path}")
            return True
        else:
            logger.error(f"FFmpeg thumbnail fout: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"Fout bij thumbnail maken: {e}")
        return False

def merge_video_audio(video_path: str, audio_path: str, output_path: str) -> bool:
    """
    Voeg audio toe aan een video bestand
    
    Args:
        video_path: Pad naar het video bestand
        audio_path: Pad naar het audio bestand
        output_path: Pad naar het output bestand
    
    Returns:
        True bij succes, False bij fout
    """
    try:
        if not os.path.exists(video_path) or not os.path.exists(audio_path):
            logger.error("Video of audio bestand bestaat niet")
            return False
        
        cmd = [
            "ffmpeg", "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",  # Kopieer video codec
            "-c:a", "aac",   # Converteer audio naar AAC
            "-shortest",     # Stop bij kortste stream
            "-y",
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
        
        if result.returncode == 0 and os.path.exists(output_path):
            logger.info(f"Video en audio succesvol samengevoegd: {output_path}")
            return True
        else:
            logger.error(f"FFmpeg merge fout: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"Fout bij video-audio merge: {e}")
        return False

def convert_video_format(input_path: str, output_path: str, format_type: str = "mp4") -> bool:
    """
    Converteer video naar een ander formaat
    
    Args:
        input_path: Pad naar input video bestand
        output_path: Pad naar output video bestand
        format_type: Gewenst formaat (mp4, avi, mkv, etc.)
    
    Returns:
        True bij succes, False bij fout
    """
    try:
        cmd = [
            "ffmpeg", "-i", input_path,
            "-c:v", "libx264",  # H.264 video codec
            "-c:a", "aac",      # AAC audio codec
            "-preset", "medium", # Encoding preset
            "-crf", "23",       # Constant Rate Factor
            "-y",
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        
        if result.returncode == 0 and os.path.exists(output_path):
            logger.info(f"Video succesvol geconverteerd naar {format_type}")
            return True
        else:
            logger.error(f"FFmpeg conversie fout: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"Fout bij video conversie: {e}")
        return False

def compress_video(input_path: str, output_path: str, target_size_mb: int = 100) -> bool:
    """
    Comprimeer video naar een gewenste bestandsgrootte
    
    Args:
        input_path: Pad naar input video bestand
        output_path: Pad naar output video bestand
        target_size_mb: Gewenste bestandsgrootte in MB
    
    Returns:
        True bij succes, False bij fout
    """
    try:
        # Bepaal video duur voor bitrate berekening
        duration = get_video_duration(input_path)
        if duration is None:
            return False
        
        # Bereken benodigde bitrate
        target_size_bits = target_size_mb * 8 * 1024 * 1024
        target_bitrate = int(target_size_bits / duration)
        
        cmd = [
            "ffmpeg", "-i", input_path,
            "-c:v", "libx264",
            "-b:v", str(target_bitrate),
            "-c:a", "aac",
            "-b:a", "128k",
            "-y",
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        
        if result.returncode == 0 and os.path.exists(output_path):
            logger.info(f"Video succesvol gecomprimeerd: {output_path}")
            return True
        else:
            logger.error(f"FFmpeg compressie fout: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"Fout bij video compressie: {e}")
        return False
