"""
Log viewer voor Magic Time Studio
Toont live logs in een apart venster
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable
import threading
import time
from ..core.logging import logger
from ..core.utils import gui_updater
from .themes import theme_manager

class LogViewer:
    """Log viewer venster voor live log weergave"""
    
    def __init__(self, parent: tk.Tk):
        self.parent = parent
        self.window = None
        self.log_text = None
        self.scrollbar = None
        self.auto_scroll = True
        self.is_running = False
        self.update_thread = None
        
        self.create_window()
    
    def create_window(self):
        """Maak het log viewer venster"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Log Viewer - Magic Time Studio")
        self.window.geometry("900x600")
        self.window.minsize(600, 400)
        
        # Maak venster niet-modal
        self.window.transient(self.parent)
        
        # Pas thema toe
        theme_manager.apply_theme(self.window, theme_manager.get_current_theme())
        
        # Protocol handlers
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Maak interface
        self.create_interface()
        
        # Start log monitoring
        self.start_log_monitoring()
        
        logger.log_debug("📋 Log viewer aangemaakt")
    
    def create_interface(self):
        """Maak de interface"""
        # Hoofdframe
        main_frame = theme_manager.create_styled_frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Titel en knoppen frame
        header_frame = theme_manager.create_styled_frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Titel
        title_label = theme_manager.create_styled_label(
            header_frame,
            "📋 Live Log Viewer",
            font=("Arial", 12, "bold")
        )
        title_label.pack(side=tk.LEFT)
        
        # Knoppen frame
        button_frame = theme_manager.create_styled_frame(header_frame)
        button_frame.pack(side=tk.RIGHT)
        
        # Clear knop
        clear_button = theme_manager.create_styled_button(
            button_frame,
            "🗑️ Wissen",
            self.clear_log
        )
        clear_button.pack(side=tk.LEFT, padx=2)
        
        # Auto scroll knop
        self.auto_scroll_button = theme_manager.create_styled_button(
            button_frame,
            "📌 Auto Scroll: AAN",
            self.toggle_auto_scroll
        )
        self.auto_scroll_button.pack(side=tk.LEFT, padx=2)
        
        # Refresh knop
        refresh_button = theme_manager.create_styled_button(
            button_frame,
            "🔄 Ververs",
            self.refresh_log
        )
        refresh_button.pack(side=tk.LEFT, padx=2)
        
        # Log frame
        log_frame = theme_manager.create_styled_frame(main_frame)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        self.scrollbar = tk.Scrollbar(log_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Log text widget
        self.log_text = tk.Text(
            log_frame,
            yscrollcommand=self.scrollbar.set,
            bg=theme_manager.colors["frame"],
            fg=theme_manager.colors["fg"],
            font=("Consolas", 9),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.log_text.yview)
        
        # Status bar
        status_frame = theme_manager.create_styled_frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = theme_manager.create_styled_label(
            status_frame,
            "Klaar voor logs...",
            font=("Arial", 9)
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Bind events
        self.log_text.bind("<MouseWheel>", self.on_mouse_wheel)
        self.log_text.bind("<Button-1>", self.on_click)
    
    def start_log_monitoring(self):
        """Start log monitoring thread"""
        self.is_running = True
        self.update_thread = threading.Thread(target=self.log_monitor_loop, daemon=True)
        self.update_thread.start()
    
    def log_monitor_loop(self):
        """Log monitoring loop"""
        log_queue = logger.get_log_queue()
        
        while self.is_running:
            try:
                # Probeer log bericht te krijgen (niet-blocking)
                try:
                    log_entry = log_queue.get_nowait()
                    self.add_log_message(log_entry)
                except:
                    pass
                
                time.sleep(0.1)  # 10 FPS update rate
                
            except Exception as e:
                print(f"❌ Fout in log monitoring: {e}")
                break
    
    def add_log_message(self, message: str):
        """Voeg log bericht toe aan viewer"""
        def update():
            try:
                self.log_text.config(state=tk.NORMAL)
                
                # Voeg timestamp toe als niet aanwezig
                if isinstance(message, str) and not message.startswith("["):
                    from datetime import datetime
                    timestamp = datetime.now().strftime("[%H:%M:%S]")
                    formatted_message = f"{timestamp} {message}\n"
                else:
                    formatted_message = f"{message}\n"
                
                self.log_text.insert(tk.END, formatted_message)
                
                # Auto scroll naar beneden
                if self.auto_scroll:
                    self.log_text.see(tk.END)
                
                # Beperk aantal regels (houd laatste 1000 regels)
                lines = self.log_text.get("1.0", tk.END).split('\n')
                if len(lines) > 1000:
                    self.log_text.delete("1.0", f"{len(lines) - 1000}.0")
                
                self.log_text.config(state=tk.DISABLED)
                
                # Update status
                self.update_status()
                
            except Exception as e:
                print(f"❌ Fout bij toevoegen log bericht: {e}")
        
        # Schedule GUI update
        gui_updater.schedule_gui_update(update)
    
    def clear_log(self):
        """Wis alle logs"""
        if messagebox.askyesno("Bevestig", "Weet je zeker dat je alle logs wilt wissen?"):
            self.log_text.config(state=tk.NORMAL)
            self.log_text.delete("1.0", tk.END)
            self.log_text.config(state=tk.DISABLED)
            self.update_status()
            logger.log_debug("🗑️ Logs gewist")
    
    def refresh_log(self):
        """Ververs log display"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        
        # Voeg wat voorbeeld logs toe
        self.log_text.insert(tk.END, "[11:00:00] 📋 Log viewer gestart\n")
        self.log_text.insert(tk.END, "[11:00:01] ✅ Alle modules geladen\n")
        self.log_text.insert(tk.END, "[11:00:02] 🎨 Thema toegepast\n")
        self.log_text.insert(tk.END, "[11:00:03] 📁 Input panel klaar\n")
        self.log_text.insert(tk.END, "[11:00:04] ⚙️ Processing panel klaar\n")
        
        self.log_text.config(state=tk.DISABLED)
        self.update_status()
        logger.log_debug("🔄 Log display verversd")
    
    def toggle_auto_scroll(self):
        """Toggle auto scroll"""
        self.auto_scroll = not self.auto_scroll
        status = "AAN" if self.auto_scroll else "UIT"
        self.auto_scroll_button.config(text=f"📌 Auto Scroll: {status}")
        
        if self.auto_scroll:
            self.log_text.see(tk.END)
        
        logger.log_debug(f"📌 Auto scroll: {status}")
    
    def on_mouse_wheel(self, event):
        """Handle mouse wheel scroll"""
        # Disable auto scroll when user scrolls manually
        if event.delta != 0:
            self.auto_scroll = False
            self.auto_scroll_button.config(text="📌 Auto Scroll: UIT")
    
    def on_click(self, event):
        """Handle mouse click"""
        # Disable auto scroll when user clicks
        self.auto_scroll = False
        self.auto_scroll_button.config(text="📌 Auto Scroll: UIT")
    
    def update_status(self):
        """Update status label"""
        try:
            # Tel aantal regels
            lines = self.log_text.get("1.0", tk.END).split('\n')
            line_count = len(lines) - 1  # -1 voor lege regel aan einde
            
            # Krijg scroll positie
            scroll_pos = self.log_text.yview()
            scroll_percent = int(scroll_pos[1] * 100)
            
            status_text = f"Regels: {line_count} | Scroll: {scroll_percent}% | Auto: {'AAN' if self.auto_scroll else 'UIT'}"
            self.status_label.config(text=status_text)
            
        except Exception as e:
            self.status_label.config(text=f"Status fout: {e}")
    
    def on_closing(self):
        """Handle venster sluiten"""
        self.is_running = False
        logger.log_debug("👋 Log viewer wordt gesloten")
        self.window.destroy()
    
    def show(self):
        """Toon het log viewer venster"""
        self.window.deiconify()
        self.window.focus_set()
    
    def add_test_message(self, message: str):
        """Voeg test bericht toe (voor debugging)"""
        self.add_log_message(message) 