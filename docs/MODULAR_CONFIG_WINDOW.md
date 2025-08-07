# Modulaire Config Window - Magic Time Studio

## Overzicht

De config window is succesvol gemodulariseerd van één groot bestand (1,031 regels) naar 8 kleinere, beheersbare bestanden.

## Nieuwe Structuur

```
magic_time_studio/ui_pyqt6/config_window/
├── __init__.py                    # Package exports
├── base_config_window.py          # Hoofd config window (156 regels)
└── tabs/
    ├── __init__.py               # Tabs package
    ├── general_tab.py            # Algemene instellingen (108 regels)
    ├── processing_tab.py         # Verwerking instellingen (292 regels)
    ├── translator_tab.py         # Vertaler instellingen (94 regels)
    ├── interface_tab.py          # Interface instellingen (151 regels)
    ├── theme_tab.py             # Thema instellingen (155 regels)
    ├── advanced_tab.py          # Geavanceerde instellingen (122 regels)
    └── plugins_tab.py           # Plugin beheer (180 regels)
```

## Bestandsgrootte Vergelijking

### ❌ Oude structuur:
- **1 bestand**: `config_window.py` (1,031 regels, 43.3 KB)
- **Problemen**: Te groot, moeilijk te onderhouden, complex

### ✅ Nieuwe structuur:
- **8 bestanden**: Totaal 1,258 regels verdeeld
- **Gemiddeld**: 157 regels per bestand
- **Voordelen**: Beheersbaar, modulair, testbaar

## Tab Verantwoordelijkheden

### 🔧 **GeneralTab** (108 regels)
- Algemene instellingen (thema, font grootte)
- Logging instellingen
- Auto cleanup en output directory

### ⚙️ **ProcessingTab** (292 regels)
- Whisper instellingen (type, model, device)
- **Gebruiksvriendelijke memory limit opties** (2GB-16GB)
- Systeem limieten (CPU, memory)
- Subtitle instellingen

### 🌐 **TranslatorTab** (94 regels)
- LibreTranslate server instellingen
- Timeout en rate limit configuratie
- Max characters instellingen

### 👁️ **InterfaceTab** (151 regels)
- Panel zichtbaarheid instellingen
- **Gebruiksvriendelijke window grootte opties** (Klein-Groot-Automatisch)
- Splitter posities

### 🎨 **ThemeTab** (155 regels)
- Thema preview en selectie
- Thema beschrijvingen
- Aangepaste kleuren instellingen

### 🔧 **AdvancedTab** (122 regels)
- Debug instellingen
- Performance instellingen (cache, thread pool)
- Backup instellingen

### 🔌 **PluginsTab** (180 regels)
- Plugin directory instellingen
- Plugin lijst en beheer
- Plugin informatie en status

## Gebruiksvriendelijke Instellingen

### Memory Limit Opties:
```
2 GB (2048 MB)     - Voor kleine systemen
4 GB (4096 MB)     - Voor gemiddelde systemen  
6 GB (6144 MB)     - Voor grotere systemen
8 GB (8192 MB)     - Voor de meeste gebruikers
12 GB (12288 MB)   - Voor gaming/workstation
16 GB (16384 MB)   - Voor high-end systemen
Automatisch         - Past zich aan aan systeem
```

### Window Grootte Opties:
```
Klein (800×600)           - Voor kleine schermen
Gemiddeld (1200×800)      - Voor de meeste gebruikers
Groot (1600×900)          - Voor grote schermen
Extra Groot (1920×1080)   - Voor Full HD schermen
Automatisch               - Past zich aan aan scherm
```

## Voordelen van Modularisatie

### ✅ **Beheersbaarheid**
- Kleinere bestanden (gemiddeld 157 regels)
- Duidelijke verantwoordelijkheden per tab
- Makkelijker te vinden en aanpassen

### ✅ **Onderhoud**
- Geïsoleerde wijzigingen per tab
- Betere code organisatie
- Snellere debugging

### ✅ **Testbaarheid**
- Individuele tab tests mogelijk
- Betere unit test coverage
- Geïsoleerde functionaliteit

### ✅ **Ontwikkeling**
- Parallel development mogelijk
- Minder merge conflicts
- Snellere feature development

### ✅ **Leesbaarheid**
- Duidelijke structuur
- Logische groepering
- Betere documentatie

## Technische Details

### Import Structuur:
```python
from magic_time_studio.ui_pyqt6.config_window import ConfigWindow
```

### Tab Interface:
Elke tab implementeert:
- `setup_ui()` - UI opbouw
- `load_configuration()` - Config laden
- `save_configuration()` - Config opslaan

### Config Manager Integratie:
Alle tabs gebruiken dezelfde `config_manager` voor consistente configuratie opslag.

## Conclusie

De modulaire config window structuur biedt:
- **Betere beheersbaarheid** - Kleinere, gefocuste bestanden
- **Behouden functionaliteit** - Alle features blijven werken
- **Gebruiksvriendelijke instellingen** - Memory en window grootte opties
- **Toekomstbestendigheid** - Makkelijker uitbreidbaar
- **Betere developer experience** - Duidelijke structuur en verantwoordelijkheden

De modularisatie maakt Magic Time Studio veel onderhoudsvriendelijker en uitbreidbaarder.
