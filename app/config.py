"""
app/config.py
Centralized configuration loader for environment variables.
"""

import os
import pathlib
from dotenv import load_dotenv

# Determine root path (project directory)
ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent

# Load .env once
load_dotenv(ROOT_DIR / ".env")

class Settings:
    """Container for application-wide settings."""

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    LANGSMITH_API_KEY: str = os.getenv("LANGSMITH_API_KEY")
    VECTORSTORE_PATH: str = os.getenv("VECTORSTORE_PATH", "./data/faiss_index")
    ENV: str = os.getenv("ENV", "development")

    @classmethod
    def summary(cls) -> str:
        """Quick diagnostic printout."""
        return (
            f"OPENAI_API_KEY: {'set' if cls.OPENAI_API_KEY else 'missing'}, "
            f"LANGSMITH_API_KEY: {'set' if cls.LANGSMITH_API_KEY else 'missing'}, "
            f"VECTORSTORE_PATH: {cls.VECTORSTORE_PATH}"
        )

settings = Settings()
