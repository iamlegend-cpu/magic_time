"""
Theme Manager voor Magic Time Studio PySide6
Beheert alle theme-gerelateerde functionaliteit
"""

class ThemeManager:
    """Beheert alle theme-gerelateerde functionaliteit"""
    
    def __init__(self, main_app):
        self.main_app = main_app
        self.theme_manager = None
        
    def initialize_theme_manager(self):
        """Initialiseer ThemeManager veilig"""
        if self.main_app.ThemeManager:
            try:
                self.theme_manager = self.main_app.ThemeManager()
                print("✅ ThemeManager geïnitialiseerd")
            except Exception as e:
                print(f"⚠️ Fout bij initialiseren ThemeManager: {e}")
                self.theme_manager = None
        else:
            print("⚠️ ThemeManager niet beschikbaar")
            self.theme_manager = None
    
    def apply_theme(self, app, theme_name):
        """Pas een thema toe - wrapper voor de echte ThemeManager"""
        if self.theme_manager and hasattr(self.theme_manager, 'apply_theme'):
            try:
                self.theme_manager.apply_theme(app, theme_name)
                return True
            except Exception as e:
                print(f"⚠️ Fout bij toepassen thema via ThemeManager: {e}")
                return False
        else:
            print("⚠️ ThemeManager niet beschikbaar of heeft geen apply_theme methode")
            return False
