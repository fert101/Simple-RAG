from pypdf import PdfReader
from src.config import CHUNK_SIZE

def load_pdf(pdf_path: str) -> list[str]:
    reader = PdfReader(pdf_path)
    chunks = []

    for page in reader.pages:
        text = page.extract_text()
        if not text:
            continue
        words = text.split()
        for i in range(0, len(words), CHUNK_SIZE):
            chunk = " ".join(words[i:i + CHUNK_SIZE])
            chunks.append(chunk)

    print(f"[loader] {len(chunks)} chunks extracted")
    return chunks
