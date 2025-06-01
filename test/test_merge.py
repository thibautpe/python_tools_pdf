import os
import subprocess
import toml
import sys
from PyPDF2 import PdfReader

def test_merged_pdf_exists():
    """
    Teste la création d'un fichier PDF fusionné en utilisant un script externe.

    Ce test charge une configuration de test, prépare le dossier de sortie, supprime le fichier de sortie existant si nécessaire,
    puis exécute le script `merge_and_toc_pdf.py` avec le bon interpréteur Python. Il vérifie ensuite que le script s'exécute sans erreur,
    que le fichier PDF fusionné est bien créé, et que le nombre de pages est correct.
    """
    # Charger la config de test
    config_path = "test/config_test.toml"
    config = toml.load(config_path)
    input_dir = config["pdf"]["input_folder"]
    output_dir = config["pdf"]["output_folder"]
    output_file = config["pdf"]["output_file"]
    output_path = os.path.join(output_dir, output_file)

    # Créer le dossier de sortie s'il n'existe pas
    os.makedirs(output_dir, exist_ok=True)

    # Supprimer le fichier de sortie s'il existe déjà
    if os.path.exists(output_path):
        os.remove(output_path)

    # Lancer le script avec le bon interpréteur Python 
    result = subprocess.run(
        [sys.executable, "merge_and_toc_pdf.py", config_path],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    print(result.stderr)
    assert result.returncode == 0, "Le script a échoué"

    # Vérifier que le fichier de sortie a été créé
    assert os.path.exists(output_path), "Le fichier PDF fusionné n'a pas été créé"

    # Vérifier le nombre de pages
    pdf_files = sorted([
        os.path.join(input_dir, f)
        for f in os.listdir(input_dir)
        if f.lower().endswith(".pdf")
    ])
    total_pages = sum(len(PdfReader(f).pages) for f in pdf_files)
    expected_pages = total_pages + 1  # +1 pour la page de sommaire

    merged_pdf = PdfReader(output_path)
    merged_pages = len(merged_pdf.pages)
    assert merged_pages == expected_pages, (
        f"Le PDF fusionné contient {merged_pages} pages, attendu : {expected_pages}"
    )