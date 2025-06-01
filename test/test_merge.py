import os
import subprocess

def test_merged_pdf_exists():
    # Nettoyer le fichier de sortie s'il existe déjà
    output_path = "test/data/out/mergedpdf.pdf"
    if os.path.exists(output_path):
        os.remove(output_path)

    # Lancer le script avec le fichier de config de test
    subprocess.run(
        ["python", "merge_and_toc_pdf.py", "test/config_test.toml"],
        check=True
    )

    # Vérifier que le fichier de sortie a été créé
    assert os.path.exists(output_path)