# Deployment Guide

## Local (Docker Compose) — the supported path

```bash
git clone https://github.com/Indir07/AI-Data-Engineering-Copilot.git
cd AI-Data-Engineering-Copilot
cp .env.example .env            # optional; compose sets sane values
docker compose up --build
```

Services and ports:

| Service | URL | Purpose |
|---------|-----|---------|
| ui | http://localhost:8501 | Streamlit dashboard |
| api | http://localhost:8000/docs | FastAPI + Swagger |
| ollama | http://localhost:11434 | Local LLM runtime |
| postgres | localhost:5432 | History / metadata |

### First run: pull the models

Ollama starts empty. Pull the default (and optional alternate) models once:

```bash
docker compose exec ollama ollama pull qwen2.5-coder:7b-instruct
docker compose exec ollama ollama pull llama3.1:8b-instruct   # optional
```

The `api` container runs `alembic upgrade head` automatically on start
(`RUN_MIGRATIONS=1`), creating the schema in Postgres. Data persists in the
`ollama`, `pgdata`, and `appdata` named volumes.

### Common commands

```bash
make up        # docker compose up --build
make down      # stop + remove volumes
make logs      # tail all logs
docker compose ps
```

## Configuration

Everything is environment-driven (see `.env.example`). Compose overrides the
important ones: `DATABASE_URL` points at Postgres, `OLLAMA_BASE_URL` at the
ollama service, and chroma/uploads live under `/app/data`.

## Resource notes

A 7B quantized model needs roughly 6–8 GB RAM available to the ollama
container. Reduce by using a smaller model via `LLM_MODEL` (e.g. a 3B coder).

## Cloud-ready path (not deployed)

The same images target a cluster. `deploy/k8s/` and `deploy/terraform/` hold
**illustrative stubs** (clearly labelled) showing the intended shape — a
Deployment/Service per component, a managed Postgres, and persistent volumes for
models and the vector store. They are a starting point, not a turnkey deploy
(ADR-0006).
