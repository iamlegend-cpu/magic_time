"""
Configuratievenster voor Magic Time Studio
Beheert alle geavanceerde instellingen
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Dict, Any, Callable, Optional
from ..core.config import config_manager
from ..core.logging import logger
from .themes import theme_manager

class ConfigWindow:
    """Configuratievenster voor geavanceerde instellingen"""
    
    def __init__(self, parent: tk.Tk):
        self.parent = parent
        self.window = None
        self.original_config = config_manager.config.copy()
        
        # Callbacks
        self.on_config_saved: Optional[Callable] = None
        
        self.create_window()
    
    def create_window(self):
        """Maak het configuratievenster"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Configuratie - Magic Time Studio")
        self.window.geometry("800x600")
        self.window.minsize(600, 400)
        
        # Maak venster modal
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Pas thema toe
        theme_manager.apply_theme(self.window, theme_manager.get_current_theme())
        
        # Protocol handlers
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Maak interface
        self.create_interface()
        
        logger.log_debug("⚙️ Configuratievenster aangemaakt")
    
    def create_interface(self):
        """Maak de interface"""
        # Hoofdframe
        main_frame = theme_manager.create_styled_frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Titel
        title_label = theme_manager.create_styled_label(
            main_frame,
            "⚙️ Configuratie",
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Notebook voor tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Maak tabs
        self.create_general_tab()
        self.create_processing_tab()
        self.create_advanced_tab()
        self.create_logging_tab()
        
        # Knoppen frame
        button_frame = theme_manager.create_styled_frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Opslaan knop
        save_button = theme_manager.create_styled_button(
            button_frame,
            "💾 Opslaan",
            self.save_configuration,
            bg="#4CAF50",
            fg="white"
        )
        save_button.pack(side=tk.RIGHT, padx=5)
        
        # Annuleren knop
        cancel_button = theme_manager.create_styled_button(
            button_frame,
            "❌ Annuleren",
            self.cancel_configuration
        )
        cancel_button.pack(side=tk.RIGHT, padx=5)
        
        # Reset knop
        reset_button = theme_manager.create_styled_button(
            button_frame,
            "🔄 Reset naar standaard",
            self.reset_to_defaults
        )
        reset_button.pack(side=tk.LEFT, padx=5)
    
    def create_general_tab(self):
        """Maak algemene instellingen tab"""
        general_frame = theme_manager.create_styled_frame(self.notebook)
        self.notebook.add(general_frame, text="🔧 Algemeen")
        
        # Thema selectie
        theme_frame = theme_manager.create_styled_frame(general_frame)
        theme_frame.pack(fill=tk.X, padx=10, pady=5)
        
        theme_label = theme_manager.create_styled_label(
            theme_frame,
            "Thema:",
            font=("Arial", 10, "bold")
        )
        theme_label.pack(anchor=tk.W)
        
        self.theme_var = tk.StringVar(value=config_manager.get("theme", "dark"))
        theme_combobox = theme_manager.create_styled_combobox(
            theme_frame,
            theme_manager.get_available_themes(),
            textvariable=self.theme_var
        )
        theme_combobox.pack(fill=tk.X, pady=2)
        theme_combobox.bind("<<ComboboxSelected>>", self.on_theme_changed)
        
        # Font grootte
        font_frame = theme_manager.create_styled_frame(general_frame)
        font_frame.pack(fill=tk.X, padx=10, pady=5)
        
        font_label = theme_manager.create_styled_label(
            font_frame,
            "Font grootte:",
            font=("Arial", 10, "bold")
        )
        font_label.pack(anchor=tk.W)
        
        self.font_size_var = tk.IntVar(value=config_manager.get("font_size", 9))
        font_scale = tk.Scale(
            font_frame,
            from_=8,
            to=16,
            orient=tk.HORIZONTAL,
            variable=self.font_size_var,
            bg=theme_manager.colors["bg"],
            fg=theme_manager.colors["fg"],
            troughcolor=theme_manager.colors["frame"],
            highlightbackground=theme_manager.colors["bg"]
        )
        font_scale.pack(fill=tk.X, pady=2)
        
        # Output directory
        output_frame = theme_manager.create_styled_frame(general_frame)
        output_frame.pack(fill=tk.X, padx=10, pady=5)
        
        output_label = theme_manager.create_styled_label(
            output_frame,
            "Output directory:",
            font=("Arial", 10, "bold")
        )
        output_label.pack(anchor=tk.W)
        
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
            "📁 Bladeren",
            self.browse_output_dir
        )
        browse_button.pack(side=tk.RIGHT, padx=(5, 0))
    
    def create_processing_tab(self):
        """Maak verwerkingsinstellingen tab"""
        processing_frame = theme_manager.create_styled_frame(self.notebook)
        self.notebook.add(processing_frame, text="🎤 Verwerking")
        
        # Standaard Whisper model
        model_frame = theme_manager.create_styled_frame(processing_frame)
        model_frame.pack(fill=tk.X, padx=10, pady=5)
        
        model_label = theme_manager.create_styled_label(
            model_frame,
            "Standaard Whisper model:",
            font=("Arial", 10, "bold")
        )
        model_label.pack(anchor=tk.W)
        
        self.default_model_var = tk.StringVar(value=config_manager.get("default_whisper_model", "base"))
        model_combobox = theme_manager.create_styled_combobox(
            model_frame,
            ["tiny", "base", "small", "medium", "large"],
            textvariable=self.default_model_var
        )
        model_combobox.pack(fill=tk.X, pady=2)
        
        # Standaard taal
        language_frame = theme_manager.create_styled_frame(processing_frame)
        language_frame.pack(fill=tk.X, padx=10, pady=5)
        
        language_label = theme_manager.create_styled_label(
            language_frame,
            "Standaard taal:",
            font=("Arial", 10, "bold")
        )
        language_label.pack(anchor=tk.W)
        
        self.default_language_var = tk.StringVar(value=config_manager.get("default_language", "auto"))
        language_combobox = theme_manager.create_styled_combobox(
            language_frame,
            ["auto", "nl", "en", "de", "fr", "es", "it", "pt", "ru", "ja", "ko", "zh"],
            textvariable=self.default_language_var
        )
        language_combobox.pack(fill=tk.X, pady=2)
        
        # Standaard vertaler
        translator_frame = theme_manager.create_styled_frame(processing_frame)
        translator_frame.pack(fill=tk.X, padx=10, pady=5)
        
        translator_label = theme_manager.create_styled_label(
            translator_frame,
            "Standaard vertaler:",
            font=("Arial", 10, "bold")
        )
        translator_label.pack(anchor=tk.W)
        
        self.default_translator_var = tk.StringVar(value=config_manager.get("default_translator", "libretranslate"))
        translator_combobox = theme_manager.create_styled_combobox(
            translator_frame,
            ["libretranslate", "geen"],
            textvariable=self.default_translator_var
        )
        translator_combobox.pack(fill=tk.X, pady=2)
        
        # Worker count
        worker_frame = theme_manager.create_styled_frame(processing_frame)
        worker_frame.pack(fill=tk.X, padx=10, pady=5)
        
        worker_label = theme_manager.create_styled_label(
            worker_frame,
            "Aantal workers:",
            font=("Arial", 10, "bold")
        )
        worker_label.pack(anchor=tk.W)
        
        self.worker_count_var = tk.IntVar(value=config_manager.get("worker_count", 4))
        worker_scale = tk.Scale(
            worker_frame,
            from_=1,
            to=8,
            orient=tk.HORIZONTAL,
            variable=self.worker_count_var,
            bg=theme_manager.colors["bg"],
            fg=theme_manager.colors["fg"],
            troughcolor=theme_manager.colors["frame"],
            highlightbackground=theme_manager.colors["bg"]
        )
        worker_scale.pack(fill=tk.X, pady=2)
    
    def create_advanced_tab(self):
        """Maak geavanceerde instellingen tab"""
        advanced_frame = theme_manager.create_styled_frame(self.notebook)
        self.notebook.add(advanced_frame, text="🔧 Geavanceerd")
        
        # Auto detect
        auto_detect_frame = theme_manager.create_styled_frame(advanced_frame)
        auto_detect_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.auto_detect_var = tk.BooleanVar(value=config_manager.get("auto_detect", True))
        auto_detect_check = tk.Checkbutton(
            auto_detect_frame,
            text="Automatische taal detectie",
            variable=self.auto_detect_var,
            bg=theme_manager.colors["bg"],
            fg=theme_manager.colors["fg"],
            selectcolor=theme_manager.colors["accent"],
            font=("Arial", 9)
        )
        auto_detect_check.pack(anchor=tk.W, pady=2)
        
        # Performance tracking
        perf_frame = theme_manager.create_styled_frame(advanced_frame)
        perf_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.performance_tracking_var = tk.BooleanVar(value=config_manager.get("performance_tracking", False))
        perf_check = tk.Checkbutton(
            perf_frame,
            text="Performance tracking",
            variable=self.performance_tracking_var,
            bg=theme_manager.colors["bg"],
            fg=theme_manager.colors["fg"],
            selectcolor=theme_manager.colors["accent"],
            font=("Arial", 9)
        )
        perf_check.pack(anchor=tk.W, pady=2)
        
        # Auto save
        auto_save_frame = theme_manager.create_styled_frame(advanced_frame)
        auto_save_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.auto_save_var = tk.BooleanVar(value=config_manager.get("auto_save", True))
        auto_save_check = tk.Checkbutton(
            auto_save_frame,
            text="Automatisch opslaan",
            variable=self.auto_save_var,
            bg=theme_manager.colors["bg"],
            fg=theme_manager.colors["fg"],
            selectcolor=theme_manager.colors["accent"],
            font=("Arial", 9)
        )
        auto_save_check.pack(anchor=tk.W, pady=2)
        
        # Batch verwerking
        batch_frame = theme_manager.create_styled_frame(advanced_frame)
        batch_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.batch_processing_var = tk.BooleanVar(value=config_manager.get("batch_processing", False))
        batch_check = tk.Checkbutton(
            batch_frame,
            text="Batch verwerking inschakelen",
            variable=self.batch_processing_var,
            bg=theme_manager.colors["bg"],
            fg=theme_manager.colors["fg"],
            selectcolor=theme_manager.colors["accent"],
            font=("Arial", 9)
        )
        batch_check.pack(anchor=tk.W, pady=2)
    
    def create_logging_tab(self):
        """Maak logging instellingen tab"""
        logging_frame = theme_manager.create_styled_frame(self.notebook)
        self.notebook.add(logging_frame, text="📋 Logging")
        
        # Logging configuratie
        log_config = config_manager.get("logging_config", {
            "debug": True,
            "info": True,
            "warning": True,
            "error": True
        })
        
        # Debug logging
        debug_frame = theme_manager.create_styled_frame(logging_frame)
        debug_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.debug_logging_var = tk.BooleanVar(value=log_config.get("debug", True))
        debug_check = tk.Checkbutton(
            debug_frame,
            text="Debug logging",
            variable=self.debug_logging_var,
            bg=theme_manager.colors["bg"],
            fg=theme_manager.colors["fg"],
            selectcolor=theme_manager.colors["accent"],
            font=("Arial", 9)
        )
        debug_check.pack(anchor=tk.W, pady=2)
        
        # Info logging
        info_frame = theme_manager.create_styled_frame(logging_frame)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.info_logging_var = tk.BooleanVar(value=log_config.get("info", True))
        info_check = tk.Checkbutton(
            info_frame,
            text="Info logging",
            variable=self.info_logging_var,
            bg=theme_manager.colors["bg"],
            fg=theme_manager.colors["fg"],
            selectcolor=theme_manager.colors["accent"],
            font=("Arial", 9)
        )
        info_check.pack(anchor=tk.W, pady=2)
        
        # Warning logging
        warning_frame = theme_manager.create_styled_frame(logging_frame)
        warning_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.warning_logging_var = tk.BooleanVar(value=log_config.get("warning", True))
        warning_check = tk.Checkbutton(
            warning_frame,
            text="Warning logging",
            variable=self.warning_logging_var,
            bg=theme_manager.colors["bg"],
            fg=theme_manager.colors["fg"],
            selectcolor=theme_manager.colors["accent"],
            font=("Arial", 9)
        )
        warning_check.pack(anchor=tk.W, pady=2)
        
        # Error logging
        error_frame = theme_manager.create_styled_frame(logging_frame)
        error_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.error_logging_var = tk.BooleanVar(value=log_config.get("error", True))
        error_check = tk.Checkbutton(
            error_frame,
            text="Error logging",
            variable=self.error_logging_var,
            bg=theme_manager.colors["bg"],
            fg=theme_manager.colors["fg"],
            selectcolor=theme_manager.colors["accent"],
            font=("Arial", 9)
        )
        error_check.pack(anchor=tk.W, pady=2)
    
    # Event handlers
    def on_theme_changed(self, event=None):
        """Handle thema wijziging"""
        new_theme = self.theme_var.get()
        theme_manager.apply_theme(self.window, new_theme)
        logger.log_debug(f"🎨 Thema gewijzigd in configuratievenster: {new_theme}")
    
    def browse_output_dir(self):
        """Blader naar output directory"""
        directory = filedialog.askdirectory(title="Selecteer output directory")
        if directory:
            self.output_dir_var.set(directory)
    
    def save_configuration(self):
        """Sla configuratie op"""
        try:
            # Verzamel alle instellingen
            config = {
                "theme": self.theme_var.get(),
                "font_size": self.font_size_var.get(),
                "output_dir": self.output_dir_var.get(),
                "default_whisper_model": self.default_model_var.get(),
                "default_language": self.default_language_var.get(),
                "default_translator": self.default_translator_var.get(),
                "worker_count": self.worker_count_var.get(),
                "auto_detect": self.auto_detect_var.get(),
                "performance_tracking": self.performance_tracking_var.get(),
                "auto_save": self.auto_save_var.get(),
                "batch_processing": self.batch_processing_var.get(),
                "logging_config": {
                    "debug": self.debug_logging_var.get(),
                    "info": self.info_logging_var.get(),
                    "warning": self.warning_logging_var.get(),
                    "error": self.error_logging_var.get()
                }
            }
            
            # Update configuratie
            for key, value in config.items():
                config_manager.set(key, value)
            
            # Sla op
            config_manager.save_configuration()
            
            logger.log_debug("💾 Configuratie opgeslagen")
            messagebox.showinfo("Succes", "Configuratie opgeslagen!")
            
            if self.on_config_saved:
                self.on_config_saved(config)
            
            self.window.destroy()
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij opslaan configuratie: {e}")
            messagebox.showerror("Fout", f"Fout bij opslaan configuratie: {e}")
    
    def cancel_configuration(self):
        """Annuleer configuratie wijzigingen"""
        # Herstel originele configuratie
        config_manager.config = self.original_config.copy()
        
        logger.log_debug("❌ Configuratie geannuleerd")
        self.window.destroy()
    
    def reset_to_defaults(self):
        """Reset naar standaard instellingen"""
        if messagebox.askyesno("Bevestig", "Weet je zeker dat je alle instellingen wilt resetten naar standaard?"):
            # Reset naar standaard waarden
            config_manager.config = config_manager.load_configuration()
            
            # Update UI
            self.update_ui_from_config()
            
            logger.log_debug("🔄 Configuratie gereset naar standaard")
            messagebox.showinfo("Succes", "Configuratie gereset naar standaard!")
    
    def update_ui_from_config(self):
        """Update UI van configuratie"""
        # Update alle variabelen
        self.theme_var.set(config_manager.get("theme", "dark"))
        self.font_size_var.set(config_manager.get("font_size", 9))
        self.output_dir_var.set(config_manager.get("output_dir", "~/MagicTime_Output"))
        self.default_model_var.set(config_manager.get("default_whisper_model", "base"))
        self.default_language_var.set(config_manager.get("default_language", "auto"))
        self.default_translator_var.set(config_manager.get("default_translator", "libretranslate"))
        self.worker_count_var.set(config_manager.get("worker_count", 4))
        self.auto_detect_var.set(config_manager.get("auto_detect", True))
        self.performance_tracking_var.set(config_manager.get("performance_tracking", False))
        self.auto_save_var.set(config_manager.get("auto_save", True))
        self.batch_processing_var.set(config_manager.get("batch_processing", False))
        
        # Logging config
        log_config = config_manager.get("logging_config", {
            "debug": True, "info": True, "warning": True, "error": True
        })
        self.debug_logging_var.set(log_config.get("debug", True))
        self.info_logging_var.set(log_config.get("info", True))
        self.warning_logging_var.set(log_config.get("warning", True))
        self.error_logging_var.set(log_config.get("error", True))
    
    def on_closing(self):
        """Handle venster sluiten"""
        logger.log_debug("👋 Configuratievenster wordt gesloten")
        self.cancel_configuration()
    
    def set_callback(self, on_config_saved=None):
        """Zet callback voor configuratie opgeslagen"""
        self.on_config_saved = on_config_saved
    
    def show(self):
        """Toon het configuratievenster"""
        self.window.deiconify()
        self.window.focus_set() 