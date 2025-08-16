"""
Menu Manager voor Magic Time Studio
Beheer alle menu functionaliteit
"""

from PySide6.QtWidgets import QMenuBar, QMenu
from PySide6.QtGui import QAction
from PySide6.QtCore import Signal, QObject

class MenuManager(QObject):
    """Manager voor menu functionaliteit"""
    
    # Signals
    add_file_triggered = Signal()
    add_folder_triggered = Signal()
    remove_selected_triggered = Signal()
    clear_list_triggered = Signal()
    start_processing_triggered = Signal()

    show_config_triggered = Signal()
    show_log_triggered = Signal()
    performance_test_triggered = Signal()
    cuda_test_triggered = Signal()
    whisper_diagnose_triggered = Signal()
    test_completed_files_triggered = Signal()
    theme_changed = Signal(str)
    exit_triggered = Signal()
    show_charts_triggered = Signal()
    show_batch_triggered = Signal()
    
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.menubar = main_window.menuBar()
        self.theme_manager = main_window.theme_manager
        
        self.create_menus()
    
    def create_menus(self):
        """Maak alle menu's"""
        self.create_file_menu()
        self.create_processing_menu()
        self.create_view_menu()
        self.create_settings_menu()
        self.create_tools_menu()
    
    def create_file_menu(self):
        """Maak het Bestand menu"""
        file_menu = self.menubar.addMenu("Bestand")
        
        # Bestand toevoegen
        add_file_action = QAction("Bestand toevoegen...", self.main_window)
        add_file_action.setShortcut("Ctrl+O")
        add_file_action.triggered.connect(self.add_file_triggered.emit)
        file_menu.addAction(add_file_action)
        
        # Map toevoegen
        add_folder_action = QAction("Map toevoegen...", self.main_window)
        add_folder_action.setShortcut("Ctrl+Shift+O")
        add_folder_action.triggered.connect(self.add_folder_triggered.emit)
        file_menu.addAction(add_folder_action)
        
        file_menu.addSeparator()
        
        # Verwijder geselecteerd
        remove_action = QAction("Verwijder geselecteerd", self.main_window)
        remove_action.setShortcut("Delete")
        remove_action.triggered.connect(self.remove_selected_triggered.emit)
        file_menu.addAction(remove_action)
        
        # Wis lijst
        clear_action = QAction("Wis lijst", self.main_window)
        clear_action.triggered.connect(self.clear_list_triggered.emit)
        file_menu.addAction(clear_action)
        
        file_menu.addSeparator()
        
        # Afsluiten
        exit_action = QAction("Afsluiten", self.main_window)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_triggered.emit)
        file_menu.addAction(exit_action)
    
    def create_processing_menu(self):
        """Maak het Verwerking menu"""
        processing_menu = self.menubar.addMenu("Verwerking")
        
        # Start verwerking
        start_action = QAction("Start verwerking", self.main_window)
        start_action.setShortcut("F5")
        start_action.triggered.connect(self.start_processing_triggered.emit)
        processing_menu.addAction(start_action)
    
    def create_view_menu(self):
        """Maak het Beeld menu"""
        view_menu = self.menubar.addMenu("Beeld")
        
        # Charts Panel
        charts_action = QAction("Grafieken Panel", self.main_window)
        charts_action.setShortcut("Ctrl+Shift+C")
        charts_action.triggered.connect(self.show_charts_triggered.emit)
        view_menu.addAction(charts_action)
        
        # Batch Panel
        batch_action = QAction("Batch Panel", self.main_window)
        batch_action.setShortcut("Ctrl+Shift+B")
        batch_action.triggered.connect(self.show_batch_triggered.emit)
        view_menu.addAction(batch_action)
    
    def create_settings_menu(self):
        """Maak het Instellingen menu"""
        settings_menu = self.menubar.addMenu("Instellingen")
        
        # Configuratie
        config_action = QAction("Configuratie...", self.main_window)
        config_action.triggered.connect(self.show_config_triggered.emit)
        settings_menu.addAction(config_action)
        
        settings_menu.addSeparator()
        
        # Thema submenu
        theme_menu = settings_menu.addMenu("Thema")
        for theme in self.theme_manager.get_available_themes():
            theme_action = QAction(theme.title(), self.main_window)
            theme_action.triggered.connect(lambda checked, t=theme: self.theme_changed.emit(t))
            theme_menu.addAction(theme_action)
    
    def create_tools_menu(self):
        """Maak het Tools menu"""
        tools_menu = self.menubar.addMenu("Tools")
        
        # Log viewer
        log_action = QAction("Log viewer...", self.main_window)
        log_action.triggered.connect(self.show_log_triggered.emit)
        tools_menu.addAction(log_action)
        
        # Performance test
        performance_action = QAction("Performance test...", self.main_window)
        performance_action.triggered.connect(self.performance_test_triggered.emit)
        tools_menu.addAction(performance_action)
        
        tools_menu.addSeparator()
        
        # CUDA test
        cuda_action = QAction("CUDA test...", self.main_window)
        cuda_action.triggered.connect(self.cuda_test_triggered.emit)
        tools_menu.addAction(cuda_action)
        
        # Whisper diagnose
        whisper_action = QAction("Whisper diagnose...", self.main_window)
        whisper_action.triggered.connect(self.whisper_diagnose_triggered.emit)
        tools_menu.addAction(whisper_action)
        
        tools_menu.addSeparator()
        
        # Test voltooide bestanden
        test_completed_action = QAction("Test Voltooide Bestanden", self.main_window)
        test_completed_action.triggered.connect(self.test_completed_files_triggered.emit)
        tools_menu.addAction(test_completed_action)
    
    def update_processing_actions(self, is_processing: bool):
        """Update processing menu acties"""
        # Deze methode kan gebruikt worden om menu items te enablen/disablen
        # gebaseerd op de verwerkingsstatus
        pass 