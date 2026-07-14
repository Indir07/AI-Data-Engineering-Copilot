"""Unit tests for the agent framework (no LangGraph, no network)."""

from __future__ import annotations

import pytest

from copilot.agents.base.types import AgentRequest
from copilot.agents.orchestrator.registry import AgentRegistry
from copilot.agents.sql.agent import SqlAgent
from copilot.domain.value_objects.enums import AgentType, SqlDialect
from tests.fixtures.fakes import FakeLLM
from tests.fixtures.retrievers import FakeRetriever


@pytest.mark.unit
def test_registry_builds_all_eight_agents() -> None:
    registry = AgentRegistry(FakeLLM())
    assert set(registry.available()) == set(AgentType)


@pytest.mark.unit
def test_base_agent_returns_typed_result() -> None:
    registry = AgentRegistry(FakeLLM(reply="answer"))
    result = registry.get(AgentType.ETL).handle(
        AgentRequest(agent=AgentType.ETL, prompt="build a bronze layer")
    )
    assert result.agent is AgentType.ETL
    assert result.content == "answer"
    assert result.citations == []


@pytest.mark.unit
def test_sql_agent_injects_dialect_into_prompt() -> None:
    llm = FakeLLM()
    SqlAgent(llm).handle(
        AgentRequest(agent=AgentType.SQL, prompt="top customers", dialect=SqlDialect.POSTGRES)
    )
    user_msg = llm.calls[0][-1].content
    assert "postgres" in user_msg.lower()


@pytest.mark.unit
def test_rag_agent_grounds_and_cites_when_context_available() -> None:
    from copilot.agents.rag.agent import RagAgent

    llm = FakeLLM()
    result = RagAgent(llm, FakeRetriever()).handle(
        AgentRequest(agent=AgentType.RAG, prompt="what is bronze?")
    )
    assert result.citations and result.citations[0].source == "medallion.md"
    assert "bronze" in llm.calls[0][-1].content.lower()


@pytest.mark.unit
def test_use_rag_flag_gates_retrieval_for_generic_agents() -> None:
    llm = FakeLLM()
    # use_rag defaults False -> retriever not consulted even if present
    registry = AgentRegistry(llm, FakeRetriever())
    result = registry.get(AgentType.SQL).handle(
        AgentRequest(agent=AgentType.SQL, prompt="q", use_rag=False)
    )
    assert result.citations == []
