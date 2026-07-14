# ADR-0004: ChromaDB + Sentence-Transformers for RAG

- **Status:** Accepted
- **Date:** 2026-07-14
- **Deciders:** Indir

## Context
The RAG engine must index uploaded docs (PDF/MD/CSV/TXT) and project docs, run
semantic search, and ground every answer. It must be free, embedded (no external
service to operate), and behind a port so it can be swapped for a managed vector
DB later.

## Options considered
**Vector store**
1. **FAISS** — fast, but a raw index: we would build persistence, metadata, and
   collection management ourselves. Rejected for ergonomics.
2. **pgvector** — great for production, but needs Postgres running for local RAG
   and more setup. Kept as the *future* swap target, not the default.
3. **ChromaDB** — embedded, persistent, metadata filtering, trivial API. Chosen.

**Embeddings**
1. **OpenAI embeddings** — paid. Rejected.
2. **Sentence-Transformers `all-MiniLM-L6-v2`** — tiny/fast, decent quality.
3. **Sentence-Transformers `bge-small-en-v1.5`** — similar size, stronger
   retrieval quality on CPU. Chosen (configurable).

## Decision
Use **ChromaDB** (persisted to a volume) behind a `VectorStorePort`, and
**Sentence-Transformers `bge-small-en-v1.5`** behind an `EmbedderPort`. Chunking
starts fixed-size with overlap; retrieval is top-k with metadata filters;
answers must carry **citations**.

## Consequences
- (+) Zero-ops, free, fully local; persists across restarts via a named volume.
- (+) Swap to pgvector/Qdrant later = new adapter, no domain change.
- (+) Citations make answers auditable and demo well.
- (−) Not built for millions of vectors; fine for a portfolio corpus.
- Follow-up: evaluate semantic/recursive chunking in a later iteration.
