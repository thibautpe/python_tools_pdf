# Installe les dépendances et lance le script principal

Write-Host "Installation des dépendances Python..."
pip install PyPDF2 reportlab toml

Write-Host "Exécution du script de fusion PDF..."
python merge_and_toc_pdf.py

Write-Host "✅ Terminé."