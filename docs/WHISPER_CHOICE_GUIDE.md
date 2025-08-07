# Whisper Keuze Gids voor Magic Time Studio

## Overzicht

Magic Time Studio ondersteunt nu **beide** Whisper types:

- 🐌 **Standaard Whisper** - Originele OpenAI Whisper
- 🚀 **Fast Whisper** - Geoptimaliseerde versie

## Whisper Manager

De nieuwe `WhisperManager` beheert beide types en biedt een uniforme interface:

```python
from magic_time_studio.processing.whisper_manager import whisper_manager

# Initialiseer met standaard Whisper
whisper_manager.initialize("standard", "large")

# Of initialiseer met Fast Whisper
whisper_manager.initialize("fast", "large-v3-turbo")

# Transcribeer audio (werkt met beide types)
result = whisper_manager.transcribe_audio("video.mp4")
```

## Vergelijking

| Feature | Standaard Whisper | Fast Whisper |
|---------|------------------|--------------|
| **Snelheid** | 1x (baseline) | 2-4x sneller |
| **Geheugen** | Hoog | 50-70% minder |
| **GPU Support** | Basis | Geoptimaliseerd |
| **Modellen** | Standaard | + Turbo modellen |
| **Stabiliteit** | Zeer stabiel | Goed |
| **Compatibiliteit** | Breed ondersteund | Nieuw |
| **Installatie** | Standaard | Extra stap |

## Wanneer Welke Kiezen?

### 🚀 Kies Fast Whisper voor

- **Snelle transcriptie** van grote bestanden
- **GPU beschikbaar** (NVIDIA/AMD)
- **Geheugen beperkt** systeem
- **Batch processing** van meerdere bestanden
- **Real-time** toepassingen

### 🐌 Kies Standaard Whisper voor

- **Maximale stabiliteit** vereist
- **CPU-only** systeem
- **Kleine bestanden** (< 10 minuten)
- **Kritieke toepassingen** waar betrouwbaarheid voorop staat
- **Compatibiliteit** met oudere systemen

## Configuratie

### Environment Variables

```env
# Whisper type keuze
WHISPER_TYPE=fast                    # "fast" of "standard"

# Standaard Whisper configuratie
DEFAULT_WHISPER_MODEL=large          # tiny, base, small, medium, large
WHISPER_DEVICE=auto                  # auto, cuda, cpu, mps

# Fast Whisper configuratie
DEFAULT_FAST_WHISPER_MODEL=large-v3-turbo  # + turbo modellen
FAST_WHISPER_DEVICE=auto             # auto, cuda, cpu, mps
```

### Aanbevolen Configuraties

#### Voor Snelle Transcriptie

```env
WHISPER_TYPE=fast
DEFAULT_FAST_WHISPER_MODEL=large-v3-turbo
FAST_WHISPER_DEVICE=auto
```

#### Voor Beste Kwaliteit

```env
WHISPER_TYPE=fast
DEFAULT_FAST_WHISPER_MODEL=large-v3-turbo
FAST_WHISPER_DEVICE=cuda
```

#### Voor Stabiliteit

```env
WHISPER_TYPE=standard
DEFAULT_WHISPER_MODEL=large
WHISPER_DEVICE=auto
```

#### Voor Lage Resources

```env
WHISPER_TYPE=fast
DEFAULT_FAST_WHISPER_MODEL=medium
FAST_WHISPER_DEVICE=cpu
```

## Gebruik in Code

### Basis Gebruik

```python
from magic_time_studio.processing.whisper_manager import whisper_manager

# Auto-detect en laad beste optie
whisper_manager.initialize()

# Of specifiek type
whisper_manager.initialize("fast", "large-v3-turbo")

# Transcribeer
result = whisper_manager.transcribe_audio("video.mp4")
```

### Type Wisselen

```python
# Wissel van standaard naar fast
whisper_manager.switch_whisper_type("fast", "large-v3-turbo")

# Wissel van fast naar standaard
whisper_manager.switch_whisper_type("standard", "large")
```

### Performance Vergelijking

