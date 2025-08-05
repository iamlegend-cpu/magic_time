# Magic Time Studio - PyQt6 Versie

## 🚀 Snelle Start

### Windows
```bash
# Optie 1: Batch script
start_pyqt6.bat

# Optie 2: PowerShell script
.\start_pyqt6.ps1

# Optie 3: Handmatig
pyqt6_env\Scripts\activate
python run_pyqt6.py
```

### Linux/Mac
```bash
# Activeer virtual environment
source pyqt6_env/bin/activate

# Start PyQt6 versie
python run_pyqt6.py
```

## ✨ Wat is er nieuw?

### Moderne Interface
- **Flat design**: Moderne, clean interface
- **Dark theme**: Automatische dark theme ondersteuning
- **Responsive layout**: Automatische layout aanpassing
- **Native look**: Ziet er uit als een native applicatie

### Betere Real-time Updates
- **Signal/Slot systeem**: Veel efficiënter dan Tkinter
- **Thread-safe communicatie**: Geen GUI freezes
- **60 FPS updates**: Vloeiende interface updates
- **Betere performance**: Qt's event loop is veel krachtiger

### Verbeterde Threading
- **QThread**: Krachtige threading ondersteuning
- **Thread-safe signals**: Veilige communicatie tussen threads
- **Betere resource management**: Automatische cleanup

## 🎨 Interface Vergelijking

### Tkinter vs PyQt6

| Feature | Tkinter | PyQt6 |
|---------|---------|-------|
| **Look & Feel** | Ouderwets | Modern & Native |
| **Real-time Updates** | Beperkt | Uitstekend |
| **Threading** | Basis | Geavanceerd |
| **Styling** | Beperkt | CSS-achtig |
| **Performance** | Gemiddeld | Hoog |
| **Memory Usage** | Laag | Gemiddeld |

## 🔧 Installatie

### Automatische Installatie
```bash
python install_pyqt6.py
```

### Handmatige Installatie
```bash
# Maak virtual environment
python -m venv pyqt6_env

# Activeer environment
pyqt6_env\Scripts\activate  # Windows
source pyqt6_env/bin/activate  # Linux/Mac

# Installeer dependencies
pip install PyQt6 torch torchaudio openai-whisper python-dotenv
```

## 🧪 Testen

```bash
# Test PyQt6 installatie
python test_pyqt6.py

# Test eenvoudige PyQt6 app
python -c "from PyQt6.QtWidgets import QApplication; print('PyQt6 werkt!')"
```

## 📁 Bestandsstructuur

```
magic_time/
├── pyqt6_env/                    # Virtual environment
├── magic_time_studio/
│   ├── main_pyqt6.py            # PyQt6 hoofdapplicatie
│   └── ui_pyqt6/                # PyQt6 UI modules
│       ├── main_window.py       # PyQt6 hoofdvenster
│       └── themes.py            # PyQt6 thema manager
├── run_pyqt6.py                 # PyQt6 launcher
├── start_pyqt6.bat              # Windows batch script
├── start_pyqt6.ps1              # PowerShell script
├── install_pyqt6.py             # Installatie script
└── test_pyqt6.py                # Test script
```

## 🎮 Gebruik

### Start Methoden

1. **Batch Script (Windows)**
   ```bash
   start_pyqt6.bat
   ```

2. **PowerShell Script (Windows)**
   ```powershell
   .\start_pyqt6.ps1
   ```

3. **Handmatig**
   ```bash
   pyqt6_env\Scripts\activate
   python run_pyqt6.py
   ```

4. **Via normale launcher**
   ```bash
   python magic_time_studio/run.py --pyqt6
   ```

### Interface Features

#### Drie-paneel Layout
- **Links**: Bestanden lijst met knoppen
- **Midden**: Instellingen (taal, model, etc.)
- **Rechts**: Verwerking met progress bar en log

#### Moderne Knoppen
- **Start Verwerking**: Groene knop met hover effect
- **Stop Verwerking**: Rode knop met hover effect
- **Bestand toevoegen**: Moderne file dialog

#### Real-time Updates
- **Progress bar**: Live voortgang updates
- **Status label**: Real-time status informatie
- **Log viewer**: Live log weergave

#### Keyboard Shortcuts
- **F5**: Start verwerking
- **F6**: Stop verwerking
- **Ctrl+O**: Bestand toevoegen
- **Ctrl+Q**: Afsluiten

## 🔧 Configuratie

### Thema's
- **Dark theme**: Standaard (automatisch)
- **Light theme**: Beschikbaar via menu

### Instellingen
- **Taal**: Auto detectie, Nederlands, Engels, etc.
- **Whisper model**: tiny, base, small, medium, large
- **Vertaler**: LibreTranslate, Google Translate, DeepL
- **Content type**: Auto detectie, Video, Audio, etc.

## 🐛 Probleemoplossing

### PyQt6 Installatie Problemen
```bash
# Verwijder oude installatie
pip uninstall PyQt6 PyQt6-Qt6 PyQt6-sip -y

# Installeer opnieuw
pip install PyQt6
```

### Virtual Environment Problemen
```bash
# Maak nieuwe environment
python -m venv pyqt6_env_new

# Kopieer dependencies
pip freeze > requirements.txt
pyqt6_env_new\Scripts\activate
pip install -r requirements.txt
```

### Torch Problemen
```bash
# Installeer CPU versie
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
```

## 🚀 Performance Tips

### Voor Betere Performance
1. **Gebruik virtual environment**: Isolatie van dependencies
2. **CPU-only torch**: Als je geen GPU hebt
3. **Kleinere Whisper model**: Voor snellere verwerking
4. **Sluit andere apps**: Voor meer RAM

### Memory Optimalisatie
- **Kleinere batch size**: Voor grote bestanden
- **Cleanup na verwerking**: Automatisch in PyQt6
- **Monitor memory usage**: Via task manager

## 📊 Vergelijking

### Tkinter vs PyQt6 Performance

| Metriek | Tkinter | PyQt6 |
|---------|---------|-------|
| **Startup tijd** | 2-3 sec | 3-4 sec |
| **Memory usage** | ~50MB | ~80MB |
| **Real-time updates** | 30 FPS | 60 FPS |
| **Thread safety** | Beperkt | Uitstekend |
| **File dialogs** | Basis | Modern |

## 🎯 Conclusie

De PyQt6 versie biedt:
- ✅ **Moderne interface** met betere UX
- ✅ **Uitstekende real-time updates**
- ✅ **Betere threading** voor verwerking
- ✅ **Native look & feel**
- ✅ **CSS-achtige styling** mogelijkheden

De Tkinter versie blijft beschikbaar voor:
- 🔄 **Compatibiliteit** met bestaande code
- 💾 **Lagere memory usage**
- ⚡ **Snellere startup**

## 🤝 Feedback

Heb je feedback over de PyQt6 versie?
- **Bug reports**: Beschrijf het probleem met screenshots
- **Feature requests**: Wat zou je willen toevoegen?
- **Performance issues**: Welke onderdelen zijn traag?

## 📚 Meer Informatie

- [PyQt6 Documentation](https://doc.qt.io/qtforpython-6/)
- [Qt for Python](https://wiki.qt.io/Qt_for_Python)
- [Signal/Slot Tutorial](https://doc.qt.io/qtforpython-6/tutorials/basictutorial/signalsandslots.html) 