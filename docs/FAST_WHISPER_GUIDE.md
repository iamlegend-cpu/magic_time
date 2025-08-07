# Fast Whisper Gids voor Magic Time Studio

## Wat is Fast Whisper?

**Fast Whisper** is een geoptimaliseerde versie van OpenAI's Whisper die:

- 🚀 **2-4x sneller** is dan standaard Whisper
- 💾 **Minder geheugen** gebruikt
- 🎯 **Betere GPU ondersteuning** heeft
- 📦 **Meer modellen** ondersteunt, inclusief `large-v3-turbo`

## Nieuwe Modellen

Fast Whisper ondersteunt alle standaard Whisper modellen plus:

- `large-v1` - Eerste grote model
- `large-v2` - Verbeterde versie
- `large-v3` - Nieuwste standaard grote model
- `large-v3-turbo` - **Nieuwste en snelste model** ⭐
- `turbo` - Alias voor large-v3-turbo

## Installatie

### 1. Installeer Fast Whisper

Voer het install script uit:

```bash
python scripts/install_fast_whisper.py
```

Of handmatig in de PyQt6 virtual environment:

```bash
# Activeer virtual environment
pyqt6_env\Scripts\activate  # Windows
# of
source pyqt6_env/bin/activate  # Linux/Mac

# Installeer Fast Whisper
pip install fast-whisper
```

### 2. Test de Installatie

```bash
python tests/test_fast_whisper.py
```

## Configuratie

### Environment Variables

Voeg deze variabelen toe aan je `.env` bestand:

```env
# Fast Whisper configuratie
DEFAULT_FAST_WHISPER_MODEL=large-v3-turbo
FAST_WHISPER_DEVICE=auto
```

### Beschikbare Opties

**Modellen:**

- `tiny` - Zeer snel, lage kwaliteit
- `base` - Snel, basis kwaliteit
- `small` - Gemiddelde snelheid/kwaliteit
- `medium` - Langzamer, goede kwaliteit
- `large` - Langzaam, beste kwaliteit
- `large-v3-turbo` - **Aanbevolen** - Nieuwste en snelste

**Devices:**

- `auto` - Automatische detectie (aanbevolen)
- `cuda` - GPU versnelling
- `cpu` - CPU alleen
- `mps` - Apple Silicon

## Gebruik in Magic Time Studio

### 1. Fast Whisper Processor

De nieuwe `FastWhisperProcessor` is beschikbaar in:

```python
from magic_time_studio.processing.fast_whisper_processor import fast_whisper_processor
```

### 2. Vergelijking met Standaard Whisper

| Feature | Standaard Whisper | Fast Whisper |
|---------|------------------|--------------|
| Snelheid | 1x | 2-4x sneller |
| Geheugen | Hoog | Laag |
| GPU Support | Basis | Geoptimaliseerd |
| Modellen | Standaard | + Turbo modellen |
| Taal Detectie | Basis | Verbeterd |

### 3. Performance Vergelijking

Typische snelheidsverbeteringen:

- **CPU**: 2-3x sneller
- **GPU**: 3-4x sneller
- **Geheugen**: 50-70% minder gebruik

## Voorbeelden

### Basis Gebruik

```python
from magic_time_studio.processing.fast_whisper_processor import fast_whisper_processor

# Initialiseer met large-v3-turbo
fast_whisper_processor.initialize("large-v3-turbo")

# Transcribeer audio
result = fast_whisper_processor.transcribe_audio("video.mp4")

if result.get("success"):
    print(f"Transcript: {result['transcript']}")
    print(f"Taal: {result['language']}")
    print(f"Segmenten: {result['segments']}")
```

### Met Progress Callback

```python
def progress_callback(progress_bar):
    print(f"Voortgang: {progress_bar}")

result = fast_whisper_processor.transcribe_audio(
    "video.mp4",
    progress_callback=progress_callback
)
```

### Taal Detectie

```python
# Automatische taal detectie
detected_language = fast_whisper_processor.detect_language("video.mp4")
print(f"Gedetecteerde taal: {detected_language}")
```

## Troubleshooting

### Veelvoorkomende Problemen

**1. Import Error**

```
❌ Fast Whisper niet geïnstalleerd. Installeer met: pip install fast-whisper
```

**Oplossing:** Voer het install script uit of installeer handmatig.

**2. CUDA Error**

```
❌ CUDA niet beschikbaar
```

**Oplossing:** Zet `FAST_WHISPER_DEVICE=cpu` in je `.env` bestand.

**3. Model Download Error**

```
❌ Model download gefaald
```

**Oplossing:** Controleer je internetverbinding en probeer opnieuw.

### Debug Mode

Zet debug mode aan voor meer informatie:

```python
# In fast_whisper_processor.py
DEBUG_MODE = True
```

## Migratie van Standaard Whisper

### Stap 1: Installeer Fast Whisper

```bash
python scripts/install_fast_whisper.py
```

### Stap 2: Update Configuratie

```env
# Vervang standaard Whisper configuratie
DEFAULT_FAST_WHISPER_MODEL=large-v3-turbo
FAST_WHISPER_DEVICE=auto
```

### Stap 3: Test Performance

```bash
python tests/test_fast_whisper.py
```

### Stap 4: Update Code (Optioneel)

Vervang imports in je code:

```python
# Oud
from magic_time_studio.processing.whisper_processor import whisper_processor

# Nieuw
from magic_time_studio.processing.fast_whisper_processor import fast_whisper_processor
```

## Aanbevelingen

### Voor Snelle Transcriptie

- **Model**: `large-v3-turbo`
- **Device**: `auto` (automatische GPU detectie)
- **Compute Type**: `float16` (GPU) of `int8` (CPU)

### Voor Beste Kwaliteit

- **Model**: `large-v3-turbo`
- **Device**: `cuda` (als beschikbaar)
- **Beam Size**: 5
- **Best Of**: 5

### Voor Lage Resource Gebruik

- **Model**: `medium` of `small`
- **Device**: `cpu`
- **Compute Type**: `int8`

## Support

Voor vragen of problemen:

1. Controleer de debug logs
2. Test met het test script
3. Vergelijk met standaard Whisper
4. Controleer je hardware configuratie

## Changelog

- **v1.0**: Eerste implementatie van Fast Whisper
- **v1.1**: Toegevoegd large-v3-turbo ondersteuning
- **v1.2**: Verbeterde GPU optimalisatie
- **v1.3**: Toegevoegd progress tracking en error handling
