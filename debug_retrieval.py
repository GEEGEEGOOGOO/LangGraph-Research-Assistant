# debug_retrieval.py
from app.vectorstore import VectorStoreManager
from app.embeddings import get_embeddings
import os, asyncio

print("PWD:", os.getcwd())
vsm = VectorStoreManager()
print("VECTORSTORE_PATH:", vsm.path)

try:
    vsm.load_index()
    print("FAISS index loaded OK.")
except Exception as e:
    print("Failed to load FAISS index:", e)
    raise SystemExit(1)

print("\n--- Top stored docs (if available) ---")
try:
    if hasattr(vsm.vectorstore, "get_all_documents"):
        docs = vsm.vectorstore.get_all_documents()
        for i, d in enumerate(docs[:5], 1):
            print(i, getattr(d, "page_content", str(d))[:300])
    else:
        print("vectorstore has no get_all_documents method; skipping listing.")
except Exception as e:
    print("Could not list docs due to:", e)

queries = [
    "How does Retrieval-Augmented Generation (RAG) work?",
    "What is Kubernetes and how does it scale applications?"
]

emb = get_embeddings()

print("\n--- Embeddings for queries (first 8 dims) ---")
for q in queries:
    try:
        if callable(emb):
            vec = emb(q)
        elif hasattr(emb, "embed_query"):
            vec = emb.embed_query(q)
        elif hasattr(emb, "embed_documents"):
            vec = emb.embed_documents([q])[0]
        else:
            raise RuntimeError("Unknown embedding API")
        print(f"Query: {q}\n len={len(vec)} first8={vec[:8]}\n")
    except Exception as e:
        print("Embedding error for query:", q, e)

print("\n--- Similarity search results (top 3) ---")
for q in queries:
    try:
        res = vsm.similarity_search(q, k=3)
        print(f"\nQuery: {q}\nRetrieved {len(res)} docs:")
        for i, d in enumerate(res, 1):
            content = getattr(d, "page_content", str(d))
            print(f"  {i}. {content[:300]}")
    except Exception as e:
        print("Similarity search error for query:", q, e)
