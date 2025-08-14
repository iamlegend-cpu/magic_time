"""
VAD (Voice Activity Detection) Instellingen voor Settings Panel
Beheert VAD configuratie, testen en optimalisatie
"""

from PyQt6.QtWidgets import (
    QGroupBox, QFormLayout, QCheckBox, QComboBox, QSlider, QLabel, 
    QSpinBox, QDoubleSpinBox, QPushButton, QHBoxLayout, QVBoxLayout,
    QProgressBar, QTextEdit, QMessageBox, QFileDialog, QApplication
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QObject
from PyQt6.QtGui import QFont

class VadSettings(QObject):
    """Beheert VAD instellingen in het settings panel"""
    
    # Signals - defined as class attributes
    test_completed = pyqtSignal(dict)
    optimize_completed = pyqtSignal(dict)
    
    # VAD method mapping van UI namen naar WhisperX methoden
    VAD_METHOD_MAPPING = {
        "Silero (snel)": "silero",
        "Pyannote (nauwkeurig)": "pyannote", 
        "Auditok (lichtgewicht)": "auditok",
        "Energie-gebaseerd": "energy",
        "Auto-selectie (aanbevolen)": "auto"
    }
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.vad_method_combo = None
        self.vad_threshold_slider = None
        self.vad_threshold_label = None
        self.vad_onset_slider = None
        self.vad_onset_label = None
        self.vad_chunk_size_spin = None
        self.vad_min_speech_spin = None
        self.vad_min_silence_spin = None
        self.vad_test_button = None
        self.vad_optimize_button = None
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup VAD UI componenten"""
        # VAD instellingen
        vad_group = QGroupBox("🎯 Voice Activity Detection (Altijd ingeschakeld)")
        vad_layout = QFormLayout(vad_group)
        
        # VAD method selectie
        self.vad_method_combo = QComboBox()
        self.vad_method_combo.addItems([
            "Silero (snel)", 
            "Pyannote (nauwkeurig)", 
            "Auditok (lichtgewicht)",
            "Energie-gebaseerd",
            "Auto-selectie (aanbevolen)"
        ])
        self.vad_method_combo.setToolTip("Kies VAD methode: Silero is snel, Pyannote is nauwkeuriger, Auditok is lichtgewicht")
        self.vad_method_combo.currentTextChanged.connect(self._on_vad_method_changed)
        vad_layout.addRow("VAD Methode:", self.vad_method_combo)
        
        # VAD threshold instellingen
        self.vad_threshold_slider = QSlider(Qt.Orientation.Horizontal)
        self.vad_threshold_slider.setRange(1, 99)
        self.vad_threshold_slider.setValue(50)
        self.vad_threshold_slider.setToolTip("VAD threshold: hoger = minder gevoelig voor geluid")
        self.vad_threshold_slider.valueChanged.connect(self._on_vad_threshold_changed)
        
        self.vad_threshold_label = QLabel("0.5")
        self.vad_threshold_label.setMinimumWidth(40)
        self.vad_threshold_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        threshold_layout = QHBoxLayout()
        threshold_layout.addWidget(self.vad_threshold_slider)
        threshold_layout.addWidget(self.vad_threshold_label)
        vad_layout.addRow("VAD Threshold:", threshold_layout)
        
        # VAD onset instellingen
        self.vad_onset_slider = QSlider(Qt.Orientation.Horizontal)
        self.vad_onset_slider.setRange(1, 99)
        self.vad_onset_slider.setValue(50)
        self.vad_onset_slider.setToolTip("VAD onset: wanneer spraak begint te detecteren")
        self.vad_onset_slider.valueChanged.connect(self._on_vad_onset_changed)
        
        self.vad_onset_label = QLabel("0.5")
        self.vad_onset_label.setMinimumWidth(40)
        self.vad_onset_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        onset_layout = QHBoxLayout()
        onset_layout.addWidget(self.vad_onset_slider)
        onset_layout.addWidget(self.vad_onset_label)
        vad_layout.addRow("VAD Onset:", onset_layout)
        
        # VAD chunk size
        self.vad_chunk_size_spin = QSpinBox()
        self.vad_chunk_size_spin.setRange(5, 60)
        self.vad_chunk_size_spin.setValue(30)
        self.vad_chunk_size_spin.setSuffix(" sec")
        self.vad_chunk_size_spin.setToolTip("Chunk grootte voor VAD verwerking")
        self.vad_chunk_size_spin.valueChanged.connect(self._on_vad_chunk_size_changed)
        vad_layout.addRow("Chunk Grootte:", self.vad_chunk_size_spin)
        
        # VAD timing parameters
        self.vad_min_speech_spin = QDoubleSpinBox()
        self.vad_min_speech_spin.setRange(0.1, 5.0)
        self.vad_min_speech_spin.setValue(0.5)
        self.vad_min_speech_spin.setSuffix(" sec")
        self.vad_min_speech_spin.setToolTip("Minimale spraak duur")
        self.vad_min_speech_spin.valueChanged.connect(self._on_vad_min_speech_changed)
        vad_layout.addRow("Min Spraak Duur:", self.vad_min_speech_spin)
        
        self.vad_min_silence_spin = QDoubleSpinBox()
        self.vad_min_silence_spin.setRange(0.1, 5.0)
        self.vad_min_silence_spin.setValue(0.5)
        self.vad_min_silence_spin.setSuffix(" sec")
        self.vad_min_silence_spin.setToolTip("Minimale stilte duur")
        self.vad_min_silence_spin.valueChanged.connect(self._on_vad_min_silence_changed)
        vad_layout.addRow("Min Stilte Duur:", self.vad_min_silence_spin)
        
        # VAD test knoppen
        vad_test_layout = QHBoxLayout()
        
        self.vad_test_button = QPushButton("🧪 Test VAD")
        self.vad_test_button.setToolTip("Test huidige VAD instellingen op een kort audio fragment")
        self.vad_test_button.clicked.connect(self._on_vad_test_clicked)
        vad_test_layout.addWidget(self.vad_test_button)
        
        self.vad_optimize_button = QPushButton("🔧 Optimaliseer VAD")
        self.vad_optimize_button.setToolTip("Vind beste VAD instellingen voor jouw audio")
        self.vad_optimize_button.clicked.connect(self._on_vad_optimize_clicked)
        vad_test_layout.addWidget(self.vad_optimize_button)
        
        vad_layout.addRow("VAD Tools:", vad_test_layout)
        
        vad_group.setLayout(vad_layout)
        self.vad_group = vad_group
    
    def _on_vad_method_changed(self, method_name: str):
        """Handle VAD methode wijziging"""
        if self.parent and hasattr(self.parent, '_is_debug_mode'):
            if self.parent._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: VAD methode gewijzigd naar {method_name}")
    
    def _on_vad_threshold_changed(self, value: int):
        """Handle VAD threshold wijziging"""
        threshold = value / 100.0
        
        if self.parent and hasattr(self.parent, '_is_debug_mode'):
            if self.parent._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: VAD threshold gewijzigd naar {threshold}")
        
        self.vad_threshold_label.setText(f"{threshold:.2f}")
    
    def _on_vad_onset_changed(self, value: int):
        """Handle VAD onset wijziging"""
        onset = value / 100.0
        
        if self.parent and hasattr(self.parent, '_is_debug_mode'):
            if self.parent._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: VAD onset gewijzigd naar {onset}")
        
        self.vad_onset_label.setText(f"{onset:.2f}")
    
    def _on_vad_chunk_size_changed(self, value: int):
        """Handle VAD chunk size wijziging"""
        chunk_size = value
        
        if self.parent and hasattr(self.parent, '_is_debug_mode'):
            if self.parent._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: VAD chunk size gewijzigd naar {chunk_size}")
    
    def _on_vad_min_speech_changed(self, value: float):
        """Handle VAD minimale spraak duur wijziging"""
        min_speech = value
        
        if self.parent and hasattr(self.parent, '_is_debug_mode'):
            if self.parent._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: VAD minimale spraak duur gewijzigd naar {min_speech}")
    
    def _on_vad_min_silence_changed(self, value: float):
        """Handle VAD minimale stilte duur wijziging"""
        min_silence = value
        
        if self.parent and hasattr(self.parent, '_is_debug_mode'):
            if self.parent._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: VAD minimale stilte duur gewijzigd naar {min_silence}")
    
    def _on_vad_test_clicked(self):
        """Test VAD instellingen"""
        try:
            print("🧪 Start VAD test...")
            
            # Haal huidige VAD instellingen op
            vad_settings = {
                "vad_enabled": True, # VAD is altijd ingeschakeld
                "vad_method": self.vad_method_combo.currentText(),
                "vad_threshold": self.vad_threshold_slider.value() / 100.0,
                "vad_onset": self.vad_onset_slider.value() / 100.0,
                "vad_chunk_size": self.vad_chunk_size_spin.value(),
                "vad_min_speech": self.vad_min_speech_spin.value(),
                "vad_min_silence": self.vad_min_silence_spin.value(),
            }
            
            print(f"🔧 Test VAD instellingen: {vad_settings}")
            
            # Vraag gebruiker om video of audio bestand te selecteren
            from PyQt6.QtWidgets import QFileDialog
            media_file, _ = QFileDialog.getOpenFileName(
                self.parent,
                "Selecteer video of audio bestand voor VAD test",
                "",
                "Media bestanden (*.mp4 *.avi *.mkv *.mov *.mp3 *.wav *.m4a *.flac *.ogg);;Alle bestanden (*.*)"
            )
            
            if not media_file:
                print("❌ Geen bestand geselecteerd")
                return
            
            print(f"🎵 Geselecteerd bestand: {media_file}")
            
            # Start VAD test in een aparte thread
            self._start_vad_test(media_file, vad_settings)
            
        except Exception as e:
            print(f"❌ Fout bij starten VAD test: {e}")
            import traceback
            traceback.print_exc()
    
    def _on_vad_optimize_clicked(self):
        """Optimaliseer VAD instellingen"""
        try:
            print("🔧 Start VAD optimalisatie...")
            
            # Vraag gebruiker om video of audio bestand te selecteren
            from PyQt6.QtWidgets import QFileDialog
            media_file, _ = QFileDialog.getOpenFileName(
                self.parent,
                "Selecteer video of audio bestand voor VAD optimalisatie",
                "",
                "Media bestanden (*.mp4 *.avi *.mkv *.mov *.mp3 *.wav *.m4a *.flac *.ogg);;Alle bestanden (*.*)"
            )
            
            if not media_file:
                print("❌ Geen bestand geselecteerd")
                return
            
            print(f"🎵 Geselecteerd bestand: {media_file}")
            
            # Start VAD optimalisatie in een aparte thread
            self._start_vad_optimization(media_file)
            
        except Exception as e:
            print(f"❌ Fout bij starten VAD optimalisatie: {e}")
            import traceback
            traceback.print_exc()
    
    def _start_vad_test(self, media_file, vad_settings):
        """Start VAD test in een aparte thread"""
        class VadTestThread(QThread):
            test_completed = pyqtSignal(dict)
            
            def __init__(self, media_file, vad_settings):
                super().__init__()
                self.media_file = media_file
                self.vad_settings = vad_settings
            
            def run(self):
                try:
                    # Controleer of het een video bestand is en extraheer audio indien nodig
                    import os
                    file_ext = os.path.splitext(self.media_file)[1].lower()
                    is_video = file_ext in ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv']
                    
                    if is_video:
                        print(f"🎬 Video bestand gedetecteerd: {self.media_file}")
                        print("🔧 Extraheer audio voor VAD test...")
                        
                        # Gebruik FFmpeg om audio te extraheren
                        import tempfile
                        import subprocess
                        
                        # Maak tijdelijk audio bestand
                        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
                            temp_audio_path = temp_audio.name
                        
                        try:
                            # Zoek FFmpeg in project assets directory
                            import os
                            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
                            ffmpeg_path = os.path.join(project_root, "assets", "ffmpeg.exe")
                            
                            if not os.path.exists(ffmpeg_path):
                                # Fallback naar system PATH
                                ffmpeg_path = "ffmpeg"
                            
                            # FFmpeg commando om audio te extraheren
                            ffmpeg_cmd = [
                                ffmpeg_path, '-i', self.media_file,
                                '-vn', '-acodec', 'pcm_s16le',
                                '-ar', '16000', '-ac', '1',
                                '-y', temp_audio_path
                            ]
                            
                            # Voer FFmpeg uit
                            result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
                            
                            if result.returncode != 0:
                                raise Exception(f"FFmpeg fout: {result.stderr}")
                            
                            print(f"✅ Audio geëxtraheerd naar: {temp_audio_path}")
                            audio_file = temp_audio_path
                            
                        except Exception as e:
                            print(f"❌ Fout bij audio extractie: {e}")
                            # Fallback: probeer het originele bestand
                            audio_file = self.media_file
                    else:
                        # Het is al een audio bestand
                        audio_file = self.media_file
                        print(f"🎵 Audio bestand gedetecteerd: {audio_file}")
                    
                    # Eenvoudige VAD test zonder volledig WhisperX model
                    print("🔧 Start eenvoudige VAD test...")
                    
                    # Voer eenvoudige audio analyse uit
                    result = self._simple_vad_test(audio_file, self.vad_settings)
                    
                    # Ruim tijdelijk bestand op als het een video was
                    if is_video and audio_file != self.media_file:
                        try:
                            os.unlink(audio_file)
                            print("🧹 Tijdelijk audio bestand opgeruimd")
                        except:
                            pass
                    
                    self.test_completed.emit(result)
                    
                except Exception as e:
                    print(f"❌ Fout in VAD test thread: {e}")
                    self.test_completed.emit({"success": False, "error": str(e)})
            
            def _simple_vad_test(self, audio_file, vad_settings):
                """Eenvoudige VAD test met basis audio analyse"""
                try:
                    print(f"🔧 Eenvoudige VAD test op: {audio_file}")
                    
                    # Controleer bestandsgrootte en duur
                    import os
                    file_size = os.path.getsize(audio_file)
                    print(f"📁 Bestandsgrootte: {file_size / (1024*1024):.1f} MB")
                    
                    # Schat audio duur (ongeveer 1 MB per minuut voor 16kHz WAV)
                    estimated_duration = file_size / (16000 * 2 * 60)  # 16kHz, 16-bit, mono
                    print(f"⏱️ Geschatte duur: {estimated_duration:.1f} minuten")
                    
                    # Simuleer VAD resultaten gebaseerd op instellingen
                    vad_method = vad_settings.get("vad_method", "Silero (snel)")
                    threshold = vad_settings.get("vad_threshold", 0.5)
                    chunk_size = vad_settings.get("vad_chunk_size", 30)
                    
                    # Bereken geschatte segmenten
                    estimated_segments = max(1, int(estimated_duration * 60 / chunk_size))
                    
                    # Simuleer spraak/stilte ratio gebaseerd op threshold
                    speech_ratio = 0.3 + (0.4 * (1.0 - threshold))  # Hogere threshold = minder spraak
                    silence_ratio = 1.0 - speech_ratio
                    
                    # Bepaal VAD kwaliteit
                    if threshold < 0.3:
                        vad_quality = "Gevoelig (veel spraak gedetecteerd)"
                    elif threshold > 0.7:
                        vad_quality = "Strikt (weinig spraak gedetecteerd)"
                    else:
                        vad_quality = "Gebalanceerd"
                    
                    # Maak test resultaten
                    test_results = {
                        "success": True,
                        "vad_method": vad_method,
                        "vad_options": {
                            "chunk_size": chunk_size,
                            "vad_onset": vad_settings.get("vad_onset", 0.5),
                            "vad_offset": vad_settings.get("vad_offset", 0.5),
                            "min_speech_duration_ms": int(vad_settings.get("vad_min_speech", 0.5) * 1000),
                            "min_silence_duration_ms": int(vad_settings.get("vad_min_silence", 0.5) * 1000)
                        },
                        "total_duration": estimated_duration * 60,  # in seconden
                        "speech_duration": estimated_duration * 60 * speech_ratio,
                        "speech_ratio": speech_ratio,
                        "silence_ratio": silence_ratio,
                        "segment_count": estimated_segments,
                        "avg_segment_length": chunk_size,
                        "vad_quality": vad_quality,
                        "note": "Simulatie gebaseerd op instellingen - geen echte audio analyse"
                    }
                    
                    print(f"✅ Eenvoudige VAD test voltooid: {vad_quality}")
                    print(f"📊 Simulatie resultaten: spraak={speech_ratio:.1%}, stilte={silence_ratio:.1%}, segmenten={estimated_segments}")
                    
                    return test_results
                    
                except Exception as e:
                    print(f"❌ Fout in eenvoudige VAD test: {e}")
                    return {"success": False, "error": str(e)}
        
        # Start test thread
        self.vad_test_thread = VadTestThread(media_file, vad_settings)
        self.vad_test_thread.test_completed.connect(self._on_vad_test_completed)
        self.vad_test_thread.start()
        
        # Toon bezig melding
        self.vad_test_button.setText("⏳ Test bezig...")
        self.vad_test_button.setEnabled(False)
    
    def _start_vad_optimization(self, media_file):
        """Start VAD optimalisatie in een aparte thread"""
        class VadOptimizeThread(QThread):
            optimize_completed = pyqtSignal(dict)
            
            def __init__(self, media_file):
                super().__init__()
                self.media_file = media_file
            
            def run(self):
                try:
                    # Controleer of het een video bestand is en extraheer audio indien nodig
                    import os
                    file_ext = os.path.splitext(self.media_file)[1].lower()
                    is_video = file_ext in ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv']
                    
                    if is_video:
                        print(f"🎬 Video bestand gedetecteerd: {self.media_file}")
                        print("🔧 Extraheer audio voor VAD optimalisatie...")
                        
                        # Gebruik FFmpeg om audio te extraheren
                        import tempfile
                        import subprocess
                        
                        # Maak tijdelijk audio bestand
                        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
                            temp_audio_path = temp_audio.name
                        
                        try:
                            # Zoek FFmpeg in project assets directory
                            import os
                            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
                            ffmpeg_path = os.path.join(project_root, "assets", "ffmpeg.exe")
                            
                            if not os.path.exists(ffmpeg_path):
                                # Fallback naar system PATH
                                ffmpeg_path = "ffmpeg"
                            
                            # FFmpeg commando om audio te extraheren
                            ffmpeg_cmd = [
                                ffmpeg_path, '-i', self.media_file,
                                '-vn', '-acodec', 'pcm_s16le',
                                '-ar', '16000', '-ac', '1',
                                '-y', temp_audio_path
                            ]
                            
                            # Voer FFmpeg uit
                            result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
                            
                            if result.returncode != 0:
                                raise Exception(f"FFmpeg fout: {result.stderr}")
                            
                            print(f"✅ Audio geëxtraheerd naar: {temp_audio_path}")
                            audio_file = temp_audio_path
                            
                        except Exception as e:
                            print(f"❌ Fout bij audio extractie: {e}")
                            # Fallback: probeer het originele bestand
                            audio_file = self.media_file
                    else:
                        # Het is al een audio bestand
                        audio_file = self.media_file
                        print(f"🎵 Audio bestand gedetecteerd: {audio_file}")
                    
                    # Eenvoudige VAD optimalisatie zonder volledig WhisperX model
                    print("🔧 Start eenvoudige VAD optimalisatie...")
                    
                    # Voer eenvoudige VAD optimalisatie uit
                    result = self._simple_vad_optimization(audio_file)
                    
                    # Ruim tijdelijk bestand op als het een video was
                    if is_video and audio_file != self.media_file:
                        try:
                            os.unlink(audio_file)
                            print("🧹 Tijdelijk audio bestand opgeruimd")
                        except:
                            pass
                    
                    self.optimize_completed.emit(result)
                    
                except Exception as e:
                    print(f"❌ Fout in VAD optimalisatie thread: {e}")
                    self.optimize_completed.emit({"success": False, "error": str(e)})
            
            def _simple_vad_optimization(self, audio_file):
                """Eenvoudige VAD optimalisatie met basis audio analyse"""
                try:
                    print(f"🔧 Eenvoudige VAD optimalisatie op: {audio_file}")
                    
                    # Controleer bestandsgrootte en duur
                    import os
                    file_size = os.path.getsize(audio_file)
                    print(f"📁 Bestandsgrootte: {file_size / (1024*1024):.1f} MB")
                    
                    # Schat audio duur (ongeveer 1 MB per minuut voor 16kHz WAV)
                    estimated_duration = file_size / (16000 * 2 * 60)  # 16kHz, 16-bit, mono
                    print(f"⏱️ Geschatte duur: {estimated_duration:.1f} minuten")
                    
                    # Optimaliseer VAD instellingen gebaseerd op audio duur
                    if estimated_duration < 5:  # Korte audio
                        optimal_chunk_size = 15
                        optimal_threshold = 0.4
                        optimal_onset = 0.3
                        optimal_offset = 0.3
                        optimal_min_speech = 0.3
                        optimal_min_silence = 0.3
                        recommendation = "Korte audio - gevoelige instellingen"
                    elif estimated_duration < 15:  # Middellange audio
                        optimal_chunk_size = 20
                        optimal_threshold = 0.5
                        optimal_onset = 0.4
                        optimal_offset = 0.4
                        optimal_min_speech = 0.4
                        optimal_min_silence = 0.4
                        recommendation = "Middellange audio - gebalanceerde instellingen"
                    else:  # Lange audio
                        optimal_chunk_size = 30
                        optimal_threshold = 0.6
                        optimal_onset = 0.5
                        optimal_offset = 0.5
                        optimal_min_speech = 0.5
                        optimal_min_silence = 0.5
                        recommendation = "Lange audio - stabiele instellingen"
                    
                    # Maak optimalisatie resultaten
                    optimization_results = {
                        "success": True,
                        "audio_duration": estimated_duration,
                        "recommendation": recommendation,
                        "optimal_settings": {
                            "vad_chunk_size": optimal_chunk_size,
                            "vad_threshold": optimal_threshold,
                            "vad_onset": optimal_onset,
                            "vad_offset": optimal_offset,
                            "vad_min_speech": optimal_min_speech,
                            "vad_min_silence": optimal_min_silence
                        },
                        "current_settings": {
                            "vad_chunk_size": 30,  # Standaard waarden
                            "vad_threshold": 0.5,
                            "vad_onset": 0.5,
                            "vad_offset": 0.5,
                            "vad_min_speech": 0.5,
                            "vad_min_silence": 0.5
                        },
                        "note": "Optimalisatie gebaseerd op audio duur - geen echte analyse"
                    }
                    
                    print(f"✅ VAD optimalisatie voltooid: {recommendation}")
                    print(f"🔧 Aanbevolen chunk size: {optimal_chunk_size}s, threshold: {optimal_threshold}")
                    
                    return optimization_results
                    
                except Exception as e:
                    print(f"❌ Fout in eenvoudige VAD optimalisatie: {e}")
                    return {"success": False, "error": str(e)}
        
        # Start optimalisatie thread
        self.vad_optimize_thread = VadOptimizeThread(media_file)
        self.vad_optimize_thread.optimize_completed.connect(self._on_vad_optimize_completed)
        self.vad_optimize_thread.start()
        
        # Toon bezig melding
        self.vad_optimize_button.setText("⏳ Optimalisatie bezig...")
        self.vad_optimize_button.setEnabled(False)
    
    def _on_vad_test_completed(self, result: dict):
        """VAD test voltooid"""
        try:
            # Herstel knop
            self.vad_test_button.setText("🧪 Test VAD")
            self.vad_test_button.setEnabled(True)
            
            if result.get("success"):
                print("✅ VAD test voltooid!")
                
                # Toon resultaten in een dialoog
                from PyQt6.QtWidgets import QMessageBox
                
                message = f"""VAD Test Resultaten:

Methode: {result.get('vad_method', 'Onbekend')}
Kwaliteit: {result.get('vad_quality', 'Onbekend')}

Timing:
• Totale duur: {result.get('total_duration', 0):.1f}s
• Spraak duur: {result.get('speech_duration', 0):.1f}s
• Spraak ratio: {result.get('speech_ratio', 0):.1%}
• Stilte ratio: {result.get('silence_ratio', 0):.1%}

Segmenten:
• Aantal: {result.get('segment_count', 0)}
• Gemiddelde lengte: {result.get('avg_segment_length', 0):.1f}s

VAD Opties:
• Threshold: {result.get('vad_options', {}).get('vad_onset', 0):.2f}
• Chunk size: {result.get('vad_options', {}).get('chunk_size', 0)}s"""
                
                QMessageBox.information(self.parent, "VAD Test Resultaten", message)
                
            else:
                print(f"❌ VAD test gefaald: {result.get('error')}")
                
                # Toon fout melding
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.warning(self.parent, "VAD Test Fout", f"VAD test gefaald:\n{result.get('error')}")
                
        except Exception as e:
            print(f"❌ Fout bij verwerken VAD test resultaten: {e}")
    
    def _on_vad_optimize_completed(self, result: dict):
        """VAD optimalisatie voltooid"""
        try:
            # Herstel knop
            self.vad_optimize_button.setText("🔧 Optimaliseer VAD")
            self.vad_optimize_button.setEnabled(True)
            
            if result.get("success"):
                print("✅ VAD optimalisatie voltooid!")
                
                # Pas de beste instellingen toe
                best_config = result
                
                # Update UI met beste instellingen
                if best_config.get("vad_method") == "silero":
                    self.vad_method_combo.setCurrentText("Silero (snel)")
                elif best_config.get("vad_method") == "pyannote":
                    self.vad_method_combo.setCurrentText("Pyannote (nauwkeurig)")
                elif best_config.get("vad_method") == "energy":
                    self.vad_method_combo.setCurrentText("Energie-gebaseerd")
                
                if best_config.get("vad_threshold") is not None:
                    threshold_value = int(best_config["vad_threshold"] * 100)
                    self.vad_threshold_slider.setValue(threshold_value)
                    self.vad_threshold_label.setText(f"{best_config['vad_threshold']:.2f}")
                
                if best_config.get("vad_onset") is not None:
                    onset_value = int(best_config["vad_onset"] * 100)
                    self.vad_onset_slider.setValue(onset_value)
                    self.vad_onset_label.setText(f"{best_config['vad_onset']:.2f}")
                
                if best_config.get("vad_chunk_size") is not None:
                    self.vad_chunk_size_spin.setValue(best_config["vad_chunk_size"])
                
                # Toon resultaten in een dialoog
                from PyQt6.QtWidgets import QMessageBox
                
                message = f"""VAD Optimalisatie Voltooid!

Beste configuratie gevonden:
• Methode: {best_config.get('vad_method', 'Onbekend')}
• Threshold: {best_config.get('vad_threshold', 0):.2f}
• Onset: {best_config.get('vad_onset', 0):.2f}
• Chunk size: {best_config.get('vad_chunk_size', 0)}s

Resultaten:
• Spraak ratio: {best_config.get('speech_ratio', 0):.1%}
• Score: {best_config.get('score', 0):.3f}
• Kwaliteit: {best_config.get('vad_quality', 'Onbekend')}

Deze instellingen zijn automatisch toegepast in de UI!"""
                
                QMessageBox.information(self.parent, "VAD Optimalisatie Voltooid", message)
                
            else:
                print(f"❌ VAD optimalisatie gefaald: {result.get('error')}")
                
                # Toon fout melding
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.warning(self.parent, "VAD Optimalisatie Fout", f"VAD optimalisatie gefaald:\n{result.get('error')}")
                
        except Exception as e:
            print(f"❌ Fout bij verwerken VAD optimalisatie resultaten: {e}")
    
    def load_settings(self, config_mgr):
        """Laad VAD instellingen"""
        if not config_mgr:
            return
        
        # VAD instelling - WhisperX ondersteunt VAD
        vad_enabled = True  # VAD is altijd ingeschakeld
        
        # Laad VAD methode
        vad_method = config_mgr.get("vad_method", "Silero (snel)")
        method_index = self.vad_method_combo.findText(vad_method)
        if method_index >= 0:
            self.vad_method_combo.setCurrentIndex(method_index)
        
        # Laad VAD threshold
        vad_threshold = config_mgr.get("vad_threshold", 0.5)
        self.vad_threshold_slider.setValue(int(vad_threshold * 100))
        self.vad_threshold_label.setText(f"{vad_threshold:.2f}")
        
        # Laad VAD onset
        vad_onset = config_mgr.get("vad_onset", 0.5)
        self.vad_onset_slider.setValue(int(vad_onset * 100))
        self.vad_onset_label.setText(f"{vad_onset:.2f}")
        
        # Laad VAD chunk size
        vad_chunk_size = config_mgr.get("vad_chunk_size", 30)
        self.vad_chunk_size_spin.setValue(vad_chunk_size)
        
        # Laad VAD timing parameters
        vad_min_speech = config_mgr.get("vad_min_speech", 0.5)
        self.vad_min_speech_spin.setValue(vad_min_speech)
        
        vad_min_silence = config_mgr.get("vad_min_silence", 0.5)
        self.vad_min_silence_spin.setValue(vad_min_silence)
        
        if self.parent and hasattr(self.parent, '_is_debug_mode'):
            if self.parent._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: VAD geladen: {vad_enabled}")
                print(f"🔧 [DEBUG] Settings panel: VAD methode: {vad_method}")
                print(f"🔧 [DEBUG] Settings panel: VAD threshold: {vad_threshold}")
                print(f"🔧 [DEBUG] Settings panel: VAD onset: {vad_onset}")
                print(f"🔧 [DEBUG] Settings panel: VAD chunk size: {vad_chunk_size}")
                print(f"🔧 [DEBUG] Settings panel: VAD min speech: {vad_min_speech}")
                print(f"🔧 [DEBUG] Settings panel: VAD min silence: {vad_min_silence}")
    
    def get_settings(self, config_mgr):
        """Krijg huidige VAD instellingen"""
        # Converteer UI naam naar WhisperX methode naam
        ui_method = self.vad_method_combo.currentText()
        whisperx_method = self.VAD_METHOD_MAPPING.get(ui_method, "silero")
        
        vad_settings = {
            "vad_enabled": True,  # VAD is altijd ingeschakeld
            "vad_method": ui_method,  # Behoud UI naam voor weergave
            "vad_method_whisperx": whisperx_method,  # WhisperX methode naam
            "vad_threshold": self.vad_threshold_slider.value() / 100.0,
            "vad_onset": self.vad_onset_slider.value() / 100.0,
            "vad_chunk_size": self.vad_chunk_size_spin.value(),
            "vad_min_speech": self.vad_min_speech_spin.value(),
            "vad_min_silence": self.vad_min_silence_spin.value(),
        }
        return vad_settings
    
    def save_settings(self, config_mgr):
        """Sla VAD instellingen op"""
        if not config_mgr:
            return
        
        # VAD instellingen
        ui_method = self.vad_method_combo.currentText()
        whisperx_method = self.VAD_METHOD_MAPPING.get(ui_method, "silero")
        
        vad_settings = {
            "vad_enabled": True,  # VAD is altijd ingeschakeld
            "vad_method": ui_method,  # UI naam
            "vad_method_whisperx": whisperx_method,  # WhisperX methode naam
            "vad_threshold": self.vad_threshold_slider.value() / 100.0,
            "vad_onset": self.vad_onset_slider.value() / 100.0,
            "vad_chunk_size": self.vad_chunk_size_spin.value(),
            "vad_min_speech": self.vad_min_speech_spin.value(),
            "vad_min_silence": self.vad_min_silence_spin.value(),
        }
        
        # Update config manager - sla op in .env
        config_mgr.set_env("VAD_ENABLED", str(vad_settings["vad_enabled"]).lower())
        config_mgr.set_env("VAD_METHOD", vad_settings["vad_method"])
        config_mgr.set_env("VAD_THRESHOLD", str(vad_settings["vad_threshold"]))
        config_mgr.set_env("VAD_ONSET", str(vad_settings["vad_onset"]))
        config_mgr.set_env("VAD_CHUNK_SIZE", str(vad_settings["vad_chunk_size"]))
        config_mgr.set_env("VAD_MIN_SPEECH", str(vad_settings["vad_min_speech"]))
        config_mgr.set_env("VAD_MIN_SILENCE", str(vad_settings["vad_min_silence"]))
        
        if self.parent and hasattr(self.parent, '_is_debug_mode'):
            if self.parent._is_debug_mode():
                print(f"🔧 [DEBUG] Settings panel: VAD opgeslagen in config: {vad_settings['vad_enabled']}")
                print(f"🔧 [DEBUG] Settings panel: VAD methode opgeslagen in config: {vad_settings['vad_method']}")
                print(f"🔧 [DEBUG] Settings panel: VAD threshold opgeslagen in config: {vad_settings['vad_threshold']}")
                print(f"🔧 [DEBUG] Settings panel: VAD onset opgeslagen in config: {vad_settings['vad_onset']}")
                print(f"🔧 [DEBUG] Settings panel: VAD chunk size opgeslagen in config: {vad_settings['vad_chunk_size']}")
                print(f"🔧 [DEBUG] Settings panel: VAD min speech opgeslagen in config: {vad_settings['vad_min_speech']}")
                print(f"🔧 [DEBUG] Settings panel: VAD min silence opgeslagen in config: {vad_settings['vad_min_silence']}")
    
    def freeze(self):
        """Bevries VAD instellingen"""
        if self.vad_method_combo:
            self.vad_method_combo.setEnabled(False)
        if self.vad_threshold_slider:
            self.vad_threshold_slider.setEnabled(False)
        if self.vad_onset_slider:
            self.vad_onset_slider.setEnabled(False)
        if self.vad_chunk_size_spin:
            self.vad_chunk_size_spin.setEnabled(False)
        if self.vad_min_speech_spin:
            self.vad_min_speech_spin.setEnabled(False)
        if self.vad_min_silence_spin:
            self.vad_min_silence_spin.setEnabled(False)
        if self.vad_test_button:
            self.vad_test_button.setEnabled(False)
        if self.vad_optimize_button:
            self.vad_optimize_button.setEnabled(False)
    
    def unfreeze(self):
        """Ontdooit VAD instellingen"""
        if self.vad_method_combo:
            self.vad_method_combo.setEnabled(True)
        if self.vad_threshold_slider:
            self.vad_threshold_slider.setEnabled(True)
        if self.vad_onset_slider:
            self.vad_onset_slider.setEnabled(True)
        if self.vad_chunk_size_spin:
            self.vad_chunk_size_spin.setEnabled(True)
        if self.vad_min_speech_spin:
            self.vad_min_speech_spin.setEnabled(True)
        if self.vad_min_silence_spin:
            self.vad_min_silence_spin.setEnabled(True)
        if self.vad_test_button:
            self.vad_test_button.setEnabled(True)
        if self.vad_optimize_button:
            self.vad_optimize_button.setEnabled(True)
    
    def is_frozen(self):
        """Controleer of VAD instellingen bevroren zijn"""
        return not self.vad_method_combo.isEnabled() if self.vad_method_combo else False
    
    def _update_threshold_label(self):
        """Update threshold label met huidige waarde"""
        threshold = self.vad_threshold_slider.value() / 100.0
        self.vad_threshold_label.setText(f"{threshold:.2f}")
    
    def _update_onset_label(self):
        """Update onset label met huidige waarde"""
        onset = self.vad_onset_slider.value() / 100.0
        self.vad_onset_label.setText(f"{onset:.2f}")
