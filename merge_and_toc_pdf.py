"""Fusionne des PDFs avec sommaire paginé et signets cliquables, configuration via config.toml."""

import os
from io import BytesIO
import toml
from PyPDF2 import PdfMerger, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Charger la configuration depuis config.toml
config = toml.load("config.toml")
pdf_folder = config["pdf"]["input_folder"]
output_folder = config["pdf"]["output_folder"]
output_file = config["pdf"]["output_file"]

# Créer le dossier de sortie s'il n'existe pas
os.makedirs(output_folder, exist_ok=True)
output_pdf = os.path.join(output_folder, output_file)

# Supprimer le fichier résultat s'il existe déjà
if os.path.exists(output_pdf):
    os.remove(output_pdf)
    print(f"🗑️ Ancien fichier supprimé : {output_pdf}")

# Enregistrer les polices Verdana et Verdana-Bold
pdfmetrics.registerFont(TTFont('Verdana', r'C:\Windows\Fonts\Verdana.ttf'))
pdfmetrics.registerFont(TTFont('Verdana-Bold', r'C:\Windows\Fonts\verdanab.ttf'))

# Récupérer tous les fichiers PDF du dossier (triés par nom)
pdf_files = sorted([
    os.path.join(pdf_folder, f)
    for f in os.listdir(pdf_folder)
    if f.lower().endswith(".pdf")
])

# Calculer le nombre de pages de chaque PDF (hors cover)
pdf_page_counts = []
for pdf_path in pdf_files[1:]:
    reader = PdfReader(pdf_path)
    pdf_page_counts.append(len(reader.pages))

# Générer la liste des titres pour le sommaire (hors cover)
toc_titles = [
    os.path.splitext(os.path.basename(f))[0]
    for f in pdf_files[1:]
]

def generate_toc(start_pages):
    """
    Génère un sommaire PDF en mémoire avec titres et numéros de page.
    start_pages : liste des pages de début de chaque section.
    Retourne un buffer PDF.
    """
    toc_mem_buffer = BytesIO()
    c = canvas.Canvas(toc_mem_buffer, pagesize=A4)
    def create_toc_header():
        c.setFont("Verdana-Bold", 18)
        c.drawString(180, 800, "Table of content")
        c.setFont("Verdana", 12)
        return 760
    y = create_toc_header()
    items_per_page = 35
    current_item = 0
    for idx, title in enumerate(toc_titles):
        if current_item >= items_per_page:
            c.showPage()
            y = create_toc_header()
            current_item = 0
        c.drawString(100, y, title)
        page_number = start_pages[idx]
        c.drawRightString(500, y, str(page_number))
        y -= 20
        current_item += 1
    c.save()
    toc_mem_buffer.seek(0)
    return toc_mem_buffer

# 1. Calculer les pages de début "provisoires" (en supposant 1 page de sommaire)
section_start_pages = []
CURRENT_PAGE = 2  # 1 = cover, 2 = sommaire (provisoire)
for count in pdf_page_counts:
    section_start_pages.append(CURRENT_PAGE + 1)
    CURRENT_PAGE += count

# 2. Générer le sommaire provisoire et obtenir le vrai nombre de pages du sommaire
toc_buffer = generate_toc(section_start_pages)
toc_reader = PdfReader(toc_buffer)
toc_pages = len(toc_reader.pages)

# 3. Recalculer les pages de début avec le vrai nombre de pages du sommaire
section_start_pages = []
CURRENT_PAGE = 1 + toc_pages  # 1 = cover, puis sommaire
for count in pdf_page_counts:
    section_start_pages.append(CURRENT_PAGE + 1)
    CURRENT_PAGE += count

# 4. Générer le sommaire définitif avec les bons numéros de pages
toc_buffer = generate_toc(section_start_pages)
toc_reader = PdfReader(toc_buffer)
toc_pages = len(toc_reader.pages)

# 5. Fusion dans le bon ordre et ajout des signets/outlines
merger = PdfMerger()
cover_pdf = pdf_files[0]
merger.append(cover_pdf)
merger.add_outline_item("00-Cover", 0, bold=True)  # 0 = première page, gras

# Table of content (signet en italique)
merger.append(toc_reader)
merger.add_outline_item("Table of content", 1, italic=True)  # 1 = deuxième page, italique

# Les autres PDFs (signets normaux)
for pdf_path in pdf_files[1:]:
    bookmark_name = os.path.splitext(os.path.basename(pdf_path))[0]
    merger.append(pdf_path, outline_item=bookmark_name)

# Sauvegarder le PDF fusionné
merger.write(output_pdf)
merger.close()

print("\n✅ Fusion terminée avec cover en page 1, sommaire en page 2,")
print(f"et signets corrects : {output_pdf}")
