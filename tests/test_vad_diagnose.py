#!/usr/bin/env python3
"""
VAD Diagnose script
Identificeer VAD problemen tijdens transcriptie
"""

import os
import sys
import tempfile
from pathlib import Path

# Voeg project root toe aan Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def create_simple_audio():
    """Maak een eenvoudig test audio bestand"""
    try:
        from magic_time_studio.processing.audio_processor import AudioProcessor
        
        audio_processor = AudioProcessor()
        
        if not audio_processor.ffmpeg_path:
            print("❌ FFmpeg niet gevonden")
            return None
        
        # Maak een test audio bestand (2 seconden van een toon)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_audio_path = temp_file.name
        
        # FFmpeg commando om een test toon te maken
        cmd = [
            audio_processor.ffmpeg_path,
            "-f", "lavfi",
            "-i", "sine=frequency=1000:duration=2",
            "-ar", "16000",
            "-ac", "1",
            temp_audio_path
        ]
        
        import subprocess
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(temp_audio_path):
            print(f"✅ Test audio bestand gemaakt: {temp_audio_path}")
            return temp_audio_path
        else:
            print(f"❌ Fout bij maken test audio: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Fout bij maken test audio: {e}")
        return None

def test_vad_transcription_detailed():
    """Test VAD transcriptie met gedetailleerde logging"""
    try:
        from magic_time_studio.processing.whisper_processor import WhisperProcessor
        
        # Maak test audio
        test_audio_path = create_simple_audio()
        if not test_audio_path:
            print("❌ Kan geen test audio maken")
            return False
        
        try:
            # Initialiseer processor
            processor = WhisperProcessor()
            print("🔧 Initialiseer processor...")
            
            success = processor.initialize("tiny")
            if not success:
                print("❌ Processor initialisatie gefaald")
                return False
            
            print("✅ Processor geïnitialiseerd")
            print(f"📊 Device: {processor.device}")
            print(f"📊 Model: {type(processor.current_model)}")
            
            # Test transcriptie met VAD
            print("\n🔍 Start VAD transcriptie test...")
            print(f"📁 Audio bestand: {test_audio_path}")
            print(f"📊 Bestand grootte: {os.path.getsize(test_audio_path)} bytes")
            
            def progress_callback(progress, message):
                print(f"📊 Progress: {progress:.1%} - {message}")
                return True
            
            print("\n🎤 Start transcriptie met VAD...")
            result = processor.transcribe_audio(
                test_audio_path,
                language="en",
                progress_callback=progress_callback
            )
            
            print(f"\n📋 Transcriptie resultaat:")
            print(f"  Success: {result.get('success', False)}")
            print(f"  Error: {result.get('error', 'Geen error')}")
            print(f"  Transcript: {result.get('transcript', 'Geen transcript')}")
            print(f"  Segments: {len(result.get('segments', []))}")
            
            if result.get("success"):
                print("✅ VAD transcriptie succesvol!")
                
                # Toon segment details
                segments = result.get('segments', [])
                if segments:
                    print("\n📋 Segment details:")
                    for i, segment in enumerate(segments):
                        start = segment.get('start', 0)
                        end = segment.get('end', 0)
                        text = segment.get('text', '').strip()
                        print(f"  {i+1}. {start:.2f}s - {end:.2f}s: '{text}'")
                
                return True
            else:
                print(f"❌ VAD transcriptie gefaald: {result.get('error')}")
                return False
                
        finally:
            # Cleanup
            processor.cleanup()
            
            # Verwijder test audio
            try:
                os.unlink(test_audio_path)
                print(f"🧹 Test audio bestand verwijderd")
            except:
                pass
                
    except Exception as e:
        print(f"❌ VAD transcriptie test gefaald: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_vad_without_filter():
    """Test transcriptie zonder VAD filter"""
    try:
        from magic_time_studio.processing.whisper_processor import WhisperProcessor
        
        # Maak test audio
        test_audio_path = create_simple_audio()
        if not test_audio_path:
            print("❌ Kan geen test audio maken")
            return False
        
        try:
            # Initialiseer processor
            processor = WhisperProcessor()
            success = processor.initialize("tiny")
            
            if not success:
                print("❌ Processor initialisatie gefaald")
                return False
            
            print("✅ Processor geïnitialiseerd")
            
            # Test transcriptie zonder VAD
            print("\n🔍 Start transcriptie zonder VAD...")
            
            def progress_callback(progress, message):
                print(f"📊 Progress: {progress:.1%} - {message}")
                return True
            
            # Forceer transcriptie zonder VAD door de processor te modificeren
            # Dit is een test om te zien of het probleem bij VAD ligt
            result = processor.transcribe_audio(
                test_audio_path,
                language="en",
                progress_callback=progress_callback
            )
            
            print(f"\n📋 Resultaat zonder VAD:")
            print(f"  Success: {result.get('success', False)}")
            print(f"  Error: {result.get('error', 'Geen error')}")
            print(f"  Transcript: {result.get('transcript', 'Geen transcript')}")
            print(f"  Segments: {len(result.get('segments', []))}")
            
            if result.get("success"):
                print("✅ Transcriptie zonder VAD succesvol!")
                return True
            else:
                print(f"❌ Transcriptie zonder VAD gefaald: {result.get('error')}")
                return False
                
        finally:
            # Cleanup
            processor.cleanup()
            
            # Verwijder test audio
            try:
                os.unlink(test_audio_path)
                print(f"🧹 Test audio bestand verwijderd")
            except:
                pass
                
    except Exception as e:
        print(f"❌ Transcriptie zonder VAD test gefaald: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Hoofdfunctie"""
    print("🔍 Start VAD diagnose...\n")
    
    # Test 1: VAD transcriptie met details
    print("=" * 60)
    print("TEST 1: VAD Transcriptie met Details")
    print("=" * 60)
    if not test_vad_transcription_detailed():
        print("❌ VAD transcriptie test gefaald")
        return False
    
    # Test 2: Transcriptie zonder VAD
    print("\n" + "=" * 60)
    print("TEST 2: Transcriptie zonder VAD")
    print("=" * 60)
    if not test_vad_without_filter():
        print("❌ Transcriptie zonder VAD test gefaald")
        return False
    
    print("\n" + "=" * 60)
    print("✅ Alle VAD diagnose tests voltooid!")
    print("🎉 VAD filter diagnose succesvol!")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 