```python
comparison = whisper_manager.get_performance_comparison()
print(f"Fast beschikbaar: {comparison['fast_available']}")
print(f"Standard beschikbaar: {comparison['standard_available']}")
print(f"Huidig type: {comparison['current_type']}")
```

## UI Component

De `WhisperSelectorWidget` biedt een grafische interface:

```python
from magic_time_studio.ui_pyqt6.components.whisper_selector import WhisperSelectorWidget

# Maak widget
selector = WhisperSelectorWidget()

# Connect signals
selector.whisper_changed.connect(on_whisper_changed)
selector.model_loaded.connect(on_model_loaded)
```

## Installatie

### 1. Standaard Whisper (altijd beschikbaar)

```bash
pip install openai-whisper
```

### 2. Fast Whisper (optioneel)

```bash
# Via script
python scripts/install_fast_whisper.py

# Of handmatig
pip install fast-whisper
```

### 3. Test Beide

```bash
python tests/test_whisper_manager.py
```

## Performance Tips

### Voor Fast Whisper

- **GPU**: Gebruik CUDA voor beste prestaties
- **Model**: `large-v3-turbo` voor beste kwaliteit/snelheid
- **Batch**: Verwerk meerdere bestanden tegelijk
- **Memory**: Monitor geheugengebruik

### Voor Standaard Whisper

- **Model**: `large` voor beste kwaliteit
- **CPU**: Multi-core CPU voor betere prestaties
- **Memory**: Zorg voor voldoende RAM
- **Batch**: Verwerk één bestand tegelijk

## Troubleshooting

### Fast Whisper Problemen

**Import Error**

```
❌ Fast Whisper niet geïnstalleerd
```

**Oplossing:**

```bash
python scripts/install_fast_whisper.py
```

**CUDA Error**

```
❌ CUDA niet beschikbaar
```

**Oplossing:**

```env
FAST_WHISPER_DEVICE=cpu
```

**Memory Error**

```
❌ Onvoldoende geheugen
```

**Oplossing:**

```env
DEFAULT_FAST_WHISPER_MODEL=medium
```

### Standaard Whisper Problemen

**Model Download Error**

```
❌ Model download gefaald
```

**Oplossing:** Controleer internetverbinding

**CUDA Error**

```
❌ CUDA niet beschikbaar
```

**Oplossing:**

```env
WHISPER_DEVICE=cpu
```

## Migratie van Oude Code

### Van Standaard Whisper

```python
# Oud
from magic_time_studio.processing.whisper_processor import whisper_processor
whisper_processor.initialize("large")
result = whisper_processor.transcribe_audio("video.mp4")

# Nieuw
from magic_time_studio.processing.whisper_manager import whisper_manager
whisper_manager.initialize("standard", "large")
result = whisper_manager.transcribe_audio("video.mp4")
```

### Naar Fast Whisper

```python
# Wissel naar Fast Whisper
whisper_manager.switch_whisper_type("fast", "large-v3-turbo")
result = whisper_manager.transcribe_audio("video.mp4")
```

## Aanbevelingen per Gebruik

### Content Creators

- **Type**: Fast Whisper
- **Model**: `large-v3-turbo`
- **Device**: `cuda` (als beschikbaar)

### Developers

- **Type**: Beide beschikbaar houden
- **Model**: `large` (standard) / `large-v3-turbo` (fast)
- **Device**: `auto`

### Production Systems

- **Type**: Standaard Whisper
- **Model**: `large`
- **Device**: `auto`

### Testing/Development

- **Type**: Fast Whisper
- **Model**: `medium`
- **Device**: `cpu`

## Support

Voor vragen of problemen:

1. **Test beide types**: `python tests/test_whisper_manager.py`
2. **Controleer configuratie**: Environment variables
3. **Vergelijk performance**: Gebruik performance vergelijking
4. **Check logs**: Debug mode aanzetten

## Changelog

- **v1.0**: Eerste implementatie van Whisper Manager
- **v1.1**: Toegevoegd Fast Whisper ondersteuning
- **v1.2**: UI component voor type selectie
- **v1.3**: Performance vergelijking en aanbevelingen
- **v1.4**: Verbeterde error handling en switching
