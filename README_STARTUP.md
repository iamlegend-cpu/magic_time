# Magic Time Studio - Start Instructies

## 🚀 Snelle Start

### Optie 1: Batch Bestand (Windows)

```bash
start_magic_time.bat
```

### Optie 2: PowerShell Script

```powershell
.\start_magic_time.ps1
```

### Optie 3: Handmatig

```bash
# Activeer virtual environment
venv\Scripts\activate

# Start applicatie
python Magic_Time_Studio_v1.9.4.py
```

## 🌐 Nieuwe DeepL Functionaliteit

### Vertaler Menu

- **Menu**: "🌐 Vertaler" in de menubalk
- **Opties**:
  - ⚙️ DeepL Configuratie
  - 🔄 Wissel naar Google Translate
  - 🔄 Wissel naar DeepL

### Configuratie

1. Ga naar **🌐 Vertaler → ⚙️ DeepL Configuratie**
2. Voer je **DeepL API key** in
3. Test de API key met **"Test API Key"**
4. Selecteer **DeepL** als standaard vertaler
5. Klik **"Opslaan"**

### Status Display

- **Vertaler status** wordt getoond in het linker paneel
- **Real-time updates** bij wisselen tussen vertalers
- **Waarschuwingen** als DeepL niet geconfigureerd is

## 🔧 Troubleshooting

### ModuleNotFoundError

Als je een `ModuleNotFoundError` krijgt:

1. Zorg dat je de virtual environment activeert
2. Gebruik `venv\Scripts\python.exe` direct
3. Of gebruik de meegeleverde batch/PowerShell scripts

### DeepL API Key

- Gratis te krijgen op: <https://www.deepl.com/pro-api>
- Test altijd je API key voordat je hem gebruikt
- Fallback naar Google Translate als DeepL faalt

## 📋 Vereisten

- Python 3.8+
- Virtual environment met alle dependencies
- DeepL API key (optioneel, voor DeepL vertalingen)

## 🎯 Features

- ✅ Google Translate (standaard)
- ✅ DeepL vertalingen (met API key)
- ✅ Automatische fallback
- ✅ Configuratie opslag
- ✅ Real-time status updates
