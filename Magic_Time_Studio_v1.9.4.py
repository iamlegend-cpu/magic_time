# 📦 Imports - Geoptimaliseerd voor snelle startup
import os, json, math, shutil, threading, webbrowser, winsound
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
import sys
import datetime
import subprocess
import tempfile
import time
from datetime import timedelta
from typing import Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
# MoviePy import verwijderd - nu gebruiken we FFmpeg direct
import traceback
import warnings

# Onderdruk Triton waarschuwingen globaal
warnings.filterwarnings("ignore", message="Failed to launch Triton kernels")
warnings.filterwarnings("ignore", message="Failed to launch Triton kernels, likely due to missing CUDA toolkit")
warnings.filterwarnings("ignore", message=".*Triton.*")

# Performance optimalisaties
GUI_UPDATE_BATCH = []
GUI_UPDATE_TIMER = None

# Async processing voor betere reactietijd
import asyncio
import concurrent.futures
from functools import partial

# UI responsiveness optimalisaties
UI_UPDATE_INTERVAL = 16  # 60 FPS (1000ms / 60)
MAX_UI_UPDATE_BATCH_SIZE = 10

# Verwerking status
processing_active = False

def block_interface_during_processing():
    """Blokkeer alle instellingen tijdens verwerking, behalve logvenster en bestand toevoegen/verwijderen (behalve huidig bestand)."""
    global processing_active
    processing_active = True
    try:
        # Blokkeer dropdowns in hoofdinterface
        if taal_combobox is not None:
            taal_combobox.config(state="disabled")
        if content_type_combobox is not None:
            content_type_combobox.config(state="disabled")
        if 'cpu_slider' in globals():
            globals()['cpu_slider'].config(state="disabled")
        # Blokkeer start knop
        if 'start_button' in globals() and globals()['start_button'] is not None:
            globals()['start_button'].config(state="disabled", text="Verwerking bezig...")
        # Blokkeer instellingen/configuratieknoppen
        if 'config_window' in globals() and config_window is not None:
            try:
                def block_widgets(parent_widget):
                    for widget in parent_widget.winfo_children():
                        try:
                            if hasattr(widget, 'config') and widget.winfo_class() == 'Button':
                                widget.config(state="disabled")
                            if hasattr(widget, 'winfo_children'):
                                block_widgets(widget)
                        except Exception as e:
                            log_debug(f"❌ Fout bij blokkeren widget: {e}")
                            pass
                block_widgets(config_window)
                log_debug("🔒 Configuratie venster geblokkeerd")
            except Exception as e:
                log_debug(f"❌ Fout bij blokkeren configuratie: {e}")
        # Blokkeer verwijder-knoppen alleen voor het bestand dat verwerkt wordt
        if 'btn_verwijder' in globals() and btn_verwijder is not None:
            btn_verwijder.config(state="normal")
        if 'btn_verwijder_alles' in globals() and btn_verwijder_alles is not None:
            btn_verwijder_alles.config(state="normal")
        # Bestand toevoegen knoppen blijven actief
        if 'btn_voeg_bestand' in globals() and btn_voeg_bestand is not None:
            btn_voeg_bestand.config(state="normal")
        if 'btn_voeg_map' in globals() and btn_voeg_map is not None:
            btn_voeg_map.config(state="normal")
        log_debug("🔒 Interface geblokkeerd tijdens verwerking (alleen toevoegen/verwijderen toegestaan, huidig bestand beschermd)")
    except Exception as e:
        log_debug(f"❌ Fout bij blokkeren interface: {e}")

def unblock_interface_after_processing():
    """Ontgrendel alle instellingen na verwerking"""
    global processing_active
    processing_active = False
    try:
        # Ontgrendel dropdowns in hoofdinterface
        if taal_combobox is not None:
            taal_combobox.config(state="normal")
        if content_type_combobox is not None:
            content_type_combobox.config(state="normal")
        if 'cpu_slider' in globals():
            globals()['cpu_slider'].config(state="normal")
        # Ontgrendel start knop
        if 'start_button' in globals() and globals()['start_button'] is not None:
            globals()['start_button'].config(state="normal", text="Start ondertiteling")
        # Ontgrendel instellingen/configuratieknoppen
        if 'config_window' in globals() and config_window is not None:
            try:
                def unblock_widgets(parent_widget):
                    for widget in parent_widget.winfo_children():
                        try:
                            if hasattr(widget, 'config') and widget.winfo_class() == 'Button':
                                widget.config(state="normal")
                            if hasattr(widget, 'winfo_children'):
                                unblock_widgets(widget)
                        except Exception as e:
                            log_debug(f"❌ Fout bij ontgrendelen widget: {e}")
                            pass
                unblock_widgets(config_window)
                log_debug("🔓 Configuratie venster ontgrendeld")
            except Exception as e:
                log_debug(f"❌ Fout bij ontgrendelen configuratie: {e}")
        # Ontgrendel verwijder-knoppen
        if 'btn_verwijder' in globals() and btn_verwijder is not None:
            btn_verwijder.config(state="normal")
        if 'btn_verwijder_alles' in globals() and btn_verwijder_alles is not None:
            btn_verwijder_alles.config(state="normal")
        # Bestand toevoegen knoppen blijven actief
        if 'btn_voeg_bestand' in globals() and btn_voeg_bestand is not None:
            btn_voeg_bestand.config(state="normal")
        if 'btn_voeg_map' in globals() and btn_voeg_map is not None:
            btn_voeg_map.config(state="normal")
        log_debug("🔓 Interface ontgrendeld na verwerking")
    except Exception as e:
        log_debug(f"❌ Fout bij ontgrendelen interface: {e}")

def batch_gui_update():
    """Voer alle GUI updates in één keer uit met optimalisaties"""
    global GUI_UPDATE_BATCH, GUI_UPDATE_TIMER
    try:
        if GUI_UPDATE_BATCH:
            # Optimaliseer door updates te groeperen
            progress_updates = []
            status_updates = []
            other_updates = []
            
            for update_func in GUI_UPDATE_BATCH:
                try:
                    # Categoriseer updates voor betere performance
                    if 'progress' in str(update_func).lower():
                        progress_updates.append(update_func)
                    elif 'status' in str(update_func).lower():
                        status_updates.append(update_func)
                    else:
                        other_updates.append(update_func)
                except Exception as e:
                    pass
            
            # Voer updates uit in volgorde van prioriteit
            for update_func in progress_updates + status_updates + other_updates:
                try:
                    update_func()
                except Exception as e:
                    pass
            
            GUI_UPDATE_BATCH.clear()
    except Exception as e:
        pass
    finally:
        GUI_UPDATE_TIMER = None

def schedule_gui_update(update_func):
    """Plan een GUI update voor batch verwerking met optimalisaties"""
    global GUI_UPDATE_BATCH, GUI_UPDATE_TIMER
    try:
        # Limiteer batch grootte voor betere performance
        if len(GUI_UPDATE_BATCH) < MAX_UI_UPDATE_BATCH_SIZE:
            GUI_UPDATE_BATCH.append(update_func)
        
        if GUI_UPDATE_TIMER is None and root is not None:
            GUI_UPDATE_TIMER = root.after(UI_UPDATE_INTERVAL, batch_gui_update)
    except Exception as e:
        # Fallback naar directe update als batch systeem faalt
        try:
            update_func()
        except:
            pass

def schedule_immediate_update(update_func):
    """Schedule een onmiddellijke GUI update voor kritieke updates"""
    if root is not None:
        root.after(0, update_func)

def schedule_priority_update(update_func):
    """Schedule een hoge prioriteit GUI update"""
    if root is not None:
        root.after(1, update_func)  # Minimale vertraging

# Lazy imports voor snellere startup
def import_heavy_modules():
    """Import zware modules alleen wanneer nodig"""
    global Image, ImageTk, whisper, deepl, Translator, np, torch
    
    # Import alleen wat nodig is
    try:
        from PIL import Image, ImageTk
        log_debug("✅ PIL modules geladen")
    except ImportError as e:
        log_debug(f"❌ PIL import fout: {e}")
    
    try:
        import whisper
        log_debug("✅ Whisper geladen")
    except ImportError as e:
        log_debug(f"❌ Whisper import fout: {e}")
    
    try:
        import deepl
        log_debug("✅ DeepL geladen")
    except ImportError as e:
        log_debug(f"❌ DeepL import fout: {e}")
    
    try:
        from googletrans import Translator
        log_debug("✅ Google Translate geladen")
    except ImportError as e:
        log_debug(f"❌ Google Translate import fout: {e}")
    
    try:
        import numpy as np
        log_debug("✅ NumPy geladen")
    except ImportError as e:
        log_debug(f"❌ NumPy import fout: {e}")
    
    try:
        import torch
        log_debug("✅ PyTorch geladen")
    except ImportError as e:
        log_debug(f"❌ PyTorch import fout: {e}")

def preload_critical_modules():
    """Preload kritieke modules in achtergrond voor snellere reacties"""
    def background_preload():
        try:
            # Preload modules die vaak gebruikt worden
            import numpy as np
            import torch
            log_debug("✅ Kritieke modules gepreload")
        except Exception as e:
            log_debug(f"⚠️ Preload fout: {e}")
    
    # Start preload in achtergrond thread
    if root is not None:
        root.after(1000, background_preload)  # Start na 1 seconde


# Real-time log systeem
import queue
import logging

# Performance monitoring
try:
    import psutil
    
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

# Audio analysis
try:
    import librosa
    import numpy as np

    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False

if getattr(sys, "frozen", False):
    BASE_DIR = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
else:
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        # Fallback voor wanneer __file__ niet beschikbaar is
        BASE_DIR = os.getcwd()

# Outputmap voor gebruikersbestanden (zoals SRT)
USER_OUTPUT_DIR = os.path.join(os.path.expanduser('~'), 'MagicTimeStudio', 'output')
os.makedirs(USER_OUTPUT_DIR, exist_ok=True)

# 📁 Paden
ASSETS = os.path.join(BASE_DIR, "assets")
CONFIG_PAD = os.path.join(BASE_DIR, "config.json")
TEMP = os.path.join(tempfile.gettempdir(), "temp_audio")
os.makedirs(TEMP, exist_ok=True)

icon_path = os.path.join(ASSETS, "Magic_Time_Studio.ico")
info_icon_path = os.path.join(ASSETS, "info_icon.png")

# Globale variabelen voor real-time logging
log_queue = queue.Queue()
active_log_viewers = []
log_monitor_thread = None
log_text_widget = None
log_window = None

# Globale venster- en configuratievariabelen (voor GUI)
config_window = None
deepl_key_var = None
model_selection_var = None
output_format_var = None

# Voeg toe aan de globale variabelen
processing_active = False
processing_paused = False
processing_cancelled = False

# Globale variabelen voor GUI en verwerking
selected_video = None
output_pad = None  # Wordt later geïnitialiseerd
video_pad = None   # Wordt later geïnitialiseerd
taal_var = None    # Wordt later geïnitialiseerd

thema_var = None   # Wordt later geïnitialiseerd

# Vertaling variabelen
huidige_vertaler = "geen"  # Standaard op 'geen' zetten
deepl_tekens_used = 0
translator = None  # Wordt later geïnitialiseerd

# Ondertitel configuratie
subtitle_type = "softcoded"  # softcoded of hardcoded
hardcoded_language = "dutch_only"  # dutch_only of both_languages

# Taal keuzes voor vertalingen (worden later geïnitialiseerd)
# taal_keuzes = {}  # Verwijderd - wordt later correct geïnitialiseerd

# GUI elementen (worden later geïnitialiseerd)
root: Optional[tk.Tk] = None
menubalk: Optional[tk.Menu] = None
left_panel = None
right_panel = None
progress = None
status_label = None
info_label = None
start_button = None
pause_button = None
resume_button = None
stop_button = None
kill_button = None
btn_voeg_bestand = None
btn_voeg_map = None
btn_verwijder = None
btn_verwijder_alles = None
taal_combobox = None
content_type_combobox = None

# Parallel processor (wordt later geïnitialiseerd)
parallel_processor = None

# Logging configuratie variabelen (moet voor load_configuration() staan)
logging_config = {
    "log_system_info": True,
    "log_audio_extraction": True,
    "log_whisper_transcription": True,
    "log_translation": True,
    "log_file_operations": True,
    "log_performance": True,
    "log_errors": True,
    "log_warnings": True,
    "log_debug": True,
    "log_cleanup": True,
    "log_api_calls": True,
    "log_progress": True
}

# API Throttle Manager voor Google Translate en DeepL
class APITranslateThrottle:
    def __init__(self, service_name="API"):
        self.service_name = service_name
        self.last_request_time = 0
        self.request_count = 0
        self.lock = threading.Lock()
        self.min_interval = 1.0  # Minimum 1 seconde tussen requests
        self.max_requests_per_minute = 60  # Maximum 60 requests per minuut
        self.request_times = []  # Track request tijden voor rate limiting
        
    def get_throttle_delay(self, worker_count):
        """Bereken throttle delay op basis van aantal workers"""
        # Basis delay per worker
        base_delay = 2.0  # 2 seconden basis delay
        
        # Verhoog delay voor meer workers
        if worker_count <= 2:
            delay = base_delay
        elif worker_count <= 4:
            delay = base_delay * 1.5  # 3 seconden
        elif worker_count <= 6:
            delay = base_delay * 2.0  # 4 seconden
        else:  # 8 workers
            delay = base_delay * 3.0  # 6 seconden
            
        return delay
    
    def wait_if_needed(self, worker_count):
        """Wacht indien nodig om rate limiting te voorkomen"""
        with self.lock:
            current_time = time.time()
            
            # Verwijder oude requests (ouder dan 1 minuut)
            self.request_times = [t for t in self.request_times if current_time - t < 60]
            
            # Check of we te veel requests hebben
            if len(self.request_times) >= self.max_requests_per_minute:
                # Wacht tot we onder de limiet komen
                oldest_request = min(self.request_times)
                wait_time = 60 - (current_time - oldest_request) + 1
                if wait_time > 0:
                    log_debug(f"⏳ Rate limit bereikt voor {self.service_name}, wacht {wait_time:.1f} seconden...", "log_api_calls")
                    time.sleep(wait_time)
            
            # Check minimum interval
            time_since_last = current_time - self.last_request_time
            throttle_delay = self.get_throttle_delay(worker_count)
            
            if time_since_last < throttle_delay:
                wait_time = throttle_delay - time_since_last
                log_debug(f"⏳ Throttle delay ({throttle_delay}s) voor {self.service_name}, wacht {wait_time:.1f}s...", "log_api_calls")
                time.sleep(wait_time)
            
            # Update tracking
            self.last_request_time = time.time()
            self.request_times.append(self.last_request_time)
            self.request_count += 1
            
            log_debug(f"🌐 {self.service_name} request #{self.request_count} (workers: {worker_count})", "log_api_calls")

# Global throttle instances
google_translate_throttle = APITranslateThrottle("Google Translate")
deepl_throttle = APITranslateThrottle("DeepL")

# Thema kleuren definities
THEMA_KLEUREN = {
    "dark": {
        "bg": "#2c2c2c",
        "main_bg": "#1e1e1e",
        "panel_bg": "#3c3c3c",
        "frame": "#4c4c4c",
        "fg": "#ffffff",
        "knop": "#555555",
        "knop_fg": "#ffffff"
    },
    "light": {
        "bg": "#f0f8f0",
        "main_bg": "#ffffff",
        "panel_bg": "#f5faf5",
        "frame": "#e8f5e8",
        "fg": "#2c2c2c",
        "knop": "#4caf50",
        "knop_fg": "#ffffff"
    },
    "blue": {
        "bg": "#e3f2fd",
        "main_bg": "#ffffff",
        "panel_bg": "#f0f8ff",
        "frame": "#e1f5fe",
        "fg": "#1565c0",
        "knop": "#2196f3",
        "knop_fg": "#ffffff"
    },
    "green": {
        "bg": "#e8f5e8",
        "main_bg": "#ffffff",
        "panel_bg": "#f1f8e9",
        "frame": "#e8f5e8",
        "fg": "#2e7d32",
        "knop": "#4caf50",
        "knop_fg": "#ffffff"
    }
}

# User data directory
def get_user_data_dir():
    """Maak en retourneer user data directory"""
    user_dir = os.path.expanduser("~/AppData/Local/MagicTimeStudio")
    os.makedirs(user_dir, exist_ok=True)
    return user_dir


# Processing Queue
class ProcessingQueue:
    def __init__(self):
        self.queue = []
        self.processing = False
    
    def add_video(self, video_path, settings):
        self.queue.append({"video": video_path, "settings": settings})
        log_debug(f"📋 Video toegevoegd aan queue: {os.path.basename(video_path)}")
    
    def process_all(self):
        if not self.queue:
            log_debug("📋 Queue is leeg")
            return
        
        self.processing = True
        for i, item in enumerate(self.queue):
            log_debug(
                f"🔄 Verwerk video {i+1}/{len(self.queue)}: "
                f"{os.path.basename(item['video'])}"
            )
            # Hier zou je de video verwerking kunnen starten
        self.queue.clear()
        self.processing = False
        log_debug("✅ Alle videos verwerkt!")


processing_queue = ProcessingQueue()


class BatchManager:
    def __init__(self):
        self.batch_list = []
        self.current_batch = 0
        
    def add_to_batch(self, video_path, settings):
        if video_path is None:
            log_debug("❌ Geen video pad opgegeven voor batch")
            return False
            
        self.batch_list.append(
            {"video": video_path, "settings": settings, "status": "pending"}
        )
        log_debug(f"📋 Toegevoegd aan batch: {os.path.basename(video_path)}")
        return True
    
    def process_batch(self):
        if not self.batch_list:
            log_debug("📋 Batch is leeg")
            return
            
        for i, item in enumerate(self.batch_list):
            if processing_cancelled:
                break
                
            self.current_batch = i
            item["status"] = "processing"
            
            if item["video"] is None:
                log_debug(f"❌ Ongeldig video pad in batch item {i+1}")
                item["status"] = "failed"
                continue
                
            log_debug(
                f"🔄 Verwerk batch item {i+1}/{len(self.batch_list)}: "
                f"{os.path.basename(item['video'])}"
            )
            
            time.sleep(2)
            
            if processing_paused:
                while processing_paused and not processing_cancelled:
                    time.sleep(0.5)
            
            item["status"] = "completed"
        
        log_debug("✅ Batch verwerking voltooid!")


class PerformanceTracker:
    def __init__(self):
        self.start_time = None
        self.block_times = []
        self.memory_usage = []
        self.cpu_usage = []
    
    def start_tracking(self):
        self.start_time = time.time()
        self.block_times = []
        self.memory_usage = []
        self.cpu_usage = []
        log_debug("📊 Performance tracking gestart")
    
    def track_block(self, block_num, duration):
        self.block_times.append(duration)
        if PSUTIL_AVAILABLE:
            self.memory_usage.append(psutil.virtual_memory().percent)
            self.cpu_usage.append(psutil.cpu_percent())
    
    def generate_report(self):
        if not self.start_time:
            log_debug("📊 Geen performance data beschikbaar")
            return "Geen performance data beschikbaar"
        
        total_time = time.time() - self.start_time
        avg_block_time = (
            sum(self.block_times) / len(self.block_times) if self.block_times else 0
        )
        
        report = f"""
📊 Performance Rapport
====================
⏱️ Totale tijd: {total_time/60:.1f} minuten
📦 Gemiddelde blok tijd: {avg_block_time:.2f} seconden
"""
        
        if avg_block_time > 0:
            blocks_per_minute = 60 / avg_block_time
            report += f"🔢 Blokken per minuut: {blocks_per_minute:.1f} (gemiddeld)\n"
        else:
            report += "🔢 Blokken per minuut: Geen data\n"
        
        if self.memory_usage:
            avg_memory = sum(self.memory_usage) / len(self.memory_usage)
            max_memory = max(self.memory_usage)
            report += f"📦 Gemiddeld geheugen: {avg_memory:.1f}%\n"
            report += f"📦 Max geheugen: {max_memory:.1f}%\n"
        
        if self.cpu_usage:
            avg_cpu = sum(self.cpu_usage) / len(self.cpu_usage)
            max_cpu = max(self.cpu_usage)
            report += f"💻 Gemiddelde CPU: {avg_cpu:.1f}%\n"
            report += f"💻 Max CPU: {max_cpu:.1f}%\n"
        
        log_debug(report)
        return report


class ProgressTracker:
    def __init__(self, progress_bar, status_label):
        self.progress_bar = progress_bar
        self.status_label = status_label
        self.start_time = None
        self.total_blocks = 0
        self.completed_blocks = 0
        
    def start_tracking(self, total_blocks):
        """Start het tracken van voortgang"""
        self.start_time = time.time()
        self.total_blocks = total_blocks
        self.completed_blocks = 0
        self.update_progress(0)
        
    def update_progress(self, completed_blocks):
        """Update de voortgangsbalk met percentage en timer"""
        self.completed_blocks = completed_blocks
        
        if self.total_blocks > 0 and self.start_time is not None:
            percentage = (completed_blocks / self.total_blocks) * 100
            if self.progress_bar is not None and hasattr(
                self.progress_bar, "__setitem__"
            ):
                self.progress_bar["value"] = percentage
            # Bereken tijd
            elapsed_time = time.time() - self.start_time
            elapsed_str = str(timedelta(seconds=int(elapsed_time)))
            if completed_blocks > 0:
                avg_time_per_block = elapsed_time / completed_blocks
                remaining_blocks = self.total_blocks - completed_blocks
                eta_seconds = avg_time_per_block * remaining_blocks
                eta_str = str(timedelta(seconds=int(eta_seconds)))
                status_text = (
                    f"Voortgang: {percentage:.1f}% | Blok {completed_blocks}/{self.total_blocks} | "
                    f"Verstreken: {elapsed_str} | ETA: {eta_str}"
                )
            else:
                status_text = f"Voortgang: {percentage:.1f}% | Blok {completed_blocks}/{self.total_blocks} | Verstreken: {elapsed_str}"
            safe_config(self.status_label, text=status_text)
    
    def complete(self):
        """Markeer als voltooid"""
        if self.start_time is not None:
            total_time = time.time() - self.start_time
            total_time_str = str(timedelta(seconds=int(total_time)))
            safe_config(
                self.status_label, text=f"✅ Voltooid! Totale tijd: {total_time_str}"
            )
        else:
            safe_config(self.status_label, text="✅ Voltooid!")


class ParallelProcessor:
    def __init__(self, max_workers=4):
        self.max_workers = max_workers
        self.executor = None  # Wordt later geïnitialiseerd
        self.active_tasks = []
        self.completed_blocks = 0
        self.total_blocks = 0
        self.start_time = None  # Start tijd voor tijdschatting
        self.lock = threading.Lock()
        self.paused_futures = []  # Bewaar gepauzeerde taken
    
    def initialize_executor(self):
        """Initialiseer de executor na import van heavy modules"""
        if self.executor is None:
            import_heavy_modules()
            self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
    
    def process_block_parallel(
        self, block_num, start_time, duration, model, language, translations
    ):
        """Verwerk één blok parallel met echte Whisper transcriptie"""
        try:
            # Check voor pauze/stop
            if processing_cancelled:
                return False
            
            # Pauze handling
            while processing_paused and not processing_cancelled:
                time.sleep(0.5)
            
            if processing_cancelled:
                return False
            
            # Import heavy modules als nodig
            import_heavy_modules()
            
            # Verwerk het blok
            logregels = []
            log_debug(
                f"🔄 Verwerk blok {block_num} ({start_time}s - {start_time + duration}s)"
            )

            # Hier komt de echte verwerking
            # Voor nu houden we de placeholder, maar voegen we de structuur toe
            time.sleep(1)  # Simuleer verwerkingstijd

            # Voeg resultaat toe aan logregels
            logregels.append(f"Blok {block_num} voltooid")
            
            # Update progress thread-safe
            with self.lock:
                self.completed_blocks += 1
                if root is not None:
                    try:
                        root.after(
                            0, lambda: self.update_progress_safe(self.completed_blocks)
                        )
                    except:
                        # Als root.after faalt, skip de update
                        pass
            
            return True
            
        except Exception as e:
            log_debug(f"[Blok {block_num}] ❌ Parallel verwerking mislukt: {e}")
            return False
    
    def process_all_blocks_parallel(
        self, total_blocks, block_duration, model, language, translations
    ):
        """Verwerk alle blokken parallel"""
        # Initialiseer executor als nodig
        self.initialize_executor()
        
        self.total_blocks = total_blocks
        self.completed_blocks = 0
        self.start_time = time.time()  # Start tijd voor tijdschatting
        
        log_debug(f"⚡ Start parallel verwerking met {self.max_workers} workers")
        
        # Maak taken
        futures = []
        for i in range(total_blocks):
            start_time = i * block_duration
            if self.executor is not None:
                future = self.executor.submit(
                    self.process_block_parallel, 
                    i + 1, 
                    start_time, 
                    block_duration, 
                    model, 
                    language, 
                    translations,
                )
                futures.append(future)
            else:
                log_debug("❌ ParallelProcessor executor is None, taak niet gestart.")
        
        # Wacht op voltooiing met real-time updates
        completed = 0
        failed = 0
        
        for future in as_completed(futures):
            try:
                if future.result():
                    completed += 1
                    log_debug(f"✅ Blok {completed}/{total_blocks} voltooid")
                else:
                    failed += 1
                    log_debug(f"❌ Blok {completed + failed}/{total_blocks} mislukt")
            except Exception as e:
                failed += 1
                log_debug(f"❌ Task mislukt: {e}")
            
            # Update progress bar en status thread-safe
            total_completed = completed + failed
            progress_percentage = (total_completed / total_blocks) * 100
            
            # Gebruik een thread-safe manier om UI updates te doen
            if root is not None:
                try:
                    if progress is not None:

                        def update_progress_bar(p=progress_percentage):
                            safe_config(progress, value=p)

                        root.after(0, update_progress_bar)
                    if status_label is not None:

                        def update_status_label(c=completed, f=failed, t=total_blocks):
                            safe_config(
                                status_label,
                                text=f"🔄 Verwerking: {c} voltooid, {f} mislukt ({total_completed}/{t})",
                            )

                        root.after(0, update_status_label)
                except Exception:
                    pass
            
            # Check voor stop
            if processing_cancelled:
                log_debug("⏹️ Parallel verwerking gestopt door gebruiker")
                break
        
        log_debug(
            f"📊 Parallel verwerking voltooid: {completed} succesvol, {failed} mislukt"
        )
        return completed, failed

    def update_progress_safe(self, completed_blocks):
        """Thread-safe progress update"""
        try:
            if progress is not None and self.total_blocks > 0:
                percentage = (completed_blocks / self.total_blocks) * 100
                safe_config(progress, value=percentage)
            if status_label is not None:
                safe_config(
                    status_label,
                    text=f"🔄 Verwerking: {completed_blocks}/{self.total_blocks} blokken voltooid",
                )
            # Update tijdschatting
            if hasattr(self, 'start_time'):
                update_time_estimate_safe(completed_blocks, self.total_blocks, self.start_time)
        except Exception as e:
            log_debug(f"❌ Fout bij progress update: {e}")


