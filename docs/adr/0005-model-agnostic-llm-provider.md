# ADR-0005: Model-agnostic LLM provider, default Qwen2.5-Coder 7B

- **Status:** Accepted
- **Date:** 2026-07-14
- **Deciders:** Indir

## Context
The spec allowed "Qwen 3 or Llama 3." Rather than hard-code one, a senior design
hides the model behind an interface so it can change by config. We still pick a
sensible default optimised for *this* workload: SQL, PySpark, dbt, and pipeline
code generation.

## Options considered
1. **Hard-code Llama 3.1 8B.** Widely recognised, strong generalist; slightly
   weaker on pure code than a code-specialised model.
2. **Hard-code Qwen2.5-Coder 7B.** Excellent code/SQL generation for its size;
   ideal for a data-engineering copilot.
3. **Model-agnostic provider** with a configurable default and fallback. Small
   amount of extra engineering; maximum flexibility and a stronger portfolio
   signal.

## Decision
Build a **model-agnostic provider layer** (`LLMPort` + `OllamaProvider` + a
factory) with the model chosen via `LLM_MODEL`. Default to
**`qwen2.5-coder:7b-instruct`** (best free coder for the workload), with
**`llama3.1:8b-instruct`** configured as an easy alternative/fallback. Low
temperature (0.1) for deterministic, reviewable code output.

## Consequences
- (+) "Use the best model" is answered without coupling to a vendor.
- (+) Reviewers see the Strategy pattern applied to model selection.
- (+) A/B comparing models becomes a config change, enabling future evals.
- (−) One more abstraction; justified because model choice is volatile.
