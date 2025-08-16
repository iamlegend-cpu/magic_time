"""
Transcription Core voor WhisperX
Handelt de daadwerkelijke transcriptie logica af
"""

import os
import time
import shutil
import whisperx
from typing import Dict, Any, List, Optional, Callable

class TranscriptionCore:
    """Core transcriptie logica voor WhisperX"""
    
    def __init__(self, model_manager, time_estimator, vad_integration):
        self.model_manager = model_manager
        self.time_estimator = time_estimator
        self.vad_integration = vad_integration
    
    def transcribe_with_alignment(self, audio_path: str, language: Optional[str] = None, 
                                 progress_callback: Optional[Callable[[float, str], None]] = None,
                                 vad_settings: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Transcribeer audio met WhisperX en word-level alignment"""
        try:
            print(f"🎤 [START] WhisperX transcriptie gestart voor: {os.path.basename(audio_path)}")
            
            # Controleer of audio bestand bestaat
            if not os.path.exists(audio_path):
                print(f"❌ [FOUT] Audio bestand niet gevonden: {audio_path}")
                return None
            
            # Controleer bestandsgrootte
            file_size = os.path.getsize(audio_path)
            print(f"🔍 [INFO] Bestand bestaat: {os.path.exists(audio_path)}")
            print(f"🔍 [INFO] Bestandsgrootte: {file_size} bytes")
            
            # Test of bestand kan worden geopend
            try:
                with open(audio_path, 'rb') as test_file:
                    test_file.read(1024)
                print(f"✅ [INFO] Bestand kan worden geopend en gelezen")
            except Exception as e:
                print(f"❌ [FOUT] Bestand kan niet worden geopend: {e}")
                return None
            
            # Voer transcriptie uit
            result = self._perform_basic_transcription(audio_path, language, progress_callback, vad_settings)
            if result:
                print(f"✅ [VOLTOOID] WhisperX transcriptie succesvol voltooid")
                return result
            else:
                print(f"❌ [FOUT] WhisperX transcriptie gefaald")
                return None
                
        except Exception as e:
            print(f"❌ [FOUT] Fout tijdens WhisperX transcriptie: {e}")
            return None
    
    def _show_eta(self, audio_path: str, progress_callback: Optional[Callable[[float, str], None]], model_name: str = None):
        """Toon ETA informatie"""
        audio_duration = self.time_estimator.get_audio_duration(audio_path)
        if audio_duration:
            # Gebruik doorgegeven model naam of haal op uit model manager
            if not model_name:
                model_name = getattr(self.model_manager.model, 'name', 'large-v3')
            
            print(f"🔧 [DEBUG] ETA berekening voor model: {model_name}")
            eta_info = self.time_estimator.estimate_time(audio_duration, model_name, self.model_manager.device)
            if eta_info:
                eta_message = self.time_estimator.format_eta(eta_info)
                print(f"⏱️ {eta_message}")
                if progress_callback:
                    progress_callback(0.02, f"⏱️ {eta_message}")
            else:
                print(f"⏱️ Audio duur: {audio_duration:.1f}s | Model: {model_name}")
        else:
            print("⏱️ Kon audio duur niet bepalen voor ETA")
    
    def _perform_basic_transcription(self, audio_path: str, language: Optional[str] = None, 
                                    progress_callback: Optional[Callable[[float, str], None]] = None,
                                    vad_settings: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Voer basis transcriptie uit met WhisperX"""
        try:
            print(f"🔧 [BEZIG] Start basis transcriptie...")
            
            # Laad VAD instellingen uit configuratie als niet opgegeven
            if vad_settings is None:
                vad_settings = self.vad_integration.get_vad_settings()
            
            # VAD is ALTIJD ingeschakeld voor WhisperX
            vad_enabled = True
            if not vad_settings:
                vad_settings = {
                    "vad_enabled": True,
                    "vad_method": "Pyannote (nauwkeurig)",
                    "vad_threshold": 0.5,
                    "vad_onset": 0.5,
                    "vad_chunk_size": 30,
                    "vad_min_speech": 0.5,
                    "vad_min_silence": 0.5,
                }
            else:
                vad_settings["vad_enabled"] = True  # Forceer VAD aan
            
            print(f"🔧 [INFO] VAD altijd ingeschakeld voor WhisperX transcriptie")
            
            # Bereken ETA voor deze transcriptie
            # Haal model naam op uit VAD instellingen of gebruik standaard
            model_name = vad_settings.get('whisper_model', 'large-v3') if vad_settings else 'large-v3'
            self._show_eta(audio_path, progress_callback, model_name)
            
            # Wacht even tot het bestand volledig is geschreven
            print(f"⏳ [BEZIG] Wacht tot bestand volledig is geschreven...")
            time.sleep(1)
            
            # Kopieer het bestand naar een eenvoudiger pad om WhisperX problemen te voorkomen
            try:
                simple_filename = "whisperx_audio.wav"
                simple_path = os.path.join(os.path.dirname(audio_path), simple_filename)
                shutil.copy2(audio_path, simple_path)
                print(f"✅ [INFO] Bestand gekopieerd naar eenvoudig pad: {simple_path}")
                time.sleep(0.5)
                if os.path.exists(simple_path):
                    audio_path = simple_path
                    print(f"✅ [INFO] Gebruik gekopieerd bestand: {audio_path}")
                else:
                    print(f"⚠️ [WAARSCHUWING] Gekopieerd bestand niet gevonden, gebruik origineel")
            except Exception as e:
                print(f"⚠️ [WAARSCHUWING] Fout bij kopiëren bestand: {e}")
            
            # Converteer Windows pad naar formaat dat WhisperX kan begrijpen
            try:
                if os.name == 'nt':
                    audio_path = os.path.abspath(audio_path)
                    audio_path = os.path.normpath(audio_path)
                    alt_path = audio_path.replace('\\', '/')
                    if os.path.exists(alt_path):
                        audio_path = alt_path
                        print(f"✅ [INFO] Pad geconverteerd naar forward slashes: {audio_path}")
                    else:
                        print(f"⚠️ [WAARSCHUWING] Forward slash conversie niet succesvol, gebruik origineel pad")
                else:
                    audio_path = os.path.abspath(os.path.normpath(audio_path))
            except Exception as e:
                print(f"⚠️ [WAARSCHUWING] Fout bij pad conversie: {e}")
            
            # Test of het bestand daadwerkelijk kan worden geopend
            try:
                with open(audio_path, 'rb') as test_file:
                    test_file.read(1024)
                print(f"✅ [INFO] Bestand kan worden geopend en gelezen")
            except Exception as e:
                print(f"❌ [FOUT] Bestand kan niet worden geopend: {e}")
                return None
            
            # Test of WhisperX het bestand kan vinden door het pad te controleren
            print(f"🔍 [INFO] Finale pad voor WhisperX: {audio_path}")
            print(f"🔍 [INFO] Pad type: {type(audio_path)}")
            print(f"🔍 [INFO] Pad encoding: {audio_path.encode('utf-8') if isinstance(audio_path, str) else 'N/A'}")
            
            # WhisperX transcriptie MET VAD (altijd)
            print(f"🎯 [START] WhisperX transcriptie gestart met VAD")
            print(f"🔧 [INFO] VAD instellingen: methode={vad_settings.get('vad_method', 'silero')}, threshold={vad_settings.get('vad_threshold', 0.5):.2f}, onset={vad_settings.get('vad_onset', 0.5):.2f}")
            
            # Start progress tracking voor transcriptie
            if progress_callback:
                progress_callback(50.0, "WhisperX transcriptie gestart...")
            
            # Start tijd tracking voor ETA berekening
            start_time = time.time()
            audio_duration = self.time_estimator.get_audio_duration(audio_path)
            
                         # Progress tracking tijdens transcriptie (UITGESCHAKELD - te veel console output)
             # def progress_wrapper(current_progress):
             #     if progress_callback and audio_duration:
             #         # Bereken progress op basis van verstreken tijd vs verwachte tijd
             #         elapsed = time.time() - start_time
             #         expected_time = self.time_estimator.estimate_time(audio_duration, 
             #                                                        getattr(self.model_manager.model, 'name', 'large-v3'), 
             #                                                        self.model_manager.device)
             #         if expected_time and expected_time.get('total_time'):
             #         # Bereken progress percentage (50-90% voor transcriptie)
             #         progress_percent = 50.0 + (elapsed / expected_time['total_time']) * 40.0
             #         progress_percent = min(90.0, max(50.0, progress_percent))
             #         
             #         # Stuur progress update elke 2 seconden
             #         if int(elapsed) % 2 == 0:
             #         progress_callback(progress_percent, f"WhisperX transcriptie... ({progress_percent:.1f}%)")
             #         print(f"🔧 [DEBUG] Progress update: {progress_percent:.1f}% - elapsed: {elapsed:.1f}s")
            
                         # Start progress timer (UITGESCHAKELD - te veel console output)
             # import threading
             # progress_thread = threading.Thread(target=self._progress_timer, args=(progress_wrapper,))
             # progress_thread.daemon = True
             # progress_thread.start()
            
            result = self.model_manager.model.transcribe(
                audio_path,
                language=language,
                chunk_size=vad_settings.get("vad_chunk_size", 30)
            )
            
            # Stop progress tracking
            if progress_callback:
                progress_callback(90.0, "WhisperX transcriptie voltooid")
            
            if result:
                print(f"✅ [VOLTOOID] WhisperX transcriptie succesvol")
                return result
            else:
                print(f"❌ [FOUT] WhisperX transcriptie gaf geen resultaat")
                return None
                
        except Exception as e:
            print(f"❌ [FOUT] Fout tijdens basis transcriptie: {e}")
            return None
    
    def _progress_timer(self, progress_wrapper):
        """Progress timer voor real-time updates"""
        try:
            while True:
                progress_wrapper(None)
                time.sleep(2)  # Update elke 2 seconden
        except Exception as e:
            print(f"⚠️ [WAARSCHUWING] Progress timer fout: {e}")
    
    def _detect_language(self, result: Dict[str, Any], language: Optional[str], 
                         progress_callback: Optional[Callable[[float, str], None]]) -> str:
        """Detecteer of gebruik ingestelde taal"""
        if progress_callback:
            progress_callback(0.35, "🎤 WhisperX: Language detection...")
        
        # Voer alleen taal detectie uit als geen taal is ingesteld
        if language is None:
            language = result["language"]
            print(f"🌍 Gedetecteerde taal: {language}")
        else:
            print(f"🌍 Gebruik ingestelde taal: {language}")
        
        if progress_callback:
            progress_callback(0.4, f"🌍 Taal: {language}")
        
        return language
    
    def _perform_word_alignment(self, result: Dict[str, Any], audio_path: str, language: str,
                               progress_callback: Optional[Callable[[float, str], None]]) -> Optional[Dict[str, Any]]:
        """Voer word-level alignment uit"""
        if progress_callback:
            progress_callback(0.45, "🎤 WhisperX: Alignment model laden...")
        
        # Laad juiste alignment model voor de taal
        try:
            if self.model_manager.align_model is None:
                print(f"🔍 Laad alignment model voor taal: {language}")
                self.model_manager.align_model, self.model_manager.align_extend = whisperx.load_align_model(
                    language_code=language,
                    device=self.model_manager.device
                )
                print(f"✅ Alignment model geladen voor taal: {language}")
            else:
                print(f"✅ Alignment model al geladen")
        except Exception as e:
            print(f"❌ Kon alignment model niet laden voor taal {language}: {e}")
            return None
        
        # Stap 3: Word-level alignment (50% van de tijd)
        if progress_callback:
            progress_callback(0.5, "🎤 WhisperX: Word-level alignment...")
        
        try:
            # Voer word-level alignment uit
            result = whisperx.align(
                result["segments"],
                self.model_manager.align_model,
                self.model_manager.align_extend,
                audio_path,
                self.model_manager.device,
                return_char_alignments=False
            )
            
            if progress_callback:
                progress_callback(0.9, "🎤 WhisperX: Word-level alignment voltooid")
            
            print(f"✅ Word-level alignment voltooid: {len(result.get('segments', []))} segmenten")
            return result
            
        except Exception as e:
            print(f"❌ Fout bij word-level alignment: {e}")
            return None
    
    def _convert_to_standard_format(self, result: Dict[str, Any], language: str,
                                   progress_callback: Optional[Callable[[float, str], None]]) -> Optional[Dict[str, Any]]:
        """Converteer naar standaard formaat"""
        if progress_callback:
            progress_callback(0.95, "🎤 WhisperX: Converteer naar standaard formaat...")
        
        try:
            # Converteer naar standaard formaat
            from ..whisperx_utils import convert_to_standard_format
            transcriptions = convert_to_standard_format(result)
            
            if progress_callback:
                progress_callback(1.0, "🎤 WhisperX: Transcriptie voltooid!")
            
            print(f"✅ Transcriptie voltooid: {len(transcriptions)} segmenten")
            
            return {
                "transcriptions": transcriptions,
                "language": language,
                "word_alignments": result.get("word_segments", []),
                "model": "whisperx"
            }
            
        except Exception as e:
            print(f"❌ Fout bij converteren naar standaard formaat: {e}")
            return None
    
    def _create_basic_result(self, result: Dict[str, Any], language: str) -> Dict[str, Any]:
        """Maak basis resultaat zonder alignment"""
        from ..whisperx_utils import convert_to_standard_format
        return {
            "transcriptions": convert_to_standard_format({"segments": result["segments"]}),
            "language": language,
            "word_alignments": [],
            "model": "whisperx"
        }
