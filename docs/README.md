# Magic Time Studio

Een geavanceerde video ondertiteling applicatie gebouwd met PyQt6.

## 📁 Project Structuur

magic_time/
├── 📁 magic_time_studio/          # Hoofdapplicatie
│   ├── 📁 core/                   # Kern functionaliteit
│   ├── 📁 models/                 # Data modellen
│   ├── 📁 processing/             # Verwerking modules
│   ├── 📁 ui_pyqt6/              # PyQt6 gebruikersinterface
│   ├── 📁 docs/                   # Documentatie
│   ├── main_pyqt6.py             # Hoofdapplicatie entry point
│   ├── run.py                     # Start script
│   └── startup.py                 # Initialisatie script
├── 📁 tools/                      # Hulpmiddelen en build tools
│   ├── 📁 bin/                    # Binaire bestanden (ffmpeg.exe)
│   ├── 📁 build/                  # Build bestanden
│   ├── 📁 dist/                   # Distributie bestanden
│   ├── 📁 hooks/                  # PyInstaller hooks
│   └── config.json                # Configuratie bestanden
├── 📁 scripts/                    # Scripts en utilities
│   ├── start_pyqt6.bat           # Windows start script
│   ├── start_pyqt6.ps1           # PowerShell start script
│   ├── install_pyqt6.py          # PyQt6 installatie script
│   └── build_exe.py              # Executable build script
├── 📁 docs/                       # Project documentatie
│   ├── README.md                  # Project overzicht
│   ├── BUILD_INSTRUCTIONS.md      # Build instructies
│   ├── PYQT6_MIGRATION.md         # PyQt6 migratie
│   └── PYQT6_README.md           # PyQt6 documentatie
├── 📁 tests/                      # Test bestanden
│   ├── test_pyqt6.py             # PyQt6 tests
│   ├── test_exe_ffmpeg.py        # FFmpeg tests
│   └── test_ffmpeg_bundle.py     # Bundle tests
├── 📁 assets/                     # Media bestanden
│   └── *.ico, .png              # Iconen en afbeeldingen
├── 📁 pyqt6_env/                 # Python virtual environment
└── .gitignore                     # Git ignore bestanden

## 🚀 Snel Starten

### Vereisten

- Python 3.8+
- PyQt6
- FFmpeg

### Installatie

```bash
# Clone het project
git clone <repository-url>
cd magic_time

# Activeer virtual environment
pyqt6_env\Scripts\activate

# Start de applicatie
python magic_time_studio\run.py
```

### Of gebruik de start scripts

```bash
# Windows
scripts\start_pyqt6.bat

# PowerShell
scripts\start_pyqt6.ps1
```

## 🔧 Build Executable

```bash
# Installeer PyInstaller
pip install pyinstaller

# Build executable
python scripts\build_exe.py
```

## 📚 Documentatie

- `docs/README.md` - Project overzicht
- `docs/BUILD_INSTRUCTIONS.md` - Build instructies
- `docs/PYQT6_MIGRATION.md` - PyQt6 migratie details
- `docs/PYQT6_README.md` - PyQt6 specifieke documentatie

## 🧪 Tests

```bash
# Voer tests uit
python tests\test_pyqt6.py
python tests\test_exe_ffmpeg.py
```

## 🛠️ Ontwikkeling

### Project Structuur

- **core/**: Kern functionaliteit (config, logging, utils)
- **models/**: Data modellen (performance tracker, processing queue)
- **processing/**: Verwerking modules (whisper, translator, audio/video)
- **ui_pyqt6/**: PyQt6 gebruikersinterface
  - **components/**: UI componenten (panels, menu manager)
  - **features/**: Geavanceerde features (drag & drop, charts, plugins)

### Belangrijke Bestanden

- `magic_time_studio/main_pyqt6.py` - Hoofdapplicatie
- `magic_time_studio/run.py` - Start script
- `magic_time_studio/ui_pyqt6/main_window.py` - Hoofdvenster
- `magic_time_studio/ui_pyqt6/config_window.py` - Configuratie venster

## 📦 Distributie

De applicatie kan worden gebouwd als standalone executable met:

- FFmpeg gebundeld
- PyQt6 runtime
- Whisper modellen
- Alle dependencies

## 🤝 Bijdragen

1. Fork het project
2. Maak een feature branch
3. Commit je wijzigingen
4. Push naar de branch
5. Open een Pull Request

## 📄 Licentie

Dit project is gelicenseerd onder de MIT License.
