"""
Whisper Processor Module voor Magic Time Studio
Handelt speech-to-text transcriptie af met beide Whisper types
"""

import os
from typing import Optional, Dict, Any

# Import beide Whisper types
try:
    from ..standard_whisper import StandardWhisper
    from ..fast_whisper import FastWhisper
    from ..whisper_manager import whisper_manager
except ImportError:
    # Fallback als imports falen
    StandardWhisper = None
    FastWhisper = None
    whisper_manager = None

class WhisperProcessor:
    """Whisper transcriptie module met ondersteuning voor beide types"""
    
    def __init__(self, processing_thread):
        self.processing_thread = processing_thread
        self.standard_whisper = StandardWhisper() if StandardWhisper else None
        self.fast_whisper = FastWhisper() if FastWhisper else None
        self.settings = None  # Instellingen worden later ingesteld
        
        # Initialiseer Whisper manager
        if whisper_manager:
            # Gebruik het model uit de instellingen, niet hardcoded medium
            whisper_type = "fast"  # Default naar fast
            model = "tiny"  # Default naar tiny
            device = "cuda"  # Default naar CUDA
            compute_type = "float16"  # Default naar float16
            
            print(f"🚀 WhisperProcessor initialisatie: {whisper_type} - {model}")
            print(f"🔧 GPU instellingen: device={device}, compute_type={compute_type}")
            
            # Stel GPU instellingen in
            whisper_manager.set_gpu_device(device)
            whisper_manager.set_compute_type(compute_type)
            
            # Initialiseer whisper manager
            whisper_manager.initialize(whisper_type, model)
            
            # Initialiseer ook Fast Whisper met GPU instellingen
            if self.fast_whisper:
                print(f"📥 Laad Fast Whisper model: {model} op {device} ({compute_type})")
                success = self.fast_whisper.load_model(model, device, compute_type)
                if success:
                    print(f"✅ Fast Whisper model geladen: {model} op {device}")
                    
                    # GPU informatie wordt niet meer getoond om spam te voorkomen
                    pass
                else:
                    print(f"❌ Fast Whisper model laden gefaald: {model} op {device}")
                    # Probeer fallback naar CPU als CUDA faalt
                    if device == "cuda":
                        print("🔄 Probeer fallback naar CPU...")
                        success = self.fast_whisper.load_model(model, "cpu", compute_type)
                        if success:
                            print(f"✅ Fast Whisper model geladen op CPU: {model}")
                        else:
                            print(f"❌ CPU fallback ook gefaald: {model}")
        else:
            print("⚠️ Whisper manager niet beschikbaar")
    
    def set_settings(self, settings: dict):
        """Stel instellingen in voor de whisper processor"""
        print(f"🔍 [DEBUG] WhisperProcessor.set_settings: Ontvangen instellingen = {settings}")
        self.settings = settings
        print(f"🔍 [DEBUG] WhisperProcessor.set_settings: self.settings ingesteld = {self.settings}")
        
        # Update whisper manager met nieuwe instellingen
        if whisper_manager and self.settings:
            whisper_type = self.settings.get("whisper_type", "fast")
            if whisper_type == "fast":
                whisper_type = "fast"
            else:
                whisper_type = "standard"
            
            model = self.settings.get("whisper_model", "tiny")
            
            # Haal GPU instellingen op uit settings of gebruik defaults
            device = self.settings.get("whisper_device", "cuda")
            compute_type = self.settings.get("whisper_compute_type", "float16")
            
            print(f"🔄 Whisper instellingen bijgewerkt: type={whisper_type}, model={model}")
            print(f"🔧 GPU instellingen: device={device}, compute_type={compute_type}")
            
            # Stel GPU instellingen in
            whisper_manager.set_gpu_device(device)
            whisper_manager.set_compute_type(compute_type)
            
            # Initialiseer whisper manager
            whisper_manager.initialize(whisper_type, model)
            
            # Initialiseer ook Fast Whisper met nieuwe GPU instellingen
            if self.fast_whisper and whisper_type == "fast":
                print(f"📥 Herlaad Fast Whisper model: {model} op {device} ({compute_type})")
                success = self.fast_whisper.load_model(model, device, compute_type)
                if success:
                    print(f"✅ Fast Whisper model herladen: {model} op {device}")
                    
                    # GPU informatie wordt niet meer getoond om spam te voorkomen
                    pass
            else:
                print(f"❌ Fast Whisper model herladen gefaald: {model} op {device}")
                # Probeer fallback naar CPU als CUDA faalt
                if device == "cuda":
                    print("🔄 Probeer fallback naar CPU...")
                    success = self.fast_whisper.load_model(model, "cpu", compute_type)
                    if success:
                        print(f"✅ Fast Whisper model geladen op CPU: {model}")
                    else:
                        print(f"❌ CPU fallback ook gefaald: {model}")
    
    def transcribe_audio(self, audio_path: str, video_path: str) -> Optional[Dict[str, Any]]:
        """Transcribeer audio naar tekst met geselecteerde Whisper type"""
        try:
            print(f"🔍 [DEBUG] WhisperProcessor.transcribe_audio: self.settings = {self.settings}")
            
            if not whisper_manager:
                print("❌ Whisper manager niet beschikbaar")
                return None
            
            whisper_type = whisper_manager.get_current_type()
            model = whisper_manager.get_current_model()
            
            # Haal GPU instellingen op
            device = whisper_manager.get_gpu_device()
            compute_type = whisper_manager.get_compute_type()
            
            print(f"🎤 Whisper transcriptie ({whisper_type}): {audio_path}")
            print(f"🔍 Gebruik model: {model} op {device} ({compute_type})")
            
            # Update status
            self.processing_thread.status_updated.emit(f"🎤 Audio wordt getranscribeerd met {whisper_type}...")
            self.processing_thread.progress_updated.emit(50.0, f"{whisper_type} transcriptie...")
            
            # GPU informatie wordt niet meer getoond om spam te voorkomen
            pass
            
            # Kies juiste Whisper implementatie
            if whisper_type == "fast":
                if not self.fast_whisper:
                    print("❌ Faster Whisper niet beschikbaar")
                    return None
                
                # Laad model als nodig
                if not self.fast_whisper.is_loaded:
                    self.processing_thread.status_updated.emit(f"📥 Laad Fast Whisper model: {model} op {device}...")
                    self.fast_whisper.load_model(model, device, compute_type)
                elif self.fast_whisper.device != device or self.fast_whisper.compute_type != compute_type:
                    # Herlaad model als device of compute type is gewijzigd
                    self.processing_thread.status_updated.emit(f"🔄 Herlaad Fast Whisper model op {device} ({compute_type})...")
                    print(f"🔄 Herlaad Fast Whisper model op {device} ({compute_type})")
                    self.fast_whisper.load_model(model, device, compute_type)
                
                # Maak voortgang callback voor real-time updates
                def progress_callback(progress: float, message: str):
                    # Update progress bar met transcriptie voortgang
                    # Whisper transcriptie is ongeveer 65% van de totale verwerking
                    whisper_progress = 50.0 + (progress * 15.0)  # 50% tot 65%
                    self.processing_thread.progress_updated.emit(whisper_progress, message)
                    # Stuur ook status update
                    self.processing_thread.status_updated.emit(message)
                
                result = self.fast_whisper.transcribe(audio_path, progress_callback=progress_callback)
                
            else:  # standard
                if not self.standard_whisper:
                    print("❌ Standaard Whisper niet beschikbaar")
                    return None
                
                # Laad model als nodig
                if not self.standard_whisper.is_loaded:
                    self.processing_thread.status_updated.emit(f"📥 Laad Standard Whisper model: {model} op {device}...")
                    self.standard_whisper.load_model(model, device)
                elif hasattr(self.standard_whisper, 'device') and self.standard_whisper.device != device:
                    # Herlaad model als device is gewijzigd
                    self.processing_thread.status_updated.emit(f"🔄 Herlaad Standard Whisper model op {device}...")
                    print(f"🔄 Herlaad Standard Whisper model op {device}")
                    self.standard_whisper.load_model(model, device)
                
                result = self.standard_whisper.transcribe(audio_path)
            
            if result:
                print(f"✅ {whisper_type} transcriptie voltooid op {device}")
                
                # GPU informatie wordt niet meer getoond om spam te voorkomen
                pass
                
                return result
            else:
                print(f"❌ {whisper_type} transcriptie gefaald op {device}")
                return None
            
        except Exception as e:
            print(f"❌ Fout bij Whisper transcriptie: {e}")
            self.processing_thread.error_occurred.emit(f"Whisper transcriptie gefaald: {e}")
            return None
    
    def save_transcript(self, transcript: str, output_path: str) -> bool:
        """Sla transcript op als SRT bestand"""
        try:
            # Maak SRT bestand
            srt_content = f"1\n00:00:00,000 --> 00:00:05,000\n{transcript}\n\n"
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(srt_content)
            
            print(f"💾 Transcript opgeslagen: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Fout bij opslaan transcript: {e}")
            return False
    
    def get_whisper_info(self) -> Dict[str, Any]:
        """Krijg informatie over beschikbare Whisper types"""
        return {
            "fast_whisper": self.fast_whisper is not None,
            "standard_whisper": self.standard_whisper is not None,
            "current_type": whisper_manager.get_current_type() if whisper_manager else None,
            "current_model": whisper_manager.get_current_model() if whisper_manager else None,
            "gpu_device": whisper_manager.get_gpu_device() if whisper_manager else None,
            "compute_type": whisper_manager.get_compute_type() if whisper_manager else None
        }
