"""
Audio Analyzer Plugin voor Magic Time Studio
Toont spectrogrammen en frequentie analyse van audio bestanden
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFileDialog, QGroupBox, QComboBox,
    QSpinBox, QCheckBox, QProgressBar, QTextEdit
)
from PySide6.QtCore import Qt, Signal, QThread
import librosa
import librosa.display

from magic_time_studio.ui_pyside6.features.plugin_manager import PluginBase

class AudioAnalysisThread(QThread):
    """Thread voor audio analyse"""
    analysis_complete = Signal(dict)
    progress_updated = Signal(int, str)
    error_occurred = Signal(str)
    
    def __init__(self, audio_path: str, analysis_type: str, settings: dict):
        super().__init__()
        self.audio_path = audio_path
        self.analysis_type = analysis_type
        self.settings = settings
        
    def run(self):
        """Voer audio analyse uit"""
        try:
            self.progress_updated.emit(10, "Audio laden...")
            
            # Laad audio
            y, sr = librosa.load(self.audio_path, sr=None)
            
            self.progress_updated.emit(30, "Analyseren...")
            
            results = {}
            
            if self.analysis_type == "Mel Spectrogram":
                mel_spec = librosa.feature.melspectrogram(y=y, sr=sr)
                mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
                results['mel_spectrogram'] = mel_spec_db
                results['sample_rate'] = sr
                
            elif self.analysis_type == "Linear Spectrogram":
                D = librosa.stft(y)
                S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
                results['linear_spectrogram'] = S_db
                results['sample_rate'] = sr
                
            elif self.analysis_type == "Chroma":
                chroma = librosa.feature.chroma_stft(y=y, sr=sr)
                results['chroma'] = chroma
                results['sample_rate'] = sr
                
            elif self.analysis_type == "MFCC":
                mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
                results['mfcc'] = mfcc
                results['sample_rate'] = sr
                
            elif self.analysis_type == "Spectral Centroid":
                spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
                results['spectral_centroids'] = spectral_centroids
                results['sample_rate'] = sr
                
            elif self.analysis_type == "Spectral Rolloff":
                spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
                results['spectral_rolloff'] = spectral_rolloff
                results['sample_rate'] = sr
                
            elif self.analysis_type == "Zero Crossing Rate":
                zero_crossing_rate = librosa.feature.zero_crossing_rate(y)[0]
                results['zero_crossing_rate'] = zero_crossing_rate
                results['sample_rate'] = sr
                
            elif self.analysis_type == "Complete Analysis":
                # Alle analyses tegelijk
                results['mel_spectrogram'] = librosa.power_to_db(
                    librosa.feature.melspectrogram(y=y, sr=sr), ref=np.max
                )
                results['chroma'] = librosa.feature.chroma_stft(y=y, sr=sr)
                results['mfcc'] = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
                results['spectral_centroids'] = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
                results['spectral_rolloff'] = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
                results['zero_crossing_rate'] = librosa.feature.zero_crossing_rate(y)[0]
                results['sample_rate'] = sr
            
            # Basis statistieken
            results['duration'] = len(y) / sr
            results['sample_rate'] = sr
            results['rms_energy'] = np.sqrt(np.mean(y**2))
            results['peak_amplitude'] = np.max(np.abs(y))
            
            self.progress_updated.emit(100, "Analyse voltooid!")
            self.analysis_complete.emit(results)
            
        except Exception as e:
            self.error_occurred.emit(str(e))

class AudioAnalyzerPlugin(PluginBase):
    """Verbeterde Audio Analyzer Plugin"""
    
    def __init__(self, main_window):
        super().__init__(main_window)
        self.name = "Advanced Audio Analyzer"
        self.version = "2.0.0"
        self.description = "Geavanceerde audio analyse met meerdere visualisaties"
        self.author = "Magic Time Studio"
        self.category = "Analysis"
        
        self.current_file = None
        self.audio_data = None
        self.sample_rate = None
        self.analysis_thread = None
        self.current_results = None
        
    def initialize(self) -> bool:
        """Initialiseer de plugin"""
        print(f"🔌 Advanced Audio Analyzer Plugin geïnitialiseerd: {self.name}")
        return True
    
    def cleanup(self):
        """Cleanup bij afsluiten"""
        print(f"🔌 Advanced Audio Analyzer Plugin cleanup: {self.name}")
        if self.analysis_thread and self.analysis_thread.isRunning():
            self.analysis_thread.quit()
            self.analysis_thread.wait()
    
    def get_widget(self) -> QWidget:
        """Retourneer plugin widget"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Titel
        title = QLabel("🎵 Advanced Audio Analyzer")
        title.setStyleSheet("font-weight: bold; font-size: 14px; color: #4caf50;")
        layout.addWidget(title)
        
        # Bestand selectie
        file_group = QGroupBox("📁 Audio Bestand")
        file_layout = QVBoxLayout(file_group)
        
        self.file_label = QLabel("Geen bestand geselecteerd")
        self.file_label.setStyleSheet("color: #888888;")
        file_layout.addWidget(self.file_label)
        
        file_btn_layout = QHBoxLayout()
        
        self.load_btn = QPushButton("📂 Laad Audio")
        self.load_btn.clicked.connect(self.load_audio_file)
        file_btn_layout.addWidget(self.load_btn)
        
        self.analyze_btn = QPushButton("🔍 Analyseer")
        self.analyze_btn.clicked.connect(self.analyze_audio)
        self.analyze_btn.setEnabled(False)
        file_btn_layout.addWidget(self.analyze_btn)
        
        file_layout.addLayout(file_btn_layout)
        layout.addWidget(file_group)
        
        # Analyse opties
        options_group = QGroupBox("⚙️ Analyse Opties")
        options_layout = QVBoxLayout(options_group)
        
        # Analyse type
        analysis_layout = QHBoxLayout()
        analysis_layout.addWidget(QLabel("Analyse Type:"))
        
        self.analysis_combo = QComboBox()
        self.analysis_combo.addItems([
            "Mel Spectrogram",
            "Linear Spectrogram", 
            "Chroma",
            "MFCC",
            "Spectral Centroid",
            "Spectral Rolloff",
            "Zero Crossing Rate",
            "Complete Analysis"
        ])
        analysis_layout.addWidget(self.analysis_combo)
        
        options_layout.addLayout(analysis_layout)
        
        # Geavanceerde opties
        advanced_layout = QHBoxLayout()
        
        self.show_stats_check = QCheckBox("Toon Statistieken")
        self.show_stats_check.setChecked(True)
        advanced_layout.addWidget(self.show_stats_check)
        
        self.save_plot_check = QCheckBox("Sla Plot Op")
        self.save_plot_check.setChecked(False)
        advanced_layout.addWidget(self.save_plot_check)
        
        options_layout.addLayout(advanced_layout)
        layout.addWidget(options_group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Resultaat gebied
        result_group = QGroupBox("📊 Resultaat")
        result_layout = QVBoxLayout(result_group)
        
        self.result_label = QLabel("Selecteer een audio bestand om te analyseren")
        self.result_label.setStyleSheet("color: #888888; font-style: italic;")
        result_layout.addWidget(self.result_label)
        
        # Statistieken text area
        self.stats_text = QTextEdit()
        self.stats_text.setMaximumHeight(100)
        self.stats_text.setReadOnly(True)
        self.stats_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 4px;
                font-family: 'Consolas', monospace;
                font-size: 10px;
            }
        """)
        result_layout.addWidget(self.stats_text)
        
        layout.addWidget(result_group)
        
        return widget
    
    def load_audio_file(self):
        """Laad audio bestand"""
        file_path, _ = QFileDialog.getOpenFileName(
            self.main_window,
            "Selecteer Audio Bestand",
            "",
            "Audio bestanden (*.mp3 *.wav *.m4a *.flac *.ogg *.aac)"
        )
        
        if file_path:
            try:
                # Laad audio met librosa
                self.audio_data, self.sample_rate = librosa.load(file_path, sr=None)
                self.current_file = file_path
                
                # Update UI
                self.file_label.setText(os.path.basename(file_path))
                self.file_label.setStyleSheet("color: #4caf50; font-weight: bold;")
                self.analyze_btn.setEnabled(True)
                
                # Toon basis info
                duration = len(self.audio_data) / self.sample_rate
                self.result_label.setText(
                    f"✅ Bestand geladen\n"
                    f"Duur: {duration:.2f} seconden\n"
                    f"Sample rate: {self.sample_rate} Hz\n"
                    f"Channels: Mono"
                )
                
            except Exception as e:
                self.result_label.setText(f"❌ Fout bij laden bestand: {e}")
    
    def analyze_audio(self):
        """Analyseer het geladen audio bestand"""
        if self.audio_data is None:
            return
        
        # Start analyse thread
        analysis_type = self.analysis_combo.currentText()
        settings = {
            "show_stats": self.show_stats_check.isChecked(),
            "save_plot": self.save_plot_check.isChecked()
        }
        
        self.analysis_thread = AudioAnalysisThread(
            self.current_file, analysis_type, settings
        )
        self.analysis_thread.analysis_complete.connect(self.on_analysis_complete)
        self.analysis_thread.progress_updated.connect(self.on_progress_update)
        self.analysis_thread.error_occurred.connect(self.on_analysis_error)
        
        self.analysis_thread.start()
        
        # Update UI
        self.analyze_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.result_label.setText("🔄 Analyseren...")
    
    def on_progress_update(self, value: int, message: str):
        """Update progress"""
        self.progress_bar.setValue(value)
        self.result_label.setText(message)
    
    def on_analysis_complete(self, results: dict):
        """Analyse voltooid"""
        self.current_results = results
        self.analyze_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        # Toon statistieken
        if self.show_stats_check.isChecked():
            stats_text = f"""
