#!/usr/bin/env python3
"""
Eenvoudige test om te zien wat er gebeurt met transcript_result
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_simple_transcript():
    print("🔍 [DEBUG] Eenvoudige transcript test")
    print("=" * 50)
    
    # Simuleer wat er gebeurt in ProcessingThread
    transcript_result = None  # Simuleer een probleem
    
    print(f"🔍 [DEBUG] transcript_result: {transcript_result}")
    print(f"🔍 [DEBUG] transcript_result type: {type(transcript_result)}")
    
    # Test de exacte logica uit ProcessingThread
    if not transcript_result:
        print(f"🔍 [DEBUG] transcript_result is None")
        print("❌ Fast Whisper transcriptie gefaald: Geen resultaat")
        return
    
    if not isinstance(transcript_result, dict):
        print(f"🔍 [DEBUG] transcript_result is geen dict: {type(transcript_result)}")
        print("❌ Fast Whisper transcriptie gefaald: Ongeldig resultaat")
        return
    
    print("🔍 [DEBUG] transcript_result is geldig, ga door...")
    
    # Test de rest van de logica
    if transcript_result and "error" not in transcript_result:
        print("🔍 [DEBUG] Transcript result is geldig, ga door naar volgende stap")
        transcript = transcript_result.get("transcript", "")
        transcriptions = transcript_result.get("transcriptions", [])
        
        print(f"🔍 [DEBUG] transcript length: {len(transcript)}")
        print(f"🔍 [DEBUG] transcriptions count: {len(transcriptions)}")
        
        # Test vertaling sectie
        print("🔍 [DEBUG] Test vertaling sectie...")
        enable_translation = False  # Simuleer settings
        print(f"🔍 [DEBUG] Enable translation: {enable_translation}")
        
        if enable_translation:
            print("🔍 [DEBUG] Vertaling ingeschakeld")
        else:
            print("🔍 [DEBUG] Geen vertaling")
            translated_transcriptions = transcriptions
        
        # Test video verwerking sectie
        print("🔍 [DEBUG] Test video verwerking sectie...")
        subtitle_type = "softcoded"  # Simuleer settings
        print(f"🔍 [DEBUG] subtitle_type: {subtitle_type}")
        
        # Video verwerking
        if subtitle_type == "softcoded":
            print("🔍 [DEBUG] Softcoded subtitles, genereer SRT bestanden...")
            # Simuleer video_processor.generate_srt_files call
            print("🔍 [DEBUG] SRT generatie succesvol!")
        else:
            print("🔍 [DEBUG] Hardcoded subtitles, skip SRT generatie")
        
        print("🔍 [DEBUG] Video verwerking voltooid!")
    else:
        print("🔍 [DEBUG] Transcript result is ongeldig of bevat error")
        if transcript_result and "error" in transcript_result:
            error_message = f"Fast Whisper transcriptie gefaald: {transcript_result['error']}"
            print(f"🔍 [DEBUG] {error_message}")

if __name__ == "__main__":
    test_simple_transcript() 