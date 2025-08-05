# Magic Time Studio - PyQt6 Migratie

## 🚀 Overstap naar PyQt6

Deze migratie brengt Magic Time Studio naar PyQt6 voor een moderne, fraaiere interface met betere real-time updates.

## ✨ Voordelen van PyQt6

### Real-time Updates
- **Signal/Slot systeem**: Veel efficiënter dan Tkinter's `after()` calls
- **Thread-safe communicatie**: Automatische event handling tussen threads
- **Betere performance**: Qt's event loop is veel krachtiger
- **Moderne async support**: Betere ondersteuning voor asynchrone operaties

### Moderne Interface
- **Flat design**: Moderne, clean interface
- **Betere styling**: CSS-achtige styling mogelijkheden
- **Responsive layout**: Automatische layout aanpassing
- **Native look**: Ziet er uit als een native applicatie

### Threading
- **QThread**: Krachtige threading ondersteuning
- **Thread-safe signals**: Veilige communicatie tussen threads
- **Betere resource management**: Automatische cleanup

## 📦 Installatie

### 1. Installeer PyQt6
```bash
python install_pyqt6.py
```

### 2. Test de installatie
```bash
python -c "from PyQt6.QtWidgets import QApplication; print('PyQt6 werkt!')"
```

## 🎮 Gebruik

### Start de PyQt6 versie
```bash
python run_pyqt6.py
```

### Of via de normale launcher
```bash
python magic_time_studio/run.py --pyqt6
```

## 🏗️ Architectuur

### Nieuwe Bestanden
- `magic_time_studio/main_pyqt6.py` - PyQt6 hoofdapplicatie
- `magic_time_studio/ui_pyqt6/` - PyQt6 UI modules
- `run_pyqt6.py` - Launcher voor PyQt6 versie
- `install_pyqt6.py` - Installatie script

### Belangrijke Klassen
- `MagicTimeStudioPyQt6` - Hoofdapplicatie klasse
- `MainWindow` - PyQt6 hoofdvenster
- `ProcessingThread` - Thread voor verwerking
- `ThemeManager` - Thema management

## 🔄 Migratie van Tkinter naar PyQt6

### Threading
```python
# Oud (Tkinter)
import threading
def update_gui():
    root.after(100, update_gui)

# Nieuw (PyQt6)
from PyQt6.QtCore import QThread, pyqtSignal
class ProcessingThread(QThread):
    progress_updated = pyqtSignal(float, str)
    def run(self):
        self.progress_updated.emit(0.5, "Verwerken...")
```

### Real-time Updates
```python
# Oud (Tkinter)
def update_progress():
    progress_bar['value'] = value
    root.after(100, update_progress)

# Nieuw (PyQt6)
def update_progress(self, value: float, status: str):
    self.progress_bar.setValue(int(value))
    self.status_label.setText(status)
```

### Signal/Slot Systeem
```python
# Verbind signals
self.processing_thread.progress_updated.connect(self.update_progress)
self.processing_thread.status_updated.connect(self.update_status)

# Emit signals
self.processing_started.emit(files, settings)
```

## 🎨 Theming

### Dark Theme
```python
# Automatische dark theme ondersteuning
palette.setColor(QPalette.ColorRole.Window, QColor("#2b2b2b"))
palette.setColor(QPalette.ColorRole.WindowText, QColor("#ffffff"))
```

### Custom Styling
```python
# CSS-achtige styling
button.setStyleSheet("""
    QPushButton {
        background-color: #4caf50;
        color: white;
        border: none;
        padding: 10px;
        font-weight: bold;
        border-radius: 5px;
    }
""")
```

## 🔧 Configuratie

### Bestaande Configuratie
- Alle bestaande configuratie wordt automatisch geladen
- Thema instellingen worden bewaard
- Processing instellingen blijven hetzelfde

### Nieuwe Instellingen
- PyQt6-specifieke instellingen kunnen worden toegevoegd
- Betere thema ondersteuning
- Verbeterde layout opties

## 🚀 Performance Verbeteringen

### Real-time Updates
- **60 FPS updates**: Vloeiende interface updates
- **Thread-safe**: Geen GUI freezes tijdens verwerking
- **Memory efficient**: Betere resource management

### Verwerking
- **Parallel processing**: Betere multi-threading
- **Progress tracking**: Real-time voortgang updates
- **Status updates**: Live status informatie

## 🐛 Bekende Problemen

### Installatie
- PyQt6 is een grote library (~50MB)
- Mogelijk conflicten met bestaande Qt installaties
- Windows: Mogelijk extra Visual C++ redistributables nodig

### Compatibiliteit
- Niet alle Tkinter widgets hebben directe PyQt6 equivalenten
- Sommige custom widgets moeten worden herschreven
- File dialogs werken iets anders

## 🔮 Toekomstige Verbeteringen

### Geplande Features
- [ ] Geavanceerde thema editor
- [ ] Custom widgets voor specifieke use cases
- [ ] Betere drag & drop ondersteuning
- [ ] Keyboard shortcuts configuratie
- [ ] Plugin systeem

### Performance Optimalisaties
- [ ] Lazy loading van UI componenten
- [ ] Betere memory management
- [ ] GPU acceleratie voor rendering
- [ ] Async file operations

## 📚 Documentatie

### PyQt6 Resources
- [PyQt6 Documentation](https://doc.qt.io/qtforpython-6/)
- [Qt for Python](https://wiki.qt.io/Qt_for_Python)
- [PyQt6 Examples](https://github.com/PyQt6/PyQt6/tree/master/examples)

### Migratie Gids
- [Tkinter naar PyQt6](https://doc.qt.io/qtforpython-6/tutorials/index.html)
- [Signal/Slot Tutorial](https://doc.qt.io/qtforpython-6/tutorials/basictutorial/signalsandslots.html)

## 🤝 Bijdragen

### Bug Reports
- Gebruik GitHub Issues voor bug reports
- Voeg screenshots toe voor UI problemen
- Beschrijf stappen om het probleem te reproduceren

### Feature Requests
- Beschrijf de gewenste functionaliteit
- Voeg use cases toe
- Overweeg implementatie complexiteit

## 📄 Licentie

Deze migratie volgt dezelfde licentie als het originele project. 