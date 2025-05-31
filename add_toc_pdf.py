import os
from PyPDF2 import PdfMerger, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 📁 Dossier contenant les fichiers PDF à fusionner
pdf_folder = r"E:\Guitare - Webrip\Paetreon tiefsaiter\tabs"
output_pdf = r"E:\Guitare - Webrip\Paetreon tiefsaiter\tabs\FusionFinale.pdf"

# Supprimer le fichier résultat s'il existe déjà
if os.path.exists(output_pdf):
    os.remove(output_pdf)
    print(f"🗑️ Ancien fichier supprimé : {output_pdf}")

# Enregistrer Verdana et Verdana-Bold
pdfmetrics.registerFont(TTFont('Verdana', r'C:\Windows\Fonts\Verdana.ttf'))
pdfmetrics.registerFont(TTFont('Verdana-Bold', r'C:\Windows\Fonts\verdanab.ttf'))

# Récupérer tous les fichiers PDF du dossier (triés par nom)
pdf_files = sorted([
    os.path.join(pdf_folder, f)
    for f in os.listdir(pdf_folder)
    if f.lower().endswith(".pdf")
])

# Génération du sommaire (avec ReportLab)
toc_titles = []
for pdf_path in pdf_files[1:]:
    bookmark_name = os.path.splitext(os.path.basename(pdf_path))[0]
    toc_titles.append(bookmark_name)

toc_buffer = BytesIO()
c = canvas.Canvas(toc_buffer, pagesize=A4)
def create_toc_header():
    c.setFont("Verdana-Bold", 18)
    c.drawString(180, 800, "Table of content")
    c.setFont("Verdana", 12)
    return 760
y = create_toc_header()
items_per_page = 35
current_item = 0
right_margin = 500
for title in toc_titles:
    if current_item >= items_per_page:
        c.showPage()
        y = create_toc_header()
        current_item = 0
    c.drawString(100, y, title)
    y -= 20
    current_item += 1
c.save()
toc_buffer.seek(0)
toc_reader = PdfReader(toc_buffer)
toc_pages = len(toc_reader.pages)

# Fusion dans le bon ordre
merger = PdfMerger()
cover_pdf = pdf_files[0]
merger.append(cover_pdf)
merger.add_outline_item("00-Cover", 0, bold=True)  # 0 = première page, gras

# Table of content (signet en italique)
merger.append(toc_reader)
merger.add_outline_item("Table of content", 1, italic=True)  # 1 = deuxième page, italique

# Les autres PDFs (signets normaux)
current_page = 1 + toc_pages
page_indices = [("00-Cover", 1)]
for pdf_path in pdf_files[1:]:
    bookmark_name = os.path.splitext(os.path.basename(pdf_path))[0]
    merger.append(pdf_path, outline_item=bookmark_name)
    page_indices.append((bookmark_name, current_page + 1))
    current_page += len(PdfReader(pdf_path).pages)

# Sauvegarder le PDF fusionné
merger.write(output_pdf)
merger.close()

print(f"\n✅ Fusion terminée avec cover en page 1, sommaire en page 2, et signets corrects : {output_pdf}")