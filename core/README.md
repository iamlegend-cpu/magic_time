# Magic Time Studio Core Module

Dit is de kern module van Magic Time Studio met alle functionaliteit georganiseerd in aparte bestanden per categorie.

## Structuur

```
core/
├── __init__.py              # Hoofdmodule import
├── all_functions.py         # Alle functies samen in één overzicht
├── audio_functions.py       # Audio-gerelateerde functies
├── video_functions.py       # Video-gerelateerde functies
├── whisper_functions.py     # Whisper transcriptie functies
├── translation_functions.py # Vertaling functies
├── subtitle_functions.py    # Ondertitel functies
├── file_functions.py        # Bestand beheer functies
├── config.py               # Configuratie management
├── logging.py              # Logging functionaliteit
├── utils.py                # Algemene utilities
├── stop_manager.py         # Stop management
├── diagnostics.py          # Diagnostische functies
└── README.md               # Dit bestand
```

## Functie Categorieën

### 1. Audio Functies (`audio_functions.py`)
- `extract_audio_from_video()` - Audio extraheren uit video
- `get_audio_duration()` - Audio duur bepalen
- `convert_audio_format()` - Audio formaat converteren
- `normalize_audio()` - Audio volume normaliseren
- `split_audio_by_silence()` - Audio splitsen op stilte

### 2. Video Functies (`video_functions.py`)
- `get_video_info()` - Video informatie ophalen
- `get_video_duration()` - Video duur bepalen
- `get_video_resolution()` - Video resolutie bepalen
- `extract_video_frame()` - Frame uit video extraheren
- `create_video_thumbnail()` - Video thumbnail maken
- `merge_video_audio()` - Video en audio samenvoegen
- `convert_video_format()` - Video formaat converteren
- `compress_video()` - Video comprimeren

### 3. Whisper Functies (`whisper_functions.py`)
- `load_whisper_model()` - Whisper model laden
- `transcribe_audio_fast_whisper()` - Audio transcriberen met fast-whisper
- `transcribe_audio_standard_whisper()` - Audio transcriberen met standaard whisper
- `detect_language()` - Taal detecteren
- `transcribe_with_timestamps()` - Transcriptie met timestamps
- `save_transcription_to_srt()` - Transcriptie opslaan als SRT
- `format_timestamp()` - Timestamp formatteren
- `get_whisper_model_info()` - Model informatie ophalen

### 4. Vertaling Functies (`translation_functions.py`)
- `translate_text_libretranslate()` - Tekst vertalen met LibreTranslate
- `translate_text_google()` - Tekst vertalen met Google Translate
- `translate_text_deepl()` - Tekst vertalen met DeepL
- `translate_text()` - Algemene vertaling functie
- `translate_transcriptions()` - Transcripties vertalen
- `batch_translate_texts()` - Meerdere teksten vertalen
- `detect_language_from_text()` - Taal detecteren uit tekst
- `get_supported_languages()` - Ondersteunde talen ophalen

### 5. Ondertitel Functies (`subtitle_functions.py`)
- `create_srt_content()` - SRT ondertitel bestand maken
- `create_vtt_content()` - WebVTT ondertitel bestand maken
- `create_ass_content()` - ASS/SSA ondertitel bestand maken
- `format_timestamp()` - Timestamp formatteren
- `merge_subtitle_files()` - Ondertitel bestanden samenvoegen
- `read_subtitle_file()` - Ondertitel bestand lezen
- `read_srt_file()` - SRT bestand lezen
- `read_vtt_file()` - VTT bestand lezen
- `read_ass_file()` - ASS bestand lezen

### 6. Bestand Functies (`file_functions.py`)
- `is_video_file()` - Controleer of bestand een video is
- `is_audio_file()` - Controleer of bestand een audio is
- `is_subtitle_file()` - Controleer of bestand een ondertitel is
- `get_file_info()` - Bestand informatie ophalen
- `get_directory_files()` - Bestanden uit directory ophalen
- `get_video_files()` - Video bestanden ophalen
- `get_audio_files()` - Audio bestanden ophalen
- `get_subtitle_files()` - Ondertitel bestanden ophalen
- `create_temp_file()` - Tijdelijk bestand maken
- `copy_file()` - Bestand kopiëren
- `move_file()` - Bestand verplaatsen
- `delete_file()` - Bestand verwijderen
- `backup_file()` - Backup maken
- `restore_backup()` - Backup herstellen

## Gebruik

### Basis Import
```python
from magic_time_studio.core import all_functions

# Alle functies zijn nu beschikbaar
audio_path = all_functions.extract_audio_from_video("video.mp4")
```

### Specifieke Module Import
```python
from magic_time_studio.core import audio_functions, video_functions

# Audio functies
audio_path = audio_functions.extract_audio_from_video("video.mp4")

# Video functies
video_info = video_functions.get_video_info("video.mp4")
```

### Functie Categorieën Bekijken
```python
from magic_time_studio.core.all_functions import get_all_categories, get_functions_by_category

# Alle categorieën bekijken
categories = get_all_categories()
print(f"Beschikbare categorieën: {categories}")

# Functies in een categorie bekijken
audio_functions = get_functions_by_category("Audio")
print(f"Audio functies: {audio_functions}")
```

### Functies Zoeken
```python
from magic_time_studio.core.all_functions import search_functions

# Zoek functies met "video" in de naam
video_functions = search_functions("video")
print(f"Video-gerelateerde functies: {video_functions}")
```

## Voordelen van de Nieuwe Structuur

1. **Modulair**: Elke functie categorie heeft zijn eigen bestand
2. **Overzichtelijk**: Duidelijke scheiding van functionaliteit
3. **Onderhoudbaar**: Makkelijk om specifieke functies te vinden en aan te passen
4. **Uitbreidbaar**: Nieuwe functies kunnen eenvoudig toegevoegd worden
5. **Herbruikbaar**: Functies kunnen onafhankelijk geïmporteerd worden
6. **Testbaar**: Elke module kan apart getest worden

## Toevoegen van Nieuwe Functies

1. **Bepaal de categorie** van je nieuwe functie
2. **Voeg de functie toe** aan het juiste bestand
3. **Update `all_functions.py`** met de nieuwe functie naam
4. **Update de categorie lijst** in `all_functions.py`
5. **Test de functie** om er zeker van te zijn dat deze werkt

## Voorbeeld van Nieuwe Functie Toevoegen

```python
# In video_functions.py
def new_video_function(video_path: str) -> bool:
    """
    Nieuwe video functie
    
    Args:
        video_path: Pad naar het video bestand
    
    Returns:
        True bij succes, False bij fout
    """
    try:
        # Implementatie hier
        return True
    except Exception as e:
        logger.error(f"Fout bij nieuwe video functie: {e}")
        return False

# In all_functions.py toevoegen:
__all__.append('new_video_function')
FUNCTION_CATEGORIES["Video"].append('new_video_function')
```

## Afhankelijkheden

Deze module heeft de volgende externe afhankelijkheden:
- `PyQt6` - Voor UI functies
- `requests` - Voor API calls (vertaling)
- `ffmpeg` - Voor audio/video verwerking (moet geïnstalleerd zijn op systeem)
- `whisper` of `fast-whisper` - Voor transcriptie

## Licentie

Dit project is onderdeel van Magic Time Studio en volgt dezelfde licentie voorwaarden.
