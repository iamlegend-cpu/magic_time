"""
File Preview Widget voor Magic Time Studio
Toon thumbnails en metadata van bestanden
"""

import os
import subprocess
from typing import Optional, Dict, Any
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QGroupBox, QTextEdit, QScrollArea
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QPixmap, QFont, QIcon


class FilePreviewWidget(QWidget):
    """Widget voor bestand preview"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_file = ""
        self.setup_ui()
    
    def setup_ui(self):
        """Setup de UI"""
        layout = QVBoxLayout(self)
        
        # Titel
        title = QLabel("👁️ Bestand Preview")
        title.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff;")
        layout.addWidget(title)
        
        # Scroll area voor content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Content widget
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        
        # Thumbnail
        self.thumbnail_label = QLabel()
        self.thumbnail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thumbnail_label.setMinimumHeight(200)
        self.thumbnail_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #555555;
                border-radius: 8px;
                background-color: rgba(255, 255, 255, 0.05);
            }
        """)
        self.thumbnail_label.setText("Geen bestand geselecteerd")
        self.content_layout.addWidget(self.thumbnail_label)
        
        # Metadata
        metadata_group = QGroupBox("📊 Metadata")
        metadata_layout = QVBoxLayout(metadata_group)
        
        self.metadata_text = QTextEdit()
        self.metadata_text.setMaximumHeight(150)
        self.metadata_text.setReadOnly(True)
        self.metadata_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 4px;
                font-family: 'Consolas', monospace;
                font-size: 10px;
            }
        """)
        metadata_layout.addWidget(self.metadata_text)
        
        self.content_layout.addWidget(metadata_group)
        
        scroll_area.setWidget(self.content_widget)
        layout.addWidget(scroll_area)
    
    def load_file_preview(self, file_path: str):
        """Laad preview van bestand"""
        if not os.path.exists(file_path):
            self.show_error("Bestand niet gevonden")
            return
        
        self.current_file = file_path
        filename = os.path.basename(file_path)
        
        # Laad thumbnail
        self.load_thumbnail(file_path)
        
        # Laad metadata
        self.load_metadata(file_path)
        
        print(f"👁️ Preview geladen voor: {filename}")
    
    def load_thumbnail(self, file_path: str):
        """Laad thumbnail van bestand"""
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext in {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'}:
                # Video thumbnail
                thumbnail = self.generate_video_thumbnail(file_path)
                if thumbnail:
                    self.thumbnail_label.setPixmap(thumbnail)
                    return
            elif file_ext in {'.mp3', '.wav', '.m4a', '.aac', '.flac', '.ogg', '.wma'}:
                # Audio icoon
                self.thumbnail_label.setText("🎵 Audio Bestand")
                self.thumbnail_label.setStyleSheet("""
                    QLabel {
                        border: 2px dashed #555555;
                        border-radius: 8px;
                        background-color: rgba(255, 255, 255, 0.05);
                        font-size: 48px;
                        color: #4caf50;
                    }
                """)
                return
            
            # Fallback: bestand icoon
            self.thumbnail_label.setText("📄 Bestand")
            self.thumbnail_label.setStyleSheet("""
                QLabel {
                    border: 2px dashed #555555;
                    border-radius: 8px;
                    background-color: rgba(255, 255, 255, 0.05);
                    font-size: 48px;
                    color: #2196f3;
                }
            """)
            
        except Exception as e:
            print(f"❌ Fout bij laden thumbnail: {e}")
            self.thumbnail_label.setText("❌ Fout bij laden preview")
    
    def generate_video_thumbnail(self, file_path: str) -> Optional[QPixmap]:
        """Genereer video thumbnail met FFmpeg"""
        try:
            # Gebruik FFmpeg om thumbnail te genereren
            output_path = os.path.join(os.path.dirname(file_path), "temp_thumbnail.jpg")
            
            cmd = [
                "ffmpeg", "-i", file_path,
                "-ss", "00:00:01",  # Neem frame op 1 seconde
                "-vframes", "1",
                "-vf", "scale=320:240",  # Schaal naar 320x240
                "-y",  # Overschrijf output
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and os.path.exists(output_path):
                # Laad thumbnail
                pixmap = QPixmap(output_path)
                
                # Verwijder temp bestand
                try:
                    os.remove(output_path)
                except:
                    pass
                
                return pixmap
            
        except Exception as e:
            print(f"❌ Fout bij genereren thumbnail: {e}")
        
        return None
    
    def load_metadata(self, file_path: str):
        """Laad metadata van bestand"""
        try:
            metadata = self.get_file_metadata(file_path)
            
            # Format metadata voor weergave
            metadata_text = f"""Bestand: {os.path.basename(file_path)}
