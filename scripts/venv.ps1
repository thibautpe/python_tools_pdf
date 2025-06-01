# venv.ps1
# Crée et active un venv, puis installe les dépendances

# 1. Créer le venv s'il n'existe pas
if (-not (Test-Path "venv")) {
    python -m venv venv
    Write-Host "✅ Environnement virtuel créé."
} else {
    Write-Host "ℹ️  Le venv existe déjà."
}

# 2. Activer le venv
& .\venv\Scripts\Activate.ps1
Write-Host "✅ venv activé."

# 3. Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt
Write-Host "✅ Dépendances installées."