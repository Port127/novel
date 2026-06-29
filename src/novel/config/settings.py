from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from functools import lru_cache

class Settings(BaseSettings):
    OPENAI_API_KEY: SecretStr | None = None
    PROJECTS_DIR: str = "./novels"
    TEMPLATES_DIR: str = "./templates"
    DATABASE_URL: str | None = None
    NOVEL_MATERIAL_DIR: str | None = None
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()
