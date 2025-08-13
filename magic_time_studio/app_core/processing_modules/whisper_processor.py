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
            # Detecteer automatisch beste device en compute type
            whisper_type = "fast"  # Default naar fast
            model = "tiny"  # Default naar tiny
            
            # Detecteer automatisch beste device
            device, compute_type = self._detect_best_device()
            
            print(f"🚀 WhisperProcessor initialisatie: {whisper_type} - {model}")
            print(f"🔧 Detectie resultaat: device={device}, compute_type={compute_type}")
            
            # Stel GPU instellingen in
            whisper_manager.set_gpu_device(device)
            whisper_manager.set_compute_type(compute_type)
            
            # Initialiseer whisper manager
            whisper_manager.initialize(whisper_type, model)
            
            # Initialiseer ook Fast Whisper met gedetecteerde instellingen
            if self.fast_whisper:
                print(f"📥 Laad Fast Whisper model: {model} op {device} ({compute_type})")
                success = self.fast_whisper.load_model(model, device, compute_type)
                if success:
                    print(f"✅ Fast Whisper model geladen: {model} op {device}")
                else:
                    print(f"❌ Fast Whisper model laden gefaald: {model} op {device}")
                    # Probeer fallback naar CPU als GPU faalt
                    if device != "cpu":
                        print("🔄 Probeer fallback naar CPU...")
                        success = self.fast_whisper.load_model(model, "cpu", "float32")
                        if success:
                            print(f"✅ Fast Whisper model geladen op CPU: {model}")
                            # Update whisper manager met CPU instellingen
                            whisper_manager.set_gpu_device("cpu")
                            whisper_manager.set_compute_type("float32")
                        else:
                            print(f"❌ CPU fallback ook gefaald: {model}")
        else:
            print("⚠️ Whisper manager niet beschikbaar")
    
    def _detect_best_device(self):
        """Detecteer automatisch beste device en compute type"""
        try:
            import torch
            if torch.cuda.is_available():
                # CUDA beschikbaar - gebruik GPU
                device = "cuda"
                compute_type = "float16"
                print("✅ CUDA gedetecteerd - gebruik GPU")
            else:
                # Geen CUDA - gebruik CPU
                device = "cpu"
                compute_type = "float32"
                print("⚠️ CUDA niet beschikbaar - gebruik CPU")
        except ImportError:
            # PyTorch niet beschikbaar - gebruik CPU
            device = "cpu"
            compute_type = "float32"
            print("⚠️ PyTorch niet beschikbaar - gebruik CPU")
        except Exception as e:
            # Fallback naar CPU bij fouten
            device = "cpu"
            compute_type = "float32"
            print(f"⚠️ Fout bij device detectie: {e} - gebruik CPU")
        
        return device, compute_type
    
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
            
            # Gebruik gedetecteerde device in plaats van hardcoded CUDA
            device, compute_type = self._detect_best_device()
            
            print(f"🔄 Whisper instellingen bijgewerkt: type={whisper_type}, model={model}")
            print(f"🔧 Device instellingen: device={device}, compute_type={compute_type}")
            
            # Stel device instellingen in
            whisper_manager.set_gpu_device(device)
            whisper_manager.set_compute_type(compute_type)
            
            # Initialiseer whisper manager
            whisper_manager.initialize(whisper_type, model)
            
            # Initialiseer ook Fast Whisper met nieuwe instellingen
            if self.fast_whisper and whisper_type == "fast":
                print(f"📥 Herlaad Fast Whisper model: {model} op {device} ({compute_type})")
                success = self.fast_whisper.load_model(model, device, compute_type)
                if success:
                    print(f"✅ Fast Whisper model herladen: {model} op {device}")
                else:
                    print(f"❌ Fast Whisper model herladen gefaald: {model} op {device}")
                    # Probeer fallback naar CPU als GPU faalt
                    if device != "cpu":
                        print("🔄 Probeer fallback naar CPU...")
                        success = self.fast_whisper.load_model(model, "cpu", "float32")
                        if success:
                            print(f"✅ Fast Whisper model geladen op CPU: {model}")
                            # Update whisper manager met CPU instellingen
                            whisper_manager.set_gpu_device("cpu")
                            whisper_manager.set_compute_type("float32")
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
            
            # Haal device instellingen op
            device = whisper_manager.get_gpu_device()
            compute_type = whisper_manager.get_compute_type()
            
            print(f"🎤 Whisper transcriptie ({whisper_type}): {audio_path}")
            print(f"🔍 Gebruik model: {model} op {device} ({compute_type})")
            
            # Update status
            self.processing_thread.status_updated.emit(f"🎤 Audio wordt getranscribeerd met {whisper_type}...")
            self.processing_thread.progress_updated.emit(50.0, f"{whisper_type} transcriptie...")
            
            # Kies juiste Whisper implementatie
            if whisper_type == "fast":
                if not self.fast_whisper:
                    print("❌ Faster Whisper niet beschikbaar")
                    return None
                
                # Laad model als nodig
                if not self.fast_whisper.is_loaded:
                    self.processing_thread.status_updated.emit(f"📥 Laad Fast Whisper model: {model} op {device}...")
                    success = self.fast_whisper.load_model(model, device, compute_type)
                    if not success and device != "cpu":
                        # Probeer CPU fallback
                        print("🔄 Probeer CPU fallback...")
                        success = self.fast_whisper.load_model(model, "cpu", "float32")
                        if success:
                            device = "cpu"
                            compute_type = "float32"
                            # Update whisper manager
                            whisper_manager.set_gpu_device("cpu")
                            whisper_manager.set_compute_type("float32")
                
                elif self.fast_whisper.device != device or self.fast_whisper.compute_type != compute_type:
                    # Herlaad model als device of compute type is gewijzigd
                    self.processing_thread.status_updated.emit(f"🔄 Herlaad Fast Whisper model op {device} ({compute_type})...")
                    print(f"🔄 Herlaad Fast Whisper model op {device} ({compute_type})")
                    success = self.fast_whisper.load_model(model, device, compute_type)
                    if not success and device != "cpu":
                        # Probeer CPU fallback
                        print("🔄 Probeer CPU fallback...")
                        success = self.fast_whisper.load_model(model, "cpu", "float32")
                        if success:
                            device = "cpu"
                            compute_type = "float32"
                            # Update whisper manager
                            whisper_manager.set_gpu_device("cpu")
                            whisper_manager.set_compute_type("float32")
                
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
                    success = self.standard_whisper.load_model(model, device)
                    if not success and device != "cpu":
                        # Probeer CPU fallback
                        print("🔄 Probeer CPU fallback...")
                        success = self.standard_whisper.load_model(model, "cpu")
                        if success:
                            device = "cpu"
                            # Update whisper manager
                            whisper_manager.set_gpu_device("cpu")
                
                elif hasattr(self.standard_whisper, 'device') and self.standard_whisper.device != device:
                    # Herlaad model als device is gewijzigd
                    self.processing_thread.status_updated.emit(f"🔄 Herlaad Standard Whisper model op {device}...")
                    print(f"🔄 Herlaad Standard Whisper model op {device}")
                    success = self.standard_whisper.load_model(model, device)
                    if not success and device != "cpu":
                        # Probeer CPU fallback
                        print("🔄 Probeer CPU fallback...")
                        success = self.standard_whisper.load_model(model, "cpu")
                        if success:
                            device = "cpu"
                            # Update whisper manager
                            whisper_manager.set_gpu_device("cpu")
                
                result = self.standard_whisper.transcribe(audio_path)
            
            if result:
                print(f"✅ {whisper_type} transcriptie voltooid op {device}")
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
