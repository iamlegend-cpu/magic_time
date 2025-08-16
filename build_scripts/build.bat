@echo off
echo Building Magic Time Studio...
echo.

REM Activeer virtual environment
call pyqt_venv\Scripts\activate.bat

REM Build met --clean en --noconfirm voor snelle builds
pyinstaller magic_time_studio.spec --clean --noconfirm

echo.
echo Build voltooid! Executable staat in dist\Magic_Time_Studio\
echo.
pause
