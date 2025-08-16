"""
FFmpeg Monitoring module voor Magic Time Studio
Toont FFmpeg status (rood voor niet actief, groen voor actief)
"""

import psutil
import time
from typing import Optional, Dict, Any
from PySide6.QtCore import Qt, QTimer

class FFmpegMonitor:
    """FFmpeg Monitoring klasse"""
    
    def __init__(self, parent_widget):
        self.parent = parent_widget
        
        # UI componenten
        self.ffmpeg_chart = None
        self.ffmpeg_timer = None
        self.main_window = None
        
        # FFmpeg monitoring instellingen
        self.ffmpeg_update_interval = 1000  # ms
        self.processing_active = False
        
        # FFmpeg cache en timing
        self.ffmpeg_cache = {}
        self.ffmpeg_cache_timeout = 2  # Cache voor 2 seconden
        self.last_ffmpeg_check = 0
        
        # Setup timer voor FFmpeg monitoring
        self.ffmpeg_timer = QTimer()
        self.ffmpeg_timer.timeout.connect(self.update_ffmpeg_monitoring)
        self.ffmpeg_timer.start(self.ffmpeg_update_interval)  # Update elke seconde
        
        # Verwerkingsstatus tracking
        self.processing_active = False
    
    def set_processing_status(self, is_processing: bool):
        """Stel verwerkingsstatus in voor betere FFmpeg detectie"""
        self.processing_active = is_processing
        print(f"🔍 FFmpeg Monitor: Verwerking status bijgewerkt - Processing: {is_processing}")
        
        # Start/s stop snellere monitoring tijdens verwerking
        if is_processing:
            self.start_processing_monitoring()
        else:
            self.stop_processing_monitoring()
    
    def get_ffmpeg_info(self):
        """Haal FFmpeg informatie op"""
        try:
            # Zoek naar FFmpeg processen
            ffmpeg_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_info']):
                try:
                    # Controleer of het een FFmpeg proces is
                    if proc.info['name'] and 'ffmpeg' in proc.info['name'].lower():
                        ffmpeg_processes.append(proc.info)
                    elif proc.info['cmdline']:
                        cmdline = ' '.join(proc.info['cmdline']).lower()
                        if 'ffmpeg' in cmdline:
                            ffmpeg_processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            # Bepaal FFmpeg status
            ffmpeg_active = len(ffmpeg_processes) > 0
            ffmpeg_count = len(ffmpeg_processes)
            
            # Bereken totale CPU en memory gebruik van FFmpeg processen
            total_cpu = 0.0
            total_memory = 0.0
            
            for proc_info in ffmpeg_processes:
                try:
                    if proc_info['cpu_percent'] is not None:
                        total_cpu += proc_info['cpu_percent']
                    if proc_info['memory_info']:
                        total_memory += proc_info['memory_info'].rss / (1024**2)  # MB
                except:
                    pass
            
            return {
                'active': ffmpeg_active,
                'process_count': ffmpeg_count,
                'cpu_percent': total_cpu,
                'memory_mb': total_memory,
                'processes': ffmpeg_processes
            }
            
        except Exception as e:
            print(f"⚠️ Fout bij ophalen FFmpeg info: {e}")
            return {
                'active': False,
                'process_count': 0,
                'cpu_percent': 0.0,
                'memory_mb': 0.0,
                'processes': []
            }
    
    def start_processing_monitoring(self):
        """Start snellere monitoring tijdens verwerking"""
        if self.ffmpeg_timer:
            self.ffmpeg_timer.stop()  # Stop huidige timer
            self.ffmpeg_timer.start(500)  # Snellere updates tijdens verwerking (500ms)
        print("🚀 FFmpeg monitoring versneld voor verwerking (500ms updates)")
        
        # Update FFmpeg status om verwerking te tonen
        if self.main_window:
            self.main_window.ffmpeg_status_label.setText("🔄 FFmpeg: Verwerking...")
            self.main_window.ffmpeg_status_label.setStyleSheet("""
                QLabel {
                    color: #2196F3;
                    font-size: 9px;
                    padding: 2px 4px;
                    background-color: #0D47A1;
                    border-radius: 2px;
                    border: 1px solid #2196F3;
                    font-weight: bold;
                }
            """)
    
    def stop_processing_monitoring(self):
        """Stop snellere monitoring na verwerking"""
        if self.ffmpeg_timer:
            self.ffmpeg_timer.stop()  # Stop huidige timer
            self.ffmpeg_timer.start(1000)  # Normale snelheid na verwerking
        print("🛑 FFmpeg monitoring terug naar normale snelheid (1000ms updates)")
        
        # Reset FFmpeg status na verwerking
        if self.main_window:
            self.main_window.ffmpeg_status_label.setText("⚪ FFmpeg: Inactief")
            self.main_window.ffmpeg_status_label.setStyleSheet("""
                QLabel {
                    color: #888888;
                    font-size: 9px;
                    padding: 2px 4px;
                    background-color: #1a1a1a;
                    border-radius: 2px;
                    border: 1px solid #333333;
                }
            """)
    
    def update_ffmpeg_monitoring(self):
        """Update FFmpeg monitoring data"""
        try:
            # Haal FFmpeg info op
            ffmpeg_info = self.get_ffmpeg_info()
            
            # Update FFmpeg chart met data
            if self.ffmpeg_chart and hasattr(self.ffmpeg_chart, 'add_data_point'):
                # Voeg CPU percentage toe aan chart
                self.ffmpeg_chart.add_data_point(ffmpeg_info['cpu_percent'])
            
            # Update FFmpeg status text met kleurgecodeerde status
            if self.main_window:
                if ffmpeg_info['active'] or self.processing_active:
                    # Groen voor FFmpeg actief
                    if ffmpeg_info['process_count'] > 0:
                        status_text = f"🟢 FFmpeg: {ffmpeg_info['process_count']} proces(s) actief"
                    else:
                        status_text = f"🟢 FFmpeg: Verwerking actief"
                    
                    self.main_window.ffmpeg_status_label.setText(status_text)
                    self.main_window.ffmpeg_status_label.setStyleSheet("""
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
                else:
                    # Rood voor inactief
                    status_text = f"🔴 FFmpeg: Niet actief"
                    self.main_window.ffmpeg_status_label.setText(status_text)
                    self.main_window.ffmpeg_status_label.setStyleSheet("""
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
                
                # Update FFmpeg info label met details
                if ffmpeg_info['active']:
                    info_text = f"CPU: {ffmpeg_info['cpu_percent']:.1f}% | RAM: {ffmpeg_info['memory_mb']:.1f}MB"
                else:
                    info_text = "Geen actieve processen"
                
                if hasattr(self.main_window, 'ffmpeg_info_label'):
                    self.main_window.ffmpeg_info_label.setText(info_text)
                    
                    # Update styling op basis van activiteit
                    if ffmpeg_info['active']:
                        self.main_window.ffmpeg_info_label.setStyleSheet("""
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
                        self.main_window.ffmpeg_info_label.setStyleSheet("""
                            QLabel {
                                color: #888888;
                                font-size: 9px;
                                padding: 2px 4px;
                                background-color: #1a1a1a;
                                border-radius: 2px;
                                border: 1px solid #333333;
                            }
                        """)
            else:
                print(f"⚠️ Main window niet beschikbaar: {self.main_window}")
                
        except Exception as e:
            # Stille fout om performance niet te beïnvloeden
            print(f"⚠️ Fout bij FFmpeg monitoring update: {e}")
            # Voeg nog steeds 0% toe aan chart als fallback
            if self.ffmpeg_chart and hasattr(self.ffmpeg_chart, 'add_data_point'):
                self.ffmpeg_chart.add_data_point(0.0)
