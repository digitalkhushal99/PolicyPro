"""RAG part 1: read policy PDFs, split into chunks, embed them, save a FAISS index.
Run once, and again whenever the PDFs in data/policies change."""
import json
import re
from pathlib import Path

import faiss
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

PDF_DIR = Path("data/policies")
INDEX_DIR = Path("index")
EMBED_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE = 800        # characters per chunk
CHUNK_OVERLAP = 150     # shared characters between neighbouring chunks
MIN_CHUNK_CHARS = 100   # drop tiny fragments (headers, page numbers)

# Friendly names shown as sources in the bot's answers
SOURCE_NAMES = {
    "code_of_conduct": "Code of Conduct",
    "anti_bribery": "Anti-Bribery Policy",
    "posh_policy": "POSH Policy",
    "data_privacy": "Data Privacy Policy",
}


def clean(text: str) -> str:
    """Collapse the messy line breaks and spaces that PDFs produce."""
    return re.sub(r"\s+", " ", text).strip()


def load_chunks() -> list[dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = []
    for pdf in sorted(PDF_DIR.glob("*.pdf")):
        source = SOURCE_NAMES.get(pdf.stem, pdf.stem.replace("_", " ").title())
        reader = PdfReader(pdf)
        for page_num, page in enumerate(reader.pages, start=1):
            raw = page.extract_text() or ""
            for piece in splitter.split_text(raw):
                text = clean(piece)
                if len(text) >= MIN_CHUNK_CHARS:
                    chunks.append({
                        "id": len(chunks),
                        "source": source,
                        "file": pdf.name,
                        "page": page_num,
                        "text": text,
                    })
        print(f"  {pdf.name}: {len(reader.pages)} pages read")
    return chunks


def main():
    print("Reading and chunking PDFs...")
    chunks = load_chunks()
    print(f"Created {len(chunks)} chunks\n")

    print(f"Loading embedding model '{EMBED_MODEL}' (first run downloads about 90 MB)...")
    model = SentenceTransformer(EMBED_MODEL)
    vectors = model.encode(
        [c["text"] for c in chunks],
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True,   # so inner product = cosine similarity
    ).astype("float32")

    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)

    INDEX_DIR.mkdir(exist_ok=True)
    faiss.write_index(index, str(INDEX_DIR / "policies.faiss"))
    (INDEX_DIR / "chunks.json").write_text(
        json.dumps(chunks, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"\nSaved {index.ntotal} vectors to {INDEX_DIR}/")


if __name__ == "__main__":
    main()