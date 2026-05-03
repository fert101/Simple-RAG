import faiss
import numpy as np
from fastembed import TextEmbedding

model = TextEmbedding("BAAI/bge-small-en-v1.5")

def get_embeddings(texts: list[str]) -> np.ndarray:
    embeddings = list(model.embed(texts))
    return np.array(embeddings, dtype="float32")

def build_index(chunks: list[str]):
    print("[embedder] Embedding chunks...")
    vectors = get_embeddings(chunks)
    index   = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)
    print("[embedder] Index ready")
    return index