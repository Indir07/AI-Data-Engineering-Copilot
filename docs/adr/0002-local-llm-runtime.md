# ADR-0002: Local LLM runtime via Ollama

- **Status:** Accepted
- **Date:** 2026-07-14
- **Deciders:** Indir

## Context
Hard requirement: **no paid APIs**, fully reproducible by anyone who clones the
repo. We still need solid code-generation quality and an OpenAI-style interface
so the app code stays clean.

## Options considered
1. **Hosted APIs (OpenAI/Anthropic/etc.)** — best quality, but violates the
   free-to-run constraint and adds secret management. Rejected.
2. **Raw `transformers` / `llama.cpp` in-process** — free, but couples model
   lifecycle, GPU/CPU handling, and quantization into our app; heavy images and
   slow cold starts. Rejected as the primary path.
3. **Ollama** — a small local server that manages model pull/quantization and
   exposes a clean HTTP API; runs as its own container; large model catalog
   (Qwen, Llama, Mistral). Chosen.

## Decision
Use **Ollama** as the inference runtime, in its own container, reached over HTTP
by an `OllamaProvider` adapter that implements `LLMPort`.

## Consequences
- (+) Free, local, reproducible; models cached in a named volume.
- (+) Clean separation — model runtime is infrastructure, not app code.
- (+) Trivial to switch models (see ADR-0005).
- (−) Quality/latency below frontier hosted models; mitigated by using a
  code-specialised model and low temperature.
- (−) Needs adequate RAM (~6–8 GB for a 7B quantized model); documented in the
  deployment guide.
