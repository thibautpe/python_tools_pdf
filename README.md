# Fusion PDF avec Sommaire et Signets

Ce script Python fusionne tous les PDF d'un dossier, ajoute une page de sommaire paginée, et crée des signets cliquables pour chaque section.

## Fonctionnalités

- Fusionne tous les PDF d'un dossier (le premier est la couverture).
- Génère un sommaire paginé (table des matières).
- Ajoute des signets/outlines cliquables pour chaque section.
- Utilise les polices Verdana (Windows).

## Utilisation

1. Installation des dépendances avec un environnement virtuel (Windows PowerShell)

Vous pouvez automatiser la création de l'environnement virtuel et l'installation des dépendances grâce au script fourni dans le dossier `scripts` :

```powershell
.\scripts\venv.ps1
```

Ce script va :
- Créer un environnement virtuel Python dans le dossier `venv` (s'il n'existe pas déjà)
- Activer cet environnement virtuel
- Installer toutes les dépendances listées dans `requirements.txt`

Après exécution, vous pouvez lancer le script principal normalement :

```powershell
python merge_and_toc_pdf.py
```

Pour désactiver l'environnement virtuel, tapez simplement :
```powershell
deactivate
```

---

## Exécution automatisée (Windows PowerShell)

Vous pouvez automatiser l'installation **et** l'exécution complète avec le script PowerShell suivant, également situé dans le dossier `scripts` :

```powershell
.\scripts\run_all.ps1
```

Ce script :
- Installe les dépendances nécessaires (`PyPDF2`, `reportlab`, `toml`...)
- Lance automatiquement le script principal `merge_and_toc_pdf.py`

2. **Configurer les chemins** :  
   Modifiez `config.toml` pour indiquer le dossier source et le fichier de sortie.

3. **Lancer le script** :
   ```
   python merge_and_toc_pdf.py
   ```

   ```

## Configuration

Le fichier `config.toml` permet de définir :
- Le dossier contenant les PDF à fusionner (`input_folder`)
- Le chemin du PDF de sortie (`output_file`)

## Dépendances

- **PyPDF2** : Manipulation et fusion de fichiers PDF.
- **reportlab** : Génération de PDF dynamiques (pour créer le sommaire paginé).
- **toml** : Lecture des fichiers de configuration au format TOML.
- **pytest** : Exécution des tests automatisés.
- **nox** : Gestion automatisée des environnements de test et des sessions CI.

## Résultat

- Le PDF fusionné commence par la couverture, puis le sommaire, puis les sections.
- Les signets (dans la barre latérale du lecteur PDF) permettent d'accéder directement à chaque section.

## À propos de nox

**nox** est un outil d'automatisation qui permet de gérer et d'exécuter facilement des sessions de tests, de linting ou d'autres tâches dans des environnements virtuels isolés.  
Dans ce projet, nox est utilisé pour lancer automatiquement les tests (`pytest`) dans un environnement propre, sans polluer votre installation Python principale.  
Il suffit d'exécuter la commande `nox` pour que toutes les dépendances nécessaires soient installées dans un environnement temporaire, puis que les tests soient lancés.  
Cela garantit la reproductibilité et la fiabilité des tests, que ce soit en local ou dans un pipeline CI.

