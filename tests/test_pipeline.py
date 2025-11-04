# tests/test_pipeline.py
import pytest
from app.graph import PipelineGraph

@pytest.mark.asyncio
async def test_full_pipeline_runs():
    graph = PipelineGraph()
    result = await graph.run("How do MCP and RAG work?")
    assert result["planner_action"] == "retrieve"
    assert len(result["retrieved_docs"]) >= 1
    assert "MCP" in result["final_answer"] or "RAG" in result["final_answer"]
