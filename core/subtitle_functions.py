"""
Ondertitel functies voor Magic Time Studio
Bevat alle ondertitel functionaliteit
"""

import os
import re
from typing import Optional, Dict, List, Any, Tuple
import logging

logger = logging.getLogger(__name__)

def create_srt_content(transcriptions: List[Dict[str, Any]], 
                      output_path: str,
                      use_whisperx: bool = False,
                      word_alignments: Optional[List[Dict[str, Any]]] = None) -> bool:
    """
    Maak SRT ondertitel bestand van transcripties
    
    Args:
        transcriptions: Lijst van transcriptie segmenten
        output_path: Pad naar het output SRT bestand
        use_whisperx: Gebruik WhisperX SRT functies voor betere accuracy
        word_alignments: Word-level timing informatie voor WhisperX
    
    Returns:
        True bij succes, False bij fout
    """
    try:
        if not transcriptions:
            logger.error("Geen transcripties om te verwerken")
            return False
        
        # Maak output directory als deze niet bestaat
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Gebruik WhisperX SRT functies als beschikbaar en gewenst
        if use_whisperx:
            try:
                from core.whisperx_srt_functions import create_whisperx_srt_content
                srt_content = create_whisperx_srt_content(
                    transcriptions, 
                    word_alignments, 
                    output_path
                )
                if srt_content:
                    logger.info(f"WhisperX SRT bestand aangemaakt: {output_path}")
                    return True
                else:
                    logger.warning("WhisperX SRT functies gefaald, gebruik standaard SRT generatie")
            except ImportError:
                logger.warning("WhisperX SRT functies niet beschikbaar, gebruik standaard SRT generatie")
            except Exception as e:
                logger.warning(f"WhisperX SRT functies gefaald: {e}, gebruik standaard SRT generatie")
        
        # Standaard SRT generatie als fallback
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(transcriptions, 1):
                start_time = format_timestamp(segment.get("start", 0))
                end_time = format_timestamp(segment.get("end", 0))
                text = segment.get("text", "").strip()
                
                if not text:  # Skip lege segmenten
                    continue
                
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")
        
        logger.info(f"Standaard SRT bestand aangemaakt: {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"Fout bij aanmaken SRT bestand: {e}")
        return False

def create_vtt_content(transcriptions: List[Dict[str, Any]], 
                      output_path: str) -> bool:
    """
    Maak WebVTT ondertitel bestand van transcripties
    
    Args:
        transcriptions: Lijst van transcriptie segmenten
        output_path: Pad naar het output VTT bestand
    
    Returns:
        True bij succes, False bij fout
    """
    try:
        if not transcriptions:
            logger.error("Geen transcripties om te verwerken")
            return False
        
        # Maak output directory als deze niet bestaat
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("WEBVTT\n\n")
            
            for i, segment in enumerate(transcriptions, 1):
                start_time = format_vtt_timestamp(segment.get("start", 0))
                end_time = format_vtt_timestamp(segment.get("end", 0))
                text = segment.get("text", "").strip()
                
                if not text:  # Skip lege segmenten
                    continue
                
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")
        
        logger.info(f"VTT bestand aangemaakt: {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"Fout bij aanmaken VTT bestand: {e}")
        return False

def create_whisperx_srt_content(transcriptions: List[Dict[str, Any]], 
                               output_path: str,
                               word_alignments: Optional[List[Dict[str, Any]]] = None,
                               enhanced: bool = False) -> bool:
    """
    Maak WhisperX SRT ondertitel bestand met word-level alignment voor maximale accuracy
    
    Args:
        transcriptions: Lijst van transcriptie segmenten
        output_path: Pad naar het output SRT bestand
        word_alignments: Word-level timing informatie
        enhanced: Gebruik verbeterde SRT met word timing info
    
    Returns:
        True bij succes, False bij fout
    """
    try:
        if not transcriptions:
            logger.error("Geen transcripties om te verwerken")
            return False
        
        # Maak output directory als deze niet bestaat
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Implementeer WhisperX SRT generatie direct om circulaire import te voorkomen
        srt_content = ""
        
        for i, segment in enumerate(transcriptions, 1):
            # Converteer seconden naar SRT timestamp formaat
            start_time = format_timestamp(segment.get("start", 0))
            end_time = format_timestamp(segment.get("end", 0))
            
            # Gebruik word-level timing als beschikbaar voor betere accuracy
            if word_alignments and segment.get("words"):
                words = segment["words"]
                if words:
                    # Gebruik eerste woord start en laatste woord end voor betere segmentatie
                    segment_start = words[0].get("start", segment.get("start", 0))
                    segment_end = words[-1].get("end", segment.get("end", 0))
                    start_time = format_timestamp(segment_start)
                    end_time = format_timestamp(segment_end)
            
            text = segment.get("text", "").strip()
            if not text:  # Skip lege segmenten
                continue
            
            # Voeg segment toe aan SRT
            srt_content += f"{i}\n{start_time} --> {end_time}\n{text}\n\n"
        
        # Schrijf naar bestand
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(srt_content)
        
        logger.info(f"WhisperX SRT bestand aangemaakt: {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"Fout bij aanmaken WhisperX SRT bestand: {e}")
        return False

def create_ass_content(transcriptions: List[Dict[str, Any]], 
                      output_path: str, style_config: Optional[Dict[str, Any]] = None) -> bool:
    """
    Maak ASS/SSA ondertitel bestand van transcripties
    
    Args:
        transcriptions: Lijst van transcriptie segmenten
        output_path: Pad naar het output ASS bestand
        style_config: Stijl configuratie (optioneel)
    
    Returns:
        True bij succes, False bij fout
    """
    try:
        if not transcriptions:
            logger.error("Geen transcripties om te verwerken")
            return False
        
        # Maak output directory als deze niet bestaat
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Standaard stijl configuratie
        default_style = {
            "name": "Default",
            "fontname": "Arial",
            "fontsize": "20",
            "primary_colour": "&H00FFFFFF",
            "secondary_colour": "&H000000FF",
            "outline_colour": "&H00000000",
            "back_colour": "&H80000000",
            "bold": "0",
            "italic": "0",
            "underline": "0",
            "strikeout": "0",
            "scale_x": "100",
            "scale_y": "100",
            "spacing": "0",
            "angle": "0",
            "border_style": "1",
            "outline": "2",
            "shadow": "2",
            "alignment": "2",
            "margin_l": "10",
            "margin_r": "10",
            "margin_v": "10"
        }
        
        if style_config:
            default_style.update(style_config)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            # ASS header
            f.write("[Script Info]\n")
            f.write("Title: Magic Time Studio Generated Subtitles\n")
            f.write("ScriptType: v4.00+\n")
            f.write("WrapStyle: 0\n")
            f.write("ScaledBorderAndShadow: yes\n")
            f.write("YCbCr Matrix: TV.601\n\n")
            
            # Stijlen sectie
            f.write("[V4+ Styles]\n")
            f.write("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")
            
            style_line = f"Style: {default_style['name']}, {default_style['fontname']}, {default_style['fontsize']}, {default_style['primary_colour']}, {default_style['secondary_colour']}, {default_style['outline_colour']}, {default_style['back_colour']}, {default_style['bold']}, {default_style['italic']}, {default_style['underline']}, {default_style['strikeout']}, {default_style['scale_x']}, {default_style['scale_y']}, {default_style['spacing']}, {default_style['angle']}, {default_style['border_style']}, {default_style['outline']}, {default_style['shadow']}, {default_style['alignment']}, {default_style['margin_l']}, {default_style['margin_r']}, {default_style['margin_v']}, 1\n"
            f.write(style_line)
            f.write("\n")
            
            # Events sectie
            f.write("[Events]\n")
            f.write("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
            
            for segment in transcriptions:
                start_time = format_ass_timestamp(segment.get("start", 0))
                end_time = format_ass_timestamp(segment.get("end", 0))
                text = segment.get("text", "").strip()
                
                if not text:  # Skip lege segmenten
                    continue
                
                # Escape speciale karakters voor ASS
                text = escape_ass_text(text)
                
                event_line = f"Dialogue: 0, {start_time}, {end_time}, {default_style['name']}, , 0, 0, 0, , {text}\n"
                f.write(event_line)
        
        logger.info(f"ASS bestand aangemaakt: {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"Fout bij aanmaken ASS bestand: {e}")
        return False

def format_timestamp(seconds: float) -> str:
    """
    Converteer seconden naar SRT timestamp formaat
    
    Args:
        seconds: Tijd in seconden
    
    Returns:
        Geformatteerde timestamp string (HH:MM:SS,mmm)
    """
    try:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        milliseconds = int((secs % 1) * 1000)
        secs = int(secs)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"
    except Exception as e:
        logger.error(f"Fout bij formatteren timestamp: {e}")
        return "00:00:00,000"

def format_vtt_timestamp(seconds: float) -> str:
    """
    Converteer seconden naar WebVTT timestamp formaat
    
    Args:
        seconds: Tijd in seconden
    
    Returns:
        Geformatteerde timestamp string (HH:MM:SS.mmm)
    """
    try:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        milliseconds = int((secs % 1) * 1000)
        secs = int(secs)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{milliseconds:03d}"
    except Exception as e:
        logger.error(f"Fout bij formatteren VTT timestamp: {e}")
        return "00:00:00.000"

def format_ass_timestamp(seconds: float) -> str:
    """
    Converteer seconden naar ASS timestamp formaat
    
    Args:
        seconds: Tijd in seconden
    
    Returns:
        Geformatteerde timestamp string (H:MM:SS.cc)
    """
    try:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        centiseconds = int((secs % 1) * 100)
        secs = int(secs)
        
        return f"{hours}:{minutes:02d}:{secs:02d}.{centiseconds:02d}"
    except Exception as e:
        logger.error(f"Fout bij formatteren ASS timestamp: {e}")
        return "0:00:00.00"

def escape_ass_text(text: str) -> str:
    """
    Escape speciale karakters voor ASS formaat
    
    Args:
        text: Tekst om te escapen
    
    Returns:
        Geëscapte tekst
    """
    # ASS speciale karakters
    replacements = {
        "\\": "\\\\",
        "{": "\\{",
        "}": "\\}",
        "\n": "\\N",
        "\r": "\\N"
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text

def merge_subtitle_files(subtitle_files: List[str], output_path: str, 
                        format_type: str = "srt") -> bool:
    """
    Voeg meerdere ondertitel bestanden samen
    
    Args:
        subtitle_files: Lijst van paden naar ondertitel bestanden
        output_path: Pad naar het output bestand
        format_type: Type ondertitel formaat (srt, vtt, ass)
    
    Returns:
        True bij succes, False bij fout
    """
    try:
        if not subtitle_files:
            logger.error("Geen ondertitel bestanden om samen te voegen")
            return False
        
        all_transcriptions = []
        current_time_offset = 0.0
        
        for subtitle_file in subtitle_files:
            if not os.path.exists(subtitle_file):
                logger.warning(f"Ondertitel bestand bestaat niet: {subtitle_file}")
                continue
            
            # Lees ondertitel bestand
            transcriptions = read_subtitle_file(subtitle_file, format_type)
            if not transcriptions:
                continue
            
            # Pas tijd offset toe
            for segment in transcriptions:
                segment["start"] += current_time_offset
                segment["end"] += current_time_offset
            
            all_transcriptions.extend(transcriptions)
            
            # Bereken volgende tijd offset
            if transcriptions:
                max_end_time = max(segment["end"] for segment in transcriptions)
                current_time_offset = max_end_time
        
        # Sla samengevoegde ondertitels op
        if format_type == "srt":
            return create_srt_content(all_transcriptions, output_path)
        elif format_type == "vtt":
            return create_vtt_content(all_transcriptions, output_path)
        elif format_type == "ass":
            return create_ass_content(all_transcriptions, output_path)
        else:
            logger.error(f"Onbekend ondertitel formaat: {format_type}")
            return False
        
    except Exception as e:
        logger.error(f"Fout bij samenvoegen ondertitel bestanden: {e}")
        return False

def read_subtitle_file(file_path: str, format_type: str) -> Optional[List[Dict[str, Any]]]:
    """
    Lees een ondertitel bestand
    
    Args:
        file_path: Pad naar het ondertitel bestand
        format_type: Type ondertitel formaat
    
    Returns:
        Lijst van transcriptie segmenten of None bij fout
    """
    try:
        if format_type == "srt":
            return read_srt_file(file_path)
        elif format_type == "vtt":
            return read_vtt_file(file_path)
        elif format_type == "ass":
            return read_ass_file(file_path)
        else:
            logger.error(f"Onbekend ondertitel formaat: {format_type}")
            return None
            
    except Exception as e:
        logger.error(f"Fout bij lezen ondertitel bestand: {e}")
        return None

def read_srt_file(file_path: str) -> Optional[List[Dict[str, Any]]]:
    """
    Lees een SRT ondertitel bestand
    
    Args:
        file_path: Pad naar het SRT bestand
    
    Returns:
        Lijst van transcriptie segmenten of None bij fout
    """
    try:
        transcriptions = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split op dubbele newlines om segmenten te scheiden
        segments = content.strip().split('\n\n')
        
        for segment in segments:
            lines = segment.strip().split('\n')
            if len(lines) < 3:
                continue
            
            try:
                # Parse timestamp regel
                timestamp_line = lines[1]
                start_time, end_time = parse_srt_timestamp(timestamp_line)
                
                # Haal tekst op
                text = '\n'.join(lines[2:]).strip()
                
                if start_time is not None and end_time is not None and text:
                    transcriptions.append({
                        "start": start_time,
                        "end": end_time,
                        "text": text
                    })
                    
            except Exception as e:
                logger.warning(f"Fout bij parsen SRT segment: {e}")
                continue
        
        return transcriptions
        
    except Exception as e:
        logger.error(f"Fout bij lezen SRT bestand: {e}")
        return None

def parse_srt_timestamp(timestamp_line: str) -> Tuple[Optional[float], Optional[float]]:
    """
    Parse een SRT timestamp regel
    
    Args:
        timestamp_line: Timestamp regel (HH:MM:SS,mmm --> HH:MM:SS,mmm)
    
    Returns:
        Tuple met (start_time, end_time) in seconden
    """
    try:
        # Split op arrow
        parts = timestamp_line.split(' --> ')
        if len(parts) != 2:
            return None, None
        
        start_str, end_str = parts
        
        # Parse timestamps
        start_time = parse_timestamp_to_seconds(start_str)
        end_time = parse_timestamp_to_seconds(end_str)
        
        return start_time, end_time
        
    except Exception as e:
        logger.error(f"Fout bij parsen SRT timestamp: {e}")
        return None, None

def parse_timestamp_to_seconds(timestamp: str) -> Optional[float]:
    """
    Converteer timestamp string naar seconden
    
    Args:
        timestamp: Timestamp string (HH:MM:SS,mmm of HH:MM:SS.mmm)
    
    Returns:
        Tijd in seconden of None bij fout
    """
    try:
        # Vervang komma door punt voor consistentie
        timestamp = timestamp.replace(',', '.')
        
        # Split op kolon en punt
        parts = timestamp.split(':')
        if len(parts) != 3:
            return None
        
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds_parts = parts[2].split('.')
        seconds = int(seconds_parts[0])
        milliseconds = int(seconds_parts[1]) if len(seconds_parts) > 1 else 0
        
        total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000
        return total_seconds
        
    except Exception as e:
        logger.error(f"Fout bij parsen timestamp: {e}")
        return None

def read_vtt_file(file_path: str) -> Optional[List[Dict[str, Any]]]:
    """
    Lees een WebVTT ondertitel bestand
    
    Args:
        file_path: Pad naar het VTT bestand
    
    Returns:
        Lijst van transcriptie segmenten of None bij fout
    """
    try:
        transcriptions = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Skip header regels
        i = 0
        while i < len(lines) and not lines[i].strip().startswith('-->'):
            i += 1
        
        # Parse segmenten
        while i < len(lines):
            line = lines[i].strip()
            
            if '-->' in line:
                try:
                    # Parse timestamp regel
                    start_time, end_time = parse_vtt_timestamp(line)
                    
                    # Haal tekst op
                    text_lines = []
                    i += 1
                    while i < len(lines) and lines[i].strip() and not '-->' in lines[i]:
                        text_lines.append(lines[i].strip())
                        i += 1
                    
                    text = ' '.join(text_lines).strip()
                    
                    if start_time is not None and end_time is not None and text:
                        transcriptions.append({
                            "start": start_time,
                            "end": end_time,
                            "text": text
                        })
                        
                except Exception as e:
                    logger.warning(f"Fout bij parsen VTT segment: {e}")
                    i += 1
            else:
                i += 1
        
        return transcriptions
        
    except Exception as e:
        logger.error(f"Fout bij lezen VTT bestand: {e}")
        return None

def parse_vtt_timestamp(timestamp_line: str) -> Tuple[Optional[float], Optional[float]]:
    """
    Parse een VTT timestamp regel
    
    Args:
        timestamp_line: Timestamp regel (HH:MM:SS.mmm --> HH:MM:SS.mmm)
    
    Returns:
        Tuple met (start_time, end_time) in seconden
    """
    try:
        # Split op arrow
        parts = timestamp_line.split(' --> ')
        if len(parts) != 2:
            return None, None
        
        start_str, end_str = parts
        
        # Parse timestamps
        start_time = parse_timestamp_to_seconds(start_str)
        end_time = parse_timestamp_to_seconds(end_str)
        
        return start_time, end_time
        
    except Exception as e:
        logger.error(f"Fout bij parsen VTT timestamp: {e}")
        return None, None

def read_ass_file(file_path: str) -> Optional[List[Dict[str, Any]]]:
    """
    Lees een ASS/SSA ondertitel bestand
    
    Args:
        file_path: Pad naar het ASS bestand
    
    Returns:
        Lijst van transcriptie segmenten of None bij fout
    """
    try:
        transcriptions = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Zoek naar Events sectie
        events_start = -1
        for i, line in enumerate(lines):
            if line.strip() == '[Events]':
                events_start = i
                break
        
        if events_start == -1:
            logger.error("Events sectie niet gevonden in ASS bestand")
            return None
        
        # Skip format regel
        i = events_start + 2
        
        # Parse events
        while i < len(lines):
            line = lines[i].strip()
            
            if line.startswith('[') or not line:
                break
            
            if line.startswith('Dialogue:'):
                try:
                    # Parse dialogue regel
                    parts = line.split(',', 9)  # Split op eerste 9 komma's
                    if len(parts) >= 10:
                        start_time_str = parts[1].strip()
                        end_time_str = parts[2].strip()
                        text = parts[9].strip()
                        
                        # Parse timestamps
                        start_time = parse_ass_timestamp(start_time_str)
                        end_time = parse_ass_timestamp(end_time_str)
                        
                        if start_time is not None and end_time is not None and text:
                            transcriptions.append({
                                "start": start_time,
                                "end": end_time,
                                "text": text
                            })
                            
                except Exception as e:
                    logger.warning(f"Fout bij parsen ASS event: {e}")
            
            i += 1
        
        return transcriptions
        
    except Exception as e:
        logger.error(f"Fout bij lezen ASS bestand: {e}")
        return None

def is_whisperx_srt_available() -> bool:
    """
    Controleer of WhisperX SRT functies beschikbaar zijn
    
    Returns:
        True als WhisperX SRT functies beschikbaar zijn
    """
    try:
        # Controleer of whisperx_srt_functions module beschikbaar is
        from core.whisperx_srt_functions import create_whisperx_srt_content
        return True
    except ImportError:
        return False

def parse_ass_timestamp(timestamp: str) -> Optional[float]:
    """
    Converteer ASS timestamp string naar seconden
    
    Args:
        timestamp: Timestamp string (H:MM:SS.cc)
    
    Returns:
        Tijd in seconden of None bij fout
    """
    try:
        # Split op kolon en punt
        parts = timestamp.split(':')
        if len(parts) != 3:
            return None
        
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds_parts = parts[2].split('.')
        seconds = int(seconds_parts[0])
        centiseconds = int(seconds_parts[1]) if len(seconds_parts) > 1 else 0
        
        total_seconds = hours * 3600 + minutes * 60 + seconds + centiseconds / 100
        return total_seconds
        
    except Exception as e:
        logger.error(f"Fout bij parsen ASS timestamp: {e}")
        return None
