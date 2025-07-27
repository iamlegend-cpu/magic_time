"""
Geavanceerde processing panel voor Magic Time Studio
Integreert alle verwerkingsfunctionaliteit
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Dict, Any, Optional, Callable, List
from ..core.logging import logger
from ..core.config import config_manager
from ..core.utils import gui_updater
from .themes import theme_manager
from ..processing import whisper_processor, translator, audio_processor, video_processor, batch_processor

class ProcessingPanel:
    """Geavanceerde processing panel met alle functionaliteit"""
    
    def __init__(self, parent: tk.Widget):
        self.parent = parent
        self.frame = None
        self.processing_active = False
        
        # Callbacks
        self.on_start_processing: Optional[Callable] = None
        self.on_stop_processing: Optional[Callable] = None
        self.on_file_processed: Optional[Callable] = None
        
        # UI elements
        self.progress_bar = None
        self.status_label = None
        self.progress_label = None
        self.file_list = []
        
        self.create_panel()
    
    def create_panel(self):
        """Maak het processing panel"""
        self.frame = theme_manager.create_styled_frame(self.parent)
        
        # Titel
        title_label = theme_manager.create_styled_label(
            self.frame,
            "🎬 Video Verwerking",
            font=("Arial", 12, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        # Settings frame
        settings_frame = theme_manager.create_styled_frame(self.frame)
        settings_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Whisper settings
        whisper_frame = theme_manager.create_styled_frame(settings_frame)
        whisper_frame.pack(fill=tk.X, pady=2)
        
        whisper_label = theme_manager.create_styled_label(
            whisper_frame,
            "Whisper Model:",
            font=("Arial", 10, "bold")
        )
        whisper_label.pack(anchor=tk.W)
        
        self.whisper_model_var = tk.StringVar(value=config_manager.get("default_whisper_model", "base"))
        whisper_combobox = theme_manager.create_styled_combobox(
            whisper_frame,
            whisper_processor.get_available_models(),
            textvariable=self.whisper_model_var
        )
        whisper_combobox.pack(fill=tk.X, pady=2)
        
        # Language settings
        language_frame = theme_manager.create_styled_frame(settings_frame)
        language_frame.pack(fill=tk.X, pady=2)
        
        language_label = theme_manager.create_styled_label(
            language_frame,
            "Taal:",
            font=("Arial", 10, "bold")
        )
        language_label.pack(anchor=tk.W)
        
        self.language_var = tk.StringVar(value=config_manager.get("default_language", "auto"))
        language_combobox = theme_manager.create_styled_combobox(
            language_frame,
            list(whisper_processor.get_supported_languages().keys()),
            textvariable=self.language_var
        )
        language_combobox.pack(fill=tk.X, pady=2)
        
        # Translator settings
        translator_frame = theme_manager.create_styled_frame(settings_frame)
        translator_frame.pack(fill=tk.X, pady=2)
        
        translator_label = theme_manager.create_styled_label(
            translator_frame,
            "Vertaler:",
            font=("Arial", 10, "bold")
        )
        translator_label.pack(anchor=tk.W)
        
        self.translator_var = tk.StringVar(value=config_manager.get("default_translator", "libretranslate"))
        translator_combobox = theme_manager.create_styled_combobox(
            translator_frame,
            list(translator.get_supported_services().keys()),
            textvariable=self.translator_var
        )
        translator_combobox.pack(fill=tk.X, pady=2)
        
        # Target language
        target_language_frame = theme_manager.create_styled_frame(settings_frame)
        target_language_frame.pack(fill=tk.X, pady=2)
        
        target_language_label = theme_manager.create_styled_label(
            target_language_frame,
            "Doeltaal:",
            font=("Arial", 10, "bold")
        )
        target_language_label.pack(anchor=tk.W)
        
        self.target_language_var = tk.StringVar(value="nl")
        target_language_combobox = theme_manager.create_styled_combobox(
            target_language_frame,
            list(translator.get_supported_languages().keys()),
            textvariable=self.target_language_var
        )
        target_language_combobox.pack(fill=tk.X, pady=2)
        
        # Output settings
        output_frame = theme_manager.create_styled_frame(settings_frame)
        output_frame.pack(fill=tk.X, pady=2)
        
        output_label = theme_manager.create_styled_label(
            output_frame,
            "Output:",
            font=("Arial", 10, "bold")
        )
        output_label.pack(anchor=tk.W)
        
        # Output directory
        output_dir_frame = theme_manager.create_styled_frame(output_frame)
        output_dir_frame.pack(fill=tk.X, pady=2)
        
        self.output_dir_var = tk.StringVar(value=config_manager.get("output_dir", "~/MagicTime_Output"))
        output_dir_entry = theme_manager.create_styled_entry(
            output_dir_frame,
            textvariable=self.output_dir_var
        )
        output_dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        browse_button = theme_manager.create_styled_button(
            output_dir_frame,
            "📁",
            self.browse_output_dir
        )
        browse_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Output format checkboxes
        format_frame = theme_manager.create_styled_frame(output_frame)
        format_frame.pack(fill=tk.X, pady=2)
        
        self.generate_srt_var = tk.BooleanVar(value=True)
        srt_check = tk.Checkbutton(
            format_frame,
            text="SRT bestand",
            variable=self.generate_srt_var,
            bg=theme_manager.colors["bg"],
            fg=theme_manager.colors["fg"],
            selectcolor=theme_manager.colors["accent"],
            font=("Arial", 9)
        )
        srt_check.pack(side=tk.LEFT, padx=5)
        
        self.generate_translated_srt_var = tk.BooleanVar(value=True)
        translated_srt_check = tk.Checkbutton(
            format_frame,
            text="Vertaalde SRT",
            variable=self.generate_translated_srt_var,
            bg=theme_manager.colors["bg"],
            fg=theme_manager.colors["fg"],
            selectcolor=theme_manager.colors["accent"],
            font=("Arial", 9)
        )
        translated_srt_check.pack(side=tk.LEFT, padx=5)
        
        # Progress frame
        progress_frame = theme_manager.create_styled_frame(self.frame)
        progress_frame.pack(fill=tk.X, padx=5, pady=10)
        
        self.progress_label = theme_manager.create_styled_label(
            progress_frame,
            "Klaar voor verwerking...",
            font=("Arial", 9)
        )
        self.progress_label.pack(anchor=tk.W)
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='determinate',
            length=300
        )
        self.progress_bar.pack(fill=tk.X, pady=2)
        
        self.status_label = theme_manager.create_styled_label(
            progress_frame,
            "Status: Klaar",
            font=("Arial", 9)
        )
        self.status_label.pack(anchor=tk.W)
        
        # Control buttons
        button_frame = theme_manager.create_styled_frame(self.frame)
        button_frame.pack(fill=tk.X, padx=5, pady=10)
        
        self.start_button = theme_manager.create_styled_button(
            button_frame,
            "▶️ Start Verwerking",
            self.start_processing,
            bg="#4CAF50",
            fg="white"
        )
        self.start_button.pack(side=tk.LEFT, padx=2)
        
        self.stop_button = theme_manager.create_styled_button(
            button_frame,
            "⏹️ Stop",
            self.stop_processing,
            bg="#f44336",
            fg="white"
        )
        self.stop_button.pack(side=tk.LEFT, padx=2)
        
        self.test_button = theme_manager.create_styled_button(
            button_frame,
            "🧪 Test",
            self.test_settings
        )
        self.test_button.pack(side=tk.RIGHT, padx=2)
        
        # Batch processing
        batch_frame = theme_manager.create_styled_frame(self.frame)
        batch_frame.pack(fill=tk.X, padx=5, pady=5)
        
        batch_label = theme_manager.create_styled_label(
            batch_frame,
            "📦 Batch Verwerking",
            font=("Arial", 10, "bold")
        )
        batch_label.pack(anchor=tk.W)
        
        batch_button_frame = theme_manager.create_styled_frame(batch_frame)
        batch_button_frame.pack(fill=tk.X, pady=2)
        
        self.add_to_batch_button = theme_manager.create_styled_button(
            batch_button_frame,
            "➕ Voeg toe aan batch",
            self.add_to_batch
        )
        self.add_to_batch_button.pack(side=tk.LEFT, padx=2)
        
        self.start_batch_button = theme_manager.create_styled_button(
            batch_button_frame,
            "🚀 Start batch",
            self.start_batch_processing
        )
        self.start_batch_button.pack(side=tk.LEFT, padx=2)
        
        self.clear_batch_button = theme_manager.create_styled_button(
            batch_button_frame,
            "🗑️ Wis batch",
            self.clear_batch
        )
        self.clear_batch_button.pack(side=tk.RIGHT, padx=2)
        
        # Update button states
        self.update_button_states()
        
        logger.log_debug("🎬 Geavanceerde processing panel aangemaakt")
    
    def set_file_list(self, file_list: List[str]):
        """Zet lijst van bestanden om te verwerken"""
        self.file_list = file_list
        logger.log_debug(f"📁 File list gezet: {len(file_list)} bestanden")
    
    def get_settings(self) -> Dict[str, Any]:
        """Krijg huidige instellingen"""
        return {
            "whisper": {
                "model": self.whisper_model_var.get(),
                "language": self.language_var.get()
            },
            "translator": {
                "service": self.translator_var.get(),
                "target_language": self.target_language_var.get()
            },
            "output": {
                "directory": self.output_dir_var.get(),
                "generate_srt": self.generate_srt_var.get(),
                "generate_translated_srt": self.generate_translated_srt_var.get()
            },
            "auto_detect": True
        }
    
    def start_processing(self):
        """Start verwerking van geselecteerde bestanden"""
        if not self.file_list:
            messagebox.showwarning("Waarschuwing", "Geen bestanden geselecteerd")
            return
        
        if self.processing_active:
            messagebox.showwarning("Waarschuwing", "Verwerking is al actief")
            return
        
        # Valideer instellingen
        settings = self.get_settings()
        if not self._validate_settings(settings):
            return
        
        # Start verwerking
        self.processing_active = True
        self.update_button_states()
        self.update_status("Verwerking gestart...")
        
        if self.on_start_processing:
            self.on_start_processing()
        
        # Start processing thread
        import threading
        processing_thread = threading.Thread(
            target=self._process_files,
            args=(self.file_list, settings),
            daemon=True
        )
        processing_thread.start()
    
    def _process_files(self, file_list: List[str], settings: Dict[str, Any]):
        """Verwerk bestanden in thread"""
        try:
            total_files = len(file_list)
            completed_files = 0
            
            for i, file_path in enumerate(file_list):
                if not self.processing_active:
                    break
                
                # Update progress
                progress = i / total_files
                self.update_progress(progress, f"Verwerken: {i+1}/{total_files}")
                
                # Verwerk bestand
                result = video_processor.process_video(
                    file_path, 
                    settings,
                    lambda p, s: self.update_progress(progress + (p / total_files), s)
                )
                
                if result.get("success"):
                    completed_files += 1
                    logger.log_debug(f"✅ Bestand verwerkt: {safe_basename(file_path)}")
                    
                    if self.on_file_processed:
                        self.on_file_processed(file_path, result)
                else:
                    logger.log_debug(f"❌ Fout bij verwerken: {safe_basename(file_path)} - {result.get('error')}")
            
            # Voltooid
            self.update_progress(1.0, "Verwerking voltooid!")
            self.update_status(f"Voltooid: {completed_files}/{total_files} bestanden")
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij verwerken bestanden: {e}")
            self.update_status(f"Fout: {e}")
        finally:
            self.processing_active = False
            self.update_button_states()
            
            if self.on_stop_processing:
                self.on_stop_processing()
    
    def stop_processing(self):
        """Stop verwerking"""
        self.processing_active = False
        self.update_status("Verwerking gestopt")
        self.update_button_states()
        
        if self.on_stop_processing:
            self.on_stop_processing()
    
    def add_to_batch(self):
        """Voeg bestanden toe aan batch"""
        if not self.file_list:
            messagebox.showwarning("Waarschuwing", "Geen bestanden geselecteerd")
            return
        
        settings = self.get_settings()
        if not self._validate_settings(settings):
            return
        
        result = batch_processor.add_files_to_batch(self.file_list, settings)
        
        if result.get("success"):
            messagebox.showinfo("Succes", f"{result['added_files']} bestanden toegevoegd aan batch")
            logger.log_debug(f"📦 Batch uitgebreid: {result['total_in_batch']} bestanden")
        else:
            messagebox.showerror("Fout", result.get("error", "Onbekende fout"))
    
    def start_batch_processing(self):
        """Start batch verwerking"""
        if batch_processor.is_processing_active():
            messagebox.showwarning("Waarschuwing", "Batch verwerking is al actief")
            return
        
        batch_status = batch_processor.get_batch_status()
        if batch_status["total_files"] == 0:
            messagebox.showwarning("Waarschuwing", "Geen bestanden in batch")
            return
        
        # Start batch verwerking
        result = batch_processor.start_batch_processing(
            progress_callback=self.update_progress,
            status_callback=self.update_status
        )
        
        if result.get("success"):
            messagebox.showinfo("Succes", f"Batch verwerking gestart: {result['total_files']} bestanden")
        else:
            messagebox.showerror("Fout", result.get("error", "Onbekende fout"))
    
    def clear_batch(self):
        """Wis batch"""
        if messagebox.askyesno("Bevestig", "Weet je zeker dat je de batch wilt wissen?"):
            result = batch_processor.clear_batch()
            if result.get("success"):
                messagebox.showinfo("Succes", "Batch gewist")
            else:
                messagebox.showerror("Fout", result.get("error", "Onbekende fout"))
    
    def test_settings(self):
        """Test huidige instellingen"""
        settings = self.get_settings()
        
        # Test Whisper
        if not whisper_processor.is_model_loaded():
            messagebox.showwarning("Waarschuwing", "Whisper model niet geladen")
            return
        
        # Test FFmpeg
        if not audio_processor.is_ffmpeg_available():
            messagebox.showwarning("Waarschuwing", "FFmpeg niet gevonden")
            return
        
        # Test translator
        translator_service = settings["translator"]["service"]
        if translator_service != "geen":
            if translator.test_service(translator_service):
                messagebox.showinfo("Test", "Alle instellingen OK!")
            else:
                messagebox.showwarning("Waarschuwing", f"Vertaler service '{translator_service}' niet beschikbaar")
        else:
            messagebox.showinfo("Test", "Alle instellingen OK!")
    
    def browse_output_dir(self):
        """Blader naar output directory"""
        directory = filedialog.askdirectory(title="Selecteer output directory")
        if directory:
            self.output_dir_var.set(directory)
    
    def _validate_settings(self, settings: Dict[str, Any]) -> bool:
        """Valideer instellingen"""
        # Controleer output directory
        output_dir = settings["output"]["directory"]
        if not output_dir:
            messagebox.showerror("Fout", "Output directory is verplicht")
            return False
        
        # Controleer Whisper model
        if not whisper_processor.is_model_loaded():
            messagebox.showerror("Fout", "Whisper model niet geladen")
            return False
        
        # Controleer FFmpeg
        if not audio_processor.is_ffmpeg_available():
            messagebox.showerror("Fout", "FFmpeg niet gevonden")
            return False
        
        return True
    
    def update_progress(self, progress: float, status: str):
        """Update voortgangsbalk"""
        def update():
            self.progress_bar["value"] = progress * 100
            self.progress_label.config(text=status)
        
        gui_updater.schedule_gui_update(update)
    
    def update_status(self, status: str):
        """Update status label"""
        def update():
            self.status_label.config(text=f"Status: {status}")
        
        gui_updater.schedule_gui_update(update)
    
    def update_button_states(self):
        """Update button states"""
        def update():
            self.start_button.config(state=tk.NORMAL if not self.processing_active else tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL if self.processing_active else tk.DISABLED)
            self.add_to_batch_button.config(state=tk.NORMAL if not self.processing_active else tk.DISABLED)
            self.start_batch_button.config(state=tk.NORMAL if not self.processing_active else tk.DISABLED)
        
        gui_updater.schedule_gui_update(update)
    
    def set_callbacks(self, on_start_processing=None, on_stop_processing=None, on_file_processed=None):
        """Zet callbacks"""
        self.on_start_processing = on_start_processing
        self.on_stop_processing = on_stop_processing
        self.on_file_processed = on_file_processed
    
    def set_processing_state(self, is_processing: bool):
        """Zet processing state"""
        self.processing_active = is_processing
        self.update_button_states() 