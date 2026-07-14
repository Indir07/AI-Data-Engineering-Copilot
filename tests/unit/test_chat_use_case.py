"""Unit tests for ChatUseCase (no infra: FakeLLM only)."""

from __future__ import annotations

import pytest

from copilot.application.dto.chat import ChatRequestDTO
from copilot.application.services.prompts import BASE_SYSTEM_PROMPT
from copilot.application.use_cases.chat import ChatUseCase
from copilot.domain.value_objects.message import Message, Role
from tests.fixtures.fakes import FakeLLM


@pytest.mark.unit
def test_execute_returns_completion() -> None:
    llm = FakeLLM(reply="SELECT 1;")
    use_case = ChatUseCase(llm)

    result = use_case.execute(ChatRequestDTO(prompt="give me a query"))

    assert result.content == "SELECT 1;"
    assert result.model == "fake-model"


@pytest.mark.unit
def test_prepends_default_system_prompt() -> None:
    llm = FakeLLM()
    ChatUseCase(llm).execute(ChatRequestDTO(prompt="hello"))

    sent = llm.calls[0]
    assert sent[0].role is Role.SYSTEM
    assert sent[0].content == BASE_SYSTEM_PROMPT
    assert sent[-1] == Message(role=Role.USER, content="hello")


@pytest.mark.unit
def test_history_is_preserved_between_system_and_user() -> None:
    llm = FakeLLM()
    history = [Message(Role.USER, "first"), Message(Role.ASSISTANT, "answer")]

    ChatUseCase(llm).execute(ChatRequestDTO(prompt="second", history=history))

    roles = [m.role for m in llm.calls[0]]
    assert roles == [Role.SYSTEM, Role.USER, Role.ASSISTANT, Role.USER]


@pytest.mark.unit
def test_custom_system_prompt_overrides_default() -> None:
    llm = FakeLLM()
    ChatUseCase(llm).execute(ChatRequestDTO(prompt="hi", system="You are terse."))

    assert llm.calls[0][0].content == "You are terse."
