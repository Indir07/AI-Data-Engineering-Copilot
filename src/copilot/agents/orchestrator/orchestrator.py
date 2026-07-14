"""Agent orchestrator built on a LangGraph state graph (ADR-0003).

The graph is intentionally small right now — an explicit route to the selected
agent (the UI has an agent picker) — but the structure is what matters: nodes and
edges are inspectable and testable, and richer flows (retrieve → reason →
validate → retry, or an auto-router node) slot in without changing callers.

The node logic delegates to the plain ``AgentRegistry`` so the business behaviour
stays testable independent of LangGraph.
"""

from __future__ import annotations

from typing import Any, TypedDict

from langgraph.graph import END, StateGraph

from copilot.agents.base.types import AgentRequest, AgentResult
from copilot.agents.orchestrator.registry import AgentRegistry
from copilot.domain.value_objects.enums import AgentType


class _AgentState(TypedDict):
    request: AgentRequest
    result: AgentResult | None


class AgentOrchestrator:
    def __init__(self, registry: AgentRegistry) -> None:
        self._registry = registry
        self._graph = self._build_graph()

    def _build_graph(self) -> Any:
        graph = StateGraph(_AgentState)
        graph.add_node("dispatch", self._dispatch_node)
        graph.set_entry_point("dispatch")
        graph.add_edge("dispatch", END)
        return graph.compile()

    def _dispatch_node(self, state: _AgentState) -> dict[str, AgentResult]:
        request = state["request"]
        agent = self._registry.get(request.agent)
        return {"result": agent.handle(request)}

    def run(self, request: AgentRequest) -> AgentResult:
        final_state = self._graph.invoke({"request": request, "result": None})
        result = final_state["result"]
        assert result is not None  # dispatch node always sets it
        return result

    def available_agents(self) -> list[AgentType]:
        return self._registry.available()
