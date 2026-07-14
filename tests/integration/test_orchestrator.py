"""Orchestrator test — exercises the real LangGraph graph.

Skipped automatically if LangGraph is not installed so the rest of the suite
still runs in minimal environments.
"""

from __future__ import annotations

import pytest

pytest.importorskip("langgraph")

from copilot.agents.base.types import AgentRequest  # noqa: E402
from copilot.agents.orchestrator.orchestrator import AgentOrchestrator  # noqa: E402
from copilot.agents.orchestrator.registry import AgentRegistry  # noqa: E402
from copilot.domain.value_objects.enums import AgentType  # noqa: E402
from tests.fixtures.fakes import FakeLLM  # noqa: E402


@pytest.mark.integration
def test_orchestrator_dispatches_to_selected_agent() -> None:
    orchestrator = AgentOrchestrator(AgentRegistry(FakeLLM(reply="ok")))
    result = orchestrator.run(AgentRequest(agent=AgentType.PYSPARK, prompt="optimize a join"))
    assert result.agent is AgentType.PYSPARK
    assert result.content == "ok"
