# tests/test_retriever.py
import pytest
from app.agents.retriever import Retriever
from app.vectorstore import VectorStoreManager

@pytest.mark.asyncio
async def test_retriever_returns_docs():
    vsm = VectorStoreManager()
    retriever = Retriever(vsm)
    out = await retriever.run("MCP and RAG", k=2)
    assert "docs" in out
    assert isinstance(out["docs"], list)
    assert len(out["docs"]) > 0
