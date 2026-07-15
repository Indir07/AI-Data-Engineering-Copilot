# API Reference

Base URL (local): `http://localhost:8000`. Interactive docs: `/docs` (Swagger)
and `/redoc`. All request/response bodies are JSON unless noted.

## System

### `GET /health`
Liveness/readiness. Returns the active model.
```json
{ "status": "ok", "version": "0.1.0", "app_env": "local", "llm_model": "qwen2.5-coder:7b-instruct" }
```

### `GET /`
Service banner with links.

## Chat (stateless)

### `POST /chat`
One-shot completion; no history is persisted.
```bash
curl -s localhost:8000/chat -H 'content-type: application/json' -d '{
  "prompt": "Write SQL for the top 10 customers by revenue",
  "temperature": 0.1
}'
```
Response: `{ "content": "...", "model": "...", "prompt_tokens": n, "completion_tokens": n }`

## Conversations (persistent)

### `POST /conversations`
Start a new conversation, or continue one with `conversation_id`.
```bash
curl -s localhost:8000/conversations -H 'content-type: application/json' -d '{
  "prompt": "Explain the medallion architecture"
}'
# -> { "conversation_id": "…", "content": "…", "model": "…" }
```

### `GET /conversations`
List recent conversations: `[{ id, title, created_at, message_count }]`.

### `GET /conversations/{id}`
Full message history (system prompt omitted). `404` if not found.

## Agents

### `GET /agents`
List the 8 specialists: `[{ agent, description }]`.

### `POST /agents/{agent}`
Run a specialist. `agent` ∈ `sql|pyspark|etl|data_quality|documentation|airflow|dbt|rag`.
```bash
curl -s localhost:8000/agents/sql -H 'content-type: application/json' -d '{
  "prompt": "top customers by revenue",
  "dialect": "postgres",
  "use_rag": false
}'
```
Response: `{ agent, content, model, citations: [{source, snippet}], prompt_tokens, completion_tokens }`.

## RAG

### `POST /upload`  (multipart/form-data)
Index a document (`pdf` | `md` | `csv` | `txt`).
```bash
curl -s -F 'file=@medallion.md' localhost:8000/upload
# -> { "document_id": "…", "source": "medallion.md", "chunks_indexed": 7 }
```

### `POST /rag/search`
Semantic search over indexed chunks.
```bash
curl -s localhost:8000/rag/search -H 'content-type: application/json' -d '{
  "query": "how is the silver layer defined?", "top_k": 5
}'
# -> { "query": "…", "results": [{ "text": "…", "source": "…", "score": 0.87 }] }
```

### `GET /rag/stats`
`{ "indexed_chunks": n }`.

## Errors

Domain failures map to HTTP status codes via a single handler:

| Exception | Status |
|-----------|--------|
| `LLMTimeoutError` | 504 |
| `LLMError`, `RetrievalError` | 502 |
| `NotFoundError` | 404 |
| `ConfigurationError`, other | 500 |
| Pydantic validation | 422 |

Error body: `{ "error": "<ExceptionName>", "detail": "...", "status": <code> }`.
