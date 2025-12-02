# app/agents/retriever.py
from typing import Dict, Any, List
from app.vectorstore import VectorStoreManager

class Retriever:
    """
    Retriever uses the VectorStoreManager to run similarity search.
    """
    def __init__(self, vsm: VectorStoreManager = None):
        self.vsm = vsm or VectorStoreManager()

    async def run(self, query: str, k: int = 3) -> Dict[str, Any]:
        """
        Runs the retrieval process using the Knowledge Graph.
        """
        # The VSM now uses SimpleKnowledgeGraph
        # similarity_search returns Documents where page_content is the entity/neighbor
        docs = self.vsm.similarity_search(query, k=k)
        
        texts = []
        for d in docs:
            if hasattr(d, "page_content"):
                texts.append(d.page_content)
            else:
                try:
                    texts.append(str(d))
                except Exception:
                    texts.append("")
        
        # If no results found, we might want to fallback or just return empty
        if not texts:
            print(f"[INFO] No graph neighbors found for query: {query}")
            
        return {"docs": texts}
