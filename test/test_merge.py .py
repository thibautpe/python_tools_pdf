import os

def test_merged_pdf_exists():
    assert os.path.exists("/data/out/mergedpdf.pdf")