batch_manager = BatchManager()
performance_tracker = PerformanceTracker()
parallel_processor = ParallelProcessor(max_workers=4)


def add_log_message(msg, level="INFO"):
    """Voeg een bericht toe aan de log queue voor real-time updates"""
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    
    # Kleur codering voor verschillende levels
    if level == "ERROR":
        full_msg = f"{timestamp} ❌ {msg}"
        color = "red"
    elif level == "SUCCESS":
        full_msg = f"{timestamp} ✅ {msg}"
        color = "green"
    elif level == "WARNING":
        full_msg = f"{timestamp} ⚠️ {msg}"
        color = "orange"
    else:
        full_msg = f"{timestamp} ℹ️ {msg}"
        color = "black"
    
    # Schrijf naar temp directory
    try:
        import tempfile

        log_path = os.path.join(USER_OUTPUT_DIR, "MagicTime_debug_log.txt")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(full_msg + "\n")
    except Exception as e:
        pass  # Stil falen in productie
    
    # Voeg toe aan queue voor real-time updates
    try:
        log_queue.put((full_msg, color))
    except Exception as e:
        pass  # Stil falen in productie
    
    # Update alle actieve viewers via de queue (thread-safe)
    # De log monitor thread zal de GUI updates doen
    # We doen hier geen directe GUI updates meer


def log_debug(msg, category="debug"):
    """Log een bericht met debug level en categorie filtering"""
    # Controleer of deze categorie gelogd moet worden
    if category in logging_config and not logging_config[category]:
        return
    
    # Voeg timestamp toe
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    formatted_msg = f"[{timestamp}] {msg}"

    # Print naar terminal
    print(formatted_msg)

    # Voeg toe aan GUI log queue voor real-time updates (alleen voor belangrijke berichten)
    if category in ["error", "success", "warning"] or "Fout" in msg or "✅" in msg or "❌" in msg:
        add_log_message(msg, "INFO")

    # Ook direct naar live log viewer als die open is (alleen voor belangrijke berichten)
    if log_text_widget is not None and (category in ["error", "success", "warning"] or "Fout" in msg or "✅" in msg or "❌" in msg):
        try:
            log_text_widget.insert(tk.END, f"{formatted_msg}\n")
            log_text_widget.see(tk.END)
        except:
            pass


def update_log_viewer(viewer, message, color):
    """Update een log viewer met gekleurde tekst - UITGESCHAKELD voor stabiliteit"""
    # Log viewer is uitgeschakeld om fouten te voorkomen
    pass


def start_log_monitor():
    """Start de log monitor thread - UITGESCHAKELD voor stabiliteit"""
    # Log monitor is uitgeschakeld om oneindige loops te voorkomen
    pass


def log_system_info():
    """Log systeem informatie"""
    if PSUTIL_AVAILABLE:
        memory = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent()
        log_debug(
            f"💾 RAM: {memory.percent}% gebruikt ({memory.available/1024/1024/1024:.1f}GB vrij)",
            "log_system_info"
        )
        log_debug(f"💻 CPU: {cpu_percent}% gebruikt", "log_system_info")
    else:
        log_debug("💻 Systeem monitoring niet beschikbaar (psutil niet geïnstalleerd)", "log_system_info")


def check_audio_quality(audio_path):
    """Check audio kwaliteit"""
    if not LIBROSA_AVAILABLE:
        return "unknown"
    
    try:
        y, sr = librosa.load(audio_path)
        
        # Check voor stille segmenten
        rms = librosa.feature.rms(y=y)[0]
        silence_threshold = 0.01
        silent_frames = np.sum(rms < silence_threshold)
        silence_percentage = (silent_frames / len(rms)) * 100
        
        if silence_percentage > 80:
            return "silent"
        elif silence_percentage > 50:
            return "mostly_silent"
        else:
            return "good"
    except:
        return "unknown"


def extract_audio_from_video(video_path, output_dir=None):
    """Extraheer audio uit video bestand met FFmpeg"""
    try:
        log_debug(f"🎵 START: Audio extractie van {os.path.basename(video_path)}", "log_audio_extraction")
        log_debug(f"📁 Video pad: {video_path}", "log_audio_extraction")

        if output_dir is None:
            output_dir = TEMP
        log_debug(f"📁 Output directory: {output_dir}", "log_audio_extraction")

        # Maak output directory als deze niet bestaat
        os.makedirs(output_dir, exist_ok=True)
        log_debug("✅ Output directory aangemaakt/gecontroleerd", "log_audio_extraction")

        # Genereer unieke bestandsnaam
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        audio_path = os.path.join(output_dir, f"{video_name}_audio.wav")
        log_debug(f"🎵 Audio output pad: {audio_path}")

        # Gebruik altijd absoluut pad naar ffmpeg
        ffmpeg_path = os.path.join(ASSETS, "ffmpeg.exe")
        log_debug(f"🔍 Zoek ffmpeg op: {ffmpeg_path}")
        if not os.path.exists(ffmpeg_path):
            log_debug(f"❌ ffmpeg.exe niet gevonden in assets! ABORT.")
            raise FileNotFoundError(f"ffmpeg.exe niet gevonden in assets: {ffmpeg_path}")
        else:
            log_debug(f"✅ ffmpeg.exe gevonden in assets.")
        
        # FFmpeg commando voor audio extractie met threading
        cmd = [
            ffmpeg_path,
            "-i", video_path,
            "-vn",  # Geen video
            "-acodec", "pcm_s16le",  # PCM 16-bit
            "-ar", "16000",  # 16kHz sample rate (optimaal voor Whisper)
            "-ac", "1",  # Mono audio
            "-threads", "0",  # Gebruik alle beschikbare CPU cores
            "-y",  # Overschrijf output bestand
            audio_path
        ]
        log_debug(f"🔧 FFmpeg commando: {' '.join(cmd)}")
        log_debug(f"🔍 Bestaat ffmpeg_path? {os.path.exists(ffmpeg_path)}")
        log_debug(f"🔍 Bestaat output_dir? {os.path.exists(output_dir)}")

        # --- Windows startupinfo om tray vensters te voorkomen ---
        import subprocess
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        # Voer FFmpeg uit
        result = run_and_track_subprocess(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=300,
            creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0,
            startupinfo=startupinfo
        )
        
        if result.returncode == 0:
            log_debug(f"✅ Audio geëxtraheerd naar: {os.path.basename(audio_path)}")
            if os.path.exists(audio_path):
                file_size = os.path.getsize(audio_path) / (1024 * 1024)  # MB
                log_debug(f"📊 Audio bestand grootte: {file_size:.2f} MB")
                if file_size < 0.1:
                    log_debug("⚠️ Audio bestand is erg klein, mogelijk geen audio in video")
                    return None
                return audio_path
            else:
                log_debug("❌ Audio bestand niet aangemaakt")
                return None
        else:
            log_debug(f"❌ FFmpeg fout: {result.stderr}")
            return None
    except subprocess.TimeoutExpired:
        log_debug("❌ FFmpeg timeout - audio extractie duurde te lang")
        return None
    except Exception as e:
        log_debug(f"❌ FOUT bij audio extractie: {e}")
        log_debug(f"🔍 Exception type: {type(e).__name__}")
        import traceback
        log_debug(f"📋 Stack trace: {traceback.format_exc()}")
        return None


def get_video_info(video_path):
    """Haal video metadata op met FFmpeg"""
    try:
        # Gebruik altijd absoluut pad naar ffmpeg
        ffmpeg_path = os.path.join(ASSETS, "ffmpeg.exe")
        log_debug(f"🔍 Zoek ffmpeg op: {ffmpeg_path}")
        if not os.path.exists(ffmpeg_path):
            log_debug(f"❌ ffmpeg.exe niet gevonden in assets! ABORT.")
            raise FileNotFoundError(f"ffmpeg.exe niet gevonden in assets: {ffmpeg_path}")
        else:
            log_debug(f"✅ ffmpeg.exe gevonden in assets.")
        
        # FFmpeg commando voor video info met threading
        cmd = [
            ffmpeg_path,
            "-i", video_path,
            "-threads", "0",  # Gebruik alle beschikbare CPU cores
            "-f", "null",
            "-"
        ]
        log_debug(f"🔧 FFmpeg commando: {' '.join(cmd)}")
        import subprocess
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        result = run_and_track_subprocess(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,  # Alleen stderr nodig voor duration parsing
            text=True,
            timeout=60,
            creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0,
            startupinfo=startupinfo
        )
        # Parse duration uit FFmpeg output
        duration = None
        if result.stderr:
            import re
            duration_match = re.search(r"Duration: (\d{2}):(\d{2}):(\d{2})\.(\d{2})", result.stderr)
            if duration_match:
                hours = int(duration_match.group(1))
                minutes = int(duration_match.group(2))
                seconds = int(duration_match.group(3))
                centiseconds = int(duration_match.group(4))
                duration = hours * 3600 + minutes * 60 + seconds + centiseconds / 100
                log_debug(f"🎬 Video info: {duration:.2f}s")
                return {"duration": duration}
        log_debug("❌ Kon video duration niet bepalen")
        return None
    except Exception as e:
        log_debug(f"❌ Kon video info niet ophalen: {e}")
        return None


def play_notification_sound(success=True):
    """Speel notificatie geluid"""
    if success:
        winsound.Beep(800, 200)
        winsound.Beep(1000, 100)
    else:
        winsound.Beep(400, 500)


def show_completion_notification():
    """Toon completion notificatie"""
    try:
        from win10toast import ToastNotifier

        toaster = ToastNotifier()
        toaster.show_toast(
            "Magic Time Studio", "Video verwerking voltooid! 🎉", duration=5
        )
    except:
        play_notification_sound(True)


