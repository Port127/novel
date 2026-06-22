import os
import pytest
from pydantic import ValidationError

# We will import Settings from our novel module
from novel.config.settings import Settings

def test_settings_load_from_env(monkeypatch):
    """Test that settings load correctly from environment variables."""
    monkeypatch.setenv("OPENAI_API_KEY", "test_openai_key")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test_anthropic_key")
    monkeypatch.setenv("PROJECTS_DIR", "./test_novels")
    
    # Avoid loading .env file during tests
    monkeypatch.setenv("PVD_DOTENV_IGNORE", "1")
    
    settings = Settings(_env_file=None)
    
    assert settings.OPENAI_API_KEY.get_secret_value() == "test_openai_key"
    assert settings.ANTHROPIC_API_KEY.get_secret_value() == "test_anthropic_key"
    assert settings.PROJECTS_DIR == "./test_novels"

def test_settings_missing_required_api_key(monkeypatch):
    """Test that a ValidationError is raised if OPENAI_API_KEY is missing."""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("PVD_DOTENV_IGNORE", "1")
    
    with pytest.raises(ValidationError) as exc_info:
        Settings(_env_file=None)
    
    assert "OPENAI_API_KEY" in str(exc_info.value)

def test_settings_defaults(monkeypatch):
    """Test that default values are applied when optional env vars are omitted."""
    monkeypatch.setenv("OPENAI_API_KEY", "test_openai_key")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("PROJECTS_DIR", raising=False)
    monkeypatch.setenv("PVD_DOTENV_IGNORE", "1")
    
    settings = Settings(_env_file=None)
    
    assert settings.OPENAI_API_KEY.get_secret_value() == "test_openai_key"
    assert settings.ANTHROPIC_API_KEY is None
    assert settings.PROJECTS_DIR == "./novels"
