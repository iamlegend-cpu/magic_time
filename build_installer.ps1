# Magic Time Studio - Installer Builder (PowerShell)
# ================================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Magic Time Studio - Installer Builder" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Controleer of Inno Setup is geïnstalleerd (probeer beide namen)
$isccPath = $null

try {
    # Probeer eerst iscc (kleine letters)
    $isccPath = Get-Command iscc -ErrorAction Stop
    Write-Host "Inno Setup gevonden: $($isccPath.Source)" -ForegroundColor Green
} catch {
    try {
        # Probeer dan ISCC (hoofdletters)
        $isccPath = Get-Command ISCC -ErrorAction Stop
        Write-Host "Inno Setup gevonden: $($isccPath.Source)" -ForegroundColor Green
    } catch {
        # Probeer directe paden
        $possiblePaths = @(
            "C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
            "C:\Program Files\Inno Setup 6\ISCC.exe"
        )
        
        foreach ($path in $possiblePaths) {
            if (Test-Path $path) {
                $isccPath = $path
                Write-Host "Inno Setup gevonden: $isccPath" -ForegroundColor Green
                break
            }
        }
        
        if (-not $isccPath) {
            Write-Host "ERROR: Inno Setup is niet geïnstalleerd!" -ForegroundColor Red
            Write-Host ""
            Write-Host "Download Inno Setup van: https://jrsoftware.org/isdl.php" -ForegroundColor Yellow
            Write-Host "Installeer het en voer dit script opnieuw uit." -ForegroundColor Yellow
            Write-Host ""
            Read-Host "Druk op Enter om af te sluiten"
            exit 1
        }
    }
}

Write-Host ""

# Maak installer directory aan
if (-not (Test-Path "installer")) {
    New-Item -ItemType Directory -Path "installer" | Out-Null
    Write-Host "Installer directory aangemaakt." -ForegroundColor Green
}

# Controleer of de dist directory bestaat
if (-not (Test-Path "dist\Magic_Time_Studio")) {
    Write-Host "ERROR: Dist directory niet gevonden!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Bouw eerst de executable met: pyinstaller --clean magic_time_studio.spec" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Druk op Enter om af te sluiten"
    exit 1
}

Write-Host "Bouw installer..." -ForegroundColor Yellow
Write-Host ""

# Bouw de installer
try {
    if ($isccPath -is [System.Management.Automation.CommandInfo]) {
        # Het is een command in PATH
        $process = Start-Process -FilePath $isccPath.Source -ArgumentList "Magic_Time_Studio_Setup.iss" -Wait -PassThru -NoNewWindow
    } else {
        # Het is een direct pad
        $process = Start-Process -FilePath $isccPath -ArgumentList "Magic_Time_Studio_Setup.iss" -Wait -PassThru -NoNewWindow
    }
    
    if ($process.ExitCode -eq 0) {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "Installer succesvol gebouwd!" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Installer bestand: installer\Magic_Time_Studio_Setup_v3.0.exe" -ForegroundColor Green
        Write-Host ""
        Write-Host "Je kunt nu de installer distribueren." -ForegroundColor Green
        Write-Host ""
        
        # Open de installer directory
        if (Test-Path "installer") {
            Write-Host "Open installer directory..." -ForegroundColor Yellow
            Start-Process "explorer.exe" -ArgumentList "installer"
        }
    } else {
        Write-Host ""
        Write-Host "ERROR: Installer bouw gefaald!" -ForegroundColor Red
        Write-Host "Exit code: $($process.ExitCode)" -ForegroundColor Red
        Write-Host ""
        Read-Host "Druk op Enter om af te sluiten"
        exit 1
    }
} catch {
    Write-Host ""
    Write-Host "ERROR: Installer bouw gefaald!" -ForegroundColor Red
    Write-Host "Fout: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Read-Host "Druk op Enter om af te sluiten"
    exit 1
}

Write-Host ""
Read-Host "Druk op Enter om af te sluiten"
