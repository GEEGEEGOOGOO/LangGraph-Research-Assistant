# app/graph.py
import asyncio
from app.agents.planner import Planner
from app.agents.retriever import Retriever
from app.agents.synthesizer import Synthesizer

class PipelineGraph:
    def __init__(self):
        self.planner = Planner()
        self.retriever = Retriever()
        self.synth = Synthesizer()

    async def run(self, user_query: str):
        # 1. Plan
        plan = await self.planner.run(user_query)
        # 2. Retrieve if requested
        if plan.get("action") == "retrieve":
            retrieved = await self.retriever.run(plan.get("query"), k=3)
        else:
            retrieved = {"docs": []}
        # 3. Synthesize
        synth_out = await self.synth.run(user_query, retrieved.get("docs", []))
        return {
            "planner_action": plan.get("action"),
            "retrieved_docs": retrieved.get("docs", []),
            "final_answer": synth_out.get("answer", "")
        }

# convenience sync runner
def run_pipeline_sync(query: str):
    g = PipelineGraph()
    return asyncio.run(g.run(query))

if __name__ == "__main__":
    res = run_pipeline_sync("What is MCP and RAG?")
    print(res)
