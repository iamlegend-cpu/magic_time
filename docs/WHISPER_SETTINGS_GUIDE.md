# Whisper Instellingen Gids

## 🔧 Hoe wisselen van Standaard naar Fast Whisper

Er zijn verschillende manieren om tussen Whisper types te wisselen in Magic Time Studio:

### **1. Eenvoudige Methode: Script Gebruiken**

#### Voor Fast Whisper:
```bash
# Python script
python scripts/switch_whisper_type.py fast

# Windows batch script
scripts/switch_whisper_type.bat fast
```

#### Voor Standaard Whisper:
```bash
# Python script
python scripts/switch_whisper_type.py standard

# Windows batch script
scripts/switch_whisper_type.bat standard
```

#### Huidige configuratie bekijken:
```bash
python scripts/switch_whisper_type.py status
```

### **2. Handmatige Methode: .env Bestand Bewerken**

Maak een `.env` bestand aan in de root van je project:

```env
# Whisper Type Configuratie
# Kies tussen "standard" en "fast"
WHISPER_TYPE=fast

# Standaard Whisper instellingen
DEFAULT_WHISPER_MODEL=large
WHISPER_DEVICE=cuda

# Fast Whisper instellingen
DEFAULT_FAST_WHISPER_MODEL=large-v3-turbo
FAST_WHISPER_DEVICE=cuda

# Andere instellingen
DEFAULT_THEME=dark
DEFAULT_FONT_SIZE=9
DEFAULT_WORKER_COUNT=4
DEFAULT_SUBTITLE_TYPE=softcoded
DEFAULT_HARDCODED_LANGUAGE=dutch_only
LOG_LEVEL=INFO
LOG_TO_FILE=false
AUTO_CREATE_OUTPUT_DIR=true
CPU_LIMIT_PERCENTAGE=80
MEMORY_LIMIT_MB=8192
AUTO_CLEANUP_TEMP=true
```

### **3. Runtime Wisselen in Code**

```python
from magic_time_studio.processing.whisper_manager import whisper_manager

# Wissel naar Fast Whisper
whisper_manager.switch_whisper_type("fast", "large-v3-turbo")

# Wissel naar Standaard Whisper
whisper_manager.switch_whisper_type("standard", "large")
```

## 📊 Configuratie Opties

### **Fast Whisper Instellingen**
```env
WHISPER_TYPE=fast
DEFAULT_FAST_WHISPER_MODEL=large-v3-turbo  # Snelste model
FAST_WHISPER_DEVICE=cuda                    # GPU versnelling
```

### **Standaard Whisper Instellingen**
```env
WHISPER_TYPE=standard
DEFAULT_WHISPER_MODEL=large                 # Beste kwaliteit
WHISPER_DEVICE=cuda                         # GPU versnelling
```

## 🎯 Aanbevolen Configuraties

### **Voor Snelle Verwerking (Content Creators)**
```env
WHISPER_TYPE=fast
DEFAULT_FAST_WHISPER_MODEL=large-v3-turbo
FAST_WHISPER_DEVICE=cuda
```
**Voordelen:**
- 6.8x sneller model loading
- 2-4x snellere transcriptie
- 50-70% minder geheugengebruik

### **Voor Stabiliteit (Production)**
```env
WHISPER_TYPE=standard
DEFAULT_WHISPER_MODEL=large
WHISPER_DEVICE=cuda
```
**Voordelen:**
- Zeer stabiel en betrouwbaar
- Goed getest
- Consistente resultaten

### **Voor Ontwikkeling (Developers)**
```env
WHISPER_TYPE=fast
DEFAULT_FAST_WHISPER_MODEL=medium
FAST_WHISPER_DEVICE=auto
```
**Voordelen:**
- Snelle iteratie
- Balans tussen snelheid en kwaliteit
- Auto-detect van beste device

## 🔍 Configuratie Controleren

### **Huidige Instellingen Bekijken**
```bash
python scripts/switch_whisper_type.py status
```

**Output voorbeeld:**
```
🔍 Huidige Whisper configuratie:

📁 Configuratie bestand: .env
  WHISPER_TYPE=fast
  DEFAULT_WHISPER_MODEL=large
  WHISPER_DEVICE=cuda
  DEFAULT_FAST_WHISPER_MODEL=large-v3-turbo
  FAST_WHISPER_DEVICE=cuda
```

### **Test Configuratie**
```bash
python tests/test_whisper_manager.py
```

## 🚀 Performance Vergelijking

| Feature | Standaard Whisper | Fast Whisper |
|---------|------------------|--------------|
| **Model Loading** | 19.18s | 2.80s (6.8x sneller) |
| **Transcriptie** | 1x baseline | 2-4x sneller |
| **Geheugen** | Hoog | 50-70% minder |
| **GPU Support** | Basis | Geoptimaliseerd |
| **Modellen** | 5 standaard | 10 (incl. turbo) |

## ⚠️ Belangrijke Notities

### **1. Fast Whisper Installatie**
Zorg ervoor dat Fast Whisper geïnstalleerd is:
```bash
# In de virtual environment
pyqt6_env\Scripts\activate
pip install faster-whisper
```

### **2. GPU Ondersteuning**
Voor beste prestaties:
- **CUDA**: Voor NVIDIA GPU's
- **MPS**: Voor Apple Silicon
- **CPU**: Fallback optie

### **3. Model Keuze**
- **large-v3-turbo**: Snelste Fast Whisper model
- **large**: Beste kwaliteit standaard Whisper
- **medium**: Goede balans voor ontwikkeling

## 🔄 Migratie van Oude Code

### **Van Standaard Whisper**
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

### **Naar Fast Whisper**
```python
# Wissel naar Fast Whisper
whisper_manager.switch_whisper_type("fast", "large-v3-turbo")
result = whisper_manager.transcribe_audio("video.mp4")
```

## 🎉 Conclusie

Met deze gids kun je eenvoudig wisselen tussen Whisper types:

1. **Script methode**: `python scripts/switch_whisper_type.py fast`
2. **Handmatig**: Bewerk `.env` bestand
3. **Runtime**: Gebruik `whisper_manager.switch_whisper_type()`

**Aanbeveling**: Gebruik Fast Whisper voor snelle verwerking en Standaard Whisper voor kritieke toepassingen waar stabiliteit belangrijk is. 