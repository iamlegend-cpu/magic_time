"""
UI Controls Mapping voor Magic Time Studio
Bevat een overzicht van alle knoppen en besturingselementen georganiseerd per module
"""

# Export de mapping voor gebruik in andere modules
UI_CONTROLS_MAPPING = {
    "files_panel": [
        "add_file_btn", "remove_btn", "add_folder_btn", "clear_btn",
        "file_list_widget", "processing_status_label", "files_count_label", "current_file_label"
    ],
    "processing_panel": [
        "start_btn", "stop_btn", "progress_bar", "console_output", "log_output"
    ],
    "settings_panel": [
        "translator_combo", "model_combo", "language_combo",
        "preserve_subtitles_combo", "vad_checkbox"
    ],
    "batch_panel": [
        "batch_queue_manager"
    ],
    "batch_queue": [
        "max_concurrent_spin", "auto_start_check", "continue_on_error_check",
        "start_btn", "stop_btn", "clear_btn", "queue_list"
    ],
    "whisper_selector": [
        "type_combo", "model_combo", "load_model_btn", "model_status_label"
    ],
    "charts_panel": [
        "tab_widget", "system_monitor", "performance_chart"
    ],
    "system_monitor": [
        "cpu_chart", "memory_chart", "gpu_chart", "cpu_progress", "memory_progress", "gpu_progress"
    ],
    "performance_chart": [
        "io_chart", "network_chart", "io_label", "network_label", "uptime_label"
    ],
    "completed_files_panel": [
        "completed_list_widget", "clear_btn"
    ],
    "menu_manager": [
        "file_menu", "processing_menu", "view_menu", "settings_menu", "tools_menu", "help_menu"
    ],
    "config_window": [
        "general_tab", "processing_tab", "translator_tab", "interface_tab",
        "theme_tab", "advanced_tab", "plugins_tab", "save_btn", "cancel_btn", "reset_btn"
    ],
    "plugin_manager": [
        "plugins_list", "refresh_plugins_btn", "enable_plugin_btn", "disable_plugin_btn"
    ],
    "audio_analyzer_plugin": [
        "analysis_type_combo", "file_selector", "analyze_btn", "progress_bar", "results_widget"
    ],
    "batch_processor_plugin": [
        "add_files_btn", "add_folder_btn", "clear_btn", "start_processing_btn"
    ],
    "log_viewer": [
        "clear_button", "auto_scroll_button", "log_output"
    ]
}

def get_controls_for_module(module_name: str) -> list:
    """Haal alle knoppen op voor een specifieke module"""
    return UI_CONTROLS_MAPPING.get(module_name, [])

def get_all_controls() -> dict:
    """Haal alle knoppen op georganiseerd per module"""
    return UI_CONTROLS_MAPPING.copy()

def get_control_info(control_name: str) -> dict:
    """Haal informatie op over een specifieke knop"""
    for module, controls in UI_CONTROLS_MAPPING.items():
        if control_name in controls:
            return {
                "module": module,
                "control_name": control_name,
                "file_path": f"magic_time_studio/ui_pyqt6/components/{module}.py"
            }
    return None
