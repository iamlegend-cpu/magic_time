# 🚀 Magic Time Studio v2.0.0 - Installatie Instructies

## 📋 Vereisten

### Systeem Vereisten
- **Python 3.8 of hoger**
- **FFmpeg** (automatisch gedetecteerd of handmatig geïnstalleerd)
- **Windows 10/11** (getest), **Linux** (compatibel), **macOS** (compatibel)

### Python Dependencies
- openai-whisper
- requests
- tkinter (meestal meegeleverd met Python)

## 🛠️ Installatie Stappen

### Stap 1: Python Installeren
1. Download Python 3.8+ van [python.org](https://www.python.org/downloads/)
2. Installeer Python met "Add to PATH" optie aangevinkt
3. Controleer installatie: `python --version`

### Stap 2: FFmpeg Installeren (indien nodig)
Magic Time Studio detecteert automatisch FFmpeg als het geïnstalleerd is.

**Windows:**
1. Download FFmpeg van [ffmpeg.org](https://ffmpeg.org/download.html)
2. Pak uit naar `C:\ffmpeg\`
3. Voeg `C:\ffmpeg\bin` toe aan PATH

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

### Stap 3: Magic Time Studio Installeren

#### Optie A: Van ZIP bestand
1. Download `Magic_Time_Studio_v2.0.0.zip`
2. Pak uit naar gewenste locatie
3. Open terminal/command prompt in de uitgepakte map
4. Installeer dependencies:
   ```bash
   pip install -r requirements.txt
   ```

#### Optie B: Van Source Code
1. Download `Magic_Time_Studio_v2.0.0_source.zip`
2. Pak uit naar gewenste locatie
3. Open terminal/command prompt in de `magic_time_studio` map
4. Installeer dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Stap 4: Applicatie Starten

#### Eenvoudige start (aanbevolen):
```bash
python startup.py
```

#### Alternatieve start methoden:
```bash
# Direct uitvoeren
python run.py

# Als module
python -m main
```

## 🎯 Eerste Gebruik

### 1. Applicatie Starten
- Start de applicatie met `python startup.py`
- De GUI verschijnt met de vertrouwde v1.9.4 layout

### 2. Configuratie
- Ga naar **Instellingen → Configuratie** voor API keys en instellingen
- Stel je voorkeuren in voor Whisper model, vertaler, etc.

### 3. Bestanden Toevoegen
- Klik **"Voeg een bestand toe"** of **"Voeg een map toe"**
- Selecteer video bestanden (.mp4, .avi, .mkv, etc.)

### 4. Verwerking Starten
- Stel taal en instellingen in
- Klik **"Start ondertiteling"**
- Monitor voortgang in de rechter panel

## 🔧 Troubleshooting

### Python niet gevonden
```bash
# Controleer Python installatie
python --version
# of
python3 --version
```

### Dependencies installatie problemen
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Installeer dependencies met verbose output
pip install -r requirements.txt -v
```

### FFmpeg niet gevonden
```bash
# Controleer FFmpeg installatie
ffmpeg -version
```

### Whisper model download problemen
- De eerste keer dat je Whisper gebruikt, wordt het model automatisch gedownload
- Dit kan enkele minuten duren afhankelijk van je internetverbinding
- Zorg voor een stabiele internetverbinding

### GUI problemen
```bash
# Voor Linux, installeer tkinter indien nodig
sudo apt install python3-tk

# Voor macOS, installeer tkinter indien nodig
brew install python-tk
```

## 📁 Bestandsstructuur

Na installatie heb je deze structuur:
```
magic_time_studio/
├── core/              # Kern modules
├── models/            # Data modellen
├── ui/                # Gebruikersinterface
├── processing/        # Verwerkingsmodules
├── main.py           # Hoofdapplicatie
├── startup.py        # Startup script
├── requirements.txt  # Dependencies
└── README.md         # Documentatie
```

## 🎬 Gebruik

### Basis Workflow
1. **Start applicatie** → `python startup.py`
2. **Voeg bestanden toe** → Klik "Voeg een bestand toe"
3. **Configureer instellingen** → Taal, model, vertaler
4. **Start verwerking** → Klik "Start ondertiteling"
5. **Bekijk resultaten** → SRT bestanden worden gegenereerd

### Geavanceerde Features
- **Batch verwerking** → Verwerk meerdere bestanden tegelijk
- **Configuratievenster** → Uitgebreide instellingen
- **Log viewer** → Real-time logging
- **Thema switching** → Dark, light, blue thema's

## 📞 Support

### Documentatie
- Zie `README.md` voor uitgebreide documentatie
- Zie `RELEASE_v2.0.0.md` voor release notes

### Issues
- Open een issue op GitHub voor bugs of feature requests
- Zorg voor gedetailleerde beschrijving van het probleem

### Community
- We verwelkomen bijdragen van de community
- Zie CONTRIBUTING.md voor richtlijnen

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

---

**Magic Time Studio v2.0.0** - Professionele video ondertiteling en vertaling! 🎬✨

**Releasedatum:** 27 juli 2025  
**Versie:** 2.0.0  
**Compatibiliteit:** Python 3.8+ 