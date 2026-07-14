"""Agent registry — builds and looks up the specialist agents.

One place constructs all agents from the shared ``LLMPort`` (+ ``RetrieverPort``
for grounding). The registry is framework-free and fully unit-testable.
"""

from __future__ import annotations

from copilot.agents.airflow.agent import AirflowAgent
from copilot.agents.base.agent import BaseAgent
from copilot.agents.data_quality.agent import DataQualityAgent
from copilot.agents.dbt.agent import DbtAgent
from copilot.agents.documentation.agent import DocumentationAgent
from copilot.agents.etl.agent import EtlAgent
from copilot.agents.pyspark.agent import PySparkAgent
from copilot.agents.rag.agent import RagAgent
from copilot.agents.sql.agent import SqlAgent
from copilot.domain.exceptions import ConfigurationError
from copilot.domain.ports.llm import LLMPort
from copilot.domain.ports.retriever import RetrieverPort
from copilot.domain.value_objects.enums import AgentType


class AgentRegistry:
    def __init__(self, llm: LLMPort, retriever: RetrieverPort | None = None) -> None:
        self._agents: dict[AgentType, BaseAgent] = {
            AgentType.SQL: SqlAgent(llm, retriever),
            AgentType.PYSPARK: PySparkAgent(llm, retriever),
            AgentType.ETL: EtlAgent(llm, retriever),
            AgentType.DATA_QUALITY: DataQualityAgent(llm, retriever),
            AgentType.DOCUMENTATION: DocumentationAgent(llm, retriever),
            AgentType.AIRFLOW: AirflowAgent(llm, retriever),
            AgentType.DBT: DbtAgent(llm, retriever),
            AgentType.RAG: RagAgent(llm, retriever),
        }

    def get(self, agent_type: AgentType) -> BaseAgent:
        try:
            return self._agents[agent_type]
        except KeyError as exc:  # pragma: no cover - defensive
            raise ConfigurationError(f"No agent registered for {agent_type!r}") from exc

    def available(self) -> list[AgentType]:
        return list(self._agents.keys())
