# app/agents/synthesizer.py
from typing import Dict, Any
import os
import asyncio

# We will use a simple deterministic synthesizer.
# If OPENAI_API_KEY present and you want to call OpenAI, you can replace this with LangChain LLM usage.
from app.config import settings

class Synthesizer:
    def __init__(self, temperature: float = 0.0):
        self.temperature = temperature
        # Use OpenAI only if desired & available; otherwise fallback to local deterministic text
        self.use_openai = bool(settings.OPENAI_API_KEY)

        if self.use_openai:
            try:
                from langchain.chat_models import ChatOpenAI
                self.llm = ChatOpenAI(temperature=self.temperature, model_name="gpt-3.5-turbo")
                self.async_predict = getattr(self.llm, "apredict", None)
            except Exception:
                self.llm = None
                self.async_predict = None
        else:
            self.llm = None
            self.async_predict = None

    async def run(self, user_query: str, docs: list) -> Dict[str, Any]:
        prompt = "Synthesize a concise, accurate answer to the question using ONLY the documents below.\n\nQUESTION:\n" + user_query + "\n\nDOCUMENTS:\n\n" + "\n\n".join(docs)

        if self.llm and self.async_predict:
            try:
                answer = await self.async_predict(prompt)
                return {"answer": answer}
            except Exception as e:
                # fallback
                return {"answer": "SYNTHESIS (fallback): " + prompt[:800]}
        else:
            # deterministic local synthesis: join top docs with a header
            await asyncio.sleep(0.02)
            summary = "LOCAL SYNTHESIS: Based on the docs: " + " || ".join(docs[:3])
            return {"answer": summary}