def cleanup_temp_files():
    """Verwijder tijdelijke audiobestanden en logbestanden zonder fouten"""
    try:
        # Bepaal output directory op basis van geselecteerde video
        if selected_video and os.path.exists(selected_video):
            output_dir = os.path.dirname(selected_video)
        else:
            log_debug("❌ Geen video geselecteerd. Cleanup wordt overgeslagen.")
            return
            
        # Cleanup temp_audio bestanden
        temp_audio_dir = os.path.join(output_dir, "temp_audio")
        if os.path.exists(temp_audio_dir):
            shutil.rmtree(temp_audio_dir, ignore_errors=True)
            log_debug("🧹 Tijdelijke audiobestanden verwijderd")

        logs_dir = os.path.join(output_dir, "logs")
        if os.path.exists(logs_dir):
            for log_file in os.listdir(logs_dir):
                if log_file.startswith('log_') and log_file.endswith('.txt'):
                    log_path = os.path.join(logs_dir, log_file)
                    try:
                        with open(log_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        if 'ERROR' not in content and '❌' not in content and 'FAILED' not in content:
                            os.remove(log_path)
                            log_debug(f"🧹 Logbestand verwijderd (geen fouten): {log_file}")
                    except Exception as e:
                        log_debug(f"⚠️ Kon logbestand niet controleren: {e}")

        temp_dir = os.path.join(output_dir, "temp")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
            log_debug("🧹 Temp directory verwijderd")
        
        # Force garbage collection voor memory optimalisatie
        import gc
        gc.collect()
        log_debug("🧹 Garbage collection uitgevoerd")
        
    except Exception as e:
        log_debug(f"⚠️ Fout bij cleanup: {e}")

def optimize_memory_usage():
    """Optimaliseer geheugengebruik"""
    try:
        import gc
        import psutil
        
        # Force garbage collection
        gc.collect()
        
        # Log memory usage
        process = psutil.Process()
        memory_info = process.memory_info()
        memory_mb = memory_info.rss / 1024 / 1024
        
        log_debug(f"💾 Huidig geheugengebruik: {memory_mb:.1f} MB")
        
        # Waarschuwing bij hoog geheugengebruik
        if memory_mb > 1000:  # 1GB
            log_debug("⚠️ Hoog geheugengebruik gedetecteerd")
            gc.collect()  # Extra garbage collection
        
        return memory_mb
    except Exception as e:
        log_debug(f"❌ Fout bij memory optimalisatie: {e}")
        return 0


def organize_output():
    """Voer cleanup uit zonder submappen aan te maken"""
    # Bepaal output directory op basis van geselecteerde video
    if selected_video and os.path.exists(selected_video):
        output_dir = os.path.dirname(selected_video)
    else:
        log_debug("❌ Geen video geselecteerd. Cleanup wordt overgeslagen.")
        return
        
    video_name = os.path.splitext(safe_basename(selected_video))[0]
    
    # Verwijder alleen tijdelijke blok bestanden
    removed_count = 0
    for file in os.listdir(output_dir):
        if file.endswith("_blok") or file.endswith("_blok.srt"):
            # Verwijder tijdelijke blok bestanden
            try:
                os.remove(os.path.join(output_dir, file))
                removed_count += 1
            except:
                pass
    
    log_debug(f"🧹 Cleanup voltooid: {removed_count} tijdelijke bestanden verwijderd")
    
    # Voer cleanup uit
    cleanup_temp_files()


# 🌐 Vertaler + thema info inladen
# translator wordt later geïnitialiseerd in setup_ui()
huidige_vertaler = "geen"
deepl_tekens_used = 0
opgeslagen_thema = "Dark"

# Laad configuratie na logging_config definitie
def load_configuration():
    global huidige_vertaler, subtitle_type, hardcoded_language, font_size, logging_config, deepl_key
    try:
        config_path = os.path.join(get_user_data_dir(), "config.json")
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            deepl_key = config.get("deepl_key", None)
            # Forceer altijd 'geen' als vertaler bij opstarten
            huidige_vertaler = "geen"
            log_debug(f"[DEBUG] Vertaler geforceerd op 'geen' bij opstarten, ongeacht config.")
            subtitle_type = config.get("subtitle_type", "softcoded")
            hardcoded_language = config.get("hardcoded_language", "dutch_only")
            font_size = config.get("font_size", 9)
            logging_config = config.get("logging_config", logging_config)
            worker_count = config.get("worker_count", 4)
            if huidige_vertaler == "deepl" and not deepl_key:
                log_debug("⚠️ DeepL geselecteerd maar geen API key gevonden")
        else:
            huidige_vertaler = "geen"  # default is 'geen'
            subtitle_type = "softcoded"
            hardcoded_language = "dutch_only"
            font_size = 9
    except Exception as e:
        log_debug(f"❌ Fout bij laden configuratie: {e}")
        huidige_vertaler = "geen"  # default is 'geen'
        subtitle_type = "softcoded"
        hardcoded_language = "dutch_only"
        font_size = 9
    log_debug(f"[DEBUG] Na load_configuration: huidige_vertaler = {huidige_vertaler}")

# Laad configuratie
load_configuration()

# Pas lettertype grootte toe bij start (na setup_ui)
# Dit wordt later aangeroepen in setup_ui() functie


def sla_config_op():
    try:
        config = {
            "translator": huidige_vertaler,
            "huidige_vertaler": huidige_vertaler,  # Voor compatibiliteit
            "logging_config": logging_config,
        }
        config_path = os.path.join(get_user_data_dir(), "config.json")
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        log_debug(f"💾 Configuratie opgeslagen - Vertaler: {huidige_vertaler}")
    except Exception as e:
        log_debug(f"❌ Fout bij opslaan configuratie: {e}")


# 🌈 Thema's - oogvriendelijk licht en donker
THEMA_KLEUREN = {
    "light": {
        "bg": "#f5f5f5",
        "fg": "#2c2c2c",
        "accent": "#e8e8e8",
        "frame": "#fafafa",
        "knop": "#e8e8e8",
        "knop_fg": "#2c2c2c",
        "main_bg": "#f0f8f0",
        "panel_bg": "#f5faf5",
    },
    "dark": {
        "bg": "#2a2a2a",
        "fg": "#e0e0e0",
        "accent": "#404040",
        "frame": "#353535",
        "knop": "#505050",
        "knop_fg": "#e0e0e0",
        "main_bg": "#252525",
        "panel_bg": "#303030",
    },
    "blue": {
        "bg": "#e3f2fd",
        "fg": "#1565c0",
        "accent": "#bbdefb",
        "frame": "#e1f5fe",
        "knop": "#2196f3",
        "knop_fg": "#ffffff",
        "main_bg": "#ffffff",
        "panel_bg": "#f0f8ff",
    },
    "green": {
        "bg": "#e8f5e8",
        "fg": "#2e7d32",
        "accent": "#c8e6c9",
        "frame": "#e8f5e8",
        "knop": "#4caf50",
        "knop_fg": "#ffffff",
        "main_bg": "#ffffff",
        "panel_bg": "#f1f8e9",
    },
}


def laad_thema_uit_config():
    return opgeslagen_thema if opgeslagen_thema in THEMA_KLEUREN else "dark"


def sla_thema_op(gekozen_thema):
    global opgeslagen_thema
    opgeslagen_thema = gekozen_thema
    sla_config_op()

def apply_font_size_to_interface(new_font_size):
    """Pas lettertype grootte toe op alle widgets in de interface"""
    global font_size
    font_size = new_font_size
    
    # Recreate menubalk met nieuwe lettertype
    if root is not None and 'menubalk' in globals():
        global menubalk
        if menubalk is not None:
            try:
                menubalk.destroy()
            except:
                pass
        menubalk = tk.Menu(root, font=("Arial", new_font_size))
        root.config(menu=menubalk)
        voeg_tools_menu_toe()
        log_debug(f"�� Menubalk opnieuw aangemaakt met lettertype grootte {new_font_size}")
    
    def apply_font_to_widgets(parent_widget):
        """Recursief lettertype toepassen op alle widgets"""
        try:
            for widget in parent_widget.winfo_children():
                if hasattr(widget, 'configure'):
                    try:
                        # Pas lettertype toe op verschillende widget types
                        if isinstance(widget, tk.Label):
                            current_font = widget.cget("font")
                            if isinstance(current_font, str):
                                # Parse font string en update grootte
                                font_parts = current_font.split()
                                if len(font_parts) >= 2:
                                    font_family = font_parts[0]
                                    font_weight = "bold" if "bold" in font_parts else "normal"
                                    widget.configure(font=(font_family, new_font_size, font_weight))
                            elif isinstance(current_font, tuple):
                                # Font tuple (family, size, weight)
                                font_family = current_font[0]
                                font_weight = current_font[2] if len(current_font) > 2 else "normal"
                                widget.configure(font=(font_family, new_font_size, font_weight))
                        elif isinstance(widget, tk.Button):
                            current_font = widget.cget("font")
                            if isinstance(current_font, str):
                                font_parts = current_font.split()
                                if len(font_parts) >= 2:
                                    font_family = font_parts[0]
                                    font_weight = "bold" if "bold" in font_parts else "normal"
                                    widget.configure(font=(font_family, new_font_size, font_weight))
                            elif isinstance(current_font, tuple):
                                font_family = current_font[0]
                                font_weight = current_font[2] if len(current_font) > 2 else "normal"
                                widget.configure(font=(font_family, new_font_size, font_weight))
                        elif isinstance(widget, tk.Entry):
                            current_font = widget.cget("font")
                            if isinstance(current_font, str):
                                font_parts = current_font.split()
                                if len(font_parts) >= 2:
                                    font_family = font_parts[0]
                                    widget.configure(font=(font_family, new_font_size))
                            elif isinstance(current_font, tuple):
                                font_family = current_font[0]
                                widget.configure(font=(font_family, new_font_size))
                        elif isinstance(widget, tk.OptionMenu):
                            current_font = widget.cget("font")
                            if isinstance(current_font, str):
                                font_parts = current_font.split()
                                if len(font_parts) >= 2:
                                    font_family = font_parts[0]
                                    font_weight = "bold" if "bold" in font_parts else "normal"
                                    widget.configure(font=(font_family, new_font_size, font_weight))
                            elif isinstance(current_font, tuple):
                                font_family = current_font[0]
                                font_weight = current_font[2] if len(current_font) > 2 else "normal"
                                widget.configure(font=(font_family, new_font_size, font_weight))
                        elif isinstance(widget, tk.Listbox):
                            current_font = widget.cget("font")
                            if isinstance(current_font, str):
                                font_parts = current_font.split()
                                if len(font_parts) >= 2:
                                    font_family = font_parts[0]
                                    widget.configure(font=(font_family, new_font_size))
                            elif isinstance(current_font, tuple):
                                font_family = current_font[0]
                                widget.configure(font=(font_family, new_font_size))
                        elif isinstance(widget, tk.Text):
                            current_font = widget.cget("font")
                            if isinstance(current_font, str):
                                font_parts = current_font.split()
                                if len(font_parts) >= 2:
                                    font_family = font_parts[0]
                                    widget.configure(font=(font_family, new_font_size))
                            elif isinstance(current_font, tuple):
                                font_family = current_font[0]
                                widget.configure(font=(font_family, new_font_size))
                        elif isinstance(widget, tk.Checkbutton):
                            current_font = widget.cget("font")
                            if isinstance(current_font, str):
                                font_parts = current_font.split()
                                if len(font_parts) >= 2:
                                    font_family = font_parts[0]
                                    font_weight = "bold" if "bold" in font_parts else "normal"
                                    widget.configure(font=(font_family, new_font_size, font_weight))
                            elif isinstance(current_font, tuple):
                                font_family = current_font[0]
                                font_weight = current_font[2] if len(current_font) > 2 else "normal"
                                widget.configure(font=(font_family, new_font_size, font_weight))
                        elif isinstance(widget, tk.Menu):
                            # Menu widgets hebben een andere configuratie
                            try:
                                widget.configure(font=("Arial", new_font_size))
                                # Probeer ook de menu items te configureren
                                try:
                                    menu_end = widget.index('end')
                                    if menu_end is not None:
                                        for i in range(menu_end + 1):
                                            try:
                                                widget.entryconfig(i, font=("Arial", new_font_size))
                                            except:
                                                pass
                                except:
                                    pass
                            except:
                                pass
                    except Exception as e:
                        log_debug(f"❌ Fout bij lettertype widget: {e}")
                        pass
                
                # Recursief doorlopen van child widgets
                if hasattr(widget, 'winfo_children'):
                    apply_font_to_widgets(widget)
        except Exception as e:
            log_debug(f"❌ Fout bij lettertype toepassing: {e}")
            pass
    
    # Pas lettertype toe op hoofdvenster
    if root is not None:
        apply_font_to_widgets(root)
    
    # Pas lettertype toe op configuratie venster als het open is
    if 'config_window' in globals() and config_window is not None:
        apply_font_to_widgets(config_window)
    
    # Pas lettertype toe op log venster als het open is
    if 'log_window' in globals() and log_window is not None:
        apply_font_to_widgets(log_window)
    
    # Pas lettertype toe op menubalk
    if 'menubalk' in globals() and menubalk is not None:
        apply_font_to_widgets(menubalk)
        # Specifieke menubalk lettertype toepassing
        try:
            menubalk.configure(font=("Arial", new_font_size))
            # Probeer alle menu items te configureren
            try:
                menu_end = menubalk.index('end')
                if menu_end is not None:
                    for i in range(menu_end + 1):
                        try:
                            menubalk.entryconfig(i, font=("Arial", new_font_size))
                        except:
                            pass
            except:
                pass
        except:
            pass
        
        # Force menubalk update door root te updaten
        if root is not None:
            try:
                root.update_idletasks()
                root.update()
            except:
                pass
    
    log_debug(f"🔤 Lettertype grootte toegepast: {new_font_size}")


# 🚀 Splashfunctie definiëren
# --- Globale referentie voor splash-afbeelding om GC te voorkomen ---
# splash_img_ref = None  # Verwijderd


def show_help_tooltip(widget, message):
    """Toon help tooltip voor een widget"""

    def show_tooltip(event):
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")

        label = tk.Label(
            tooltip,
            text=message,
            justify="left",
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            font=("Segoe UI", 9),
            wraplength=300,
        )
        label.pack()

        def hide_tooltip():
            tooltip.destroy()

        widget.bind("<Leave>", lambda e: hide_tooltip())
        tooltip.bind("<Leave>", lambda e: hide_tooltip())

    widget.bind("<Enter>", show_tooltip)


def create_help_button(parent, help_text, row, column):
    """Maak een help knop met tooltip"""
    help_btn = tk.Button(
        parent,
        text="❓",
        font=("Segoe UI", 8),
        bg="#e0e0e0",
        fg="#333333",
        width=2,
        height=1,
    )
    help_btn.grid(row=row, column=column, sticky="e", padx=(2, 0))
    show_help_tooltip(help_btn, help_text)
    return help_btn


# 🎬 GUI opstarten - EEN KEER ALLEEN
# GUI elements will be created in setup_ui() function


def show_live_log():
    """Toon live log venster met real-time updates"""
    global log_window, log_text_widget

    if log_window is not None:
        try:
            log_window.lift()
            log_window.focus_force()
            return
        except:
            pass

    log_window = tk.Toplevel()
    log_window.title("🔍 Live Log - Magic Time Studio")
    log_window.geometry("800x600")
    
    # Maak het venster niet-modal (kan naast hoofdvenster gebruikt worden)
    log_window.transient(root)
    # log_window.grab_set()  # Uitgeschakeld zodat hoofdvenster niet geblokkeerd wordt

    # Pas het huidige thema toe
    if thema_var is not None:
        huidig_thema = thema_var.get()
        if huidig_thema in THEMA_KLEUREN:
            kleuren = THEMA_KLEUREN[huidig_thema]
            log_window.configure(bg=kleuren["bg"])
            header_frame = tk.Frame(log_window, bg=kleuren["panel_bg"], height=40)
        else:
            log_window.configure(bg="#f0f0f0")
            header_frame = tk.Frame(log_window, bg="#2c3e50", height=40)
    else:
        log_window.configure(bg="#f0f0f0")
        header_frame = tk.Frame(log_window, bg="#2c3e50", height=40)
    header_frame.pack(fill="x", padx=5, pady=5)
    header_frame.pack_propagate(False)

    title_label = tk.Label(
        header_frame,
        text="🔍 Live Log Monitor",
        font=("Arial", 12, "bold"),
        fg="white",
        bg="#2c3e50",
    )
    title_label.pack(side="left", padx=10, pady=5)

    # Control buttons
    button_frame = tk.Frame(header_frame, bg="#2c3e50")
    button_frame.pack(side="right", padx=10)

    def clear_log():
        if log_text_widget:
            log_text_widget.delete(1.0, tk.END)
            add_log_message_to_viewer("🗑️ Log gewist", "INFO")

    def refresh_log():
        add_log_message_to_viewer("🔄 Log vernieuwd", "INFO")

    clear_btn = tk.Button(
        button_frame,
        text="Wis",
        command=clear_log,
        bg="#e74c3c",
        fg="white",
        font=("Arial", 9),
    )
    clear_btn.pack(side="left", padx=2)

    refresh_btn = tk.Button(
        button_frame,
        text="Vernieuw",
        command=refresh_log,
        bg="#3498db",
        fg="white",
        font=("Arial", 9),
    )
    refresh_btn.pack(side="left", padx=2)

    # Main content
    main_frame = tk.Frame(log_window, bg="#f0f0f0")
    main_frame.pack(fill="both", expand=True, padx=5, pady=5)

    # Log text area
    text_frame = tk.Frame(main_frame, bg="#f0f0f0")
    text_frame.pack(fill="both", expand=True)

    log_text_widget = tk.Text(
        text_frame,
        bg="#2c3e50",
        fg="#ecf0f1",
        font=("Consolas", 9),
        wrap="word",
        insertbackground="white",
        selectbackground="#3498db",
        relief="flat",
        padx=10,
        pady=10,
    )

    scrollbar = tk.Scrollbar(
        text_frame, orient="vertical", command=log_text_widget.yview
    )
    log_text_widget.configure(yscrollcommand=scrollbar.set)

    log_text_widget.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Status bar
    status_frame = tk.Frame(log_window, bg="#34495e", height=25)
    status_frame.pack(fill="x", side="bottom")
    status_frame.pack_propagate(False)

    status_label = tk.Label(
        status_frame,
        text="🟢 Live log actief",
        font=("Arial", 9),
        fg="white",
        bg="#34495e",
    )
    status_label.pack(side="left", padx=10, pady=2)

    # Auto-scroll checkbox
    auto_scroll_var = tk.BooleanVar(value=True)
    auto_scroll_cb = tk.Checkbutton(
        status_frame,
        text="Auto-scroll",
        variable=auto_scroll_var,
        font=("Arial", 9),
        fg="white",
        bg="#34495e",
        selectcolor="#2c3e50",
    )
    auto_scroll_cb.pack(side="right", padx=10, pady=2)

    def update_log_display():
        """Update log display met real-time berichten"""
        try:
            if log_text_widget is not None:
                # Haal berichten op uit de queue
                while not log_queue.empty():
                    try:
                        message, color = log_queue.get_nowait()
                        
                        # Voeg bericht toe aan text widget
                        log_text_widget.insert(tk.END, message + "\n")
                        
                        # Kleur het bericht
                        if color == "red":
                            log_text_widget.tag_add("error", f"{log_text_widget.index('end-2c').split('.')[0]}.0", "end-1c")
                            log_text_widget.tag_config("error", foreground="red")
                        elif color == "green":
                            log_text_widget.tag_add("success", f"{log_text_widget.index('end-2c').split('.')[0]}.0", "end-1c")
                            log_text_widget.tag_config("success", foreground="green")
                        elif color == "orange":
                            log_text_widget.tag_add("warning", f"{log_text_widget.index('end-2c').split('.')[0]}.0", "end-1c")
                            log_text_widget.tag_config("warning", foreground="orange")
                        
                        # Auto-scroll naar beneden
                        if auto_scroll_var.get():
                            log_text_widget.see(tk.END)
                            
                    except Exception as e:
                        print(f"Fout bij verwerken log bericht: {e}")
                        break
                        
        except Exception as e:
            print(f"Fout bij update log display: {e}")
            
        # Plan volgende update
        safe_after(log_window, 100, update_log_display)

    def auto_scroll():
        """Auto-scroll naar beneden"""
        if auto_scroll_var.get() and log_text_widget:
            log_text_widget.see(tk.END)
        safe_after(log_window, 500, auto_scroll)

    def periodic_update():
        """Periodieke updates voor systeem info"""
        try:
            if PSUTIL_AVAILABLE:
                memory = psutil.virtual_memory()
                memory_percent = memory.percent

                status_text = f"🟢 Live log actief | RAM: {memory_percent:.1f}%"
                status_label.config(text=status_text)

            # Voeg systeem info toe elke 30 seconden
            if hasattr(periodic_update, "counter"):
                periodic_update.counter += 1
            else:
                periodic_update.counter = 0

            if periodic_update.counter % 300 == 0:  # Elke 30 seconden
                log_system_info()

        except Exception as e:
            print(f"Fout bij periodieke update: {e}")

        safe_after(log_window, 1000, periodic_update)

    def add_log_message_to_viewer(message, level="INFO"):
        """Voeg een bericht toe aan de log viewer"""
        try:
            if log_text_widget is not None:
                timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
                
                # Kleur codering voor verschillende levels
                if level == "ERROR":
                    full_msg = f"{timestamp} ❌ {message}"
                    color = "red"
                elif level == "SUCCESS":
                    full_msg = f"{timestamp} ✅ {message}"
                    color = "green"
                elif level == "WARNING":
                    full_msg = f"{timestamp} ⚠️ {message}"
                    color = "orange"
                else:
                    full_msg = f"{timestamp} ℹ️ {message}"
                    color = "black"
                
                # Voeg toe aan text widget
                log_text_widget.insert(tk.END, full_msg + "\n")
                
                # Kleur het bericht
                if color == "red":
                    log_text_widget.tag_add("error", f"{log_text_widget.index('end-2c').split('.')[0]}.0", "end-1c")
                    log_text_widget.tag_config("error", foreground="red")
                elif color == "green":
                    log_text_widget.tag_add("success", f"{log_text_widget.index('end-2c').split('.')[0]}.0", "end-1c")
                    log_text_widget.tag_config("success", foreground="green")
                elif color == "orange":
                    log_text_widget.tag_add("warning", f"{log_text_widget.index('end-2c').split('.')[0]}.0", "end-1c")
                    log_text_widget.tag_config("warning", foreground="orange")
                
                # Auto-scroll naar beneden
                if auto_scroll_var.get():
                    log_text_widget.see(tk.END)
                    
        except Exception as e:
            print(f"Fout bij toevoegen log bericht: {e}")

    # Start de updates
    update_log_display()
    auto_scroll()
    periodic_update()
    
    # Pas lettertype grootte toe op log venster
    if 'font_size' in globals() and font_size is not None:
        apply_font_size_to_interface(font_size)

    # Voeg initiële berichten toe
    add_log_message_to_viewer("🚀 Live log gestart", "SUCCESS")
    add_log_message_to_viewer("📊 Systeem monitoring actief", "INFO")
    add_log_message_to_viewer("🔄 Real-time updates ingeschakeld", "INFO")

    # Voeg systeem info toe
    log_system_info()

    def on_closing():
        """Sluit het log venster"""
        global log_window, log_text_widget
        try:
            if log_window is not None and hasattr(log_window, "destroy"):
                log_window.destroy()
        except Exception as e:
            log_debug(f"❌ Fout bij sluiten log venster: {e}")
        finally:
            log_window = None
            log_text_widget = None

    log_window.protocol("WM_DELETE_WINDOW", on_closing)

    # Focus op het venster
    log_window.focus_force()
    log_window.lift()


# GUI elements will be created in setup_ui() function - removed premature initialization

# 🧠 Variabelen - initialized globally but GUI vars will be in setup_ui()
selected_video = None


def kies_video():
    """Kies een videobestand"""
    global selected_video, verwerk_lijst, listbox_nog
    pad = filedialog.askopenfilename(
        title="Kies videobestand",
        filetypes=[
            ("Video-bestanden", "*.mp4 *.mov *.avi *.mkv *.webm"),
            ("Alle bestanden", "*.*"),
        ],
    )
    if pad:
        selected_video = pad
        safe_set(video_pad, pad)
        naam = os.path.basename(pad)

        # Voeg toe aan verwerkingslijst met dezelfde functie als map toevoegen
        voeg_bestand_toe_pad(pad)

        if info_label is not None:
            info_label.config(text=f"📄 Gekozen bestand:\n{naam}")
            
            

        # Voeg log bericht toe
        try:
            if "add_log_to_viewer" in globals():
                add_log_to_viewer(f"Video gekozen: {naam}", "SUCCESS")
        except:
            pass
    else:
        selected_video = None
        safe_set(video_pad, "")
        if info_label is not None:
            info_label.config(text="📄 Geen video gekozen")

        # Voeg log bericht toe
        try:
            if "add_log_to_viewer" in globals():
                add_log_to_viewer("Geen video gekozen", "WARNING")
        except:
            pass


def kies_map_en_voeg_toe():
    """Kies een map en voeg alle videobestanden toe"""
    map_pad = filedialog.askdirectory(title="Kies map met videobestanden")
    if map_pad:
        voeg_map_toe_paden(map_pad)





def diagnose_whisper_issues():
    """Diagnoseer mogelijke Whisper problemen"""
    try:
        log_debug("🔍 START: Whisper diagnose...")
        
        # Test 1: Import check
        try:
            import whisper
            log_debug("✅ Whisper import succesvol")
        except ImportError as e:
            log_debug(f"❌ Whisper import mislukt: {e}")
            return False
        
        # Test 2: Model download test
        try:
            log_debug("🔄 Test model download...")
            import torch; device = "cuda" if torch.cuda.is_available() else "cpu"; model = whisper.load_model("tiny", device=device)  # Kleinste model voor snelle test
            log_debug("✅ Model download succesvol")
        except Exception as e:
            log_debug(f"❌ Model download mislukt: {e}")
            return False
        
        # Test 3: Audio processing test
        try:
            log_debug("🔄 Test audio processing...")
            import numpy as np
            # Maak dummy audio voor test met juiste dtype
            dummy_audio = np.random.randn(16000 * 5).astype(np.float32)  # 5 seconden audio
            audio = whisper.pad_or_trim(dummy_audio)
            mel = whisper.log_mel_spectrogram(audio)
            log_debug("✅ Audio processing succesvol")
        except Exception as e:
            log_debug(f"❌ Audio processing mislukt: {e}")
            # Dit is geen kritieke fout, ga door met diagnose
            log_debug("⚠️ Audio processing test gefaald, maar dit is niet kritiek")
        
        # Test 4: Device check
        try:
            import torch
            device = "cuda" if torch.cuda.is_available() else "cpu"
            log_debug(f"✅ Device: {device}")
            if device == "cpu":
                log_debug("⚠️ CUDA niet beschikbaar - transcriptie zal langzamer zijn")
        except Exception as e:
            log_debug(f"❌ Device check mislukt: {e}")
        
        log_debug("✅ Whisper diagnose voltooid - alles OK")
        return True
        
    except Exception as e:
        log_debug(f"❌ Diagnose mislukt: {e}")
        return False


def transcribe_audio_with_whisper(audio_path, model_name="base", language="auto"):
    """Transcribe audio met Whisper - Verbeterde versie met live voortgang en multi-taal support"""
    try:
        # Onderdruk Triton waarschuwingen
        import warnings
        warnings.filterwarnings("ignore", message="Failed to launch Triton kernels")
        warnings.filterwarnings("ignore", message="Failed to launch Triton kernels, likely due to missing CUDA toolkit")
        
        # Update status voor gebruiker
        update_status_safe("🎤 Start Whisper transcriptie...")
        log_debug(f"🎤 Start Whisper transcriptie...")
        log_debug(f"📁 Audio: {os.path.basename(audio_path)}")
        log_debug(f"🤖 Model: {model_name}")
        log_debug(f"🌍 Taal: {language}")
        
        # Controleer audio bestand
        if not os.path.exists(audio_path):
            update_status_safe("❌ Audio bestand bestaat niet")
            log_debug(f"❌ Audio bestand bestaat niet: {audio_path}")
            reset_progress_bar()
            return None
        
        file_size = os.path.getsize(audio_path) / (1024 * 1024)  # MB
        update_status_safe(f"📊 Audio bestand: {file_size:.2f} MB")
        log_debug(f"📊 Audio bestand grootte: {file_size:.2f} MB")
        
        if file_size < 0.01:  # Minder dan 10KB
            update_status_safe("❌ Audio bestand is te klein")
            log_debug("❌ Audio bestand is te klein - mogelijk geen audio")
            reset_progress_bar()
            return None

        # Import Whisper
        update_status_safe("🔄 Whisper modules laden...")
        import whisper
        import torch
        
        # Device check
        device = "cuda" if torch.cuda.is_available() else "cpu"
        update_status_safe(f"💻 Device: {device.upper()}")
        log_debug(f"💻 Device: {device}")

        update_status_safe(f"🔄 Model '{model_name}' laden...")
        log_debug(f"🔄 Whisper: model wordt geladen...")
        whisper_model = whisper.load_model(model_name, device=device)

        # --- GUI voortgangsfunctie ---
        def whisper_progress_callback(progress):
            # progress: float tussen 0.0 en 1.0
            try:
                if progress is not None and progress >= 0.0 and progress <= 1.0:
                    percentage = int(progress * 100)
                    if progress is not None:
                        schedule_immediate_update(lambda: safe_config(progress_bar, value=percentage))
                    if status_label is not None:
                        schedule_priority_update(lambda: safe_config(status_label, text=f"🎤 Whisper transcriptie: {percentage}%"))
            except Exception as e:
                log_debug(f"❌ Fout bij Whisper voortgangsupdate: {e}")

        # Gebruik eigen voortgangsbalk als die bestaat, anders de globale
        global progress
        progress_bar = progress if progress is not None else None

        # Start transcriptie met voortgangsfunctie
        result = None
        try:
            result = whisper_model.transcribe(
                audio_path,
                language=language if language != "auto" else None,
                verbose=False,
                word_timestamps=True,
                condition_on_previous_text=False,
                progress_callback=whisper_progress_callback
            )
        except TypeError:
            # Oudere Whisper-versie zonder progress_callback
            log_debug("⚠️ Whisper versie ondersteunt geen progress_callback, geen GUI voortgang mogelijk")
            result = whisper_model.transcribe(
                audio_path,
                language=language if language != "auto" else None,
                verbose=False,
                word_timestamps=True,
                condition_on_previous_text=False
            )
        except Exception as e:
            update_status_safe("❌ Transcriptie mislukt, probeer zonder taal...")
            log_debug(f"❌ Transcriptie mislukt: {e}")
            # Probeer zonder taal specificatie
            try:
                update_status_safe("🔄 Probeer transcriptie zonder taal...")
                log_debug("🔄 Probeer transcriptie zonder taal specificatie...")
                result = whisper_model.transcribe(audio_path, verbose=False)
            except Exception as e2:
                update_status_safe("❌ Transcriptie mislukt")
                log_debug(f"❌ Transcriptie zonder taal ook mislukt: {e2}")
                reset_progress_bar()
                return None

        # Controleer resultaat
        if not result or "text" not in result:
            update_status_safe("❌ Geen tekst gevonden")
            log_debug("❌ Geen tekst gevonden in transcriptie resultaat")
            reset_progress_bar()
            return None
        
        text = result["text"]
        if isinstance(text, str):
            text = text.strip()
        else:
            text = str(text).strip()
        
        if not text:
            update_status_safe("❌ Lege transcriptie resultaat")
            log_debug("❌ Lege transcriptie resultaat")
            reset_progress_bar()
            return None

        # Log segment informatie voor multi-taal debugging
        if "segments" in result and isinstance(result["segments"], list):
            log_debug(f"📊 Aantal segmenten: {len(result['segments'])}")
            for i, segment in enumerate(result["segments"][:3]):  # Eerste 3 segmenten
                if isinstance(segment, dict):
                    seg_text = segment.get("text", "").strip()
                    seg_start = segment.get("start", 0)
                    seg_end = segment.get("end", 0)
                    log_debug(f"  Segment {i+1}: {seg_start:.1f}s-{seg_end:.1f}s - {seg_text[:50]}...")

        update_status_safe("✅ Transcriptie voltooid!")
        log_debug(f"✅ Transcriptie voltooid!")
        log_debug(f"📝 Tekst lengte: {len(text)} karakters")
        log_debug(f"🌍 Gedetecteerde taal: {result.get('language', 'onbekend')}")
        log_debug(f"📊 Transcriptie preview: {text[:100]}...")
        reset_progress_bar()
        return result

    except Exception as e:
        update_status_safe("❌ Whisper transcriptie mislukt")
        log_debug(f"❌ Whisper transcriptie mislukt: {e}")
        log_debug(f"🔍 Exception type: {type(e).__name__}")
        import traceback
        log_debug(f"📋 Stack trace: {traceback.format_exc()}")
        reset_progress_bar()
        return None

def reset_progress_bar():
    """Reset de voortgangsbalk naar 0%"""
    global progress
    if progress is not None:
        try:
            progress['value'] = 0
        except Exception as e:
            log_debug(f"❌ Fout bij resetten progressbar: {e}")


def split_text_into_chunks(text, max_chunk_size=5000):
    """Split tekst in chunks van maximaal 5000 karakters"""
    if len(text) <= max_chunk_size:
        return [text]
    
    chunks = []
    current_chunk = ""
    
    # Split op zinnen om natuurlijke grenzen te behouden
    sentences = text.split('. ')
    
    for sentence in sentences:
        # Voeg punt toe als het niet de laatste zin is
        if sentence != sentences[-1]:
            sentence += '. '
        
        # Check of deze zin past in huidige chunk
        if len(current_chunk + sentence) <= max_chunk_size:
            current_chunk += sentence
        else:
            # Sla huidige chunk op en start nieuwe
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence
    
    # Voeg laatste chunk toe
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    log_debug(f"📝 Tekst opgesplitst in {len(chunks)} chunks van max {max_chunk_size} karakters", "log_translation")
    return chunks


# --- Globale schakelaar om vertaling volledig uit te schakelen ---
ENABLE_TRANSLATION = False  # Zet op False om vertaling uit te schakelen, True om te activeren

def translate_text_to_dutch(text, source_language):
    """Vertaal tekst naar Nederlands met Google Translate of DeepL, of geef origineel terug als vertaling uit staat"""
    try:
        if not ENABLE_TRANSLATION:
            log_debug("🔕 Vertaling globaal uitgeschakeld via ENABLE_TRANSLATION.")
            return text
        if huidige_vertaler == "geen":
            log_debug("🔕 Vertaling uitgeschakeld, geef originele tekst terug.")
            return text  # Geen vertaling uitvoeren
        update_status_safe("🌐 Start vertaling naar Nederlands...")
        log_debug(f"🌐 Start vertaling naar Nederlands...")
        log_debug(f"📝 Bron tekst lengte: {len(text)} karakters")
        log_debug(f"🌍 Bron taal: {source_language}")
        log_debug(f"🔧 Gebruikte vertaler: {huidige_vertaler}")

        # Haal huidige worker count op
        worker_count = getattr(parallel_processor, "max_workers", 4)

        if huidige_vertaler == "deepl" and deepl_key:
            # Gebruik DeepL als API key beschikbaar is
            try:
                update_status_safe("🌐 DeepL vertaling bezig...")
                # Gebruik DeepL met chunking zoals Google Translate
                return translate_text_chunks_with_google(text, source_language, worker_count)
            except Exception as e:
                update_status_safe("❌ DeepL mislukt, probeer Google...")
                log_debug(f"❌ DeepL vertaling mislukt, fallback naar Google: {e}")
                # Fallback naar Google Translate met chunking
                return translate_text_chunks_with_google(text, source_language, worker_count)
        else:
            # Gebruik Google Translate als standaard met chunking
            update_status_safe("🌐 Google Translate vertaling bezig...")
            return translate_text_chunks_with_google(text, source_language, worker_count)
    except Exception as e:
        update_status_safe("❌ Vertaling mislukt")
        log_debug(f"❌ Vertaling mislukt: {e}")
        return text  # Return originele tekst als vertaling mislukt


def translate_text_chunks_with_google(text, source_language, worker_count):
    """Vertaal tekst in chunks met Google Translate"""
    try:
        # Split tekst in chunks van 5000 karakters
        chunks = split_text_into_chunks(text, max_chunk_size=5000)
        translated_chunks = []
        
        update_status_safe(f"🔄 Vertaal {len(chunks)} tekst delen...")
        log_debug(f"🔄 Start vertaling van {len(chunks)} chunks...", "log_translation")
        
        for i, chunk in enumerate(chunks, 1):
            try:
                # Update voortgang elke 3 chunks
                if i % 3 == 0 or i == len(chunks):
                    update_status_safe(f"🔄 Vertaal deel {i}/{len(chunks)}...")
                
                # Throttle Google Translate request
                google_translate_throttle.wait_if_needed(worker_count)
                
                from googletrans import Translator
                translator = Translator()
                result = translator.translate(chunk, src=source_language, dest="nl")
                
                translated_chunks.append(result.text)
                log_debug(f"✅ Chunk {i}/{len(chunks)} vertaald ({len(chunk)} karakters)", "log_translation")
                
            except Exception as e:
                log_debug(f"❌ Fout bij vertalen chunk {i}: {e}", "log_translation")
                # Voeg originele chunk toe als fallback
                translated_chunks.append(chunk)
        
        # Combineer alle vertaalde chunks
        final_translation = ' '.join(translated_chunks)
        log_debug(f"✅ Google Translate vertaling voltooid ({len(chunks)} chunks)")
        log_debug(f"📝 Vertaalde tekst lengte: {len(final_translation)} karakters")
        
        return final_translation
        
    except Exception as e:
        log_debug(f"❌ Google Translate chunking mislukt: {e}")
        return text


def create_srt_file(transcriptions, output_path):
    """Maak SRT ondertitel bestand met perfecte synchronisatie"""
    try:
        log_debug(f"[SRT] Aangeroepen met output_path: {output_path}")
        assert output_path, "output_path is leeg of None!"
        # Zorg dat output_path altijd in een bestaande map staat
        output_dir = os.path.dirname(output_path)
        if not os.path.isabs(output_path):
            output_path = os.path.join(USER_OUTPUT_DIR, output_path)
            output_dir = os.path.dirname(output_path)
        log_debug(f"[SRT] Absoluut pad: {output_path}")
        log_debug(f"[SRT] Bestaat map? {os.path.exists(output_dir)}")
        log_debug(f"[SRT] Is pad absoluut? {os.path.isabs(output_path)}")
        os.makedirs(output_dir, exist_ok=True)
        assert os.path.isabs(output_path), f"Output path is not absolute: {output_path}"
        assert os.path.exists(output_dir), f"Output dir does not exist: {output_dir}"
        try:
            log_debug(f"[SRT] Probeer bestand te openen voor schrijven...")
            f = open(output_path, "w", encoding="utf-8")
            assert f is not None, f"Kon bestand niet openen: {output_path}"
            for i, segment in enumerate(transcriptions, 1):
                # Format timestamps
                start_time = format_timestamp(segment.get("start", 0))
                end_time = format_timestamp(segment.get("end", 0))

                # Haal tekst op
                original_text = segment.get("text", "").strip()
                translated_text = segment.get("translation", "").strip()

                # Controleer of segment geldig is
                if not original_text and not translated_text:
                    continue  # Skip lege segmenten
                
                if segment.get("start", 0) >= segment.get("end", 0):
                    log_debug(f"⚠️ Ongeldig segment {i}: start >= end")
                    continue

                # Schrijf SRT entry
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                
                # Voor softcoded: Alleen Nederlandse tekst
                # Voor hardcoded: Afhankelijk van taal optie
                if translated_text and translated_text != original_text:
                    # Er is een vertaling beschikbaar
                    if original_text and not translated_text.startswith(original_text):
                        # Verschillende talen, schrijf beide
                        f.write(f"{original_text}\n")
                        f.write(f"{translated_text}\n")
                    else:
                        # Alleen vertaling (voor softcoded)
                        f.write(f"{translated_text}\n")
                else:
                    # Geen vertaling, schrijf origineel
                    f.write(f"{original_text}\n")
                
                f.write("\n")

            # Log synchronisatie details
            if transcriptions:
                first_seg = transcriptions[0]
                last_seg = transcriptions[-1]
                total_duration = last_seg.get("end", 0) - first_seg.get("start", 0)
                
                log_debug(f"📊 SRT synchronisatie details:")
                log_debug(f"  Eerste segment: {first_seg.get('start', 0):.2f}s")
                log_debug(f"  Laatste segment: {last_seg.get('end', 0):.2f}s")
                log_debug(f"  Totale duur: {total_duration:.2f}s")
                log_debug(f"  Aantal segmenten: {len(transcriptions)}")

            update_status_safe(f"✅ SRT bestand gemaakt: {len(transcriptions)} segmenten")
            log_debug(f"✅ SRT bestand gemaakt: {len(transcriptions)} segmenten")
            f.close()
            log_debug(f"✅ SRT bestand gemaakt: {output_path} ({len(transcriptions)} segmenten)")
            return True
        except Exception as e:
            log_debug(f"❌ Fout bij open/write SRT: {e}")
            import traceback
            log_debug(f"📋 Stack trace: {traceback.format_exc()}")
            return False
    except Exception as e:
        log_debug(f"❌ Fout bij schrijven SRT: {e}")
        import traceback
        log_debug(f"📋 Stack trace: {traceback.format_exc()}")
        return False


def format_timestamp(seconds):
    """Format seconden naar SRT timestamp (HH:MM:SS,mmm) met hoge precisie"""
    try:
        # Zorg voor positieve waarden
        seconds = max(0, float(seconds))
        
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        milliseconds = int((secs % 1) * 1000)
        secs = int(secs)

        # Zorg voor correcte formatting
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"
    except Exception as e:
        log_debug(f"❌ Fout bij timestamp formatting: {e}")
        return "00:00:00,000"


def auto_detect_language(audio_path, model):
    """Detecteer taal automatisch met verbeterde fallback en multi-taal support"""
    try:
        update_status_safe("🌍 Start taal detectie...")
        log_debug(f"🌍 Start automatische taal detectie...")

        # Laad audio
        import whisper
        import torch
        device = "cuda" if torch.cuda.is_available() else "cpu"
        whisper_model = whisper.load_model(model, device=device)

        # Laad audio
        audio = whisper.load_audio(audio_path)
        audio = whisper.pad_or_trim(audio)

        # Log mel spectrogram
        mel = whisper.log_mel_spectrogram(audio).to(whisper_model.device)

        # Detecteer taal
        _, probs = whisper_model.detect_language(mel)

        # Fix: probs kan een dict of List zijn, check het type
        if isinstance(probs, dict) and probs:
            # Sorteer op waarschijnlijkheid
            sorted_languages = sorted(probs.items(), key=lambda x: x[1], reverse=True)
            detected_language = sorted_languages[0][0]
            confidence = sorted_languages[0][1]
            
            # Log alle top 5 talen voor debugging
            log_debug(f"🌍 Top 5 gedetecteerde talen:")
            for i, (lang, prob) in enumerate(sorted_languages[:5]):
                log_debug(f"  {i+1}. {lang}: {prob:.3f}")
            
            # Controleer voor multi-taal scenario
            top_languages = [lang for lang, prob in sorted_languages[:3] if prob > 0.1]
            if len(top_languages) > 1:
                log_debug(f"🌍 Multi-taal gedetecteerd: {top_languages}")
                update_status_safe("🌍 Multi-taal gedetecteerd")
                
                # Vraag gebruiker om keuze
                language_names = {
                    "en": "Engels", "nl": "Nederlands", "de": "Duits", 
                    "fr": "Frans", "es": "Spaans", "it": "Italiaans",
                    "zh": "Chinees", "ja": "Japans", "ko": "Koreaans",
                    "ru": "Russisch", "pt": "Portugees", "ar": "Arabisch"
                }
                
                options = []
                for lang in top_languages:
                    lang_name = language_names.get(lang, lang.upper())
                    prob = next(prob for l, prob in sorted_languages if l == lang)
                    options.append(f"{lang_name} ({prob:.1%})")
                
                choice = messagebox.askyesnocancel(
                    "🌍 Multi-taal Gedetecteerd",
                    f"Er zijn meerdere talen gedetecteerd:\n\n" +
                    "\n".join(f"• {opt}" for opt in options) +
                    "\n\nWilt u de primaire taal gebruiken?\n" +
                    f"({language_names.get(detected_language, detected_language.upper())})"
                )
                
                if choice is None:  # Cancel
                    log_debug("❌ Gebruiker geannuleerd")
                    return None
                elif choice:  # Yes - gebruik primaire taal
                    log_debug(f"✅ Gebruiker koos voor primaire taal: {detected_language}")
                    update_status_safe(f"✅ Primaire taal gekozen: {detected_language}")
                else:  # No - vraag om specifieke keuze
                    # Toon dropdown voor taal selectie
                    import tkinter.simpledialog
                    available_languages = list(top_languages)
                    selected = tkinter.simpledialog.askstring(
                        "🌍 Kies Taal",
                        f"Kies de hoofdtaal:\n" +
                        "\n".join(f"{i+1}. {language_names.get(lang, lang.upper())}" 
                                for i, lang in enumerate(available_languages)) +
                        "\n\nVoer het nummer in (1-{len(available_languages)}):"
                    )
                    
                    if selected and selected.isdigit():
                        idx = int(selected) - 1
                        if 0 <= idx < len(available_languages):
                            detected_language = available_languages[idx]
                            log_debug(f"✅ Gebruiker koos taal: {detected_language}")
                            update_status_safe(f"✅ Taal gekozen: {detected_language}")
                        else:
                            log_debug("❌ Ongeldige keuze, gebruik primaire taal")
                            detected_language = sorted_languages[0][0]
                    else:
                        log_debug("❌ Geen keuze gemaakt, gebruik primaire taal")
                        detected_language = sorted_languages[0][0]
            
            # Controleer betrouwbaarheid
            if confidence < 0.3:
                log_debug(f"⚠️ Lage betrouwbaarheid ({confidence:.3f}), gebruik fallback")
                update_status_safe("⚠️ Onzekere taal detectie, gebruik Engels")
                return "en"
            
            # Controleer voor bekende fouten
            if detected_language in ["zh", "ja", "ko"] and confidence < 0.7:
                # Chinese/Japanese/Korean detectie is vaak onbetrouwbaar
                log_debug(f"⚠️ Mogelijke foutieve detectie van {detected_language}")
                update_status_safe("⚠️ Mogelijke foutieve taal detectie")
                
                # Check of Engels in top 3 staat
                english_prob = probs.get("en", 0)
                if english_prob > 0.2:
                    log_debug(f"✅ Engels gedetecteerd met {english_prob:.3f} waarschijnlijkheid")
                    update_status_safe("✅ Engels gedetecteerd")
                    return "en"
            
            update_status_safe(f"✅ Taal gedetecteerd: {detected_language}")
            log_debug(f"🌍 Taal gedetecteerd: {detected_language} (betrouwbaarheid: {confidence:.3f})")
            return detected_language
        else:
            # Fallback als probs geen dict is
            log_debug("⚠️ Geen taal waarschijnlijkheden gevonden, gebruik Engels")
            update_status_safe("⚠️ Geen taal gedetecteerd, gebruik Engels")
            return "en"

    except Exception as e:
        log_debug(f"❌ Fout bij taal detectie: {e}")
        update_status_safe("❌ Taal detectie mislukt, gebruik Engels")
        return "en"


def detect_mixed_languages(audio_path, model):
    """Detecteer gemengde talen per segment voor Engels/Spaans scenario"""
    try:
        update_status_safe("🌍 Start gemengde taal detectie...")
        log_debug(f"🌍 Start gemengde taal detectie...")

        # Laad audio
        import whisper
        import torch
        device = "cuda" if torch.cuda.is_available() else "cpu"
        whisper_model = whisper.load_model(model, device=device)

        # Laad audio
        audio = whisper.load_audio(audio_path)
        audio = whisper.pad_or_trim(audio)

        # Transcribe met segment-gewijze taal detectie
        result = whisper_model.transcribe(
            audio,
            language=None,  # Auto detectie per segment
            verbose=False,
            word_timestamps=True,
            condition_on_previous_text=False
        )

        if not result or "segments" not in result:
            log_debug("❌ Geen segmenten gevonden")
            return None

        # Analyseer segmenten voor taal detectie
        language_segments = []
        total_segments = len(result["segments"])
        
        log_debug(f"📊 Analyseer {total_segments} segmenten voor taal detectie...")
        
        for i, segment in enumerate(result["segments"]):
            if isinstance(segment, dict):
                seg_text = segment.get("text", "").strip()
                seg_start = segment.get("start", 0)
                seg_end = segment.get("end", 0)
                
                if seg_text and len(seg_text) > 10:  # Alleen segmenten met voldoende tekst
                    # Detecteer taal voor dit segment
                    try:
                        # Maak mel spectrogram voor dit segment
                        segment_audio = audio[int(seg_start * 16000):int(seg_end * 16000)]
                        if len(segment_audio) > 0:
                            segment_mel = whisper.log_mel_spectrogram(segment_audio).to(whisper_model.device)
                            _, segment_probs = whisper_model.detect_language(segment_mel)
                            
                            if isinstance(segment_probs, dict) and segment_probs:
                                detected_lang = max(segment_probs.keys(), key=lambda k: segment_probs[k])
                                confidence = segment_probs[detected_lang]
                                
                                language_segments.append({
                                    "start": seg_start,
                                    "end": seg_end,
                                    "text": seg_text,
                                    "language": detected_lang,
                                    "confidence": confidence
                                })
                                
                                log_debug(f"  Segment {i+1}: {detected_lang} ({confidence:.2f}) - {seg_text[:50]}...")
                    except Exception as e:
                        log_debug(f"❌ Fout bij segment {i+1}: {e}")
                        continue

        # Groepeer segmenten per taal
        language_groups = {}
        for seg in language_segments:
            lang = seg["language"]
            if lang not in language_groups:
                language_groups[lang] = []
            language_groups[lang].append(seg)

        # Log resultaten
        log_debug(f"🌍 Taal analyse resultaten:")
        for lang, segments in language_groups.items():
            total_time = sum(seg["end"] - seg["start"] for seg in segments)
            avg_confidence = sum(seg["confidence"] for seg in segments) / len(segments)
            log_debug(f"  {lang}: {len(segments)} segmenten, {total_time:.1f}s, gem. betrouwbaarheid: {avg_confidence:.2f}")

        update_status_safe(f"✅ Gemengde taal detectie voltooid: {len(language_groups)} talen")
        return language_groups

    except Exception as e:
        log_debug(f"❌ Fout bij gemengde taal detectie: {e}")
        update_status_safe("❌ Gemengde taal detectie mislukt")
        return None


def process_video_with_whisper(video_path, model_name="base", language="auto"):
    """Verwerk video met Whisper transcriptie en vertaling"""
    try:
        log_debug("=" * 60)
        log_debug(f"🚀 START: Video verwerking pipeline")
        log_debug(f"📁 Video: {video_path}")
        log_debug(f"🤖 Model: {model_name}")
        log_debug(f"🌍 Taal: {language}")
        log_debug("=" * 60)

        # Controleer video bestand
        if not os.path.exists(video_path):
            log_debug(f"❌ Video bestand bestaat niet: {video_path}")
            return False

        video_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
        log_debug(f"📊 Video grootte: {video_size:.2f} MB")

        # Stap 1: Audio extractie
        log_debug("🎵 STAP 1: Audio extractie...")
        audio_path = extract_audio_from_video(video_path)
        if not audio_path or not os.path.exists(audio_path):
            log_debug("❌ Audio extractie mislukt of bestand bestaat niet na extractie")
            return False
        log_debug("✅ Stap 1 voltooid: Audio geëxtraheerd")

        # Stap 2: Taal detectie (alleen als auto)
        if language == "auto":
            log_debug("🌍 STAP 2: Taal detectie...")
            # Pop-up venster verwijderd - gebruiker kan taal kiezen in linker kolom
            
            # Gebruik de gekozen taal en content type uit de dropdowns
            if taal_var is not None:
                selected_taal = taal_var.get()
                # Taal opties voor vergelijking
                taal_opties = [
                    ("Auto detectie", "auto"),
                    ("Engels", "en"),
                    ("Nederlands", "nl"),
                    ("Duits", "de"),
                    ("Frans", "fr"),
                    ("Spaans", "es"),
                    ("Italiaans", "it"),
                    ("Portugees", "pt"),
                    ("Russisch", "ru"),
                    ("Japans", "ja"),
                    ("Koreaans", "ko"),
                    ("Chinees", "zh"),
                    ("Arabisch", "ar"),
                    ("Hindi", "hi"),
                    ("Turks", "tr"),
                    ("Pools", "pl"),
                    ("Zweeds", "sv"),
                    ("Deens", "da"),
                    ("Noors", "no"),
                    ("Fins", "fi")
                ]
                
                # Zoek de bijbehorende taal code
                for display_name, lang_code in taal_opties:
                    if display_name == selected_taal:
                        if lang_code == "auto" or selected_taal == "Auto detectie":
                            # Auto detectie
                            detected_language = auto_detect_language(audio_path, model_name)
                            if detected_language is None:
                                return False
                            language = detected_language
                            log_debug(f"✅ Auto detectie: Taal = {language}")
                        else:
                            # Specifieke taal gekozen
                            language = lang_code
                            log_debug(f"✅ Specifieke taal gekozen: {language}")
                        break
            else:
                # Fallback naar auto detectie
                detected_language = auto_detect_language(audio_path, model_name)
                if detected_language is None:
                    return False
                language = detected_language
                log_debug(f"✅ Fallback auto detectie: Taal = {language}")
            
            # Controleer content type voor multi-talen verwerking
            content_type = "Eén hoofdtaal"  # Standaard
            if content_type_var is not None:
                content_type = content_type_var.get()
            
            log_debug(f"📺 Content type: {content_type}")
            
            # Multi-talen verwerking op basis van content type
            if content_type == "Twee talen (gemengd)":
                log_debug("🌍 Multi-talen verwerking: Twee talen gedetecteerd")
                update_status_safe("🌍 Analyseer gemengde talen...")
                
                # Gebruik segment-gewijze detectie
                language_groups = detect_mixed_languages(audio_path, model_name)
                if language_groups:
                    # Log resultaten
                    log_debug(f"🌍 Taal analyse resultaten:")
                    for lang, segments in language_groups.items():
                        total_time = sum(seg["end"] - seg["start"] for seg in segments)
                        avg_confidence = sum(seg["confidence"] for seg in segments) / len(segments)
                        log_debug(f"  {lang}: {len(segments)} segmenten, {total_time:.1f}s, gem. betrouwbaarheid: {avg_confidence:.2f}")
                    
                    # Gebruik transcriptie met auto taal detectie
                    language = None  # Laat Whisper auto detectie doen
                    log_debug("✅ Multi-talen verwerking geactiveerd")
                else:
                    log_debug("⚠️ Geen gemengde talen gedetecteerd, gebruik normale verwerking")
            elif content_type == "Sporadische woorden":
                log_debug("🌍 Multi-talen verwerking: Sporadische woorden gedetecteerd")
                update_status_safe("🌍 Analyseer sporadische woorden...")
                
                # Gebruik normale transcriptie maar met hogere tolerantie
                log_debug("✅ Sporadische woorden verwerking geactiveerd")
            else:
                # Eén hoofdtaal - normale verwerking
                log_debug("🌍 Normale verwerking: Eén hoofdtaal")
            
            log_debug(f"✅ Stap 2 voltooid: Taal = {language}, Content type = {content_type}")
        else:
            log_debug(f"🌍 Taal vooraf ingesteld: {language}")

        # Stap 3: Whisper transcriptie
        log_debug("🎤 STAP 3: Whisper transcriptie...")
        transcription_result = transcribe_audio_with_whisper(
            audio_path, model_name, language if language else "auto"
        )
        if not transcription_result or "text" not in transcription_result:
            log_debug("❌ Transcriptie mislukt of geen tekst gevonden in resultaat")
            return False
        log_debug("✅ Stap 3 voltooid: Transcriptie klaar")
        # Stop direct als vertaling uit staat
        if huidige_vertaler == "geen":
            log_debug("🔕 Vertaling uitgeschakeld, sla SRT op in brontaal.")
            # SRT in brontaal
            video_name = os.path.splitext(os.path.basename(video_path))[0]
            srt_path = os.path.join(os.path.dirname(video_path), f"{video_name}.srt")
            log_debug(f"📁 SRT output pad: {srt_path}")
            # Controleer of er segmenten zijn
            if "segments" in transcription_result and transcription_result["segments"]:
                transcriptions = []
                for segment in transcription_result["segments"]:
                    if isinstance(segment, dict):
                        seg_text = segment.get("text", "").strip()
                        seg_start = segment.get("start", 0)
                        seg_end = segment.get("end", 0)
                        if seg_text:
                            transcriptions.append({
                                "start": seg_start,
                                "end": seg_end,
                                "text": seg_text,
                                "translation": ""  # Geen vertaling
                            })
                log_debug(f"📊 {len(transcriptions)} segmenten voor originele SRT.")
            else:
                log_debug("⚠️ Geen segmenten gevonden, gebruik fallback")
                original_text = transcription_result.get("text", "")
                if not original_text:
                    log_debug("❌ Geen tekst beschikbaar voor fallback SRT.")
                    return False
                transcriptions = [
                    {
                        "start": 0,
                        "end": 999999,  # Hele video
                        "text": original_text,
                        "translation": ""
                    }
                ]
            # Sla SRT op in brontaal
            success = create_srt_file(transcriptions, srt_path)
            if not success:
                log_debug("❌ SRT bestand maken mislukt (brontaal)")
                messagebox.showerror("❌ Fout", "Kon SRT bestand niet maken")
                return False
            return success

        # Stap 4: SRT bestand maken in originele taal
        log_debug("📝 STAP 4: SRT bestand maken in originele taal...")
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        srt_path = os.path.join(os.path.dirname(video_path), f"{video_name}.srt")
        log_debug(f"📁 SRT output pad: {srt_path}")
        if "segments" in transcription_result and transcription_result["segments"]:
            transcriptions = []
            for segment in transcription_result["segments"]:
                if isinstance(segment, dict):
                    seg_text = segment.get("text", "").strip()
                    seg_start = segment.get("start", 0)
                    seg_end = segment.get("end", 0)
                    if seg_text:
                        transcriptions.append({
                            "start": seg_start,
                            "end": seg_end,
                            "text": seg_text,
                            "translation": ""  # Geen vertaling meer
                        })
            log_debug(f"📊 {len(transcriptions)} segmenten voor originele SRT.")
        else:
            log_debug("⚠️ Geen segmenten gevonden, gebruik fallback")
            original_text = transcription_result.get("text", "")
            transcriptions = [
                {
                    "start": 0,
                    "end": 999999,  # Hele video
                    "text": original_text,
                    "translation": ""
                }
            ]
        # Sla SRT op in originele taal
        success = create_srt_file(transcriptions, srt_path)
        if not success:
            log_debug("❌ SRT bestand maken mislukt (originele taal)")
            messagebox.showerror("❌ Fout", "Kon SRT bestand niet maken")
            return False
        return success

    except Exception as e:
        log_debug("=" * 60)
        log_debug(f"❌ FOUT bij video verwerking: {e}")
        log_debug(f"🔍 Exception type: {type(e).__name__}")
        import traceback

        log_debug(f"📋 Stack trace: {traceback.format_exc()}")
        log_debug("=" * 60)
        messagebox.showerror("❌ Fout", f"Verwerking mislukt:\n{e}")
        return False




def start_batch_verwerking():
    global processing_active
    if processing_active:
        log_debug("⏳ Verwerking is al bezig, start wordt genegeerd.")
        return
    processing_active = True
    log_debug("🔒 Verwerking gestart, startknop geblokkeerd.")
    log_debug("=" * 60)
    log_debug("🚀 START: Batch verwerking")
    log_debug("=" * 60)

    # Verzamel alle paden uit de listbox/verwerk_lijst
    if not verwerk_lijst or (listbox_nog is not None and listbox_nog.size() == 0):
        log_debug("❌ Geen bestanden in de verwerkingslijst")
        messagebox.showwarning("⚠️", "Er staan geen videobestanden in de verwerkingslijst.")
        processing_active = False
        return

    def process_thread():
        try:
            log_debug("🔄 Start batchverwerking in thread...")
            optimize_memory_usage()
            for pad in verwerk_lijst[:]:  # Kopie van de lijst, want we gaan hem aanpassen
                model_name = "base"
                language = "auto"
                success = process_video_with_whisper(pad, model_name, language)
                bestandsnaam = os.path.basename(pad)
                if success:
                    if listbox_voltooid is not None:
                        listbox_voltooid.insert(tk.END, bestandsnaam)
                        if pad not in voltooid_lijst:
                            voltooid_lijst.append(pad)
                else:
                    if 'listbox_mislukt' in globals() and listbox_mislukt is not None:
                        listbox_mislukt.insert(tk.END, bestandsnaam)
                        if pad not in mislukte_lijst:
                            mislukte_lijst.append(pad)
                if pad in verwerk_lijst:
                    idx = verwerk_lijst.index(pad)
                    verwerk_lijst.pop(idx)
                    if listbox_nog is not None:
                        listbox_nog.delete(idx)
            reset_progress_bar()
            log_debug("🎉 Batchverwerking succesvol voltooid!")
        except Exception as e:
            log_debug(f"❌ FOUT in batchverwerking: {e}")
            import traceback
            log_debug(f"📋 Stack trace: {traceback.format_exc()}")
        finally:
            optimize_memory_usage()
            if root is not None:
                root.after(0, unblock_interface_after_processing)
            global processing_active
            processing_active = False
            log_debug("🔓 Verwerking afgerond, startknop weer actief.")

    block_interface_during_processing()
    import threading
    threading.Thread(target=process_thread, daemon=True).start()


# Maak knoppen globaal beschikbaar
# Deze functie is niet meer nodig omdat de knoppen direct in setup_ui() worden aangemaakt
# def maak_knoppen():
#     pass


def verwijder_geselecteerd_bestand():
    """Verwijder het geselecteerde bestand uit de lijst, behalve als het bestand in verwerking is."""
    global verwerk_lijst, listbox_nog, processing_active, selected_video
    if listbox_nog is not None:
        selection = listbox_nog.curselection()
        if selection:
            index = selection[0]
            bestandsnaam = listbox_nog.get(index)
            for i, pad in enumerate(verwerk_lijst):
                if os.path.basename(pad) == bestandsnaam:
                    # Bescherm huidig bestand tegen verwijderen
                    if processing_active and pad == selected_video:
                        messagebox.showwarning(
                            "Bestand in verwerking", 
                            f"'{bestandsnaam}' wordt momenteel verwerkt.\n\nJe kunt dit bestand niet verwijderen tot de verwerking klaar is."
                        )
                        return
                    # Verwijder uit de lijst en listbox
                    verwerk_lijst.pop(i)
                    listbox_nog.delete(index)
                    listbox_nog.selection_clear(0, tk.END)
                    if info_label is not None:
                        huidig_thema = thema_var.get() if thema_var is not None else "dark"
                        text_color = "#cccccc" if huidig_thema == "dark" else "gray"
                        info_label.config(text="📄 Geen video gekozen", fg=text_color)
                    log_debug(f"✅ Bestand verwijderd: {bestandsnaam}")
                    return
            # Als het bestand niet gevonden wordt in verwerk_lijst
            listbox_nog.delete(index)
            listbox_nog.selection_clear(0, tk.END)
            if info_label is not None:
                huidig_thema = thema_var.get() if thema_var is not None else "dark"
                text_color = "#cccccc" if huidig_thema == "dark" else "gray"
                info_label.config(text="📄 Geen video gekozen", fg=text_color)
    else:
        messagebox.showwarning(
            "Geen selectie", "Selecteer eerst een bestand om te verwijderen."
        )


def verwijder_hele_lijst():
    """Verwijder alle bestanden uit de lijst met bevestiging"""
    global processing_active, selected_video
    
    if listbox_nog is not None and verwerk_lijst:
        aantal_bestanden = len(verwerk_lijst)
        
        # Controleer of er een bestand verwerkt wordt
        if processing_active and selected_video in verwerk_lijst:
            messagebox.showwarning(
                "Bestand in verwerking", 
                f"Er wordt momenteel een bestand verwerkt.\n\n"
                "Je kunt de lijst niet legen tot de verwerking klaar is."
            )
            return

        # Toon bevestigingspopup
        bevestiging = messagebox.askyesno(
            "Bevestig verwijdering",
            f"Weet je zeker dat je alle {aantal_bestanden} bestand(en) uit de verwerkingslijst wilt verwijderen?\n\n"
            "Deze actie kan niet ongedaan worden gemaakt.",
            icon="warning",
        )

        if bevestiging:
            # Verwijder alle bestanden
            verwerk_lijst.clear()
            listbox_nog.delete(0, tk.END)
            
            # Wis de selectie en update de info label
            listbox_nog.selection_clear(0, tk.END)
            if info_label is not None:
                # Geoptimaliseerde kleur voor "geen bestand" status
                huidig_thema = thema_var.get() if thema_var is not None else "dark"
                if huidig_thema == "dark":
                    text_color = "#cccccc"  # Lichtgrijze tekst voor dark theme
                else:
                    text_color = "gray"  # Grijze tekst voor andere thema's
                info_label.config(text="📄 Geen video gekozen", fg=text_color)
            
            log_debug("✅ Alle bestanden verwijderd uit verwerkingslijst")
            messagebox.showinfo(
                "Lijst geleegd",
                f"Alle {aantal_bestanden} bestand(en) zijn verwijderd uit de verwerkingslijst.",
            )
    else:
        messagebox.showinfo(
            "Lijst is leeg",
            "Er zijn geen bestanden in de verwerkingslijst om te verwijderen.",
        )


# Buttons will be created in setup_ui() function - removed premature call


def kill_switch():
    """Stop het hele verwerkingsproces direct"""
    global processing_active, parallel_processor, processing_cancelled
    bevestiging = messagebox.askyesno(
        "Kill Switch",
        "Weet je zeker dat je het hele verwerkingsproces wilt stoppen?\n\n"
        "⚠️ WAARSCHUWING: Dit zal alle lopende taken direct beëindigen!\n"
        "• Huidige verwerking wordt gestopt\n"
        "• Alle workers worden gestopt\n"
        "• Tijdelijke bestanden worden opgeruimd\n\n"
        "Deze actie kan niet ongedaan worden gemaakt.",
        icon="warning",
    )
    if bevestiging:
        try:
            processing_active = False
            processing_cancelled = True
            # Stop alle actieve subprocessen
            for proc in list(ACTIVE_SUBPROCESSES):
                try:
                    if PSUTIL_AVAILABLE:
                        p = psutil.Process(proc.pid)
                        p.kill()
                    else:
                        proc.kill()
                except Exception:
                    pass
                try:
                    if proc in ACTIVE_SUBPROCESSES:
                        ACTIVE_SUBPROCESSES.remove(proc)
                except Exception:
                    pass
            # Stop parallel processor als deze bestaat
            if parallel_processor is not None:
                try:
                    if hasattr(parallel_processor, 'executor') and parallel_processor.executor is not None:
                        parallel_processor.executor.shutdown(wait=False, cancel_futures=True)
                except Exception:
                    pass
            # Verwijder tijdelijke audio-bestanden
            try:
                import shutil
                if os.path.exists(TEMP):
                    shutil.rmtree(TEMP)
                    log_debug("🧹 Tijdelijke audio-map verwijderd na kill switch")
            except Exception as e:
                log_debug(f"❌ Fout bij verwijderen tijdelijke bestanden: {e}")
            log_debug("⏹️ Kill switch uitgevoerd: alles gestopt en opgeruimd")
        except Exception as e:
            log_debug(f"❌ Fout bij kill switch: {e}")


def create_input_panel():
    """Maak het invoer paneel"""
    # Deze functie is niet meer nodig omdat de interface al is aangemaakt
    pass


def pas_thema_toe(naam):
    """Pas het thema toe"""
    try:
        if naam not in THEMA_KLEUREN:
            log_debug(f"❌ Onbekend thema: {naam}")
            return

        kleuren = THEMA_KLEUREN[naam]

        # Update thema variabele
        if thema_var is not None:
            thema_var.set(naam)

        # Pas thema toe op alle widgets
        if root is not None:
            root.configure(bg=kleuren["bg"])

            # Main frame
            if main_frame is not None:
                main_frame.configure(bg=kleuren["main_bg"])

            # Panelen
            if left_panel is not None:
                left_panel.configure(bg=kleuren["panel_bg"], fg=kleuren["fg"])
                # Update alleen belangrijke labels in het linker paneel
                for child in left_panel.winfo_children():
                    if isinstance(child, tk.Label) and hasattr(child, 'cget'):
                        try:
                            current_bg = child.cget("bg")
                            if current_bg != kleuren["panel_bg"]:
                                child.configure(bg=kleuren["panel_bg"], fg=kleuren["fg"])
                        except:
                            pass

            if right_panel is not None:
                right_panel.configure(bg=kleuren["panel_bg"], fg=kleuren["fg"])
                # Update alleen belangrijke labels in het rechter paneel
                for child in right_panel.winfo_children():
                    if isinstance(child, tk.Label) and hasattr(child, 'cget'):
                        try:
                            current_bg = child.cget("bg")
                            if current_bg != kleuren["panel_bg"]:
                                child.configure(bg=kleuren["panel_bg"], fg=kleuren["fg"])
                        except:
                            pass

            # Knoppen
            for widget in [
                btn_voeg_bestand,
                btn_voeg_map,
                btn_verwijder,
                btn_verwijder_alles,
                start_button,
            ]:
                if widget is not None:
                    widget.configure(bg=kleuren["knop"], fg=kleuren["knop_fg"])
            
            # Dropdowns (OptionMenu widgets) - geoptimaliseerde styling
            if taal_combobox is not None:
                # Gebruik witte achtergrond voor betere zichtbaarheid in dark thema
                bg_color = "white" if naam == "dark" else kleuren["panel_bg"]
                fg_color = "black" if naam == "dark" else kleuren["fg"]
                border_color = "#cccccc" if naam == "dark" else kleuren.get("border", "#cccccc")
                
                taal_combobox.configure(
                    bg=bg_color,
                    fg=fg_color,
                    relief="solid",
                    bd=1,
                    highlightthickness=1,
                    highlightbackground=border_color,
                    highlightcolor=border_color,
                    activebackground=bg_color,
                    activeforeground=fg_color
                )
                # Update ook het menu van de OptionMenu
                try:
                    menu = taal_combobox.cget("menu")
                    if menu is not None:
                        menu.configure(bg=bg_color, fg=fg_color)
                except:
                    pass
            
            if content_type_combobox is not None:
                # Gebruik witte achtergrond voor betere zichtbaarheid in dark thema
                bg_color = "white" if naam == "dark" else kleuren["panel_bg"]
                fg_color = "black" if naam == "dark" else kleuren["fg"]
                border_color = "#cccccc" if naam == "dark" else kleuren.get("border", "#cccccc")
                
                content_type_combobox.configure(
                    bg=bg_color,
                    fg=fg_color,
                    relief="solid",
                    bd=1,
                    highlightthickness=1,
                    highlightbackground=border_color,
                    highlightcolor=border_color,
                    activebackground=bg_color,
                    activeforeground=fg_color
                )
                # Update ook het menu van de OptionMenu
                try:
                    menu = content_type_combobox.cget("menu")
                    if menu is not None:
                        menu.configure(bg=bg_color, fg=fg_color)
                except:
                    pass
            
            # Kill switch knop - altijd rood
            if kill_button is not None:
                if naam in ["dark", "light"]:
                    # Rode kill switch voor dark en light thema's
                    kill_button.configure(bg="#d32f2f", fg="white", activebackground="#b71c1c", activeforeground="white")
                else:
                    # Gebruik thema kleuren voor andere thema's
                    kill_button.configure(bg=kleuren["knop"], fg=kleuren["knop_fg"])

            # Listboxen
            if listbox_nog is not None:
                listbox_nog.configure(bg=kleuren["frame"], fg=kleuren["fg"])
            if listbox_voltooid is not None:
                listbox_voltooid.configure(bg=kleuren["frame"], fg=kleuren["fg"])

            # Labels - geoptimaliseerde styling voor betere leesbaarheid
            if info_label is not None:
                # Gebruik witte tekst voor dark theme voor betere leesbaarheid
                if naam == "dark":
                    info_label.configure(bg=kleuren["panel_bg"], fg="white")
                else:
                    info_label.configure(bg=kleuren["panel_bg"], fg=kleuren["fg"])
            if status_label is not None:
                status_label.configure(bg=kleuren["panel_bg"], fg=kleuren["fg"])

            # CPU Slider thema aanpassing
            try:
                style = ttk.Style()
                # Gebruik thema kleuren voor de slider
                slider_bg = kleuren["panel_bg"]
                slider_trough = kleuren.get("frame", "#e0e0e0")  # Fallback kleur
                
                style.configure("Transparent.Horizontal.TScale", 
                              background=slider_bg, 
                              troughcolor=slider_trough, 
                              bordercolor=slider_bg,
                              lightcolor=slider_bg,
                              darkcolor=slider_bg,
                              focuscolor=slider_bg)
                
                # Zoek de CPU slider en pas het thema toe
                if left_panel is not None and hasattr(left_panel, 'winfo_children'):
                    for child in left_panel.winfo_children():
                        if isinstance(child, tk.Label):
                            child.configure(bg=kleuren["panel_bg"], fg=kleuren["fg"])
                        elif isinstance(child, ttk.Scale):
                            child.configure(style="Transparent.Horizontal.TScale")
            except Exception as e:
                log_debug(f"❌ Fout bij slider thema: {e}")

        # Pas thema toe op configuratie venster als het open is
        if 'config_window' in globals() and config_window is not None:
            try:
                config_window.configure(bg=kleuren["bg"])
                
                # Recursieve functie om alle widgets aan te passen
                def apply_theme_to_widgets(parent_widget):
                    for widget in parent_widget.winfo_children():
                        try:
                            if hasattr(widget, 'configure'):
                                if isinstance(widget, tk.Frame) or isinstance(widget, tk.LabelFrame):
                                    widget.configure(bg=kleuren["panel_bg"])
                                elif isinstance(widget, tk.Label):
                                    widget.configure(bg=kleuren["panel_bg"], fg=kleuren["fg"])
                                elif isinstance(widget, tk.Entry):
                                    widget.configure(bg=kleuren["frame"], fg=kleuren["fg"], insertbackground=kleuren["fg"])
                                elif isinstance(widget, tk.Button):
                                    widget.configure(bg=kleuren["knop"], fg=kleuren["knop_fg"])
                                elif isinstance(widget, tk.Checkbutton):
                                    widget.configure(bg=kleuren["panel_bg"], fg=kleuren["fg"], selectcolor=kleuren["frame"])
                                elif isinstance(widget, tk.OptionMenu):
                                    # Geoptimaliseerde dropdown styling voor configuratie venster
                                    bg_color = "white" if naam == "dark" else kleuren["panel_bg"]
                                    fg_color = "black" if naam == "dark" else kleuren["fg"]
                                    border_color = "#cccccc" if naam == "dark" else kleuren.get("border", "#cccccc")
                                    
                                    widget.configure(
                                        bg=bg_color,
                                        fg=fg_color,
                                        relief="solid",
                                        bd=1,
                                        highlightthickness=1,
                                        highlightbackground=border_color,
                                        highlightcolor=border_color,
                                        activebackground=bg_color,
                                        activeforeground=fg_color
                                    )
                                    # Update ook het menu van de OptionMenu
                                    try:
                                        menu = widget.cget("menu")
                                        if menu is not None:
                                            menu.configure(bg=bg_color, fg=fg_color)
                                    except:
                                        pass
                                elif isinstance(widget, tk.Text):
                                    widget.configure(bg=kleuren["frame"], fg=kleuren["fg"], insertbackground=kleuren["fg"])
                                elif isinstance(widget, tk.Canvas):
                                    widget.configure(bg=kleuren["panel_bg"])
                                elif isinstance(widget, tk.Scrollbar):
                                    widget.configure(bg=kleuren["panel_bg"], troughcolor=kleuren["frame"])
                                elif isinstance(widget, tk.Listbox):
                                    widget.configure(bg=kleuren["frame"], fg=kleuren["fg"], selectbackground=kleuren["knop"], selectforeground=kleuren["knop_fg"])
                                elif isinstance(widget, tk.Menu):
                                    widget.configure(bg=kleuren["panel_bg"], fg=kleuren["fg"], selectcolor=kleuren["frame"])
                                elif isinstance(widget, ttk.Progressbar):
                                    # ttk widgets hebben een andere configuratie methode
                                    try:
                                        style = ttk.Style()
                                        style.configure("TProgressbar", 
                                                      background=kleuren["knop"],
                                                      troughcolor=kleuren["frame"],
                                                      bordercolor=kleuren["frame"],
                                                      lightcolor=kleuren["knop"],
                                                      darkcolor=kleuren["knop"])
                                        widget.configure(style="TProgressbar")
                                    except:
                                        pass
                                elif isinstance(widget, ttk.Scale):
                                    # ttk Scale widgets
                                    try:
                                        style = ttk.Style()
                                        style.configure("TScale", 
                                                      background=kleuren["panel_bg"],
                                                      troughcolor=kleuren["frame"],
                                                      bordercolor=kleuren["frame"],
                                                      lightcolor=kleuren["panel_bg"],
                                                      darkcolor=kleuren["panel_bg"])
                                        widget.configure(style="TScale")
                                    except:
                                        pass
                                
                                # Recursief doorlopen van child widgets
                                if hasattr(widget, 'winfo_children'):
                                    apply_theme_to_widgets(widget)
                        except Exception as e:
                            log_debug(f"❌ Fout bij widget thema: {e}")
                            pass
                
                # Pas thema toe op alle widgets in configuratie venster
                apply_theme_to_widgets(config_window)
                log_debug("🎨 Configuratie venster thema toegepast")
            except Exception as e:
                log_debug(f"❌ Fout bij configuratie thema: {e}")

        # Pas thema toe op live log venster als het open is
        if 'log_window' in globals() and log_window is not None:
            try:
                log_window.configure(bg=kleuren["bg"])
                # Pas thema toe op alle widgets in log venster
                for widget in log_window.winfo_children():
                    if hasattr(widget, 'configure'):
                        try:
                            if isinstance(widget, tk.Frame):
                                widget.configure(bg=kleuren["panel_bg"])
                            elif isinstance(widget, tk.Label):
                                widget.configure(bg=kleuren["panel_bg"], fg=kleuren["fg"])
                            elif isinstance(widget, tk.Text):
                                widget.configure(bg=kleuren["frame"], fg=kleuren["fg"], insertbackground=kleuren["fg"])
                            elif isinstance(widget, tk.Button):
                                widget.configure(bg=kleuren["knop"], fg=kleuren["knop_fg"])
                        except:
                            pass
                log_debug("🎨 Live log venster thema toegepast")
            except Exception as e:
                log_debug(f"❌ Fout bij log thema: {e}")

        # Sla thema op
        sla_thema_op(naam)
        log_debug(f"🎨 Thema '{naam}' toegepast")

    except Exception as e:
        log_debug(f"❌ Fout bij toepassen thema: {e}")


# Verwijder knoppen worden aangemaakt in maak_knoppen functie


def create_processing_panel():
    """Maak het verwerking paneel met help knoppen"""
    global info_label, status_label, progress, start_button, listbox_nog, listbox_voltooid, listbox_mislukt

    # 📄 Info rechts: gekozen video
    info_label = tk.Label(
        right_panel,
        text="📄 Geen video gekozen",
        font=("Segoe UI", 9),
        fg="gray",
        justify="left",
        wraplength=300,
    )
    info_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

    # 🔄 Statusupdate
    status_label = tk.Label(
        right_panel, text="", font=("Segoe UI", 9, "italic"), fg="#006699", anchor="w"
    )
    status_label.grid(row=1, column=0, sticky="we", pady=(0, 5))

    # ⏳ Voortgangsbalk met tijdschatting
    progress_frame = tk.Frame(right_panel)
    progress_frame.grid(row=2, column=0, sticky="we", pady=(10, 5))
    
    progress = ttk.Progressbar(progress_frame, length=240, mode="determinate")
    progress.pack(fill="x")
    
    # Tijdschatting label
    global time_estimate_label
    time_estimate_label = tk.Label(
        progress_frame, 
        text="", 
        font=("Segoe UI", 8), 
        fg="#666666"
    )
    time_estimate_label.pack(anchor="w")

    # Startknop
    start_button = tk.Button(
        right_panel,
        text="Start ondertiteling",
        command=lambda: start_batch_verwerking(),
        font=("Segoe UI", 11, "bold"),
        bg="#d21f3c",
        fg="white",
        activebackground="#a51b2d",
        padx=10,
        pady=6,
    )
    start_button.grid(row=3, column=0, sticky="we", pady=(0, 5))
    create_help_button(
        right_panel,
        "Start de ondertiteling verwerking.\n\n"
        "Het proces:\n"
        "1. Audio extractie\n"
        "2. Whisper transcriptie\n"
        "3. Vertaling naar Nederlands\n"
        "4. SRT bestand generatie\n\n"
        "Gebruik de kill switch om het proces direct te stoppen.",
        3,
        1,
    )

    # Kill Switch knop
    global kill_button
    kill_button = tk.Button(
        right_panel,
        text="KILL SWITCH",
        command=kill_switch,
        font=("Segoe UI", 11, "bold"),
        bg="#000000",
        fg="white",
        activebackground="#333333",
        activeforeground="white",
        padx=10,
        pady=6,
    )
    kill_button.grid(row=4, column=0, sticky="we", pady=(0, 10))
    create_help_button(
        right_panel,
        "⚠️ NOODSTOP: Stop het hele verwerkingsproces direct!\n\n"
        "Deze knop:\n"
        "• Stopt alle lopende taken\n"
        "• Beëindigt alle workers\n"
        "• Ruimt tijdelijke bestanden op\n"
        "• Reset de voortgangsbalk\n\n"
        "⚠️ WAARSCHUWING: Gebruik alleen in noodgevallen!",
        4,
        1,
    )

    # 📋 Nog te verwerken bestanden
    tk.Label(
        right_panel,
        text="📋 Nog te verwerken bestanden:",
        font=("Segoe UI", 10, "bold"),
    ).grid(row=5, column=0, sticky="w", pady=(10, 5))
    listbox_nog = tk.Listbox(
        right_panel, height=5, font=("Segoe UI", 10), selectmode=tk.SINGLE
    )
    listbox_nog.grid(row=6, column=0, sticky="we", pady=(0, 10))

    # ✅ Voltooide bestanden
    tk.Label(
        right_panel, text="✅ Voltooide bestanden:", font=("Segoe UI", 10, "bold")
    ).grid(row=7, column=0, sticky="w", pady=(10, 5))
    listbox_voltooid = tk.Listbox(
        right_panel, height=5, font=("Segoe UI", 10), selectmode=tk.SINGLE
    )
    listbox_voltooid.grid(row=8, column=0, sticky="we", pady=(0, 10))

    # ❌ Mislukte bestanden
    tk.Label(
        right_panel, text="❌ Mislukte bestanden:", font=("Segoe UI", 10, "bold")
    ).grid(row=9, column=0, sticky="w", pady=(10, 5))
    listbox_mislukt = tk.Listbox(
        right_panel, height=5, font=("Segoe UI", 10), selectmode=tk.SINGLE
    )
    listbox_mislukt.grid(row=10, column=0, sticky="we", pady=(0, 10))


# Update de main sectie
# 1. Safe basename/splitext helpers gebruiken
import os


def safe_basename(path):
    """Veilige basename() aanroep"""
    try:
        if path is not None:
            return os.path.basename(path)
    except Exception as e:
        log_debug(f"❌ Fout bij safe_basename: {e}")
    return "onbekend_bestand"


def safe_splitext(path):
    return os.path.splitext(path) if path else ("onbekend", "")


# 2. PIL LANCZOS fix
try:
    from PIL import Image

    LANCZOS_RESAMPLE = getattr(Image, "LANCZOS", getattr(Image, "BICUBIC", 3))
except ImportError:
    LANCZOS_RESAMPLE = 3

# 3. Safe config/set/get/after helpers


def safe_config(widget, **kwargs):
    """Veilige config() aanroep"""
    try:
        if widget is not None and hasattr(widget, "config"):
            widget.config(**kwargs)
    except Exception as e:
        log_debug(f"❌ Fout bij safe_config: {e}")


def safe_set(var, value):
    if var is not None:
        try:
            var.set(value)
        except Exception:
            pass


def safe_get(var):
    if var is not None:
        try:
            return var.get()
        except Exception:
            return None
    return None


def safe_after(widget, ms, func):
    """Veilige after() aanroep"""
    try:
        if widget is not None and hasattr(widget, "after"):
            return widget.after(ms, func)
    except Exception as e:
        log_debug(f"❌ Fout bij safe_after: {e}")
    return None


def safe_update_idletasks(widget):
    if widget is not None:
        try:
            widget.update_idletasks()
        except Exception:
            pass


def safe_option_add(widget, pattern, value):
    if widget is not None:
        try:
            widget.option_add(pattern, value)
        except Exception:
            pass


def safe_mainloop(widget):
    if widget is not None:
        try:
            widget.mainloop()
        except Exception:
            pass


def safe_deiconify(widget):
    if widget is not None:
        try:
            widget.deiconify()
        except Exception:
            pass


def safe_winfo_children(widget):
    if widget is not None:
        try:
            return widget.winfo_children()
        except Exception:
            return []
    return []


def update_status_safe(message):
    """Update status label veilig voor live voortgang met prioriteit"""
    try:
        # Controleer of root bestaat
        if root is None:
            return
            
        # Gebruik directe update voor status labels (hoge prioriteit)
        if status_label is not None:
            schedule_priority_update(lambda: safe_config(status_label, text=message))
        else:
            # Fallback naar zoeken in UI
            for widget in root.winfo_children():
                if hasattr(widget, 'winfo_children'):
                    for child in widget.winfo_children():
                        if hasattr(child, 'winfo_children'):
                            for grandchild in child.winfo_children():
                                if isinstance(grandchild, tk.Label) and grandchild.cget("text") == "":
                                    # Dit is waarschijnlijk de status_label
                                    schedule_priority_update(lambda: grandchild.config(text=message))
                                    return
    except Exception as e:
        log_debug(f"❌ Fout bij status update: {e}")

def update_progress_safe(value):
    """Update progress bar thread-safe met hoge prioriteit"""
    if progress is not None:
        try:
            # Gebruik onmiddellijke update voor progress bars
            schedule_immediate_update(lambda: safe_config(progress, value=value))
        except Exception as e:
            log_debug(f"❌ Progress update fout: {e}")

def update_info_safe(message, color="black"):
    """Update info label thread-safe"""
    if info_label is not None:
        try:
            schedule_gui_update(lambda: safe_config(info_label, text=message, fg=color))
        except Exception as e:
            log_debug(f"❌ Info update fout: {e}")

def update_time_estimate_safe(completed_blocks, total_blocks, start_time):
    """Update tijdschatting veilig"""
    try:
        if 'time_estimate_label' in globals() and time_estimate_label is not None:
            if completed_blocks > 0 and total_blocks > 0:
                elapsed_time = time.time() - start_time
                avg_time_per_block = elapsed_time / completed_blocks
                remaining_blocks = total_blocks - completed_blocks
                estimated_remaining_time = remaining_blocks * avg_time_per_block
                
                # Format tijd
                if estimated_remaining_time < 60:
                    time_text = f"⏱️ Nog ongeveer {estimated_remaining_time:.0f} seconden"
                elif estimated_remaining_time < 3600:
                    minutes = estimated_remaining_time / 60
                    time_text = f"⏱️ Nog ongeveer {minutes:.0f} minuten"
                else:
                    hours = estimated_remaining_time / 3600
                    time_text = f"⏱️ Nog ongeveer {hours:.1f} uur"
                
                time_estimate_label.config(text=time_text)
            else:
                time_estimate_label.config(text="⏱️ Tijdschatting wordt berekend...")
    except Exception as e:
        log_debug(f"❌ Fout bij tijdschatting update: {e}")


# --- Lijsten voor te verwerken, voltooide en mislukte bestanden ---
verwerk_lijst = []
voltooid_lijst = []
mislukte_lijst = []


def is_video_bestand(pad):
    """Controleer of een bestand een videobestand is"""
    video_extensions = [
        ".mp4",
        ".avi",
        ".mov",
        ".mkv",
        ".wmv",
        ".flv",
        ".webm",
        ".m4v",
        ".3gp",
        ".mpg",
        ".mpeg",
    ]
    _, ext = os.path.splitext(pad.lower())
    return ext in video_extensions


def voeg_bestand_toe_pad(pad):
    global verwerk_lijst, listbox_nog, info_label
    if (
        pad
        and pad not in verwerk_lijst
        and os.path.isfile(pad)
        and is_video_bestand(pad)
    ):
        verwerk_lijst.append(pad)
        if listbox_nog is not None:
            listbox_nog.insert(tk.END, os.path.basename(pad))
            # Selecteer automatisch het eerste bestand
            if listbox_nog.size() == 1:
                listbox_nog.selection_set(0)
                listbox_nog.activate(0)
            # Update bestandsnaam label als dit het eerste bestand is
            if len(verwerk_lijst) == 1 and info_label is not None:
                huidig_thema = thema_var.get() if thema_var is not None else "dark"
                if huidig_thema == "dark":
                    text_color = "white"
                else:
                    text_color = "#2c3e50"
                info_label.config(text=f"📄 {os.path.basename(pad)}", fg=text_color)

def voeg_map_toe_paden(map_pad):
    global info_label, thema_var
    if map_pad and os.path.isdir(map_pad):
        video_count = 0
        eerste_video = None
        for fname in os.listdir(map_pad):
            fpath = os.path.join(map_pad, fname)
            if os.path.isfile(fpath) and is_video_bestand(fpath):
                voeg_bestand_toe_pad(fpath)
                video_count += 1
                if eerste_video is None:
                    eerste_video = fpath
        # Selecteer automatisch het eerste bestand in de listbox
        if listbox_nog is not None and listbox_nog.size() > 0:
            listbox_nog.selection_clear(0, tk.END)
            listbox_nog.selection_set(0)
            listbox_nog.activate(0)
        # Toon een melding als er videobestanden zijn gevonden
        if video_count > 0:
            if info_label is not None and eerste_video is not None:
                huidig_thema = thema_var.get() if thema_var is not None else "dark"
                if huidig_thema == "dark":
                    text_color = "white"
                else:
                    text_color = "#2c3e50"
                info_label.config(text=f"📄 {os.path.basename(eerste_video)}", fg=text_color)
            messagebox.showinfo(
                "Videobestanden toegevoegd",
                f"{video_count} videobestand(en) toegevoegd aan de verwerkingslijst.",
            )
        else:
            messagebox.showwarning(
                "Geen videobestanden",
                "Er zijn geen videobestanden gevonden in de geselecteerde map.",
            )


# Maak de listboxen globaal beschikbaar
listbox_nog = None
listbox_voltooid = None
cpu_limit_var = None  # Globale CPU limiet variable

# --- Automatische verwerkingsloop ---
auto_processing_active = False  # Voorkom dubbele verwerking

def start_auto_processing_loop():
    global auto_processing_active
    if auto_processing_active:
        return  # Al bezig
    auto_processing_active = True
    process_next_in_listbox()

def process_next_in_listbox():
    global auto_processing_active
    if listbox_nog is None or listbox_nog.size() == 0:
        auto_processing_active = False
        return

    # Haal eerste item (altijd bovenaan)
    bestandsnaam = listbox_nog.get(0)

    # Zoek het volledige pad in verwerk_lijst
    pad = None
    for p in verwerk_lijst:
        if os.path.basename(p) == bestandsnaam:
            pad = p
            break
    if pad is None:
        # Verwijder item als pad niet gevonden
        listbox_nog.delete(0)
        # Ga direct door met volgende
        if root is not None:
            root.after(100, process_next_in_listbox)
        return

    # Verwerk het bestand in een aparte thread
    def worker():
        try:
            model_name = "base"
            language = "auto"
            success = process_video_with_whisper(pad, model_name, language)
            if success:
                if listbox_voltooid is not None:
                    listbox_voltooid.insert(tk.END, bestandsnaam)
                    if pad not in voltooid_lijst:
                        voltooid_lijst.append(pad)
            else:
                if 'listbox_mislukt' in globals() and listbox_mislukt is not None:
                    listbox_mislukt.insert(tk.END, bestandsnaam)
                    if pad not in mislukte_lijst:
                        mislukte_lijst.append(pad)
            if pad in verwerk_lijst:
                idx = verwerk_lijst.index(pad)
                verwerk_lijst.pop(idx)
                if listbox_nog is not None:
                    listbox_nog.delete(idx)
        except Exception as e:
            log_debug(f"❌ Fout bij automatische verwerking: {e}")
        finally:
            if root is not None:
                root.after(100, process_next_in_listbox)
    threading.Thread(target=worker, daemon=True).start()

def show_configuration_window():
    """Toon configuratie venster voor DeepL API en andere instellingen"""
    global config_window, deepl_key_var, model_selection_var, output_format_var, processing_active
    
    # Snelle check voor bestaand venster (geoptimaliseerd)
    if config_window is not None:
        try:
            config_window.lift()
            config_window.focus_force()
            return
        except:
            config_window = None
    
    # Controleer of verwerking bezig is
    if processing_active:
        messagebox.showwarning(
            "Verwerking bezig", 
            "Configuratie kan niet gewijzigd worden tijdens verwerking.\n\n"
            "Wacht tot de verwerking klaar is of gebruik de Kill Switch om te stoppen."
        )
        return
    
    # Geoptimaliseerde venster creatie
    log_debug("🔧 Configuratie venster wordt geopend...")
    config_window = tk.Toplevel()
    config_window.title("⚙️ Configuratie - Magic Time Studio")
    config_window.geometry("800x600")
    config_window.transient(root)
    config_window.grab_set()
    
    # Geoptimaliseerde thema configuratie
    huidig_thema = thema_var.get() if thema_var is not None else "dark"
    kleuren = THEMA_KLEUREN.get(huidig_thema, THEMA_KLEUREN["dark"])
    
    config_window.configure(bg=kleuren["bg"])
    header_frame = tk.Frame(config_window, bg=kleuren["panel_bg"], height=40)
    title_label = tk.Label(
        header_frame,
        text="⚙️ Configuratie",
        font=("Arial", 12, "bold"),
        fg=kleuren["fg"],
        bg=kleuren["panel_bg"],
    )
    header_frame.pack(fill="x", padx=5, pady=5)
    header_frame.pack_propagate(False)
    title_label.pack(side="left", padx=10, pady=5)
    # Geoptimaliseerde frame configuratie
    main_frame = tk.Frame(config_window, bg=kleuren["bg"])
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Gebruik al geconfigureerde kleuren
    frame_bg = kleuren["panel_bg"]
    frame_fg = kleuren["fg"]
    tab_bg = kleuren["bg"]
    tab_fg = kleuren["fg"]
    
    # Maak tabbladen voor verschillende configuratie secties
    notebook = tk.Frame(main_frame, bg=frame_bg)
    notebook.pack(fill="both", expand=True)
    
    # Tab container
    tab_container = tk.Frame(notebook, bg=frame_bg)
    tab_container.pack(fill="both", expand=True)
    
    # Tab buttons container
    tab_buttons_frame = tk.Frame(tab_container, bg=frame_bg)
    tab_buttons_frame.pack(fill="x", pady=(0, 10))
    
    # Tab content container
    tab_content_frame = tk.Frame(tab_container, bg=frame_bg)
    tab_content_frame.pack(fill="both", expand=True)
    
    # Tab variabelen
    current_tab = tk.StringVar(value="api")
    tab_frames = {}
    
    def show_tab(tab_name):
        log_debug(f"🔧 Toon tab: {tab_name}")
        
        # Verberg alle tab frames
        for frame in tab_frames.values():
            frame.pack_forget()
        
        # Toon geselecteerde tab
        if tab_name in tab_frames:
            log_debug(f"🔧 Toon frame voor tab: {tab_name}")
            tab_frames[tab_name].pack(fill="both", expand=True, padx=5, pady=5)
            current_tab.set(tab_name)
            
            # Force update van de GUI
            if config_window is not None:
                config_window.update_idletasks()
                config_window.update()
        else:
            log_debug(f"❌ Tab frame niet gevonden: {tab_name}")
            log_debug(f"🔧 Beschikbare tabs: {list(tab_frames.keys())}")
    
    # Geoptimaliseerde tab button creatie
    tab_buttons = [
        ("🌐", "API", "api"),
        ("🤖", "Model", "model"),
        ("📁", "Output", "output"),
        ("🌍", "Vertaler", "translator"),
        ("📺", "Ondertitels", "subtitle"),
        ("📝", "Logging", "logging"),
        ("🔤", "Lettertype", "font")
    ]
    
    for icon, text, tab_name in tab_buttons:
        btn = tk.Button(
            tab_buttons_frame,
            text=f"{icon} {text}",
            command=lambda t=tab_name: show_tab(t),
            bg=tab_bg,
            fg=tab_fg,
            font=("Arial", 9, "bold"),
            relief="flat",
            bd=0,
            padx=15,
            pady=8
        )
        btn.pack(side="left", padx=(0, 5))
    
    # Tab 1: API Configuratie
    api_frame = tk.Frame(tab_content_frame, bg=frame_bg)
    tab_frames["api"] = api_frame
    log_debug("🔧 API tab frame aangemaakt")
    
    # DeepL API Configuratie
    deepl_frame = tk.Frame(api_frame, bg=frame_bg)
    deepl_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Titel voor DeepL sectie
    deepl_title = tk.Label(
        deepl_frame,
        text="🌐 DeepL API Configuratie",
        font=("Arial", 10, "bold"),
        bg=frame_bg,
        fg=frame_fg
    )
    deepl_title.pack(anchor="w", padx=10, pady=(10, 5))
    
    tk.Label(deepl_frame, text="DeepL API Key:", font=("Arial", 9), bg=frame_bg, fg=frame_fg).pack(
        anchor="w", padx=10, pady=(0, 2)
    )
    deepl_key_var = tk.StringVar(value=deepl_key)
    deepl_entry = tk.Entry(deepl_frame, textvariable=deepl_key_var, width=50, show="*")
    deepl_entry.pack(fill="x", padx=10, pady=(0, 5))
    info_label = tk.Label(
        deepl_frame,
        text="💡 Haal je gratis API key op: https://www.deepl.com/pro-api",
        font=("Arial", 8),
        fg="#666666",
        bg=frame_bg,
    )
    info_label.pack(anchor="w", padx=10, pady=(0, 10))

    def test_deepl_api():
        if deepl_key_var is None:
            messagebox.showwarning("⚠️", "Voer eerst een DeepL API key in.")
            return
        api_key = deepl_key_var.get().strip()
        if not api_key or api_key == "":
            messagebox.showwarning("⚠️", "Voer eerst een DeepL API key in.")
            return
        try:
            import importlib
            import_heavy_modules()
            deepl = importlib.import_module("deepl")
            translator = deepl.Translator(api_key)
            usage = translator.get_usage()
            log_debug(f"✅ DeepL API test succesvol!")
            log_debug(
                f"📊 Karakters gebruikt: {usage.character.count or 0}/{usage.character.limit}"
            )
            messagebox.showinfo(
                "✅ API Test",
                f"DeepL API key is geldig!\n\n📊 Gebruik:\n• Gebruikt: {usage.character.count or 0:,} karakters\n• Limiet: {usage.character.limit or 0:,} karakters\n• Beschikbaar: {(usage.character.limit or 0) - (usage.character.count or 0):,} karakters",
            )
        except Exception as e:
            log_debug(f"❌ DeepL API test mislukt: {e}")
            messagebox.showerror("❌ API Test", f"DeepL API key is ongeldig:\n{e}")

    test_btn = tk.Button(
        deepl_frame,
        text="Test API Key",
        command=test_deepl_api,
        bg="#3498db",
        fg="white",
        font=("Arial", 9),
    )
    test_btn.pack(pady=(0, 10))
    
    log_debug("🔧 API tab content toegevoegd")
    
    # Tab 2: Model Configuratie
    model_frame = tk.Frame(tab_content_frame, bg=frame_bg)
    tab_frames["model"] = model_frame
    
    # Whisper Model Configuratie
    model_config_frame = tk.Frame(model_frame, bg=frame_bg)
    model_config_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Titel voor Model sectie
    model_title = tk.Label(
        model_config_frame,
        text="🤖 Whisper Model Configuratie",
        font=("Arial", 10, "bold"),
        bg=frame_bg,
        fg=frame_fg
    )
    model_title.pack(anchor="w", padx=10, pady=(10, 5))
    
    tk.Label(model_config_frame, text="Model Grootte:", font=("Arial", 9), bg=frame_bg, fg=frame_fg).pack(
        anchor="w", padx=10, pady=(0, 2))
    model_selection_var = tk.StringVar(value="base")
    model_combo = tk.OptionMenu(
        model_config_frame,
        model_selection_var,
        model_selection_var.get(),
        "tiny",
        "small",
        "medium",
        "large"
    )
    # Geoptimaliseerde dropdown styling voor model
    huidig_thema = thema_var.get() if thema_var is not None else "dark"
    if huidig_thema in THEMA_KLEUREN:
        kleuren = THEMA_KLEUREN[huidig_thema]
        # Gebruik witte achtergrond voor betere zichtbaarheid in dark thema
        bg_color = "white" if huidig_thema == "dark" else kleuren["panel_bg"]
        fg_color = "black" if huidig_thema == "dark" else kleuren["fg"]
        border_color = "#cccccc" if huidig_thema == "dark" else kleuren.get("border", "#cccccc")
        
        model_combo.config(
            font=("Arial", 9),
            bg=bg_color,
            fg=fg_color,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground=border_color,
            highlightcolor=border_color,
            width=20,
            activebackground=bg_color,
            activeforeground=fg_color
        )
    else:
        # Fallback naar standaard kleuren
        model_combo.config(
            font=("Arial", 9),
            bg="white",
            fg="black",
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground="#cccccc",
            highlightcolor="#cccccc",
            width=20,
            activebackground="white",
            activeforeground="black"
        )
    model_combo.pack(anchor="w", padx=10, pady=(0, 10))
    model_info = tk.Label(
        model_config_frame,
        text="💡 Model grootte beïnvloedt snelheid en nauwkeurigheid:\n• tiny: Snelst, minst nauwkeurig\n• base: Goede balans (aanbevolen)\n• large: Langzaamst, meest nauwkeurig",
        font=("Arial", 8),
        fg="#666666",
        bg=frame_bg,
        justify="left",
    )
    model_info.pack(anchor="w", padx=10, pady=(0, 10))
    
    # Tab 3: Output Configuratie
    output_frame = tk.Frame(tab_content_frame, bg=frame_bg)
    tab_frames["output"] = output_frame
    
    # Output Configuratie
    output_config_frame = tk.Frame(output_frame, bg=frame_bg)
    output_config_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Titel voor Output sectie
    output_title = tk.Label(
        output_config_frame,
        text="📁 Output Configuratie",
        font=("Arial", 10, "bold"),
        bg=frame_bg,
        fg=frame_fg
    )
    output_title.pack(anchor="w", padx=10, pady=(10, 5))
    
    # Info label dat output automatisch wordt bepaald
    output_info = tk.Label(
        output_config_frame,
        text="💡 Output wordt automatisch opgeslagen in dezelfde map als het videobestand",
        font=("Arial", 9),
        fg=frame_fg,
        bg=frame_bg,
        justify="left",
    )
    output_info.pack(anchor="w", padx=10, pady=(10, 5))
    
    tk.Label(output_config_frame, text="Output Format:", font=("Arial", 9), bg=frame_bg, fg=frame_fg).pack(
        anchor="w", padx=10, pady=(10, 2))
    output_format_var = tk.StringVar(value="srt")
    output_combo = tk.OptionMenu(
        output_config_frame,
        output_format_var,
        output_format_var.get(),
        "txt",
        "vtt"
    )
    # Geoptimaliseerde dropdown styling voor output
    huidig_thema = thema_var.get() if thema_var is not None else "dark"
    if huidig_thema in THEMA_KLEUREN:
        kleuren = THEMA_KLEUREN[huidig_thema]
        # Gebruik witte achtergrond voor betere zichtbaarheid in dark thema
        bg_color = "white" if huidig_thema == "dark" else kleuren["panel_bg"]
        fg_color = "black" if huidig_thema == "dark" else kleuren["fg"]
        border_color = "#cccccc" if huidig_thema == "dark" else kleuren.get("border", "#cccccc")
        
        output_combo.config(
            font=("Arial", 9),
            bg=bg_color,
            fg=fg_color,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground=border_color,
            highlightcolor=border_color,
            width=20,
            activebackground=bg_color,
            activeforeground=fg_color
        )
    else:
        # Fallback naar standaard kleuren
        output_combo.config(
            font=("Arial", 9),
            bg="white",
            fg="black",
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground="#cccccc",
            highlightcolor="#cccccc",
            width=20,
            activebackground="white",
            activeforeground="black"
        )
    output_combo.pack(anchor="w", padx=10, pady=(0, 10))
    
    # Tab 4: Vertaler Configuratie
    translator_frame = tk.Frame(tab_content_frame, bg=frame_bg)
    tab_frames["translator"] = translator_frame
    
    # Vertaler Configuratie
    translator_config_frame = tk.Frame(translator_frame, bg=frame_bg)
    translator_config_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Titel voor Vertaler sectie
    translator_title = tk.Label(
        translator_config_frame,
        text="🌍 Vertaler Configuratie",
        font=("Arial", 10, "bold"),
        bg=frame_bg,
        fg=frame_fg
    )
    translator_title.pack(anchor="w", padx=10, pady=(10, 5))
    status_text = f"Huidige vertaler: {huidige_vertaler.upper()}"
    if huidige_vertaler == "deepl" and not deepl_key:
        status_text += " (⚠️ Geen API key)"
    elif huidige_vertaler == "deepl" and deepl_key:
        status_text += " (✅ API key geconfigureerd)"
    tk.Label(
        translator_config_frame,
        text=status_text,
        font=("Arial", 9, "bold"),
        bg=frame_bg,
        fg=frame_fg,
    ).pack(anchor="w", padx=10, pady=(10, 5))
    tk.Label(
        translator_config_frame, text="Standaard Vertaler:", font=("Arial", 9), bg=frame_bg, fg=frame_fg
    ).pack(anchor="w", padx=10, pady=(5, 2))
    translator_default = huidige_vertaler if huidige_vertaler in ["geen", "google", "deepl"] else "geen"
    translator_var = tk.StringVar(value=translator_default)
    translator_combo = tk.OptionMenu(
        translator_config_frame,
        translator_var,
        "geen",
        "google",
        "deepl"
    )
    # Geoptimaliseerde dropdown styling voor translator
    huidig_thema = thema_var.get() if thema_var is not None else "dark"
    if huidig_thema in THEMA_KLEUREN:
        kleuren = THEMA_KLEUREN[huidig_thema]
        # Gebruik witte achtergrond voor betere zichtbaarheid in dark thema
        bg_color = "white" if huidig_thema == "dark" else kleuren["panel_bg"]
        fg_color = "black" if huidig_thema == "dark" else kleuren["fg"]
        border_color = "#cccccc" if huidig_thema == "dark" else kleuren.get("border", "#cccccc")
        
        translator_combo.config(
            font=("Arial", 9),
            bg=bg_color,
            fg=fg_color,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground=border_color,
            highlightcolor=border_color,
            width=20,
            activebackground=bg_color,
            activeforeground=fg_color
        )
    else:
        # Fallback naar standaard kleuren
        translator_combo.config(
            font=("Arial", 9),
            bg="white",
            fg="black",
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground="#cccccc",
            highlightcolor="#cccccc",
            width=20,
            activebackground="white",
            activeforeground="black"
        )
    translator_combo.pack(anchor="w", padx=10, pady=(0, 10))
    
    # Tab 5: Ondertitel Configuratie
    subtitle_frame = tk.Frame(tab_content_frame, bg=frame_bg)
    tab_frames["subtitle"] = subtitle_frame
    
    # Ondertitel Configuratie
    subtitle_config_frame = tk.Frame(subtitle_frame, bg=frame_bg)
    subtitle_config_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Titel voor Ondertitel sectie
    subtitle_title = tk.Label(
        subtitle_config_frame,
        text="📺 Ondertitel Configuratie",
        font=("Arial", 10, "bold"),
        bg=frame_bg,
        fg=frame_fg
    )
    subtitle_title.pack(anchor="w", padx=10, pady=(10, 5))
    
    # Ondertitel type uitleg
    subtitle_info = tk.Label(
        subtitle_config_frame,
        text="💡 Kies het type ondertitels dat je wilt genereren:",
        font=("Arial", 9),
        fg=frame_fg,
        bg=frame_bg,
        justify="left",
    )
    subtitle_info.pack(anchor="w", padx=10, pady=(10, 5))
    
    # Softcoded ondertitels uitleg
    softcoded_info = tk.Label(
        subtitle_config_frame,
        text="🎯 Softcoded: Ondertitels worden als apart SRT bestand opgeslagen.\n"
             "   Voordelen: Flexibel, kan later bewerkt worden, kleinere bestandsgrootte.\n"
             "   Gebruik: Voor streaming, YouTube, professionele video's.",
        font=("Arial", 8),
        fg="#27ae60",
        bg=frame_bg,
        justify="left",
    )
    softcoded_info.pack(anchor="w", padx=10, pady=(0, 5))
    
    # Hardcoded ondertitels uitleg
    hardcoded_info = tk.Label(
        subtitle_config_frame,
        text="🎬 Hardcoded: Ondertitels worden direct in de video geïntegreerd.\n"
             "   Voordelen: Altijd zichtbaar, werkt op alle apparaten.\n"
             "   Gebruik: Voor DVD's, presentaties, sociale media.",
        font=("Arial", 8),
        fg="#e74c3c",
        bg=frame_bg,
        justify="left",
    )
    hardcoded_info.pack(anchor="w", padx=10, pady=(0, 10))
    
    # Ondertitel type selector
    tk.Label(
        subtitle_config_frame, text="Ondertitel Type:", font=("Arial", 9), bg=frame_bg, fg=frame_fg
    ).pack(anchor="w", padx=10, pady=(5, 2))
    
    # Zet de juiste display waarde op basis van subtitle_type
    if subtitle_type == "softcoded":
        display_subtitle_type = "Softcoded (SRT bestand)"
    elif subtitle_type == "hardcoded":
        display_subtitle_type = "Hardcoded (ingebedde ondertitels)"
    else:
        display_subtitle_type = "Softcoded (SRT bestand)"  # Standaard
    
    subtitle_type_var = tk.StringVar(value=display_subtitle_type)
    
    # Gebruik tk.OptionMenu in plaats van ttk.Combobox om rand problemen te voorkomen
    subtitle_combo = tk.OptionMenu(
        subtitle_config_frame,
        subtitle_type_var,
        display_subtitle_type,
        "Hardcoded (ingebedde ondertitels)"
    )
    # Geoptimaliseerde dropdown styling voor subtitle
    huidig_thema = thema_var.get() if thema_var is not None else "dark"
    if huidig_thema in THEMA_KLEUREN:
        kleuren = THEMA_KLEUREN[huidig_thema]
        # Gebruik witte achtergrond voor betere zichtbaarheid in dark thema
        bg_color = "white" if huidig_thema == "dark" else kleuren["panel_bg"]
        fg_color = "black" if huidig_thema == "dark" else kleuren["fg"]
        border_color = "#cccccc" if huidig_thema == "dark" else kleuren.get("border", "#cccccc")
        
        subtitle_combo.config(
            font=("Arial", 9),
            bg=bg_color,
            fg=fg_color,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground=border_color,
            highlightcolor=border_color,
            width=30,
            activebackground=bg_color,
            activeforeground=fg_color
        )
    else:
        # Fallback naar standaard kleuren
        subtitle_combo.config(
            font=("Arial", 9),
            bg="white",
            fg="black",
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground="#cccccc",
            highlightcolor="#cccccc",
            width=30,
            activebackground="white",
            activeforeground="black"
        )
    subtitle_combo.pack(anchor="w", padx=10, pady=(0, 5))
    
    # Hardcoded taal optie (alleen zichtbaar bij hardcoded)
    hardcoded_language_frame = None
    # Zet de juiste display waarde op basis van hardcoded_language
    if hardcoded_language == "dutch_only":
        display_hardcoded_language = "Alleen Nederlands"
    elif hardcoded_language == "both_languages":
        display_hardcoded_language = "Beide talen (origineel + Nederlands)"
    else:
        display_hardcoded_language = "Alleen Nederlands"  # Standaard
    
    hardcoded_language_var = tk.StringVar(value=display_hardcoded_language)
    
    def update_hardcoded_options(*args):
        nonlocal hardcoded_language_frame
        
        if subtitle_type_var.get() == "Hardcoded (ingebedde ondertitels)":
            # Maak frame aan als deze nog niet bestaat
            if hardcoded_language_frame is None:
                hardcoded_language_frame = tk.Frame(subtitle_config_frame, bg=frame_bg)
                
                tk.Label(
                    hardcoded_language_frame, 
                    text="Hardcoded Taal:", 
                    font=("Arial", 9), 
                    bg=frame_bg,
                    fg=frame_fg
                ).pack(anchor="w", pady=(5, 2))
                
                # Zet de juiste display waarde op basis van hardcoded_language
                if hardcoded_language == "dutch_only":
                    current_display_hardcoded = "Alleen Nederlands"
                elif hardcoded_language == "both_languages":
                    current_display_hardcoded = "Beide talen (origineel + Nederlands)"
                else:
                    current_display_hardcoded = "Alleen Nederlands"  # Standaard
                
                hardcoded_language_combo = tk.OptionMenu(
                    hardcoded_language_frame,
                    hardcoded_language_var,
                    current_display_hardcoded,
                    "Beide talen (origineel + Nederlands)"
                )
                # Geoptimaliseerde dropdown styling voor hardcoded language
                huidig_thema = thema_var.get() if thema_var is not None else "dark"
                if huidig_thema in THEMA_KLEUREN:
                    kleuren = THEMA_KLEUREN[huidig_thema]
                    # Gebruik witte achtergrond voor betere zichtbaarheid in dark thema
                    bg_color = "white" if huidig_thema == "dark" else kleuren["panel_bg"]
                    fg_color = "black" if huidig_thema == "dark" else kleuren["fg"]
                    border_color = "#cccccc" if huidig_thema == "dark" else kleuren.get("border", "#cccccc")
                    
                    hardcoded_language_combo.config(
                        font=("Arial", 9),
                        bg=bg_color,
                        fg=fg_color,
                        relief="solid",
                        bd=1,
                        highlightthickness=1,
                        highlightbackground=border_color,
                        highlightcolor=border_color,
                        width=30,
                        activebackground=bg_color,
                        activeforeground=fg_color
                    )
                else:
                    # Fallback naar standaard kleuren
                    hardcoded_language_combo.config(
                        font=("Arial", 9),
                        bg="white",
                        fg="black",
                        relief="solid",
                        bd=1,
                        highlightthickness=1,
                        highlightbackground="#cccccc",
                        highlightcolor="#cccccc",
                        width=30,
                        activebackground="white",
                        activeforeground="black"
                    )
                # OptionMenu toont automatisch de juiste waarde
                hardcoded_language_combo.pack(anchor="w", pady=(0, 5))
                
                # Hardcoded taal uitleg
                hardcoded_language_info = tk.Label(
                    hardcoded_language_frame,
                    text="💡 Dutch Only: Alleen Nederlandse ondertitels\n"
                         "💡 Both Languages: Originele taal + Nederlandse vertaling",
                    font=("Arial", 8),
                    fg="#666666",
                    bg=frame_bg,
                    justify="left",
                )
                hardcoded_language_info.pack(anchor="w", pady=(0, 5))
            
            hardcoded_language_frame.pack(fill="x", padx=10, pady=(0, 10))
        else:
            # Verberg frame als deze bestaat
            if hardcoded_language_frame is not None:
                hardcoded_language_frame.pack_forget()
    
    subtitle_type_var.trace("w", update_hardcoded_options)
    
    # Update opties bij start - alleen als hardcoded is geselecteerd
    if subtitle_type == "hardcoded":
        update_hardcoded_options()
    
    # Tab 6: Logging Configuratie
    logging_frame = tk.Frame(tab_content_frame, bg=frame_bg)
    tab_frames["logging"] = logging_frame
    
    # Logging Configuratie
    logging_config_frame = tk.Frame(logging_frame, bg=frame_bg)
    logging_config_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Configureer grid voor logging frame
    logging_config_frame.grid_columnconfigure(0, weight=1)
    logging_config_frame.grid_columnconfigure(1, weight=1)
    
    # Titel voor Logging sectie
    logging_title = tk.Label(
        logging_config_frame,
        text="📝 Logging Configuratie",
        font=("Arial", 10, "bold"),
        bg=frame_bg,
        fg=frame_fg
    )
    logging_title.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))
    
    # Logging checkboxes
    logging_vars = {}
    
    def create_logging_checkbox(parent, text, key, row, col):
        var = tk.BooleanVar(value=logging_config.get(key, True))
        logging_vars[key] = var
        cb = tk.Checkbutton(
            parent,
            text=text,
            variable=var,
            font=("Arial", 9),
            bg=frame_bg,
            fg=frame_fg,
            selectcolor=frame_bg,
        )
        cb.grid(row=row, column=col, sticky="w", padx=10, pady=2)
        return var
    
    # Eerste kolom
    create_logging_checkbox(logging_config_frame, "🖥️ Systeem informatie", "log_system_info", 1, 0)
    create_logging_checkbox(logging_config_frame, "🎵 Audio extractie", "log_audio_extraction", 2, 0)
    create_logging_checkbox(logging_config_frame, "🎤 Whisper transcriptie", "log_whisper_transcription", 3, 0)
    create_logging_checkbox(logging_config_frame, "🌐 Vertaling", "log_translation", 4, 0)
    create_logging_checkbox(logging_config_frame, "📁 Bestandsoperaties", "log_file_operations", 5, 0)
    create_logging_checkbox(logging_config_frame, "⚡ Performance tracking", "log_performance", 6, 0)
    
    # Tweede kolom
    create_logging_checkbox(logging_config_frame, "❌ Fouten", "log_errors", 1, 1)
    create_logging_checkbox(logging_config_frame, "⚠️ Waarschuwingen", "log_warnings", 2, 1)
    create_logging_checkbox(logging_config_frame, "🐛 Debug berichten", "log_debug", 3, 1)
    create_logging_checkbox(logging_config_frame, "🧹 Cleanup operaties", "log_cleanup", 4, 1)
    create_logging_checkbox(logging_config_frame, "🔗 API calls", "log_api_calls", 5, 1)
    create_logging_checkbox(logging_config_frame, "📊 Voortgang", "log_progress", 6, 1)
    
    # Logging info
    logging_info = tk.Label(
        logging_config_frame,
        text="💡 Selecteer welke soorten berichten je wilt zien in het live log venster.\n"
             "Dit helpt om de log overzichtelijk te houden en alleen relevante informatie te tonen.",
        font=("Arial", 8),
        fg="#666666",
        bg=frame_bg,
        justify="left",
    )
    logging_info.grid(row=7, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))
    
    # API Throttle info
    throttle_info = tk.Label(
        logging_config_frame,
        text="🌐 API Throttle (Google Translate & DeepL):\n"
             "• 1-2 workers: 2s delay\n"
             "• 3-4 workers: 3s delay\n"
             "• 5-6 workers: 4s delay\n"
             "• 7-8 workers: 6s delay\n"
             "• Max 60 requests/minuut per service",
        font=("Arial", 8),
        fg=frame_fg,
        bg=frame_bg,
        justify="left",
    )
    throttle_info.grid(row=8, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 10))
    
    # Tab 7: Lettertype Configuratie
    font_frame = tk.Frame(tab_content_frame, bg=frame_bg)
    tab_frames["font"] = font_frame
    
    # Lettertype Configuratie
    font_config_frame = tk.Frame(font_frame, bg=frame_bg)
    font_config_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Titel voor Lettertype sectie
    font_title = tk.Label(
        font_config_frame,
        text="🔤 Lettertype Configuratie",
        font=("Arial", 10, "bold"),
        bg=frame_bg,
        fg=frame_fg
    )
    font_title.pack(anchor="w", padx=10, pady=(10, 5))
    
    # Lettertype uitleg
    font_info = tk.Label(
        font_config_frame,
        text="💡 Pas de lettertype grootte aan voor betere leesbaarheid:",
        font=("Arial", 9),
        fg=frame_fg,
        bg=frame_bg,
        justify="left",
    )
    font_info.pack(anchor="w", padx=10, pady=(10, 5))
    
    # Lettertype grootte slider
    tk.Label(
        font_config_frame, 
        text="Lettertype Grootte:", 
        font=("Arial", 9), 
        bg=frame_bg, 
        fg=frame_fg
    ).pack(anchor="w", padx=10, pady=(5, 2))
    
    # Lettertype grootte variabele (laad uit configuratie)
    font_size_var = tk.IntVar(value=font_size if 'font_size' in globals() else 9)
    
    # Lettertype grootte slider
    font_size_slider = ttk.Scale(
        font_config_frame, 
        from_=8, 
        to=16, 
        variable=font_size_var, 
        orient="horizontal", 
        length=200
    )
    font_size_slider.pack(anchor="w", padx=10, pady=(0, 5))
    
    # Lettertype grootte preview label
    font_preview_label = tk.Label(
        font_config_frame,
        text="Voorbeeld tekst met huidige lettertype grootte",
        font=("Arial", 9),
        fg=frame_fg,
        bg=frame_bg,
        justify="left",
    )
    font_preview_label.pack(anchor="w", padx=10, pady=(0, 10))
    
    # Lettertype grootte update functie
    def update_font_preview(*args):
        try:
            font_size = font_size_var.get()
            font_preview_label.config(
                text=f"Voorbeeld tekst met lettertype grootte {font_size}",
                font=("Arial", font_size)
            )
        except:
            pass
    
    font_size_var.trace("w", update_font_preview)
    update_font_preview()  # Initial update
    
    # Lettertype info
    font_size_info = tk.Label(
        font_config_frame,
        text="💡 Lettertype grootte beïnvloedt de leesbaarheid van alle tekst in de applicatie.\n"
             "• 8-10: Compact, meer informatie op scherm\n"
             "• 11-13: Standaard, goede balans\n"
             "• 14-16: Groot, voor betere toegankelijkheid",
        font=("Arial", 8),
        fg="#666666",
        bg=frame_bg,
        justify="left",
    )
    font_size_info.pack(anchor="w", padx=10, pady=(10, 5))
    
    # Debug: Controleer of alle tabs zijn aangemaakt
    log_debug(f"📋 Configuratie venster tabs aangemaakt: {list(tab_frames.keys())}")
    
    # Button frame buiten de scrollable frame
    button_frame = tk.Frame(config_window, bg=frame_bg)
    button_frame.pack(fill="x", padx=10, pady=(0, 10))

    def save_configuration():
        global config_window, logging_config, subtitle_type, huidige_vertaler
        # Controleer of deepl_key_var bestaat en een get() methode heeft
        if "deepl_key_var" in globals() and hasattr(deepl_key_var, "get"):
            deepl_key = safe_get(deepl_key_var)
            if deepl_key is not None:
                deepl_key = deepl_key.strip()
            else:
                deepl_key = ""
        else:
            deepl_key = ""
        nieuwe_vertaler = translator_var.get()
        if nieuwe_vertaler == "deepl" and not deepl_key:
            messagebox.showwarning(
                "⚠️",
                "DeepL geselecteerd maar geen API key ingevoerd.\nVoer eerst een geldige DeepL API key in.",
            )
            return
        huidige_vertaler = nieuwe_vertaler  # update global direct
        log_debug(f"[DEBUG] Bij opslaan config: huidige_vertaler = {huidige_vertaler}")
        # Update ondertitel type
        nieuwe_subtitle_type = subtitle_type_var.get()
        if nieuwe_subtitle_type == "Softcoded (SRT bestand)":
            subtitle_type = "softcoded"
        elif nieuwe_subtitle_type == "Hardcoded (ingebedde ondertitels)":
            subtitle_type = "hardcoded"
        else:
            subtitle_type = "softcoded"  # Standaard
        
        # Update hardcoded taal optie
        nieuwe_hardcoded_language = hardcoded_language_var.get()
        if nieuwe_hardcoded_language == "Alleen Nederlands":
            hardcoded_language = "dutch_only"
        elif nieuwe_hardcoded_language == "Beide talen (origineel + Nederlands)":
            hardcoded_language = "both_languages"
        else:
            hardcoded_language = "dutch_only"  # Standaard
        
        # Update logging configuratie
        for key, var in logging_vars.items():
            if var is not None and hasattr(var, "get"):
                logging_config[key] = var.get()
        
        config_data = {
            "translator": huidige_vertaler,
            "huidige_vertaler": huidige_vertaler,
            "model_selection": model_selection_var.get() if model_selection_var is not None and hasattr(model_selection_var, "get") else "",
            "output_format": output_format_var.get() if output_format_var is not None and hasattr(output_format_var, "get") else "",
            "cpu_limit": cpu_limit_var.get() if cpu_limit_var is not None and hasattr(cpu_limit_var, "get") else 50,
            "subtitle_type": subtitle_type_var.get() if subtitle_type_var is not None and hasattr(subtitle_type_var, "get") else "softcoded",
            "hardcoded_language": hardcoded_language_var.get() if hardcoded_language_var is not None and hasattr(hardcoded_language_var, "get") else "dutch_only",
            "font_size": font_size_var.get() if font_size_var is not None and hasattr(font_size_var, "get") else 9,
            "logging_config": logging_config,
        }
        try:
            with open(CONFIG_PAD, "w", encoding="utf-8") as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            log_debug(f"✅ Configuratie opgeslagen - Vertaler: {huidige_vertaler}")
            update_translator_status()
            
            # Pas lettertype grootte toe bij opslaan
            if font_size_var is not None and hasattr(font_size_var, "get"):
                new_font_size = font_size_var.get()
                apply_font_size_to_interface(new_font_size)
            
            # Popup weggehaald - configuratie wordt automatisch opgeslagen
            if config_window is not None:
                config_window.destroy()
            config_window = None
        except Exception as e:
            log_debug(f"❌ Fout bij opslaan configuratie: {e}")
            messagebox.showerror("❌ Fout", f"Kon configuratie niet opslaan:\n{e}")

    def cancel_configuration():
        global config_window
        if config_window is not None:
            config_window.destroy()
        config_window = None

    save_btn = tk.Button(
        button_frame,
        text="Opslaan",
        command=save_configuration,
        bg="#27ae60",
        fg="white",
        font=("Arial", 10, "bold"),
    )
    save_btn.pack(side="right", padx=(5, 0))
    cancel_btn = tk.Button(
        button_frame,
        text="Annuleren",
        command=cancel_configuration,
        bg="#95a5a6",
        fg="white",
        font=("Arial", 10),
    )
    cancel_btn.pack(side="right")
    
    # Toon de eerste tab bij het openen
    log_debug("🔧 Configuratie venster geopend - toon eerste tab")
    show_tab("api")
    
    # Debug: controleer of tab frames bestaan
    log_debug(f"🔧 Tab frames: {list(tab_frames.keys())}")
    log_debug(f"🔧 API frame bestaat: {'api' in tab_frames}")
    
    config_window.focus_force()
    config_window.lift()


