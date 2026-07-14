"""Airflow agent: DAGs, scheduling, retries, task groups, sensors."""

from __future__ import annotations

from copilot.agents.base.agent import BaseAgent
from copilot.domain.value_objects.enums import AgentType


class AirflowAgent(BaseAgent):
    agent_type = AgentType.AIRFLOW
