# Debug Logging en SRT Generatie Gids

## Problemen Geïdentificeerd

### 1. Console Logging Probleem
- **Debug logging was uitgeschakeld**: `LOG_TO_FILE=false` en `debug: False` in de logging config
- **Alleen INFO, WARNING, ERROR berichten werden getoond**: Debug berichten werden gefilterd
- **Test bericht 1 (debug) werd niet getoond**: Dit bevestigde dat debug logging uit stond

### 2. SRT Generatie Werkt Wel
- De SRT generatie functionaliteit werkt correct
- Test SRT bestand wordt succesvol aangemaakt met correcte inhoud

## Oplossingen Geïmplementeerd

### 1. Environment Variables Aangepast
```bash
# In magic_time_studio/whisper_config.env
LOG_LEVEL=DEBUG
LOG_TO_FILE=true
```

### 2. Logging Configuratie Aangepast
```python
# In magic_time_studio/core/config.py
"logging_config": {
    "debug": True,  # Zet debug logging aan standaard
    "info": True,
    "warning": True,
    "error": True
}
```

### 3. Debug Mode Forceren
```python
# In magic_time_studio/core/logging.py
# Forceer debug mode als LOG_LEVEL=DEBUG
if self.log_level == "DEBUG":
    # Toon alle berichten in debug mode
    pass
elif category in logging_config and not logging_config[category]:
    return
```

### 4. Verbeterde SRT Debug Logging
```python
# In magic_time_studio/processing/video_processor.py
logger.log_debug(f"🎬 Start SRT generatie voor: {safe_basename(video_path)}")
logger.log_debug(f"📄 Aantal transcriptions: {len(transcriptions)} segmenten")
logger.log_debug(f"📄 Segment {i}: {start_time} --> {end_time} - {text[:50]}...")
```

## Hoe Te Gebruiken

### Methode 1: Environment Variables Zetten
```bash
# Windows Command Prompt
set LOG_LEVEL=DEBUG
set LOG_TO_FILE=true
python magic_time_studio/run.py
```

### Methode 2: PowerShell Script
```powershell
# Gebruik het debug script
.\scripts\start_debug.ps1
```

### Methode 3: Batch Script
```cmd
# Gebruik het debug script
scripts\start_debug.bat
```

### Methode 4: Direct in Python
```python
import os
os.environ["LOG_LEVEL"] = "DEBUG"
os.environ["LOG_TO_FILE"] = "true"

# Start applicatie
from magic_time_studio.run import main
main()
```

## Debug Output Voorbeelden

### Console Logging
```
[02:28:03] 🎬 Start SRT generatie voor: video.mp4
[02:28:03] 📄 Video bestand gevonden: C:\path\to\video.mp4
[02:28:03] 📄 Aantal transcriptions: 15 segmenten
[02:28:03] 📄 Output directory: C:\path\to
[02:28:03] 📄 Video naam zonder extensie: video
[02:28:03] 📄 Settings gebruikt: {'generate_srt': True, ...}
[02:28:03] 📝 Originele ondertitels behouden: True
[02:28:03] 📄 Maak origineel SRT bestand: C:\path\to\video.srt
[02:28:03] 📄 Start SRT bestand maken: video.srt
[02:28:03] 📄 Aantal transcriptions: 15
[02:28:03] 📄 Segment 1: 00:00:00,000 --> 00:00:05,000 - Dit is de eerste zin...
[02:28:03] 📄 Segment 2: 00:00:05,000 --> 00:00:10,000 - Dit is de tweede zin...
...
[02:28:03] ✅ SRT bestand succesvol gemaakt: video.srt
[02:28:03] ✅ Origineel SRT bestand gemaakt: C:\path\to\video.srt
[02:28:03] 📄 SRT bestanden gegenereerd: 1 bestanden
[02:28:03] 📄 Output files: {'srt': 'C:\\path\\to\\video.srt'}
```

### Debug Log Bestand
Als `LOG_TO_FILE=true` is ingesteld, worden alle debug berichten ook opgeslagen in:
```
~/MagicTime_Output/MagicTime_debug_log.txt
```

## Troubleshooting

### Debug Berichten Verschijnen Niet
1. Controleer of `LOG_LEVEL=DEBUG` is ingesteld
2. Controleer of `LOG_TO_FILE=true` is ingesteld
3. Herstart de applicatie na het wijzigen van environment variables

### SRT Bestanden Worden Niet Gemaakt
1. Controleer of de video bestanden bestaan en leesbaar zijn
2. Controleer of er transcriptions zijn gegenereerd
3. Controleer de debug output voor foutmeldingen
4. Controleer of de output directory schrijfrechten heeft

### Console Output is Verwarrend
1. Gebruik de debug scripts om environment variables correct in te stellen
2. Controleer of er geen conflicterende .env bestanden zijn
3. Herstart de applicatie volledig na configuratie wijzigingen

## Belangrijke Bestanden

- `magic_time_studio/whisper_config.env` - Environment variables
- `magic_time_studio/core/logging.py` - Logging functionaliteit
- `magic_time_studio/core/config.py` - Configuratie management
- `magic_time_studio/processing/video_processor.py` - SRT generatie
- `scripts/start_debug.bat` - Debug start script (Windows)
- `scripts/start_debug.ps1` - Debug start script (PowerShell)

## Conclusie

De debug logging en SRT generatie functionaliteit werkt nu correct. De belangrijkste wijzigingen zijn:

1. **Debug logging is ingeschakeld** door environment variables aan te passen
2. **Verbeterde debug output** voor SRT generatie proces
3. **Debug scripts** voor eenvoudige start van de applicatie in debug mode
4. **Log bestand ondersteuning** voor persistente debug informatie

Gebruik de debug scripts om de applicatie te starten en alle debug informatie te zien in de console. 