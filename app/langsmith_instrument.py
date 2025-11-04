"""
app/langsmith_instrument.py
Handles tracing and logging events for LangSmith or local console fallback.
"""

import os
import json
from datetime import datetime
from typing import Optional

try:
    # Try importing LangSmith SDK (optional)
    from langsmith import Client
    LANGSMITH_AVAILABLE = True
except ImportError:
    LANGSMITH_AVAILABLE = False

from app.config import settings

class LangSmithTracer:
    def __init__(self):
        self.enabled = bool(settings.LANGSMITH_API_KEY and LANGSMITH_AVAILABLE)
        self.client: Optional["Client"] = None
        if self.enabled:
            try:
                self.client = Client(api_key=settings.LANGSMITH_API_KEY)
                print("[LangSmith] Connected to LangSmith successfully.")
            except Exception as e:
                print(f"[LangSmith] Connection failed: {e}")
                self.enabled = False

    def trace_event(self, event_name: str, data: dict):
        """Record an event to LangSmith or console fallback."""
        timestamp = datetime.utcnow().isoformat()
        record = {"timestamp": timestamp, "event": event_name, "data": data}
        if self.enabled and self.client:
            try:
                # Simplified logging via metadata
                self.client.create_run(
                    name=event_name,
                    inputs=data,
                    outputs={},
                    run_type="chain",
                )
            except Exception as e:
                print(f"[LangSmith] Trace error: {e}")
        else:
            print(f"[TRACE] {event_name} - {json.dumps(data, indent=2)}")

# global tracer instance
tracer = LangSmithTracer()
trace_event = tracer.trace_event
