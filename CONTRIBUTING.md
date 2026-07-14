# Contributing

Thanks for your interest! This project follows a small set of conventions that
keep it production-credible.

## Getting started

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"        # or: pip install -r requirements/dev.txt
pre-commit install
```

## Development loop

```bash
make format     # black + ruff --fix
make lint       # ruff + black --check (CI gate)
make typecheck  # mypy
make test       # pytest
```

All four must pass before a PR is opened; `pre-commit` runs the fast ones on
every commit and CI enforces them (Phase 11).

## Architecture rules (please respect the dependency direction)

- `domain/` is pure Python — **no** imports of FastAPI, Ollama, Chroma, or any
  framework. It defines entities, value objects, and **ports** (interfaces).
- `application/` orchestrates the domain via ports (use cases, agents).
- `infrastructure/` provides concrete adapters that **implement** domain ports.
- `presentation/` (FastAPI, Streamlit) depends inward only.
- New external capability → add a **port** in `domain/ports/`, then an adapter.
- Significant decisions get an ADR in `docs/adr/` (copy `0000-template.md`).

## Commits & branches

- Small, focused commits with imperative messages ("Add SQL agent prompt").
- Branch per feature: `feat/…`, `fix/…`, `docs/…`, `chore/…`.

## Tests

- `@pytest.mark.unit` — fast, all I/O mocked (the default).
- `@pytest.mark.integration` — real infra (db, vector store).
- `@pytest.mark.e2e` — full stack through the API.
