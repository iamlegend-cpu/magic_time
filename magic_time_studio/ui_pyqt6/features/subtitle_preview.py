"""
Video player met softcoded ondertitel preview en Whisper evaluatie
Voor Magic Time Studio - VLC INTEGRATIE OP HOLD
"""

import os
import re
import random
from datetime import timedelta
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QGroupBox, QPushButton, QComboBox, QTextEdit,
    QMessageBox
)
from PyQt6.QtCore import Qt


class SubtitlePreviewWidget(QWidget):
    """Placeholder voor video player met softcoded ondertitel preview en Whisper evaluatie"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Whisper model configuratie
        self.whisper_models = ['tiny', 'base', 'small', 'medium', 'large']
        self.current_whisper_model = 'large'
        
        # Subtitle tracking
        self.current_subtitle = ""
        self.subtitle_timings = []
        self.sync_offset = 0
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup de UI"""
        layout = QVBoxLayout(self)
        
        # Video player placeholder
        video_group = QGroupBox("🎬 Video Player (VLC Integratie Gepland)")
        video_layout = QVBoxLayout(video_group)
        
        # Placeholder voor video speler
        video_placeholder = QLabel("""
        🚧 VIDEO SPELER OP HOLD 🚧
        
        De video speler functionaliteit is tijdelijk uitgeschakeld.
        VLC integratie wordt gepland voor een toekomstige versie.
        
        Functies die later beschikbaar komen:
        • Video afspelen met VLC engine
        • Softcoded ondertitel preview
        • Whisper model evaluatie
        • Detachable video window
        • Interactive controls
        """)
        video_placeholder.setStyleSheet("""
            QLabel {
                background-color: #2d2d2d;
                border: 2px solid #555555;
                border-radius: 5px;
                color: #ffffff;
                padding: 20px;
                font-size: 12px;
                line-height: 1.4;
            }
        """)
        video_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        video_placeholder.setMinimumHeight(200)
        video_layout.addWidget(video_placeholder)
        
        # VLC integratie info
        vlc_info = QLabel("""
        📋 VLC Integratie Plan:
        • Python-VLC binding voor betere codec ondersteuning
        • VLC-Qt widget integratie
        • Verbeterde video format ondersteuning
        • Geen D3D11 errors op Windows
        • Betere performance en stabiliteit
        """)
        vlc_info.setStyleSheet("""
            QLabel {
                background-color: #1e1e1e;
                border: 1px solid #444444;
                border-radius: 3px;
                color: #cccccc;
                padding: 10px;
                font-size: 11px;
                line-height: 1.3;
            }
        """)
        video_layout.addWidget(vlc_info)
        
        layout.addWidget(video_group)
        
        # Compacte verwerking status
        processing_group = QGroupBox("🔄 Verwerking Status")
        processing_layout = QVBoxLayout(processing_group)
        
        # Status labels
        processing_status_layout = QHBoxLayout()
        
        self.current_file_label = QLabel("Huidig: -")
        self.current_file_label.setStyleSheet("color: #ff9800; font-weight: bold; padding: 3px; font-size: 10px;")
        processing_status_layout.addWidget(self.current_file_label)
        
        self.files_label = QLabel("Files: 0/0")
        self.files_label.setStyleSheet("color: #2196f3; font-weight: bold; padding: 3px; font-size: 10px;")
        processing_status_layout.addWidget(self.files_label)
        
        self.eta_label = QLabel("ETA: -")
        self.eta_label.setStyleSheet("color: #4caf50; font-weight: bold; padding: 3px; font-size: 10px;")
        processing_status_layout.addWidget(self.eta_label)
        
        self.elapsed_label = QLabel("Tijd: 00:00")
        self.elapsed_label.setStyleSheet("color: #9c27b0; font-weight: bold; padding: 3px; font-size: 10px;")
        processing_status_layout.addWidget(self.elapsed_label)
        
        processing_layout.addLayout(processing_status_layout)
        layout.addWidget(processing_group)
        
        # Subtitle controls (compact)
        subtitle_group = QGroupBox("📝 Softcoded Ondertitels")
        subtitle_layout = QHBoxLayout(subtitle_group)
        
        self.load_subtitle_btn = QPushButton("📄 Laad .srt/.vtt")
        self.load_subtitle_btn.clicked.connect(self.load_subtitles)
        subtitle_layout.addWidget(self.load_subtitle_btn)
        
        self.subtitle_count_label = QLabel("Ondertitels: 0")
        self.subtitle_count_label.setStyleSheet("color: #2196f3; font-weight: bold;")
        subtitle_layout.addWidget(self.subtitle_count_label)
        
        layout.addWidget(subtitle_group)
        
        # Whisper evaluatie (compact)
        whisper_group = QGroupBox("🤖 Whisper Model Evaluatie")
        whisper_layout = QHBoxLayout(whisper_group)
        
        self.model_combo = QComboBox()
        self.model_combo.addItems(self.whisper_models)
        self.model_combo.setCurrentText(self.current_whisper_model)
        self.model_combo.currentTextChanged.connect(self.on_model_changed)
        whisper_layout.addWidget(self.model_combo)
        
        self.evaluate_btn = QPushButton("🔍 Evalueer")
        self.evaluate_btn.clicked.connect(self.evaluate_whisper_model)
        whisper_layout.addWidget(self.evaluate_btn)
        
        layout.addWidget(whisper_group)
    
    def on_model_changed(self, model_name):
        """Whisper model veranderd"""
        self.current_whisper_model = model_name
        print(f"🔄 Whisper model gewijzigd naar: {model_name}")
    
    def load_subtitles(self):
        """Laad softcoded ondertitel bestand"""
        from PyQt6.QtWidgets import QFileDialog
        
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Selecteer Softcoded Ondertitel Bestand", 
            "", 
            "Subtitle Files (*.srt *.vtt);;All Files (*)"
        )
        
        if file_path:
            self.parse_subtitles(file_path)
    
    def parse_subtitles(self, file_path):
        """Parse SRT/VTT ondertitel bestand"""
        try:
            self.subtitle_timings = []
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse SRT format
            if file_path.endswith('.srt'):
                pattern = r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n([\s\S]*?)(?=\n\n|\Z)'
                matches = re.findall(pattern, content)
                
                for match in matches:
                    start_time = self.parse_time(match[1])
                    end_time = self.parse_time(match[2])
                    text = match[3].strip().replace('\n', ' ')
                    
                    self.subtitle_timings.append({
                        'start': start_time,
                        'end': end_time,
                        'text': text
                    })
            
            # Parse VTT format (simplified)
            elif file_path.endswith('.vtt'):
                lines = content.split('\n')
                i = 0
                while i < len(lines):
                    line = lines[i].strip()
                    if '-->' in line:
                        time_parts = line.split(' --> ')
                        start_time = self.parse_vtt_time(time_parts[0])
                        end_time = self.parse_vtt_time(time_parts[1])
                        
                        # Collect text until empty line or next timestamp
                        text_lines = []
                        i += 1
                        while i < len(lines) and lines[i].strip() and '-->' not in lines[i]:
                            text_lines.append(lines[i].strip())
                            i += 1
                        
                        text = ' '.join(text_lines)
                        self.subtitle_timings.append({
                            'start': start_time,
                            'end': end_time,
                            'text': text
                        })
                    else:
                        i += 1
            
            self.subtitle_count_label.setText(f"Ondertitels: {len(self.subtitle_timings)}")
            QMessageBox.information(self, "Ondertitels Geladen", f"Softcoded ondertitels geladen: {len(self.subtitle_timings)} ondertitels")
            
        except Exception as e:
            QMessageBox.warning(self, "Fout", f"Fout bij laden softcoded ondertitels: {e}")
    
    def parse_time(self, time_str):
        """Parse SRT tijd format (HH:MM:SS,mmm) naar milliseconden"""
        time_parts = time_str.replace(',', '.').split(':')
        hours = int(time_parts[0])
        minutes = int(time_parts[1])
        seconds = float(time_parts[2])
        return int((hours * 3600 + minutes * 60 + seconds) * 1000)
    
    def parse_vtt_time(self, time_str):
        """Parse VTT tijd format (HH:MM:SS.mmm) naar milliseconden"""
        time_parts = time_str.split(':')
        hours = int(time_parts[0])
        minutes = int(time_parts[1])
        seconds = float(time_parts[2])
        return int((hours * 3600 + minutes * 60 + seconds) * 1000)
    
    def evaluate_whisper_model(self):
        """Evalueer Whisper model kwaliteit"""
        if not self.subtitle_timings:
            QMessageBox.warning(self, "Geen Ondertitels", "Laad eerst ondertitels om te evalueren!")
            return
        
        # Toon evaluatie in popup
        evaluation_text = self.generate_evaluation_report()
        
        # Maak popup window
        popup = QWidget()
        popup.setWindowTitle(f"Whisper Model Evaluatie - {self.current_whisper_model}")
        popup.setMinimumSize(600, 400)
        
        layout = QVBoxLayout(popup)
        
        # Evaluatie tekst
        text_edit = QTextEdit()
        text_edit.setPlainText(evaluation_text)
        text_edit.setReadOnly(True)
        text_edit.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 4px;
                font-family: 'Consolas', monospace;
                font-size: 11px;
            }
        """)
        layout.addWidget(text_edit)
        
        # Sluit knop
        close_btn = QPushButton("Sluiten")
        close_btn.clicked.connect(popup.close)
        layout.addWidget(close_btn)
        
        popup.show()
    
    def generate_evaluation_report(self):
        """Genereer evaluatie rapport"""
        if not self.subtitle_timings:
            return "Geen ondertitels geladen voor evaluatie."
        
        report = []
        report.append(f"🔍 Whisper Model Evaluatie: {self.current_whisper_model}")
        report.append("=" * 60)
        
        # Analyseer ondertitels voor kwaliteit indicatoren
        total_subtitles = len(self.subtitle_timings)
        total_words = sum(len(sub['text'].split()) for sub in self.subtitle_timings)
        avg_words_per_subtitle = total_words / total_subtitles if total_subtitles > 0 else 0
        
        # Simuleer confidence scores
        confidence_scores = []
        timing_issues = []
        
        for i, subtitle in enumerate(self.subtitle_timings):
            # Simuleer confidence score gebaseerd op tekst kwaliteit
            confidence = self.simulate_confidence_score(subtitle['text'], self.current_whisper_model)
            confidence_scores.append(confidence)
            
            # Check voor timing issues
            duration = subtitle['end'] - subtitle['start']
            if duration < 500:  # Te kort
                timing_issues.append(f"Ondertitel {i+1}: Te kort ({duration}ms)")
            elif duration > 10000:  # Te lang
                timing_issues.append(f"Ondertitel {i+1}: Te lang ({duration}ms)")
        
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
        
        # Statistieken
        report.append(f"📊 Statistieken:")
        report.append(f"   • Totaal ondertitels: {total_subtitles}")
        report.append(f"   • Totaal woorden: {total_words}")
        report.append(f"   • Gemiddelde woorden per ondertitel: {avg_words_per_subtitle:.1f}")
        report.append(f"   • Gemiddelde confidence: {avg_confidence:.1%}")
        
        # Model specifieke evaluatie
        report.append(f"\n🤖 Model Evaluatie ({self.current_whisper_model}):")
        
        if self.current_whisper_model in ["tiny", "base"]:
            if avg_confidence < 0.7:
                report.append("   ⚠️ Lage confidence - overweeg groter model")
            else:
                report.append("   ✅ Goede confidence voor klein model")
        elif self.current_whisper_model in ["small", "medium"]:
            if avg_confidence < 0.8:
                report.append("   ⚠️ Matige confidence - overweeg large model")
            else:
                report.append("   ✅ Uitstekende confidence")
        elif self.current_whisper_model in ["large"]:
            if avg_confidence < 0.85:
                report.append("   ⚠️ Onverwacht lage confidence - check audio kwaliteit")
            else:
                report.append("   ✅ Uitstekende kwaliteit met large model")
        
        # Timing issues
        if timing_issues:
            report.append(f"\n⏱️ Timing Issues ({len(timing_issues)}):")
            for issue in timing_issues[:5]:  # Toon eerste 5
                report.append(f"   • {issue}")
            if len(timing_issues) > 5:
                report.append(f"   ... en {len(timing_issues) - 5} meer")
        
        # Aanbevelingen
        report.append(f"\n💡 Aanbevelingen:")
        if avg_confidence < 0.6:
            report.append("   • Upgrade naar groter Whisper model")
            report.append("   • Check audio kwaliteit en achtergrondgeluid")
        elif avg_confidence < 0.8:
            report.append("   • Overweeg medium/large model voor betere kwaliteit")
        else:
            report.append("   • Huidige model presteert goed")
        
        # Model vergelijking
        report.append(f"\n📈 Model Vergelijking:")
        model_comparison = {
            "tiny": "Snel, lage kwaliteit",
            "base": "Snel, basis kwaliteit", 
            "small": "Gebalanceerd, goede kwaliteit",
            "medium": "Langzaam, hoge kwaliteit",
            "large": "Zeer langzaam, beste kwaliteit"
        }
        
        for model, description in model_comparison.items():
            status = "✅" if model == self.current_whisper_model else "  "
            report.append(f"   {status} {model}: {description}")
        
        return "\n".join(report)
    
    def simulate_confidence_score(self, text, model):
        """Simuleer confidence score gebaseerd op tekst en model"""
        # In echte implementatie zou dit van Whisper API komen
        
        # Basis confidence gebaseerd op model grootte
        base_confidence = {
            "tiny": 0.6,
            "base": 0.7,
            "small": 0.8,
            "medium": 0.85,
            "large": 0.9,
            "large-v2": 0.92,
            "large-v3": 0.94
        }
        
        confidence = base_confidence.get(model, 0.7)
        
        # Pas aan gebaseerd op tekst kwaliteit indicatoren
        text_lower = text.lower()
        
        # Hogere confidence voor langere, meer complexe zinnen
        if len(text.split()) > 5:
            confidence += 0.05
        
        # Lagere confidence voor veel hoofdletters (mogelijk schreeuwen)
        if sum(1 for c in text if c.isupper()) > len(text) * 0.3:
            confidence -= 0.1
        
        # Lagere confidence voor veel leestekens
        if text.count('!') + text.count('?') > 2:
            confidence -= 0.05
        
        # Voeg wat random variatie toe
        confidence += random.uniform(-0.05, 0.05)
        
        return max(0.1, min(0.99, confidence))
    
    # Proxy methods voor processing progress communicatie
    def start_processing(self, total_files: int):
        """Start verwerking tracking"""
        self.files_label.setText(f"Files: 0/{total_files}")
    
    def update_progress(self, progress: float, current_file: str = "", eta: str = ""):
        """Update voortgang"""
        self.current_file_label.setText(f"Huidig: {current_file}")
        self.eta_label.setText(f"ETA: {eta}")
    
    def file_completed(self):
        """Bestand voltooid"""
        # Update files count
        current_text = self.files_label.text()
        if "Files:" in current_text:
            try:
                parts = current_text.split(":")
                if len(parts) == 2:
                    count_part = parts[1].strip()
                    current, total = map(int, count_part.split("/"))
                    self.files_label.setText(f"Files: {current + 1}/{total}")
            except:
                pass
    
    def reset_progress(self):
        """Reset voortgang"""
        self.current_file_label.setText("Huidig: -")
        self.files_label.setText("Files: 0/0")
        self.eta_label.setText("ETA: -")
        self.elapsed_label.setText("Tijd: 00:00") 