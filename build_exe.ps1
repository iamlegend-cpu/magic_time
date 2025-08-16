# Magic Time Studio - Exe Builder (PowerShell)
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Magic Time Studio - Exe Builder" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Stap 1: Activeer virtual environment
Write-Host "[1/4] Activeer virtual environment..." -ForegroundColor Yellow
& "pyqt_venv\Scripts\Activate.ps1"

# Stap 2: Controleer PyInstaller
Write-Host "[2/4] Controleer PyInstaller..." -ForegroundColor Yellow
try {
    python -c "import PyInstaller" 2>$null
    Write-Host "✅ PyInstaller gevonden" -ForegroundColor Green
} catch {
    Write-Host "PyInstaller niet gevonden - installeer..." -ForegroundColor Red
    pip install PyInstaller
}

# Stap 3: Bouw de exe
Write-Host "[3/4] Bouw Magic Time Studio exe..." -ForegroundColor Yellow
pyinstaller magic_time_studio.spec --noconfirm

# Stap 4: Controleer resultaat
Write-Host "[4/4] Controleer resultaat..." -ForegroundColor Yellow
if (Test-Path "dist\Magic_Time_Studio\Magic_Time_Studio.exe") {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✅ EXE SUCCESVOL GEBOUWD!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Locatie: dist\Magic_Time_Studio\" -ForegroundColor White
    Write-Host "Bestand: Magic_Time_Studio.exe" -ForegroundColor White
    Write-Host ""
    Write-Host "Je kunt nu de exe starten!" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "❌ EXE BOUWEN GEFAALD!" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Controleer de foutmeldingen hierboven." -ForegroundColor White
    Write-Host ""
}

Read-Host "Druk op Enter om af te sluiten"
