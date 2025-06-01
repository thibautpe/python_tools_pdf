import os

def test_merged_pdf_exists():
    assert os.path.exists("test/data/out/mergedpdf.pdf")