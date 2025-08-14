@echo off
echo ========================================
echo Magic Time Studio - Installer Builder
echo ========================================
echo.

REM Controleer of Inno Setup is geïnstalleerd (probeer beide namen)
set "ISCC_PATH="
where iscc >nul 2>&1
if %errorlevel% equ 0 (
    set "ISCC_PATH=iscc"
    echo Inno Setup gevonden: iscc
) else (
    where ISCC >nul 2>&1
    if %errorlevel% equ 0 (
        set "ISCC_PATH=ISCC"
        echo Inno Setup gevonden: ISCC
    ) else (
        REM Probeer directe paden
        if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
            set "ISCC_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
            echo Inno Setup gevonden: %ISCC_PATH%
        ) else (
            if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
                set "ISCC_PATH=C:\Program Files\Inno Setup 6\ISCC.exe"
                echo Inno Setup gevonden: %ISCC_PATH%
            ) else (
                echo ERROR: Inno Setup is niet geïnstalleerd!
                echo.
                echo Download Inno Setup van: https://jrsoftware.org/isdl.php
                echo Installeer het en voer dit script opnieuw uit.
                echo.
                pause
                exit /b 1
            )
        )
    )
)

echo.

REM Maak installer directory aan
if not exist "installer" mkdir installer

REM Controleer of de dist directory bestaat
if not exist "dist\Magic_Time_Studio" (
    echo ERROR: Dist directory niet gevonden!
    echo.
    echo Bouw eerst de executable met: pyinstaller --clean magic_time_studio.spec
    echo.
    pause
    exit /b 1
)

echo Bouw installer...
echo.

REM Bouw de installer
"%ISCC_PATH%" Magic_Time_Studio_Setup.iss

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo Installer succesvol gebouwd!
    echo ========================================
    echo.
    echo Installer bestand: installer\Magic_Time_Studio_Setup_v3.0.exe
    echo.
    echo Je kunt nu de installer distribueren.
    echo.
) else (
    echo.
    echo ERROR: Installer bouw gefaald!
    echo.
    pause
    exit /b 1
)

pause
