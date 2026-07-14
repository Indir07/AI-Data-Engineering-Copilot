# ADR-0001: Clean / Hexagonal Architecture

- **Status:** Accepted
- **Date:** 2026-07-14
- **Deciders:** Indir (with Copilot as tech lead)

## Context
The project must read as production software to senior reviewers at data/cloud
companies, be highly testable without paid infrastructure, and let us swap the
LLM, vector store, and database freely. The architecture is the first thing a
reviewer judges.

## Options considered
1. **Flat / script-style** (one package, functions call libraries directly).
   Fast to write; but business logic is welded to FastAPI/Ollama/Chroma, unit
   testing needs real infra, and it screams "prototype." Rejected.
2. **Standard layered MVC** (controllers → services → models). Familiar, but the
   dependency direction still flows toward infrastructure; the domain ends up
   importing the ORM and HTTP framework. Better, not enough.
3. **Clean / Hexagonal (ports & adapters).** Domain is pure; everything external
   is an interface with interchangeable implementations. More upfront structure.

## Decision
Adopt **Clean/Hexagonal Architecture**. The dependency rule points inward:
`presentation → application → domain` and `infrastructure → domain`. External
capabilities are `Protocol` ports in `domain/ports/`, wired by a single
composition root.

## Consequences
- (+) Business logic is framework-free and unit-testable with fakes — no Ollama
  needed to test an agent.
- (+) Infrastructure is swappable (Ollama→hosted LLM, Chroma→pgvector) with zero
  domain changes.
- (+) The folder structure itself demonstrates SOLID (esp. Dependency Inversion).
- (−) More indirection and boilerplate; a few extra files per feature.
- Follow-up: enforce the dependency rule in CI with an import-linter contract
  (Phase 11).
