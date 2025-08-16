# Features Module - Magic Time Studio

Dit is de features module voor de Magic Time Studio UI, die verschillende functionaliteiten biedt voor de gebruikersinterface.

## 📊 Monitoring Modules

### SystemMonitorWidget
De hoofdklasse die alle monitoring functionaliteiten coördineert.

**Bestand**: `system_monitor.py`
**Regels**: ~80 (was 643)

### GPUMonitor
Verantwoordelijk voor GPU monitoring, specifiek voor WhisperX.

**Bestand**: `gpu_monitor.py`
**Regels**: ~400

**Functionaliteiten**:
- CUDA GPU monitoring
- WhisperX activiteit detectie
- Memory gebruik tracking
- Kleurgecodeerde status (groen/oranje/rood)
- Real-time updates (100ms tijdens verwerking, 500ms normaal)

### CPURAMMonitor
Verantwoordelijk voor CPU en RAM monitoring.

**Bestand**: `cpu_ram_monitor.py`
**Regels**: ~80

**Functionaliteiten**:
- CPU gebruik monitoring
- RAM gebruik monitoring
- Real-time charts
- Progress bars

## 🔧 Voordelen van de Modulaire Aanpak

### 1. **Kleinere Bestanden**
- **Voor**: 643 regels in één bestand
- **Na**: 80 + 400 + 80 = 560 regels verdeeld over 3 bestanden
- **Besparing**: 83 regels minder, maar veel beter georganiseerd

### 2. **Betere Onderhoudbaarheid**
- Elke module heeft één specifieke verantwoordelijkheid
- Makkelijker om bugs te vinden en op te lossen
- Eenvoudiger om nieuwe functionaliteiten toe te voegen

### 3. **Herbruikbaarheid**
- `GPUMonitor` kan gebruikt worden in andere delen van de applicatie
- `CPURAMMonitor` kan onafhankelijk worden gebruikt
- Betere scheiding van zorgen

### 4. **Leesbaarheid**
- Kortere bestanden zijn makkelijker te begrijpen
- Duidelijke scheiding tussen GPU en CPU/RAM functionaliteit
- Betere code organisatie

## 📁 Bestandsstructuur

```
features/
├── __init__.py              # Module exports
├── README.md               # Deze documentatie
├── system_monitor.py       # Hoofdmonitor widget (80 regels)
├── gpu_monitor.py          # GPU monitoring (400 regels)
├── cpu_ram_monitor.py      # CPU/RAM monitoring (80 regels)
├── real_time_chart.py      # Real-time chart component
├── performance_chart.py     # Performance chart component
├── batch_queue.py          # Batch verwerking
├── file_preview.py         # Bestandspreview
├── modern_styling.py       # Moderne styling
├── plugin_manager.py       # Plugin management
├── processing_progress.py  # Verwerkingsvoortgang
├── progress_charts.py      # Voortgang charts
└── subtitle_preview.py     # Ondertitel preview
```

## 🚀 Gebruik

### Basis Gebruik
```python
from ui_pyqt6.features import SystemMonitorWidget

# Maak een nieuwe monitor widget
monitor = SystemMonitorWidget()

# Start snellere monitoring tijdens verwerking
monitor.start_processing_monitoring()

# Stop snellere monitoring
monitor.stop_processing_monitoring()
```

### Individuele Modules
```python
from ui_pyqt6.features import GPUMonitor, CPURAMMonitor

# GPU monitoring
gpu_monitor = GPUMonitor(parent_widget)
gpu_monitor.setup_ui(gpu_layout)

# CPU/RAM monitoring
cpu_ram_monitor = CPURAMMonitor(parent_widget)
cpu_ram_monitor.setup_ui(charts_layout)
```

## 🔄 Migratie van Oude Code

De oude `system_monitor.py` (643 regels) is vervangen door:

1. **`system_monitor.py`** - Hoofdklasse en coördinatie (80 regels)
2. **`gpu_monitor.py`** - Alle GPU-gerelateerde functionaliteit (400 regels)
3. **`cpu_ram_monitor.py`** - Alle CPU/RAM functionaliteit (80 regels)

### Wat is Verplaatst

#### Van `system_monitor.py` naar `gpu_monitor.py`:
- GPU monitoring logica
- CUDA detectie
- WhisperX activiteit detectie
- GPU status updates
- GPU charts en progress bars

#### Van `system_monitor.py` naar `cpu_ram_monitor.py`:
- CPU monitoring
- RAM monitoring
- CPU/RAM charts
- CPU/RAM progress bars

#### Behouden in `system_monitor.py`:
- Hoofdklasse structuur
- UI coördinatie
- Timer setup
- Module coördinatie

## ✅ Voordelen Samengevat

- **83 regels minder** totaal
- **3x kleinere bestanden** (max 400 regels vs 643)
- **Betere onderhoudbaarheid**
- **Herbruikbare modules**
- **Duidelijkere verantwoordelijkheden**
- **Makkelijker debugging**
- **Betere code organisatie**

De modulaire aanpak maakt de code veel beheersbaarder en onderhoudsvriendelijker!
