---
name: pdf
description: Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill.
license: Proprietary. LICENSE.txt has complete terms
---

## Available Scripts (Base directory: same as this file)

This skill includes a `scripts/` directory with **8 ready-to-use Python scripts**. All must be executed with `uv run` — do NOT use `python`.

| Script | Purpose |
|--------|---------|
| `scripts/check_fillable_fields.py` | Check if a PDF has fillable form fields |
| `scripts/extract_form_field_info.py` | Extract fillable field metadata to JSON |
| `scripts/fill_fillable_fields.py` | Fill fillable form fields from a JSON values file |
| `scripts/extract_form_structure.py` | Extract text labels, lines, checkboxes from non-fillable PDFs |
| `scripts/check_bounding_boxes.py` | Validate bounding boxes before filling non-fillable forms |
| `scripts/fill_pdf_form_with_annotations.py` | Add text annotations to non-fillable PDFs |
| `scripts/convert_pdf_to_images.py` | Convert PDF pages to PNG/JPG images |
| `scripts/create_validation_image.py` | Create visual validation overlays for filled forms |

**Usage pattern:** `uv run scripts/<script_name>.py <args...>`

## Execution Environment and Guidelines

### Running Scripts

**All Python scripts in this skill MUST be executed using `uv run`.**

- NEVER use `python script.py`
- NEVER use `pip install` — scripts include PEP 723 inline metadata (`# /// script ... # ///`), so `uv run` automatically resolves and installs all dependencies
- NEVER attempt to manually install packages. If a dependency is missing, the script's inline metadata is incomplete — fix the metadata instead

**Correct Usage:**
```bash
uv run scripts/check_fillable_fields.py document.pdf
uv run scripts/extract_form_structure.py input.pdf output.json
```

### Temporary Files and Directories

**Unless the user explicitly requests a specific output location, always use temporary directories for intermediate files.**

This applies to all scripts and operations that generate intermediate files (images, extracted data, temporary PDFs, etc.).

**Ways to create temporary directories:**

1. **Bash (cross-platform):**
   ```bash
   temp_dir=$(mktemp -d)
   uv run scripts/convert_pdf_to_images.py input.pdf "$temp_dir"
   ```

2. **Python:**
   ```python
   import tempfile
   temp_dir = tempfile.mkdtemp(prefix="pdf_")
   ```

3. **Let scripts auto-create:** When scripts support it, omit the output directory to use a temporary location:
   ```bash
   uv run scripts/convert_pdf_to_images.py input.pdf
   # Output: Created temporary directory: /tmp/pdf_images_abc123/
   ```

**Core principle:** Only save to user-specified locations when explicitly requested. Temporary directories are automatically cleaned up by the system, preventing file clutter.

## Read REFERENCE.md Before Advanced Operations

This file (SKILL.md) covers common PDF tasks. **If your task is not covered here, or you need advanced features (pypdfium2 rendering, JavaScript libraries, batch processing, troubleshooting), read REFERENCE.md before attempting anything.** It is in the same directory as this file.

## Overview

This guide covers essential PDF processing operations. It is a quick-start reference — for anything beyond the basics, read **REFERENCE.md** first. It contains:

- **pypdfium2** — fast PDF rendering, image generation, text extraction (Chromium's PDFium engine)
- **pdf-lib (JavaScript)** — advanced PDF creation, modification, form filling
- **pdfjs-dist (JavaScript)** — browser-based PDF rendering, text extraction with coordinates
- **Advanced CLI operations** — poppler-utils, qpdf optimization, encryption, repair
- **Advanced Python techniques** — pdfplumber with custom table settings, reportlab with styled tables
- **Complex workflows** — figure extraction, batch processing with error handling, PDF cropping
- **Performance optimization** — handling large PDFs, memory management, tool selection guidance
- **Troubleshooting** — encrypted PDFs, corrupted files, text extraction fallbacks

If you need to fill out a PDF form, read **FORMS.md** and follow its instructions.

## Quick Start

```python
from pypdf import PdfReader, PdfWriter

# Read a PDF
reader = PdfReader("document.pdf")
print(f"Pages: {len(reader.pages)}")

# Extract text
text = ""
for page in reader.pages:
    text += page.extract_text()
```

## Python Libraries

### pypdf - Basic Operations

#### Merge PDFs
```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

#### Split PDF
```python
reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

#### Extract Metadata
```python
reader = PdfReader("document.pdf")
meta = reader.metadata
print(f"Title: {meta.title}")
print(f"Author: {meta.author}")
print(f"Subject: {meta.subject}")
print(f"Creator: {meta.creator}")
```

#### Rotate Pages
```python
reader = PdfReader("input.pdf")
writer = PdfWriter()

page = reader.pages[0]
page.rotate(90)  # Rotate 90 degrees clockwise
writer.add_page(page)

with open("rotated.pdf", "wb") as output:
    writer.write(output)
```

### pdfplumber - Text and Table Extraction

#### Extract Text with Layout
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

#### Extract Tables
```python
with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            print(f"Table {j+1} on page {i+1}:")
            for row in table:
                print(row)
```

#### Advanced Table Extraction
```python
import pandas as pd

with pdfplumber.open("document.pdf") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:  # Check if table is not empty
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

# Combine all tables
if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_excel("extracted_tables.xlsx", index=False)
```

### reportlab - Create PDFs

#### Basic PDF Creation
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=letter)
width, height = letter