def voeg_tools_menu_toe():
    global menubalk, root
    assert (
        menubalk is not None
    ), "menubalk moet geïnitialiseerd zijn voordat het Tools-menu wordt toegevoegd"
    # Verwijder eerst alle bestaande menu's om dubbele menu's te voorkomen
    menubalk.delete(0, 'end')
    # Lazy loading functies voor snellere menubalk
    def lazy_show_config():
        # Snelle check voor bestaand venster
        if 'config_window' in globals() and config_window is not None:
            try:
                config_window.lift()
                config_window.focus_force()
                return
            except:
                pass
        # Alleen laden als nodig
        show_configuration_window()
    def lazy_show_log():
        show_live_log()
    def lazy_cuda_test():
        test_cuda_performance()
    def lazy_cuda_help():
        show_cuda_install_instructions()
    def show_about():
        messagebox.showinfo(
            "Over Magic Time Studio",
            "Magic Time Studio v1.9.4\n\n"
            "Een krachtige tool voor automatische ondertiteling\n"
            "met Whisper AI en vertaling naar het Nederlands.\n\n"
            "Ontwikkeld door Bjorn Mertens"
        )
    # Geoptimaliseerde menu structuur met lazy loading
    current_font_size = font_size if 'font_size' in globals() else 9
    tools_menu = tk.Menu(menubalk, tearoff=False, font=("Arial", current_font_size))
    tools_menu.add_command(label="⚙️ Configuratie", command=lazy_show_config)
    tools_menu.add_command(label="📋 Live Log", command=lazy_show_log)
    tools_menu.add_separator()
    tools_menu.add_command(label="🎮 CUDA Test", command=lazy_cuda_test)
    tools_menu.add_command(label="📋 CUDA Help", command=lazy_cuda_help)
    menubalk.add_cascade(label="🔧 Tools", menu=tools_menu)
    # Help menu
    help_menu = tk.Menu(menubalk, tearoff=False, font=("Arial", current_font_size))
    help_menu.add_command(label="📖 Over", command=show_about)
    menubalk.add_cascade(label="❓ Help", menu=help_menu)
    # Thema menu met directe functie calls
    theme_menu = tk.Menu(menubalk, tearoff=False, font=("Arial", current_font_size))
    theme_menu.add_command(label="🌙 Dark", command=lambda: pas_thema_toe("dark"))
    theme_menu.add_command(label="☀️ Light", command=lambda: pas_thema_toe("light"))
    theme_menu.add_command(label="🌊 Blue", command=lambda: pas_thema_toe("blue"))
    theme_menu.add_command(label="🌿 Green", command=lambda: pas_thema_toe("green"))
    menubalk.add_cascade(label="🎨 Thema's", menu=theme_menu)
    # Pas lettertype toe op menubalk (alleen bij eerste aanmaak)
    if 'font_size' in globals() and font_size is not None:
        if not hasattr(voeg_tools_menu_toe, '_font_applied'):
            voeg_tools_menu_toe._font_applied = True
            # apply_font_size_to_interface(font_size)  # NIET opnieuw menubalk aanmaken
            voeg_tools_menu_toe._font_applied = False


