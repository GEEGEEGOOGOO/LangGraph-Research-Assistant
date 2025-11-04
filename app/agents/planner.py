# app/agents/planner.py
from typing import Dict, Any

class Planner:
    """
    Simple deterministic planner:
    - inspects the incoming user_query and decides the action (retrieve / none)
    - returns an intent dict consumed by downstream nodes.
    """
    def __init__(self):
        pass

    async def run(self, user_query: str) -> Dict[str, Any]:
        # Very simple deterministic planning: always retrieve
        return {"action": "retrieve", "query": user_query}
