# ADR-0006: Docker Compose now, cloud-ready structure

- **Status:** Accepted
- **Date:** 2026-07-14
- **Deciders:** Indir

## Context
The project must start with a single `docker compose up`, cost nothing, and yet
credibly answer "how would you run this in the cloud?" We want the local path to
be effortless and the cloud path to be a short, believable extension — without
building (and paying for) real cloud infra now.

## Options considered
1. **Compose only.** Simplest; but leaves the cloud story implicit.
2. **Kubernetes/Terraform as the primary target.** Impressive, but heavy,
   costly, and overkill for a demo; slows everyone who just wants to run it.
3. **Compose primary + cloud-ready stubs.** Local is one command; `deploy/k8s/`
   and `deploy/terraform/` hold documented stubs showing the intended path.
   Chosen.

## Decision
**Docker Compose** is the supported runtime (services: `ui`, `api`, `ollama`,
`postgres`; named volumes for models/chroma/db). Relational storage is SQLite
locally and **Postgres in compose**, selected by `DATABASE_URL`. `deploy/k8s/`
and `deploy/terraform/` contain skeletons for a future managed deployment.

## Consequences
- (+) Frictionless, free local demo; no cloud account needed.
- (+) Container images are the same artifacts a cluster would run — the cloud
  path is real, not hand-wavy.
- (+) SQLite↔Postgres swap proves the persistence port works.
- (−) The k8s/terraform stubs are illustrative, not deployed; clearly labelled as
  such to avoid over-claiming.
