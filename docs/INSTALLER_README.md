# Magic Time Studio - Inno Setup Installer

Deze directory bevat alle bestanden die nodig zijn om een professionele Inno Setup installer te maken voor Magic Time Studio.

## 📋 Vereisten

### 1. Inno Setup
- Download en installeer Inno Setup van: https://jrsoftware.org/isdl.php
- Versie 6.0 of hoger wordt aanbevolen
- Zorg ervoor dat `iscc.exe` beschikbaar is in je PATH

### 2. Magic Time Studio Executable
- Zorg ervoor dat je eerst de executable hebt gebouwd met PyInstaller
- De `dist\Magic_Time_Studio` directory moet bestaan

## 🚀 Installer Bouwen

### Optie 1: Batch Script (Windows)
```cmd
build_installer.bat
```

### Optie 2: PowerShell Script
```powershell
.\build_installer.ps1
```

### Optie 3: Handmatig
```cmd
iscc Magic_Time_Studio_Setup.iss
```

## 📁 Bestandsstructuur

```
├── Magic_Time_Studio_Setup.iss    # Hoofdinstaller script
├── LICENSE.txt                    # Licentie bestand
├── build_installer.bat           # Batch script voor bouwen
├── build_installer.ps1           # PowerShell script voor bouwen
├── installer/                     # Output directory (wordt aangemaakt)
└── dist/Magic_Time_Studio/       # PyInstaller output (moet bestaan)
```

## ⚙️ Installer Functies

### ✅ Geoptimaliseerde Features
- **LZMA2/Ultra64 compressie** voor kleinere bestandsgrootte
- **Moderne wizard interface** met custom afbeeldingen
- **Taal detectie** (Nederlands/Engels)
- **Component-based installatie** (volledig/minimaal/aangepast)
- **Automatische dependency checks** (.NET Framework, VC++ Redistributable)
- **Registry integratie** voor bestandsextensies (.srt)
- **Start Menu shortcuts** en optionele desktop iconen
- **PATH variabele update** (optioneel)
- **Professionele uninstaller**

### 🔧 Installatie Opties
- **Volledige installatie**: Alle componenten inclusief Whisper modellen
- **Minimale installatie**: Alleen hoofdprogramma
- **Aangepaste installatie**: Kies welke componenten je wilt

### 📱 Extra Features
- **Desktop shortcut** (optioneel)
- **Quick Launch shortcut** (optioneel)
- **Startup shortcut** (optioneel)
- **Bestandsextensie registratie** (.srt bestanden openen met Magic Time Studio)

## 🎯 Optimalisaties

### Compressie
- **LZMA2/Ultra64**: Beste compressie ratio
- **Solid compression**: Kleinere bestandsgrootte
- **Geen disk spanning**: Eén bestand

### Performance
- **Geen admin rechten vereist** (lowest privileges)
- **Geen applicaties sluiten** tijdens installatie
- **Geen herstart vereist**
- **Snelle installatie** door geoptimaliseerde bestanden

### Gebruiksvriendelijkheid
- **Moderne wizard interface**
- **Taal detectie** op basis van systeem instellingen
- **Progress bars** en duidelijke feedback
- **Foutafhandeling** met duidelijke berichten

## 🚨 Dependency Checks

De installer controleert automatisch of de volgende vereisten zijn voldaan:

### .NET Framework
- **Vereist**: .NET Framework 4.5 of hoger
- **Controle**: Registry check
- **Actie**: Waarschuwing als niet beschikbaar

### Visual C++ Redistributable
- **Vereist**: VC++ 2015-2022 Redistributable
- **Controle**: Registry check
- **Actie**: Waarschuwing als niet beschikbaar

## 📦 Output

Na succesvolle build vind je de installer in:
```
installer/Magic_Time_Studio_Setup_v3.0.exe
```

## 🔄 Updates

### Versie Wijzigen
1. Update `MyAppVersion` in `Magic_Time_Studio_Setup.iss`
2. Update `OutputBaseFilename` in `Magic_Time_Studio_Setup.iss`
3. Update `AppId` als je een nieuwe applicatie versie wilt

### Componenten Toevoegen
1. Voeg nieuwe component toe in `[Components]` sectie
2. Voeg bijbehorende bestanden toe in `[Files]` sectie
3. Update installatie logica indien nodig

## 🐛 Troubleshooting

### Veelvoorkomende Problemen

#### "Inno Setup is niet geïnstalleerd"
- Download en installeer Inno Setup
- Zorg ervoor dat `iscc.exe` in PATH staat

#### "Dist directory niet gevonden"
- Bouw eerst de executable: `pyinstaller --clean magic_time_studio.spec`
- Controleer of `dist\Magic_Time_Studio` bestaat

#### "Installer bouw gefaald"
- Controleer of alle bestanden bestaan
- Controleer of je schrijfrechten hebt
- Bekijk de Inno Setup error logs

### Debug Tips
- Voeg `/LOG` toe aan iscc commando voor gedetailleerde logs
- Controleer of alle source paden correct zijn
- Test met een minimale installatie eerst

## 📞 Ondersteuning

Voor vragen of problemen:
- Controleer de Inno Setup documentatie
- Bekijk de error logs
- Test met verschillende configuraties

## 📄 Licentie

Dit installer script is onderdeel van Magic Time Studio en valt onder dezelfde licentie als de hoofdapplicatie.
