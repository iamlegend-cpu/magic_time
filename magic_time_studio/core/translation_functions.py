"""
Vertaling functies voor Magic Time Studio
Bevat alle vertaling functionaliteit
"""

import os
import json
import requests
from typing import Optional, Dict, List, Any, Tuple
import logging

logger = logging.getLogger(__name__)

# Ondersteunde vertaling services
TRANSLATION_SERVICES = {
    "libretranslate": {
        "name": "LibreTranslate",
        "url": "https://libretranslate.com/translate",
        "free": True,
        "languages": ["en", "nl", "de", "fr", "es", "it", "pt", "ru", "ja", "ko", "zh"]
    },
    "google": {
        "name": "Google Translate",
        "url": "https://translation.googleapis.com/language/translate/v2",
        "free": False,
        "languages": ["en", "nl", "de", "fr", "es", "it", "pt", "ru", "ja", "ko", "zh"]
    },
    "deepl": {
        "name": "DeepL",
        "url": "https://api-free.deepl.com/v2/translate",
        "free": False,
        "languages": ["en", "nl", "de", "fr", "es", "it", "pt", "ru", "ja", "ko", "zh"]
    }
}

# Taal codes en namen
LANGUAGE_CODES = {
    "en": "English",
    "nl": "Nederlands", 
    "de": "Deutsch",
    "fr": "Français",
    "es": "Español",
    "it": "Italiano",
    "pt": "Português",
    "ru": "Русский",
    "ja": "日本語",
    "ko": "한국어",
    "zh": "中文"
}

