# Terraform (illustrative stubs)

> **Not a turnkey deploy.** These files sketch the cloud resources a production
> deployment needs; they are intentionally provider-light so you can adapt them
> to AWS, GCP, or Azure. See
> [ADR-0006](../../docs/adr/0006-deployment-compose-cloud-ready.md).

What a real module would create:

- **Compute** for the `api` and `ui` containers (ECS/Fargate, Cloud Run, App
  Runner, or a node pool on EKS/GKE/AKS) running the repo's image.
- **Managed Postgres** (RDS / Cloud SQL / Azure DB) — its connection string is
  the only thing the app needs (satisfies the persistence port).
- **Persistent storage** (PVC or object storage) for the ChromaDB directory.
- **LLM**: a GPU instance running Ollama, *or* a managed OpenAI-compatible
  endpoint swapped in behind `LLMPort` with zero application changes.
- Networking (LB/ingress), secrets manager for `DATABASE_URL`, and a registry
  for the image.

Because the app is 12-factor and image-based, wiring these together is
straightforward — fill in a provider block and the resources in `main.tf`.
