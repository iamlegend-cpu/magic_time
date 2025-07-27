# Magic Time Studio v2.0

Een geavanceerde applicatie voor automatische ondertiteling en vertaling van video's, volledig herschreven met een modulaire architectuur.

## 🚀 Nieuwe Versie 2.0

Magic Time Studio v2.0 is een complete herstructurering van de originele applicatie met:

- ✅ **Modulaire architectuur** - Alle functionaliteit opgesplitst in logische modules
- ✅ **Identieke GUI** - Exact dezelfde interface als versie 1.9.4
- ✅ **Verbeterde onderhoudbaarheid** - Makkelijker uit te breiden en aan te passen
- ✅ **Thread-safe** - Veilige multi-threading voor betere performance
- ✅ **Moderne best practices** - Professionele code structuur

## 📁 Project Structuur

```
magic_time/
├── Magic_Time_Studio_v1.9.4.py    # Originele versie (behouden voor referentie)
├── magic_time_studio/             # Nieuwe modulaire versie v2.0
│   ├── core/                      # Kern functionaliteit
│   │   ├── config.py             # Configuratie management
│   │   ├── logging.py            # Logging systeem
│   │   └── utils.py              # Utility functies
│   ├── models/                   # Data modellen
│   │   ├── processing_queue.py   # Verwerkingswachtrij
│   │   ├── progress_tracker.py   # Voortgang tracking
│   │   └── performance_tracker.py # Performance monitoring
│   ├── ui/                       # Gebruikersinterface
│   │   ├── main_window.py        # Hoofdvenster
│   │   ├── themes.py             # Thema management
│   │   ├── config_window.py      # Configuratievenster
│   │   └── log_viewer.py         # Log viewer
│   ├── processing/               # Verwerkingsmodules
│   │   ├── whisper_processor.py  # Whisper transcriptie
│   │   ├── translator.py         # Vertaling
│   │   ├── audio_processor.py    # Audio verwerking
│   │   ├── video_processor.py    # Video verwerking
│   │   └── batch_processor.py    # Batch verwerking
│   ├── main.py                   # Hoofdapplicatie
│   ├── startup.py                # Startup script
│   ├── requirements.txt          # Dependencies
│   └── README.md                 # Documentatie
└── README.md                     # Dit bestand
```

## 🚀 Hoe te starten

### Optie 1: Startup script (aanbevolen)
```bash
python magic_time_studio/startup.py
```

### Optie 2: Direct uitvoeren
```bash
python magic_time_studio/run.py
```

### Optie 3: Als module
```bash
python -m magic_time_studio.main
```

### Dependencies installeren
```bash
pip install -r magic_time_studio/requirements.txt
```

## ✨ Belangrijkste Features

### 🎯 Identieke GUI
- **Exact dezelfde interface** als versie 1.9.4
- **Vertrouwde layout** met linker en rechter panel
- **Alle originele knoppen** en functionaliteit
- **Zelfde kleuren en styling**

### 🔧 Modulaire Architectuur
- **Core modules** voor configuratie, logging en utilities
- **UI modules** voor alle interface componenten
- **Processing modules** voor audio, video en vertaling
- **Data models** voor wachtrij en tracking

### 🚀 Geavanceerde Functionaliteit
- **Whisper AI** voor automatische transcriptie
- **LibreTranslate/Google Translate** voor vertaling
- **FFmpeg** voor audio/video verwerking
- **Batch verwerking** voor meerdere bestanden
- **Real-time logging** met live viewer
- **Thema ondersteuning** (dark, light, blue)
- **Performance monitoring**

### 📊 Output Formaten
- **SRT** - Standaard ondertiteling
- **VTT** - Web video ondertiteling
- **JSON** - Gestructureerde data
- **TXT** - Plain text transcriptie

## 🔄 Migratie van v1.9.4

### Wat is hetzelfde:
- ✅ **Identieke GUI** en gebruikerservaring
- ✅ **Alle originele functionaliteit**
- ✅ **Zelfde configuratie opties**
- ✅ **Zelfde output formaten**

### Wat is verbeterd:
- ✅ **Modulaire code structuur**
- ✅ **Betere error handling**
- ✅ **Thread-safe operaties**
- ✅ **Uitbreidbare architectuur**
- ✅ **Moderne Python best practices**

## 📋 Vereisten

- **Python 3.8+**
- **FFmpeg** (automatisch gedetecteerd of handmatig geïnstalleerd)
- **openai-whisper** (automatisch geïnstalleerd)
- **requests** (voor API calls)

## 🛠️ Ontwikkeling

### Project structuur begrijpen
```bash
# Core functionaliteit
magic_time_studio/core/           # Configuratie, logging, utilities

# Gebruikersinterface
magic_time_studio/ui/             # Alle GUI componenten

# Verwerking
magic_time_studio/processing/     # Audio, video, transcriptie, vertaling

# Data modellen
magic_time_studio/models/         # Wachtrij, tracking, monitoring
```

### Nieuwe module toevoegen
1. Maak een nieuwe Python file in de juiste directory
2. Voeg `__init__.py` toe voor package imports
3. Update de relevante `__init__.py` bestanden
4. Test de integratie

## 📝 Changelog

### v2.0.0 (Huidige versie)
- ✅ **Complete modulaire herstructurering**
- ✅ **Identieke GUI als v1.9.4**
- ✅ **Verbeterde error handling**
- ✅ **Thread-safe operaties**
- ✅ **Moderne Python architectuur**

### v1.9.4 (Origineel)
- Originele monolithische versie
- Behouden voor referentie en vergelijking

## 🤝 Bijdragen

1. Fork het project
2. Maak een feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit je wijzigingen (`git commit -m 'Add some AmazingFeature'`)
4. Push naar de branch (`git push origin feature/AmazingFeature`)
5. Open een Pull Request

## 📄 Licentie

Dit project is gelicenseerd onder de MIT License - zie het [LICENSE](LICENSE) bestand voor details.

## 🙏 Dankbetuiging

- **OpenAI Whisper** voor de transcriptie functionaliteit
- **LibreTranslate** voor de vertaling services
- **FFmpeg** voor audio/video verwerking
- **Tkinter** voor de GUI framework

---

**Magic Time Studio v2.0** - Professionele video ondertiteling en vertaling met modulaire architectuur! 🎬✨
