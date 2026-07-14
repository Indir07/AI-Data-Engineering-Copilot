"""Data Quality agent: Great Expectations/Soda suites, profiling, anomalies."""

from __future__ import annotations

from copilot.agents.base.agent import BaseAgent
from copilot.domain.value_objects.enums import AgentType


class DataQualityAgent(BaseAgent):
    agent_type = AgentType.DATA_QUALITY
