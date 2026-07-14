"""ETL agent: Bronze/Silver/Gold, incremental loads, CDC, SCD."""

from __future__ import annotations

from copilot.agents.base.agent import BaseAgent
from copilot.domain.value_objects.enums import AgentType


class EtlAgent(BaseAgent):
    agent_type = AgentType.ETL
