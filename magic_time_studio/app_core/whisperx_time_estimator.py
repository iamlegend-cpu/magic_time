"""
Time Estimator voor WhisperX
Berekent ETA voor WhisperX transcripties gebaseerd op audio lengte en model
"""

import os
import platform
import subprocess
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

class TimeEstimator:
    """Berekent ETA voor WhisperX transcripties gebaseerd op audio lengte en model"""
    
    def __init__(self):
        # Gemiddelde verwerkingstijden per minuut audio (in seconden)
        # Deze zijn gebaseerd op RTX 3050 Laptop GPU met float16
        self.processing_times = {
            "tiny": {"transcription": 0.5, "alignment": 0.3},      # ~0.8s per minuut
            "base": {"transcription": 1.0, "alignment": 0.5},      # ~1.5s per minuut  
            "small": {"transcription": 1.5, "alignment": 0.8},     # ~2.3s per minuut
            "medium": {"transcription": 2.5, "alignment": 1.2},    # ~3.7s per minuut
            "large": {"transcription": 4.0, "alignment": 2.0},     # ~6.0s per minuut
            "large-v2": {"transcription": 4.5, "alignment": 2.5},  # ~7.0s per minuut
            "large-v3": {"transcription": 5.0, "alignment": 3.0},  # ~8.0s per minuut
        }
        
        # CPU fallback tijden (langzamer)
        self.cpu_multiplier = 3.0
        
    def estimate_time(self, audio_duration: float, model_name: str, device: str = "cuda") -> Optional[Dict[str, Any]]:
        """Bereken geschatte verwerkingstijd voor audio"""
        try:
            # Haal model tijden op
            if model_name not in self.processing_times:
                model_name = "large-v3"  # Default fallback
                
            model_times = self.processing_times[model_name]
            
            # Bereken totale tijd per minuut
            if device == "cuda":
                time_per_minute = model_times["transcription"] + model_times["alignment"]
            else:
                # CPU is langzamer
                time_per_minute = (model_times["transcription"] + model_times["alignment"]) * self.cpu_multiplier
            
            # Bereken totale geschatte tijd
            audio_minutes = audio_duration / 60.0
            total_estimated_seconds = time_per_minute * audio_minutes
            
            # Voeg wat buffer toe voor onzekerheid
            total_estimated_seconds *= 1.2
            
            # Converteer naar timedelta
            estimated_duration = timedelta(seconds=int(total_estimated_seconds))
            
            # Bereken ETA
            start_time = datetime.now()
            eta = start_time + estimated_duration
            
            return {
                "audio_duration_minutes": round(audio_minutes, 1),
                "time_per_minute": round(time_per_minute, 1),
                "total_estimated_seconds": int(total_estimated_seconds),
                "estimated_duration": estimated_duration,
                "start_time": start_time,
                "eta": eta,
                "model": model_name,
                "device": device
            }
            
        except Exception as e:
            print(f"⚠️ Kon ETA niet berekenen: {e}")
            return None
    
    def get_audio_duration(self, audio_path: str) -> Optional[float]:
        """Haal audio duur op in seconden"""
        try:
            import librosa
            duration = librosa.get_duration(path=audio_path)
            return duration
        except ImportError:
            # Fallback: probeer met ffprobe
            try:
                import subprocess
                result = subprocess.run([
                    "ffprobe", "-v", "quiet", "-show_entries", 
                    "format=duration", "-of", "csv=p=0", audio_path
                ], capture_output=True, text=True)
                if result.returncode == 0:
                    return float(result.stdout.strip())
            except:
                pass
        except Exception as e:
            print(f"⚠️ Kon audio duur niet bepalen: {e}")
        
        return None
    
    def format_eta(self, eta_dict: Dict[str, Any]) -> str:
        """Format ETA naar leesbare string"""
        if not eta_dict:
            return "Onbekend"
            
        eta_time = eta_dict["eta"]
        duration = eta_dict["estimated_duration"]
        
        # Format duur
        if duration.total_seconds() < 60:
            duration_str = f"{int(duration.total_seconds())}s"
        elif duration.total_seconds() < 3600:
            minutes = int(duration.total_seconds() // 60)
            seconds = int(duration.total_seconds() % 60)
            duration_str = f"{minutes}m {seconds}s"
        else:
            hours = int(duration.total_seconds() // 3600)
            minutes = int((duration.total_seconds() % 3600) // 60)
            duration_str = f"{hours}u {minutes}m"
        
        # Format ETA tijd
        eta_str = eta_time.strftime("%H:%M:%S")
        
        return f"Geschatte tijd: {duration_str} | Klaar om: {eta_str}"
