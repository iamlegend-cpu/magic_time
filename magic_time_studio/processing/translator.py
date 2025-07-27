"""
Translator voor Magic Time Studio
Beheert tekstvertaling met LibreTranslate
"""

import os
import time
import requests
from typing import Dict, Any, List, Optional
from ..core.logging import logger
from ..core.config import config_manager
from ..models.processing_queue import api_throttle

class Translator:
    """Translator voor tekstvertaling"""
    
    def __init__(self):
        self.supported_services = {
            "libretranslate": "LibreTranslate (gratis)",
            "geen": "Geen vertaling"
        }
        
        self.supported_languages = {
            "nl": "Nederlands",
            "en": "Engels",
            "de": "Duits", 
            "fr": "Frans",
            "es": "Spaans",
            "it": "Italiaans",
            "pt": "Portugees",
            "ru": "Russisch",
            "ja": "Japans",
            "ko": "Koreaans",
            "zh": "Chinees"
        }
        
        self.default_server = "http://100.90.127.78:5000"
        self.current_service = "libretranslate"
        
    def set_service(self, service: str):
        """Zet vertaler service"""
        if service in self.supported_services:
            self.current_service = service
            logger.log_debug(f"🌐 Vertaler service gewijzigd: {service}")
        else:
            logger.log_debug(f"❌ Onbekende vertaler service: {service}")
    
    def translate_text(self, text: str, source_lang: str, target_lang: str, 
                      service: Optional[str] = None) -> Dict[str, Any]:
        """Vertaal tekst"""
        try:
            if not text or not text.strip():
                return {"error": "Lege tekst"}
            
            if service is None:
                service = self.current_service
            
            if service == "geen":
                return {"success": True, "translated_text": text, "service": "geen"}
            
            logger.log_debug(f"🌐 Start vertaling ({service}): {source_lang} -> {target_lang}")
            
            # Wacht voor API rate limiting
            api_throttle.wait_if_needed(1)
            
            if service == "libretranslate":
                return self._translate_libretranslate(text, source_lang, target_lang)
            else:
                return {"error": f"Onbekende service: {service}"}
                
        except Exception as e:
            logger.log_debug(f"❌ Fout bij vertaling: {e}")
            return {"error": str(e)}
    
    def _translate_libretranslate(self, text: str, source_lang: str, target_lang: str) -> Dict[str, Any]:
        """Vertaal met LibreTranslate"""
        try:
            server_url = config_manager.get("libretranslate_server", self.default_server)
            
            # Split tekst in chunks als te lang
            chunks = self._split_text_into_chunks(text, max_chunk_size=5000)
            translated_chunks = []
            
            for i, chunk in enumerate(chunks):
                logger.log_debug(f"🌐 LibreTranslate chunk {i+1}/{len(chunks)}")
                
                payload = {
                    "q": chunk,
                    "source": source_lang,
                    "target": target_lang,
                    "format": "text"
                }
                
                response = requests.post(
                    f"{server_url}/translate",
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    translated_chunks.append(result.get("translatedText", chunk))
                else:
                    logger.log_debug(f"❌ LibreTranslate fout: {response.status_code}")
                    return {"error": f"LibreTranslate fout: {response.status_code}"}
                
                # Korte pauze tussen chunks
                time.sleep(0.1)
            
            translated_text = " ".join(translated_chunks)
            logger.log_debug(f"✅ LibreTranslate vertaling voltooid")
            
            return {
                "success": True,
                "translated_text": translated_text,
                "service": "libretranslate",
                "chunks": len(chunks)
            }
            
        except requests.exceptions.RequestException as e:
            logger.log_debug(f"❌ LibreTranslate netwerk fout: {e}")
            return {"error": f"Netwerk fout: {e}"}
        except Exception as e:
            logger.log_debug(f"❌ LibreTranslate fout: {e}")
            return {"error": str(e)}
    

    
    def _split_text_into_chunks(self, text: str, max_chunk_size: int = 5000) -> List[str]:
        """Split tekst in chunks voor vertaling"""
        if len(text) <= max_chunk_size:
            return [text]
        
        chunks = []
        current_chunk = ""
        
        # Split op zinnen
        sentences = text.split('. ')
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < max_chunk_size:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def translate_transcriptions(self, transcriptions: List[Dict[str, Any]], 
                                source_lang: str, target_lang: str,
                                service: Optional[str] = None) -> List[Dict[str, Any]]:
        """Vertaal transcriptie segmenten"""
        try:
            if not transcriptions:
                return []
            
            logger.log_debug(f"🌐 Start vertaling van {len(transcriptions)} transcriptie segmenten")
            
            translated_transcriptions = []
            
            for i, segment in enumerate(transcriptions):
                original_text = segment.get("text", "")
                
                if not original_text.strip():
                    translated_transcriptions.append(segment)
                    continue
                
                # Vertaal tekst
                translation_result = self.translate_text(
                    original_text, source_lang, target_lang, service
                )
                
                if translation_result.get("success"):
                    # Update segment met vertaling
                    segment["translated_text"] = translation_result["translated_text"]
                    segment["translation_service"] = translation_result["service"]
                else:
                    # Fallback naar origineel
                    segment["translated_text"] = original_text
                    segment["translation_service"] = "geen"
                    logger.log_debug(f"⚠️ Vertaling gefaald voor segment {i}: {translation_result.get('error')}")
                
                translated_transcriptions.append(segment)
                
                # Progress logging
                if (i + 1) % 10 == 0:
                    logger.log_debug(f"📊 Vertaling voortgang: {i+1}/{len(transcriptions)}")
            
            logger.log_debug(f"✅ Vertaling van transcripties voltooid")
            return translated_transcriptions
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij vertalen transcripties: {e}")
            return transcriptions  # Return origineel als fallback
    
    def get_supported_services(self) -> Dict[str, str]:
        """Krijg lijst van ondersteunde services"""
        return self.supported_services.copy()
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Krijg lijst van ondersteunde talen"""
        return self.supported_languages.copy()
    
    def test_service(self, service: str) -> bool:
        """Test vertaler service"""
        try:
            test_text = "Hello world"
            result = self.translate_text(test_text, "en", "nl", service)
            return result.get("success", False)
        except Exception as e:
            logger.log_debug(f"❌ Service test gefaald: {e}")
            return False
    
    def get_current_service(self) -> str:
        """Krijg huidige service"""
        return self.current_service

# Globale translator instantie
translator = Translator() 