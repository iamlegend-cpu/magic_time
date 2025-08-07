@echo off
echo 🔧 Start Magic Time Studio in Debug Mode...
echo.

REM Zet environment variables voor debug
set LOG_LEVEL=DEBUG
set LOG_TO_FILE=true

echo 📋 Environment variables:
echo   LOG_LEVEL=%LOG_LEVEL%
echo   LOG_TO_FILE=%LOG_TO_FILE%
echo.

REM Start de applicatie
cd /d "%~dp0.."
python magic_time_studio/run.py

pause 