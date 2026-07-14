"""Agents router — list specialists and run a selected one."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from copilot.agents.base.types import AgentRequest
from copilot.application.use_cases.run_agent import RunAgentUseCase
from copilot.domain.value_objects.enums import AgentType
from copilot.presentation.api.dependencies import get_run_agent_use_case
from copilot.presentation.api.schemas.agent import (
    AgentInfo,
    AgentRunRequest,
    AgentRunResponse,
    CitationSchema,
)

router = APIRouter(prefix="/agents", tags=["agents"])

_DESCRIPTIONS: dict[AgentType, str] = {
    AgentType.SQL: "Generate, explain, debug, optimize, and translate SQL.",
    AgentType.PYSPARK: "Generate & optimize PySpark; explain Spark errors.",
    AgentType.ETL: "Bronze/Silver/Gold, incremental loads, CDC, SCD.",
    AgentType.DATA_QUALITY: "Great Expectations/Soda suites and profiling.",
    AgentType.DOCUMENTATION: "READMEs, architecture, API, and pipeline docs.",
    AgentType.AIRFLOW: "DAGs, scheduling, retries, task groups, sensors.",
    AgentType.DBT: "Models, tests, sources, snapshots, macros.",
    AgentType.RAG: "Answer from your uploaded documents with citations.",
}


@router.get("", response_model=list[AgentInfo], summary="List available agents")
def list_agents() -> list[AgentInfo]:
    return [AgentInfo(agent=a, description=_DESCRIPTIONS[a]) for a in AgentType]


@router.post("/{agent}", response_model=AgentRunResponse, summary="Run a specialist agent")
def run_agent(
    agent: AgentType,
    request: AgentRunRequest,
    use_case: RunAgentUseCase = Depends(get_run_agent_use_case),
) -> AgentRunResponse:
    result = use_case.execute(
        AgentRequest(
            agent=agent,
            prompt=request.prompt,
            dialect=request.dialect,
            model=request.model,
            temperature=request.temperature,
            use_rag=request.use_rag,
        )
    )
    return AgentRunResponse(
        agent=result.agent,
        content=result.content,
        model=result.model,
        citations=[CitationSchema(source=c.source, snippet=c.snippet) for c in result.citations],
        prompt_tokens=result.prompt_tokens,
        completion_tokens=result.completion_tokens,
    )
