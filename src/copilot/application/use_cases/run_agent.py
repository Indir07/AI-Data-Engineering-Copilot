"""Run-agent use case.

Wraps the orchestrator behind a use case so the API depends on a small, easily
overridable seam. Typed against a structural ``_Orchestrator`` protocol so this
module does not import LangGraph — keeping the app's import graph (and most
tests) free of that dependency.
"""

from __future__ import annotations

from typing import Protocol

from copilot.agents.base.types import AgentRequest, AgentResult


class _Orchestrator(Protocol):
    def run(self, request: AgentRequest) -> AgentResult: ...


class RunAgentUseCase:
    def __init__(self, orchestrator: _Orchestrator) -> None:
        self._orchestrator = orchestrator

    def execute(self, request: AgentRequest) -> AgentResult:
        return self._orchestrator.run(request)