📊 Audio Statistieken:
├─ Duur: {results.get('duration', 0):.2f} seconden
├─ Sample Rate: {results.get('sample_rate', 0)} Hz
├─ RMS Energy: {results.get('rms_energy', 0):.4f}
├─ Peak Amplitude: {results.get('peak_amplitude', 0):.4f}
└─ Analyse Type: {self.analysis_combo.currentText()}
            """
            self.stats_text.setText(stats_text)
        
        # Maak en toon plot
        self.create_plot(results)
        
        self.result_label.setText(f"✅ {self.analysis_combo.currentText()} gegenereerd")
    
    def on_analysis_error(self, error: str):
        """Fout tijdens analyse"""
        self.analyze_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.result_label.setText(f"❌ Fout bij analyseren: {error}")
    
    def create_plot(self, results: dict):
        """Maak visualisatie plot"""
        try:
            analysis_type = self.analysis_combo.currentText()
            
            # Maak nieuwe figure
            fig, ax = plt.subplots(figsize=(10, 6))
            
            if analysis_type == "Mel Spectrogram":
                librosa.display.specshow(
                    results['mel_spectrogram'], 
                    sr=results['sample_rate'],
                    x_axis='time',
                    y_axis='mel',
                    ax=ax
                )
                ax.set_title('Mel Spectrogram')
                plt.colorbar(ax.images[0], ax=ax, format='%+2.0f dB')
                
            elif analysis_type == "Linear Spectrogram":
                librosa.display.specshow(
                    results['linear_spectrogram'],
                    sr=results['sample_rate'],
                    x_axis='time',
                    y_axis='hz',
                    ax=ax
                )
                ax.set_title('Linear Spectrogram')
                plt.colorbar(ax.images[0], ax=ax, format='%+2.0f dB')
                
            elif analysis_type == "Chroma":
                librosa.display.specshow(
                    results['chroma'],
                    sr=results['sample_rate'],
                    x_axis='time',
                    y_axis='chroma',
                    ax=ax
                )
                ax.set_title('Chroma Features')
                plt.colorbar(ax.images[0], ax=ax)
                
            elif analysis_type == "MFCC":
                librosa.display.specshow(
                    results['mfcc'],
                    sr=results['sample_rate'],
                    x_axis='time',
                    ax=ax
                )
                ax.set_title('MFCC Features')
                plt.colorbar(ax.images[0], ax=ax)
                
            elif analysis_type == "Spectral Centroid":
                times = librosa.times_like(results['spectral_centroids'])
                ax.plot(times, results['spectral_centroids'])
                ax.set_title('Spectral Centroid')
                ax.set_ylabel('Hz')
                ax.set_xlabel('Time')
                
            elif analysis_type == "Spectral Rolloff":
                times = librosa.times_like(results['spectral_rolloff'])
                ax.plot(times, results['spectral_rolloff'])
                ax.set_title('Spectral Rolloff')
                ax.set_ylabel('Hz')
                ax.set_xlabel('Time')
                
            elif analysis_type == "Zero Crossing Rate":
                times = librosa.times_like(results['zero_crossing_rate'])
                ax.plot(times, results['zero_crossing_rate'])
                ax.set_title('Zero Crossing Rate')
                ax.set_ylabel('Rate')
                ax.set_xlabel('Time')
                
            elif analysis_type == "Complete Analysis":
                # Subplot voor complete analyse
                fig, axes = plt.subplots(2, 2, figsize=(12, 8))
                
                # Mel spectrogram
                librosa.display.specshow(
                    results['mel_spectrogram'], 
                    sr=results['sample_rate'],
                    x_axis='time',
                    y_axis='mel',
                    ax=axes[0,0]
                )
                axes[0,0].set_title('Mel Spectrogram')
                
                # Chroma
                librosa.display.specshow(
                    results['chroma'],
                    sr=results['sample_rate'],
                    x_axis='time',
                    y_axis='chroma',
                    ax=axes[0,1]
                )
                axes[0,1].set_title('Chroma')
                
                # Spectral Centroid
                times = librosa.times_like(results['spectral_centroids'])
                axes[1,0].plot(times, results['spectral_centroids'])
                axes[1,0].set_title('Spectral Centroid')
                axes[1,0].set_ylabel('Hz')
                
                # Zero Crossing Rate
                times = librosa.times_like(results['zero_crossing_rate'])
                axes[1,1].plot(times, results['zero_crossing_rate'])
                axes[1,1].set_title('Zero Crossing Rate')
                axes[1,1].set_ylabel('Rate')
            
            # Sla plot op als gewenst
            if self.save_plot_check.isChecked():
                filename = f"audio_analysis_{analysis_type.lower().replace(' ', '_')}.png"
                plt.savefig(filename, dpi=300, bbox_inches='tight')
                self.result_label.setText(f"✅ Plot opgeslagen als {filename}")
            
            # Toon plot
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            self.result_label.setText(f"❌ Fout bij maken plot: {e}")
    
    def get_menu_items(self) -> list:
        """Retourneer menu items"""
        return [
            {
                "text": "Advanced Audio Analyzer",
                "action": self.show_analyzer,
                "shortcut": "Ctrl+Shift+A"
            }
        ]
    
    def show_analyzer(self):
        """Toon analyzer widget"""
        if hasattr(self, 'widget'):
            self.widget.show()
            self.widget.raise_() 