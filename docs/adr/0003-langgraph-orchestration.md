# ADR-0003: LangGraph for agent orchestration

- **Status:** Accepted
- **Date:** 2026-07-14
- **Deciders:** Indir

## Context
We have eight specialist agents plus a RAG step. A request must be routed to the
right agent, optionally retrieve context first, call the LLM, validate the
output, and sometimes retry or hand off. This control flow must be explicit,
inspectable, and testable.

## Options considered
1. **Single mega-prompt** ("you are an expert who can do everything"). Simple,
   but no separation of concerns, hard to test, unpredictable routing, no place
   to insert validation/retry. Rejected.
2. **Hand-rolled `if/elif` router + function calls.** Full control and no deps,
   but we would re-implement state management, branching, and retries ourselves,
   and lose a recognizable, reviewable pattern. Viable fallback.
3. **LangGraph.** Purpose-built stateful graph for LLM apps: nodes, conditional
   edges, shared typed state, checkpointing. Explicit and unit-testable per node.
   Chosen.

## Decision
Use **LangGraph** to model orchestration as a graph: a router node dispatches to
agent nodes; a retrieval node runs before agents that need grounding; a
validation node can loop back on failure. State is a typed dict flowing through
the graph.

## Consequences
- (+) Control flow is a diagram we can test node-by-node and show reviewers.
- (+) Adding an agent = adding a node + an edge, not editing a giant function.
- (+) Room for retries, guardrails, and human-in-the-loop later.
- (−) A dependency and a learning curve; kept contained inside
  `agents/orchestrator/` so the rest of the app just calls `orchestrator.run()`.
