"""
Hoofdvenster UI voor Magic Time Studio
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional, Callable
from ..core.config import config_manager
from ..core.logging import logger
from ..core.utils import gui_updater
from .themes import theme_manager
from .config_window import ConfigWindow
from .log_viewer import LogViewer
from ..processing import batch_processor, whisper_processor, audio_processor, translator

class MainWindow:
    """Hoofdvenster van Magic Time Studio"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.setup_window()
        self.create_menu()
        self.create_main_interface()
        self.create_status_bar()
        
        # Callbacks
        self.on_file_selected: Optional[Callable] = None
        self.on_start_processing: Optional[Callable] = None
        self.on_stop_processing: Optional[Callable] = None
        
    def setup_window(self):
        """Setup het hoofdvenster zoals in versie 1.9.4"""
        self.root.title("Magic Time Studio v2.0")
        self.root.geometry("900x500")
        self.root.minsize(800, 500)
        
        # Protocol handlers
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        logger.log_debug("🏠 Hoofdvenster aangemaakt")
    
    def create_menu(self):
        """Maak de menubalk"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Bestand menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Bestand", menu=file_menu)
        file_menu.add_command(label="Bestand toevoegen...", command=self.add_file)
        file_menu.add_command(label="Map toevoegen...", command=self.add_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Verwijder geselecteerd", command=self.remove_selected)
        file_menu.add_command(label="Wis lijst", command=self.clear_list)
        file_menu.add_separator()
        file_menu.add_command(label="Lijst opslaan...", command=self.save_list)
        file_menu.add_command(label="Lijst laden...", command=self.load_list)
        file_menu.add_separator()
        file_menu.add_command(label="Afsluiten", command=self.on_closing)
        
        # Verwerking menu
        processing_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Verwerking", menu=processing_menu)
        processing_menu.add_command(label="Start verwerking", command=self.start_processing)
        processing_menu.add_command(label="Stop verwerking", command=self.stop_processing)
        processing_menu.add_separator()
        processing_menu.add_command(label="Batch verwerking", command=self.batch_processing)
        processing_menu.add_command(label="Auto verwerking", command=self.auto_processing)
        
        # Instellingen menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Instellingen", menu=settings_menu)
        settings_menu.add_command(label="Configuratie...", command=self.show_config)
        settings_menu.add_separator()
        
        # Thema submenu
        theme_menu = tk.Menu(settings_menu, tearoff=0)
        settings_menu.add_cascade(label="Thema", menu=theme_menu)
        for theme in theme_manager.get_available_themes():
            theme_menu.add_command(
                label=theme.title(),
                command=lambda t=theme: self.change_theme(t)
            )
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Log viewer...", command=self.show_log)
        tools_menu.add_command(label="Performance test...", command=self.performance_test)
        tools_menu.add_separator()
        tools_menu.add_command(label="CUDA test...", command=self.cuda_test)
        tools_menu.add_command(label="Whisper diagnose...", command=self.whisper_diagnose)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Over...", command=self.show_about)
        help_menu.add_command(label="Documentatie...", command=self.show_docs)
    
    def create_main_interface(self):
        """Maak de hoofdinterface zoals versie 1.9.4"""
        # Hoofdframe met grid layout
        self.main_frame = tk.Frame(self.root, bg="#f0f8f0")
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=16, pady=(16, 8))
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Configureer root window
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Maak panels zoals in versie 1.9.4
        self.create_panels_v1_9_4()
    
    def create_panels_v1_9_4(self):
        """Maak panels zoals in versie 1.9.4"""
        # Linker panel (Invoer)
        self.left_panel = tk.LabelFrame(
            self.main_frame, 
            text="Invoer", 
            font=("Segoe UI", 11, "bold"), 
            bg="#f5faf5", 
            fg="#2c2c2c", 
            bd=2, 
            relief="groove", 
            padx=12, 
            pady=12
        )
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 12), pady=0)
        self.left_panel.grid_rowconfigure(99, weight=1)
        self.left_panel.grid_columnconfigure(0, weight=1)
        self.left_panel.grid_columnconfigure(1, weight=1)
        
        # Rechter panel (Verwerking)
        self.right_panel = tk.LabelFrame(
            self.main_frame, 
            text="Verwerking", 
            font=("Segoe UI", 11, "bold"), 
            bg="#f5faf5", 
            fg="#2c2c2c", 
            bd=2, 
            relief="groove", 
            padx=12, 
            pady=12
        )
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=(12, 0), pady=0)
        self.right_panel.grid_rowconfigure(6, weight=1)  # Listbox nog te verwerken krijgt extra ruimte
        self.right_panel.grid_rowconfigure(8, weight=1)  # Listbox voltooid krijgt extra ruimte
        self.right_panel.grid_rowconfigure(99, weight=1)
        self.right_panel.grid_columnconfigure(0, weight=1)
        
        # Maak de inhoud van beide panels
        self.create_left_panel_content()
        self.create_right_panel_content()
    
    def create_left_panel_content(self):
        """Maak de inhoud van het linker panel zoals in versie 1.9.4"""
        # Vertaler status label
        self.translator_status_label = tk.Label(
            self.left_panel, 
            text=f"Vertaler: {translator.get_current_service().upper()}", 
            font=("Segoe UI", 9, "bold"), 
            bg="#f5faf5", 
            fg="#2c3e50"
        )
        self.translator_status_label.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 5))
        
        # CPU status label
        self.cpu_status_label = tk.Label(
            self.left_panel, 
            text="CPU Limiet: 50%", 
            font=("Segoe UI", 8), 
            bg="#f5faf5", 
            fg="#666666"
        )
        self.cpu_status_label.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 5))
        
        # Taal selectie
        tk.Label(self.left_panel, text="Gesproken taal:", font=("Segoe UI", 10), bg="#f5faf5").grid(row=2, column=0, sticky="w")
        
        # Taal dropdown
        self.taal_var = tk.StringVar(value="Auto detectie")
        taal_options = [
            "Auto detectie", "Engels", "Nederlands", "Duits", "Frans", "Spaans", 
            "Italiaans", "Portugees", "Russisch", "Japans", "Koreaans", "Chinees", 
            "Arabisch", "Hindi", "Turks", "Pools", "Zweeds", "Deens", "Noors", "Fins"
        ]
        
        self.taal_combobox = tk.OptionMenu(self.left_panel, self.taal_var, "Auto detectie", *taal_options[1:])
        self.style_dropdown(self.taal_combobox)
        self.taal_combobox.grid(row=2, column=1, sticky="ew", padx=(5, 0))
        
        # Content type
        tk.Label(self.left_panel, text="Content type:", font=("Segoe UI", 10), bg="#f5faf5").grid(row=3, column=0, sticky="w")
        
        self.content_type_var = tk.StringVar(value="Eén hoofdtaal")
        content_type_options = ["Eén hoofdtaal", "Twee talen (gemengd)", "Sporadische woorden"]
        
        self.content_type_combobox = tk.OptionMenu(self.left_panel, self.content_type_var, "Eén hoofdtaal", *content_type_options[1:])
        self.style_dropdown(self.content_type_combobox)
        self.content_type_combobox.grid(row=3, column=1, sticky="ew", padx=(5, 0))
        
        # CPU Limiet
        tk.Label(self.left_panel, text="CPU Limiet:", font=("Segoe UI", 10), bg="#f5faf5").grid(row=4, column=0, sticky="w")
        
        self.cpu_limit_var = tk.IntVar(value=50)
        self.cpu_slider = ttk.Scale(
            self.left_panel, 
            from_=10, 
            to=100, 
            variable=self.cpu_limit_var, 
            orient="horizontal", 
            length=120
        )
        self.cpu_slider.grid(row=4, column=1, sticky="ew", padx=(5, 0))
        
        # CPU percentage label
        self.cpu_percent_label = tk.Label(
            self.left_panel, 
            text="50%", 
            font=("Segoe UI", 8), 
            bg="#f5faf5", 
            fg="#666666"
        )
        self.cpu_percent_label.grid(row=4, column=2, sticky="w", padx=(5, 0))
        
        # CPU load label
        self.cpu_load_label = tk.Label(
            self.left_panel, 
            text="Huidig: --", 
            font=("Segoe UI", 8), 
            bg="#f5faf5", 
            fg="#666666"
        )
        self.cpu_load_label.grid(row=4, column=3, sticky="w", padx=(5, 0))
        
        # Knoppen
        self.btn_voeg_bestand = tk.Button(
            self.left_panel, 
            text="Voeg een bestand toe", 
            font=("Segoe UI", 10, "bold"), 
            height=2, 
            command=self.add_file
        )
        self.btn_voeg_bestand.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 2))
        
        self.btn_voeg_map = tk.Button(
            self.left_panel, 
            text="Voeg een map toe", 
            font=("Segoe UI", 10, "bold"), 
            height=2, 
            command=self.add_folder
        )
        self.btn_voeg_map.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(0, 2))
        
        self.btn_verwijder = tk.Button(
            self.left_panel, 
            text="Verwijder geselecteerd bestand", 
            font=("Segoe UI", 10, "bold"), 
            height=2, 
            bg="#ffebee", 
            fg="#c62828", 
            activebackground="#ffcdd2", 
            activeforeground="#b71c1c", 
            command=self.remove_selected
        )
        self.btn_verwijder.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(0, 2))
        
        self.btn_verwijder_alles = tk.Button(
            self.left_panel, 
            text="Verwijder hele lijst", 
            font=("Segoe UI", 10, "bold"), 
            height=2, 
            bg="#d32f2f", 
            fg="white", 
            activebackground="#b71c1c", 
            activeforeground="white", 
            command=self.clear_list
        )
        self.btn_verwijder_alles.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(0, 2))
        
        # Bind events
        self.taal_var.trace("w", self.on_taal_change)
        self.content_type_var.trace("w", self.on_content_type_change)
        self.cpu_limit_var.trace("w", self.update_cpu_limit)
        
        # Start monitoring
        self.update_cpu_load()
        self.periodic_translator_update()
    
    def create_right_panel_content(self):
        """Maak de inhoud van het rechter panel zoals in versie 1.9.4"""
        # Info label
        self.info_label = tk.Label(
            self.right_panel, 
            text="📄 Geen video gekozen", 
            font=("Segoe UI", 9), 
            fg="gray", 
            justify="left", 
            wraplength=300,
            bg="#f5faf5"
        )
        self.info_label.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        
        # Status label
        self.status_label = tk.Label(
            self.right_panel, 
            text="", 
            font=("Segoe UI", 9, "italic"), 
            fg="#006699", 
            anchor="w",
            bg="#f5faf5"
        )
        self.status_label.grid(row=1, column=0, sticky="ew", pady=(0, 5))
        
        # Progress bar
        self.progress = ttk.Progressbar(self.right_panel, mode="determinate")
        self.progress.grid(row=2, column=0, sticky="ew", pady=(10, 10))
        
        # Start button
        self.start_button = tk.Button(
            self.right_panel, 
            text="Start ondertiteling", 
            font=("Segoe UI", 11, "bold"), 
            bg="#d21f3c", 
            fg="white", 
            activebackground="#a51b2d", 
            padx=10, 
            pady=6, 
            command=self.start_processing
        )
        self.start_button.grid(row=3, column=0, sticky="ew", pady=(0, 5))
        
        # Kill button
        self.kill_button = tk.Button(
            self.right_panel, 
            text="KILL SWITCH", 
            font=("Segoe UI", 11, "bold"), 
            bg="#000000", 
            fg="white", 
            activebackground="#333333", 
            activeforeground="white", 
            padx=10, 
            pady=6, 
            command=self.stop_processing
        )
        self.kill_button.grid(row=4, column=0, sticky="ew", pady=(0, 10))
        
        # Nog te verwerken bestanden
        tk.Label(
            self.right_panel, 
            text="📋 Nog te verwerken bestanden:", 
            font=("Segoe UI", 10, "bold"),
            bg="#f5faf5"
        ).grid(row=5, column=0, sticky="ew", pady=(10, 5))
        
        # Listbox voor nog te verwerken bestanden
        self.listbox_nog = tk.Listbox(
            self.right_panel, 
            height=3, 
            font=("Segoe UI", 9), 
            selectmode=tk.SINGLE,
            bg="white",
            fg="black"
        )
        self.listbox_nog.grid(row=6, column=0, sticky="ewns", pady=(0, 5))
        
        # Voltooid bestanden
        tk.Label(
            self.right_panel, 
            text="✅ Voltooid:", 
            font=("Segoe UI", 10, "bold"),
            bg="#f5faf5"
        ).grid(row=7, column=0, sticky="ew", pady=(10, 5))
        
        # Listbox voor voltooid bestanden
        self.listbox_voltooid = tk.Listbox(
            self.right_panel, 
            height=3, 
            font=("Segoe UI", 9), 
            selectmode=tk.SINGLE,
            bg="white",
            fg="black"
        )
        self.listbox_voltooid.grid(row=8, column=0, sticky="ewns", pady=(0, 5))
        
        # Bind selectie events
        self.listbox_nog.bind('<<ListboxSelect>>', self.on_listbox_select)
        self.listbox_voltooid.bind('<<ListboxSelect>>', self.on_listbox_select)
    
    def style_dropdown(self, dropdown):
        """Pas dropdown styling toe zoals in versie 1.9.4"""
        dropdown.config(
            font=("Segoe UI", 9),
            bg="white",
            fg="black",
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground="#cccccc",
            highlightcolor="#cccccc",
            width=15,
            activebackground="white",
            activeforeground="black"
        )
    
    def on_taal_change(self, *args):
        """Handle taal wijziging"""
        try:
            selected_text = self.taal_var.get()
            logger.log_debug(f"🌍 Taal gekozen: {selected_text}")
            self.update_status(f"🌍 Taal ingesteld: {selected_text}")
        except Exception as e:
            logger.log_debug(f"❌ Fout bij taal wijziging: {e}")
    
    def on_content_type_change(self, *args):
        """Handle content type wijziging"""
        try:
            selected_type = self.content_type_var.get()
            logger.log_debug(f"📺 Content type gekozen: {selected_type}")
            self.update_status(f"📺 Content type: {selected_type}")
        except Exception as e:
            logger.log_debug(f"❌ Fout bij content type wijziging: {e}")
    
    def update_cpu_limit(self, *args):
        """Update CPU limiet"""
        try:
            cpu_limit = self.cpu_limit_var.get()
            self.cpu_percent_label.config(text=f"{cpu_limit}%")
            
            # Bereken worker count op basis van CPU limiet
            if cpu_limit <= 25:
                worker_count = 1
            elif cpu_limit <= 50:
                worker_count = 2
            elif cpu_limit <= 75:
                worker_count = 4
            else:
                worker_count = 6
            
            logger.log_debug(f"⚡ CPU limiet aangepast naar: {cpu_limit}% ({worker_count} workers)")
        except Exception as e:
            logger.log_debug(f"❌ Fout bij update CPU limiet: {e}")
    
    def update_cpu_load(self):
        """Update CPU load display"""
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=0.1)
            cpu_limit = self.cpu_limit_var.get()
            
            # Kleur logica
            color = "#44aa44" if cpu_percent <= cpu_limit else "#ff4444"
            self.cpu_load_label.config(text=f"Huidig: {cpu_percent:.0f}%", fg=color)
        except:
            self.cpu_load_label.config(text="Huidig: --")
        
        # Update elke 10 seconden
        self.root.after(10000, self.update_cpu_load)
    
    def periodic_translator_update(self):
        """Update vertaler status periodiek"""
        try:
            self.translator_status_label.config(text=f"Vertaler: {translator.get_current_service().upper()}")
        except:
            pass
        
        # Update elke 10 seconden
        self.root.after(10000, self.periodic_translator_update)
    
    def on_listbox_select(self, event):
        """Handle listbox selectie"""
        try:
            widget = event.widget
            selection = widget.curselection()
            if selection:
                selected_index = selection[0]
                selected_item = widget.get(selected_index)
                self.info_label.config(text=f"📄 {selected_item}", fg="#2c3e50")
                logger.log_debug(f"📄 Bestand geselecteerd: {selected_item}")
            else:
                self.info_label.config(text="📄 Geen video gekozen", fg="gray")
        except Exception as e:
            logger.log_debug(f"❌ Fout bij listbox selectie: {e}")
    
    def create_panels(self):
        """Legacy methode - niet meer gebruikt in v1.9.4 layout"""
        pass
    

    
    def create_status_bar(self):
        """Maak de statusbalk zoals in versie 1.9.4"""
        # Status frame
        self.status_bar = tk.Frame(self.root, bg="#f0f8f0", relief="sunken", bd=1)
        self.status_bar.grid(row=1, column=0, sticky="ew")
        
        # Status label
        self.status_text = tk.StringVar(value="Klaar")
        self.status_label = tk.Label(
            self.status_bar,
            textvariable=self.status_text,
            font=("Segoe UI", 9),
            bg="#f0f8f0",
            fg="#2c2c2c"
        )
        self.status_label.pack(side=tk.LEFT, padx=5, pady=2)
    
    # Menu handlers
    def add_file(self):
        """Voeg bestand toe zoals in versie 1.9.4"""
        file_path = filedialog.askopenfilename(
            title="Selecteer video bestand",
            filetypes=[
                ("Video bestanden", "*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm"),
                ("Audio bestanden", "*.mp3 *.wav *.flac *.m4a *.aac"),
                ("Alle bestanden", "*.*")
            ]
        )
        if file_path:
            self.voeg_bestand_toe_pad(file_path)
    
    def add_folder(self):
        """Voeg map toe zoals in versie 1.9.4"""
        folder_path = filedialog.askdirectory(title="Selecteer map met video's")
        if folder_path:
            self.voeg_map_toe_paden(folder_path)
    
    def remove_selected(self):
        """Verwijder geselecteerd bestand zoals in versie 1.9.4"""
        selection = self.listbox_nog.curselection()
        if selection:
            selected_index = selection[0]
            self.listbox_nog.delete(selected_index)
            logger.log_debug("🗑️ Geselecteerd bestand verwijderd")
            self.update_status("Geselecteerd bestand verwijderd")
    
    def clear_list(self):
        """Wis hele lijst zoals in versie 1.9.4"""
        self.listbox_nog.delete(0, tk.END)
        logger.log_debug("🗑️ Hele lijst gewist")
        self.update_status("Lijst gewist")
    
    def voeg_bestand_toe_pad(self, file_path: str):
        """Voeg bestand toe aan lijst"""
        filename = os.path.basename(file_path)
        self.listbox_nog.insert(tk.END, filename)
        logger.log_debug(f"📁 Bestand toegevoegd: {filename}")
        self.update_status(f"Bestand toegevoegd: {filename}")
    
    def voeg_map_toe_paden(self, folder_path: str):
        """Voeg alle video bestanden uit map toe"""
        video_extensions = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'}
        added_count = 0
        
        try:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    _, ext = os.path.splitext(filename.lower())
                    if ext in video_extensions:
                        self.listbox_nog.insert(tk.END, filename)
                        added_count += 1
            
            logger.log_debug(f"📂 {added_count} bestanden toegevoegd uit map: {folder_path}")
            self.update_status(f"{added_count} bestanden toegevoegd")
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij toevoegen map: {e}")
            messagebox.showerror("Fout", f"Fout bij toevoegen map: {e}")
    
    def save_list(self):
        """Sla lijst op"""
        logger.log_debug("💾 Lijst opslaan (nog niet geïmplementeerd)")
        messagebox.showinfo("Info", "Lijst opslaan nog niet geïmplementeerd")
    
    def load_list(self):
        """Laad lijst"""
        logger.log_debug("📂 Lijst laden (nog niet geïmplementeerd)")
        messagebox.showinfo("Info", "Lijst laden nog niet geïmplementeerd")
    
    def start_processing(self):
        """Start verwerking zoals in versie 1.9.4"""
        logger.log_debug("▶️ Start ondertiteling")
        
        # Controleer of er bestanden zijn
        if self.listbox_nog.size() == 0:
            messagebox.showwarning("Waarschuwing", "Geen bestanden om te verwerken")
            return
        
        # Start batch verwerking
        self.start_batch_verwerking()
    
    def start_batch_verwerking(self):
        """Start batch verwerking zoals in versie 1.9.4"""
        logger.log_debug("🚀 Batch verwerking gestart")
        self.update_status("Batch verwerking gestart...")
        
        # Hier zou je de daadwerkelijke verwerking kunnen starten
        # Voor nu tonen we een bericht
        messagebox.showinfo("Info", "Batch verwerking gestart (nog niet volledig geïmplementeerd)")
    
    def stop_processing(self):
        """Stop verwerking zoals in versie 1.9.4 (KILL SWITCH)"""
        logger.log_debug("⏹️ KILL SWITCH geactiveerd")
        self.update_status("Verwerking gestopt")
        
        # Hier zou je alle lopende processen kunnen stoppen
        messagebox.showinfo("Info", "KILL SWITCH geactiveerd - alle verwerking gestopt")
    
    def batch_processing(self):
        """Batch verwerking zoals in versie 1.9.4"""
        logger.log_debug("📦 Batch verwerking via menu")
        self.start_batch_verwerking()
    
    def auto_processing(self):
        """Auto verwerking"""
        logger.log_debug("🤖 Auto verwerking (nog niet geïmplementeerd)")
        messagebox.showinfo("Info", "Auto verwerking nog niet geïmplementeerd")
    
    def show_config(self):
        """Toon configuratievenster"""
        logger.log_debug("⚙️ Configuratievenster wordt geopend")
        config_window = ConfigWindow(self.root)
        config_window.set_callback(self._on_config_saved)
        config_window.show()
    
    def change_theme(self, theme_name: str):
        """Verander thema zoals in versie 1.9.4"""
        # Pas thema toe op alle widgets
        self.apply_theme_to_widgets(theme_name)
        logger.log_debug(f"🎨 Thema gewijzigd naar: {theme_name}")
    
    def apply_theme_to_widgets(self, theme_name: str):
        """Pas thema toe op alle widgets"""
        try:
            # Definieer thema kleuren
            theme_colors = {
                "dark": {
                    "bg": "#2c2c2c",
                    "panel_bg": "#3c3c3c",
                    "fg": "#ffffff",
                    "button_bg": "#4a4a4a",
                    "button_fg": "#ffffff"
                },
                "light": {
                    "bg": "#f0f8f0",
                    "panel_bg": "#f5faf5",
                    "fg": "#2c2c2c",
                    "button_bg": "#e0e0e0",
                    "button_fg": "#2c2c2c"
                },
                "blue": {
                    "bg": "#e3f2fd",
                    "panel_bg": "#f3f9ff",
                    "fg": "#1a237e",
                    "button_bg": "#2196f3",
                    "button_fg": "#ffffff"
                }
            }
            
            colors = theme_colors.get(theme_name, theme_colors["light"])
            
            # Pas thema toe op hoofdvenster
            self.root.configure(bg=colors["bg"])
            self.main_frame.configure(bg=colors["bg"])
            
            # Pas thema toe op panels
            if hasattr(self, 'left_panel'):
                self.left_panel.configure(bg=colors["panel_bg"], fg=colors["fg"])
            if hasattr(self, 'right_panel'):
                self.right_panel.configure(bg=colors["panel_bg"], fg=colors["fg"])
            
            # Pas thema toe op status bar
            if hasattr(self, 'status_bar'):
                self.status_bar.configure(bg=colors["bg"])
                self.status_label.configure(bg=colors["bg"], fg=colors["fg"])
            
            logger.log_debug(f"🎨 Thema '{theme_name}' toegepast")
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij toepassen thema: {e}")
    
    def show_log(self):
        """Toon log viewer"""
        logger.log_debug("📋 Log viewer wordt geopend")
        log_viewer = LogViewer(self.root)
        log_viewer.show()
    
    def performance_test(self):
        """Performance test"""
        logger.log_debug("📊 Menu: Performance test")
        try:
            # Start performance tracking
            from ..models.performance_tracker import performance_tracker
            performance_tracker.start_tracking()
            
            # Voer een korte test uit
            import time
            time.sleep(2)
            
            # Genereer rapport
            report = performance_tracker.generate_report()
            
            # Toon resultaat
            report_text = f"""
