# Fast Whisper Installatie Script voor PowerShell
Write-Host "🤖 Fast Whisper Installatie Script" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Controleer of Python beschikbaar is
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python gevonden: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python niet gevonden!" -ForegroundColor Red
    Write-Host "💡 Installeer Python en voer dit script opnieuw uit" -ForegroundColor Yellow
    Read-Host "Druk op Enter om af te sluiten"
    exit 1
}

Write-Host ""

# Voer het Python install script uit
Write-Host "🚀 Start Fast Whisper installatie..." -ForegroundColor Yellow
try {
    python scripts\install_fast_whisper.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "🎉 Fast Whisper installatie voltooid!" -ForegroundColor Green
        Write-Host "💡 Je kunt nu Fast Whisper gebruiken in Magic Time Studio" -ForegroundColor Cyan
        Write-Host "💡 Test met: python tests\test_fast_whisper.py" -ForegroundColor Cyan
    } else {
        Write-Host ""
        Write-Host "❌ Fast Whisper installatie gefaald!" -ForegroundColor Red
        Write-Host "💡 Controleer je internetverbinding en probeer opnieuw" -ForegroundColor Yellow
    }
} catch {
    Write-Host ""
    Write-Host "❌ Fout bij uitvoeren install script: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Read-Host "Druk op Enter om af te sluiten" 