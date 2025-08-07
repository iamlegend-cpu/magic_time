#!/usr/bin/env python3
"""
Script om debug output op te schonen in processing_thread.py
"""

import re

def cleanup_debug_output():
    """Verwijder overbodige debug prints uit processing_thread.py"""
    
    file_path = "magic_time_studio/app_core/processing_thread.py"
    
    # Lees het bestand
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Debug prints die we willen behouden (alleen belangrijke)
    important_debug_patterns = [
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Audio extractie gefaald voor.*?"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Fast Whisper transcriptie gefaald voor.*?"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Vertaling gefaald voor.*?"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Video verwerking gefaald voor.*?"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Fout bij verwerken.*?"\)',
    ]
    
    # Debug prints die we willen verwijderen (overbodige)
    remove_patterns = [
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: DEBUG_MODE is actief!"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: DEBUG_MODE = \{DEBUG_MODE\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: \{len\(self\.files\)\} bestanden ontvangen"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Bestand \{i\+1\}: \{file_path\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: \{total_files\} video bestanden gevonden"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Video bestand \{i\+1\}: \{file_path\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Start verwerking van bestand \{i\+1\}/\{total_files\}: \{file_path\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Verwerking gestopt door gebruiker"\)',
        r'print\(f"🔍 \[DEBUG\] Reset progress bar voor nieuw bestand: \{os\.path\.basename\(file_path\)\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Progress voor bestand \{i\+1\}: \{file_progress:\.1f\}%"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Start audio extractie voor \{file_path\}"\)',
        r'print\(f"🔍 \[DEBUG\] Audio extractie gestart: \{os\.path\.basename\(file_path\)\}"\)',
        r'print\(f"🔍 \[DEBUG\] Audio progress: \{ffmpeg_progress:\.1f\}% - \{progress_text\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Audio extractie voltooid voor \{file_path\}"\)',
        r'print\(f"🔍 \[DEBUG\] Fast Whisper transcriptie gestart: \{os\.path\.basename\(file_path\)\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Fast Whisper initialisatie gefaald"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Verwerking gestopt voor Fast Whisper"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Fast Whisper stop callback - verwerking gestopt voor \{file_path\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Fast Whisper transcriptie voltooid!"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: transcript_result type: \{type\(transcript_result\)\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: transcript_result keys: \{list\(transcript_result\.keys\(\)\) if isinstance\(transcript_result, dict\) else \'N/A\'\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Gaat door naar volgende stap\.\.\."\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: transcript_result is None"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: transcript_result is geen dict: \{type\(transcript_result\)\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: transcript_result is geldig, ga door\.\.\."\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: transcript_result: \{transcript_result\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Transcript result is geldig, ga door naar volgende stap"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: transcript length: \{len\(transcript\)\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: transcriptions count: \{len\(transcriptions\)\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Test vertaling sectie\.\.\."\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Enable translation: \{enable_translation\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Vertaling ingeschakeld"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Vertaling fout voor segment: \{e\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Vertaling voltooid, \{len\(translated_transcriptions\)\} segmenten"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Geen vertaling"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Test video verwerking sectie\.\.\."\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: subtitle_type: \{self\.settings\.get\(\'subtitle_type\', \'softcoded\'\)\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Softcoded subtitles, genereer SRT bestanden\.\.\."\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Video result: \{video_result\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: SRT generatie gefaald: \{video_result\[\'error\'\]\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: SRT generatie succesvol!"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Hardcoded subtitles, skip SRT generatie"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Video verwerking voltooid!"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Transcript result is ongeldig of bevat error"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: \{error_message\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Geen transcriptie gegenereerd voor \{file_path\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: transcript_result keys: \{list\(transcript_result\.keys\(\)\)\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: transcript_result: \{transcript_result\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Placeholder transcriptie gemaakt: \{transcript\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Fast Whisper transcriptie voltooid voor \{file_path\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Gaat door naar volgende stap\.\.\."\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: transcript_result keys: \{list\(transcript_result\.keys\(\)\)\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: transcript length: \{len\(transcript\)\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: transcriptions count: \{len\(transcriptions\)\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: First transcription: \{transcriptions\[0\]\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: is_running: \{self\.is_running\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Gaat door naar vertaling sectie\.\.\."\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Verwerking gestopt na Whisper"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Verwerking gaat door\.\.\."\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Start vertaling sectie\.\.\."\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: enable_translation: \{self\.settings\.get\(\'enable_translation\', False\)\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Start vertaling voor \{file_path\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Vertaling instellingen - target: \{target_language\}, source: \{source_language\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Vertaling result: \{translation_result\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Vertaling voltooid voor \{file_path\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Start vertaling van transcriptions lijst"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Vertaling transcriptions voltooid: \{len\(translated_transcriptions\)\} segmenten"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Verwerking gestopt na vertaling"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Geen vertaling ingeschakeld, ga door naar video verwerking"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Vertaling sectie voltooid"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Start video verwerking sectie\.\.\."\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: subtitle_type: \{self\.settings\.get\(\'subtitle_type\', \'Niet ingesteld\'\)\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: is_running: \{self\.is_running\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Start hardcoded video verwerking voor \{file_path\}"\)',
        r'print\(f"🔍 \[DEBUG\] Video progress: \{ffmpeg_progress:\.1f\}% - \{progress_text\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Start SRT bestanden genereren voor \{file_path\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: transcriptions: \{len\(transcriptions\)\} segmenten"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: translated_transcriptions: \{translated_transcriptions is not None\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: settings: \{self\.settings\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Roep video_processor\.generate_srt_files aan"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: video_result: \{video_result\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: SRT bestanden succesvol gegenereerd"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Output files: \{video_result\[\'output_files\'\]\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: SRT generatie gefaald: \{video_result\.get\(\'error\'\)\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Video verwerking sectie voltooid"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: \{file_type\.upper\(\)\} bestand gegenereerd: \{file_path_srt\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Start cleanup sectie\.\.\."\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Cleanup sectie voltooid"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Bestand \{i\+1\}/\{total_files\} voltooid: \{file_path\}"\)',
        r'print\(f"🔍 \[DEBUG\] Signal uitgezonden: \{completed_signal\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Bestand verwerking voltooid"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Loop voltooid\. Completed: \{completed\}/\{total_files\}"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Verwerking voltooid!"\)',
        r'print\(f"🔍 \[DEBUG\] ProcessingThread\.run: Verwerking gestopt door gebruiker"\)',
    ]
    
    # Verwijder overbodige debug prints
    for pattern in remove_patterns:
        content = re.sub(pattern, '', content)
    
    # Schrijf het bestand terug
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Debug output opgeschoond!")
    print("📝 Alleen belangrijke debug berichten (fouten) zijn behouden")

if __name__ == "__main__":
    cleanup_debug_output()
