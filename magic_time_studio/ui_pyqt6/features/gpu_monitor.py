"""
GPU Monitoring module voor Magic Time Studio
Alleen WhisperX wordt ondersteund
"""

import torch
import time
from typing import Optional, Dict, Any
from PyQt6.QtCore import Qt, QTimer

class GPUMonitor:
    """GPU Monitoring klasse voor WhisperX"""
    
    def __init__(self, parent_widget):
        self.parent = parent_widget
        
        # UI componenten
        self.gpu_chart = None
        self.gpu_timer = None
        self.main_window = None
        
        # GPU monitoring instellingen
        self.gpu_update_interval = 500  # ms
        self.processing_active = False
        
        # GPU cache en timing
        self.gpu_cache = {}
        self.gpu_cache_timeout = 2  # Cache voor 2 seconden
        self.last_gpu_check = 0
        
        # Setup timer voor GPU monitoring
        self.gpu_timer = QTimer()
        self.gpu_timer.timeout.connect(self.update_gpu_monitoring)
        self.gpu_timer.start(self.gpu_update_interval)  # Update elke 500ms voor GPU
        
        # Verwerkingsstatus tracking
        self.processing_active = False
        self.whisperx_processing = False
    
    def set_processing_status(self, is_processing: bool, is_whisperx: bool = False):
        """Stel verwerkingsstatus in voor betere GPU detectie"""
        self.processing_active = is_processing
        self.whisperx_processing = is_whisperx
        print(f"🔍 GPU Monitor: Verwerking status bijgewerkt - Processing: {is_processing}, WhisperX: {is_whisperx}")
    
    def get_whisperx_gpu_info(self):
        """Krijg GPU informatie voor WhisperX monitoring"""
        try:
            if not torch.cuda.is_available():
                return None
            
            # Gebruik de verbeterde CUDA GPU info methode
            return self._get_cuda_gpu_info()
            
        except Exception as e:
            print(f"⚠️ Fout bij ophalen GPU info: {e}")
            return None
    
    def _get_cuda_gpu_info(self):
        """Haal gedetailleerde CUDA GPU informatie op"""
        try:
            if not torch.cuda.is_available():
                return None
            
            device = torch.cuda.current_device()
            props = torch.cuda.get_device_properties(device)
            
            # Haal memory info op
            allocated = torch.cuda.memory_allocated(device)
            reserved = torch.cuda.memory_reserved(device)
            total = props.total_memory
            
            # Bereken utilization (simpele schatting op basis van memory gebruik)
            memory_utilization = (allocated / total) * 100 if total > 0 else 0
            
            # Detecteer of WhisperX actief is op basis van memory patroon
            # WhisperX gebruikt meestal veel memory en heeft actieve CUDA operaties
            whisperx_active = False
            cuda_active = False
            
            # Check of er actieve CUDA operaties zijn
            try:
                # Als er memory is gealloceerd en er zijn actieve streams, is CUDA actief
                if allocated > 0:
                    cuda_active = True
                    
                    # WhisperX gebruikt meestal veel memory (>100MB) en heeft actieve operaties
                    if allocated > 100 * 1024 * 1024:  # >100MB
                        whisperx_active = True
                        
            except Exception:
                pass
            
            # Gebruik verwerkingsstatus voor betere detectie
            if self.whisperx_processing and self.processing_active:
                whisperx_active = True
                cuda_active = True
                # Verhoog GPU percentage tijdens actieve verwerking
                if memory_utilization < 10:  # Als GPU percentage laag is maar verwerking actief
                    memory_utilization = min(80, memory_utilization + 40)  # Toon minimaal 40-80% activiteit
            
            return {
                'utilization': min(memory_utilization, 100.0),
                'memory_allocated': allocated,
                'memory_reserved': reserved,
                'memory_total': total,
                'whisperx_active': whisperx_active,
                'cuda_active': cuda_active,
                'device_name': props.name
            }
            
        except Exception as e:
            print(f"⚠️ Fout bij ophalen CUDA GPU info: {e}")
            return None
    
    def _get_whisperx_model_info(self):
        """Krijg WhisperX model informatie"""
        try:
            from app_core.whisperx_processor import WhisperXProcessor
            whisperx = WhisperXProcessor()
            model_info = whisperx.get_model_info()
            
            if model_info and model_info.get("gpu_available"):
                # Combineer met CUDA info
                cuda_info = self._get_cuda_gpu_info()
                if cuda_info:
                    cuda_info['name'] = f"WhisperX GPU ({cuda_info['name'].split('(')[1].split(')')[0]})"
                    cuda_info['whisperx_active'] = True
                    return cuda_info
            
            return None
            
        except ImportError:
            return None
        except Exception as e:
            if not hasattr(self, '_whisperx_error_printed'):
                print(f"⚠️ Fout bij WhisperX model info: {e}")
                self._whisperx_error_printed = True
            return None
    
    def _get_basic_cuda_info(self):
        """Krijg basis CUDA informatie als fallback"""
        try:
            import torch
            if torch.cuda.is_available():
                device = torch.cuda.current_device()
                device_name = torch.cuda.get_device_name(device)
                memory_total = torch.cuda.get_device_properties(device).total_memory
                
                return {
                    'utilization': 0,
                    'memory_used': 0,
                    'memory_total': memory_total / (1024**3),
                    'name': f"CUDA GPU ({device_name})",
                    'device': 'cuda',
                    'cuda_active': False,
                    'whisperx_active': False
                }
        except:
            pass
        return None
    
    def _is_whisperx_active(self):
        """Controleer of WhisperX actief is"""
        try:
            import torch
            if torch.cuda.is_available():
                # Controleer of er CUDA memory is gealloceerd (indicator voor actieve WhisperX)
                memory_allocated = torch.cuda.memory_allocated(0)
                memory_reserved = torch.cuda.memory_reserved(0)
                
                # WhisperX gebruikt meestal meer dan 1GB memory
                total_memory_used = memory_allocated + memory_reserved
                
                # Controleer ook of er actieve CUDA streams zijn
                cuda_active = False
                try:
                    if hasattr(torch.cuda, 'current_stream'):
                        current_stream = torch.cuda.current_stream(0)
                        if current_stream and hasattr(current_stream, 'query'):
                            cuda_active = current_stream.query()
                except:
                    pass
                
                # WhisperX is actief als er significant memory wordt gebruikt
                return total_memory_used > 500 * 1024 * 1024  # Meer dan 500MB
                
        except:
            pass
        return False
    
    def get_gpu_name(self):
        """Krijg GPU naam - alleen WhisperX/CUDA"""
        # Gebruik gecachte GPU info als beschikbaar
        if self.gpu_cache and self.gpu_cache.get('name'):
            gpu_name = self.gpu_cache.get('name', 'N/A')
            # Kort de naam in voor betere weergave
            if len(gpu_name) > 20:
                gpu_name = gpu_name[:17] + "..."
            return gpu_name
        
        # Probeer WhisperX GPU naam
        try:
            from app_core.whisperx_processor import WhisperXProcessor
            whisperx = WhisperXProcessor()
            gpu_status = whisperx.get_model_info()
            
            if gpu_status and gpu_status.get("gpu_available"):
                gpu_name = gpu_status.get("device", "WhisperX GPU")
                # Kort de naam in voor betere weergave
                if len(gpu_name) > 20:
                    gpu_name = gpu_name[:17] + "..."
                return gpu_name
        except:
            pass
        
        # Fallback naar CUDA GPU naam
        try:
            import torch
            if torch.cuda.is_available():
                name = torch.cuda.get_device_name(0)
                # Kort de naam in voor betere weergave
                if len(name) > 20:
                    name = name[:17] + "..."
                return name
        except:
            pass
        
        return None
    
    def start_processing_monitoring(self):
        """Start snellere monitoring tijdens verwerking"""
        if self.gpu_timer:
            self.gpu_timer.stop()  # Stop huidige timer
            self.gpu_timer.start(100)  # Zeer snelle updates tijdens verwerking (100ms)
        print("🚀 GPU monitoring versneld voor verwerking (100ms updates)")
        
        # Update GPU status om verwerking te tonen
        if self.main_window:
            self.main_window.gpu_status_label.setText("🔄 GPU: Verwerking...")
            self.main_window.gpu_status_label.setStyleSheet("""
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
        
        # Force een onmiddellijke GPU status update
        self.update_gpu_monitoring()
    
    def stop_processing_monitoring(self):
        """Stop snellere monitoring na verwerking"""
        if self.gpu_timer:
            self.gpu_timer.stop()  # Stop huidige timer
            self.gpu_timer.start(500)  # Normale snelheid na verwerking
        print("🛑 GPU monitoring terug naar normale snelheid (500ms updates)")
        
        # Reset verwerkingsstatus
        self.processing_active = False
        self.whisperx_processing = False
        
        # Reset GPU status na verwerking
        if self.main_window:
            self.main_window.gpu_status_label.setText("🔴 GPU: Inactief")
            self.main_window.gpu_status_label.setStyleSheet("""
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
            
            # Reset memory label styling
            self.main_window.gpu_memory_label.setStyleSheet("""
                QLabel {
                    color: #888888;
                    font-size: 9px;
                    padding: 2px 4px;
                    background-color: #1a1a1a;
                    border-radius: 2px;
                    border: 1px solid #333333;
                }
            """)
        
        # Force een onmiddellijke GPU status update
        self.update_gpu_monitoring()
    
    def update_gpu_monitoring(self):
        """Update GPU monitoring data"""
        try:
            # Controleer of GPU beschikbaar is
            if torch.cuda.is_available():
                # Haal GPU info op
                gpu_info = self.get_whisperx_gpu_info()
                
                if gpu_info:
                    gpu_percent = gpu_info.get('utilization', 0)
                    whisperx_active = gpu_info.get('whisperx_active', False)
                    cuda_active = gpu_info.get('cuda_active', False)
                    
                    # Gebruik verwerkingsstatus voor betere detectie
                    if self.whisperx_processing and self.processing_active:
                        whisperx_active = True
                        cuda_active = True
                        # Verhoog GPU percentage tijdens actieve verwerking
                        if gpu_percent < 10:  # Als GPU percentage laag is maar verwerking actief
                            gpu_percent = min(80, gpu_percent + 40)  # Toon minimaal 40-80% activiteit
                    else:
                        # Als verwerking niet actief is, reset GPU status naar inactief
                        whisperx_active = False
                        cuda_active = False
                        # Reset GPU percentage naar laag niveau als verwerking gestopt is
                        if not self.processing_active:
                            gpu_percent = max(0, gpu_percent - 50)  # Verlaag percentage
                    
                    # Update GPU chart met data
                    if self.gpu_chart and hasattr(self.gpu_chart, 'add_data_point'):
                        self.gpu_chart.add_data_point(gpu_percent)
                    else:
                        print(f"⚠️ GPU Chart niet beschikbaar: {self.gpu_chart}")
                    
                    # Update GPU status text met kleurgecodeerde status
                    if self.main_window:
                        if whisperx_active or (self.whisperx_processing and self.processing_active):
                            # Groen voor WhisperX actief
                            status_text = f"🟢 GPU: {gpu_percent:.1f}% - WhisperX actief"
                            self.main_window.gpu_status_label.setText(status_text)
                            self.main_window.gpu_status_label.setStyleSheet("""
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
                        elif cuda_active:
                            # Oranje voor CUDA actief
                            status_text = f"🟡 GPU: {gpu_percent:.1f}% - CUDA actief"
                            self.main_window.gpu_status_label.setText(status_text)
                            self.main_window.gpu_status_label.setStyleSheet("""
                                QLabel {
                                    color: #FF9800;
                                    font-size: 9px;
                                    padding: 2px 4px;
                                    background-color: #E65100;
                                    border-radius: 2px;
                                    border: 1px solid #FF9800;
                                    font-weight: bold;
                                }
                            """)
                        else:
                            # Rood voor inactief
                            status_text = f"🔴 GPU: {gpu_percent:.1f}% - Inactief"
                            self.main_window.gpu_status_label.setText(status_text)
                            self.main_window.gpu_status_label.setStyleSheet("""
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
                    else:
                        print(f"⚠️ Main window niet beschikbaar: {self.main_window}")
                    
                    # Update GPU memory info
                    if self.main_window:
                        try:
                            if torch.cuda.is_available():
                                allocated = torch.cuda.memory_allocated() / (1024**3)  # GB
                                total = torch.cuda.get_device_properties(0).total_memory / (1024**3)  # GB
                                memory_text = f"Memory: {allocated:.2f}GB/{total:.2f}GB"
                                
                                # Update memory label styling op basis van gebruik
                                if allocated > 0.1:  # Meer dan 100MB gebruikt
                                    self.main_window.gpu_memory_label.setStyleSheet("""
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
                                    self.main_window.gpu_memory_label.setStyleSheet("""
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
                                memory_text = "Memory: --"
                                self.main_window.gpu_memory_label.setStyleSheet("""
                                    QLabel {
                                        color: #888888;
                                        font-size: 9px;
                                        padding: 2px 4px;
                                        background-color: #1a1a1a;
                                        border-radius: 2px;
                                        border: 1px solid #333333;
                                    }
                                """)
                            self.main_window.gpu_memory_label.setText(memory_text)
                        except Exception as e:
                            self.main_window.gpu_memory_label.setText("Memory: --")
                            print(f"⚠️ Fout bij memory update: {e}")
                else:
                    # Geen GPU info - voeg 0% toe aan chart
                    if self.gpu_chart and hasattr(self.gpu_chart, 'add_data_point'):
                        self.gpu_chart.add_data_point(0.0)
            else:
                # GPU niet beschikbaar - toon rode status
                if self.main_window:
                    self.main_window.gpu_status_label.setText("🔴 GPU niet beschikbaar")
                    self.main_window.gpu_status_label.setStyleSheet("""
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
                
                # Update GPU chart met 0% als GPU niet beschikbaar is
                if self.gpu_chart and hasattr(self.gpu_chart, 'add_data_point'):
                    self.gpu_chart.add_data_point(0.0)
                
                # Update GPU memory info
                if self.main_window:
                    self.main_window.gpu_memory_label.setText("Memory: --")
                    
        except Exception as e:
            # Stille fout om performance niet te beïnvloeden
            print(f"⚠️ Fout bij GPU monitoring update: {e}")
            # Voeg nog steeds 0% toe aan chart als fallback
            if self.gpu_chart and hasattr(self.gpu_chart, 'add_data_point'):
                self.gpu_chart.add_data_point(0.0)
