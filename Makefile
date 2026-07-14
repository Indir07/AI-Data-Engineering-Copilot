# ---------------------------------------------------------------------------
# Developer entry points. `make help` lists everything.
# These are thin wrappers so the same commands work locally and in CI.
# ---------------------------------------------------------------------------
.DEFAULT_GOAL := help
.PHONY: help install format lint typecheck test cov run-api run-ui up down logs pull-models

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

install: ## Install package + dev tooling and git hooks
	pip install -e ".[dev]"
	pre-commit install

format: ## Auto-format with black + ruff --fix
	black src tests
	ruff check --fix src tests

lint: ## Lint without modifying files (CI gate)
	ruff check src tests
	black --check src tests

typecheck: ## Static type checking
	mypy src

test: ## Run the full test suite
	pytest

cov: ## Run tests with coverage report
	pytest --cov=copilot --cov-report=html

run-api: ## Run the FastAPI backend locally
	uvicorn copilot.presentation.api.main:app --reload --host 0.0.0.0 --port 8000

run-ui: ## Run the Streamlit UI locally
	streamlit run src/copilot/presentation/ui/app.py

up: ## Start the full stack (compose)
	docker compose up --build

down: ## Stop the stack and remove volumes
	docker compose down -v

logs: ## Tail all container logs
	docker compose logs -f

pull-models: ## Pull the local LLM + embedding models into Ollama
	docker compose exec ollama ollama pull qwen2.5-coder:7b-instruct
	docker compose exec ollama ollama pull llama3.1:8b-instruct
