"""PySpark agent: generate & optimize Spark, explain Spark errors."""

from __future__ import annotations

from copilot.agents.base.agent import BaseAgent
from copilot.domain.value_objects.enums import AgentType


class PySparkAgent(BaseAgent):
    agent_type = AgentType.PYSPARK
