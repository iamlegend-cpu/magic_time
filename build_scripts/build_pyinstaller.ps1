# Magic Time Studio - PyInstaller Build Script
# PowerShell script to build the executable

Write-Host "Starting Magic Time Studio PyInstaller build..." -ForegroundColor Green

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\pyqt_venv\Scripts\Activate.ps1"

# Clean previous build
if (Test-Path "build_pyinstaller") {
    Write-Host "Cleaning previous build..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force "build_pyinstaller"
}

# Verify directory structure
Write-Host "Verifying directory structure..." -ForegroundColor Yellow
if (-not (Test-Path "magic_time_studio\run.py")) {
    Write-Host "❌ ERROR: magic_time_studio\run.py not found!" -ForegroundColor Red
    Write-Host "💡 Make sure you're in the project root directory" -ForegroundColor Yellow
    Write-Host "💡 Current directory: $(Get-Location)" -ForegroundColor Yellow
    Write-Host "💡 Expected structure: magic_time\magic_time_studio\run.py" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ Directory structure verified" -ForegroundColor Green
Write-Host "📁 Project root: $(Get-Location)" -ForegroundColor Cyan
Write-Host "📁 Main script: magic_time_studio\run.py" -ForegroundColor Cyan

# Run PyInstaller build
Write-Host "Running PyInstaller build..." -ForegroundColor Yellow
python build_pyinstaller.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "Build completed successfully!" -ForegroundColor Green
    Write-Host "Executable location: build_pyinstaller\Magic_Time_Studio\Magic_Time_Studio.exe" -ForegroundColor Cyan
    
    # Test if executable exists
    if (Test-Path "build_pyinstaller\Magic_Time_Studio\Magic_Time_Studio.exe") {
        $fileSize = (Get-Item "build_pyinstaller\Magic_Time_Studio\Magic_Time_Studio.exe").Length / 1MB
        Write-Host "📦 Executable size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Green
        Write-Host "📁 Directory: build_pyinstaller\Magic_Time_Studio\" -ForegroundColor Cyan
    }
} else {
    Write-Host "Build failed with exit code: $LASTEXITCODE" -ForegroundColor Red
}

Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
