@echo off
echo Preparing Magic Time Studio for distribution...
echo.

REM Controleer of de build bestaat
if not exist "dist\Magic_Time_Studio\Magic_Time_Studio.exe" (
    echo ERROR: Executable not found! Please build first using build.bat
    pause
    exit /b 1
)

REM Maak distributie directory
set DIST_DIR=Magic_Time_Studio_Distribution
if exist "%DIST_DIR%" rmdir /s /q "%DIST_DIR%"
mkdir "%DIST_DIR%"

REM Kopieer executable en dependencies
echo Copying executable and dependencies...
xcopy "dist\Magic_Time_Studio\*" "%DIST_DIR%\" /E /I /Y

REM Kopieer README en installatie instructies
if exist "INSTALLER_README.md" copy "INSTALLER_README.md" "%DIST_DIR%\"
if exist "magic_time_studio\docs\README.md" copy "magic_time_studio\docs\README.md" "%DIST_DIR%\README.md"

REM Maak een snelle start script
echo @echo off > "%DIST_DIR%\Start_Magic_Time_Studio.bat"
echo cd /d "%%~dp0" >> "%DIST_DIR%\Start_Magic_Time_Studio.bat"
echo Magic_Time_Studio.exe >> "%DIST_DIR%\Start_Magic_Time_Studio.bat"
echo pause >> "%DIST_DIR%\Start_Magic_Time_Studio.bat"

echo.
echo Distribution package created in: %DIST_DIR%
echo.
echo Contents:
dir "%DIST_DIR%" /B
echo.
echo Ready for distribution!
pause
