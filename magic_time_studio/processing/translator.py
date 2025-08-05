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
        
        # Haal server alleen uit env, geen default IP meer
        self.default_server = None
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
            # Haal server uit env/config, geen fallback naar IP
            server_url = config_manager.get_env("LIBRETRANSLATE_SERVER", None)
            if not server_url:
                logger.log_debug("❌ LIBRETRANSLATE_SERVER niet ingesteld in .env bestand!")
                return {"error": "LIBRETRANSLATE_SERVER niet ingesteld in .env bestand!"}
            
            # Voeg protocol toe als het ontbreekt
            if not server_url.startswith(('http://', 'https://')):
                server_url = f"http://{server_url}"
                logger.log_debug(f"🌐 Server URL aangepast: {server_url}")
            
            # Haal chunk limiet uit env, standaard 10000
            max_chunk_size = int(config_manager.get_env("LIBRETRANSLATE_MAX_CHARS", "10000"))
            # Split tekst in chunks als te lang
            chunks = self._split_text_into_chunks(text, max_chunk_size=max_chunk_size)
            translated_chunks = []
            
            for i, chunk in enumerate(chunks):
                logger.log_debug(f"🌐 LibreTranslate chunk {i+1}/{len(chunks)}")
                
                payload = {
                    "q": chunk,
                    "source": source_lang,
                    "target": target_lang,
                    "format": "text"
                }
                
                timeout = int(config_manager.get_env("LIBRETRANSLATE_TIMEOUT", "30"))
                response = requests.post(
                    f"{server_url}/translate",
                    json=payload,
                    timeout=timeout
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
            
        except requests.exceptions.ConnectionError as e:
            logger.log_debug(f"❌ LibreTranslate verbinding fout: {e}")
            return {"error": f"Kan geen verbinding maken met LibreTranslate server. Controleer of de server draait."}
        except requests.exceptions.Timeout as e:
            logger.log_debug(f"❌ LibreTranslate timeout: {e}")
            return {"error": f"LibreTranslate server reageert niet binnen de timeout."}
        except requests.exceptions.RequestException as e:
            logger.log_debug(f"❌ LibreTranslate netwerk fout: {e}")
            return {"error": f"Netwerk fout: {e}"}
        except Exception as e:
            logger.log_debug(f"❌ LibreTranslate fout: {e}")
            return {"error": str(e)}
    

    
    def _split_text_into_chunks(self, text: str, max_chunk_size: int = 10000) -> List[str]:
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
    
    def _create_translation_batches(self, transcriptions: List[Dict[str, Any]], max_chunk_size: int) -> List[List[Dict[str, Any]]]:
        """Maak batches van transcriptie segmenten voor efficiënte vertaling"""
        batches = []
        current_batch = []
        current_size = 0
        
        for segment in transcriptions:
            text = segment.get("text", "")
            text_length = len(text)
            
            # Als deze tekst de batch te groot maakt, start een nieuwe batch
            if current_size + text_length > max_chunk_size and current_batch:
                batches.append(current_batch)
                current_batch = [segment]
                current_size = text_length
            else:
                current_batch.append(segment)
                current_size += text_length
        
        # Voeg laatste batch toe
        if current_batch:
            batches.append(current_batch)
        
        return batches
    
    def _split_translation_back_to_segments(self, translated_text: str, original_batch: List[Dict[str, Any]]) -> List[str]:
        """Split vertaalde tekst terug naar originele segmenten"""
        if not original_batch:
            return []
        
        # Als er maar 1 segment is, return de hele vertaalde tekst
        if len(original_batch) == 1:
            return [translated_text]
        
        # Split de vertaalde tekst op basis van de originele segment lengtes
        segments = []
        remaining_text = translated_text
        
        for i, segment in enumerate(original_batch):
            original_text = segment.get("text", "")
            
            if not original_text.strip():
                segments.append("")
                continue
            
            # Probeer de vertaalde tekst te splitsen op basis van de originele lengte
            # Dit is een eenvoudige benadering - voor betere resultaten zou je NLP kunnen gebruiken
            if i == len(original_batch) - 1:
                # Laatste segment krijgt alle overgebleven tekst
                segments.append(remaining_text.strip())
            else:
                # Schat de lengte van dit segment in de vertaling
                # Gebruik een eenvoudige ratio benadering
                original_length = len(original_text)
                total_original_length = sum(len(s.get("text", "")) for s in original_batch)
                
                if total_original_length > 0:
                    estimated_length = int((original_length / total_original_length) * len(translated_text))
                    estimated_length = max(estimated_length, 10)  # Minimaal 10 karakters
                    
                    # Zoek naar een natuurlijke splitsing (punt, komma, etc.)
                    split_point = min(estimated_length, len(remaining_text))
                    
                    # Zoek naar het dichtstbijzijnde punt of komma
                    for j in range(max(0, split_point - 50), min(len(remaining_text), split_point + 50)):
                        if remaining_text[j] in '.!?':
                            split_point = j + 1
                            break
                    
                    segment_text = remaining_text[:split_point].strip()
                    remaining_text = remaining_text[split_point:].strip()
                    segments.append(segment_text)
                else:
                    segments.append("")
        
        return segments
    
    def translate_transcriptions(self, transcriptions: List[Dict[str, Any]], 
                                source_lang: str, target_lang: str,
                                service: Optional[str] = None) -> List[Dict[str, Any]]:
        """Vertaal transcriptie segmenten in batches"""
        try:
            if not transcriptions:
                return []
            
            logger.log_debug(f"🌐 Start vertaling van {len(transcriptions)} transcriptie segmenten")
            
            # Groepeer zinnen in batches van max 10.000 karakters
            max_chunk_size = int(config_manager.get_env("LIBRETRANSLATE_MAX_CHARS", "10000"))
            batches = self._create_translation_batches(transcriptions, max_chunk_size)
            
            translated_transcriptions = []
            
            for batch_idx, batch in enumerate(batches):
                logger.log_debug(f"🌐 Vertaal batch {batch_idx+1}/{len(batches)} ({len(batch)} segmenten)")
                
                # Combineer alle teksten in deze batch
                combined_text = " ".join([segment.get("text", "") for segment in batch])
                
                if not combined_text.strip():
                    # Voeg originele segmenten toe als er geen tekst is
                    translated_transcriptions.extend(batch)
                    continue
                
                # Vertaal de gecombineerde tekst
                translation_result = self.translate_text(
                    combined_text, source_lang, target_lang, service
                )
                
                if translation_result.get("success"):
                    # Split de vertaalde tekst terug in segmenten
                    translated_segments = self._split_translation_back_to_segments(
                        translation_result["translated_text"], batch
                    )
                    
                    # Update segmenten met vertalingen
                    for i, segment in enumerate(batch):
                        if i < len(translated_segments):
                            segment["translated_text"] = translated_segments[i]
                        else:
                            segment["translated_text"] = segment.get("text", "")
                        segment["translation_service"] = translation_result["service"]
                        
                    translated_transcriptions.extend(batch)
                else:
                    # Fallback naar origineel voor deze batch
                    for segment in batch:
                        segment["translated_text"] = segment.get("text", "")
                        segment["translation_service"] = "geen"
                    translated_transcriptions.extend(batch)
                    logger.log_debug(f"⚠️ Vertaling gefaald voor batch {batch_idx}: {translation_result.get('error')}")
                
                # Progress logging
                if (batch_idx + 1) % 5 == 0:
                    logger.log_debug(f"📊 Vertaling voortgang: {batch_idx+1}/{len(batches)} batches")
            
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