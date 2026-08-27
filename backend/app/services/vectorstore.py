import os
import json
import math
from typing import List, Dict

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
VECTORS_PATH = os.path.join(DATA_DIR, "vectors.json")
META_PATH = os.path.join(DATA_DIR, "vectors_meta.json")
INDEX_PATH = os.path.join(DATA_DIR, "faiss.index")

os.makedirs(DATA_DIR, exist_ok=True)

try:
    import faiss
    import numpy as np
    _FAISS_AVAILABLE = True
except Exception:
    _FAISS_AVAILABLE = False


def _cosine(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


class VectorStore:
    def __init__(self):
        self.vectors: List[List[float]] = []
        self.metadatas: List[Dict] = []
        self.index = None
        self.dim = None
        self._load()

    def _load(self):
        if _FAISS_AVAILABLE and os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
            idx = faiss.read_index(INDEX_PATH)
            self.index = idx
            with open(META_PATH, 'r', encoding='utf-8') as f:
                self.metadatas = json.load(f)
            self.dim = self.index.d
        elif os.path.exists(VECTORS_PATH) and os.path.exists(META_PATH):
            with open(VECTORS_PATH, 'r', encoding='utf-8') as f:
                self.vectors = json.load(f)
            with open(META_PATH, 'r', encoding='utf-8') as f:
                self.metadatas = json.load(f)
        else:
            self.vectors = []
            self.metadatas = []

    def add(self, vectors: List[List[float]], metadatas: List[Dict]):
        if _FAISS_AVAILABLE:
            arr = np.array(vectors).astype('float32')
            if self.index is None:
                self.dim = arr.shape[1]
                self.index = faiss.IndexFlatL2(self.dim)
            self.index.add(arr)
            self.metadatas.extend(metadatas)
            faiss.write_index(self.index, INDEX_PATH)
            with open(META_PATH, 'w', encoding='utf-8') as f:
                json.dump(self.metadatas, f)
        else:
            self.vectors.extend(vectors)
            self.metadatas.extend(metadatas)
            with open(VECTORS_PATH, 'w', encoding='utf-8') as f:
                json.dump(self.vectors, f)
            with open(META_PATH, 'w', encoding='utf-8') as f:
                json.dump(self.metadatas, f)

    def search(self, vector: List[float], top_k: int = 5):
        if _FAISS_AVAILABLE and self.index is not None:
            q = np.array([vector]).astype('float32')
            D, I = self.index.search(q, top_k)
            results = []
            for dist, idx in zip(D[0], I[0]):
                if idx < 0 or idx >= len(self.metadatas):
                    continue
                m = self.metadatas[idx]
                results.append({"score": float(dist), "metadata": m})
            return results
        else:
            scores = []
            for idx, v in enumerate(self.vectors):
                sim = _cosine(vector, v)
                scores.append((sim, idx))
            scores.sort(key=lambda x: x[0], reverse=True)
            results = []
            for sim, idx in scores[:top_k]:
                results.append({"score": float(sim), "metadata": self.metadatas[idx]})
            return results


store = VectorStore()