Performance Test Resultaat:

CPU Gebruik: {report.get('cpu_usage', 'N/A')}%
Geheugen Gebruik: {report.get('memory_usage', 'N/A')}%
Test Tijd: {report.get('test_duration', 'N/A')} seconden

Whisper Model: {'Geladen' if whisper_processor.is_model_loaded() else 'Niet geladen'}
FFmpeg: {'Beschikbaar' if audio_processor.is_ffmpeg_available() else 'Niet beschikbaar'}
Vertaler: {translator.get_current_service()}
            """
            
            messagebox.showinfo("Performance Test", report_text)
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij performance test: {e}")
            messagebox.showerror("Fout", f"Performance test gefaald: {e}")
    
    def cuda_test(self):
        """CUDA test"""
        logger.log_debug("🔧 CUDA test (nog niet geïmplementeerd)")
        messagebox.showinfo("Info", "CUDA test nog niet geïmplementeerd")
    
    def whisper_diagnose(self):
        """Whisper diagnose"""
        logger.log_debug("🎤 Whisper diagnose (nog niet geïmplementeerd)")
        messagebox.showinfo("Info", "Whisper diagnose nog niet geïmplementeerd")
    
    def show_about(self):
        """Toon over venster"""
        about_text = """
        Magic Time Studio v2.0
        
        Een geavanceerde applicatie voor automatische
        ondertiteling en vertaling van video's.
        
        Modulaire versie - Ontwikkeld met Python en Tkinter
        
        © 2024 Magic Time Studio Team
        """
        messagebox.showinfo("Over Magic Time Studio", about_text)
    
    def show_docs(self):
        """Toon documentatie"""
        logger.log_debug("📚 Documentatie (nog niet geïmplementeerd)")
        messagebox.showinfo("Info", "Documentatie nog niet geïmplementeerd")
    
    def _on_file_added(self, file_path: str):
        """Callback voor bestand toegevoegd"""
        logger.log_debug(f"📁 Bestand toegevoegd in hoofdvenster: {file_path}")
        self.update_status(f"Bestand toegevoegd: {os.path.basename(file_path)}")
    
    def _on_file_removed(self, file_path: str):
        """Callback voor bestand verwijderd"""
        logger.log_debug(f"🗑️ Bestand verwijderd in hoofdvenster: {file_path}")
        self.update_status(f"Bestand verwijderd: {os.path.basename(file_path)}")
    
    def _on_file_selected(self, file_path: str):
        """Callback voor bestand geselecteerd"""
        logger.log_debug(f"📋 Bestand geselecteerd in hoofdvenster: {file_path}")
        self.update_status(f"Geselecteerd: {os.path.basename(file_path)}")
        
        # Update processing panel met geselecteerde bestanden
        if hasattr(self, 'processing_panel'):
            selected_files = self.input_panel.get_selected_files()
            self.processing_panel.set_file_list(selected_files)
    
    def _on_settings_changed(self, settings: dict):
        """Callback voor instellingen gewijzigd"""
        logger.log_debug(f"⚙️ Instellingen gewijzigd in hoofdvenster: {settings}")
        self.update_status("Instellingen bijgewerkt")
    
    def _on_start_processing(self):
        """Callback voor start verwerking"""
        logger.log_debug("▶️ Verwerking gestart vanuit hoofdvenster")
        self.update_status("Verwerking gestart...")
        # Update processing panel status
        if hasattr(self, 'processing_panel'):
            self.processing_panel.set_processing_state(True)
    
    def _on_stop_processing(self):
        """Callback voor stop verwerking"""
        logger.log_debug("⏹️ Verwerking gestopt vanuit hoofdvenster")
        self.update_status("Verwerking gestopt")
        # Update processing panel status
        if hasattr(self, 'processing_panel'):
            self.processing_panel.set_processing_state(False)
    
    def _on_file_processed(self, file_path: str, result: dict):
        """Callback voor verwerkt bestand"""
        logger.log_debug(f"✅ Bestand verwerkt: {os.path.basename(file_path)}")
        self.update_status(f"Verwerkt: {os.path.basename(file_path)}")
        
        # Toon resultaat
        if result.get("success"):
            output_files = result.get("output_files", {})
            if output_files:
                file_count = len(output_files)
                messagebox.showinfo("Succes", f"Bestand verwerkt!\n{file_count} output bestand(en) gegenereerd.")
        else:
            error_msg = result.get("error", "Onbekende fout")
            messagebox.showerror("Fout", f"Fout bij verwerken: {error_msg}")
    
    def _on_config_saved(self, config: dict):
        """Callback voor configuratie opgeslagen"""
        logger.log_debug(f"💾 Configuratie opgeslagen in hoofdvenster: {config}")
        self.update_status("Configuratie opgeslagen")
        
        # Pas thema toe als gewijzigd
        if "theme" in config:
            theme_manager.apply_theme(self.root, config["theme"])
    
    def on_closing(self):
        """Handle venster sluiten"""
        logger.log_debug("👋 Hoofdvenster wordt gesloten")
        self.root.quit()
    
    # Public methods
    def update_status(self, message: str):
        """Update statusbalk"""
        self.status_text.set(message)
        logger.log_debug(f"📊 Status update: {message}")
    
    def update_progress(self, value: float):
        """Update voortgangsbalk"""
        self.progress_bar["value"] = value
        gui_updater.schedule_gui_update(lambda: None)  # Force update
    
    def set_callbacks(self, on_file_selected=None, on_start_processing=None, on_stop_processing=None):
        """Zet callbacks voor events"""
        self.on_file_selected = on_file_selected
        self.on_start_processing = on_start_processing
        self.on_stop_processing = on_stop_processing 