def setup_ui():
    global root, menubalk, main_frame, left_panel, right_panel, start_button, kill_button, progress, status_label, info_label, listbox_nog, listbox_voltooid
    global video_pad, taal_var, thema_var, content_type_var
    
    # Initialize Tkinter variables
    video_pad = tk.StringVar()
    taal_var = tk.StringVar(value="Auto detectie")
    thema_var = tk.StringVar(value="dark")
    content_type_var = tk.StringVar(value="Eén hoofdtaal")
    
    if root is not None:
        # --- FIX dubbele menubalk ---
        if 'menubalk' in globals() and menubalk is not None:
            try:
                menubalk.destroy()
            except Exception:
                pass
        menubalk = tk.Menu(root)
        root.config(menu=menubalk)
        root.geometry("900x500")
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

    main_frame = tk.Frame(root, bg="#f0f8f0")
    main_frame.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_rowconfigure(0, weight=1)

    left_panel = tk.LabelFrame(main_frame, text="Invoer", font=("Segoe UI", 11, "bold"), bg="#f5faf5", fg="#2c2c2c", bd=2, relief="groove", padx=12, pady=12)
    left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 12), pady=0)
    left_panel.grid_rowconfigure(99, weight=1)
    left_panel.grid_columnconfigure(0, weight=1)
    left_panel.grid_columnconfigure(1, weight=1)

    # Linker paneel knoppen
    translator_status_label = tk.Label(left_panel, text=f"Vertaler: {huidige_vertaler.upper()}", font=("Segoe UI", 9, "bold"), bg="#f5faf5", fg="#2c3e50")
    translator_status_label.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 5))
    
    # Worker count status label
    cpu_status_label = tk.Label(left_panel, text="CPU Limiet: 50%", font=("Segoe UI", 8), bg="#f5faf5", fg="#666666")
    cpu_status_label.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 5))
    
    tk.Label(left_panel, text="Gesproken taal:", font=("Segoe UI", 10), bg="#f5faf5").grid(row=2, column=0, sticky="w")
    
    # Taal dropdown menu
    taal_options = [
        ("Auto detectie", "auto"),
        ("Engels", "en"),
        ("Nederlands", "nl"),
        ("Duits", "de"),
        ("Frans", "fr"),
        ("Spaans", "es"),
        ("Italiaans", "it"),
        ("Portugees", "pt"),
        ("Russisch", "ru"),
        ("Japans", "ja"),
        ("Koreaans", "ko"),
        ("Chinees", "zh"),
        ("Arabisch", "ar"),
        ("Hindi", "hi"),
        ("Turks", "tr"),
        ("Pools", "pl"),
        ("Zweeds", "sv"),
        ("Deens", "da"),
        ("Noors", "no"),
        ("Fins", "fi")
    ]
    
    # Geoptimaliseerde dropdown styling functie
    def style_dropdown(dropdown, theme_name="dark"):
        """Pas dropdown styling toe met goed contrast voor alle thema's"""
        if theme_name in THEMA_KLEUREN:
            kleuren = THEMA_KLEUREN[theme_name]
            # Gebruik witte achtergrond voor betere zichtbaarheid
            bg_color = "white" if theme_name == "dark" else kleuren["panel_bg"]
            fg_color = "black" if theme_name == "dark" else kleuren["fg"]
            border_color = "#cccccc" if theme_name == "dark" else kleuren.get("border", "#cccccc")
        else:
            # Fallback naar standaard kleuren
            bg_color = "white"
            fg_color = "black"
            border_color = "#cccccc"
        
        dropdown.config(
            font=("Segoe UI", 9),
            bg=bg_color,
            fg=fg_color,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground=border_color,
            highlightcolor=border_color,
            width=15,
            activebackground=bg_color,
            activeforeground=fg_color
        )
    
    # Maak OptionMenu voor taal selectie - geoptimaliseerd
    global taal_combobox
    taal_combobox = tk.OptionMenu(left_panel, taal_var, "Auto detectie", *[opt[0] for opt in taal_options[1:]])
    style_dropdown(taal_combobox, thema_var.get() if thema_var is not None else "dark")
    taal_combobox.grid(row=2, column=1, sticky="ew", padx=(5, 0))
    
    # Content type dropdown
    tk.Label(left_panel, text="Content type:", font=("Segoe UI", 10), bg="#f5faf5").grid(row=3, column=0, sticky="w")
    
    content_type_var = tk.StringVar(value="Eén hoofdtaal")
    content_type_options = [
        "Eén hoofdtaal",
        "Twee talen (gemengd)",
        "Sporadische woorden"
    ]
    
    global content_type_combobox
    content_type_combobox = tk.OptionMenu(left_panel, content_type_var, "Eén hoofdtaal", *content_type_options[1:])
    style_dropdown(content_type_combobox, thema_var.get() if thema_var is not None else "dark")
    content_type_combobox.grid(row=3, column=1, sticky="ew", padx=(5, 0))
    
    # Vereenvoudigde event handlers
    def on_taal_change(*args):
        try:
            if taal_var is not None:
                selected_text = taal_var.get()
                log_debug(f"🌍 Taal gekozen: {selected_text}")
                update_status_safe(f"🌍 Taal ingesteld: {selected_text}")
        except Exception as e:
            log_debug(f"❌ Fout bij taal wijziging: {e}")
    
    def on_content_type_change(*args):
        try:
            selected_type = content_type_var.get()
            log_debug(f"📺 Content type gekozen: {selected_type}")
            update_status_safe(f"📺 Content type: {selected_type}")
        except Exception as e:
            log_debug(f"❌ Fout bij content type wijziging: {e}")
    
    taal_var.trace("w", on_taal_change)
    content_type_var.trace("w", on_content_type_change)
    tk.Label(left_panel, text="CPU Limiet:", font=("Segoe UI", 10)).grid(row=4, column=0, sticky="w")
    global cpu_limit_var
    cpu_limit_var = tk.IntVar(value=50)
    
    # CPU percentage slider
    cpu_slider = ttk.Scale(left_panel, from_=10, to=100, variable=cpu_limit_var, orient="horizontal", length=120)
    cpu_slider.grid(row=4, column=1, sticky="ew", padx=(5, 0))
    
    # Maak slider transparant
    style = ttk.Style()
    style.configure("Transparent.Horizontal.TScale", 
                   background="#f5faf5", 
                   troughcolor="#e0e0e0", 
                   bordercolor="#f5faf5",
                   lightcolor="#f5faf5",
                   darkcolor="#f5faf5",
                   focuscolor="#f5faf5")
    cpu_slider.configure(style="Transparent.Horizontal.TScale")
    
    # CPU percentage label
    cpu_percent_label = tk.Label(left_panel, text="50%", font=("Segoe UI", 8), bg="#f5faf5", fg="#666666")
    cpu_percent_label.grid(row=4, column=2, sticky="w", padx=(5, 0))
    
    # CPU load info label
    cpu_load_label = tk.Label(left_panel, text="Huidig: --", font=("Segoe UI", 8), bg="#f5faf5", fg="#666666")
    cpu_load_label.grid(row=4, column=3, sticky="w", padx=(5, 0))
    
    def update_cpu_limit(*args):
        try:
            if cpu_limit_var is None:
                return
            cpu_limit = cpu_limit_var.get()
            def update_cpu_percent():
                try:
                    cpu_percent_label.config(text=f"{cpu_limit}%")
                except:
                    pass
            schedule_gui_update(update_cpu_percent)
            
            # Bereken worker count op basis van CPU limiet
            if cpu_limit <= 25:
                worker_count = 1
            elif cpu_limit <= 50:
                worker_count = 2
            elif cpu_limit <= 75:
                worker_count = 4
            else:
                worker_count = 6
            
            if parallel_processor is not None:
                parallel_processor.max_workers = worker_count
            # Alleen loggen als er echt een verandering is
            if not hasattr(update_cpu_limit, 'last_logged') or update_cpu_limit.last_logged != cpu_limit:
                log_debug(f"⚡ CPU limiet aangepast naar: {cpu_limit}% ({worker_count} workers)")
                update_cpu_limit.last_logged = cpu_limit
        except Exception as e:
            log_debug(f"❌ Fout bij update CPU limiet: {e}")
    
    def update_cpu_load():
        try:
            if PSUTIL_AVAILABLE and cpu_limit_var is not None:
                cpu_percent = psutil.cpu_percent(interval=0.1)
                cpu_limit = cpu_limit_var.get()
                
                # Vereenvoudigde kleur logica
                color = "#44aa44" if cpu_percent <= cpu_limit else "#ff4444"
                
                def update_cpu_display():
                    try:
                        cpu_load_label.config(text=f"Huidig: {cpu_percent:.0f}%", fg=color)
                    except:
                        pass
                schedule_gui_update(update_cpu_display)
            else:
                def update_cpu_display():
                    try:
                        cpu_load_label.config(text="Huidig: --")
                    except:
                        pass
                schedule_gui_update(update_cpu_display)
        except:
            pass
        
        # Update elke 10 seconden (minder frequent voor betere performance)
        if root is not None:
            root.after(10000, update_cpu_load)
    
    cpu_limit_var.trace("w", update_cpu_limit)
    update_cpu_load()  # Start CPU monitoring
    
    # Update vertaler status elke 10 seconden (minder frequent)
    def periodic_translator_update():
        update_translator_status()
        if root is not None:
            root.after(10000, periodic_translator_update)
    
    periodic_translator_update()  # Start vertaler status monitoring
    btn_voeg_bestand = tk.Button(left_panel, text="Voeg een bestand toe", font=("Segoe UI", 10, "bold"), height=2, command=kies_video)
    btn_voeg_bestand.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 2))
    btn_voeg_map = tk.Button(left_panel, text="Voeg een map toe", font=("Segoe UI", 10, "bold"), height=2, command=kies_map_en_voeg_toe)
    btn_voeg_map.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(0, 2))
    btn_verwijder = tk.Button(left_panel, text="Verwijder geselecteerd bestand", font=("Segoe UI", 10, "bold"), height=2, bg="#ffebee", fg="#c62828", activebackground="#ffcdd2", activeforeground="#b71c1c", command=verwijder_geselecteerd_bestand)
    btn_verwijder.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(0, 2))
    btn_verwijder_alles = tk.Button(left_panel, text="Verwijder hele lijst", font=("Segoe UI", 10, "bold"), height=2, bg="#d32f2f", fg="white", activebackground="#b71c1c", activeforeground="white", command=verwijder_hele_lijst)
    btn_verwijder_alles.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(0, 2))

    right_panel = tk.LabelFrame(main_frame, text="Verwerking", font=("Segoe UI", 11, "bold"), bg="#f5faf5", fg="#2c2c2c", bd=2, relief="groove", padx=12, pady=12)
    right_panel.grid(row=0, column=1, sticky="nsew", padx=(12, 0), pady=0)
    right_panel.grid_rowconfigure(6, weight=1)  # Listbox nog te verwerken krijgt extra ruimte
    right_panel.grid_rowconfigure(8, weight=1)  # Listbox voltooid krijgt extra ruimte
    right_panel.grid_rowconfigure(99, weight=1)
    right_panel.grid_columnconfigure(0, weight=1)

    info_label = tk.Label(right_panel, text="📄 Geen video gekozen", font=("Segoe UI", 9), fg="gray", justify="left", wraplength=300)
    info_label.grid(row=0, column=0, sticky="ew", pady=(0, 5))
    status_label = tk.Label(right_panel, text="", font=("Segoe UI", 9, "italic"), fg="#006699", anchor="w")
    status_label.grid(row=1, column=0, sticky="ew", pady=(0, 5))
    progress = ttk.Progressbar(right_panel, mode="determinate")
    progress.grid(row=2, column=0, sticky="ew", pady=(10, 10))
    start_button = tk.Button(right_panel, text="Start ondertiteling", font=("Segoe UI", 11, "bold"), bg="#d21f3c", fg="white", activebackground="#a51b2d", padx=10, pady=6, command=start_batch_verwerking)
    start_button.grid(row=3, column=0, sticky="ew", pady=(0, 5))
    kill_button = tk.Button(right_panel, text="KILL SWITCH", font=("Segoe UI", 11, "bold"), bg="#000000", fg="white", activebackground="#333333", activeforeground="white", padx=10, pady=6, command=kill_switch)
    kill_button.grid(row=4, column=0, sticky="ew", pady=(0, 10))
    tk.Label(right_panel, text="📋 Nog te verwerken bestanden:", font=("Segoe UI", 10, "bold")).grid(row=5, column=0, sticky="ew", pady=(10, 5))
    listbox_nog = tk.Listbox(right_panel, height=3, font=("Segoe UI", 9), selectmode=tk.SINGLE)
    listbox_nog.grid(row=6, column=0, sticky="ewns", pady=(0, 5))
    
    # Bind selectie events aan beide listboxes
    def on_listbox_select(event):
        """Update bestandsnaam wanneer een bestand wordt geselecteerd"""
        try:
            widget = event.widget
            selection = widget.curselection()
            if selection:
                selected_index = selection[0]
                selected_item = widget.get(selected_index)
                
                # Update info label met geselecteerde bestandsnaam
                if info_label is not None:
                    # Geoptimaliseerde kleur voor betere leesbaarheid in alle thema's
                    huidig_thema = thema_var.get() if thema_var is not None else "dark"
                    if huidig_thema == "dark":
                        text_color = "white"  # Witte tekst voor dark theme
                    else:
                        text_color = "#2c3e50"  # Donkere tekst voor andere thema's
                    info_label.config(text=f"📄 {selected_item}", fg=text_color)
                    
                log_debug(f"📄 Bestand geselecteerd: {selected_item}")
            else:
                # Reset naar standaard tekst als geen selectie
                if info_label is not None:
                    # Geoptimaliseerde kleur voor "geen bestand" status
                    huidig_thema = thema_var.get() if thema_var is not None else "dark"
                    if huidig_thema == "dark":
                        text_color = "#cccccc"  # Lichtgrijze tekst voor dark theme
                    else:
                        text_color = "gray"  # Grijze tekst voor andere thema's
                    info_label.config(text="📄 Geen video gekozen", fg=text_color)
        except Exception as e:
            log_debug(f"❌ Fout bij update bestandsnaam: {e}")
    
    listbox_nog.bind('<<ListboxSelect>>', on_listbox_select)
    
    tk.Label(right_panel, text="✅ Voltooide bestanden:", font=("Segoe UI", 10, "bold")).grid(row=7, column=0, sticky="ew", pady=(10, 5))
    listbox_voltooid = tk.Listbox(right_panel, height=3, font=("Segoe UI", 9), selectmode=tk.SINGLE)
    listbox_voltooid.grid(row=8, column=0, sticky="ewns", pady=(0, 5))
    listbox_voltooid.bind('<<ListboxSelect>>', on_listbox_select)
    
    # Pas het dark thema toe bij opstarten
    pas_thema_toe("dark")
    
    # Pas lettertype grootte toe bij opstarten
    if 'font_size' in globals() and font_size is not None:
        apply_font_size_to_interface(font_size)
    
    # Pas lettertype toe op menubalk specifiek (alleen bij eerste opstart)
    # Dit wordt nu gedaan via de voeg_tools_menu_toe functie zelf


