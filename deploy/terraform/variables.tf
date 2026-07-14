# STUB — variables a real deployment would expose. Illustrative only.

variable "project_name" {
  type    = string
  default = "ai-data-engineering-copilot"
}

variable "region" {
  type    = string
  default = "eu-west-1"
}

variable "image" {
  description = "Container image (built from the repo Dockerfile) used by api & ui."
  type        = string
  default     = "ghcr.io/indir07/ai-data-engineering-copilot:latest"
}

variable "db_instance_class" {
  type    = string
  default = "db.t3.micro"
}

variable "api_desired_count" {
  type    = number
  default = 2
}
