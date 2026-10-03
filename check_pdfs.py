from pathlib import Path
from pypdf import PdfReader

for pdf in Path("data/policies").glob("*.pdf"):
    reader = PdfReader(pdf)
    text = "".join(page.extract_text() or "" for page in reader.pages)
    print(f"{pdf.name}: {len(reader.pages)} pages, {len(text):,} characters")
    print("   Sample:", text[:150].replace("\n", " "), "\n")