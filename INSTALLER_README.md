# Magic Time Studio Installer

## 📋 Vereisten

Om de installer te maken heb je het volgende nodig:

1. **Inno Setup Compiler** - Download van: https://jrsoftware.org/isdl.php
2. **Magic Time Studio executable** - Gebouwd met PyInstaller
3. **Alle benodigde bestanden** - Assets, documentatie, etc.

## 🚀 Installer Maken

### Stap 1: Download Inno Setup
1. Ga naar https://jrsoftware.org/isdl.php
2. Download de laatste versie van Inno Setup Compiler
3. Installeer Inno Setup op je systeem

### Stap 2: Bereid bestanden voor
Zorg ervoor dat je de volgende bestanden hebt:
- `dist/Magic_Time_Studio/` - De gebouwde executable en alle bestanden
- `assets/` - Iconen en andere assets
- `docs/` - Documentatie (optioneel)
- `LICENSE.txt` - Licentie bestand

### Stap 3: Compileer de installer
1. Open Inno Setup Compiler
2. Open het bestand `installer_setup.iss`
3. Klik op "Compile" (groene play knop)
4. De installer wordt gemaakt in `installer_output/`

## 📁 Bestandsstructuur

```
project/
├── dist/
│   └── Magic_Time_Studio/
│       ├── Magic_Time_Studio.exe
│       └── _internal/
├── assets/
│   ├── Magic_Time_Studio.ico
│   ├── Magic_Time_Studio_wit.ico
│   └── ffmpeg.exe
├── docs/
├── installer_setup.iss
├── LICENSE.txt
└── installer_output/
    └── Magic_Time_Studio_Setup.exe
```

## ⚙️ Installer Configuratie

### Wat de installer doet:

1. **Installeert de applicatie** in `Program Files\Magic Time Studio`
2. **Maakt startmenu items** aan
3. **Optioneel desktop icoon** (gebruiker kan kiezen)
4. **Registreert bestandsextensies** (.mp4, .avi, .mkv, etc.)
5. **Maakt uninstaller** aan
6. **Start de applicatie** na installatie (optioneel)

### Installer opties:

- **Taal**: Nederlands en Engels
- **Architectuur**: Alleen 64-bit
- **Rechten**: Laagste rechten (geen admin nodig)
- **Compressie**: LZMA (kleine bestandsgrootte)
- **Moderne wizard**: Mooie gebruikersinterface

## 🔧 Aanpassingen

### Versie wijzigen:
```ini
AppVersion=1.0.0
```

### Publisher wijzigen:
```ini
AppPublisher=Jouw Bedrijf
AppPublisherURL=https://jouw-website.com
```

### Extra bestanden toevoegen:
```ini
[Files]
Source: "extra_bestanden\*"; DestDir: "{app}\extra"; Flags: ignoreversion recursesubdirs
```

### Extra bestandsextensies registreren:
```ini
[Registry]
Root: HKCU; Subkey: "Software\Classes\.nieuwext"; ValueType: string; ValueName: ""; ValueData: "MagicTimeStudio.Video"; Flags: uninsdeletevalue
```

## 🐛 Troubleshooting

### Probleem: "Source file not found"
- Controleer of alle bestanden bestaan
- Zorg ervoor dat de paden correct zijn
- Gebruik relatieve paden vanaf de project root

### Probleem: "Access denied"
- Zorg ervoor dat Inno Setup als administrator draait
- Controleer of bestanden niet in gebruik zijn

### Probleem: Installer is te groot
- Gebruik `SolidCompression=yes`
- Verwijder onnodige bestanden uit de dist map
- Gebruik `Compression=lzma`

## 📦 Distributie

De installer (`Magic_Time_Studio_Setup.exe`) kan worden gedistribueerd via:

1. **Website download**
2. **Email attachment**
3. **USB stick**
4. **Network share**

## 🔄 Updates

Voor updates:
1. Bouw nieuwe executable met PyInstaller
2. Update versienummer in `installer_setup.iss`
3. Compileer nieuwe installer
4. Distribueer nieuwe installer

## 📞 Support

Voor vragen over de installer:
- Controleer de Inno Setup documentatie
- Bekijk de log bestanden in `%TEMP%`
- Test de installer op een schone VM 