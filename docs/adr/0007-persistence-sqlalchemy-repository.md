# ADR-0007: Persistence via SQLAlchemy + Repository pattern + Alembic

- **Status:** Accepted
- **Date:** 2026-07-14
- **Deciders:** Indir

## Context
Conversations and generated artifacts must survive restarts. Local dev should
need zero setup; compose/cloud should use a real RDBMS. The domain must not know
which database is in use.

## Options considered
1. **Raw SQL / sqlite3.** No dependency, but hand-rolled mapping, no migrations,
   and DB-specific SQL leaks everywhere. Rejected.
2. **An ORM used directly in use cases.** Convenient, but couples application
   logic to the ORM/session and makes unit tests need a database. Rejected.
3. **SQLAlchemy 2.0 behind a Repository port, with Alembic migrations.** The
   domain defines `ConversationRepository`; a SQLAlchemy adapter implements it;
   Alembic versions the schema. Chosen.

## Decision
- **SQLAlchemy 2.0** (typed `Mapped` models) as the ORM, hidden behind the
  `ConversationRepository` **port**.
- **SQLite** locally (`sqlite:///./data/copilot.db`), **Postgres** in compose,
  selected purely by `DATABASE_URL` (see ADR-0006).
- **Alembic** for schema migrations; `Base.metadata.create_all` is used only as a
  convenience for the local SQLite path.
- The adapter maps ORM rows ↔ domain entities so the ORM never escapes
  infrastructure.

## Consequences
- (+) Use cases depend on an interface → unit-tested with an in-memory fake, no DB.
- (+) SQLite↔Postgres is a config change; proves the port abstraction.
- (+) Versioned, reviewable schema history via Alembic.
- (−) Mapping code between ORM and domain is extra boilerplate; the payoff is a
  domain that stays pure and portable.
