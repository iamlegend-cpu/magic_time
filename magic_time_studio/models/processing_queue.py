"""
Processing queue en batch management voor Magic Time Studio
"""

import os
import time
import threading
from typing import Dict, Any, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from ..core.logging import logger
# Lazy import van config_manager om circulaire import te voorkomen
def _get_config_manager():
    """Lazy config manager import om circulaire import te voorkomen"""
    try:
        from ..core.config import config_manager
        return config_manager
    except ImportError:
        # Fallback voor directe import
        import sys
        sys.path.append('..')
        try:
            from core.config import config_manager
            return config_manager
        except ImportError:
            return None

class ProcessingQueue:
    """Beheert de wachtrij voor video verwerking"""
    
    def __init__(self):
        self.queue = []
        self.processing = False
        self.processing_cancelled = False
        self.processing_paused = False
    
    def add_video(self, video_path: str, settings: Dict[str, Any]) -> None:
        """Voeg een video toe aan de verwerkingswachtrij"""
        self.queue.append({"video": video_path, "settings": settings})
        logger.log_debug(f"📋 Video toegevoegd aan queue: {os.path.basename(video_path)}")
    
    def process_all(self) -> None:
        """Verwerk alle videos in de wachtrij"""
        if not self.queue:
            logger.log_debug("📋 Queue is leeg")
            return
        
        self.processing = True
        for i, item in enumerate(self.queue):
            logger.log_debug(
                f"🔄 Verwerk video {i+1}/{len(self.queue)}: "
                f"{os.path.basename(item['video'])}"
            )
            # Hier zou je de video verwerking kunnen starten
        self.queue.clear()
        self.processing = False
        logger.log_debug("✅ Alle videos verwerkt!")
    
    def clear_queue(self) -> None:
        """Leeg de wachtrij"""
        self.queue.clear()
        logger.log_debug("📋 Wachtrij geleegd")
    
    def get_queue_size(self) -> int:
        """Krijg de grootte van de wachtrij"""
        return len(self.queue)
    
    def is_processing(self) -> bool:
        """Controleer of er verwerking bezig is"""
        return self.processing



class APITranslateThrottle:
    """Beheert API rate limiting voor vertalingen"""
    
    def __init__(self, service_name: str = "API"):
        self.service_name = service_name
        self.last_request_time = 0
        self.request_count = 0
        # Haal limiet uit config
        config_mgr = _get_config_manager()
        self.max_requests_per_minute = int(config_mgr.get_env("LIBRETRANSLATE_RATE_LIMIT", "60") if config_mgr else 60)
        # Bereken minimale delay op basis van limiet
        if self.max_requests_per_minute > 0:
            self.min_delay_between_requests = 60.0 / self.max_requests_per_minute
        else:
            self.min_delay_between_requests = 0.0
    
    def get_throttle_delay(self, worker_count: int) -> float:
        """Bereken de benodigde vertraging voor rate limiting"""
        if worker_count <= 0:
            return 0
        
        # Basis vertraging per worker
        base_delay = self.min_delay_between_requests / worker_count
        
        # Extra vertraging bij hoge worker counts
        if worker_count > 4:
            base_delay *= 1.5
        if worker_count > 8:
            base_delay *= 2.0
        
        return max(base_delay, 0.1)  # Minimum 0.1 seconde
    
    def wait_if_needed(self, worker_count: int) -> None:
        """Wacht indien nodig voor rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        required_delay = self.get_throttle_delay(worker_count)
        
        if time_since_last < required_delay:
            sleep_time = required_delay - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
        self.request_count += 1

# Globale instanties
processing_queue = ProcessingQueue()

# Lazy instantie van API throttle om circulaire import te voorkomen
_api_throttle = None

def get_api_throttle():
    """Lazy instantie van API throttle om circulaire import te voorkomen"""
    global _api_throttle
    if _api_throttle is None:
        _api_throttle = APITranslateThrottle()
    return _api_throttle 