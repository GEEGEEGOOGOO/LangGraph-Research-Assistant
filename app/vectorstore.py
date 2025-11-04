"""
app/vectorstore.py
Handles FAISS vectorstore creation, loading, and similarity search.
"""

import os
from typing import List
from langchain_community.vectorstores import FAISS   # ✅ new import path
from langchain_core.documents import Document
from app.embeddings import get_embeddings
from app.config import settings


class VectorStoreManager:
    def __init__(self, path: str = settings.VECTORSTORE_PATH):
        self.path = path
        self.embeddings = get_embeddings()
        self.vectorstore: FAISS = None

    def build_index(self, documents: List[Document]):
        """Builds and saves a FAISS index from a list of documents."""
        print(f"[INFO] Building FAISS index at: {self.path}")
        os.makedirs(self.path, exist_ok=True)
        self.vectorstore = FAISS.from_documents(documents, self.embeddings)
        self.vectorstore.save_local(self.path)
        print(f"[SUCCESS] FAISS index saved at {self.path}")

    def load_index(self):
        """Loads the FAISS index if it exists."""
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"FAISS index not found at {self.path}")
        print(f"[INFO] Loading FAISS index from {self.path}")
        self.vectorstore = FAISS.load_local(self.path, self.embeddings, allow_dangerous_deserialization=True)
        return self.vectorstore

    def similarity_search(self, query: str, k: int = 3) -> List[Document]:
        """Retrieves the top-k most similar documents for a given query."""
        if self.vectorstore is None:
            self.load_index()
        results = self.vectorstore.similarity_search(query, k=k)
        return results


# Example usage
if __name__ == "__main__":
    # ✅ Document is already imported at the top of the file, so remove this line
    # from langchain.docstore.document import Document

    docs = [
        Document(page_content="Model Context Protocol (MCP) defines how models share tools and resources."),
        Document(page_content="Retrieval-Augmented Generation (RAG) adds context to LLMs using vector search."),
        Document(page_content="LangGraph supports multi-agent reasoning and orchestration.")
    ]

    vsm = VectorStoreManager()
    vsm.build_index(docs)
    vsm.load_index()
    result = vsm.similarity_search("Explain how RAG works with MCP")
    for r in result:
        print("-", r.page_content)