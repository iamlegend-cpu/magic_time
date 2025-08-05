@echo off
echo Starting Magic Time Studio PyQt6...
echo.

REM Activeer virtual environment
call pyqt6_env\Scripts\activate.bat

REM Start de PyQt6 versie
python magic_time_studio\run.py

pause 