"""
VAD (Voice Activity Detection) functionaliteit voor WhisperX
Beheert VAD instellingen, testen en optimalisatie
"""

import os
from typing import Dict, Any, List, Optional

class VADManager:
    """Beheert VAD instellingen en functionaliteit voor WhisperX"""
    
    def __init__(self):
        # Standaard VAD instellingen
        self.default_settings = {
            "vad_method": "Pyannote (nauwkeurig)",
            "vad_threshold": 0.5,
            "vad_onset": 0.5,
            "vad_chunk_size": 30
        }
        
        # VAD methode mapping
        self.vad_method_map = {
            "Silero (snel)": "silero",
            "Pyannote (nauwkeurig)": "pyannote",
            "Energie-gebaseerd": "auditok"
        }
        
        # Standaard VAD instellingen
        self.default_vad_settings = {
            "vad_enabled": False,
            "vad_method": "Pyannote (nauwkeurig)",
            "vad_threshold": 0.5,
            "vad_onset": 0.5,
            "vad_offset": 0.5,
            "vad_chunk_size": 30,
            "vad_min_speech": 0.5,
            "vad_min_silence": 0.5
        }
    
    def convert_vad_method(self, ui_method: str) -> str:
        """Converteer UI VAD methode naar WhisperX formaat"""
        return self.vad_method_map.get(ui_method, "silero")
    
    def create_vad_options(self, vad_settings: Dict[str, Any]) -> Dict[str, Any]:
        """Maak VAD opties voor WhisperX"""
        vad_options = {
            "chunk_size": vad_settings.get("vad_chunk_size", 30),
            "vad_onset": vad_settings.get("vad_onset", 0.5),
            "vad_offset": vad_settings.get("vad_offset", 0.5),
        }
        
        # Voeg extra VAD opties toe voor betere controle
        if vad_settings.get("vad_min_speech"):
            vad_options["min_speech_duration_ms"] = int(vad_settings["vad_min_speech"] * 1000)
        if vad_settings.get("vad_min_silence"):
            vad_options["min_silence_duration_ms"] = int(vad_settings["vad_min_silence"] * 1000)
        
        return vad_options
    
    def validate_vad_settings(self, vad_settings: Dict[str, Any]) -> Dict[str, Any]:
        """Valideer en normaliseer VAD instellingen"""
        validated = self.default_vad_settings.copy()
        validated.update(vad_settings)
        
        # Zorg ervoor dat waarden binnen geldige bereiken vallen
        validated["vad_threshold"] = max(0.1, min(0.9, validated["vad_threshold"]))
        validated["vad_onset"] = max(0.1, min(0.9, validated["vad_onset"]))
        validated["vad_offset"] = max(0.1, min(0.9, validated["vad_offset"]))
        validated["vad_chunk_size"] = max(5, min(60, validated["vad_chunk_size"]))
        validated["vad_min_speech"] = max(0.1, min(5.0, validated["vad_min_speech"]))
        validated["vad_min_silence"] = max(0.1, min(5.0, validated["vad_min_silence"]))
        
        return validated

