"""Application configuration (12-factor, environment-driven).

A single, validated :class:`Settings` object is the *only* thing the composition
root reads to wire the application. Nothing else in the codebase touches
``os.environ`` — this keeps configuration explicit, typed, and testable.

Why one flat, cached Settings object?
    * Typed & validated at startup: a bad ``LLM_TEMPERATURE`` fails fast with a
      clear error instead of surfacing deep inside an agent.
    * Test-friendly: tests build ``Settings(**overrides)`` without env vars.
    * Cached: :func:`get_settings` returns a singleton so importing modules do
      not each re-parse the environment.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Strongly-typed application settings loaded from env / ``.env``."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- Application ---
    app_env: Literal["local", "dev", "prod"] = "local"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    # --- LLM provider (model-agnostic; see ADR-0002 / ADR-0005) ---
    llm_provider: Literal["ollama", "openai_compatible"] = "ollama"
    ollama_base_url: str = "http://ollama:11434"
    llm_model: str = "qwen2.5-coder:7b-instruct"
    llm_fallback_model: str = "llama3.1:8b-instruct"
    llm_temperature: float = Field(default=0.1, ge=0.0, le=2.0)
    llm_max_tokens: int = Field(default=2048, gt=0)
    llm_request_timeout: int = Field(default=120, gt=0)

    # --- Embeddings (RAG) ---
    embedding_provider: Literal["sentence_transformers"] = "sentence_transformers"
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    embedding_device: Literal["cpu", "cuda"] = "cpu"

    # --- Vector store ---
    vector_store: Literal["chroma"] = "chroma"
    chroma_persist_dir: str = "./data/chroma"
    chroma_collection: str = "copilot_docs"
    rag_top_k: int = Field(default=5, gt=0)
    rag_chunk_size: int = Field(default=800, gt=0)
    rag_chunk_overlap: int = Field(default=120, ge=0)

    # --- Relational storage ---
    database_url: str = "sqlite:///./data/copilot.db"

    # --- Analytical engine ---
    duckdb_path: str = "./data/analytics.duckdb"

    # --- Uploads ---
    upload_dir: str = "./data/uploads"
    max_upload_mb: int = Field(default=25, gt=0)

    @property
    def is_prod(self) -> bool:
        return self.app_env == "prod"


@lru_cache
def get_settings() -> Settings:
    """Return the process-wide singleton settings instance."""
    return Settings()
