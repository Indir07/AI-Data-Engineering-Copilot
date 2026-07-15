# Changelog

All notable changes to this project. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/); the project is pre-1.0 and was
built in twelve phases.

## [Unreleased]

### Phase 12 — Documentation
- API reference (`docs/API.md`), data-flow diagrams (`docs/DATA_FLOW.md`),
  system-context & deployment Mermaid diagrams, this changelog, README polish.

### Phase 10 — Cloud-ready deployment
- Kubernetes manifests (namespace, config/secret, Postgres, Ollama, api + ui
  Deployments, HPA, Ingress, kustomization); Terraform variables + guidance;
  GHCR image-publish workflow.

### Phase 11 — CI/CD
- GitHub Actions: lint (ruff + black), advisory mypy, tests + coverage.

### Phase 9 — Testing
- e2e API journey, error-mapping tests, failing-LLM doubles, `docs/TESTING.md`.

### Phase 5 — RAG engine
- Embedder & vector-store ports; Sentence-Transformers embedder; ChromaDB store;
  chunker, loaders, retriever; `/upload`, `/rag/search`, `/rag/stats`; the RAG
  agent is now grounded.

### Phase 8 — Docker & Compose
- Single image for api & ui; entrypoint runs Alembic; `docker compose` stack
  (ollama + postgres + api + ui) with healthchecks and volumes.

### Phase 7 — Streamlit UI
- Dashboard: agent selector, chat with citations & downloads, uploader, health.

### Phase 6 — Multi-agent system
- BaseAgent template + 8 specialists; AgentRegistry; LangGraph orchestrator;
  `/agents` API.

### Phase 4 — Persistence
- ConversationRepository port; SQLAlchemy models + adapter; Alembic; `/conversations`.

### Phase 3 — Backend backbone
- Domain ports/entities; OllamaProvider; DI composition root; `/chat`.

### Phase 2 — Tooling & skeleton
- Settings, structured logging, FastAPI `/health`, Streamlit stub, first tests.

### Phase 1 — Architecture
- Clean/Hexagonal scaffold, ARCHITECTURE.md, seven ADRs, README.
