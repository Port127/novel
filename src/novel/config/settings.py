from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings for Novel V2.
    Loads automatically from environment variables and .env file.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    OPENAI_API_KEY: SecretStr = Field(
        ...,
        description="OpenAI API Key for LLM generation"
    )
    
    ANTHROPIC_API_KEY: SecretStr | None = Field(
        default=None,
        description="Anthropic API Key for Claude generation (optional)"
    )
    
    PROJECTS_DIR: str = Field(
        default="./novels",
        description="Directory where all novel projects are stored"
    )
    
    TEMPLATES_DIR: str = Field(
        default="./templates",
        description="Directory where project templates are stored"
    )

from functools import lru_cache

@lru_cache
def get_settings() -> Settings:
    """Return a cached instance of Settings."""
    return Settings()