Pad: {file_path}
Grootte: {metadata.get('size', 'Onbekend')}
Type: {metadata.get('type', 'Onbekend')}
Duur: {metadata.get('duration', 'Onbekend')}
Resolutie: {metadata.get('resolution', 'Onbekend')}
Bitrate: {metadata.get('bitrate', 'Onbekend')}
Codec: {metadata.get('codec', 'Onbekend')}
"""
            
            self.metadata_text.setText(metadata_text)
            
        except Exception as e:
            print(f"❌ Fout bij laden metadata: {e}")
            self.metadata_text.setText(f"Fout bij laden metadata: {e}")
    
    def get_file_metadata(self, file_path: str) -> Dict[str, Any]:
        """Haal bestand metadata op"""
        metadata = {}
        
        try:
            # Bestandsgrootte
            size_bytes = os.path.getsize(file_path)
            metadata['size'] = self.format_file_size(size_bytes)
            
            # Bestandstype
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext in {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'}:
                metadata['type'] = 'Video'
                video_metadata = self.get_video_metadata(file_path)
                metadata.update(video_metadata)
            elif file_ext in {'.mp3', '.wav', '.m4a', '.aac', '.flac', '.ogg', '.wma'}:
                metadata['type'] = 'Audio'
                audio_metadata = self.get_audio_metadata(file_path)
                metadata.update(audio_metadata)
            else:
                metadata['type'] = 'Onbekend'
            
        except Exception as e:
            print(f"❌ Fout bij ophalen metadata: {e}")
        
        return metadata
    
    def get_video_metadata(self, file_path: str) -> Dict[str, Any]:
        """Haal video metadata op met FFprobe"""
        metadata = {}
        
        try:
            cmd = [
                "ffprobe", "-v", "quiet",
                "-print_format", "json",
                "-show_format", "-show_streams",
                file_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                import json
                data = json.loads(result.stdout)
                
                # Zoek video stream
                video_stream = None
                for stream in data.get('streams', []):
                    if stream.get('codec_type') == 'video':
                        video_stream = stream
                        break
                
                if video_stream:
                    # Duur
                    duration = data.get('format', {}).get('duration')
                    if duration:
                        metadata['duration'] = self.format_duration(float(duration))
                    
                    # Resolutie
                    width = video_stream.get('width')
                    height = video_stream.get('height')
                    if width and height:
                        metadata['resolution'] = f"{width}x{height}"
                    
                    # Codec
                    codec = video_stream.get('codec_name')
                    if codec:
                        metadata['codec'] = codec.upper()
                    
                    # Bitrate
                    bitrate = data.get('format', {}).get('bit_rate')
                    if bitrate:
                        metadata['bitrate'] = f"{int(bitrate) // 1000} kbps"
            
        except Exception as e:
            print(f"❌ Fout bij ophalen video metadata: {e}")
        
        return metadata
    
    def get_audio_metadata(self, file_path: str) -> Dict[str, Any]:
        """Haal audio metadata op"""
        metadata = {}
        
        try:
            cmd = [
                "ffprobe", "-v", "quiet",
                "-print_format", "json",
                "-show_format", "-show_streams",
                file_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                import json
                data = json.loads(result.stdout)
                
                # Zoek audio stream
                audio_stream = None
                for stream in data.get('streams', []):
                    if stream.get('codec_type') == 'audio':
                        audio_stream = stream
                        break
                
                if audio_stream:
                    # Duur
                    duration = data.get('format', {}).get('duration')
                    if duration:
                        metadata['duration'] = self.format_duration(float(duration))
                    
                    # Sample rate
                    sample_rate = audio_stream.get('sample_rate')
                    if sample_rate:
                        metadata['sample_rate'] = f"{sample_rate} Hz"
                    
                    # Codec
                    codec = audio_stream.get('codec_name')
                    if codec:
                        metadata['codec'] = codec.upper()
                    
                    # Bitrate
                    bitrate = data.get('format', {}).get('bit_rate')
                    if bitrate:
                        metadata['bitrate'] = f"{int(bitrate) // 1000} kbps"
            
        except Exception as e:
            print(f"❌ Fout bij ophalen audio metadata: {e}")
        
        return metadata
    
    def format_file_size(self, size_bytes: int) -> str:
        """Format bestandsgrootte"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    def format_duration(self, seconds: float) -> str:
        """Format duur"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
    
    def show_error(self, message: str):
        """Toon foutmelding"""
        self.thumbnail_label.setText(f"❌ {message}")
        self.metadata_text.setText(f"Fout: {message}")
    
    def clear_preview(self):
        """Wis preview"""
        self.current_file = ""
        self.thumbnail_label.setText("Geen bestand geselecteerd")
        self.thumbnail_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #555555;
                border-radius: 8px;
                background-color: rgba(255, 255, 255, 0.05);
            }
        """)
        self.metadata_text.clear() 