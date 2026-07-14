# Testing

The suite follows the classic pyramid, made possible by the ports/adapters
design: because the core depends on interfaces, almost everything runs with fast
fakes and no external services.

## Layers

| Marker | Scope | External deps |
|--------|-------|---------------|
| `@pytest.mark.unit` | one class/function in isolation | none (fakes only) |
| `@pytest.mark.integration` | real adapter against local infra | in-memory SQLite; LangGraph |
| `@pytest.mark.e2e` | full journey through the FastAPI app | none (adapters faked) |

## Test doubles (`tests/fixtures/`)

- `FakeLLM` / `RaisingLLM` / `TimingOutLLM` — scripted `LLMPort` implementations.
- `InMemoryConversationRepository` — `ConversationRepository` without a DB.
- `FakeEmbedder` / `FakeVectorStore` — RAG ports without a model or Chroma.
- `FakeRetriever` — canned grounding context.

All satisfy their ports *structurally* (Protocols), so no inheritance is needed.

## Running

```bash
pip install -r requirements/dev.txt
pip install -e .
pytest                     # everything
pytest -m unit             # fast inner loop
pytest -m "not integration"
pytest --cov=copilot --cov-report=html
```

## What each layer proves

- **Unit** — business rules: prompt assembly, dialect injection, chunking,
  upsert-replaces-messages, error→HTTP mapping, Ollama response parsing.
- **Integration** — the SQLAlchemy repository against real SQLite, and the real
  LangGraph orchestrator (skipped if LangGraph is absent).
- **E2E** — a user journey (`health → chat → conversations → upload → search →
  agents`) through the real use cases with only external adapters faked.

## CI

GitHub Actions (`.github/workflows/ci.yml`) runs lint (ruff + black), an advisory
mypy pass, and the full suite with coverage on every push and PR to `main`.
