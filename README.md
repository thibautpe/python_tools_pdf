# Fusion PDF avec Sommaire et Signets

Ce script Python fusionne tous les PDF d'un dossier, ajoute une page de sommaire paginée, et crée des signets cliquables pour chaque section.

## Fonctionnalités

- Fusionne tous les PDF d'un dossier (le premier est la couverture).
- Génère un sommaire paginé (table des matières).
- Ajoute des signets/outlines cliquables pour chaque section.
- Utilise les polices Verdana (Windows).

## Utilisation

1. **Installer les dépendances** :
   ```
   pip install PyPDF2 reportlab toml
   ```

2. **Configurer les chemins** :  
   Modifiez `config.toml` pour indiquer le dossier source et le fichier de sortie.

3. **Lancer le script** :
   ```
   python merge_and_toc_pdf.py
   ```

## Exécution automatisée (Windows PowerShell)

Vous pouvez automatiser l'installation et l'exécution avec le script PowerShell fourni :

```powershell
.\run_all.ps1
```

Ce script :
- Installe les dépendances nécessaires (`PyPDF2`, `reportlab`, `toml`)
- Lance automatiquement le script principal `merge_and_toc_pdf.py`

## Configuration

Le fichier `config.toml` permet de définir :
- Le dossier contenant les PDF à fusionner (`input_folder`)
- Le chemin du PDF de sortie (`output_file`)

## Dépendances

- PyPDF2
- reportlab
- toml

## Résultat

- Le PDF fusionné commence par la couverture, puis le sommaire, puis les sections.
- Les signets (dans la barre latérale du lecteur PDF) permettent d'accéder directement à chaque section.

---