# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from app.graph import PipelineGraph
from app.langsmith_instrument import trace_event
from typing import List

app = FastAPI(title="LangGraph Research Assistant v2")

graph = PipelineGraph()

class RunRequest(BaseModel):
    query: str

class RunResponse(BaseModel):
    planner_action: str
    retrieved_docs: List[str]
    final_answer: str

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/run", response_model=RunResponse)
async def run_endpoint(req: RunRequest):
    trace_event("request.received", {"query": req.query})
    result = await graph.run(req.query)
    trace_event("graph.completed", {"planner_action": result["planner_action"]})
    return RunResponse(
        planner_action=result["planner_action"],
        retrieved_docs=result["retrieved_docs"],
        final_answer=result["final_answer"]
    )
