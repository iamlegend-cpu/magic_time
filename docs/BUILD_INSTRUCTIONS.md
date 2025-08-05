# Magic Time Studio - Exe Build Instructies

## Overzicht

Dit document beschrijft hoe je de Magic Time Studio applicatie kunt bouwen tot een standalone exe met ffmpeg correct meegenomen.

## Vereisten

1. **Python 3.8+** geïnstalleerd
2. **PyInstaller** geïnstalleerd: `pip install pyinstaller`
3. **FFmpeg** aanwezig in de `assets/` map als `ffmpeg.exe`

## FFmpeg Setup

Zorg ervoor dat `ffmpeg.exe` aanwezig is in de `assets/` map:

```
magic_time/
├── assets/
│   ├── ffmpeg.exe          # ← Moet hier staan
│   ├── Magic_Time_Studio.ico
│   └── ...
```

## Build Stappen

### Methode 1: Automatisch Build Script

```bash
python build_exe.py
```

Dit script:
1. Controleert of ffmpeg aanwezig is
2. Bouwt de exe met PyInstaller
3. Test of ffmpeg correct is meegenomen

### Methode 2: Handmatig

```bash
# 1. Controleer ffmpeg
ls assets/ffmpeg.exe

# 2. Bouw exe
pyinstaller --clean --noconfirm magic_time_studio.spec

# 3. Test resultaat
ls dist/Magic_Time_Studio/ffmpeg.exe
```

## Configuratie

### Spec File

De `magic_time_studio.spec` file is geconfigureerd om:

- FFmpeg als binary mee te nemen: `('assets/ffmpeg.exe', '.')`
- Assets (ico's, png's) mee te nemen
- Whisper assets mee te nemen
- Alle benodigde Python modules te bundelen

### Hooks

De `hooks/` map bevat custom hooks voor:

- `hook_ffmpeg.py` - Zorgt ervoor dat ffmpeg correct wordt meegenomen
- `hook_torch_*.py` - Fixes voor PyTorch bundling
- `hook-librosa.py` - Librosa bundling

## Troubleshooting

### FFmpeg niet gevonden

Als ffmpeg niet wordt gevonden in de gebouwde exe:

1. Controleer of `assets/ffmpeg.exe` bestaat
2. Controleer of de spec file correct is geconfigureerd
3. Test met `python test_ffmpeg_bundle.py`

### Build Errors

Veelvoorkomende problemen:

1. **PyInstaller niet geïnstalleerd**: `pip install pyinstaller`
2. **Ontbrekende dependencies**: Controleer `requirements.txt`
3. **FFmpeg niet aanwezig**: Download ffmpeg en plaats in `assets/`

### Runtime Errors

Als de exe wel bouwt maar niet werkt:

1. Test de exe in de console om error messages te zien
2. Controleer of alle assets correct zijn meegenomen
3. Test ffmpeg functionaliteit met een test video

## Testen

### Test FFmpeg Functionaliteit

```bash
# Test ffmpeg in development
python test_ffmpeg_bundle.py

# Test ffmpeg in gebouwde exe
cd dist/Magic_Time_Studio
./Magic_Time_Studio.exe
```

### Test Video Verwerking

1. Plaats een test video in de exe directory
2. Start de applicatie
3. Test video verwerking functionaliteit

## Output

Na succesvolle build vind je de exe in:

```
dist/
└── Magic_Time_Studio/
    ├── Magic_Time_Studio.exe
    ├── ffmpeg.exe              # ← FFmpeg moet hier staan
    ├── assets/
    └── ...
```

## Distributie

Voor distributie:

1. Test de exe op een schone machine
2. Zorg ervoor dat alle dependencies correct zijn meegenomen
3. Test video verwerking functionaliteit
4. Package de hele `dist/Magic_Time_Studio/` map

## Notities

- FFmpeg wordt nu als binary meegenomen in plaats van als data file
- De applicatie zoekt ffmpeg eerst in de bundle directory
- Fallback naar PATH en andere locaties is nog steeds beschikbaar
- Console output is ingeschakeld voor debugging 