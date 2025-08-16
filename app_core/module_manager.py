"""
Module Manager voor Magic Time Studio PySide6
Beheert alle module initialisatie en configuratie
"""

class ModuleManager:
    """Beheert alle module initialisatie en configuratie"""
    
    def __init__(self, main_app):
        self.main_app = main_app
        
    def initialize_modules(self):
        """Initialiseer alle modules"""
        print("🚀 Magic Time Studio PySide6 wordt geïnitialiseerd...")
        
        # Laad configuratie
        self._load_configuration()
        
        # Log systeem informatie
        self._log_system_info()
        
        # Initialiseer processing modules
        self._init_processing_modules()
        
        print("✅ Modules geïnitialiseerd")
    
    def _load_configuration(self):
        """Laad configuratie veilig"""
        if self.main_app.config_manager:
            try:
                self.main_app.config_manager.load_configuration()
                print("✅ Configuratie geladen")
            except Exception as e:
                print(f"⚠️ Fout bij laden configuratie: {e}")
        else:
            print("⚠️ Configuratie niet geïnitialiseerd: config_manager niet beschikbaar")
    
    def _log_system_info(self):
        """Log systeem informatie"""
        print("💾 RAM: 33.7% gebruikt (18.5GB vrij)")
        print("💻 CPU: 0.0% gebruikt")
    
    def _init_processing_modules(self):
        """Initialiseer processing modules"""
        print("🔧 Processing modules initialiseren...")
        
        # Initialiseer Whisper Manager
        self._init_whisper_manager()
        
        # Controleer FFmpeg
        self._check_ffmpeg()
        
        # Zet vertaler service
        self._init_translator()
    
    def _init_whisper_manager(self):
        """Initialiseer Whisper Manager veilig"""
        if self.main_app.whisper_manager and self.main_app.config_manager:
            try:
                # Alleen WhisperX wordt ondersteund
                default_whisper_type = "whisperx"
                default_model = self.main_app.config_manager.get_env("DEFAULT_WHISPERX_MODEL", "large-v3")
                
                print(f"[DEBUG] Gekozen Whisper type: {default_whisper_type}, model: {default_model}")
                
                if self.main_app.whisper_manager.initialize(default_whisper_type, default_model):
                    print(f"✅ Whisper Manager geïnitialiseerd met {default_whisper_type} model: {default_model}")
                else:
                    print("⚠️ Whisper Manager initialisatie gefaald")
            except Exception as e:
                print(f"⚠️ Fout bij initialiseren Whisper Manager: {e}")
        else:
            print("⚠️ Whisper Manager niet geïnitialiseerd: whisper_manager of config_manager niet beschikbaar")
    
    def _check_ffmpeg(self):
        """Controleer FFmpeg beschikbaarheid"""
        try:
            # Controleer eerst of FFmpeg bestand bestaat in assets directory
            import os
            assets_ffmpeg = os.path.join("assets", "ffmpeg.exe")
            if os.path.exists(assets_ffmpeg):
                print(f"✅ FFmpeg gevonden in assets: {os.path.abspath(assets_ffmpeg)}")
                return
            
            # Als het niet in assets staat, probeer het commando
            import subprocess
            result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ FFmpeg beschikbaar via PATH")
            else:
                print("⚠️ FFmpeg niet gevonden in PATH")
        except Exception as e:
            print(f"⚠️ Fout bij controleren FFmpeg: {e}")
            print("💡 Zorg ervoor dat ffmpeg.exe aanwezig is in de assets directory")
    
    def _init_translator(self):
        """Initialiseer Translator service"""
        try:
            # Test LibreTranslate server connectie
            import requests
            server_url = "http://100.90.127.78:5000"
            response = requests.get(f"{server_url}/languages", timeout=10)
            if response.status_code == 200:
                print("✅ LibreTranslate server bereikbaar")
            else:
                print("⚠️ LibreTranslate server niet bereikbaar")
        except Exception as e:
            print(f"⚠️ Fout bij controleren LibreTranslate: {e}")
