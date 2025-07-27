"""
Magic Time Studio - Hoofdapplicatie
Modulaire versie van de video ondertiteling applicatie
"""

import os
import sys
import tkinter as tk
from tkinter import messagebox
import warnings

# Onderdruk waarschuwingen
warnings.filterwarnings("ignore", message="Failed to launch Triton kernels")
warnings.filterwarnings("ignore", message="Failed to launch Triton kernels, likely due to missing CUDA toolkit")
warnings.filterwarnings("ignore", message=".*Triton.*")

# Import onze modules
from .core.config import config_manager
from .core.logging import logger
from .core.utils import gui_updater
from .models.processing_queue import processing_queue, batch_manager
from .models.progress_tracker import progress_tracker
from .models.performance_tracker import performance_tracker

# Import UI modules
from .ui.main_window import MainWindow
from .ui.themes import theme_manager

# Import processing modules
from .processing import whisper_processor, translator, audio_processor, video_processor, batch_processor

class MagicTimeStudio:
    """Hoofdapplicatie klasse"""
    
    def __init__(self):
        self.root = None
        self.main_window = None
        self.processing_active = False
        
        # Initialiseer modules
        self._init_modules()
    
    def _init_modules(self):
        """Initialiseer alle modules"""
        logger.log_debug("🚀 Magic Time Studio wordt geïnitialiseerd...")
        
        # Laad configuratie
        config_manager.load_configuration()
        
        # Log systeem informatie
        logger.log_system_info()
        
        # Initialiseer processing modules
        self._init_processing_modules()
        
        logger.log_debug("✅ Modules geïnitialiseerd")
    
    def _init_processing_modules(self):
        """Initialiseer processing modules"""
        logger.log_debug("🔧 Processing modules initialiseren...")
        
        # Initialiseer Whisper
        default_model = config_manager.get("default_whisper_model", "base")
        if whisper_processor.initialize(default_model):
            logger.log_debug(f"✅ Whisper geïnitialiseerd met model: {default_model}")
        else:
            logger.log_debug("⚠️ Whisper initialisatie gefaald")
        
        # Controleer FFmpeg
        if audio_processor.is_ffmpeg_available():
            logger.log_debug("✅ FFmpeg beschikbaar")
        else:
            logger.log_debug("⚠️ FFmpeg niet gevonden")
        
        # Zet vertaler service
        default_translator = config_manager.get("default_translator", "libretranslate")
        translator.set_service(default_translator)
        logger.log_debug(f"✅ Translator geïnitialiseerd: {default_translator}")
    
    def create_ui(self):
        """Maak de gebruikersinterface"""
        logger.log_debug("🎨 UI wordt aangemaakt...")
        
        # Maak root window
        self.root = tk.Tk()
        
        # Zet root voor GUI updater
        gui_updater.set_root(self.root)
        
        # Maak hoofdvenster
        self.main_window = MainWindow(self.root)
        
        # Zet callbacks
        self.main_window.set_callbacks(
            on_file_selected=self._on_file_selected,
            on_start_processing=self._on_start_processing,
            on_stop_processing=self._on_stop_processing
        )
        
        logger.log_debug("✅ UI aangemaakt")
    
    def _on_file_selected(self, file_path: str):
        """Callback voor bestand selectie"""
        logger.log_debug(f"📁 Bestand geselecteerd in hoofdapp: {file_path}")
        # TODO: Implementeer bestand verwerking
    
    def _on_start_processing(self):
        """Callback voor start verwerking"""
        logger.log_debug("▶️ Verwerking gestart in hoofdapp")
        # TODO: Implementeer verwerking starten
    
    def _on_stop_processing(self):
        """Callback voor stop verwerking"""
        logger.log_debug("⏹️ Verwerking gestopt in hoofdapp")
        # TODO: Implementeer verwerking stoppen
    
    def run(self):
        """Start de applicatie"""
        try:
            logger.log_debug("🚀 Magic Time Studio wordt gestart...")
            
            # Maak UI
            self.create_ui()
            
            # Start mainloop
            logger.log_debug("🔄 Mainloop gestart")
            self.root.mainloop()
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij starten applicatie: {e}")
            messagebox.showerror("Fout", f"Fout bij starten applicatie: {e}")
    
    def quit_app(self):
        """Sluit de applicatie"""
        logger.log_debug("👋 Magic Time Studio wordt afgesloten...")
        
        # Sla configuratie op
        config_manager.save_configuration()
        
        # Sluit root window
        if self.root:
            self.root.quit()
            self.root.destroy()

def main():
    """Hoofdfunctie"""
    try:
        # Maak en start applicatie
        app = MagicTimeStudio()
        app.run()
    except Exception as e:
        print(f"❌ Kritieke fout: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 