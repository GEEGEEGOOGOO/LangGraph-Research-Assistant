# app/embeddings.py
"""
Local embeddings adapter using sentence-transformers.
Provides the methods expected by LangChain and is callable for compatibility.
"""

from typing import List, Any
import os
from app.config import settings

try:
    from sentence_transformers import SentenceTransformer
except Exception as e:
    raise ImportError("sentence-transformers not installed. Run: pip install sentence-transformers") from e

DEFAULT_MODEL = os.getenv("LOCAL_EMBEDDING_MODEL", "all-MiniLM-L6-v2")

class LocalEmbeddings:
    def __init__(self, model_name: str = DEFAULT_MODEL):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if not isinstance(texts, list):
            texts = [texts]
        embeddings = self.model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
        return [e.tolist() for e in embeddings]

    def embed_query(self, text: str) -> List[float]:
        v = self.model.encode([text], show_progress_bar=False, convert_to_numpy=True)[0]
        return v.tolist()

    # Compatibility: make the instance callable like a function
    # LangChain's FAISS wrapper sometimes calls embedding_function(text) directly.
    def __call__(self, texts_or_text: Any):
        """
        If given a list, behave like embed_documents.
        If given a single string, behave like embed_query.
        """
        if isinstance(texts_or_text, (list, tuple)):
            return self.embed_documents(list(texts_or_text))
        if isinstance(texts_or_text, str):
            return self.embed_query(texts_or_text)
        # fallback: try to coerce
        try:
            return self.embed_documents(list(texts_or_text))
        except Exception:
            raise TypeError("Unsupported input type for LocalEmbeddings: " + str(type(texts_or_text)))

def get_embeddings():
    """
    Factory used by vectorstore.py. Returns a LocalEmbeddings instance for local-mode.
    """
    return LocalEmbeddings()
