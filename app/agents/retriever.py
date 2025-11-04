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
        docs = self.vsm.similarity_search(query, k=k)
        # docs are langchain Documents; turn into simple dicts
        texts = []
        for d in docs:
            if hasattr(d, "page_content"):
                texts.append(d.page_content)
            else:
                try:
                    texts.append(str(d))
                except Exception:
                    texts.append("")
        return {"docs": texts}