def translate_text_libretranslate(text: str, source_lang: str, target_lang: str,
                                api_url: str = "https://libretranslate.com/translate") -> Optional[str]:
    """
    Vertaal tekst met LibreTranslate
    
    Args:
        text: Tekst om te vertalen
        source_lang: Bron taal code
        target_lang: Doel taal code
        api_url: LibreTranslate API URL
    
    Returns:
        Vertaalde tekst of None bij fout
    """
    try:
        payload = {
            "q": text,
            "source": source_lang,
            "target": target_lang,
            "format": "text"
        }
        
        response = requests.post(api_url, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            translated_text = result.get("translatedText", "")
            logger.info(f"LibreTranslate vertaling voltooid: {source_lang} -> {target_lang}")
            return translated_text
        else:
            logger.error(f"LibreTranslate API fout: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        logger.error("LibreTranslate vertaling timeout")
        return None
    except Exception as e:
        logger.error(f"Fout bij LibreTranslate vertaling: {e}")
        return None

def translate_text_google(text: str, source_lang: str, target_lang: str,
                         api_key: str) -> Optional[str]:
    """
    Vertaal tekst met Google Translate
    
    Args:
        text: Tekst om te vertalen
        source_lang: Bron taal code
        target_lang: Doel taal code
        api_key: Google Translate API key
    
    Returns:
        Vertaalde tekst of None bij fout
    """
    try:
        url = "https://translation.googleapis.com/language/translate/v2"
        params = {
            "key": api_key,
            "q": text,
            "source": source_lang,
            "target": target_lang
        }
        
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            translated_text = result["data"]["translations"][0]["translatedText"]
            logger.info(f"Google Translate vertaling voltooid: {source_lang} -> {target_lang}")
            return translated_text
        else:
            logger.error(f"Google Translate API fout: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"Fout bij Google Translate vertaling: {e}")
        return None

def translate_text_deepl(text: str, source_lang: str, target_lang: str,
                        api_key: str) -> Optional[str]:
    """
    Vertaal tekst met DeepL
    
    Args:
        text: Tekst om te vertalen
        source_lang: Bron taal code
        target_lang: Doel taal code
        api_key: DeepL API key
    
    Returns:
        Vertaalde tekst of None bij fout
    """
    try:
        url = "https://api-free.deepl.com/v2/translate"
        headers = {
            "Authorization": f"DeepL-Auth-Key {api_key}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "text": text,
            "source_lang": source_lang.upper(),
            "target_lang": target_lang.upper()
        }
        
        response = requests.post(url, headers=headers, data=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            translated_text = result["translations"][0]["text"]
            logger.info(f"DeepL vertaling voltooid: {source_lang} -> {target_lang}")
            return translated_text
        else:
            logger.error(f"DeepL API fout: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"Fout bij DeepL vertaling: {e}")
        return None

def translate_text(text: str, source_lang: str, target_lang: str,
                  service: str = "libretranslate", **kwargs) -> Optional[str]:
    """
    Vertaal tekst met de opgegeven service
    
    Args:
        text: Tekst om te vertalen
        source_lang: Bron taal code
        target_lang: Doel taal code
        service: Vertaling service (libretranslate, google, deepl)
        **kwargs: Extra parameters (api_key, api_url, etc.)
    
    Returns:
        Vertaalde tekst of None bij fout
    """
    try:
        if service == "libretranslate":
            api_url = kwargs.get("api_url", "https://libretranslate.com/translate")
            return translate_text_libretranslate(text, source_lang, target_lang, api_url)
        
        elif service == "google":
            api_key = kwargs.get("api_key")
            if not api_key:
                logger.error("Google Translate API key vereist")
                return None
            return translate_text_google(text, source_lang, target_lang, api_key)
        
        elif service == "deepl":
            api_key = kwargs.get("api_key")
            if not api_key:
                logger.error("DeepL API key vereist")
                return None
            return translate_text_deepl(text, source_lang, target_lang, api_key)
        
        else:
            logger.error(f"Onbekende vertaling service: {service}")
            return None
            
    except Exception as e:
        logger.error(f"Fout bij vertaling: {e}")
        return None

def translate_transcriptions(transcriptions: List[Dict[str, Any]], source_lang: str,
                           target_lang: str, service: str = "libretranslate", **kwargs) -> Optional[List[Dict[str, Any]]]:
    """
    Vertaal transcriptie segmenten
    
    Args:
        transcriptions: Lijst van transcriptie segmenten
        source_lang: Bron taal code
        target_lang: Doel taal code
        service: Vertaling service
        **kwargs: Extra parameters
    
    Returns:
        Lijst van vertaalde transcriptie segmenten of None bij fout
    """
    try:
        if not transcriptions:
            return []
        
        translated_transcriptions = []
        
        for segment in transcriptions:
            original_text = segment.get("text", "")
            if not original_text.strip():
                continue
            
            # Vertaal de tekst
            translated_text = translate_text(original_text, source_lang, target_lang, service, **kwargs)
            
            if translated_text:
                translated_segment = segment.copy()
                translated_segment["text"] = translated_text
                translated_segment["original_text"] = original_text
                translated_segment["source_language"] = source_lang
                translated_segment["target_language"] = target_lang
                translated_transcriptions.append(translated_segment)
            else:
                # Gebruik originele tekst als vertaling faalt
                translated_segment = segment.copy()
                translated_segment["original_text"] = original_text
                translated_segment["source_language"] = source_lang
                translated_segment["target_language"] = target_lang
                translated_transcriptions.append(translated_segment)
        
        logger.info(f"Vertaling voltooid: {len(translated_transcriptions)} segmenten")
        return translated_transcriptions
        
    except Exception as e:
        logger.error(f"Fout bij vertalen transcripties: {e}")
        return None

def batch_translate_texts(texts: List[str], source_lang: str, target_lang: str,
                         service: str = "libretranslate", **kwargs) -> Optional[List[str]]:
    """
    Vertaal meerdere teksten in batch
    
    Args:
        texts: Lijst van teksten om te vertalen
        source_lang: Bron taal code
        target_lang: Doel taal code
        service: Vertaling service
        **kwargs: Extra parameters
    
    Returns:
        Lijst van vertaalde teksten of None bij fout
    """
    try:
        if not texts:
            return []
        
        translated_texts = []
        
        for text in texts:
            if not text.strip():
                translated_texts.append("")
                continue
            
            translated_text = translate_text(text, source_lang, target_lang, service, **kwargs)
            if translated_text:
                translated_texts.append(translated_text)
            else:
                # Gebruik originele tekst als vertaling faalt
                translated_texts.append(text)
        
        logger.info(f"Batch vertaling voltooid: {len(translated_texts)} teksten")
        return translated_texts
        
    except Exception as e:
        logger.error(f"Fout bij batch vertaling: {e}")
        return None

def detect_language_from_text(text: str, service: str = "libretranslate") -> Optional[Tuple[str, float]]:
    """
    Detecteer taal van tekst
    
    Args:
        text: Tekst om taal van te detecteren
        service: Service voor taal detectie
    
    Returns:
        Tuple met (taal_code, waarschijnlijkheid) of None bij fout
    """
    try:
        if service == "libretranslate":
            # LibreTranslate taal detectie
            url = "https://libretranslate.com/detect"
            payload = {"q": text}
            
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result:
                    detected_lang = result[0].get("language", "unknown")
                    confidence = result[0].get("confidence", 0.0)
                    return (detected_lang, confidence)
            
            return None
            
        else:
            logger.error(f"Taal detectie niet ondersteund voor service: {service}")
            return None
            
    except Exception as e:
        logger.error(f"Fout bij taal detectie: {e}")
        return None

def get_supported_languages(service: str = "libretranslate") -> Optional[List[Dict[str, str]]]:
    """
    Haal ondersteunde talen op voor een service
    
    Args:
        service: Vertaling service
    
    Returns:
        Lijst van ondersteunde talen of None bij fout
    """
    try:
        if service == "libretranslate":
            url = "https://libretranslate.com/languages"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                languages = response.json()
                return [
                    {
                        "code": lang.get("code", ""),
                        "name": lang.get("name", ""),
                        "native_name": lang.get("nativeName", "")
                    }
                    for lang in languages
                ]
            
            return None
            
        else:
            logger.error(f"Taal lijst niet ondersteund voor service: {service}")
            return None
            
    except Exception as e:
        logger.error(f"Fout bij ophalen ondersteunde talen: {e}")
        return None

def validate_language_code(lang_code: str) -> bool:
    """
    Valideer een taal code
    
    Args:
        lang_code: Taal code om te valideren
    
    Returns:
        True als geldig, False anders
    """
    return lang_code in LANGUAGE_CODES

def get_language_name(lang_code: str) -> Optional[str]:
    """
    Haal taal naam op voor een taal code
    
    Args:
        lang_code: Taal code
    
    Returns:
        Taal naam of None bij fout
    """
    return LANGUAGE_CODES.get(lang_code)
