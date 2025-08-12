"""
Translation Processor Module voor Magic Time Studio
Handelt vertaling van transcripties af
"""

import os
import requests
from typing import Optional, Dict, Any, List

class TranslationProcessor:
    """Vertaling module met LibreTranslate ondersteuning"""
    
    def __init__(self, processing_thread):
        self.processing_thread = processing_thread
        self.settings = None  # Instellingen worden later ingesteld
        # Haal server URL op uit instellingen of gebruik default
        self.server_url = self._get_server_url()
        # Haal target language op uit instellingen of gebruik default
        self.target_language = self._get_target_language()
    
    def set_settings(self, settings: dict):
        """Stel instellingen in voor de translation processor"""
        print(f"🔍 [DEBUG] TranslationProcessor.set_settings: Ontvangen instellingen = {settings}")
        self.settings = settings
        print(f"🔍 [DEBUG] TranslationProcessor.set_settings: self.settings ingesteld = {self.settings}")
        
        # Update server URL en target language uit nieuwe instellingen
        if self.settings:
            if 'libretranslate_server' in self.settings:
                self.server_url = self.settings['libretranslate_server']
                print(f"🔍 [DEBUG] TranslationProcessor.set_settings: Server URL ingesteld op {self.server_url}")
            if 'target_language' in self.settings:
                self.target_language = self.settings['target_language']
                print(f"🔍 [DEBUG] TranslationProcessor.set_settings: Target language ingesteld op {self.target_language}")
            if 'translator' in self.settings:
                translator = self.settings['translator']
                print(f"🔍 [DEBUG] TranslationProcessor.set_settings: Translator ingesteld op {translator}")
                # Als vertaling is uitgeschakeld, gebruik originele tekst
                if translator == "none":
                    print(f"🔍 [DEBUG] TranslationProcessor.set_settings: Vertaling uitgeschakeld, gebruik originele tekst")
                    self.server_url = ""  # Lege server URL betekent geen vertaling
    
    def _get_server_url(self) -> str:
        """Haal server URL op uit instellingen"""
        try:
            # Probeer server URL uit instellingen te halen
            if hasattr(self.processing_thread, 'settings') and self.processing_thread.settings:
                server_url = self.processing_thread.settings.get('libretranslate_server')
                if server_url:
                    return server_url
        except:
            pass
        
        # Fallback naar default server
        return "http://100.90.127.78:5000"
    
    def _get_target_language(self) -> str:
        """Haal target language op uit instellingen"""
        try:
            # Probeer target language uit instellingen te halen
            if hasattr(self.processing_thread, 'settings') and self.processing_thread.settings:
                target_lang = self.processing_thread.settings.get('target_language')
                if target_lang:
                    return target_lang
        except:
            pass
        
        # Fallback naar default taal
        return "nl"
    
    def set_server(self, server_url: str):
        """Stel LibreTranslate server in"""
        self.server_url = server_url
    
    def set_target_language(self, target_lang: str):
        """Stel doeltaal in"""
        self.target_language = target_lang
    
    def translate_text(self, text: str, source_lang: str = "auto") -> Optional[str]:
        """Vertaal enkele tekst"""
        try:
            # Controleer of vertaling is ingeschakeld
            if not self.server_url or self.server_url == "":
                print(f"🔍 [DEBUG] TranslationProcessor.translate_text: Vertaling uitgeschakeld, gebruik originele tekst")
                return text
            
            payload = {
                "q": text,
                "source": source_lang,
                "target": self.target_language,
                "format": "text"
            }
            
            response = requests.post(
                f"{self.server_url}/translate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("translatedText", text)
            else:
                print(f"❌ Vertaling fout: {response.status_code} - {response.text}")
                return text
                
        except Exception as e:
            print(f"❌ Fout bij vertaling: {e}")
            return text
    
    def translate_bulk_texts(self, texts: List[str], source_lang: str = "auto") -> List[str]:
        """Vertaal meerdere teksten in één keer voor betere prestaties"""
        try:
            # Controleer of vertaling is ingeschakeld
            if not self.server_url or self.server_url == "":
                print(f"🔍 [DEBUG] TranslationProcessor.translate_bulk_texts: Vertaling uitgeschakeld, gebruik originele teksten")
                return texts
            
            if not texts:
                return []
            
            # Combineer alle teksten met scheidingstekens voor bulk vertaling
            # LibreTranslate ondersteunt bulk vertaling door meerdere teksten te combineren
            combined_text = "\n---SEGMENT---\n".join(texts)
            
            payload = {
                "q": combined_text,
                "source": source_lang,
                "target": self.target_language,
                "format": "text"
            }
            
            print(f"📤 Bulk vertaling: {len(texts)} teksten gecombineerd tot één request")
            
            response = requests.post(
                f"{self.server_url}/translate",
                json=payload,
                timeout=60  # Langere timeout voor bulk vertaling
            )
            
            if response.status_code == 200:
                result = response.json()
                translated_combined = result.get("translatedText", combined_text)
                
                # Split de vertaalde tekst terug in segmenten
                translated_segments = translated_combined.split("\n---SEGMENT---\n")
                
                # Zorg ervoor dat we evenveel segmenten hebben als origineel
                if len(translated_segments) != len(texts):
                    print(f"⚠️ Aantal vertaalde segmenten ({len(translated_segments)}) komt niet overeen met origineel ({len(texts)})")
                    # Fallback: gebruik originele teksten voor ontbrekende segmenten
                    while len(translated_segments) < len(texts):
                        translated_segments.append("")
                    translated_segments = translated_segments[:len(texts)]
                
                print(f"✅ Bulk vertaling succesvol: {len(translated_segments)} segmenten vertaald")
                return translated_segments
                
            else:
                print(f"❌ Bulk vertaling fout: {response.status_code} - {response.text}")
                # Fallback naar individuele vertaling
                print("🔄 Fallback naar individuele vertaling...")
                return [self.translate_text(text, source_lang) for text in texts]
                
        except Exception as e:
            print(f"❌ Fout bij bulk vertaling: {e}")
            # Fallback naar individuele vertaling
            print("🔄 Fallback naar individuele vertaling...")
            return [self.translate_text(text, source_lang) for text in texts]
    
    def translate_content(self, transcript: str, transcriptions: List[Dict[str, Any]], 
                         source_language: str = "auto") -> tuple:
        """Vertaal transcript en transcriptie segmenten in één keer voor betere prestaties"""
        try:
            print(f"🔍 [DEBUG] TranslationProcessor.translate_content: self.settings = {self.settings}")
            print(f"🔍 [DEBUG] TranslationProcessor.translate_content: self.server_url = {self.server_url}")
            
            # Controleer of vertaling is ingeschakeld
            if not self.server_url or self.server_url == "":
                print(f"🔍 [DEBUG] TranslationProcessor.translate_content: Vertaling uitgeschakeld, gebruik originele tekst")
                return transcript, transcriptions
            
            print(f"🌐 Start vertaling naar {self.target_language}")
            
            # Bereid alle segment teksten voor voor bulk vertaling
            segment_texts = [segment["text"] for segment in transcriptions]
            total_segments = len(transcriptions)
            
            # Update progress voor bulk vertaling
            self.processing_thread.progress_updated.emit(
                25, 
                f"Bereid {total_segments} segmenten voor bulk vertaling..."
            )
            
            # Vertaal alle segment teksten in één keer
            print(f"🚀 Bulk vertaling van {total_segments} segmenten...")
            translated_segment_texts = self.translate_bulk_texts(segment_texts, source_language)
            
            # Update progress
            self.processing_thread.progress_updated.emit(
                35, 
                f"Verwerk vertaalde segmenten..."
            )
            
            # Vertaal hoofdtranscript
            translated_transcript = self.translate_text(transcript, source_language)
            
            # Maak vertaalde transcripties aan
            translated_transcriptions = []
            for i, (segment, translated_text) in enumerate(zip(transcriptions, translated_segment_texts)):
                translated_segment = {
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": translated_text,
                    "original_text": segment["text"]
                }
                translated_transcriptions.append(translated_segment)
            
            print(f"✅ Bulk vertaling voltooid: {len(translated_transcriptions)} segmenten")
            return translated_transcript, translated_transcriptions
            
        except Exception as e:
            print(f"❌ Fout bij vertaling: {e}")
            # Return originele content als vertaling faalt
            return transcript, transcriptions
    
    def detect_language(self, text: str) -> Optional[str]:
        """Detecteer taal van tekst"""
        try:
            # Controleer of vertaling is ingeschakeld
            if not self.server_url or self.server_url == "":
                print(f"🔍 [DEBUG] TranslationProcessor.detect_language: Vertaling uitgeschakeld, gebruik auto detectie")
                return "auto"
            
            payload = {"q": text}
            
            response = requests.post(
                f"{self.server_url}/detect",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result and len(result) > 0:
                    return result[0].get("language", "auto")
            
            return "auto"
            
        except Exception as e:
            print(f"❌ Fout bij taal detectie: {e}")
            return "auto"
    
    def get_available_languages(self) -> List[Dict[str, str]]:
        """Krijg beschikbare talen"""
        try:
            # Controleer of vertaling is ingeschakeld
            if not self.server_url or self.server_url == "":
                print(f"🔍 [DEBUG] TranslationProcessor.get_available_languages: Vertaling uitgeschakeld, geen talen beschikbaar")
                return []
            
            response = requests.get(f"{self.server_url}/languages", timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                return []
                
        except Exception as e:
            print(f"❌ Fout bij ophalen talen: {e}")
            return []
