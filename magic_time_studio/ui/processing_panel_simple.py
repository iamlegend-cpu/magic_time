"""
Eenvoudige Processing panel voor Magic Time Studio
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Callable, Optional
from ..core.config import config_manager
from ..core.logging import logger
from .themes import theme_manager

class ProcessingPanelSimple:
    """Eenvoudige versie van processing panel"""
    
    def __init__(self, parent: tk.Widget):
        self.parent = parent
        
        # Callbacks
        self.on_start_processing: Optional[Callable] = None
        self.on_stop_processing: Optional[Callable] = None
        
        self.create_panel()
    
    def create_panel(self):
        """Maak het processing panel"""
        # Hoofdframe
        self.frame = theme_manager.create_styled_frame(
            self.parent,
            relief=tk.RAISED,
            borderwidth=2
        )
        self.frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Titel
        title_label = theme_manager.create_styled_label(
            self.frame,
            "⚙️ Verwerkingsinstellingen",
            font=("Arial", 12, "bold")
        )
        title_label.pack(pady=(5, 15))
        
        # Whisper model
        model_frame = theme_manager.create_styled_frame(self.frame)
        model_frame.pack(fill=tk.X, padx=10, pady=5)
        
        model_label = theme_manager.create_styled_label(
            model_frame,
            "Whisper Model:",
            font=("Arial", 10, "bold")
        )
        model_label.pack(anchor=tk.W)
        
        self.model_var = tk.StringVar(value="base")
        model_combobox = theme_manager.create_styled_combobox(
            model_frame,
            ["tiny", "base", "small", "medium", "large"],
            textvariable=self.model_var
        )
        model_combobox.pack(fill=tk.X, pady=2)
        
        # Taal
        language_frame = theme_manager.create_styled_frame(self.frame)
        language_frame.pack(fill=tk.X, padx=10, pady=5)
        
        language_label = theme_manager.create_styled_label(
            language_frame,
            "Taal:",
            font=("Arial", 10, "bold")
        )
        language_label.pack(anchor=tk.W)
        
        self.language_var = tk.StringVar(value="auto")
        language_combobox = theme_manager.create_styled_combobox(
            language_frame,
            ["auto", "nl", "en", "de", "fr", "es"],
            textvariable=self.language_var
        )
        language_combobox.pack(fill=tk.X, pady=2)
        
        # Vertaler
        translator_frame = theme_manager.create_styled_frame(self.frame)
        translator_frame.pack(fill=tk.X, padx=10, pady=5)
        
        translator_label = theme_manager.create_styled_label(
            translator_frame,
            "Vertaler:",
            font=("Arial", 10, "bold")
        )
        translator_label.pack(anchor=tk.W)
        
        self.translator_var = tk.StringVar(value="libretranslate")
        translator_combobox = theme_manager.create_styled_combobox(
            translator_frame,
            ["libretranslate", "geen"],
            textvariable=self.translator_var
        )
        translator_combobox.pack(fill=tk.X, pady=2)
        
        # Control knoppen
        button_frame = theme_manager.create_styled_frame(self.frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Start knop
        self.start_button = theme_manager.create_styled_button(
            button_frame,
            "▶️ Start Verwerking",
            self.start_processing
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        # Stop knop
        self.stop_button = theme_manager.create_styled_button(
            button_frame,
            "⏹️ Stop Verwerking",
            self.stop_processing
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Test knop
        test_button = theme_manager.create_styled_button(
            button_frame,
            "🧪 Test Instellingen",
            self.test_settings
        )
        test_button.pack(side=tk.RIGHT, padx=5)
        
        logger.log_debug("⚙️ Eenvoudige processing panel aangemaakt")
    
    def start_processing(self):
        """Start verwerking"""
        logger.log_debug("▶️ Verwerking gestart vanuit processing panel")
        if self.on_start_processing:
            self.on_start_processing()
    
    def stop_processing(self):
        """Stop verwerking"""
        logger.log_debug("⏹️ Verwerking gestopt vanuit processing panel")
        if self.on_stop_processing:
            self.on_stop_processing()
    
    def test_settings(self):
        """Test instellingen"""
        settings = self.get_settings()
        messagebox.showinfo("Instellingen", f"Huidige instellingen:\n{settings}")
    
    def get_settings(self) -> Dict[str, Any]:
        """Krijg huidige instellingen"""
        return {
            "whisper_model": self.model_var.get(),
            "language": self.language_var.get(),
            "translator": self.translator_var.get()
        }
    
    def set_callbacks(self, on_start_processing=None, on_stop_processing=None):
        """Zet callbacks voor events"""
        self.on_start_processing = on_start_processing
        self.on_stop_processing = on_stop_processing
    
    def set_processing_state(self, is_processing: bool):
        """Zet verwerkingsstatus"""
        if is_processing:
            self.start_button.config(state=tk.DISABLED, text="🔄 Verwerking bezig...")
            self.stop_button.config(state=tk.NORMAL)
        else:
            self.start_button.config(state=tk.NORMAL, text="▶️ Start Verwerking")
            self.stop_button.config(state=tk.DISABLED) 