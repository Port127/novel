import pytest
from pydantic import ValidationError
from novel.config.settings import get_settings

def test_settings_requires_openai_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    with pytest.raises(ValidationError):
        get_settings()

def test_settings_loads_openai_api_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-123")
    settings = get_settings()
    assert settings.OPENAI_API_KEY.get_secret_value() == "sk-test-123"
