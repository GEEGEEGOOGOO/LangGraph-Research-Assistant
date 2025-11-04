# tests/conftest.py
import pytest
from app.graph import PipelineGraph
from app.agents.planner import Planner
from app.agents.retriever import Retriever
from app.agents.synthesizer import Synthesizer
from app.vectorstore import VectorStoreManager

@pytest.fixture(scope="session")
def pipeline():
    return PipelineGraph()

@pytest.fixture(scope="session")
def vsm():
    return VectorStoreManager()
