# WhisperX SRT Functies - Magic Time Studio

## Overzicht

Deze module biedt geavanceerde SRT ondertitel functionaliteit met WhisperX word-level alignment voor maximale timing accuracy. WhisperX SRT functies zijn geïntegreerd in de bestaande subtitle en whisper functies.

## Functies

### 1. WhisperX Transcriptie met Word-Level Alignment

```python
from core.whisper_functions import transcribe_audio_whisperx

# Transcribeer audio met word-level alignment
result = transcribe_audio_whisperx(
    audio_path="audio.mp3",
    model_name="large-v3",
    language="nl",
    word_level=True  # Schakel word-level alignment in
)

if result and result.get("word_level_available"):
    print("✅ Word-level alignment beschikbaar")
    transcriptions = result["transcriptions"]
    word_alignments = result["word_alignments"]
else:
    print("⚠️ Alleen standaard timing beschikbaar")
```

### 2. WhisperX SRT Bestand Maken

```python
from core.whisper_functions import create_whisperx_srt_file

# Maak SRT bestand met word-level timing
success = create_whisperx_srt_file(
    transcriptions=result["transcriptions"],
    output_path="output.srt",
    word_alignments=result["word_alignments"],
    enhanced=True  # Gebruik verbeterde SRT met word timing info
)
```

### 3. Geïntegreerde SRT Generatie

```python
from core.subtitle_functions import create_srt_content

# Automatisch WhisperX SRT gebruiken als beschikbaar
success = create_srt_content(
    transcriptions=result["transcriptions"],
    output_path="output.srt",
    use_whisperx=True,  # Schakel WhisperX SRT in
    word_alignments=result["word_alignments"]
)
```

### 4. Directe WhisperX SRT Functies

```python
from core.whisperx_srt_functions import (
    create_whisperx_srt_content,
    create_enhanced_srt_with_word_timing,
    validate_whisperx_transcriptions,
    get_whisperx_statistics
)

# Valideer transcripties
is_valid = validate_whisperx_transcriptions(transcriptions)

# Krijg statistieken
stats = get_whisperx_statistics(transcriptions, word_alignments)
print(f"Totaal segmenten: {stats['total_segments']}")
print(f"Totaal duur: {stats['total_duration_formatted']}")
print(f"Word-level alignment: {stats['word_level_alignment']}")
```

## Beschikbaarheid Controleren

```python
from core.whisper_functions import is_whisperx_srt_available
from core.subtitle_functions import is_whisperx_srt_available as sub_is_available

# Controleer beschikbaarheid
whisper_available = is_whisperx_srt_available()
subtitle_available = sub_is_available()

if whisper_available and subtitle_available:
    print("✅ WhisperX SRT functies volledig beschikbaar")
elif whisper_available:
    print("⚠️ Alleen basis WhisperX functies beschikbaar")
else:
    print("❌ WhisperX functies niet beschikbaar")
```

## Voordelen van WhisperX SRT

### 1. **Betere Timing Accuracy**

- Word-level alignment voor milliseconde precisie
- Nauwkeurige segmentatie van transcripties
- Consistente timing tussen woorden en segmenten

### 2. **Geavanceerde Functies**

- Automatische fallback naar standaard SRT
- Ondersteuning voor verschillende talen
- Word-level statistieken en validatie

### 3. **Integratie**

- Volledig geïntegreerd in bestaande subtitle functies
- Automatische detectie van beschikbaarheid
- Consistent API design

## Fallback Gedrag

Als WhisperX SRT functies niet beschikbaar zijn of falen, valt het systeem automatisch terug naar standaard SRT generatie:

```python
# Automatische fallback
success = create_srt_content(
    transcriptions=transcriptions,
    output_path="output.srt",
    use_whisperx=True,  # Probeer WhisperX eerst
    word_alignments=word_alignments
)

# Als WhisperX faalt, wordt standaard SRT gebruikt
# Geen fout - alleen waarschuwing in logs
```

## Testen

Gebruik het test bestand om te controleren of alle functies werken:

```bash
cd core
python test_whisperx_srt.py
```

## Vereisten

- WhisperX geïnstalleerd: `pip install whisperx`
- PyTorch voor GPU ondersteuning (optioneel)
- Audio bestanden in ondersteunde formaten

## Ondersteunde Modellen

- **tiny**: 39M parameters (snel, minder accuraat)
- **base**: 74M parameters (balans)
- **small**: 244M parameters (goed)
- **medium**: 769M parameters (zeer goed)
- **large**: 1550M parameters (beste)
- **large-v2**: 1550M parameters (verbeterde versie)
- **large-v3**: 1550M parameters (nieuwste versie)

## Voorbeelden

### Volledig Voorbeeld

```python
from core.whisper_functions import transcribe_audio_whisperx, create_whisperx_srt_file

# 1. Transcribeer audio
result = transcribe_audio_whisperx(
    audio_path="presentatie.mp4",
    model_name="large-v3",
    language="nl",
    word_level=True
)

if result:
    # 2. Maak SRT bestand
    success = create_whisperx_srt_file(
        transcriptions=result["transcriptions"],
        output_path="presentatie.srt",
        word_alignments=result["word_alignments"],
        enhanced=True
    )
    
    if success:
        print("✅ WhisperX SRT bestand succesvol aangemaakt")
    else:
        print("❌ SRT bestand maken gefaald")
else:
    print("❌ Transcriptie gefaald")
```

### Batch Verwerking

```python
import os
from core.whisper_functions import transcribe_audio_whisperx, create_whisperx_srt_file

audio_files = ["file1.mp3", "file2.mp3", "file3.mp3"]

for audio_file in audio_files:
    if os.path.exists(audio_file):
        # Transcribeer
        result = transcribe_audio_whisperx(audio_file, word_level=True)
        
        if result:
            # Maak SRT
            srt_file = audio_file.replace(".mp3", ".srt")
            create_whisperx_srt_file(
                result["transcriptions"],
                srt_file,
                result["word_alignments"]
            )
```

## Troubleshooting

### 1. **WhisperX niet beschikbaar**

```bash
pip install whisperx
```

### 2. **GPU ondersteuning**

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 3. **Memory problemen**

- Gebruik kleiner model (tiny, base, small)
- Schakel word_level uit: `word_level=False`

### 4. **Timing problemen**

- Controleer audio bestand integriteit
- Gebruik ondersteunde audio formaten
- Valideer transcripties met `validate_whisperx_transcriptions()`

## Logging

Alle functies gebruiken Python logging voor debugging:

```python
import logging
logging.basicConfig(level=logging.INFO)

# Nu zie je alle debug informatie
```

## Support

Voor problemen of vragen:

1. Controleer de logs voor foutmeldingen
2. Test met het test bestand
3. Controleer of alle dependencies geïnstalleerd zijn
4. Valideer audio bestanden en transcripties