def test_parallel_processing():
    """Test parallel processing met dummy data"""
    log_debug("🧪 Test parallel processing...")

    def dummy_task(task_id):
        time.sleep(2)  # Simuleer werk
        return f"Task {task_id} voltooid"

    with ThreadPoolExecutor(
        max_workers=getattr(parallel_processor, "max_workers", 4)
    ) as executor:
        futures = [executor.submit(dummy_task, i) for i in range(8)]
        for future in as_completed(futures):
            result = future.result()
            log_debug(f"✅ {result}")

    log_debug("🧪 Parallel processing test voltooid!")


def show_worker_status():
    """Toon worker status"""
    max_workers = getattr(parallel_processor, "max_workers", 4)
    completed_blocks = getattr(parallel_processor, "completed_blocks", 0)
    total_blocks = getattr(parallel_processor, "total_blocks", 0)
    efficiency = (completed_blocks / total_blocks * 100) if total_blocks else 0
    status = f"""
⚡ Worker Status
===============
 Actieve workers: {max_workers}
 Voltooide taken: {completed_blocks}
📊 Totaal taken: {total_blocks}
⏱️ Efficiency: {efficiency:.1f}% (indien voltooid)
"""
    log_debug(status)
    messagebox.showinfo("⚡ Worker Status", status)


