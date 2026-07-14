# Kubernetes manifests (illustrative stubs)

> **Not a turnkey deploy.** These show the intended shape of a cluster
> deployment (one Deployment + Service per component, managed Postgres,
> persistent volumes for models and the vector store). Treat them as a starting
> point — see [ADR-0006](../../docs/adr/0006-deployment-compose-cloud-ready.md).

Suggested resources:

- `api-deployment.yaml` — Deployment + Service + HPA for the FastAPI app.
- `ui-deployment.yaml` — Deployment + Service for Streamlit.
- Ollama as a StatefulSet with a PVC for model weights (GPU node pool ideally).
- Managed Postgres (RDS / Cloud SQL / Azure DB) via connection string secret.
- PVC or object storage for the ChromaDB persistence directory.
