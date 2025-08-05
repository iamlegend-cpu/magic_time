# UI Components - Magic Time Studio

Deze directory bevat alle UI componenten voor Magic Time Studio, georganiseerd volgens functie.

## Panel Structuur

### 📁 `files_panel.py`

Bestanden beheer

- `FilesPanel`: Handelt bestanden selectie, drag & drop, en preview af
- Functies: bestanden toevoegen, mappen scannen, bestanden verwijderen
- Features: drag & drop zone, file preview, bestandenlijst

### ⚙️ `processing_panel.py`

Verwerking en progress

- `ProcessingPanel`: Handelt verwerking start/stop en progress tracking af
- Functies: model selectie, taal selectie, progress bar, log output
- Features: start/stop knoppen, real-time progress, status updates

### 📊 `charts_panel.py`

Grafieken en monitoring

- `ChartsPanel`: Handelt real-time grafieken en system monitoring af
- Functies: system monitor, processing progress chart, performance chart
- Features: real-time data visualisatie, performance tracking

### 🔄 `batch_panel.py`

Batch verwerking

- `BatchPanel`: Handelt batch processing en queue management af
- Functies: batch queue manager, job scheduling
- Features: batch job management, queue monitoring

### ✅ `completed_files_panel.py`

Voltooide bestanden

- `CompletedFilesPanel`: Handelt voltooide bestanden tracking af
- Functies: completed files lijst, export functionaliteit, status tracking
- Features: timestamp tracking, file type icons, export naar tekst/CSV

### 🔌 `plugin_panel.py`

Plugin beheer

- `PluginPanel`: Handelt plugin management af
- Functies: plugin loading, plugin configuration
- Features: plugin manager interface

### ⚙️ `settings_panel_wrapper.py`

Settings wrapper

- `SettingsPanelWrapper`: Wrapper voor settings panel
- Functies: settings panel integratie
- Features: settings group box styling

## Centrale Import

### 📄 `panels.py`

Centrale import/export

- Importeert alle panel classes
- Biedt backward compatibility
- Exporteert alle panel classes via `__all__`

## Gebruik

```python
# Import individuele panels
from .components.files_panel import FilesPanel
from .components.processing_panel import ProcessingPanel

# Of import via centrale panels.py
from .components.panels import FilesPanel, ProcessingPanel
```

## Voordelen van deze structuur

1. **Modulariteit**: Elke panel heeft zijn eigen bestand
2. **Onderhoud**: Makkelijker om specifieke functionaliteit te vinden en aan te passen
3. **Herbruikbaarheid**: Panels kunnen onafhankelijk worden gebruikt
4. **Backward Compatibility**: Bestaande imports blijven werken
5. **Schaalbaarheid**: Nieuwe panels kunnen eenvoudig worden toegevoegd

## Toevoegen van nieuwe panels

1. Maak een nieuw bestand: `new_panel.py`
2. Definieer de panel class
3. Voeg import toe aan `panels.py`
4. Voeg toe aan `__all__` in `panels.py`
5. Update `__init__.py` indien nodig
