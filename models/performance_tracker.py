"""
Performance tracking voor Magic Time Studio
"""

import time
from typing import List, Optional

# Lazy import van logger om import problemen te voorkomen
def get_logger():
    """Lazy import van logger"""
    try:
        from ..core.logging import logger
        return logger
    except ImportError:
        # Fallback logger
        class FallbackLogger:
            def debug(self, msg): print(f"[DEBUG] {msg}")
            def info(self, msg): print(f"[INFO] {msg}")
            def warning(self, msg): print(f"[WARNING] {msg}")
            def error(self, msg): print(f"[ERROR] {msg}")
        return FallbackLogger()

logger = get_logger()

class PerformanceTracker:
    """Beheert performance monitoring voor video verwerking"""
    
    def __init__(self):
        self.start_time = None
        self.block_times = []
        self.memory_usage = []
        self.cpu_usage = []
        self.enabled = False
    
    def start_tracking(self) -> None:
        """Start performance tracking"""
        self.start_time = time.time()
        self.block_times = []
        self.memory_usage = []
        self.cpu_usage = []
        self.enabled = True
        logger.debug("📊 Performance tracking gestart")
    
    def stop_tracking(self) -> None:
        """Stop performance tracking"""
        self.enabled = False
        logger.debug("📊 Performance tracking gestopt")
    
    def track_block(self, block_num: int, duration: float) -> None:
        """Track een verwerkt blok"""
        if not self.enabled:
            return
            
        self.block_times.append(duration)
        
        # Track systeem resources als psutil beschikbaar is
        try:
            import psutil
            self.memory_usage.append(psutil.virtual_memory().percent)
            self.cpu_usage.append(psutil.cpu_percent())
        except ImportError:
            pass  # psutil niet beschikbaar
    
    def generate_report(self) -> str:
        """Genereer een performance rapport"""
        if not self.start_time:
            logger.debug("📊 Geen performance data beschikbaar")
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
        
        logger.debug(report)
        return report
    
    def get_statistics(self) -> dict:
        """Krijg performance statistieken"""
        if not self.start_time:
            return {}
        
        stats = {
            "total_time": time.time() - self.start_time,
            "total_blocks": len(self.block_times),
            "avg_block_time": sum(self.block_times) / len(self.block_times) if self.block_times else 0,
            "min_block_time": min(self.block_times) if self.block_times else 0,
            "max_block_time": max(self.block_times) if self.block_times else 0,
        }
        
        if self.memory_usage:
            stats.update({
                "avg_memory": sum(self.memory_usage) / len(self.memory_usage),
                "max_memory": max(self.memory_usage),
                "min_memory": min(self.memory_usage)
            })
        
        if self.cpu_usage:
            stats.update({
                "avg_cpu": sum(self.cpu_usage) / len(self.cpu_usage),
                "max_cpu": max(self.cpu_usage),
                "min_cpu": min(self.cpu_usage)
            })
        
        return stats
    
    def reset(self) -> None:
        """Reset performance tracking"""
        self.start_time = None
        self.block_times = []
        self.memory_usage = []
        self.cpu_usage = []
        self.enabled = False
    
    def is_tracking(self) -> bool:
        """Controleer of tracking actief is"""
        return self.enabled and self.start_time is not None
    
    def get_current_memory_usage(self) -> Optional[float]:
        """Krijg huidige geheugengebruik"""
        try:
            import psutil
            return psutil.virtual_memory().percent
        except ImportError:
            return None
    
    def get_current_cpu_usage(self) -> Optional[float]:
        """Krijg huidige CPU gebruik"""
        try:
            import psutil
            return psutil.cpu_percent()
        except ImportError:
            return None

# Globale performance tracker instantie
performance_tracker = PerformanceTracker() 