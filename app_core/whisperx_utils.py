"""
WhisperX Utilities en Hulpfuncties
Beheert SRT conversie, timestamp formatting en andere utilities
"""

from typing import Dict, Any, List

def convert_to_standard_format(whisperx_result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Converteer WhisperX output naar standaard formaat"""
    transcriptions = []
    
    for segment in whisperx_result["segments"]:
        transcription = {
            "start": segment["start"],
            "end": segment["end"],
            "text": segment["text"].strip(),
            "words": segment.get("words", []),
            "confidence": segment.get("avg_logprob", 0.0)
        }
        transcriptions.append(transcription)
    
    return transcriptions

def create_accurate_srt(transcriptions: List[Dict[str, Any]], 
                       word_alignments: List[Dict[str, Any]] = None) -> str:
    """Genereer SRT met WhisperX word-level timing voor maximale accuracy"""
    srt_content = ""
    
    for i, segment in enumerate(transcriptions, 1):
        # Converteer seconden naar SRT timestamp formaat
        start_time = seconds_to_srt_timestamp(segment["start"])
        end_time = seconds_to_srt_timestamp(segment["end"])
        
        # Gebruik word-level timing als beschikbaar
        if word_alignments and segment.get("words"):
            # Bereken gemiddelde timing per woord voor betere accuracy
            words = segment["words"]
            if words:
                # Gebruik eerste woord start en laatste woord end voor betere segmentatie
                segment["start"] = words[0]["start"]
                segment["end"] = words[-1]["end"]
                start_time = seconds_to_srt_timestamp(segment["start"])
                end_time = seconds_to_srt_timestamp(segment["end"])
        
        srt_content += f"{i}\n{start_time} --> {end_time}\n{segment['text']}\n\n"
    
    return srt_content

def seconds_to_srt_timestamp(seconds: float) -> str:
    """Converteer seconden naar SRT timestamp formaat (HH:MM:SS,mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds % 1) * 1000)
    
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"

def get_model_info(device: str, compute_type: str, gpu_available: bool, 
                  is_loaded: bool) -> Dict[str, Any]:
    """Krijg informatie over het geladen model"""
    return {
        "name": "WhisperX",
        "device": device,
        "compute_type": compute_type,
        "gpu_available": gpu_available,
        "is_loaded": is_loaded,
        "features": [
            "Word-level alignment",
            "Accurate timestamps", 
            "Better segmentation",
            "Language auto-detection"
        ]
    }

def cleanup_cuda_context():
    """Stop CUDA context om GPU geheugen vrij te maken"""
    try:
        print("🛑 WhisperX: Stop CUDA context...")
        
        # Probeer PyTorch CUDA context te stoppen
        try:
            import torch
            if torch.cuda.is_available():
                print("🛑 WhisperX: PyTorch CUDA beschikbaar, stop context...")
                
                # Stop alle CUDA streams
                if hasattr(torch.cuda, 'empty_cache'):
                    torch.cuda.empty_cache()
                    print("✅ CUDA cache geleegd")
                
                # Reset CUDA device
                if hasattr(torch.cuda, 'reset_peak_memory_stats'):
                    torch.cuda.reset_peak_memory_stats()
                    print("✅ CUDA memory stats gereset")
                
                # Synchroniseer CUDA
                if hasattr(torch.cuda, 'synchronize'):
                    torch.cuda.synchronize()
                    print("✅ CUDA gesynchroniseerd")
                    
        except ImportError:
            print("🛑 WhisperX: PyTorch niet beschikbaar")
        except Exception as e:
            print(f"⚠️ WhisperX: Fout bij PyTorch CUDA stop: {e}")
            
    except Exception as e:
        print(f"⚠️ WhisperX: Fout bij stoppen CUDA context: {e}")

def setup_tf32():
    """Schakel TF32 in voor betere prestaties en om waarschuwingen te voorkomen"""
    try:
        import torch
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
        print("✅ TF32 ingeschakeld voor betere CUDA prestaties")
        return True
    except Exception as e:
        print(f"⚠️ Kon TF32 niet inschakelen: {e}")
        return False