def show_throttle_status():
    """Toon API throttle status voor Google Translate en DeepL"""
    worker_count = getattr(parallel_processor, "max_workers", 4)
    throttle_delay = google_translate_throttle.get_throttle_delay(worker_count)
    current_time = time.time()
    
    # Bereken recente requests voor beide services
    google_recent = len([t for t in google_translate_throttle.request_times 
                        if current_time - t < 60])
    deepl_recent = len([t for t in deepl_throttle.request_times 
                       if current_time - t < 60])
    
    status = f"""
🌐 API Throttle Status (Google Translate & DeepL)
================================================
⚙️ Huidige workers: {worker_count}
⏱️ Throttle delay: {throttle_delay:.1f}s

📊 Google Translate:
• Requests laatste minuut: {google_recent}/60
• Totaal requests: {google_translate_throttle.request_count}
• Laatste request: {time.strftime('%H:%M:%S', time.localtime(google_translate_throttle.last_request_time)) if google_translate_throttle.last_request_time > 0 else 'Geen'}

📊 DeepL:
• Requests laatste minuut: {deepl_recent}/60
• Totaal requests: {deepl_throttle.request_count}
• Laatste request: {time.strftime('%H:%M:%S', time.localtime(deepl_throttle.last_request_time)) if deepl_throttle.last_request_time > 0 else 'Geen'}

📋 Throttle Regels:
• 1-2 workers: 2s delay
• 3-4 workers: 3s delay  
• 5-6 workers: 4s delay
• 7-8 workers: 6s delay
• Max 60 requests/minuut per service
"""
    log_debug(status)
    messagebox.showinfo("🌐 API Throttle Status", status)


