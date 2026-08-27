from typing import List
from hashlib import sha256
PDF_AVAILABLE = False
try:
    from PyPDF2 import PdfReader
    PDF_AVAILABLE = True
except Exception:
    try:
        from pypdf import PdfReader
        PDF_AVAILABLE = True
    except Exception:
        PDF_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    _MODEL = SentenceTransformer('all-MiniLM-L6-v2')
except Exception:
    _MODEL = None


def extract_text_from_pdf(file_path: str) -> str:
    if not PDF_AVAILABLE:
        return ""
    reader = PdfReader(file_path)
    parts = []
    for p in reader.pages:
        parts.append(p.extract_text() or "")
    return "\n".join(parts)


def _fallback_embed(text: str, dim: int = 384) -> List[float]:
    h = sha256(text.encode('utf-8')).digest()
    vals = []
    for i in range(dim):
        b = h[i % len(h)]
        vals.append((b / 255.0))
    return vals


def embed_texts(texts: List[str]) -> List[List[float]]:
    if _MODEL is not None:
        embs = _MODEL.encode(texts, show_progress_bar=False)
        return [e.tolist() for e in embs]
    return [_fallback_embed(t) for t in texts]
