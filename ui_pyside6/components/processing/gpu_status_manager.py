"""
GPU Status Manager component voor Magic Time Studio
Bevat alle GPU monitor beheer logica
"""

from PySide6.QtCore import QObject

class GPUStatusManager(QObject):
    """Beheert alle GPU monitor status updates"""
    
    def __init__(self, ui_component):
        super().__init__()
        self.ui = ui_component
    
    def update_gpu_monitor_status(self, is_active: bool):
        """Update GPU Monitor status direct vanuit ProcessingPanel"""
        try:
            # Zoek naar GPU Monitor via parent chain
            parent = self.ui.parent()
            while parent:
                if hasattr(parent, 'charts_panel'):
                    charts_panel = parent.charts_panel
                    if hasattr(charts_panel, 'gpu_monitor'):
                        charts_panel.gpu_monitor.set_processing_status(is_active, is_active)
                        print(f"🔧 [DEBUG] ProcessingPanel: GPU Monitor status bijgewerkt: {is_active}")
                        return
                parent = parent.parent()
            
            print(f"⚠️ [WAARSCHUWING] GPU Monitor niet gevonden in parent chain")
        except Exception as e:
            print(f"⚠️ [WAARSCHUWING] Kon GPU Monitor status niet bijwerken: {e}")
    
    def force_gpu_monitor_green(self):
        """Forceer GPU Monitor naar groen (WhisperX actief)"""
        try:
            # Zoek naar GPU Monitor via parent chain
            parent = self.ui.parent()
            while parent:
                if hasattr(parent, 'charts_panel'):
                    charts_panel = parent.charts_panel
                    if hasattr(charts_panel, 'gpu_monitor'):
                        # Forceer GPU Monitor naar groen
                        charts_panel.gpu_monitor.set_processing_status(True, True)
                        print(f"🟢 [FORCE] GPU Monitor geforceerd naar groen - WhisperX actief")
                        return True
                parent = parent.parent()
            
            print(f"⚠️ [WAARSCHUWING] GPU Monitor niet gevonden voor forceren")
            return False
        except Exception as e:
            print(f"⚠️ [WAARSCHUWING] Kon GPU Monitor niet forceren: {e}")
            return False
