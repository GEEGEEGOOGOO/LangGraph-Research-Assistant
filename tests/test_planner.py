# tests/test_planner.py
import pytest
from app.agents.planner import Planner

@pytest.mark.asyncio
async def test_planner_always_retrieves():
    planner = Planner()
    res = await planner.run("Explain RAG")
    assert isinstance(res, dict)
    assert res["action"] == "retrieve"
    assert "query" in res
