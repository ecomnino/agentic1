# Stop bij fouten
$ErrorActionPreference = "Stop"

$VENV_DIR = ".venv"

# Check of script gesourced wordt (dot-sourcing in PowerShell)
if ($MyInvocation.InvocationName -ne ".") {
    Write-Host "⚠️  Run dit script met: . .\scriptnaam.ps1"
    exit 1
}

# Maak venv als die nog niet bestaat
if (!(Test-Path $VENV_DIR)) {
    Write-Host "🔧 Virtual environment aanmaken..."
    python -m venv $VENV_DIR
} else {
    Write-Host "✅ Virtual environment bestaat al."
}

# Activeer venv
Write-Host "🚀 Virtual environment activeren..."
& "$VENV_DIR\Scripts\Activate.ps1"

# Installeer dependencies (optioneel)
if (Test-Path "requirements.txt") {
    Write-Host "📦 Dependencies installeren..."
    pip install -r requirements.txt
}

Write-Host "🎉 Klaar! Je venv is actief."