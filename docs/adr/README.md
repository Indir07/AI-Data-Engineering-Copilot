# Architecture Decision Records

Short, immutable records of *why* we made each significant choice. New decisions
add a new file; changed decisions supersede an old one (never edit history).

| ADR | Decision |
|-----|----------|
| [0001](0001-clean-architecture.md) | Clean / Hexagonal Architecture |
| [0002](0002-local-llm-runtime.md) | Local LLM runtime via Ollama |
| [0003](0003-langgraph-orchestration.md) | LangGraph for agent orchestration |
| [0004](0004-chromadb-vector-store.md) | ChromaDB + Sentence-Transformers for RAG |
| [0005](0005-model-agnostic-llm-provider.md) | Model-agnostic provider, default Qwen2.5-Coder 7B |
| [0006](0006-deployment-compose-cloud-ready.md) | Compose now, cloud-ready structure |

Use [`0000-template.md`](0000-template.md) for new records.
