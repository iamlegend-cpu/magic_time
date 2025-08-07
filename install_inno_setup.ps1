Write-Host "Inno Setup Compiler Installer" -ForegroundColor Green

$innoSetupPath = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if (Test-Path $innoSetupPath) {
    Write-Host "Inno Setup is al geïnstalleerd!" -ForegroundColor Green
    exit 0
}

$downloadUrl = "https://files.jrsoftware.org/is/6/innosetup-6.2.2.exe"
$installerPath = "$env:TEMP\innosetup-6.2.2.exe"

Write-Host "Downloaden van Inno Setup..." -ForegroundColor Yellow
Invoke-WebRequest -Uri $downloadUrl -OutFile $installerPath

Write-Host "Installeren..." -ForegroundColor Yellow
Start-Process -FilePath $installerPath -ArgumentList "/VERYSILENT /NORESTART" -Wait

if (Test-Path $innoSetupPath) {
    Write-Host "Installatie succesvol!" -ForegroundColor Green
    Remove-Item $installerPath -Force
} else {
    Write-Host "Installatie mislukt!" -ForegroundColor Red
} 