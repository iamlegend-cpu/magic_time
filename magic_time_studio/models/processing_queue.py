"""
Processing queue en batch management voor Magic Time Studio
"""

import os
import time
import threading
from typing import Dict, Any, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from ..core.logging import logger

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

class BatchManager:
    """Beheert batch verwerking van videos"""
    
    def __init__(self):
        self.batch_list = []
        self.current_batch = 0
        self.processing_cancelled = False
        self.processing_paused = False
        
    def add_to_batch(self, video_path: str, settings: Dict[str, Any]) -> bool:
        """Voeg een video toe aan de batch"""
        if video_path is None:
            logger.log_debug("❌ Geen video pad opgegeven voor batch")
            return False
            
        self.batch_list.append(
            {"video": video_path, "settings": settings, "status": "pending"}
        )
        logger.log_debug(f"📋 Toegevoegd aan batch: {os.path.basename(video_path)}")
        return True
    
    def process_batch(self) -> None:
        """Verwerk alle videos in de batch"""
        if not self.batch_list:
            logger.log_debug("📋 Batch is leeg")
            return
            
        for i, item in enumerate(self.batch_list):
            if self.processing_cancelled:
                break
                
            self.current_batch = i
            item["status"] = "processing"
            
            if item["video"] is None:
                logger.log_debug(f"❌ Ongeldig video pad in batch item {i+1}")
                item["status"] = "failed"
                continue
                
            logger.log_debug(
                f"🔄 Verwerk batch item {i+1}/{len(self.batch_list)}: "
                f"{os.path.basename(item['video'])}"
            )
            
            time.sleep(2)  # Simulatie van verwerking
            
            if self.processing_paused:
                while self.processing_paused and not self.processing_cancelled:
                    time.sleep(0.5)
            
            item["status"] = "completed"
        
        logger.log_debug("✅ Batch verwerking voltooid!")
    
    def clear_batch(self) -> None:
        """Leeg de batch"""
        self.batch_list.clear()
        self.current_batch = 0
        logger.log_debug("📋 Batch geleegd")
    
    def get_batch_size(self) -> int:
        """Krijg de grootte van de batch"""
        return len(self.batch_list)
    
    def get_current_batch(self) -> int:
        """Krijg het huidige batch nummer"""
        return self.current_batch
    
    def cancel_processing(self) -> None:
        """Annuleer de verwerking"""
        self.processing_cancelled = True
        logger.log_debug("❌ Verwerking geannuleerd")
    
    def pause_processing(self) -> None:
        """Pauzeer de verwerking"""
        self.processing_paused = True
        logger.log_debug("⏸️ Verwerking gepauzeerd")
    
    def resume_processing(self) -> None:
        """Hervat de verwerking"""
        self.processing_paused = False
        logger.log_debug("▶️ Verwerking hervat")

class APITranslateThrottle:
    """Beheert API rate limiting voor vertalingen"""
    
    def __init__(self, service_name: str = "API"):
        self.service_name = service_name
        self.last_request_time = 0
        self.request_count = 0
        self.max_requests_per_minute = 60
        self.min_delay_between_requests = 1.0  # seconden
    
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
batch_manager = BatchManager()
api_throttle = APITranslateThrottle() 