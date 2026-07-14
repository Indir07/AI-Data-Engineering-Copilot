"""Unit tests for the typed Settings object."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from copilot.config.settings import Settings


@pytest.mark.unit
def test_defaults_are_sane() -> None:
    s = Settings()
    assert s.app_env == "local"
    assert s.app_port == 8000
    assert s.llm_model == "qwen2.5-coder:7b-instruct"
    assert s.vector_store == "chroma"
    assert s.is_prod is False


@pytest.mark.unit
def test_overrides_apply() -> None:
    s = Settings(app_env="prod", llm_temperature=0.7)
    assert s.is_prod is True
    assert s.llm_temperature == 0.7


@pytest.mark.unit
def test_invalid_temperature_rejected() -> None:
    with pytest.raises(ValidationError):
        Settings(llm_temperature=5.0)  # outside [0, 2]


@pytest.mark.unit
def test_invalid_env_rejected() -> None:
    with pytest.raises(ValidationError):
        Settings(app_env="staging")  # not in Literal
