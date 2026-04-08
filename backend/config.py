from pathlib import Path
import json

from backend.services.yaml_service import read_yaml


# novel repo root: backend/ -> novel/
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent

LLM_CONFIG_PATH = Path(__file__).resolve().parent / "llm_config.json"


def get_current_project() -> dict:
    """Read .current.yaml from workspace root and return project info."""
    data = read_yaml(WORKSPACE_ROOT / ".current.yaml")
    if not data:
        return {"current_project": "", "current_path": ""}
    return {
        "current_project": data.get("current_project", ""),
        "current_path": data.get("current_path", ""),
    }


def get_project_root() -> Path:
    """Return the absolute path to the current project directory."""
    info = get_current_project()
    rel = info.get("current_path", "")
    if not rel:
        return WORKSPACE_ROOT / "projects"
    return WORKSPACE_ROOT / rel


def get_llm_config() -> dict:
    """Read LLM configuration from llm_config.json."""
    if not LLM_CONFIG_PATH.exists():
        return {
            "api_url": "https://api.openai.com/v1/chat/completions",
            "api_key": "",
            "model": "gpt-4o-mini",
            "temperature": 0.7,
            "max_tokens": 4096,
        }
    return json.loads(LLM_CONFIG_PATH.read_text(encoding="utf-8"))


def save_llm_config(config: dict) -> None:
    """Write LLM configuration to llm_config.json."""
    LLM_CONFIG_PATH.write_text(
        json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8"
    )
