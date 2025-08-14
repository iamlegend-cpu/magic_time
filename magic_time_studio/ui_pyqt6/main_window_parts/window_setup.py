"""
Window Setup Mixin voor MainWindow
Bevat alle window setup en configuratie functies
"""

import os
import time
import requests
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QStatusBar, QProgressBar, QGroupBox, QFormLayout
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIcon
# Lazy import van config_manager om circulaire import te voorkomen
def _get_config_manager():
    """Lazy config manager import om circulaire import te voorkomen"""
    try:
        from ...core.config import config_manager
        return config_manager
    except ImportError:
        try:
            from magic_time_studio.core.config import config_manager
            return config_manager
        except ImportError:
            return None

class WindowSetupMixin:
    """Mixin voor window setup functionaliteit"""
    
    def setup_window(self):
        """Setup het hoofdvenster"""
        self.setWindowTitle("Magic Time Studio v3.0 - PyQt6")
        
        # Stel minimum grootte in
        self.setMinimumSize(1200, 800)
        
        # Probeer window state te herstellen, anders gebruik standaard
        try:
            self.restore_window_state()
        except Exception as e:
            print(f"⚠️ Kon window state niet herstellen: {e}")
            # Fallback naar standaard setup
            screen = QApplication.primaryScreen()
            screen_geometry = screen.availableGeometry()
            
            # Bereken optimale window grootte (80% van scherm)
            window_width = int(screen_geometry.width() * 0.8)
            window_height = int(screen_geometry.height() * 0.8)
            
            # Centreer window op scherm
            x = (screen_geometry.width() - window_width) // 2
            y = (screen_geometry.height() - window_height) // 2
            
            # Stel window geometrie in
            self.setGeometry(x, y, window_width, window_height)
            self.showMaximized()
        
        # Zorg ervoor dat window zichtbaar is
        self.raise_()
        self.activateWindow()
        
        # Stel taakbalk icoon in na het tonen van het venster
        QTimer.singleShot(100, self.setTaskbarIcon)
        
        # Stel icoon in voor venster
        try:
            # Bepaal project root
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            
            # Probeer verschillende icoon paden
            icon_paths = [
                os.path.join(os.path.dirname(__file__), "..", "..", "..", "assets", "Magic_Time_Studio.ico"),
                os.path.join(os.path.dirname(__file__), "..", "..", "..", "assets", "Magic_Time_Studio_wit.ico"),
                os.path.join(project_root, "assets", "Magic_Time_Studio.ico"),
                os.path.join(project_root, "assets", "Magic_Time_Studio_wit.ico"),
                os.path.join(os.getcwd(), "assets", "Magic_Time_Studio.ico"),
                os.path.join(os.getcwd(), "assets", "Magic_Time_Studio_wit.ico"),
            ]
            
            icon_set = False
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    self.setWindowIcon(QIcon(icon_path))
                    print(f"✅ Venster icoon ingesteld: {icon_path}")
                    icon_set = True
                    break
            
            if not icon_set:
                print("⚠️ Geen icoon bestand gevonden voor venster")
            
            # Stel ook taakbalk icoon in
            self.setTaskbarIcon()
                
        except Exception as e:
            print(f"❌ Fout bij instellen venster icoon: {e}")
    
    def setTaskbarIcon(self):
        """Stel taakbalk icoon in"""
        try:
            # Bepaal project root
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            
            # Probeer verschillende icoon paden voor taakbalk
            icon_paths = [
                os.path.join(project_root, "assets", "Magic_Time_Studio_wit.ico"),
                os.path.join(project_root, "assets", "Magic_Time_Studio.ico"),
                os.path.join(os.path.dirname(__file__), "..", "..", "..", "assets", "Magic_Time_Studio_wit.ico"),
                os.path.join(os.path.dirname(__file__), "..", "..", "..", "assets", "Magic_Time_Studio.ico"),
                os.path.join(os.getcwd(), "assets", "Magic_Time_Studio_wit.ico"),
                os.path.join(os.getcwd(), "assets", "Magic_Time_Studio.ico"),
            ]
            
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    # Stel icoon in voor het venster (dit beïnvloedt de taakbalk)
                    self.setWindowIcon(QIcon(icon_path))
                    print(f"✅ Taakbalk icoon ingesteld: {icon_path}")
                    return
            
            print("⚠️ Geen icoon bestand gevonden voor taakbalk")
            
        except Exception as e:
            print(f"❌ Fout bij instellen taakbalk icoon: {e}")
    
    def create_status_bar(self):
        """Maak de statusbalk met voortgangsbalk"""
        from PyQt6.QtWidgets import QProgressBar, QLabel, QHBoxLayout, QWidget
        from PyQt6.QtCore import Qt
        
        # Maak statusbalk
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Maak widget voor voortgangsbalk en status
        status_widget = QWidget()
        status_layout = QHBoxLayout(status_widget)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setSpacing(10)
        
        # Status label - UITGESCHAKELD om overbodige updates te voorkomen
        self.status_label = QLabel("")  # Lege tekst
        self.status_label.setVisible(False)  # Volledig onzichtbaar
        self.status_label.setMinimumWidth(200)
        status_layout.addWidget(self.status_label)
        
        # Voeg spacer toe tussen status en GPU info
        status_layout.addStretch()
        
        # GPU Status label (rechts onderin)
        self.gpu_status_label = QLabel("GPU: --")
        self.gpu_status_label.setMinimumWidth(120)
        self.gpu_status_label.setStyleSheet("""
            QLabel {
                color: #888888;
                font-size: 9px;
                padding: 2px 4px;
                background-color: #1a1a1a;
                border-radius: 2px;
                border: 1px solid #333333;
            }
        """)
        self.gpu_status_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        status_layout.addWidget(self.gpu_status_label)
        
        # GPU Memory label (rechts onderin)
        self.gpu_memory_label = QLabel("Memory: --")
        self.gpu_memory_label.setMinimumWidth(120)
        self.gpu_memory_label.setStyleSheet("""
            QLabel {
                color: #888888;
                font-size: 9px;
                padding: 2px 4px;
                background-color: #1a1a1a;
                border-radius: 2px;
                border: 1px solid #333333;
            }
        """)
        self.gpu_memory_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        status_layout.addWidget(self.gpu_memory_label)
        
        # FFmpeg Status label
        self.ffmpeg_status_label = QLabel("🔴 FFmpeg: Niet actief")
        self.ffmpeg_status_label.setMinimumWidth(120)
        self.ffmpeg_status_label.setStyleSheet("""
            QLabel {
                color: #F44336;
                font-size: 9px;
                padding: 2px 4px;
                background-color: #B71C1C;
                border-radius: 2px;
                border: 1px solid #F44336;
                font-weight: bold;
            }
        """)
        self.ffmpeg_status_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        status_layout.addWidget(self.ffmpeg_status_label)
        
        # FFmpeg Info label
        self.ffmpeg_info_label = QLabel("Geen actieve processen")
        self.ffmpeg_info_label.setMinimumWidth(120)
        self.ffmpeg_info_label.setStyleSheet("""
            QLabel {
                color: #888888;
                font-size: 9px;
                padding: 2px 4px;
                background-color: #1a1a1a;
                border-radius: 2px;
                border: 1px solid #333333;
            }
        """)
        self.ffmpeg_info_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        status_layout.addWidget(self.ffmpeg_info_label)
        
        # LibreTranslate Status label
        self.libretranslate_status_label = QLabel("🔴 LibreTranslate: Niet bereikbaar")
        self.libretranslate_status_label.setMinimumWidth(120)
        self.libretranslate_status_label.setStyleSheet("""
            QLabel {
                color: #F44336;
                font-size: 9px;
                padding: 2px 4px;
                background-color: #B71C1C;
                border-radius: 2px;
                border: 1px solid #F44336;
                font-weight: bold;
            }
        """)
        self.libretranslate_status_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        status_layout.addWidget(self.libretranslate_status_label)
        
        # LibreTranslate Info label
        self.libretranslate_info_label = QLabel("Server niet bereikbaar")
        self.libretranslate_info_label.setMinimumWidth(120)
        self.libretranslate_info_label.setStyleSheet("""
            QLabel {
                color: #888888;
                font-size: 9px;
                padding: 2px 4px;
                background-color: #1a1a1a;
                border-radius: 2px;
                border: 1px solid #333333;
            }
        """)
        self.libretranslate_info_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        status_layout.addWidget(self.libretranslate_info_label)
        
        # Voortgangsbalk
        self.status_progress_bar = QProgressBar()
        self.status_progress_bar.setMinimumWidth(150)
        self.status_progress_bar.setMaximumWidth(200)
        self.status_progress_bar.setRange(0, 100)
        self.status_progress_bar.setValue(0)
        self.status_progress_bar.setVisible(False)  # Verborgen totdat er verwerking is
        self.status_progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #555555;
                border-radius: 3px;
                text-align: center;
                background-color: #2e2e2e;
                color: #ffffff;
                font-size: 10px;
            }
            QProgressBar::chunk {
                background-color: #4caf50;
                border-radius: 2px;
            }
        """)
        status_layout.addWidget(self.status_progress_bar)
        
        # Voeg widget toe aan statusbalk
        self.status_bar.addWidget(status_widget)
        
        # Stel standaard bericht in - UITGESCHAKELD om overbodige updates te voorkomen
        # self.status_bar.showMessage("Klaar")
        
        # Verbind status label met statusbalk - UITGESCHAKELD
        # self.status_label.setText("Klaar")
    
    def setup_timers(self):
        """Setup timers voor real-time updates"""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.periodic_update)
        self.update_timer.start(1000)
    
    def connect_monitors(self):
        """Verbind monitors aan het hoofdvenster na initialisatie"""
        try:
            if hasattr(self, 'charts_panel'):
                # Koppel alleen GPU monitor aan hoofdvenster
                if hasattr(self.charts_panel, 'gpu_monitor'):
                    self.charts_panel.gpu_monitor.main_window = self
                    print("✅ GPU Monitor gekoppeld aan hoofdvenster")
                else:
                    print("⚠️ GPU Monitor niet beschikbaar in charts panel")
            else:
                print("⚠️ Charts panel niet beschikbaar")
        except Exception as e:
            print(f"⚠️ Fout bij koppelen GPU monitor: {e}")
    
    def periodic_update(self):
        """Periodieke update functie"""
        # Controleer LibreTranslate server status elke 10 seconden
        if hasattr(self, '_last_libretranslate_check'):
            if time.time() - self._last_libretranslate_check > 10:  # Check elke 10 seconden
                self._check_libretranslate_status()
                self._last_libretranslate_check = time.time()
        else:
            self._last_libretranslate_check = time.time()
            self._check_libretranslate_status()
        
        # Controleer FFmpeg status elke 5 seconden
        if hasattr(self, '_last_ffmpeg_check'):
            if time.time() - self._last_ffmpeg_check > 5:  # Check elke 5 seconden
                self._check_ffmpeg_status()
                self._last_ffmpeg_check = time.time()
        else:
            self._last_ffmpeg_check = time.time()
            self._check_ffmpeg_status()
    
    def _check_libretranslate_status(self):
        """Controleer LibreTranslate server status"""
        try:
            # Haal LibreTranslate server URL op uit configuratie
            server_url = "http://100.90.127.78:5000"  # Gebruik de juiste server URL
            
            # Probeer LibreTranslate server te bereiken
            response = requests.get(f"{server_url}/languages", timeout=3)
            
            if response.status_code == 200:
                # Server is online
                self.libretranslate_status_label.setText("🟢 LibreTranslate: Online")
                self.libretranslate_status_label.setStyleSheet("""
                    QLabel {
                        color: #4CAF50;
                        font-size: 9px;
                        padding: 2px 4px;
                        background-color: #1B5E20;
                        border-radius: 2px;
                        border: 1px solid #4CAF50;
                        font-weight: bold;
                    }
                """)
                
                # Update info label
                try:
                    languages_data = response.json()
                    languages_count = len(languages_data) if isinstance(languages_data, list) else 0
                    self.libretranslate_info_label.setText(f"{languages_count} talen beschikbaar")
                    self.libretranslate_info_label.setStyleSheet("""
                        QLabel {
                            color: #4CAF50;
                            font-size: 9px;
                            padding: 2px 4px;
                            background-color: #1B5E20;
                            border-radius: 2px;
                            border: 1px solid #4CAF50;
                        }
                    """)
                except:
                    self.libretranslate_info_label.setText("Server online")
                    self.libretranslate_info_label.setStyleSheet("""
                        QLabel {
                            color: #4CAF50;
                            font-size: 9px;
                            padding: 2px 4px;
                            background-color: #1B5E20;
                            border-radius: 2px;
                            border: 1px solid #4CAF50;
                        }
                    """)
            else:
                # Server is offline
                self._set_libretranslate_offline()
                
        except requests.exceptions.RequestException:
            # Server niet bereikbaar
            self._set_libretranslate_offline()
        except Exception as e:
            # Andere fout
            print(f"⚠️ Fout bij LibreTranslate status check: {e}")
            self._set_libretranslate_offline()
    
    def _set_libretranslate_offline(self):
        """Stel LibreTranslate status in op offline"""
        self.libretranslate_status_label.setText("🔴 LibreTranslate: Offline")
        self.libretranslate_status_label.setStyleSheet("""
            QLabel {
                color: #F44336;
                font-size: 9px;
                padding: 2px 4px;
                background-color: #B71C1C;
                border-radius: 2px;
                border: 1px solid #F44336;
                font-weight: bold;
            }
        """)
        
        self.libretranslate_info_label.setText("Server niet bereikbaar")
        self.libretranslate_info_label.setStyleSheet("""
            QLabel {
                color: #888888;
                font-size: 9px;
                padding: 2px 4px;
                background-color: #1a1a1a;
                border-radius: 2px;
                border: 1px solid #333333;
            }
        """) 

    def _check_ffmpeg_status(self):
        """Controleer FFmpeg status"""
        try:
            import psutil
            
            # Zoek naar FFmpeg processen
            ffmpeg_running = False
            ffmpeg_cpu = 0.0
            
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    if 'ffmpeg' in proc.info['name'].lower():
                        ffmpeg_running = True
                        ffmpeg_cpu = proc.info['cpu_percent']
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if ffmpeg_running:
                # FFmpeg is actief
                self.ffmpeg_status_label.setText("🟢 FFmpeg: Actief")
                self.ffmpeg_status_label.setStyleSheet("""
                    QLabel {
                        color: #4CAF50;
                        font-size: 9px;
                        padding: 2px 4px;
                        background-color: #1B5E20;
                        border-radius: 2px;
                        border: 1px solid #4CAF50;
                        font-weight: bold;
                    }
                """)
                
                # Update info label met CPU gebruik
                self.ffmpeg_info_label.setText(f"CPU: {ffmpeg_cpu:.1f}%")
                self.ffmpeg_info_label.setStyleSheet("""
                    QLabel {
                        color: #4CAF50;
                        font-size: 9px;
                        padding: 2px 4px;
                        background-color: #1B5E20;
                        border-radius: 2px;
                        border: 1px solid #4CAF50;
                    }
                """)
            else:
                # FFmpeg is niet actief
                self.ffmpeg_status_label.setText("🔴 FFmpeg: Inactief")
                self.ffmpeg_status_label.setStyleSheet("""
                    QLabel {
                        color: #F44336;
                        font-size: 9px;
                        padding: 2px 4px;
                        background-color: #B71C1C;
                        border-radius: 2px;
                        border: 1px solid #F44336;
                        font-weight: bold;
                    }
                """)
                
                self.ffmpeg_info_label.setText("Geen processen")
                self.ffmpeg_info_label.setStyleSheet("""
                    QLabel {
                        color: #888888;
                        font-size: 9px;
                        padding: 2px 4px;
                        background-color: #1a1a1a;
                        border-radius: 2px;
                        border: 1px solid #333333;
                    }
                """)
                
        except Exception as e:
            print(f"⚠️ Fout bij FFmpeg status check: {e}")
            # Stel inactief in bij fout
            self.ffmpeg_status_label.setText("🔴 FFmpeg: Fout")
            self.ffmpeg_status_label.setStyleSheet("""
                QLabel {
                    color: #F44336;
                    font-size: 9px;
                    padding: 2px 4px;
                    background-color: #B71C1C;
                    border-radius: 2px;
                    border: 1px solid #F44336;
                    font-weight: bold;
                }
            """)
            
            self.ffmpeg_info_label.setText("Status check fout")
            self.ffmpeg_info_label.setStyleSheet("""
                QLabel {
                    color: #888888;
                    font-size: 9px;
                    padding: 2px 4px;
                    background-color: #1a1a1a;
                    border-radius: 2px;
                    border: 1px solid #333333;
                }
            """) 