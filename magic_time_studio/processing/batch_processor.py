"""
Batch processor voor Magic Time Studio
Beheert batch verwerking van meerdere video bestanden
"""

import os
import time
import threading
from typing import Dict, Any, List, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from ..core.logging import logger
from ..core.config import config_manager
from ..core.utils import safe_basename
from ..models.processing_queue import processing_queue, batch_manager
from ..models.progress_tracker import progress_tracker
from ..models.performance_tracker import performance_tracker
from .video_processor import video_processor

class BatchProcessor:
    """Processor voor batch verwerking van video bestanden"""
    
    def __init__(self):
        self.is_processing = False
        self.current_batch = []
        self.processing_thread = None
        self.max_workers = 4
        self.stop_requested = False
        
    def add_files_to_batch(self, file_paths: List[str], settings: Dict[str, Any]) -> Dict[str, Any]:
        """Voeg bestanden toe aan batch"""
        try:
            if not file_paths:
                return {"error": "Geen bestanden opgegeven"}
            
            # Filter video bestanden
            video_files = [f for f in file_paths if video_processor.is_video_file(f)]
            
            if not video_files:
                return {"error": "Geen video bestanden gevonden"}
            
            # Voeg toe aan batch manager
            for file_path in video_files:
                batch_manager.add_to_batch(file_path, settings)
            
            logger.log_debug(f"📦 {len(video_files)} bestanden toegevoegd aan batch")
            
            return {
                "success": True,
                "added_files": len(video_files),
                "total_in_batch": len(batch_manager.batch_queue)
            }
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij toevoegen aan batch: {e}")
            return {"error": str(e)}
    
    def start_batch_processing(self, progress_callback: Optional[Callable] = None,
                             status_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """Start batch verwerking"""
        try:
            if self.is_processing:
                return {"error": "Batch verwerking is al actief"}
            
            if not batch_manager.batch_queue:
                return {"error": "Geen bestanden in batch"}
            
            self.is_processing = True
            self.stop_requested = False
            
            # Start processing thread
            self.processing_thread = threading.Thread(
                target=self._process_batch_worker,
                args=(progress_callback, status_callback),
                daemon=True
            )
            self.processing_thread.start()
            
            logger.log_debug(f"🚀 Batch verwerking gestart: {len(batch_manager.batch_queue)} bestanden")
            
            return {
                "success": True,
                "total_files": len(batch_manager.batch_queue)
            }
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij starten batch verwerking: {e}")
            self.is_processing = False
            return {"error": str(e)}
    
    def stop_batch_processing(self) -> Dict[str, Any]:
        """Stop batch verwerking"""
        try:
            if not self.is_processing:
                return {"error": "Geen batch verwerking actief"}
            
            self.stop_requested = True
            logger.log_debug("⏹️ Stop verzoek voor batch verwerking")
            
            return {"success": True, "message": "Stop verzoek verzonden"}
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij stoppen batch verwerking: {e}")
            return {"error": str(e)}
    
    def _process_batch_worker(self, progress_callback: Optional[Callable],
                            status_callback: Optional[Callable]):
        """Worker thread voor batch verwerking"""
        try:
            total_files = len(batch_manager.batch_queue)
            completed_files = 0
            failed_files = 0
            
            # Start performance tracking
            if config_manager.get("performance_tracking", False):
                performance_tracker.start_tracking()
            
            # Maak thread pool
            max_workers = config_manager.get("worker_count", self.max_workers)
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Submit alle taken
                future_to_file = {}
                
                for file_path, settings in batch_manager.batch_queue:
                    if self.stop_requested:
                        break
                    
                    future = executor.submit(self._process_single_file, file_path, settings)
                    future_to_file[future] = file_path
                
                # Verwerk resultaten
                for future in as_completed(future_to_file):
                    if self.stop_requested:
                        break
                    
                    file_path = future_to_file[future]
                    
                    try:
                        result = future.result()
                        
                        if result.get("success"):
                            completed_files += 1
                            logger.log_debug(f"✅ Batch verwerking voltooid: {safe_basename(file_path)}")
                        else:
                            failed_files += 1
                            logger.log_debug(f"❌ Batch verwerking gefaald: {safe_basename(file_path)} - {result.get('error')}")
                        
                        # Update progress
                        progress = (completed_files + failed_files) / total_files
                        if progress_callback:
                            progress_callback(progress, f"Verwerkt: {completed_files + failed_files}/{total_files}")
                        
                        if status_callback:
                            status_callback(f"Voltooid: {completed_files}, Gefaald: {failed_files}")
                        
                    except Exception as e:
                        failed_files += 1
                        logger.log_debug(f"❌ Onverwachte fout bij batch verwerking: {e}")
            
            # Genereer rapport
            if config_manager.get("performance_tracking", False):
                performance_report = performance_tracker.generate_report()
                logger.log_debug(f"📊 Performance rapport: {performance_report}")
            
            # Update status
            if status_callback:
                status_callback(f"Batch voltooid: {completed_files} succesvol, {failed_files} gefaald")
            
            logger.log_debug(f"✅ Batch verwerking voltooid: {completed_files} succesvol, {failed_files} gefaald")
            
        except Exception as e:
            logger.log_debug(f"❌ Fout in batch worker: {e}")
        finally:
            self.is_processing = False
            self.stop_requested = False
    
    def _process_single_file(self, file_path: str, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Verwerk een enkel bestand"""
        try:
            # Progress callback voor individueel bestand
            def file_progress(progress, status):
                logger.log_debug(f"📊 {safe_basename(file_path)}: {status}")
            
            # Verwerk video
            result = video_processor.process_video(file_path, settings, file_progress)
            
            return result
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij verwerken bestand: {e}")
            return {"error": str(e)}
    
    def get_batch_status(self) -> Dict[str, Any]:
        """Krijg status van huidige batch"""
        return {
            "is_processing": self.is_processing,
            "total_files": len(batch_manager.batch_queue),
            "stop_requested": self.stop_requested
        }
    
    def clear_batch(self) -> Dict[str, Any]:
        """Wis alle bestanden uit batch"""
        try:
            batch_manager.batch_queue.clear()
            logger.log_debug("🗑️ Batch gewist")
            return {"success": True, "message": "Batch gewist"}
        except Exception as e:
            logger.log_debug(f"❌ Fout bij wissen batch: {e}")
            return {"error": str(e)}
    
    def remove_file_from_batch(self, file_path: str) -> Dict[str, Any]:
        """Verwijder specifiek bestand uit batch"""
        try:
            # Zoek en verwijder bestand
            for i, (batch_file, settings) in enumerate(batch_manager.batch_queue):
                if batch_file == file_path:
                    batch_manager.batch_queue.pop(i)
                    logger.log_debug(f"🗑️ Bestand verwijderd uit batch: {safe_basename(file_path)}")
                    return {"success": True, "message": "Bestand verwijderd"}
            
            return {"error": "Bestand niet gevonden in batch"}
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij verwijderen bestand uit batch: {e}")
            return {"error": str(e)}
    
    def get_batch_files(self) -> List[Dict[str, Any]]:
        """Krijg lijst van bestanden in batch"""
        batch_info = []
        
        for file_path, settings in batch_manager.batch_queue:
            batch_info.append({
                "file_path": file_path,
                "file_name": safe_basename(file_path),
                "settings": settings
            })
        
        return batch_info
    
    def estimate_processing_time(self) -> Dict[str, Any]:
        """Schat verwerkingstijd voor batch"""
        try:
            total_duration = 0
            total_files = len(batch_manager.batch_queue)
            
            if total_files == 0:
                return {"error": "Geen bestanden in batch"}
            
            # Schat tijd per bestand (gemiddeld 2x video duur)
            for file_path, _ in batch_manager.batch_queue:
                video_info = audio_processor.get_video_info(file_path)
                if video_info.get("success"):
                    duration = video_info.get("info", {}).get("duration", 0)
                    # Schat 2x video duur voor volledige verwerking
                    estimated_time = duration * 2
                    total_duration += estimated_time
            
            # Gemiddelde tijd per bestand
            avg_time_per_file = total_duration / total_files
            
            # Schat met worker count
            worker_count = config_manager.get("worker_count", self.max_workers)
            estimated_total_time = total_duration / worker_count
            
            return {
                "success": True,
                "total_files": total_files,
                "estimated_total_time": estimated_total_time,
                "avg_time_per_file": avg_time_per_file,
                "worker_count": worker_count
            }
            
        except Exception as e:
            logger.log_debug(f"❌ Fout bij schatten verwerkingstijd: {e}")
            return {"error": str(e)}
    
    def is_processing_active(self) -> bool:
        """Controleer of batch verwerking actief is"""
        return self.is_processing

# Globale batch processor instantie
batch_processor = BatchProcessor() 