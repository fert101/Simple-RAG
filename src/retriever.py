from src.embedder import get_embeddings
from src.config   import TOP_K

def retrieve(query: str, chunks: list[str], index) -> list[str]:
    query_vec        = get_embeddings([query])
    _, indices       = index.search(query_vec, TOP_K)
    relevant_chunks  = [chunks[i] for i in indices[0]]
    print(f"[retriever] Found {len(relevant_chunks)} relevant chunks")
    return relevant_chunks
