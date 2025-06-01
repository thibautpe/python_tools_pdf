import os
import subprocess

def test_merged_pdf_exists():
    # Préparer les chemins
    output_dir = "test/data/out"
    output_path = os.path.join(output_dir, "mergedpdf.pdf")
    config_path = "test/config_test.toml"

    # Créer le dossier de sortie s'il n'existe pas
    os.makedirs(output_dir, exist_ok=True)

    # Nettoyer le fichier de sortie s'il existe déjà
    if os.path.exists(output_path):
        os.remove(output_path)

    # Lancer le script avec le fichier de config de test
    result = subprocess.run(
        ["python", "merge_and_toc_pdf.py", config_path],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    print(result.stderr)
    assert result.returncode == 0, "Le script a échoué"

    # Vérifier que le fichier de sortie a été créé
    assert os.path.exists(output_path), "Le fichier PDF fusionné n'a pas été créé"