class VADTester:
    """Test VAD instellingen op audio bestanden"""
    
    def __init__(self, whisperx_model):
        self.model = whisperx_model
    
    def test_vad_settings(self, audio_path: str, vad_settings: Dict[str, Any]) -> Dict[str, Any]:
        """Test VAD instellingen op een kort audio fragment"""
        try:
            print(f"🧪 Test VAD instellingen op: {audio_path}")
            
            if not os.path.exists(audio_path):
                print(f"❌ Audio bestand niet gevonden: {audio_path}")
                return {"success": False, "error": "Audio bestand niet gevonden"}
            
            # Controleer of model geladen is
            if not self.model:
                print("❌ WhisperX model niet geladen")
                return {"success": False, "error": "Model niet geladen"}
            
            # Converteer VAD methode naar WhisperX formaat
            vad_method_map = {
                "Silero (snel)": "silero",
                "Pyannote (nauwkeurig)": "pyannote",
                "Energie-gebaseerd": "energy"
            }
            whisperx_vad_method = vad_method_map.get(vad_settings.get("vad_method", "Silero (snel)"), "silero")
            
            # Maak VAD opties
            vad_options = {
                "chunk_size": vad_settings.get("vad_chunk_size", 30),
                "vad_onset": vad_settings.get("vad_onset", 0.5),
                "vad_offset": vad_settings.get("vad_offset", 0.5),
            }
            
            # Voeg extra VAD opties toe voor betere controle
            if vad_settings.get("vad_min_speech"):
                vad_options["min_speech_duration_ms"] = int(vad_settings["vad_min_speech"] * 1000)
            if vad_settings.get("vad_min_silence"):
                vad_options["min_silence_duration_ms"] = int(vad_settings["vad_min_silence"] * 1000)
            
            print(f"🔧 Test VAD opties: {vad_options}")
            
            # Test transcriptie met VAD instellingen
            try:
                result = self.model.transcribe(
                    audio_path,
                    language=None,  # Auto-detect
                    verbose=False,
                    chunk_size=vad_settings.get("vad_chunk_size", 30)
                )
                
                # Analyseer resultaten
                segments = result.get('segments', [])
                total_duration = 0
                speech_duration = 0
                
                for segment in segments:
                    segment_duration = segment.get('end', 0) - segment.get('start', 0)
                    total_duration = max(total_duration, segment.get('end', 0))
                    speech_duration += segment_duration
                
                # Bereken VAD metrics
                if total_duration > 0:
                    speech_ratio = speech_duration / total_duration
                    silence_ratio = 1.0 - speech_ratio
                    avg_segment_length = speech_duration / len(segments) if segments else 0
                else:
                    speech_ratio = 0
                    silence_ratio = 0
                    avg_segment_length = 0
                
                # Bepaal VAD kwaliteit
                vad_quality = "Goed"
                if speech_ratio < 0.1:
                    vad_quality = "Te weinig spraak gedetecteerd"
                elif speech_ratio > 0.9:
                    vad_quality = "Te veel geluid gedetecteerd"
                elif avg_segment_length < 0.5:
                    vad_quality = "Segmenten te kort"
                elif avg_segment_length > 10:
                    vad_quality = "Segmenten te lang"
                
                test_results = {
                    "success": True,
                    "vad_method": whisperx_vad_method,
                    "vad_options": vad_options,
                    "total_duration": total_duration,
                    "speech_duration": speech_duration,
                    "speech_ratio": speech_ratio,
                    "silence_ratio": silence_ratio,
                    "segment_count": len(segments),
                    "avg_segment_length": avg_segment_length,
                    "vad_quality": vad_quality,
                    "segments": segments
                }
                
                print(f"✅ VAD test voltooid: {vad_quality}")
                print(f"📊 Resultaten: spraak={speech_ratio:.1%}, stilte={silence_ratio:.1%}, segmenten={len(segments)}")
                
                return test_results
                
            except Exception as e:
                print(f"❌ Fout bij VAD test transcriptie: {e}")
                return {"success": False, "error": str(e)}
                
        except Exception as e:
            print(f"❌ Fout bij VAD test: {e}")
            return {"success": False, "error": str(e)}

class VADOptimizer:
    """Optimaliseer VAD instellingen voor betere resultaten"""
    
    def __init__(self, vad_tester: VADTester):
        self.vad_tester = vad_tester
    
    def optimize_vad_settings(self, audio_path: str, target_speech_ratio: float = 0.6) -> Dict[str, Any]:
        """Optimaliseer VAD instellingen voor betere resultaten"""
        try:
            print(f"🔧 Optimaliseer VAD instellingen voor: {audio_path}")
            print(f"🎯 Doel spraak ratio: {target_speech_ratio:.1%}")
            
            # Test verschillende VAD instellingen
            test_configs = [
                {"vad_method": "Silero (snel)", "vad_threshold": 0.3, "vad_onset": 0.3, "vad_chunk_size": 30},
                {"vad_method": "Silero (snel)", "vad_threshold": 0.5, "vad_onset": 0.5, "vad_chunk_size": 30},
                {"vad_method": "Silero (snel)", "vad_threshold": 0.7, "vad_onset": 0.7, "vad_chunk_size": 30},
                {"vad_method": "Pyannote (nauwkeurig)", "vad_threshold": 0.5, "vad_onset": 0.5, "vad_chunk_size": 30},
                {"vad_method": "Energie-gebaseerd", "vad_threshold": 0.1, "vad_onset": 0.1, "vad_chunk_size": 30},
            ]
            
            best_config = None
            best_score = float('inf')
            
            for config in test_configs:
                print(f"🧪 Test configuratie: {config}")
                
                # Test deze configuratie
                test_result = self.vad_tester.test_vad_settings(audio_path, config)
                
                if test_result.get("success"):
                    # Bereken score (hoe dichter bij doel, hoe beter)
                    speech_ratio = test_result.get("speech_ratio", 0)
                    score = abs(speech_ratio - target_speech_ratio)
                    
                    print(f"📊 Score: {score:.3f} (spraak ratio: {speech_ratio:.1%})")
                    
                    if score < best_score:
                        best_score = score
                        best_config = config.copy()
                        best_config.update(test_result)
                        print(f"🏆 Nieuwe beste configuratie gevonden!")
                else:
                    print(f"❌ Configuratie gefaald: {test_result.get('error')}")
            
            if best_config:
                print(f"✅ Beste VAD configuratie gevonden:")
                print(f"🎯 Methode: {best_config['vad_method']}")
                print(f"🎯 Threshold: {best_config['vad_threshold']}")
                print(f"🎯 Onset: {best_config['vad_onset']}")
                print(f"🎯 Score: {best_score:.3f}")
                print(f"🎯 Spraak ratio: {best_config.get('speech_ratio', 0):.1%}")
                
                return best_config
            else:
                print("❌ Geen werkende VAD configuratie gevonden")
                return {"success": False, "error": "Geen werkende configuratie"}
                
        except Exception as e:
            print(f"❌ Fout bij VAD optimalisatie: {e}")
            return {"success": False, "error": str(e)}
