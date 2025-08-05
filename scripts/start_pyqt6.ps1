# PowerShell script om Magic Time Studio PyQt6 te starten

Write-Host "Starting Magic Time Studio PyQt6..." -ForegroundColor Green
Write-Host ""

# Activeer virtual environment
& "pyqt6_env\Scripts\Activate.ps1"

# Start de PyQt6 versie
python magic_time_studio\run.py

Read-Host "Press Enter to continue..." 