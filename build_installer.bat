@echo off
echo ========================================
echo Magic Time Studio Installer Builder
echo ========================================
echo.

REM Controleer of we in de juiste directory zijn
if not exist "magic_time_studio.spec" (
    echo ERROR: magic_time_studio.spec niet gevonden!
    echo Zorg ervoor dat je in de project root directory bent.
    pause
    exit /b 1
)

echo Stap 1: Activeer PyQt6 environment...
call .\pyqt6_env\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Kon PyQt6 environment niet activeren!
    pause
    exit /b 1
)

echo Stap 2: Bouw executable met PyInstaller...
pyinstaller magic_time_studio.spec --noconfirm
if errorlevel 1 (
    echo ERROR: PyInstaller build gefaald!
    pause
    exit /b 1
)

echo Stap 3: Controleer of executable is gebouwd...
if not exist "dist\Magic_Time_Studio\Magic_Time_Studio.exe" (
    echo ERROR: Executable niet gevonden in dist\Magic_Time_Studio\
    pause
    exit /b 1
)

echo Stap 4: Controleer of Inno Setup beschikbaar is...
where iscc >nul 2>&1
if errorlevel 1 (
    echo WAARSCHUWING: Inno Setup Compiler (iscc) niet gevonden in PATH
    echo.
    echo Om de installer te maken:
    echo 1. Download Inno Setup van: https://jrsoftware.org/isdl.php
    echo 2. Installeer Inno Setup
    echo 3. Voeg Inno Setup bin directory toe aan PATH
    echo 4. Run dit script opnieuw
    echo.
    echo Of compileer handmatig:
    echo - Open installer_setup.iss in Inno Setup Compiler
    echo - Klik op Compile
    echo.
    pause
    exit /b 0
)

echo Stap 5: Maak installer directory...
if not exist "installer_output" mkdir installer_output

echo Stap 6: Compileer installer met Inno Setup...
iscc installer_setup.iss
if errorlevel 1 (
    echo ERROR: Inno Setup compilation gefaald!
    pause
    exit /b 1
)

echo Stap 7: Controleer of installer is gemaakt...
if exist "installer_output\Magic_Time_Studio_Setup.exe" (
    echo.
    echo ========================================
    echo SUCCESS: Installer succesvol gemaakt!
    echo ========================================
    echo.
    echo Installer locatie: installer_output\Magic_Time_Studio_Setup.exe
    echo.
    echo Je kunt nu de installer distribueren.
    echo.
) else (
    echo ERROR: Installer niet gevonden in installer_output\
    pause
    exit /b 1
)

echo.
echo Build proces voltooid!
pause 