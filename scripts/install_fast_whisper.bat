@echo off
echo 🤖 Fast Whisper Installatie Script
echo ======================================

REM Controleer of Python beschikbaar is
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python niet gevonden!
    echo 💡 Installeer Python en voer dit script opnieuw uit
    pause
    exit /b 1
)

echo ✅ Python gevonden
echo.

REM Voer het Python install script uit
echo 🚀 Start Fast Whisper installatie...
python scripts\install_fast_whisper.py

if errorlevel 1 (
    echo.
    echo ❌ Fast Whisper installatie gefaald!
    echo 💡 Controleer je internetverbinding en probeer opnieuw
    pause
    exit /b 1
)

echo.
echo 🎉 Fast Whisper installatie voltooid!
echo 💡 Je kunt nu Fast Whisper gebruiken in Magic Time Studio
echo 💡 Test met: python tests\test_fast_whisper.py
pause 