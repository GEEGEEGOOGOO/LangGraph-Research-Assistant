"""
app/vectorstore.py
Handles FAISS vectorstore creation, loading, and similarity search.
"""

import os
from typing import List
from langchain_core.documents import Document
from app.config import settings
from app.simple_graph import SimpleKnowledgeGraph

class VectorStoreManager:
    def __init__(self, path: str = settings.VECTORSTORE_PATH):
        # Adjust path to be a json file for the graph if it was a directory
        if not path.endswith(".json"):
             path = os.path.join(path, "graph.json")
        self.path = path
        self.kg = SimpleKnowledgeGraph(path=self.path)

    def build_index(self, documents: List[Document]):
        """Builds and saves a Knowledge Graph from a list of documents."""
        print(f"[INFO] Building Knowledge Graph at: {self.path}")
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        
        for doc in documents:
            self.kg.process_document(doc)
            
        self.kg.save_graph()
        print(f"[SUCCESS] Knowledge Graph saved at {self.path}")

    def load_index(self):
        """Loads the Knowledge Graph if it exists."""
        print(f"[INFO] Loading Knowledge Graph from {self.path}")
        self.kg.load_graph()
        return self.kg

    def similarity_search(self, query: str, k: int = 3) -> List[Document]:
        """Retrieves related concepts from the graph for a given query."""
        # Ensure graph is loaded
        if len(self.kg.graph.nodes) == 0:
            self.load_index()
            
        # Use the graph search (which finds neighbors of entities in the query)
        # We assume k is mapped to hops or just ignored/used for limiting results
        results = self.kg.search(query)
        
        # Convert string results to Documents for compatibility
        documents = [Document(page_content=r) for r in results[:k]]
        return documents


# Example usage
if __name__ == "__main__":
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