# Quick Settings Structure - Magic Time Studio

## Overzicht

De GUI van Magic Time Studio heeft nu een duidelijke scheiding tussen **Quick Settings** (essentiële instellingen) en **Geavanceerde Instellingen** (configuratie venster).

## Quick Settings Panel (Hoofd GUI)

Het settings panel in de hoofdinterface bevat alleen de meest essentiële instellingen voor snelle toegang:

### 🌐 Vertaler
- **Vertaler**: LibreTranslate / Geen vertaling
- *Server URL wordt alleen in config window geconfigureerd*

### 🎤 Fast Whisper Instellingen
- **Whisper Type**: Fast Whisper (standaard)
- **Model**: Tiny, Base, Small, Medium, Large, etc.

### 🗣️ Taal
- **Taal**: Engels, Nederlands, Duits, Frans, Spaans, Auto detectie

### 📺 Ondertitels
- **Originele ondertitels**: Behoud / Vervang
- *Content Type (Softcoded/Hardcoded) wordt alleen in config window geconfigureerd*

## Geavanceerde Instellingen (Config Window)

Het configuratie venster (Menu → Instellingen) bevat alle geavanceerde instellingen:

### 🔧 Algemene Instellingen
- Theme (dark/light/blue/green/purple/orange/cyber)
- Font Size (8-16)
- Auto Cleanup
- Auto Output Directory

### 📝 Logging Instellingen
- Log Level (DEBUG/INFO/WARNING/ERROR)
- Log to File

### 🎤 Verwerking Instellingen
- Whisper Type (Fast Whisper/Standaard Whisper)
- Model (tiny/base/small/medium/large/etc)
- Device (cpu/cuda)

### 🌐 Vertaler Instellingen
- **LibreTranslate Server URL** (alleen hier)
- Timeout (5-120 seconds)
- Rate Limit (0-1000)
- Max Characters (1000-50000)

### 👁️ Interface Instellingen
- **Standaard Window Grootte**: Klein, Gemiddeld, Groot, Extra Groot, Automatisch
- Panel Visibility Settings
- Splitter Position Settings

### 🎨 Thema Instellingen
- Theme Preview
- Custom Colors

### 🔧 Geavanceerde Instellingen
- Debug Mode
- Verbose Logging
- System Info
- Cache Size (100-5000 MB)
- Thread Pool Size (2-16)

### 💾 Backup Instellingen
- Auto Backup
- Backup Interval (1-30 days)

### 🔌 Plugin Instellingen
- Plugin Directory
- Load Plugins on Startup
- Auto Scan Plugins

### 📺 Content Type Instellingen
- **Content Type** (Softcoded/Hardcoded) (alleen hier)

## Voordelen van deze structuur

### ✅ Voor gebruikers:
- **Snelle toegang**: Alleen essentiële instellingen direct beschikbaar
- **Geen verwarring**: Geen knoppen in de settings panel
- **Duidelijke scheiding**: Quick settings vs geavanceerde instellingen
- **Schonere interface**: Minder cluttered GUI
- **Eenvoudiger**: Alleen 5 essentiële instellingen in GUI

### ✅ Voor ontwikkelaars:
- **Betere organisatie**: Logische scheiding van instellingen
- **Minder duplicaten**: Van 7 naar 1 dubbele instelling
- **Eenvoudiger onderhoud**: Duidelijke verantwoordelijkheden
- **Betere UX**: Gebruikers weten waar ze wat kunnen vinden

## Dubbele instellingen

Er is nog 1 dubbele instelling tussen Quick Settings en Config Window:
1. **Whisper Type** - Voor snelle selectie en geavanceerde configuratie

Deze duplicaat is bewust behouden omdat het zowel voor snelle toegang als voor geavanceerde configuratie nodig is.

## Verwijderde items uit GUI

De volgende items zijn verwijderd uit de GUI settings panel:
- **LibreTranslate Server URL** - Nu alleen in config window
- **Content Type** - Nu alleen in config window

## Toegang tot geavanceerde instellingen

Gebruikers kunnen toegang krijgen tot geavanceerde instellingen via:
- **Menu → Instellingen → Configuratie**
- **Menu → Configuratie**

## Vergelijking

| Aspect | Quick Settings | Config Window |
|--------|----------------|---------------|
| **Aantal instellingen** | 5 | 28 |
| **Doel** | Snelle toegang | Geavanceerde configuratie |
| **Gebruiksfrequentie** | Dagelijks | Incidenteel |
| **Complexiteit** | Eenvoudig | Geavanceerd |
| **Dubbele instellingen** | 1 | 1 |

## Conclusie

De nieuwe structuur biedt een veel betere gebruikerservaring door:
- Alleen essentiële instellingen direct beschikbaar te maken
- Geavanceerde instellingen netjes georganiseerd in een apart venster
- Geen verwarrende knoppen in de hoofdinterface
- Duidelijke scheiding van verantwoordelijkheden
- Minimalisering van duplicaten (van 7 naar 1)
- Vereenvoudiging van de interface (van 7 naar 5 instellingen)
