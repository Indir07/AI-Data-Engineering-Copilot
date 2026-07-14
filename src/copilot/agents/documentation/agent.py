"""Documentation agent: README, architecture, API, pipeline & data-flow docs."""

from __future__ import annotations

from copilot.agents.base.agent import BaseAgent
from copilot.domain.value_objects.enums import AgentType


class DocumentationAgent(BaseAgent):
    agent_type = AgentType.DOCUMENTATION
