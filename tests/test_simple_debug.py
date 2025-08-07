#!/usr/bin/env python3
"""
Eenvoudige test om te debuggen wat er gebeurt in ProcessingThread
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_simple_debug():
    print("🔍 [DEBUG] Eenvoudige debug test")
    print("=" * 50)
    
    # Simuleer de logica uit ProcessingThread
    transcript_result = {
        "success": True,
        "transcript": "Test transcript",
        "transcriptions": [{"start": 0.0, "end": 10.0, "text": "Test transcript", "language": "en"}],
        "language": "en",
        "duration": 10.0,
        "segments": 1
    }
    
    print(f"🔍 [DEBUG] transcript_result type: {type(transcript_result)}")
    print(f"🔍 [DEBUG] transcript_result keys: {list(transcript_result.keys())}")
    
    # Test de exacte logica uit ProcessingThread
    if transcript_result and "error" not in transcript_result:
        print("✅ Transcript result is geldig")
        
        transcript = transcript_result.get("transcript", "")
        transcriptions = transcript_result.get("transcriptions", [])
        
        print(f"🔍 [DEBUG] transcript length: {len(transcript)}")
        print(f"🔍 [DEBUG] transcriptions count: {len(transcriptions)}")
        
        # Test vertaling sectie
        print(f"🔍 [DEBUG] Test vertaling sectie...")
        enable_translation = False  # Simuleer settings
        print(f"🔍 [DEBUG] Enable translation: {enable_translation}")
        
        if enable_translation:
            print(f"🔍 [DEBUG] Vertaling ingeschakeld")
            # Vertaal transcripties
            translated_transcriptions = []
            for segment in transcriptions:
                try:
                    # Simuleer vertaling
                    translated_text = segment["text"] + " (vertaald)"
                    translated_segment = segment.copy()
                    translated_segment["text"] = translated_text
                    translated_transcriptions.append(translated_segment)
                except Exception as e:
                    print(f"🔍 [DEBUG] Vertaling fout voor segment: {e}")
                    translated_transcriptions.append(segment)
            
            print(f"🔍 [DEBUG] Vertaling voltooid, {len(translated_transcriptions)} segmenten")
        else:
            print(f"🔍 [DEBUG] Geen vertaling")
            translated_transcriptions = transcriptions
        
        # Test video verwerking sectie
        print(f"🔍 [DEBUG] Test video verwerking sectie...")
        subtitle_type = "softcoded"  # Simuleer settings
        print(f"🔍 [DEBUG] subtitle_type: {subtitle_type}")
        
        # Video verwerking
        if subtitle_type == "softcoded":
            print(f"🔍 [DEBUG] Softcoded subtitles, genereer SRT bestanden...")
            # Simuleer video_processor.generate_srt_files
            video_result = {"success": True, "output_files": {"srt": "test.srt"}}
            print(f"🔍 [DEBUG] Video result: {video_result}")
            
            if "error" in video_result:
                print(f"🔍 [DEBUG] SRT generatie gefaald: {video_result['error']}")
                error_message = f"SRT generatie gefaald: {video_result['error']}"
                print(f"❌ {error_message}")
            else:
                print(f"🔍 [DEBUG] SRT generatie succesvol!")
        else:
            print(f"🔍 [DEBUG] Hardcoded subtitles, skip SRT generatie")
        
        print(f"🔍 [DEBUG] Video verwerking voltooid!")
    else:
        print("❌ Transcript result is ongeldig of bevat error")
        if transcript_result and "error" in transcript_result:
            error_message = f"Fast Whisper transcriptie gefaald: {transcript_result['error']}"
            print(f"🔍 [DEBUG] {error_message}")
            print(f"❌ {error_message}")
    
    print("🎉 Test voltooid!")

if __name__ == "__main__":
    test_simple_debug() 