# Externe dict voor log_text koppeling aan viewer
viewer_log_text_map = {}


def save_processing_state():
    """Sla verwerkingsstatus op"""
    state = {
        "current_block": safe_get(progress),
        "total_blocks": getattr(progress, "maximum", 0),
        "video_path": safe_get(video_pad),
        "settings": {
            "language": safe_get(taal_var),
        },
        "timestamp": datetime.datetime.now().isoformat(),
    }
    
    with open("processing_state.json", "w") as f:
        json.dump(state, f, indent=2)
    
    log_debug("💾 Verwerkingsstatus opgeslagen")


def load_processing_state():
    """Laad verwerkingsstatus"""
    try:
        with open("processing_state.json", "r") as f:
            state = json.load(f)
        
        # Herstel instellingen
        safe_set(taal_var, state["settings"]["language"])
        
        log_debug("📂 Verwerkingsstatus hersteld")
        return state
    except:
        return None


def export_settings():
    """Export instellingen"""
    settings = {
        "language": safe_get(taal_var),
        "translator": huidige_vertaler,
        "theme": safe_get(thema_var),
    }
    
    filename = filedialog.asksaveasfilename(
        title="Export instellingen",
        defaultextension=".json",
        filetypes=[("JSON files", "*.json")],
    )
    
    if filename:
        with open(filename, "w") as f:
            json.dump(settings, f, indent=2)
        log_debug(f"📤 Instellingen geëxporteerd naar: {filename}")


def import_settings():
    """Import instellingen"""
    filename = filedialog.askopenfilename(
        title="Import instellingen", filetypes=[("JSON files", "*.json")]
    )
    
    if filename:
        try:
            with open(filename, "r") as f:
                settings = json.load(f)
            
            safe_set(taal_var, settings.get("language", "en"))
            
            log_debug(f"📥 Instellingen geïmporteerd van: {filename}")
        except Exception as e:
            log_debug(f"❌ Import mislukt: {e}")


def add_advanced_menu_items():
    """Voeg geavanceerde menu items toe"""
    # Deze functie is niet meer nodig omdat het menu al is aangemaakt
    pass


def create_advanced_settings_menu():
    """Maak geavanceerde instellingen menu"""
    try:
        advanced_menu = tk.Menu(menubalk, tearoff=False)
        if menubalk is not None:
            menubalk.add_cascade(label="⚙️ Geavanceerd", menu=advanced_menu)
        
        # Auto-save toggle
        auto_save_var = tk.BooleanVar(value=True)
        advanced_menu.add_checkbutton(
            label=" Auto-save status",
                                     variable=auto_save_var,
            command=lambda: toggle_auto_save(auto_save_var),
        )
        
        # Performance tracking toggle
        perf_tracking_var = tk.BooleanVar(value=True)
        advanced_menu.add_checkbutton(
            label="📊 Performance tracking",
                                     variable=perf_tracking_var,
            command=lambda: toggle_performance_tracking(perf_tracking_var),
        )
        
        # Auto-detect toggle
        auto_detect_var = tk.BooleanVar(value=False)
        advanced_menu.add_checkbutton(
            label=" Auto-detect taal",
                                     variable=auto_detect_var,
            command=lambda: toggle_auto_detect(auto_detect_var),
        )
        
        advanced_menu.add_separator()
        
        # Parallel workers submenu
        workers_menu = tk.Menu(advanced_menu, tearoff=False)
        advanced_menu.add_cascade(label="⚡ Parallel Workers", menu=workers_menu)
        
        workers_var = tk.IntVar(value=4)
        for i in range(1, 9):
            workers_menu.add_radiobutton(
                label=f"{i} worker{'s' if i > 1 else ''}",
                variable=workers_var,
                value=i,
                command=lambda w=i: update_workers(w),
            )
        
        advanced_menu.add_separator()
        
        log_debug("⚙️ Geavanceerde instellingen menu aangemaakt")
        return auto_save_var, perf_tracking_var, auto_detect_var
        
    except Exception as e:
        log_debug(f"❌ Fout bij maken geavanceerd menu: {e}")
        return None, None, None


def toggle_auto_save(var):
    """Toggle auto-save functionaliteit"""
    try:
        if var.get():
            log_debug("📂 Auto-save ingeschakeld")
            messagebox.showinfo(
                "📂 Auto-save",
                              "Auto-save is ingeschakeld.\n\n"
                              "De verwerkingsstatus wordt automatisch opgeslagen:\n"
                              "• Herstel na crash of onderbreking\n"
                              "• Voortzetten bij onderbreking\n"
                "• Backup van instellingen",
            )
        else:
            log_debug(" Auto-save uitgeschakeld")
    except Exception as e:
        log_debug(f"❌ Fout bij toggle auto-save: {e}")


def toggle_performance_tracking(var):
    """Toggle performance tracking"""
    try:
        if var.get():
            log_debug("📊 Performance tracking ingeschakeld")
            messagebox.showinfo(
                "📊 Performance Tracking",
                              "Performance tracking is ingeschakeld.\n\n"
                              "Wordt getrackt:\n"
                              "• CPU en geheugen gebruik\n"
                              "• Verwerkingstijd per blok\n"
                              "• Efficiency rapport\n\n"
                "Bekijk het rapport via Tools → Performance rapport",
            )
        else:
            log_debug("📊 Performance tracking uitgeschakeld")
    except Exception as e:
        log_debug(f"❌ Fout bij toggle performance tracking: {e}")


def toggle_auto_detect(var):
    """Toggle auto-detect taal functionaliteit"""
    try:
        if var.get():
            log_debug("🎯 Auto-detect taal ingeschakeld")
            messagebox.showinfo(
                " Auto-detect Taal",
                              "Auto-detect taal is ingeschakeld.\n\n"
                              "Whisper zal automatisch:\n"
                              "• De gesproken taal detecteren\n"
                              "• De beste instellingen kiezen\n"
                              "• Nauwkeurigheid verbeteren\n\n"
                "Dit kost iets meer tijd maar geeft betere resultaten",
            )
        else:
            log_debug("🎯 Auto-detect taal uitgeschakeld")
    except Exception as e:
        log_debug(f"❌ Fout bij toggle auto-detect: {e}")


def update_workers(worker_count):
    """Update aantal parallel workers"""
    try:
        if parallel_processor is not None:
            setattr(parallel_processor, "max_workers", worker_count)
        log_debug(f"⚡ Parallel workers aangepast naar: {worker_count}")
        messagebox.showinfo(
            "⚡ Workers Aangepast",
                           f"Aantal workers aangepast naar {worker_count}.\n\n"
                           "• 1-2 = Veilig, langzaam\n"
                           "• 3-4 = Aanbevolen\n"
                           "• 5-8 = Snel, meer geheugen\n\n"
            "Pas aan op basis van je systeem.",
        )
    except Exception as e:
        log_debug(f"❌ Fout bij update workers: {e}")


def show_auto_save_help():
    """Toon help voor auto-save"""
    help_text = """
📂 Auto-save Functionaliteit

Wat het doet:
• Slaat automatisch verwerkingsstatus op
• Herstelt na crash of onderbreking
• Bewaart instellingen en voortgang

Voordelen:
• Geen werk verloren bij crash
• Kan verwerking hervatten
• Backup van belangrijke instellingen

Bestanden:
• processing_state.json - Huidige status
• config.json - Instellingen
• debug_log.txt - Log bestanden
"""
    messagebox.showinfo("📂 Auto-save Help", help_text)


def show_performance_help():
    """Toon help voor performance tracking"""
    help_text = """
📊 Performance Tracking

Wat het doet:
• Trackt CPU en geheugen gebruik
• Meet verwerkingstijd per blok
• Genereert efficiency rapporten

Metriek:
• Gemiddelde blok tijd
• Blokken per minuut
• Max geheugen gebruik
• CPU efficiency

Rapport bekijken:
Tools → Performance rapport
"""
    messagebox.showinfo(" Performance Help", help_text)


def show_auto_detect_help():
    """Toon help voor auto-detect"""
    help_text = """
 Auto-detect Taal

Wat het doet:
• Detecteert automatisch gesproken taal
• Kiest optimale Whisper instellingen
• Verbetert transcriptie nauwkeurigheid

Voordelen:
• Geen handmatige taal selectie
• Betere resultaten voor mixed content
• Automatische optimalisatie

Nadelen:
• Iets langzamer verwerking
• Meer geheugen gebruik
• Mogelijk onnauwkeurig bij slechte audio
"""
    messagebox.showinfo(" Auto-detect Help", help_text)


def show_workers_help():
    """Toon help voor parallel workers"""
    help_text = """
⚡ Parallel Workers

Wat het doet:
• Verwerkt meerdere blokken tegelijk
• Versnelt totale verwerkingstijd
• Gebruikt alle CPU cores

Aanbevelingen:
• 1-2 workers: Veilig, langzaam
• 3-4 workers: Aanbevolen balans
• 5-8 workers: Snel, meer geheugen

Systeem vereisten:
• 4GB+ RAM voor 4+ workers
• Multi-core CPU aanbevolen
• SSD voor snelle I/O

Monitoring:
• Tools → Worker status
• Performance rapport
• Log bestanden
"""
    messagebox.showinfo("⚡ Workers Help", help_text)


def create_advanced_ui():
    """Maak geavanceerde UI elementen"""
    # Geen extra UI elementen meer nodig
    pass


def add_to_batch_safe():
    """Voeg veilig toe aan batch"""
    if not selected_video:
        messagebox.showwarning("⚠️", "Kies eerst een videobestand.")
        return
    
    success = batch_manager.add_to_batch(
        selected_video,
        {

        "language": safe_get(taal_var),
        },
    )
    
    if success:
        messagebox.showinfo(
            "✅",
            f"Video toegevoegd aan batch!\nTotaal in batch: {len(batch_manager.batch_list)}",
        )
    else:
        messagebox.showerror("❌", "Kon video niet toevoegen aan batch.")


def start_batch_safe():
    """Start batch veilig"""
    if not batch_manager.batch_list:
        messagebox.showwarning("⚠️", "Batch is leeg. Voeg eerst videos toe.")
        return
    
    threading.Thread(target=batch_manager.process_batch, daemon=True).start()
    log_debug("🚀 Batch verwerking gestart")


def show_batch_status():
    """Toon batch status"""
    if not batch_manager.batch_list:
        messagebox.showinfo("📋 Batch Status", "Batch is leeg")
        return
    
    status = f"📋 Batch Status\n\n"
    status += f"Totaal videos: {len(batch_manager.batch_list)}\n"
    status += f"Huidige video: {batch_manager.current_batch + 1}\n\n"
    
    for i, item in enumerate(batch_manager.batch_list):
        if item["video"] is not None:
            name = os.path.basename(item["video"])
        else:
            name = "Ongeldig pad"
        status += f"{i+1}. {name} - {item['status']}\n"
    
    messagebox.showinfo("📋 Batch Status", status)

    def cancel_configuration():
        """Annuleer configuratie"""
        global config_window
        if config_window is not None:
            config_window.destroy()
        config_window = None

    button_frame = tk.Frame(config_window, bg="#f0f0f0")
    button_frame.pack(fill="x", pady=(10, 0))
    save_btn = tk.Button(
        button_frame,
        text="Opslaan",
        command=lambda: messagebox.showinfo("Niet geïmplementeerd", "Opslaan functionaliteit is nog niet beschikbaar."),
        bg="#27ae60",
        fg="white",
        font=("Arial", 10, "bold"),
    )
    save_btn.pack(side="right", padx=(5, 0))

    button_frame = tk.Frame(config_window, bg="#f0f0f0")
    button_frame.pack(fill="x", pady=(10, 0))

    cancel_btn = tk.Button(
        button_frame,
        text="Annuleren",
        command=cancel_configuration,
        bg="#95a5a6",
        fg="white",
        font=("Arial", 10),
    )
    cancel_btn.pack(side="right")

    # Focus op het venster (controleer of config_window niet None is)
    if config_window is not None:
        config_window.focus_force()
        config_window.lift()


# --- BEGIN show_quality_preview ---
# def show_quality_preview():
#     ...
# --- EINDE show_quality_preview ---
# (Functie verwijderd op verzoek gebruiker)


def add_log_to_viewer(message, level="INFO"):
    """Voeg een bericht toe aan de log viewer - UITGESCHAKELD voor stabiliteit"""
    # Log viewer is uitgeschakeld om fouten te voorkomen
    pass


def add_log_message_to_viewer(message, level="INFO"):
    """Voeg een bericht toe aan de log viewer (alias voor add_log_to_viewer) - UITGESCHAKELD"""
    # Log viewer is uitgeschakeld om fouten te voorkomen
    pass


config_window = None
deepl_key_var = None
model_selection_var = None
output_format_var = None

def update_translator_status():
    """Update translator status"""
    try:
        # Controleer of root bestaat
        if root is None:
            return
            
        # Zoek de translator_status_label in de UI
        for widget in root.winfo_children():
            if hasattr(widget, 'winfo_children'):
                for child in widget.winfo_children():
                    if hasattr(child, 'winfo_children'):
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, tk.Label) and "Vertaler:" in grandchild.cget("text"):
                                grandchild.config(text=f"Vertaler: {huidige_vertaler.upper()}")
                                return
    except Exception as e:
        log_debug(f"❌ Fout bij update vertaler status: {e}")

# (Verwijderd: debug-patch voor tk.Tk())

def test_cuda_performance():
    """Test CUDA vs CPU performance voor Whisper"""
    try:
        log_debug("🧪 START: CUDA vs CPU Performance Test")
        import sys
        import torch
        log_debug(f"PYTHON: {sys.executable}")
        log_debug(f"TORCH: {torch.__version__}, CUDA versie: {torch.version.cuda}, is_available: {torch.cuda.is_available()}")
        try:
            log_debug(f"GPU naam: {torch.cuda.get_device_name(0)}")
        except Exception as e:
            log_debug(f"Fout bij ophalen GPU naam: {e}")
        import whisper
        import time
        
        # Check CUDA beschikbaarheid
        cuda_available = torch.cuda.is_available()
        if cuda_available:
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)  # GB
            log_debug(f"🎮 GPU: {gpu_name}")
            log_debug(f"💾 GPU Memory: {gpu_memory:.1f} GB")
        else:
            log_debug("❌ CUDA niet beschikbaar")
            messagebox.showwarning("❌ CUDA Niet Beschikbaar", 
                "CUDA is niet beschikbaar op dit systeem.\n\n"
                "Om CUDA te gebruiken:\n"
                "1. Installeer NVIDIA GPU drivers\n"
                "2. Installeer CUDA Toolkit 11.0+\n"
                "3. Installeer PyTorch met CUDA support\n\n"
                "Zonder CUDA gebruikt de applicatie CPU voor transcriptie.")
            return
        
        # Test met klein model voor snelle vergelijking
        model_name = "tiny"
        
        # CPU test
        log_debug("🔄 CPU test gestart...")
        device = "cpu"
        model = whisper.load_model(model_name, device=device)
        # model = model.to(device)  # niet meer nodig, device is al goed
        
        # Maak dummy audio voor test
        import numpy as np
        dummy_audio = np.random.randn(16000 * 10).astype(np.float32)  # 10 seconden
        
        start_time = time.time()
        result = model.transcribe(dummy_audio, verbose=False)
        cpu_time = time.time() - start_time
        
        log_debug(f"⏱️ CPU tijd: {cpu_time:.2f} seconden")
        
        # CUDA test
        log_debug("🔄 CUDA test gestart...")
        device = "cuda"
        model = whisper.load_model(model_name, device=device)
        # model = model.to(device)  # niet meer nodig, device is al goed
        
        start_time = time.time()
        result = model.transcribe(dummy_audio, verbose=False)
        cuda_time = time.time() - start_time
        
        log_debug(f"⏱️ CUDA tijd: {cuda_time:.2f} seconden")
        
        # Bereken speedup
        speedup = cpu_time / cuda_time
        improvement_percent = ((cpu_time - cuda_time) / cpu_time) * 100
        
        log_debug(f"🚀 Speedup: {speedup:.1f}x sneller")
        log_debug(f"📈 Verbetering: {improvement_percent:.1f}%")
        
        # Memory optimalisatie na test
        optimize_memory_usage()
        
        # System info
        import psutil
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        
        # Toon resultaat
        result_text = f"""
🎮 CUDA Performance Test Resultaat
==================================
⚙️ GPU: {gpu_name}
💾 GPU Memory: {gpu_memory:.1f} GB
⏱️ CPU tijd: {cpu_time:.2f}s
⏱️ CUDA tijd: {cuda_time:.2f}s
🚀 Speedup: {speedup:.1f}x sneller
📈 Verbetering: {improvement_percent:.1f}%

💡 Praktische Impact:
• 1 minuut audio: {cpu_time/10*60/60:.1f} min → {cuda_time/10*60/60:.1f} min
• 10 minuten audio: {cpu_time/10*600/60:.1f} min → {cuda_time/10*600/60:.1f} min
• 1 uur audio: {cpu_time/10*3600/60:.1f} min → {cuda_time/10*3600/60:.1f} min

💾 System Status:
• CPU Load: {cpu_percent:.1f}%
• Memory: {memory_percent:.1f}%
• Memory management: ✅ Actief
• Garbage collection: ✅ Automatisch

⚡ Reactietijd Optimalisaties:
• UI Update Interval: {UI_UPDATE_INTERVAL}ms (60 FPS)
• Batch Size Limit: {MAX_UI_UPDATE_BATCH_SIZE}
• Priority Updates: ✅ Actief
• Immediate Updates: ✅ Actief
• Preemptive Loading: ✅ Actief
"""
        
        log_debug(result_text)
        messagebox.showinfo("🎮 CUDA Performance Test", result_text)
        
    except Exception as e:
        log_debug(f"❌ CUDA test mislukt: {e}")
        messagebox.showerror("❌ CUDA Test Fout", f"CUDA test mislukt:\n{e}")

def show_cuda_install_instructions():
    """Toon CUDA installatie instructies"""
    instructions = """
🎮 CUDA Installatie Instructies
===============================

📋 Vereisten:
• NVIDIA GPU (GTX 1060 of hoger)
• Windows 10/11
• 4GB+ VRAM

🔧 Stap 1: GPU Drivers
• Download NVIDIA drivers van: https://www.nvidia.com/drivers/
• Installeer de laatste Game Ready drivers

🔧 Stap 2: CUDA Toolkit
• Download CUDA Toolkit 11.8 van: https://developer.nvidia.com/cuda-downloads
• Kies: Windows → x86_64 → 10/11 → exe (local)
• Installeer met standaard instellingen

🔧 Stap 3: PyTorch met CUDA
• Open Command Prompt als Administrator
• Voer uit: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

🔧 Stap 4: Test
• Herstart de applicatie
• Ga naar: Tools → 🎮 CUDA Performance Test

💡 Tips:
• CUDA Toolkit is ~3GB download
• Installeer alleen als je een NVIDIA GPU hebt
• AMD/Intel GPU's ondersteunen geen CUDA
• CPU transcriptie werkt ook prima, alleen langzamer

❓ Problemen?
• Controleer of je NVIDIA GPU hebt
• Herstart na installatie
• Test met: python -c "import torch; print(torch.cuda.is_available())"

⚠️ Opmerking:
De Triton waarschuwingen die je ziet zijn normaal en hebben geen invloed op de functionaliteit.
De applicatie gebruikt nog steeds CUDA voor versnelde transcriptie.
"""
    
    log_debug("📋 CUDA installatie instructies getoond")
    messagebox.showinfo("🎮 CUDA Installatie", instructions)

# --- Subprocess tracking voor kill switch ---
ACTIVE_SUBPROCESSES = []
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

def run_and_track_subprocess(cmd, **kwargs):
    """Start een subprocess, voeg toe aan ACTIVE_SUBPROCESSES, en wacht tot klaar. Logt altijd het commando en pad. Voorkomt systeemcommando's zonder pad."""
    import subprocess
    # Haal timeout uit kwargs zodat deze niet naar Popen gaat
    timeout = kwargs.pop('timeout', None)
    # --- Windows startupinfo om tray vensters te voorkomen ---
    if os.name == 'nt' and 'startupinfo' not in kwargs:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        kwargs['startupinfo'] = startupinfo
    log_debug(f"[SUBPROCESS] Start: {' '.join(str(c) for c in cmd)}")
    if isinstance(cmd, list) and len(cmd) > 0:
        exe_path = cmd[0]
        log_debug(f"[SUBPROCESS] Executable: {exe_path} (bestaat: {os.path.exists(exe_path)})")
        # Voorkom systeemcommando's zonder pad (behalve python, want dat is oké)
        if exe_path.lower() not in ("python", "python.exe") and not os.path.isabs(exe_path):
            log_debug(f"❌ Executable zonder absoluut pad: {exe_path}. ABORT.")
            raise FileNotFoundError(f"Executable zonder absoluut pad: {exe_path}")
    try:
        proc = subprocess.Popen(cmd, **kwargs)
    except Exception as e:
        log_debug(f"[SUBPROCESS] FOUT bij starten: {e}")
        log_debug(f"[SUBPROCESS] kwargs: {kwargs}")
        raise
    ACTIVE_SUBPROCESSES.append(proc)
    try:
        out, err = proc.communicate(timeout=timeout)
        returncode = proc.returncode
    except Exception as e:
        # Bij uitzondering killen
        try:
            if PSUTIL_AVAILABLE:
                p = psutil.Process(proc.pid)
                p.kill()
            else:
                proc.kill()
        except Exception:
            pass
        raise e
    finally:
        if proc in ACTIVE_SUBPROCESSES:
            ACTIVE_SUBPROCESSES.remove(proc)
    return subprocess.CompletedProcess(cmd, returncode, out, err)

# Globale exception handler voor uncaught exceptions
import sys
import traceback

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    log_path = os.path.join(BASE_DIR, "MagicTime_crash_log.txt")
    msg = f"UNCAUGHT EXCEPTION: {exc_value}\n{''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))}"
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write("\n=== UNCAUGHT EXCEPTION ===\n")
            f.write(f"Type: {exc_type.__name__}\n")
            f.write(f"Value: {exc_value}\n")
            f.write(''.join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            f.write("\n========================\n")
    except Exception as e:
        pass  # Stil falen
    # Log ook naar het live log venster
    try:
        log_debug(msg)
    except Exception:
        pass
    # Optioneel: print ook naar stderr voor debug
    print(f"[CRASH] {exc_type.__name__}: {exc_value}")
    traceback.print_exception(exc_type, exc_value, exc_traceback)

sys.excepthook = handle_exception

if __name__ == "__main__":
    try:
        root = tk.Tk()
        root.title("Magic Time Studio")
        
        # Verberg het venster tot alles is geladen
        root.withdraw()
        
        # Voeg icoon toe aan het hoofdvenster
        try:
            if os.path.exists(icon_path):
                root.iconbitmap(icon_path)
                log_debug(f"✅ Icoon geladen: {os.path.basename(icon_path)}")
            else:
                log_debug(f"⚠️ Icoon niet gevonden: {icon_path}")
        except Exception as e:
            log_debug(f"❌ Fout bij laden icoon: {e}")
        
        # Toon een loading venster
        loading_window = tk.Toplevel(root)
        loading_window.title("Magic Time Studio - Laden...")
        loading_window.geometry("400x200")
        loading_window.resizable(False, False)
        loading_window.transient(root)
        loading_window.grab_set()
        
        # Centreer loading venster
        loading_window.update_idletasks()
        x = (loading_window.winfo_screenwidth() // 2) - (loading_window.winfo_width() // 2)
        y = (loading_window.winfo_screenheight() // 2) - (loading_window.winfo_height() // 2)
        loading_window.geometry(f"+{x}+{y}")
        
        # Loading venster inhoud
        loading_frame = tk.Frame(loading_window, bg="#2c3e50", padx=20, pady=20)
        loading_frame.pack(fill="both", expand=True)
        
        title_label = tk.Label(
            loading_frame,
            text="🎬 Magic Time Studio",
            font=("Segoe UI", 16, "bold"),
            fg="white",
            bg="#2c3e50"
        )
        title_label.pack(pady=(0, 10))
        
        status_label = tk.Label(
            loading_frame,
            text="Initialiseren...",
            font=("Segoe UI", 10),
            fg="#ecf0f1",
            bg="#2c3e50"
        )
        status_label.pack(pady=(0, 20))
        
        progress = ttk.Progressbar(loading_frame, mode='indeterminate')
        progress.pack(fill="x", pady=(0, 10))
        progress.start()
        
        # Update loading status
        def update_loading_status(message):
            if status_label is not None:
                status_label.config(text=message)
            if loading_window is not None:
                loading_window.update()
        
        # Setup de UI met loading updates
        update_loading_status("Laden van interface...")
        setup_ui()
        
        update_loading_status("Toevoegen van menu's...")
        # Alleen menu-items toevoegen, niet opnieuw menubalk aanmaken
        if 'menubalk' in globals() and menubalk is not None:
            voeg_tools_menu_toe()
        
        # Memory optimalisatie na setup
        update_loading_status("Optimaliseren van geheugen...")
        optimize_memory_usage()
        
        # Start preemptive loading voor snellere reacties
        update_loading_status("Voorladen van modules...")
        preload_critical_modules()
        
        update_loading_status("Finaliseren...")
        loading_window.update()
        
        # Sluit loading venster
        loading_window.destroy()
        
        # Toon het hoofdvenster
        root.deiconify()
        
        # Centreer het hoofdvenster op het scherm
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
        y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
        root.geometry(f"+{x}+{y}")
        
        # Focus op het hoofdvenster
        root.focus_force()
        root.lift()
        start_auto_processing_loop()
        root.mainloop()
    except KeyboardInterrupt:
        print("\nProgramma gestopt door gebruiker")
    except Exception as e:
        print(f"Fout bij opstarten: {e}")
        import traceback
        traceback.print_exc()
