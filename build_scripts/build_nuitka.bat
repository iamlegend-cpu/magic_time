@echo off
REM ========================================
REM Magic Time Studio - Nuitka Build Script
REM ========================================

echo ========================================
echo Magic Time Studio - Nuitka Build Script
echo ========================================
echo.

REM Controleer of Python beschikbaar is
echo [1/5] Controleer dependencies...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is niet gevonden!
    echo Installeer Python of voeg het toe aan PATH
    pause
    exit /b 1
)
echo ✅ Python gevonden
echo.

REM Detecteer en configureer CUDA
echo [2/5] Detecteer en configureer CUDA...
set CUDA_FOUND=0

REM Controleer standaard CUDA locaties
if exist "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA" (
    for /d %%i in ("C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v*") do (
        if exist "%%i\bin" (
            set "PATH=%%i\bin;%%i\lib\x64;%PATH%"
            echo ✅ CUDA gevonden: %%i
            echo    Binaries toegevoegd aan PATH: %%i\bin
            set CUDA_FOUND=1
            goto :cuda_found
        )
    )
)

if exist "C:\CUDA" (
    for /d %%i in ("C:\CUDA\v*") do (
        if exist "%%i\bin" (
            set "PATH=%%i\bin;%%i\lib\x64;%PATH%"
            echo ✅ CUDA gevonden: %%i
            echo    Binaries toegevoegd aan PATH: %%i\bin
            set CUDA_FOUND=1
            goto :cuda_found
        )
    )
)

if exist "C:\Program Files\CUDA" (
    for /d %%i in ("C:\Program Files\CUDA\v*") do (
        if exist "%%i\bin" (
            set "PATH=%%i\bin;%%i\lib\x64;%PATH%"
            echo ✅ CUDA gevonden: %%i
            echo    Binaries toegevoegd aan PATH: %%i\bin
            set CUDA_FOUND=1
            goto :cuda_found
        )
    )
)

:cuda_found
if %CUDA_FOUND%==0 (
    echo ⚠️  CUDA Toolkit niet gevonden in standaard locaties
    echo    Als je CUDA Toolkit hebt geïnstalleerd, voeg het handmatig toe aan PATH
) else (
    echo    CUDA libraries toegevoegd aan PATH
)
echo.

REM Activeer virtual environment
echo [3/5] Activeer virtual environment...
if exist "pyqt_venv\Scripts\activate.bat" (
    call "pyqt_venv\Scripts\activate.bat"
    echo ✅ Virtual environment geactiveerd
) else (
    echo ❌ Virtual environment niet gevonden: pyqt_venv
    pause
    exit /b 1
)
echo.

REM Controleer PySide6 installatie
echo [4/5] Controleer PySide6 installatie...
python -c "import PySide6; print('PySide6 gevonden')" >nul 2>&1
if errorlevel 1 (
    echo ❌ PySide6 niet gevonden in virtual environment
    echo Installeer met: pip install PySide6
    pause
    exit /b 1
)
echo ✅ PySide6 gevonden
echo.

REM Controleer Nuitka installatie
echo [5/5] Controleer Nuitka installatie...
python -c "import nuitka; print('Nuitka gevonden')" >nul 2>&1
if errorlevel 1 (
    echo ❌ Nuitka niet gevonden in virtual environment
    echo Installeer met: pip install nuitka
    pause
    exit /b 1
)
echo ✅ Nuitka gevonden
echo.

echo 🚀 Start Nuitka build...
echo.

REM Start Nuitka build (met FFmpeg support en transformers fix)
python -m nuitka ^
    --standalone ^
    --enable-plugin=pyside6 ^
    --disable-plugin=anti-bloat ^
    --no-pyi-file ^
    --assume-yes-for-downloads ^
    --include-package-data=transformers ^
    --verbose ^
    --show-progress ^
    --show-memory ^
    --include-package=torch ^
    --include-package=torchaudio ^
    --include-package=whisperx ^
    --include-package=librosa ^
    --include-package=transformers ^
    --include-package=speechbrain ^
    --include-package=pyannote.audio ^
    --include-package=accelerate ^
    --include-package=onnxruntime ^
    --include-package=openai-whisper ^
    --include-package=faster-whisper ^
    --include-data-files=assets/ffmpeg.exe=ffmpeg.exe ^
    --output-dir=build_nuitka ^
    --output-filename=Magic_Time_Studio.exe ^
    magic_time_studio\run.py

if errorlevel 1 (
    echo.
    echo ❌ Build gefaald!
) else (
    echo.
    echo ✅ Build voltooid! Executable staat in: build_nuitka\Magic_Time_Studio.exe
)
echo.
pause
