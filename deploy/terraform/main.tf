# STUB — illustrative only. Shows the cloud resources a real deployment needs.
# Not wired to a provider account; do not `apply` as-is.
# See ADR-0006 (compose now, cloud-ready structure).

terraform {
  required_version = ">= 1.5"
  # required_providers { aws = { source = "hashicorp/aws", version = "~> 5.0" } }
}

# variable "region" { type = string, default = "eu-west-1" }

# --- Container registry image (built from the repo Dockerfile) ---
# The same image runs the api and ui workloads.

# --- Managed Postgres for history/metadata (satisfies the persistence port) ---
# resource "aws_db_instance" "copilot" {
#   engine         = "postgres"
#   instance_class = "db.t3.micro"
#   db_name        = "copilot"
#   # ...
# }

# --- Compute for api/ui (ECS/Fargate, App Runner, or EKS) ---
# --- Object storage or a PVC for the ChromaDB persistence directory ---
# --- GPU node / instance for Ollama (or an OpenAI-compatible managed endpoint
#     swapped in behind LLMPort — no app changes needed) ---

output "next_steps" {
  value = "Fill in a provider + resources; the app is 12-factor and image-based, so wiring is straightforward."
}
