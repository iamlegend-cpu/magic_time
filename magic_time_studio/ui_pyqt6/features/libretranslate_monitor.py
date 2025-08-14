"""
LibreTranslate Monitoring module voor Magic Time Studio
Toont LibreTranslate status (rood voor niet actief, groen voor actief)
"""

import requests
import time
from typing import Optional, Dict, Any
from PyQt6.QtCore import Qt, QTimer

class LibreTranslateMonitor:
    """LibreTranslate Monitoring klasse"""
    
    def __init__(self, parent_widget):
        self.parent = parent_widget
        
        # UI componenten
        self.libretranslate_chart = None
        self.libretranslate_timer = None
        self.main_window = None
        
        # LibreTranslate monitoring instellingen
        self.libretranslate_update_interval = 2000  # ms (2 seconden)
        self.processing_active = False
        
        # LibreTranslate cache en timing
        self.libretranslate_cache = {}
        self.libretranslate_cache_timeout = 10  # Cache voor 10 seconden
        self.last_libretranslate_check = 0
        
        # Setup timer voor LibreTranslate monitoring
        self.libretranslate_timer = QTimer()
        self.libretranslate_timer.timeout.connect(self.update_libretranslate_monitoring)
        self.libretranslate_timer.start(self.libretranslate_update_interval)  # Update elke 5 seconden
        
        # Verwerkingsstatus tracking
        self.processing_active = False
        
        # LibreTranslate server configuratie
        self.server_url = "http://localhost:5000"  # Standaard LibreTranslate server
        self.api_key = None  # Optionele API key
    
    def set_processing_status(self, is_processing: bool):
        """Stel verwerkingsstatus in voor betere LibreTranslate detectie"""
        self.processing_active = is_processing
        print(f"🔍 LibreTranslate Monitor: Verwerking status bijgewerkt - Processing: {is_processing}")
    
    def get_libretranslate_info(self):
        """Haal LibreTranslate informatie op"""
        try:
            # Controleer of LibreTranslate server bereikbaar is
            server_status = self._check_server_status()
            
            # Bepaal LibreTranslate status
            libretranslate_active = server_status['reachable']
            response_time = server_status['response_time']
            languages_available = server_status['languages_count']
            
            # Bereken status percentage (100% = volledig actief, 0% = niet bereikbaar)
            if libretranslate_active:
                # Server is bereikbaar, status op basis van response tijd
                if response_time < 100:  # Snelle response
                    status_percent = 100.0
                elif response_time < 500:  # Gemiddelde response
                    status_percent = 80.0
                else:  # Langzame response
                    status_percent = 60.0
            else:
                status_percent = 0.0
            
            return {
                'active': libretranslate_active,
                'status_percent': status_percent,
                'response_time': response_time,
                'languages_count': languages_available,
                'server_url': self.server_url
            }
            
        except Exception as e:
            print(f"⚠️ Fout bij ophalen LibreTranslate info: {e}")
            return {
                'active': False,
                'status_percent': 0.0,
                'response_time': 0,
                'languages_count': 0,
                'server_url': self.server_url
            }
    
    def _check_server_status(self):
        """Controleer LibreTranslate server status"""
        try:
            start_time = time.time()
            
            # Probeer server te bereiken via verschillende endpoints
            endpoints = ["/languages", "/", "/health"]
            server_reachable = False
            response_time = 0
            languages_count = 0
            
            for endpoint in endpoints:
                try:
                    response = requests.get(f"{self.server_url}{endpoint}", timeout=3)
                    
                    if response.status_code == 200:
                        # Server is bereikbaar
                        server_reachable = True
                        response_time = (time.time() - start_time) * 1000  # ms
                        
                        # Probeer languages te krijgen als het de /languages endpoint is
                        if endpoint == "/languages":
                            try:
                                languages_data = response.json()
                                languages_count = len(languages_data) if isinstance(languages_data, list) else 0
                            except:
                                languages_count = 0
                        
                        break  # Stop bij eerste succesvolle response
                        
                except requests.exceptions.RequestException:
                    continue  # Probeer volgende endpoint
            
            if server_reachable:
                return {
                    'reachable': True,
                    'response_time': response_time,
                    'languages_count': languages_count,
                    'status_code': 200
                }
            else:
                # Server niet bereikbaar
                return {
                    'reachable': False,
                    'response_time': 0,
                    'languages_count': 0,
                    'status_code': 0
                }
                
        except Exception as e:
            # Andere fout
            print(f"⚠️ LibreTranslate server check fout: {e}")
            return {
                'reachable': False,
                'response_time': 0,
                'languages_count': 0,
                'status_code': 0
            }
    
    def start_processing_monitoring(self):
        """Start snellere monitoring tijdens verwerking"""
        if self.libretranslate_timer:
            self.libretranslate_timer.stop()  # Stop huidige timer
            self.libretranslate_timer.start(2000)  # Snellere updates tijdens verwerking (2 seconden)
        print("🚀 LibreTranslate monitoring versneld voor verwerking (2s updates)")
        
        # Update LibreTranslate status om verwerking te tonen
        if self.main_window:
            self.main_window.libretranslate_status_label.setText("🔄 LibreTranslate: Verwerking...")
            self.main_window.libretranslate_status_label.setStyleSheet("""
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
        if self.libretranslate_timer:
            self.libretranslate_timer.stop()  # Stop huidige timer
            self.libretranslate_timer.start(2000)  # Normale snelheid na verwerking
        print("🛑 LibreTranslate monitoring terug naar normale snelheid (2s updates)")
        
        # Reset LibreTranslate status na verwerking
        if self.main_window:
            self.main_window.libretranslate_status_label.setText("⚪ LibreTranslate: Inactief")
            self.main_window.libretranslate_status_label.setStyleSheet("""
                QLabel {
                    color: #888888;
                    font-size: 9px;
                    padding: 2px 4px;
                    background-color: #1a1a1a;
                    border-radius: 2px;
                    border: 1px solid #333333;
                }
            """)
    
    def update_libretranslate_monitoring(self):
        """Update LibreTranslate monitoring data"""
        try:
            # Haal LibreTranslate info op
            libretranslate_info = self.get_libretranslate_info()
            
            # Update LibreTranslate chart met data
            if self.libretranslate_chart and hasattr(self.libretranslate_chart, 'add_data_point'):
                # Voeg status percentage toe aan chart
                self.libretranslate_chart.add_data_point(libretranslate_info['status_percent'])
            
            # Update LibreTranslate status text met kleurgecodeerde status
            if self.main_window:
                if libretranslate_info['active']:
                    # Groen voor LibreTranslate server online (ongeacht verzoeken)
                    if libretranslate_info['languages_count'] > 0:
                        status_text = f"🟢 LibreTranslate: {libretranslate_info['languages_count']} talen beschikbaar"
                    else:
                        status_text = f"🟢 LibreTranslate: Server online"
                    
                    self.main_window.libretranslate_status_label.setText(status_text)
                    self.main_window.libretranslate_status_label.setStyleSheet("""
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
                    # Rood voor server offline/niet bereikbaar
                    status_text = f"🔴 LibreTranslate: Server offline"
                    self.main_window.libretranslate_status_label.setText(status_text)
                    self.main_window.libretranslate_status_label.setStyleSheet("""
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
                
                # Update LibreTranslate info label met details
                if libretranslate_info['active']:
                    info_text = f"Response: {libretranslate_info['response_time']:.0f}ms | Talen: {libretranslate_info['languages_count']}"
                else:
                    info_text = "Server niet bereikbaar"
                
                if hasattr(self.main_window, 'libretranslate_info_label'):
                    self.main_window.libretranslate_info_label.setText(info_text)
                    
                    # Update styling op basis van activiteit
                    if libretranslate_info['active']:
                        self.main_window.libretranslate_info_label.setStyleSheet("""
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
                        self.main_window.libretranslate_info_label.setStyleSheet("""
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
            print(f"⚠️ Fout bij LibreTranslate monitoring update: {e}")
            # Voeg nog steeds 0% toe aan chart als fallback
            if self.libretranslate_chart and hasattr(self.libretranslate_chart, 'add_data_point'):
                self.libretranslate_chart.add_data_point(0.0)
