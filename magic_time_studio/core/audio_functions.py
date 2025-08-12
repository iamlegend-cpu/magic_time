"""
Audio functies voor Magic Time Studio
Bevat alle audio-gerelateerde functionaliteit
"""

import os
import subprocess
import tempfile
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)

def extract_audio_from_video(video_path: str, output_dir: Optional[str] = None) -> Optional[str]:
    """
    Extraheer audio uit een video bestand
    
    Args:
        video_path: Pad naar het video bestand
        output_dir: Uitvoer directory (optioneel)
    
    Returns:
        Pad naar het geëxtraheerde audio bestand of None bij fout
    """
    try:
        if not os.path.exists(video_path):
            logger.error(f"Video bestand bestaat niet: {video_path}")
            return None
        
        # Bepaal output directory
        if output_dir is None:
            output_dir = os.path.dirname(video_path)
        
        # Genereer output bestandsnaam
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        audio_path = os.path.join(output_dir, f"{base_name}_audio.wav")
        
        # FFmpeg commando voor audio extractie
        cmd = [
            "ffmpeg", "-i", video_path,
            "-vn",  # Geen video
            "-acodec", "pcm_s16le",  # PCM 16-bit
            "-ar", "16000",  # 16kHz sample rate
            "-ac", "1",  # Mono
            "-y",  # Overschrijf bestaand bestand
            audio_path
        ]
        
        # Voer FFmpeg uit
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0 and os.path.exists(audio_path):
            logger.info(f"Audio succesvol geëxtraheerd: {audio_path}")
            return audio_path
        else:
            logger.error(f"FFmpeg fout: {result.stderr}")
            return None
            
    except subprocess.TimeoutExpired:
        logger.error("Audio extractie timeout (5 minuten)")
        return None
    except Exception as e:
        logger.error(f"Fout bij audio extractie: {e}")
        return None

def get_audio_duration(audio_path: str) -> Optional[float]:
    """
    Bepaal de duur van een audio bestand
    
    Args:
        audio_path: Pad naar het audio bestand
    
    Returns:
        Duur in seconden of None bij fout
    """
    try:
        cmd = [
            "ffprobe", "-v", "quiet",
            "-show_entries", "format=duration",
            "-of", "csv=p=0",
            audio_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            duration = float(result.stdout.strip())
            return duration
        else:
            logger.error(f"FFprobe fout: {result.stderr}")
            return None
            
    except Exception as e:
        logger.error(f"Fout bij bepalen audio duur: {e}")
        return None

def convert_audio_format(input_path: str, output_path: str, format_type: str = "wav") -> bool:
    """
    Converteer audio naar een ander formaat
    
    Args:
        input_path: Pad naar input audio bestand
        output_path: Pad naar output audio bestand
        format_type: Gewenst formaat (wav, mp3, etc.)
    
    Returns:
        True bij succes, False bij fout
    """
    try:
        cmd = [
            "ffmpeg", "-i", input_path,
            "-y",  # Overschrijf bestaand bestand
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0 and os.path.exists(output_path):
            logger.info(f"Audio succesvol geconverteerd naar {format_type}")
            return True
        else:
            logger.error(f"FFmpeg conversie fout: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"Fout bij audio conversie: {e}")
        return False

def normalize_audio(audio_path: str, output_path: Optional[str] = None) -> Optional[str]:
    """
    Normaliseer audio volume
    
    Args:
        audio_path: Pad naar het audio bestand
        output_path: Pad naar output bestand (optioneel)
    
    Returns:
        Pad naar genormaliseerd audio bestand of None bij fout
    """
    try:
        if output_path is None:
            base_name = os.path.splitext(audio_path)[0]
            output_path = f"{base_name}_normalized.wav"
        
        cmd = [
            "ffmpeg", "-i", audio_path,
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",  # EBU R128 standaard
            "-y",
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0 and os.path.exists(output_path):
            logger.info(f"Audio succesvol genormaliseerd: {output_path}")
            return output_path
        else:
            logger.error(f"FFmpeg normalisatie fout: {result.stderr}")
            return None
            
    except Exception as e:
        logger.error(f"Fout bij audio normalisatie: {e}")
        return None

def split_audio_by_silence(audio_path: str, output_dir: str, silence_threshold: float = -30.0) -> list:
    """
    Split audio op basis van stilte
    
    Args:
        audio_path: Pad naar het audio bestand
        output_dir: Uitvoer directory
        silence_threshold: Stilte drempel in dB
    
    Returns:
        Lijst van paden naar gesplitste audio bestanden
    """
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        base_name = os.path.splitext(os.path.basename(audio_path))[0]
        
        cmd = [
            "ffmpeg", "-i", audio_path,
            "-af", f"silencedetect=noise={silence_threshold}dB:d=0.5",
            "-f", "null", "-"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            logger.error(f"FFmpeg silence detectie fout: {result.stderr}")
            return []
        
        # Parse silence detectie output
        # Dit is een vereenvoudigde implementatie
        # Voor productie gebruik zou je een meer geavanceerde parser willen
        
        output_files = []
        # Hier zou je de silence detectie output parsen en splitsen
        # Voor nu retourneren we alleen het originele bestand
        
        return output_files
        
    except Exception as e:
        logger.error(f"Fout bij audio splitsen: {e}")
        return []
