# Start Magic Time Studio in Debug Mode
Write-Host "🔧 Start Magic Time Studio in Debug Mode..." -ForegroundColor Green
Write-Host ""

# Zet environment variables voor debug
$env:LOG_LEVEL = "DEBUG"
$env:LOG_TO_FILE = "true"

Write-Host "📋 Environment variables:" -ForegroundColor Yellow
Write-Host "  LOG_LEVEL: $env:LOG_LEVEL" -ForegroundColor Cyan
Write-Host "  LOG_TO_FILE: $env:LOG_TO_FILE" -ForegroundColor Cyan
Write-Host ""

# Start de applicatie
Set-Location $PSScriptRoot/..
python magic_time_studio/run.py

Read-Host "Druk op Enter om af te sluiten..." 