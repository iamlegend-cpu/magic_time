"""
Diagnostics voor Magic Time Studio
Alleen WhisperX wordt ondersteund
"""

import os
import sys
import platform
import subprocess
from typing import Dict, Any, Optional

def get_system_info() -> Dict[str, Any]:
    """Krijg systeem informatie"""
    return {
        "platform": platform.platform(),
        "python_version": sys.version,
        "python_executable": sys.executable,
        "architecture": platform.architecture(),
        "processor": platform.processor(),
        "machine": platform.machine()
    }

def get_python_packages() -> Dict[str, str]:
    """Krijg geïnstalleerde Python packages"""
    try:
        import pkg_resources
        installed_packages = {}
        for dist in pkg_resources.working_set:
            installed_packages[dist.project_name] = dist.version
        return installed_packages
    except ImportError:
        return {"error": "pkg_resources niet beschikbaar"}

def check_whisperx_installation() -> Dict[str, Any]:
    """Controleer WhisperX installatie"""
    result = {
        "whisperx_available": False,
        "version": None,
        "gpu_support": False,
        "models_available": []
    }
    
    try:
        import whisperx
        result["whisperx_available"] = True
        
        # Probeer versie te bepalen
        try:
            result["version"] = whisperx.__version__
        except AttributeError:
            result["version"] = "onbekend"
        
        # Controleer GPU ondersteuning
        try:
            import torch
            if torch.cuda.is_available():
                result["gpu_support"] = True
                result["gpu_count"] = torch.cuda.device_count()
                result["gpu_name"] = torch.cuda.get_device_name(0) if result["gpu_count"] > 0 else "geen"
        except ImportError:
            result["gpu_support"] = False
            result["gpu_error"] = "PyTorch niet beschikbaar"
        
        # Controleer beschikbare modellen
        try:
            # Test of we een klein model kunnen laden
            model = whisperx.load_model("tiny", device="cpu")
            result["models_available"].append("tiny")
            del model  # Ruim geheugen op
        except Exception as e:
            result["model_error"] = str(e)
            
    except ImportError as e:
        result["error"] = f"WhisperX niet geïnstalleerd: {e}"
    except Exception as e:
        result["error"] = f"Fout bij controleren WhisperX: {e}"
    
    return result

def check_ffmpeg() -> Dict[str, Any]:
    """Controleer FFmpeg installatie"""
    result = {
        "ffmpeg_available": False,
        "ffprobe_available": False,
        "version": None
    }
    
    try:
        # Controleer FFmpeg
        result_ffmpeg = subprocess.run(
            ["ffmpeg", "-version"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        if result_ffmpeg.returncode == 0:
            result["ffmpeg_available"] = True
            # Haal versie uit output
            version_line = result_ffmpeg.stdout.split('\n')[0]
            if "ffmpeg version" in version_line:
                result["version"] = version_line.split("ffmpeg version ")[1].split(" ")[0]
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
        pass
    
    try:
        # Controleer FFprobe
        result_ffprobe = subprocess.run(
            ["ffprobe", "-version"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        if result_ffprobe.returncode == 0:
            result["ffprobe_available"] = True
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
        pass
    
    return result

def run_full_diagnostics() -> Dict[str, Any]:
    """Voer volledige diagnostiek uit"""
    return {
        "system_info": get_system_info(),
        "python_packages": get_python_packages(),
        "whisperx": check_whisperx_installation(),
        "ffmpeg": check_ffmpeg()
    }

def print_diagnostics():
    """Print diagnostiek informatie naar console"""
    print("🔍 Magic Time Studio Diagnostics")
    print("=" * 50)
    
    # Systeem info
    system_info = get_system_info()
    print(f"🖥️ Platform: {system_info['platform']}")
    print(f"🐍 Python: {system_info['python_version']}")
    print(f"💻 Processor: {system_info['processor']}")
    
    # WhisperX info
    whisperx_info = check_whisperx_installation()
    print(f"\n🎤 WhisperX: {'✅ Beschikbaar' if whisperx_info['whisperx_available'] else '❌ Niet beschikbaar'}")
    if whisperx_info['whisperx_available']:
        print(f"   Versie: {whisperx_info['version']}")
        print(f"   GPU: {'✅ Ondersteund' if whisperx_info['gpu_support'] else '❌ Niet ondersteund'}")
        if whisperx_info['gpu_support']:
            print(f"   GPU Aantal: {whisperx_info['gpu_count']}")
            print(f"   GPU Naam: {whisperx_info['gpu_name']}")
    
    # FFmpeg info
    ffmpeg_info = check_ffmpeg()
    print(f"\n🎬 FFmpeg: {'✅ Beschikbaar' if ffmpeg_info['ffmpeg_available'] else '❌ Niet beschikbaar'}")
    print(f"   FFprobe: {'✅ Beschikbaar' if ffmpeg_info['ffprobe_available'] else '❌ Niet beschikbaar'}")
    if ffmpeg_info['version']:
        print(f"   Versie: {ffmpeg_info['version']}")

if __name__ == "__main__":
    print_diagnostics() 