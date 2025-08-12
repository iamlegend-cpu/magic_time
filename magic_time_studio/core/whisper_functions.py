"""
Whisper functies voor Magic Time Studio
Bevat alle Whisper transcriptie functionaliteit
"""

import os
import json
import tempfile
from typing import Optional, Dict, List, Any, Tuple
import logging

logger = logging.getLogger(__name__)

# Whisper model configuratie
WHISPER_MODELS = {
    "tiny": "openai/whisper-tiny",
    "base": "openai/whisper-base",
    "small": "openai/whisper-small",
    "medium": "openai/whisper-medium",
    "large": "openai/whisper-large",
    "large-v2": "openai/whisper-large-v2",
    "large-v3": "openai/whisper-large-v3"
}

def load_whisper_model(model_name: str = "base", device: str = "auto") -> Optional[Any]:
    """
    Laad een Whisper model
    
    Args:
        model_name: Naam van het model (tiny, base, small, medium, large)
        device: Device om het model op te laden (cpu, cuda, auto)
    
    Returns:
        Geladen Whisper model of None bij fout
    """
    try:
        # Probeer eerst fast-whisper
        try:
            from fast_whisper import WhisperModel
            logger.info(f"Laad fast-whisper model: {model_name}")
            model = WhisperModel(model_name, device=device, compute_type="int8")
            return model
        except ImportError:
            logger.info("Fast-whisper niet beschikbaar, probeer standaard whisper")
        
        # Fallback naar standaard whisper
        try:
            import whisper
            logger.info(f"Laad standaard whisper model: {model_name}")
            model = whisper.load_model(model_name, device=device)
            return model
        except ImportError:
            logger.error("Geen whisper implementatie beschikbaar")
            return None
            
    except Exception as e:
        logger.error(f"Fout bij laden Whisper model: {e}")
        return None

