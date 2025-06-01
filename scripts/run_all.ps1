# Installe les dépendances et lance le script principal

Write-Host "Installation des dépendances Python..."

if (Test-Path ".\requirements.txt") {
    pip install -r requirements.txt
} elseif (Test-Path ".\pyproject.toml") {
    if (-not (Get-Command poetry -ErrorAction SilentlyContinue)) {
        Write-Host "Poetry n'est pas installé. Installation de Poetry..."
        pip install poetry
    }
    Write-Host "Installation des dépendances via Poetry..."
    poetry install
} else {
    pip install PyPDF2 reportlab toml
}

Write-Host "Exécution du script de fusion PDF..."
python merge_and_toc_pdf.py

Write-Host "✅ Terminé."