"""dbt agent: models, tests, sources, snapshots, macros."""

from __future__ import annotations

from copilot.agents.base.agent import BaseAgent
from copilot.domain.value_objects.enums import AgentType


class DbtAgent(BaseAgent):
    agent_type = AgentType.DBT
