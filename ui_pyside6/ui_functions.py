"""
UI functies voor Magic Time Studio
Bevat alle UI-gerelateerde functionaliteit
"""

import os
from typing import Optional, Dict, List, Any, Tuple
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QGroupBox, QTextEdit, QListWidget, QListWidgetItem,
    QMainWindow, QApplication, QFileDialog, QMessageBox,
    QProgressBar, QSlider, QComboBox, QCheckBox, QLineEdit,
    QSpinBox, QDoubleSpinBox, QTabWidget, QSplitter
)
from PySide6.QtCore import Qt, QTimer, QThread, Signal
from PySide6.QtGui import QFont, QPalette, QColor, QIcon, QPixmap
import logging

logger = logging.getLogger(__name__)

def create_modern_button(text: str, icon_path: Optional[str] = None, 
                        style: str = "primary") -> QPushButton:
    """
    Maak een moderne knop met styling
    
    Args:
        text: Tekst voor de knop
        icon_path: Pad naar het icoon (optioneel)
        style: Stijl van de knop (primary, secondary, success, danger)
    
    Returns:
        Geconfigureerde QPushButton
    """
    button = QPushButton(text)
    
    # Voeg icoon toe als opgegeven
    if icon_path and os.path.exists(icon_path):
        button.setIcon(QIcon(icon_path))
    
    # Pas styling toe
    button.setMinimumHeight(40)
    button.setFont(QFont("Segoe UI", 10))
    
    # Stijl-specifieke kleuren
    style_colors = {
        "primary": {"bg": "#007bff", "fg": "#ffffff", "hover": "#0056b3"},
        "secondary": {"bg": "#6c757d", "fg": "#ffffff", "hover": "#545b62"},
        "success": {"bg": "#28a745", "fg": "#ffffff", "hover": "#1e7e34"},
        "danger": {"bg": "#dc3545", "fg": "#ffffff", "hover": "#c82333"}
    }
    
    if style in style_colors:
        colors = style_colors[style]
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors['bg']};
                color: {colors['fg']};
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {colors['hover']};
            }}
            QPushButton:pressed {{
                background-color: {colors['hover']};
            }}
        """)
    
    return button

def create_styled_group_box(title: str, layout: Optional[QWidget] = None) -> QGroupBox:
    """
    Maak een gestylede groep box
    
    Args:
        title: Titel van de groep
        layout: Layout om toe te voegen (optioneel)
    
    Returns:
        Geconfigureerde QGroupBox
    """
    group_box = QGroupBox(title)
    group_box.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
    group_box.setStyleSheet("""
        QGroupBox {
            font-weight: bold;
            border: 2px solid #cccccc;
            border-radius: 5px;
            margin-top: 1ex;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
    """)
    
    if layout:
        group_box.setLayout(layout)
    
    return group_box

def create_progress_bar(show_text: bool = True) -> QProgressBar:
    """
    Maak een gestylede progress bar
    
    Args:
        show_text: Of tekst getoond moet worden
    
    Returns:
        Geconfigureerde QProgressBar
    """
    progress_bar = QProgressBar()
    progress_bar.setShowText(show_text)
    progress_bar.setMinimumHeight(25)
    progress_bar.setStyleSheet("""
        QProgressBar {
            border: 2px solid #cccccc;
            border-radius: 5px;
            text-align: center;
            background-color: #f0f0f0;
        }
        QProgressBar::chunk {
            background-color: #007bff;
            border-radius: 3px;
        }
    """)
    
    return progress_bar

def create_styled_combo_box(items: List[str] = None) -> QComboBox:
    """
    Maak een gestylede combo box
    
    Args:
        items: Lijst van items om toe te voegen
    
    Returns:
        Geconfigureerde QComboBox
    """
    combo_box = QComboBox()
    combo_box.setMinimumHeight(35)
    combo_box.setFont(QFont("Segoe UI", 9))
    
    if items:
        combo_box.addItems(items)
    
    combo_box.setStyleSheet("""
        QComboBox {
            border: 2px solid #cccccc;
            border-radius: 5px;
            padding: 5px;
            background-color: white;
        }
        QComboBox::drop-down {
            border: none;
            width: 20px;
        }
        QComboBox::down-arrow {
            image: url(down_arrow.png);
            width: 12px;
            height: 12px;
        }
        QComboBox QAbstractItemView {
            border: 2px solid #cccccc;
            selection-background-color: #007bff;
        }
    """)
    
    return combo_box

def create_styled_line_edit(placeholder: str = "", default_text: str = "") -> QLineEdit:
    """
    Maak een gestylede line edit
    
    Args:
        placeholder: Placeholder tekst
        default_text: Standaard tekst
    
    Returns:
        Geconfigureerde QLineEdit
    """
    line_edit = QLineEdit()
    line_edit.setPlaceholderText(placeholder)
    line_edit.setText(default_text)
    line_edit.setMinimumHeight(35)
    line_edit.setFont(QFont("Segoe UI", 9))
    
    line_edit.setStyleSheet("""
        QLineEdit {
            border: 2px solid #cccccc;
            border-radius: 5px;
            padding: 5px;
            background-color: white;
        }
        QLineEdit:focus {
            border-color: #007bff;
        }
    """)
    
    return line_edit

def create_styled_checkbox(text: str, checked: bool = False) -> QCheckBox:
    """
    Maak een gestylede checkbox
    
    Args:
        text: Tekst voor de checkbox
        checked: Of de checkbox standaard aangevinkt is
    
    Returns:
        Geconfigureerde QCheckBox
    """
    checkbox = QCheckBox(text)
    checkbox.setChecked(checked)
    checkbox.setFont(QFont("Segoe UI", 9))
    
    checkbox.setStyleSheet("""
        QCheckBox {
            spacing: 8px;
        }
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
            border: 2px solid #cccccc;
            border-radius: 3px;
            background-color: white;
        }
        QCheckBox::indicator:checked {
            background-color: #007bff;
            border-color: #007bff;
        }
        QCheckBox::indicator:checked::after {
            content: "✓";
            color: white;
            font-weight: bold;
            text-align: center;
        }
    """)
    
    return checkbox

def create_styled_spinbox(minimum: int = 0, maximum: int = 100, 
                         default_value: int = 0) -> QSpinBox:
    """
    Maak een gestylede spinbox
    
    Args:
        minimum: Minimum waarde
        maximum: Maximum waarde
        default_value: Standaard waarde
    
    Returns:
        Geconfigureerde QSpinBox
    """
    spinbox = QSpinBox()
    spinbox.setMinimum(minimum)
    spinbox.setMaximum(maximum)
    spinbox.setValue(default_value)
    spinbox.setMinimumHeight(35)
    spinbox.setFont(QFont("Segoe UI", 9))
    
    spinbox.setStyleSheet("""
        QSpinBox {
            border: 2px solid #cccccc;
            border-radius: 5px;
            padding: 5px;
            background-color: white;
        }
        QSpinBox::up-button, QSpinBox::down-button {
            width: 20px;
            border: none;
            background-color: #f0f0f0;
        }
        QSpinBox::up-button:hover, QSpinBox::down-button:hover {
            background-color: #e0e0e0;
        }
    """)
    
    return spinbox

def create_styled_double_spinbox(minimum: float = 0.0, maximum: float = 100.0,
                                default_value: float = 0.0, decimals: int = 2) -> QDoubleSpinBox:
    """
    Maak een gestylede double spinbox
    
    Args:
        minimum: Minimum waarde
        maximum: Maximum waarde
        default_value: Standaard waarde
        decimals: Aantal decimalen
    
    Returns:
        Geconfigureerde QDoubleSpinBox
    """
    spinbox = QDoubleSpinBox()
    spinbox.setMinimum(minimum)
    spinbox.setMaximum(maximum)
    spinbox.setValue(default_value)
    spinbox.setDecimals(decimals)
    spinbox.setMinimumHeight(35)
    spinbox.setFont(QFont("Segoe UI", 9))
    
    spinbox.setStyleSheet("""
        QDoubleSpinBox {
            border: 2px solid #cccccc;
            border-radius: 5px;
            padding: 5px;
            background-color: white;
        }
        QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
            width: 20px;
            border: none;
            background-color: #f0f0f0;
        }
        QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {
            background-color: #e0e0e0;
        }
    """)
    
    return spinbox

def create_styled_slider(minimum: int = 0, maximum: int = 100,
                        default_value: int = 50, orientation: Qt.Orientation = Qt.Orientation.Horizontal) -> QSlider:
    """
    Maak een gestylede slider
    
    Args:
        minimum: Minimum waarde
        maximum: Maximum waarde
        default_value: Standaard waarde
        orientation: Oriëntatie van de slider
    
    Returns:
        Geconfigureerde QSlider
    """
    slider = QSlider(orientation)
    slider.setMinimum(minimum)
    slider.setMaximum(maximum)
    slider.setValue(default_value)
    
    if orientation == Qt.Orientation.Horizontal:
        slider.setMinimumHeight(25)
    else:
        slider.setMinimumWidth(25)
    
    slider.setStyleSheet("""
        QSlider::groove:horizontal {
            border: 1px solid #cccccc;
            height: 8px;
            background: #f0f0f0;
            margin: 2px 0;
            border-radius: 4px;
        }
        QSlider::handle:horizontal {
            background: #007bff;
            border: 1px solid #0056b3;
            width: 18px;
            margin: -2px 0;
            border-radius: 9px;
        }
        QSlider::handle:horizontal:hover {
            background: #0056b3;
        }
        QSlider::sub-page:horizontal {
            background: #007bff;
            border-radius: 4px;
        }
    """)
    
    return slider

def create_styled_list_widget() -> QListWidget:
    """
    Maak een gestylede list widget
    
    Returns:
        Geconfigureerde QListWidget
    """
    list_widget = QListWidget()
    list_widget.setFont(QFont("Segoe UI", 9))
    
    list_widget.setStyleSheet("""
        QListWidget {
            border: 2px solid #cccccc;
            border-radius: 5px;
            background-color: white;
            alternate-background-color: #f8f9fa;
        }
        QListWidget::item {
            padding: 8px;
            border-bottom: 1px solid #e9ecef;
        }
        QListWidget::item:selected {
            background-color: #007bff;
            color: white;
        }
        QListWidget::item:hover {
            background-color: #e9ecef;
        }
    """)
    
    return list_widget

def create_styled_text_edit() -> QTextEdit:
    """
    Maak een gestylede text edit
    
    Returns:
        Geconfigureerde QTextEdit
    """
    text_edit = QTextEdit()
    text_edit.setFont(QFont("Consolas", 9))
    
    text_edit.setStyleSheet("""
        QTextEdit {
            border: 2px solid #cccccc;
            border-radius: 5px;
            background-color: white;
            padding: 5px;
        }
        QTextEdit:focus {
            border-color: #007bff;
        }
    """)
    
    return text_edit

def create_tab_widget() -> QTabWidget:
    """
    Maak een gestylede tab widget
    
    Returns:
        Geconfigureerde QTabWidget
    """
    tab_widget = QTabWidget()
    
    tab_widget.setStyleSheet("""
        QTabWidget::pane {
            border: 2px solid #cccccc;
            border-radius: 5px;
            background-color: white;
        }
        QTabBar::tab {
            background-color: #f8f9fa;
            border: 1px solid #cccccc;
            padding: 8px 16px;
            margin-right: 2px;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
        }
        QTabBar::tab:selected {
            background-color: white;
            border-bottom-color: white;
        }
        QTabBar::tab:hover {
            background-color: #e9ecef;
        }
    """)
    
    return tab_widget

def create_splitter(orientation: Qt.Orientation = Qt.Orientation.Horizontal) -> QSplitter:
    """
    Maak een gestylede splitter
    
    Args:
        orientation: Oriëntatie van de splitter
    
    Returns:
        Geconfigureerde QSplitter
    """
    splitter = QSplitter(orientation)
    
    splitter.setStyleSheet("""
        QSplitter::handle {
            background-color: #cccccc;
        }
        QSplitter::handle:horizontal {
            width: 2px;
        }
        QSplitter::handle:vertical {
            height: 2px;
        }
        QSplitter::handle:hover {
            background-color: #007bff;
        }
    """)
    
    return splitter

def apply_dark_theme(app: QApplication):
    """
    Pas een donker thema toe op de applicatie
    
    Args:
        app: QApplication instantie
    """
    dark_palette = QPalette()
    
    # Kleuren instellen
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
    dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    
    app.setPalette(dark_palette)
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")

def apply_light_theme(app: QApplication):
    """
    Pas een licht thema toe op de applicatie
    
    Args:
        app: QApplication instantie
    """
    light_palette = QPalette()
    
    # Kleuren instellen
    light_palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
    light_palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
    light_palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
    light_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(245, 245, 245))
    light_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
    light_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
    light_palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
    light_palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
    light_palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
    light_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
    light_palette.setColor(QPalette.ColorRole.Link, QColor(0, 0, 255))
    light_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    light_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    
    app.setPalette(light_palette)
    app.setStyleSheet("")

def show_info_dialog(parent: QWidget, title: str, message: str):
    """
    Toon een informatie dialoog
    
    Args:
        parent: Parent widget
        title: Titel van de dialoog
        message: Bericht om te tonen
    """
    QMessageBox.information(parent, title, message)

def show_warning_dialog(parent: QWidget, title: str, message: str):
    """
    Toon een waarschuwing dialoog
    
    Args:
        parent: Parent widget
        title: Titel van de dialoog
        message: Bericht om te tonen
    """
    QMessageBox.warning(parent, title, message)

def show_error_dialog(parent: QWidget, title: str, message: str):
    """
    Toon een fout dialoog
    
    Args:
        parent: Parent widget
        title: Titel van de dialoog
        message: Bericht om te tonen
    """
    QMessageBox.critical(parent, title, message)

def show_question_dialog(parent: QWidget, title: str, message: str) -> bool:
    """
    Toon een vraag dialoog
    
    Args:
        parent: Parent widget
        title: Titel van de dialoog
        message: Bericht om te tonen
    
    Returns:
        True als gebruiker "Ja" kiest, False anders
    """
    reply = QMessageBox.question(parent, title, message, 
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    return reply == QMessageBox.StandardButton.Yes

def open_file_dialog(parent: QWidget, title: str = "Open Bestand",
                    filter: str = "Alle bestanden (*.*)") -> Optional[str]:
    """
    Open een bestand dialoog
    
    Args:
        parent: Parent widget
        title: Titel van de dialoog
        filter: Bestand filter
    
    Returns:
        Geselecteerd bestand pad of None
    """
    file_path, _ = QFileDialog.getOpenFileName(parent, title, "", filter)
    return file_path if file_path else None

def open_files_dialog(parent: QWidget, title: str = "Open Bestanden",
                     filter: str = "Alle bestanden (*.*)") -> List[str]:
    """
    Open een meerdere bestanden dialoog
    
    Args:
        parent: Parent widget
        title: Titel van de dialoog
        filter: Bestand filter
    
    Returns:
        Lijst van geselecteerde bestand paden
    """
    file_paths, _ = QFileDialog.getOpenFileNames(parent, title, "", filter)
    return file_paths

def save_file_dialog(parent: QWidget, title: str = "Sla Bestand Op",
                    filter: str = "Alle bestanden (*.*)") -> Optional[str]:
    """
    Open een sla bestand op dialoog
    
    Args:
        parent: Parent widget
        title: Titel van de dialoog
        filter: Bestand filter
    
    Returns:
        Geselecteerd bestand pad of None
    """
    file_path, _ = QFileDialog.getSaveFileName(parent, title, "", filter)
    return file_path if file_path else None

def open_directory_dialog(parent: QWidget, title: str = "Selecteer Directory") -> Optional[str]:
    """
    Open een directory selectie dialoog
    
    Args:
        parent: Parent widget
        title: Titel van de dialoog
    
    Returns:
        Geselecteerde directory pad of None
    """
    directory = QFileDialog.getExistingDirectory(parent, title)
    return directory if directory else None
