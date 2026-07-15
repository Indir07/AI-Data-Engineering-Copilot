"""Unit tests for ConverseUseCase using fakes (no DB, no network)."""

from __future__ import annotations

import pytest

from copilot.application.dto.conversation import ConverseRequestDTO
from copilot.application.use_cases.converse import ConverseUseCase
from copilot.domain.exceptions import NotFoundError
from copilot.domain.value_objects.message import Role
from tests.fixtures.fakes import FakeLLM
from tests.fixtures.repositories import InMemoryConversationRepository


def _use_case(reply: str = "hi") -> tuple[ConverseUseCase, InMemoryConversationRepository]:
    repo = InMemoryConversationRepository()
    return ConverseUseCase(FakeLLM(reply=reply), repo), repo


@pytest.mark.unit
def test_new_conversation_persists_user_and_assistant() -> None:
    use_case, repo = _use_case(reply="SELECT 1;")

    turn = use_case.execute(ConverseRequestDTO(prompt="a query"))

    stored = repo.get(turn.conversation_id)
    assert stored is not None
    roles = [m.role for m in stored.messages]
    assert roles == [Role.SYSTEM, Role.USER, Role.ASSISTANT]
    assert stored.messages[-1].content == "SELECT 1;"
    assert stored.title  # auto-derived


@pytest.mark.unit
def test_continue_existing_conversation_appends() -> None:
    use_case, repo = _use_case()
    first = use_case.execute(ConverseRequestDTO(prompt="one"))

    use_case.execute(ConverseRequestDTO(prompt="two", conversation_id=first.conversation_id))

    stored = repo.get(first.conversation_id)
    assert stored is not None
    user_turns = [m.content for m in stored.messages if m.role is Role.USER]
    assert user_turns == ["one", "two"]


@pytest.mark.unit
def test_unknown_conversation_raises_not_found() -> None:
    use_case, _ = _use_case()
    with pytest.raises(NotFoundError):
        use_case.execute(ConverseRequestDTO(prompt="x", conversation_id="does-not-exist"))
