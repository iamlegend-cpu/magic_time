@echo off
REM Whisper Type Switcher voor Windows
REM Gebruik: switch_whisper_type.bat [standard|fast|status]

echo 🤖 Whisper Type Switcher
echo ================================

if "%1"=="" (
    echo Gebruik:
    echo   switch_whisper_type.bat standard
    echo   switch_whisper_type.bat fast
    echo   switch_whisper_type.bat status
    echo.
    echo 💡 Opties:
    echo   • standard: Originele OpenAI Whisper
    echo   • fast: Geoptimaliseerde Fast Whisper (6.8x sneller)
    echo   • status: Toon huidige configuratie
    goto :eof
)

if "%1"=="status" (
    python scripts/switch_whisper_type.py status
) else if "%1"=="standard" (
    echo 🔄 Wissel naar Standaard Whisper...
    python scripts/switch_whisper_type.py standard
) else if "%1"=="fast" (
    echo 🚀 Wissel naar Fast Whisper...
    python scripts/switch_whisper_type.py fast
) else (
    echo ❌ Onbekend commando: %1
    echo 💡 Gebruik 'standard', 'fast', of 'status'
)

pause 