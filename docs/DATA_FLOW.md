# Data Flow

How data moves through the system for the two primary journeys. For the static
structure see [ARCHITECTURE.md](ARCHITECTURE.md).

## 1. Agent request (with optional RAG grounding)

```mermaid
flowchart TD
    A["User picks agent + prompt in UI"] --> B["POST /agents/{agent}"]
    B --> C[RunAgentUseCase]
    C --> D[AgentOrchestrator - LangGraph]
    D --> E[Specialist agent]
    E -->|use_rag?| F{Retrieve?}
    F -->|yes| G[VectorRetriever]
    G --> H[Embedder embeds query]
    H --> I[(ChromaDB top-k)]
    I --> E
    F -->|no| E
    E --> J[Prompt = system + context + task]
    J --> K[(Ollama LLM)]
    K --> L[AgentResult + citations]
    L --> M[JSON response to UI]
```

Grounding is optional per request (`use_rag`); the RAG agent always retrieves.
Citations flow back with the answer.

## 2. Document ingestion

```mermaid
flowchart LR
    U[Upload PDF/MD/CSV/TXT] --> P[POST /upload]
    P --> IN[IngestDocumentUseCase]
    IN --> L[load_text - pypdf / decode]
    L --> C[FixedSizeChunker - overlap]
    C --> E[Embedder.embed_documents]
    E --> V[(ChromaDB upsert)]
    V --> R[IngestResult: chunks_indexed]
```

## 3. Persistence of a conversation

```mermaid
flowchart LR
    Q[POST /conversations] --> UC[ConverseUseCase]
    UC --> LD{conversation_id?}
    LD -->|yes| GET[Repository.get]
    LD -->|no| NEW[new Conversation]
    GET --> ADD[append user turn]
    NEW --> ADD
    ADD --> LLM[(Ollama)]
    LLM --> ADD2[append assistant turn]
    ADD2 --> SAVE[Repository.save - upsert]
    SAVE --> DB[(SQLite / Postgres)]
```

Every boundary crossing maps transport ↔ DTO ↔ domain, so no framework or ORM
type ever reaches the domain core.
