# app/agents/synthesizer.py
import asyncio
from typing import Any, Dict, List
from app.config import settings
from app.langsmith_instrument import trace_event

class Synthesizer:
    def __init__(self, temperature: float = 0.0):
        self.temperature = temperature
        self.use_openai = bool(settings.OPENAI_API_KEY)
        try:
            if self.use_openai:
                from langchain.chat_models import ChatOpenAI
                self.llm = ChatOpenAI(temperature=self.temperature, model_name="gpt-3.5-turbo")
                self.async_predict = getattr(self.llm, "apredict", None)
            else:
                self.llm = None
                self.async_predict = None
        except Exception:
            self.llm = None
            self.async_predict = None

    async def run(self, user_query: str, docs: List[str]) -> Dict[str, Any]:
        """
        Synthesize an answer. If an external LLM is available, use it.
        Otherwise return a deterministic local synthesis that includes the query
        and the ranked documents used to create the answer.
        """
        prompt = (
            "Synthesize a concise answer to the question using the provided documents.\n\n"
            "QUESTION:\n" + user_query + "\n\nDOCUMENTS:\n\n" + "\n\n".join(docs)
        )

        try:
            trace_event("synthesizer.request", {"query": user_query, "doc_count": len(docs)})
        except Exception:
            pass

        if self.llm and self.async_predict:
            try:
                answer = await self.async_predict(prompt)
                try:
                    trace_event("synthesizer.completed", {"mode": "openai", "query": user_query})
                except Exception:
                    pass
                return {"answer": answer}
            except Exception as e:
                try:
                    trace_event("synthesizer.error", {"error": str(e)})
                except Exception:
                    pass
                return {"answer": "SYNTHESIS (fallback): " + prompt[:800]}

        # Local deterministic synthesis
        await asyncio.sleep(0.01)
        header = f"LOCAL SYNTHESIS for query: '{user_query}' -- using top {min(3, len(docs))} docs:\n\n"
        ranked = []
        for i, d in enumerate(docs[:3], start=1):
            snippet = d if isinstance(d, str) else getattr(d, "page_content", str(d))
            snippet_short = snippet[:320].replace("\n", " ")
            ranked.append(f"{i}. {snippet_short}")
        body = "\n".join(ranked)
        summary = header + body + "\n\nConcise answer: " + (" ".join(ranked))[:800]
        try:
            trace_event("synthesizer.completed", {"mode": "local", "query": user_query})
        except Exception:
            pass
        return {"answer": summary}
