"""
Real-time chart widget voor Magic Time Studio
Basis chart functionaliteit voor alle monitoring grafieken
"""

import time
from PyQt6.QtWidgets import QWidget, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen, QColor, QFont


class RealTimeChart(QWidget):
    """Basis real-time chart widget"""
    
    def __init__(self, title: str = "Chart", max_points: int = 100, parent=None):
        super().__init__(parent)
        self.title = title
        self.max_points = max_points
        self.data_points = []
        self.colors = {
            'cpu': QColor(76, 175, 80),      # Groen
            'memory': QColor(33, 150, 243),   # Blauw
            'gpu': QColor(156, 39, 176),      # Paars
            'progress': QColor(255, 193, 7),  # Geel
            'error': QColor(244, 67, 54),     # Rood
            'temperature': QColor(255, 87, 34) # Oranje
        }
        self.setup_ui()
    
    def setup_ui(self):
        """Setup de UI"""
        self.setMinimumHeight(150)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Styling
        self.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                border: 1px solid #555555;
                border-radius: 5px;
            }
        """)
    
    def add_data_point(self, value: float, label: str = ""):
        """Voeg datapunt toe"""
        try:
            timestamp = time.time()
            self.data_points.append({
                'value': value,
                'timestamp': timestamp,
                'label': label
            })
            
            # Behoud alleen de laatste max_points
            if len(self.data_points) > self.max_points:
                self.data_points.pop(0)
            
            self.update()
        except Exception as e:
            print(f"⚠️ Fout bij toevoegen datapunt: {e}")
            # Voeg een veilig datapunt toe als fallback
            try:
                self.data_points.append({
                    'value': 0.0,
                    'timestamp': time.time(),
                    'label': 'error'
                })
                if len(self.data_points) > self.max_points:
                    self.data_points.pop(0)
            except:
                pass
    
    def paintEvent(self, event):
        """Teken de grafiek"""
        try:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # Bereken afmetingen
            width = self.width()
            height = self.height()
            margin = 20
            
            # Teken achtergrond
            painter.fillRect(self.rect(), QColor(45, 45, 45))
            
            if not self.data_points:
                # Toon lege staat
                painter.setPen(QColor(150, 150, 150))
                painter.setFont(QFont("Arial", 12))
                painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Geen data")
                return
            
            # Bereken schaal
            values = [p['value'] for p in self.data_points]
            min_val = min(values) if values else 0
            max_val = max(values) if values else 100
            
            if max_val == min_val:
                max_val = min_val + 1
            
            # Teken raster
            self.draw_grid(painter, width, height, margin, min_val, max_val)
            
            # Teken grafieklijn
            self.draw_line(painter, width, height, margin, min_val, max_val)
            
            # Teken titel
            painter.setPen(QColor(255, 255, 255))
            painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            painter.drawText(margin, 15, self.title)
            
            # Teken huidige waarde
            if self.data_points:
                current_value = self.data_points[-1]['value']
                painter.drawText(width - margin - 50, 15, f"{current_value:.1f}%")
        except Exception as e:
            print(f"⚠️ Fout bij tekenen grafiek: {e}")
            # Teken een eenvoudige foutmelding
            try:
                painter = QPainter(self)
                painter.fillRect(self.rect(), QColor(45, 45, 45))
                painter.setPen(QColor(244, 67, 54))  # Rood voor fout
                painter.setFont(QFont("Arial", 10))
                painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Fout bij tekenen grafiek")
            except:
                pass
    
    def draw_grid(self, painter: QPainter, width: int, height: int, margin: int, min_val: float, max_val: float):
        """Teken raster"""
        try:
            painter.setPen(QPen(QColor(80, 80, 80), 1))
            
            # Verticale lijnen
            for i in range(5):
                x = margin + (width - 2 * margin) * i // 4
                painter.drawLine(x, margin, x, height - margin)
            
            # Horizontale lijnen
            for i in range(5):
                y = margin + (height - 2 * margin) * i // 4
                painter.drawLine(margin, y, width - margin, y)
                
                # Waarde labels
                value = max_val - (max_val - min_val) * i / 4
                painter.setPen(QColor(150, 150, 150))
                painter.setFont(QFont("Arial", 8))
                painter.drawText(5, y + 3, f"{value:.0f}")
        except Exception as e:
            print(f"⚠️ Fout bij tekenen raster: {e}")
    
    def draw_line(self, painter: QPainter, width: int, height: int, margin: int, min_val: float, max_val: float):
        """Teken grafieklijn (horizontaal)"""
        try:
            if len(self.data_points) < 2:
                return
            
            # Kies kleur gebaseerd op titel
            if 'cpu' in self.title.lower():
                color = self.colors['cpu']
            elif 'memory' in self.title.lower() or 'ram' in self.title.lower():
                color = self.colors['memory']
            elif 'gpu' in self.title.lower():
                color = self.colors['gpu']
            elif 'progress' in self.title.lower():
                color = self.colors['progress']
            elif 'temp' in self.title.lower():
                color = self.colors['temperature']
            else:
                color = self.colors['cpu']
            
            painter.setPen(QPen(color, 2))
            
            # Teken lijn (horizontaal - tijd op x-as, waarden op y-as)
            points = []
            for i, point in enumerate(self.data_points):
                # X-coördinaat (tijd) - van links naar rechts
                x = margin + (width - 2 * margin) * i / (len(self.data_points) - 1)
                # Y-coördinaat (waarde) - van onder naar boven (omgekeerd voor betere leesbaarheid)
                y = height - margin - (height - 2 * margin) * (point['value'] - min_val) / (max_val - min_val)
                points.append((x, y))
            
            # Teken verbonden lijnen
            for i in range(len(points) - 1):
                painter.drawLine(int(points[i][0]), int(points[i][1]), 
                               int(points[i+1][0]), int(points[i+1][1]))
            
            # Teken datapunten als kleine cirkels voor betere zichtbaarheid
            painter.setBrush(color)
            for point in points:
                painter.drawEllipse(int(point[0]) - 2, int(point[1]) - 2, 4, 4)
        except Exception as e:
            print(f"⚠️ Fout bij tekenen grafieklijn: {e}") 