# Add text
c.drawString(100, height - 100, "Hello World!")
c.drawString(100, height - 120, "This is a PDF created with reportlab")

# Add a line
c.line(100, height - 140, 400, height - 140)

# Save
c.save()
```

#### Create PDF with Multiple Pages
```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("report.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

# Add content
title = Paragraph("Report Title", styles['Title'])
story.append(title)
story.append(Spacer(1, 12))

body = Paragraph("This is the body of the report. " * 20, styles['Normal'])
story.append(body)
story.append(PageBreak())

# Page 2
story.append(Paragraph("Page 2", styles['Heading1']))
story.append(Paragraph("Content for page 2", styles['Normal']))

# Build PDF
doc.build(story)
```

#### Subscripts and Superscripts

**IMPORTANT**: Never use Unicode subscript/superscript characters (₀₁₂₃₄₅₆₇₈₉, ⁰¹²³⁴⁵⁶⁷⁸⁹) in ReportLab PDFs. The built-in fonts do not include these glyphs, causing them to render as solid black boxes.

Instead, use ReportLab's XML markup tags in Paragraph objects:
```python
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()

# Subscripts: use <sub> tag
chemical = Paragraph("H<sub>2</sub>O", styles['Normal'])

# Superscripts: use <super> tag
squared = Paragraph("x<super>2</super> + y<super>2</super>", styles['Normal'])
```

For canvas-drawn text (not Paragraph objects), manually adjust font the size and position rather than using Unicode subscripts/superscripts.

## Command-Line Tools

### pdftotext (poppler-utils)
```bash
# Extract text
pdftotext input.pdf output.txt

# Extract text preserving layout
pdftotext -layout input.pdf output.txt

# Extract specific pages
pdftotext -f 1 -l 5 input.pdf output.txt  # Pages 1-5
```

### qpdf
```bash
# Merge PDFs
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf

# Split pages
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf
qpdf input.pdf --pages . 6-10 -- pages6-10.pdf

# Rotate pages
qpdf input.pdf output.pdf --rotate=+90:1  # Rotate page 1 by 90 degrees

# Remove password
qpdf --password=mypassword --decrypt encrypted.pdf decrypted.pdf
```

### pdftk (if available)
```bash
# Merge
pdftk file1.pdf file2.pdf cat output merged.pdf

# Split
pdftk input.pdf burst

# Rotate
pdftk input.pdf rotate 1east output rotated.pdf
```

## Common Tasks

### Extract Text from Scanned PDFs

**Decision: How to handle scanned/image-based PDFs**

1. **If the model supports image understanding** (can read image files via the `read` tool) **AND the PDF has ≤ 5 pages**: Convert PDF pages to images and pass them directly to the model for text extraction. This is faster and more accurate than OCR for short documents.
   - Use `scripts/convert_pdf_to_images.py <pdf> [output_dir]` to convert PDF pages to images. If output_dir is not provided, a temporary directory will be created automatically.
   - Pass the images to the model using the `read` tool.

2. **If the model does NOT support image understanding, OR the PDF has > 5 pages**: Use OCR via pytesseract. This is more reliable for long documents and avoids context window limits.
   - Run scripts with `uv run` — scripts include PEP 723 inline metadata (`# /// script ... # ///`), so `uv` auto-resolves dependencies.
   - Do NOT use `pip install`.

```python
# /// script
# requires-python = ">=3.11"
# dependencies = ["pytesseract", "pdf2image"]
# ///
import pytesseract
from pdf2image import convert_from_path

# Convert PDF to images
images = convert_from_path('scanned.pdf')

# OCR each page
text = ""
for i, image in enumerate(images):
    text += f"Page {i+1}:\n"
    text += pytesseract.image_to_string(image)
    text += "\n\n"

print(text)
```

**Run with:** `uv run scripts/ocr_scanned_pdf.py scanned.pdf`

### Add Watermark
```python
from pypdf import PdfReader, PdfWriter

# Create watermark (or load existing)
watermark = PdfReader("watermark.pdf").pages[0]

# Apply to all pages
reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("watermarked.pdf", "wb") as output:
    writer.write(output)
```

### Extract Images
```bash
# Using pdfimages (poppler-utils)
pdfimages -j input.pdf output_prefix

# This extracts all images as output_prefix-000.jpg, output_prefix-001.jpg, etc.
```

### Password Protection
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

# Add password
writer.encrypt("userpassword", "ownerpassword")

with open("encrypted.pdf", "wb") as output:
    writer.write(output)
```

## Quick Reference

| Task | Best Tool | Command/Code |
|------|-----------|--------------|
| Merge PDFs | pypdf | `writer.add_page(page)` |
| Split PDFs | pypdf | One page per file |
| Extract text | pdfplumber | `page.extract_text()` |
| Extract tables | pdfplumber | `page.extract_tables()` |
| Create PDFs | reportlab | Canvas or Platypus |
| Command line merge | qpdf | `qpdf --empty --pages ...` |
| Scanned PDFs (multimodal model) | Convert to images + model vision | `scripts/convert_pdf_to_images.py <pdf> [output_dir]` |
| Scanned PDFs (non-multimodal) | pytesseract via `uv run` | See "Extract Text from Scanned PDFs" |
| Fill PDF forms | See FORMS.md | See FORMS.md |

## Next Steps

- **Before attempting any advanced operation**, read REFERENCE.md — it has detailed examples, performance tips, and troubleshooting for every tool listed above.
- If you need to fill out a PDF form, follow the instructions in FORMS.md.
