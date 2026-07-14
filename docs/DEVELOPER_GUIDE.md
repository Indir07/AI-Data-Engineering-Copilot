# Developer Guide

How the codebase is organized and how to run it during development. For the
*why* behind the structure, read [ARCHITECTURE.md](ARCHITECTURE.md) and the
[ADRs](adr/).

## Prerequisites

- Python 3.11+
- (Later phases) Docker + Docker Compose, and Ollama for local inference.

## Local setup

```bash
cp .env.example .env
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

## Run the pieces (Phase 2 skeleton)

```bash
# API (http://localhost:8000/docs)
make run-api        # uvicorn copilot.presentation.api.main:app --reload

# UI  (http://localhost:8501) — talks to the API
make run-ui         # streamlit run src/copilot/presentation/ui/app.py
```

Confirm the backend is alive:

```bash
curl http://localhost:8000/health
# {"status":"ok","version":"0.1.0","app_env":"local","llm_model":"qwen2.5-coder:7b-instruct"}
```

## Layout cheat-sheet

| Path | Layer | Put here |
|------|-------|----------|
| `src/copilot/domain/` | Domain | entities, value objects, ports (pure) |
| `src/copilot/application/` | Application | use cases, DTOs, services |
| `src/copilot/agents/` | Application | specialist agents + orchestrator |
| `src/copilot/rag/` | Application | ingestion, chunking, embeddings, retrieval |
| `src/copilot/infrastructure/` | Infrastructure | adapters (Ollama, Chroma, SQLAlchemy) |
| `src/copilot/presentation/` | Presentation | FastAPI (`api/`), Streamlit (`ui/`) |
| `src/copilot/config/` | Config | settings, logging, DI composition root |

## Configuration

All configuration flows through `copilot.config.Settings` (env / `.env`). Never
read `os.environ` elsewhere — add a typed field to `Settings` instead.

## Quality gates

`make format` before committing; `make lint typecheck test` must be green. CI
(Phase 11) runs the same commands.
