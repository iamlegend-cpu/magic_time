"""
WhisperX SRT Functies voor Magic Time Studio
Genereert zeer accurate SRT bestanden met word-level alignment
"""

import os
from typing import List, Dict, Any, Optional
from datetime import timedelta

def create_whisperx_srt_content(transcriptions: List[Dict[str, Any]], 
                               word_alignments: List[Dict[str, Any]] = None,
                               output_path: Optional[str] = None) -> str:
    """
    Maak SRT content met WhisperX word-level alignment voor maximale accuracy
    
    Args:
        transcriptions: Lijst van transcriptie segmenten
        word_alignments: Word-level timing informatie (optioneel)
        output_path: Pad naar output bestand (optioneel)
    
    Returns:
        SRT content string
    """
    srt_content = ""
    
    for i, segment in enumerate(transcriptions, 1):
        # Converteer seconden naar SRT timestamp formaat
        start_time = _seconds_to_srt_timestamp(segment["start"])
        end_time = _seconds_to_srt_timestamp(segment["end"])
        
        # Gebruik word-level timing als beschikbaar voor betere accuracy
        if word_alignments and segment.get("words"):
            words = segment["words"]
            if words:
                # Gebruik eerste woord start en laatste woord end voor betere segmentatie
                segment_start = words[0]["start"]
                segment_end = words[-1]["end"]
                start_time = _seconds_to_srt_timestamp(segment_start)
                end_time = _seconds_to_srt_timestamp(segment_end)
        
        # Voeg segment toe aan SRT
        srt_content += f"{i}\n{start_time} --> {end_time}\n{segment['text']}\n\n"
    
    # Schrijf naar bestand als output_path is opgegeven
    if output_path:
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(srt_content)
            print(f"✅ WhisperX SRT bestand opgeslagen: {output_path}")
        except Exception as e:
            print(f"❌ Fout bij opslaan WhisperX SRT bestand: {e}")
    
    return srt_content

def create_enhanced_srt_with_word_timing(transcriptions: List[Dict[str, Any]], 
                                        word_alignments: List[Dict[str, Any]] = None,
                                        output_path: Optional[str] = None) -> str:
    """
    Maak verbeterde SRT met gedetailleerde word-level timing informatie
    
    Args:
        transcriptions: Lijst van transcriptie segmenten
        word_alignments: Word-level timing informatie
        output_path: Pad naar output bestand (optioneel)
    
    Returns:
        Verbeterde SRT content string
    """
    srt_content = ""
    
    for i, segment in enumerate(transcriptions, 1):
        # Basis segment timing
        start_time = _seconds_to_srt_timestamp(segment["start"])
        end_time = _seconds_to_srt_timestamp(segment["end"])
        
        # Voeg word-level timing toe als commentaar (optioneel)
        word_timing_info = ""
        if word_alignments and segment.get("words"):
            words = segment["words"]
            if words:
                # Bereken gemiddelde timing per woord
                word_timings = []
                for word_info in words:
                    word_start = _seconds_to_srt_timestamp(word_info["start"])
                    word_end = _seconds_to_srt_timestamp(word_info["end"])
                    word_text = word_info["word"]
                    word_timings.append(f"{word_text}({word_start}-{word_end})")
                
                word_timing_info = f" [Words: {' '.join(word_timings)}]"
        
        # Voeg segment toe aan SRT
        srt_content += f"{i}\n{start_time} --> {end_time}\n{segment['text']}{word_timing_info}\n\n"
    
    # Schrijf naar bestand als output_path is opgegeven
    if output_path:
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(srt_content)
            print(f"✅ Verbeterde WhisperX SRT bestand opgeslagen: {output_path}")
        except Exception as e:
            print(f"❌ Fout bij opslaan verbeterde WhisperX SRT bestand: {e}")
    
    return srt_content

def _seconds_to_srt_timestamp(seconds: float) -> str:
    """
    Converteer seconden naar SRT timestamp formaat (HH:MM:SS,mmm)
    
    Args:
        seconds: Tijd in seconden
    
    Returns:
        SRT timestamp string
    """
    # Gebruik timedelta voor nauwkeurige conversie
    td = timedelta(seconds=seconds)
    
    # Bereken uren, minuten, seconden en milliseconden
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    millisecs = int((seconds % 1) * 1000)
    
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"

def validate_whisperx_transcriptions(transcriptions: List[Dict[str, Any]]) -> bool:
    """
    Valideer WhisperX transcripties voor correcte structuur
    
    Args:
        transcriptions: Lijst van transcriptie segmenten
    
    Returns:
        True als valid, False anders
    """
    if not transcriptions:
        print("❌ Geen transcripties gevonden")
        return False
    
    required_fields = ["start", "end", "text"]
    
    for i, segment in enumerate(transcriptions):
        # Controleer vereiste velden
        for field in required_fields:
            if field not in segment:
                print(f"❌ Segment {i+1} mist vereist veld: {field}")
                return False
        
        # Controleer timing validiteit
        if segment["start"] >= segment["end"]:
            print(f"❌ Segment {i+1} heeft ongeldige timing: start={segment['start']}, end={segment['end']}")
            return False
        
        # Controleer tekst validiteit
        if not segment["text"] or not segment["text"].strip():
            print(f"❌ Segment {i+1} heeft lege tekst")
            return False
    
    print(f"✅ {len(transcriptions)} transcriptie segmenten gevalideerd")
    return True

def get_whisperx_statistics(transcriptions: List[Dict[str, Any]], 
                           word_alignments: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Bereken statistieken voor WhisperX transcripties
    
    Args:
        transcriptions: Lijst van transcriptie segmenten
        word_alignments: Word-level timing informatie
    
    Returns:
        Dictionary met statistieken
    """
    if not transcriptions:
        return {}
    
    # Basis statistieken
    total_segments = len(transcriptions)
    total_duration = sum(seg["end"] - seg["start"] for seg in transcriptions)
    total_words = sum(len(seg["text"].split()) for seg in transcriptions)
    
    # Timing statistieken
    segment_durations = [seg["end"] - seg["start"] for seg in transcriptions]
    avg_segment_duration = sum(segment_durations) / len(segment_durations)
    min_segment_duration = min(segment_durations)
    max_segment_duration = max(segment_durations)
    
    # Word-level statistieken
    word_stats = {}
    if word_alignments:
        word_count = len(word_alignments)
        word_stats = {
            "total_words": word_count,
            "words_per_segment": word_count / total_segments if total_segments > 0 else 0
        }
    
    return {
        "total_segments": total_segments,
        "total_duration_seconds": total_duration,
        "total_duration_formatted": str(timedelta(seconds=int(total_duration))),
        "total_words": total_words,
        "words_per_segment": total_words / total_segments if total_segments > 0 else 0,
        "avg_segment_duration": avg_segment_duration,
        "min_segment_duration": min_segment_duration,
        "max_segment_duration": max_segment_duration,
        "word_level_alignment": word_alignments is not None,
        **word_stats
    }
