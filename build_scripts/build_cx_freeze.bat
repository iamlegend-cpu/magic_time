@echo off
echo ========================================
echo Magic Time Studio - cx_Freeze Build
echo ========================================
echo.

REM Activeer virtual environment
echo [1/4] Activeer virtual environment...
call pyqt_venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Kan virtual environment niet activeren!
    pause
    exit /b 1
)

REM Controleer of cx_Freeze geïnstalleerd is
echo [2/4] Controleer cx_Freeze installatie...
python -c "import cx_Freeze" 2>nul
if errorlevel 1 (
    echo ERROR: cx_Freeze is niet geïnstalleerd!
    echo Installeer het eerst met: pip install cx_Freeze
    pause
    exit /b 1
)

REM Verwijder oude build directory
echo [3/4] Verwijder oude build directory...
if exist "build_cx_freeze" (
    rmdir /s /q "build_cx_freeze"
    echo Oude build directory verwijderd.
)

REM Start build proces
echo [4/4] Start cx_Freeze build proces...
echo Dit kan enkele minuten duren...
echo.
python setup_cx_freeze.py build

if errorlevel 1 (
    echo.
    echo ERROR: Build proces mislukt!
    pause
    exit /b 1
) else (
    echo.
    echo ========================================
    echo BUILD SUCCESVOL VOLTOOID!
    echo ========================================
    echo.
    echo Je executable staat in: build_cx_freeze\
    echo Start het programma met: build_cx_freeze\Magic_Time_Studio.exe
    echo.
)

pause