def transcribe_audio_fast_whisper(audio_path: str, model_name: str = "base", 
                                 language: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Transcribeer audio met fast-whisper
    
    Args:
        audio_path: Pad naar het audio bestand
        model_name: Naam van het Whisper model
        language: Taal code (optioneel)
    
    Returns:
        Dictionary met transcriptie resultaat of None bij fout
    """
    try:
        if not os.path.exists(audio_path):
            logger.error(f"Audio bestand bestaat niet: {audio_path}")
            return None
        
        model = load_whisper_model(model_name)
        if model is None:
            return None
        
        # Transcribeer audio
        segments, info = model.transcribe(audio_path, language=language, beam_size=5)
        
        # Converteer naar gewenste formaat
        transcriptions = []
        full_transcript = ""
        
        for segment in segments:
            transcriptions.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip(),
                "language": info.language
            })
            full_transcript += segment.text.strip() + " "
        
        result = {
            "transcript": full_transcript.strip(),
            "transcriptions": transcriptions,
            "language": info.language,
            "language_probability": info.language_probability
        }
        
        logger.info(f"Fast-whisper transcriptie voltooid: {len(transcriptions)} segmenten")
        return result
        
    except Exception as e:
        logger.error(f"Fout bij fast-whisper transcriptie: {e}")
        return None

def transcribe_audio_standard_whisper(audio_path: str, model_name: str = "base",
                                    language: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Transcribeer audio met standaard whisper
    
    Args:
        audio_path: Pad naar het audio bestand
        model_name: Naam van het Whisper model
        language: Taal code (optioneel)
    
    Returns:
        Dictionary met transcriptie resultaat of None bij fout
    """
    try:
        if not os.path.exists(audio_path):
            logger.error(f"Audio bestand bestaat niet: {audio_path}")
            return None
        
        import whisper
        
        model = whisper.load_model(model_name)
        
        # Transcribeer audio
        result = model.transcribe(audio_path, language=language)
        
        # Converteer naar gewenste formaat
        transcriptions = []
        for segment in result["segments"]:
            transcriptions.append({
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"].strip(),
                "language": result.get("language", "unknown")
            })
        
        output = {
            "transcript": result["text"].strip(),
            "transcriptions": transcriptions,
            "language": result.get("language", "unknown"),
            "language_probability": result.get("language_probability", 0.0)
        }
        
        logger.info(f"Standaard whisper transcriptie voltooid: {len(transcriptions)} segmenten")
        return output
        
    except Exception as e:
        logger.error(f"Fout bij standaard whisper transcriptie: {e}")
        return None

def detect_language(audio_path: str, model_name: str = "base") -> Optional[Tuple[str, float]]:
    """
    Detecteer de taal van audio
    
    Args:
        audio_path: Pad naar het audio bestand
        model_name: Naam van het Whisper model
    
    Returns:
        Tuple met (taal_code, waarschijnlijkheid) of None bij fout
    """
    try:
        if not os.path.exists(audio_path):
            logger.error(f"Audio bestand bestaat niet: {audio_path}")
            return None
        
        # Gebruik fast-whisper voor taal detectie
        try:
            from fast_whisper import WhisperModel
            model = WhisperModel(model_name, device="cpu", compute_type="int8")
            segments, info = model.transcribe(audio_path, language=None, beam_size=1)
            
            # Haal eerste segment op voor taal detectie
            next(segments)  # Skip eerste segment
            
            return (info.language, info.language_probability)
            
        except ImportError:
            # Fallback naar standaard whisper
            import whisper
            model = whisper.load_model(model_name)
            result = model.transcribe(audio_path, language=None)
            
            return (result.get("language", "unknown"), 
                   result.get("language_probability", 0.0))
            
    except Exception as e:
        logger.error(f"Fout bij taal detectie: {e}")
        return None

def transcribe_with_timestamps(audio_path: str, model_name: str = "base",
                             language: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
    """
    Transcribeer audio met gedetailleerde timestamps
    
    Args:
        audio_path: Pad naar het audio bestand
        model_name: Naam van het Whisper model
        language: Taal code (optioneel)
    
    Returns:
        Lijst van transcriptie segmenten met timestamps of None bij fout
    """
    try:
        # Probeer fast-whisper eerst
        result = transcribe_audio_fast_whisper(audio_path, model_name, language)
        if result:
            return result["transcriptions"]
        
        # Fallback naar standaard whisper
        result = transcribe_audio_standard_whisper(audio_path, model_name, language)
        if result:
            return result["transcriptions"]
        
        return None
        
    except Exception as e:
        logger.error(f"Fout bij transcriptie met timestamps: {e}")
        return None

def save_transcription_to_srt(transcriptions: List[Dict[str, Any]], 
                             output_path: str) -> bool:
    """
    Sla transcriptie op als SRT bestand
    
    Args:
        transcriptions: Lijst van transcriptie segmenten
        output_path: Pad naar het output SRT bestand
    
    Returns:
        True bij succes, False bij fout
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(transcriptions, 1):
                start_time = format_timestamp(segment["start"])
                end_time = format_timestamp(segment["end"])
                text = segment["text"]
                
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")
        
        logger.info(f"SRT bestand opgeslagen: {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"Fout bij opslaan SRT bestand: {e}")
        return False

def format_timestamp(seconds: float) -> str:
    """
    Converteer seconden naar SRT timestamp formaat
    
    Args:
        seconds: Tijd in seconden
    
    Returns:
        Geformatteerde timestamp string (HH:MM:SS,mmm)
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds % 1) * 1000)
    seconds = int(seconds)
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def get_whisper_model_info(model_name: str = "base") -> Optional[Dict[str, Any]]:
    """
    Haal informatie op over een Whisper model
    
    Args:
        model_name: Naam van het model
    
    Returns:
        Dictionary met model informatie of None bij fout
    """
    try:
        if model_name not in WHISPER_MODELS:
            logger.error(f"Onbekend model: {model_name}")
            return None
        
        # Model informatie
        model_info = {
            "name": model_name,
            "full_name": WHISPER_MODELS[model_name],
            "parameters": {
                "tiny": "39M",
                "base": "74M", 
                "small": "244M",
                "medium": "769M",
                "large": "1550M",
                "large-v2": "1550M",
                "large-v3": "1550M"
            }.get(model_name, "Unknown"),
            "languages": "Multilingual",
            "description": f"OpenAI Whisper {model_name} model"
        }
        
        return model_info
        
    except Exception as e:
        logger.error(f"Fout bij ophalen model informatie: {e}")
        return None
