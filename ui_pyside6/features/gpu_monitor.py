"""
GPU Monitoring module voor Magic Time Studio
Alleen WhisperX wordt ondersteund
"""

import torch
import time
from typing import Optional, Dict, Any
from PySide6.QtCore import Qt, QTimer

class GPUMonitor:
    """GPU Monitoring klasse voor WhisperX"""
    
    def __init__(self, parent_widget):
        self.parent = parent_widget
        
        # UI componenten
        self.gpu_chart = None
        self.gpu_timer = None
        self.main_window = None
        
        # Zoek naar de main window
        self._find_main_window()
        
        # GPU monitoring instellingen
        self.gpu_update_interval = 500  # ms
        self.processing_active = False
        
        # GPU cache en timing
        self.gpu_cache = {}
        self.gpu_cache_timeout = 2  # Cache voor 2 seconden
        self.last_gpu_check = 0
        
        # Verwerkingsstatus tracking
        self.processing_active = False
        self.whisperx_processing = False
        
        # Koppeling aan processing manager
        self.processing_manager = None
        self._try_connect_processing_manager()
        
        # Setup timer voor GPU monitoring
        self.gpu_timer = QTimer()
        self.gpu_timer.timeout.connect(self.update_gpu_monitoring)
        self.gpu_timer.start(self.gpu_update_interval)  # Update elke 500ms voor GPU
        
        # Verwerkingsstatus tracking
        self.processing_active = False
        self.whisperx_processing = False
    
    def _find_main_window(self):
        """Zoek naar de main window in de parent hierarchy"""
        try:
            parent = self.parent
            while parent:
                if hasattr(parent, 'main_window'):
                    self.main_window = parent.main_window
                    break
                elif hasattr(parent, 'parent') and callable(parent.parent):
                    parent = parent.parent()
                else:
                    break
        except Exception as e:
            pass
    
    def _try_connect_processing_manager(self):
        """Probeer te koppelen aan de processing manager voor betere status detectie"""
        try:
            # Zoek naar de processing manager in de parent hierarchy
            parent = self.parent
            while parent:
                if hasattr(parent, 'processing_manager'):
                    self.processing_manager = parent.processing_manager
                    break
                elif hasattr(parent, 'main_window') and hasattr(parent.main_window, 'processing_manager'):
                    self.processing_manager = parent.main_window.processing_manager
                    break
                parent = parent.parent()
        except Exception as e:
            pass
    
    def _get_processing_status_from_manager(self):
        """Haal verwerkingsstatus op van de processing manager"""
        # Gebruik de ingestelde status direct in plaats van manager te vragen
        return self.processing_active
    
    def set_processing_status(self, is_processing: bool, is_whisperx: bool = False):
        """Stel verwerkingsstatus in voor betere GPU detectie"""
        self.processing_active = is_processing
        self.whisperx_processing = is_whisperx
        
        print(f"🔍 GPU Monitor: Verwerking status bijgewerkt - Processing: {is_processing}, WhisperX: {is_whisperx}")
        
        # Als verwerking stopt, reset ook de GPU cache
        if not is_processing:
            self.gpu_cache = {}
            self.last_gpu_check = 0
        
        # Start/s stop snellere monitoring tijdens verwerking
        if is_processing:
            self.start_processing_monitoring()
        else:
            self.stop_processing_monitoring()
        
        # Force een onmiddellijke update van de GPU status
        if self.main_window:
            self._update_gpu_status_display()
    
    def _update_gpu_status_display(self):
        """Update de GPU status display onmiddellijk"""
        try:
            if not self.main_window:
                return
                
            # Haal huidige GPU info op
            gpu_info = self.get_whisperx_gpu_info()
            
            if gpu_info:
                gpu_percent = gpu_info.get('utilization', 0)
                whisperx_active = gpu_info.get('whisperx_active', False)
                cuda_active = gpu_info.get('cuda_active', False)
                
                # Gebruik echte GPU utilization als deze beschikbaar is
                # Anders gebruik memory-based schatting
                if gpu_percent > 0:
                    # Echte GPU utilization beschikbaar
                    pass
                else:
                    # Fallback naar memory-based schatting
                    gpu_percent = gpu_info.get('memory_utilization', 0)
                
                # Gebruik verwerkingsstatus voor betere detectie
                if self.whisperx_processing and self.processing_active:
                    whisperx_active = True
                    cuda_active = True
                    # Gebruik echte GPU percentage tijdens verwerking
                    # Geen kunstmatige verhoging meer
                else:
                    # Als verwerking niet actief is, reset status naar inactief
                    whisperx_active = False
                    cuda_active = False
                
                # Update GPU status text met kleurgecodeerde status
                if self.whisperx_processing and self.processing_active:
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
                elif self.processing_active:
                    # Oranje voor verwerking actief
                    status_text = f"🟡 GPU: {gpu_percent:.1f}% - Verwerking actief"
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
                
                # Update GPU memory info
                try:
                    if torch.cuda.is_available():
                        # Gebruik nvidia-smi voor accurate memory monitoring
                        try:
                            import subprocess
                            # Haal memory info op via nvidia-smi
                            result = subprocess.run(['nvidia-smi', '--query-gpu=memory.used,memory.total', '--format=csv,noheader,nounits'], 
                                                 capture_output=True, text=True, timeout=5)
                            if result.returncode == 0:
                                # Parse output: "used_memory, total_memory"
                                memory_info = result.stdout.strip().split(',')
                                if len(memory_info) == 2:
                                    allocated = float(memory_info[0]) / 1024  # Convert MB to GB
                                    total = float(memory_info[1]) / 1024     # Convert MB to GB
                                else:
                                    # Fallback naar PyTorch
                                    allocated = torch.cuda.memory_allocated() / (1024**3)  # GB
                                    total = torch.cuda.get_device_properties(0).total_memory / (1024**3)  # GB
                            else:
                                # Fallback naar PyTorch
                                allocated = torch.cuda.memory_allocated() / (1024**3)  # GB
                                total = torch.cuda.get_device_properties(0).total_memory / (1024**3)  # GB
                        except:
                            # Fallback naar PyTorch
                            allocated = torch.cuda.memory_allocated() / (1024**3)  # GB
                            total = torch.cuda.get_device_properties(0).total_memory / (1024**3)  # GB
                        
                        # Als verwerking niet actief is, toon lagere memory waarden
                        if not self.processing_active:
                            # Toon alleen basis memory info zonder styling
                            memory_text = f"Memory: {allocated:.2f}GB/{total:.2f}GB"
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
                            # Toon actieve memory styling tijdens verwerking
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
                            elif allocated > 0.01:  # Meer dan 10MB gebruikt
                                self.main_window.gpu_memory_label.setStyleSheet("""
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
                    pass
                    
        except Exception as e:
            pass
    
    def get_whisperx_gpu_info(self):
        """Krijg GPU informatie voor WhisperX monitoring"""
        try:
            if not torch.cuda.is_available():
                return None
            
            # Gebruik de verbeterde CUDA GPU info methode
            return self._get_cuda_gpu_info()
            
        except Exception as e:
            return None
    
    def _get_cuda_gpu_info(self):
        """Haal gedetailleerde CUDA GPU informatie op"""
        try:
            if not torch.cuda.is_available():
                return None
            
            device = torch.cuda.current_device()
            props = torch.cuda.get_device_properties(device)
            
            # Haal memory info op
            try:
                # Gebruik nvidia-smi voor accurate memory monitoring
                import subprocess
                result = subprocess.run(['nvidia-smi', '--query-gpu=memory.used,memory.total', '--format=csv,noheader,nounits'], 
                                     capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    # Parse output: "used_memory, total_memory"
                    memory_info = result.stdout.strip().split(',')
                    if len(memory_info) == 2:
                        allocated = float(memory_info[0]) * 1024 * 1024  # Convert MB to bytes
                        total = float(memory_info[1]) * 1024 * 1024     # Convert MB to bytes
                        reserved = allocated  # nvidia-smi geeft alleen used/total
                    else:
                        # Fallback naar PyTorch
                        allocated = torch.cuda.memory_allocated(device)
                        reserved = torch.cuda.memory_reserved(device)
                        total = props.total_memory
                else:
                    # Fallback naar PyTorch
                    allocated = torch.cuda.memory_allocated(device)
                    reserved = torch.cuda.memory_reserved(device)
                    total = props.total_memory
            except:
                # Fallback naar PyTorch
                allocated = torch.cuda.memory_allocated(device)
                reserved = torch.cuda.memory_reserved(device)
                total = props.total_memory
            
            # Bereken utilization op basis van memory gebruik
            memory_utilization = (allocated / total) * 100 if total > 0 else 0
            
            # Probeer echte GPU utilization te krijgen via nvidia-smi of andere methoden
            try:
                import subprocess
                result = subprocess.run(['nvidia-smi', '--query-gpu=utilization.gpu', '--format=csv,noheader,nounits'], 
                                     capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    gpu_util = float(result.stdout.strip())
                    # Gebruik echte GPU utilization als deze beschikbaar is
                    utilization = gpu_util
                else:
                    # Fallback naar memory-based utilization
                    utilization = memory_utilization
            except:
                # Fallback naar memory-based utilization
                utilization = memory_utilization
            
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
                # Gebruik echte GPU percentage tijdens verwerking
                # Geen kunstmatige verhoging meer
            else:
                # Als verwerking niet actief is, reset alle status naar inactief
                whisperx_active = False
                cuda_active = False
                # Gebruik echte GPU percentage
                # Geen kunstmatige verlaging meer
            
            # AUTOMATISCHE DETECTIE: Als er significant CUDA memory wordt gebruikt (>50MB),
            # beschouw dit als actieve verwerking, maar alleen als verwerking daadwerkelijk actief is
            if allocated > 50 * 1024 * 1024 and self.processing_active:  # >50MB EN verwerking actief
                if not self.processing_active:
                    # Stel verwerkingsstatus automatisch in
                    self.processing_active = True
                    self.whisperx_processing = True
                    whisperx_active = True
                    cuda_active = True
                    
                    # Gebruik echte GPU percentage
                    # Geen kunstmatige verhoging meer
            
            return {
                'utilization': min(utilization, 100.0),
                'memory_utilization': min(memory_utilization, 100.0),
                'memory_allocated': allocated,
                'memory_reserved': reserved,
                'memory_total': total,
                'whisperx_active': whisperx_active,
                'cuda_active': cuda_active,
                'device_name': props.name
            }
            
        except Exception as e:
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
            self.gpu_timer.start(100)  # Snelle updates tijdens verwerking
        
        # Stel verwerkingsstatus in
        self.processing_active = True
        self.whisperx_processing = True
        
        # Force een onmiddellijke update van de GPU status
        if self.main_window:
            self._update_gpu_status_display()
    
    def stop_processing_monitoring(self):
        """Stop snellere monitoring na verwerking"""
        if self.gpu_timer:
            self.gpu_timer.stop()  # Stop huidige timer
            self.gpu_timer.start(500)  # Normale snelheid na verwerking
        
        # Reset verwerkingsstatus
        self.processing_active = False
        self.whisperx_processing = False
        
        # Reset GPU cache
        self.gpu_cache = {}
        self.last_gpu_check = 0
        
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
            if hasattr(self.main_window, 'gpu_memory_label'):
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
        self._update_gpu_status_display()
    
    def update_gpu_monitoring(self):
        """Update GPU monitoring data"""
        try:
            # Probeer verwerkingsstatus op te halen van processing manager
            if not self.processing_active:
                actual_processing_status = self._get_processing_status_from_manager()
                if actual_processing_status != self.processing_active:
                    self.processing_active = actual_processing_status
                    self.whisperx_processing = actual_processing_status
            
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
                        # Gebruik echte GPU percentage tijdens verwerking
                        # Geen kunstmatige verhoging meer
                    else:
                        # Als verwerking niet actief is, reset GPU status naar inactief
                        whisperx_active = False
                        cuda_active = False
                        # Gebruik echte GPU percentage
                        # Geen kunstmatige verlaging meer
                    
                    # Update GPU chart met data
                    if self.gpu_chart and hasattr(self.gpu_chart, 'add_data_point'):
                        self.gpu_chart.add_data_point(gpu_percent)
                    
                    # Update GPU status display
                    self._update_gpu_status_display()
                    
                else:
                    # Voeg 0% toe aan chart als fallback
                    if self.gpu_chart and hasattr(self.gpu_chart, 'add_data_point'):
                        self.gpu_chart.add_data_point(0.0)
                    
            else:
                # Geen CUDA beschikbaar
                if self.main_window:
                    self.main_window.gpu_status_label.setText("❌ GPU: CUDA niet beschikbaar")
                    self.main_window.gpu_status_label.setStyleSheet("""
                        QLabel {
                            color: #9E9E9E;
                            font-size: 9px;
                            padding: 2px 4px;
                            background-color: #424242;
                            border-radius: 2px;
                            border: 1px solid #9E9E9E;
                        }
                    """)
                    
                    # Reset memory label ook
                    if hasattr(self.main_window, 'gpu_memory_label'):
                        self.main_window.gpu_memory_label.setText("Memory: N/A")
                        self.main_window.gpu_memory_label.setStyleSheet("""
                            QLabel {
                                color: #9E9E9E;
                                font-size: 9px;
                                padding: 2px 4px;
                                background-color: #424242;
                                border-radius: 2px;
                                border: 1px solid #9E9E9E;
                            }
                        """)
                    
        except Exception as e:
            # Voeg 0% toe aan chart als fallback bij fout
            if self.gpu_chart and hasattr(self.gpu_chart, 'add_data_point'):
                self.gpu_chart.add_data_point(0.0)
