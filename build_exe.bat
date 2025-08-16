@echo off
echo ========================================
echo Magic Time Studio - Exe Builder
echo ========================================
echo.

REM Activeer virtual environment
echo [1/4] Activeer virtual environment...
call pyqt_venv\Scripts\activate.bat

REM Controleer of PyInstaller geïnstalleerd is
echo [2/4] Controleer PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller niet gevonden - installeer...
    pip install PyInstaller
)

REM Bouw de exe
echo [3/4] Bouw Magic Time Studio exe...
pyinstaller magic_time_studio.spec --noconfirm

REM Controleer resultaat
echo [4/4] Controleer resultaat...
if exist "dist\Magic_Time_Studio\Magic_Time_Studio.exe" (
    echo.
    echo ========================================
    echo ✅ EXE SUCCESVOL GEBOUWD!
    echo ========================================
    echo.
    echo Locatie: dist\Magic_Time_Studio\
    echo Bestand: Magic_Time_Studio.exe
    echo.
    echo Je kunt nu de exe starten!
    echo.
    pause
) else (
    echo.
    echo ========================================
    echo ❌ EXE BOUWEN GEFAALD!
    echo ========================================
    echo.
    echo Controleer de foutmeldingen hierboven.
    echo.
    pause
)
