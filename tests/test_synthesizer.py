# tests/test_synthesizer.py
import pytest
from app.agents.synthesizer import Synthesizer

@pytest.mark.asyncio
async def test_synthesizer_produces_answer():
    synth = Synthesizer()
    docs = [
        "Model Context Protocol defines tool-sharing.",
        "RAG uses vector search for context."
    ]
    out = await synth.run("Explain MCP and RAG", docs)
    assert "answer" in out
    assert isinstance(out["answer"], str)
    assert "RAG" in out["answer"] or "MCP" in out["answer"]
