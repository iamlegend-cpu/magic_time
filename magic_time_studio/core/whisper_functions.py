"""
Whisper functies voor Magic Time Studio
Alleen WhisperX wordt ondersteund
"""

import os
import json
import tempfile
from typing import Optional, Dict, List, Any, Tuple
import logging

logger = logging.getLogger(__name__)

# WhisperX model configuratie
WHISPERX_MODELS = {
    "tiny": "openai/whisper-tiny",
    "base": "openai/whisper-base", 
    "small": "openai/whisper-small",
    "medium": "openai/whisper-medium",
    "large": "openai/whisper-large",
    "large-v2": "openai/whisper-large-v2",
    "large-v3": "openai/whisper-large-v3"
}

def load_whisperx_model(model_name: str = "large-v3", device: str = "auto") -> Optional[Any]:
    """
    Laad een WhisperX model
    
    Args:
        model_name: Naam van het model (tiny, base, small, medium, large, large-v2, large-v3)
        device: Device om het model op te laden (cpu, cuda, auto)
    
    Returns:
        Geladen WhisperX model of None bij fout
    """
    try:
        import whisperx
        logger.info(f"Laad WhisperX model: {model_name}")
        model = whisperx.load_model(model_name, device=device)
        return model
    except ImportError:
        logger.error("WhisperX niet beschikbaar")
        return None
    except Exception as e:
        logger.error(f"Fout bij laden WhisperX model: {e}")
        return None

def transcribe_audio_whisperx(audio_path: str, model_name: str = "large-v3", 
                              language: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Transcribeer audio met WhisperX
    
    Args:
        audio_path: Pad naar het audio bestand
        model_name: Naam van het WhisperX model
        language: Taal code (optioneel)
    
    Returns:
        Dictionary met transcriptie resultaat of None bij fout
    """
    try:
        if not os.path.exists(audio_path):
            logger.error(f"Audio bestand bestaat niet: {audio_path}")
            return None
        
        model = load_whisperx_model(model_name)
        if model is None:
            return None
        
        # Transcribeer audio met WhisperX
        result = model.transcribe(audio_path, language=language, verbose=False)
        
        # Converteer naar gewenste formaat
        transcriptions = []
        full_transcript = ""
        
        for segment in result["segments"]:
            transcriptions.append({
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"].strip(),
                "language": result.get("language", "unknown")
            })
            full_transcript += segment["text"].strip() + " "
        
        result = {
            "transcript": full_transcript.strip(),
            "transcriptions": transcriptions,
            "language": result.get("language", "unknown"),
            "model": "whisperx"
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Fout bij WhisperX transcriptie: {e}")
        return None

def get_model_info(model_name: str = "large-v3") -> Optional[Dict[str, Any]]:
    """
    Krijg informatie over een WhisperX model
    
    Args:
        model_name: Naam van het model
    
    Returns:
        Dictionary met model informatie of None bij fout
    """
    try:
        if model_name not in WHISPERX_MODELS:
            logger.error(f"Onbekend model: {model_name}")
            return None
        
        model_info = {
            "name": model_name,
            "full_name": WHISPERX_MODELS[model_name],
            "parameters": {
                "tiny": "39M",
                "base": "74M", 
                "small": "244M",
                "medium": "769M",
                "large": "1550M",
                "large-v2": "1550M",
                "large-v3": "1550M"
            },
            "type": "whisperx"
        }
        
        return model_info
        
    except Exception as e:
        logger.error(f"Fout bij ophalen model informatie: {e}")
        return None

def transcribe_with_fallback(audio_path: str, model_name: str = "large-v3", 
                            language: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Transcribeer audio met WhisperX en fallback opties
    
    Args:
        audio_path: Pad naar het audio bestand
        model_name: Naam van het WhisperX model
        language: Taal code (optioneel)
    
    Returns:
        Dictionary met transcriptie resultaat of None bij fout
    """
    # Probeer eerst WhisperX
    result = transcribe_audio_whisperx(audio_path, model_name, language)
    if result:
        return result
    
    # Als WhisperX faalt, probeer een kleiner model
    if model_name != "base":
        logger.info(f"WhisperX gefaald met {model_name}, probeer base model")
        result = transcribe_audio_whisperx(audio_path, "base", language)
        if result:
            return result
    
    # Als laatste optie, probeer tiny model
    if model_name != "tiny":
        logger.info("Base model gefaald, probeer tiny model")
        result = transcribe_audio_whisperx(audio_path, "tiny", language)
        if result:
            return result
    
    logger.error("Alle WhisperX modellen gefaald")
    return None

# Alias voor backward compatibility
load_whisper_model = load_whisperx_model
transcribe_audio_fast_whisper = transcribe_audio_whisperx
transcribe_audio_standard_whisper = transcribe_audio_whisperx
