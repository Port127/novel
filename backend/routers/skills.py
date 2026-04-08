from pathlib import Path
import re

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

from backend.config import WORKSPACE_ROOT, get_project_root
from backend.services.llm_service import chat_stream
from backend.services.yaml_service import read_yaml, read_markdown

router = APIRouter(prefix="/api/skills", tags=["skills"])


class SkillExecuteRequest(BaseModel):
    skill_name: str
    arguments: str = ""
    context_files: list[str] = []


def _skills_dir() -> Path:
    return WORKSPACE_ROOT / ".claude" / "skills"


def _parse_skill_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter from a SKILL.md file."""
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    # Simple key-value extraction without importing yaml again in hot path
    result = {}
    for line in match.group(1).split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            result[key.strip()] = val.strip().strip('"').strip("'")
    return result


def _categorize_skill(name: str) -> str:
    """Infer a category from the skill name prefix."""
    prefixes = {
        "chapter": "chapters",
        "character": "characters",
        "plot": "plot",
        "relationship": "relationships",
        "setting": "worldbuilding",
        "worldbuilding": "worldbuilding",
        "timeline": "timeline",
        "pipeline": "pipeline",
        "novel": "project",
        "style": "style",
        "material": "material",
        "inspiration": "compliance",
        "anti-ai": "quality",
        "voice": "quality",
        "consistency": "quality",
        "scene": "scenes",
        "draft": "drafting",
        "rewrite": "style",
        "skill": "system",
        "project": "project",
    }
    for prefix, cat in prefixes.items():
        if name.startswith(prefix):
            return cat
    return "other"


@router.get("")
async def list_skills():
    """Scan .claude/skills/ and return list of available skills."""
    skills_dir = _skills_dir()
    if not skills_dir.exists():
        return {"skills": []}

    skills = []
    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        text = skill_file.read_text(encoding="utf-8")
        meta = _parse_skill_frontmatter(text)
        skills.append({
            "name": meta.get("name", skill_dir.name),
            "description": meta.get("description", ""),
            "when_to_use": meta.get("when_to_use", ""),
            "argument_hint": meta.get("argument-hint", ""),
            "category": _categorize_skill(skill_dir.name),
        })
    return {"skills": skills}


@router.post("/execute")
async def execute_skill(req: SkillExecuteRequest):
    """Read the skill's SKILL.md, gather project context, call LLM, stream response."""
    skill_file = _skills_dir() / req.skill_name / "SKILL.md"
    if not skill_file.exists():
        raise HTTPException(status_code=404, detail=f"Skill not found: {req.skill_name}")

    skill_content = skill_file.read_text(encoding="utf-8")
    proj_root = get_project_root()

    # Gather context files
    context_parts = []
    for rel_path in req.context_files:
        full = proj_root / rel_path
        if full.exists() and full.is_file():
            content = full.read_text(encoding="utf-8")
            context_parts.append(f"--- {rel_path} ---\n{content}")

    # Auto-include basic project context
    for auto_file in [".novel/meta.yaml", ".novel/state.yaml"]:
        p = proj_root / auto_file
        if p.exists():
            context_parts.append(f"--- {auto_file} ---\n{p.read_text(encoding='utf-8')}")

    context_block = "\n\n".join(context_parts) if context_parts else "(no project files loaded)"

    system_prompt = (
        "You are an AI novel-writing assistant. Follow the skill instructions precisely. "
        "Respond in Chinese unless the user asks otherwise."
    )

    user_prompt = (
        f"## Skill Instructions\n\n{skill_content}\n\n"
        f"## Arguments\n\n{req.arguments or '(none)'}\n\n"
        f"## Project Context\n\n{context_block}\n\n"
        f"Execute this skill now."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    async def event_generator():
        async for chunk in chat_stream(messages):
            yield {"event": "message", "data": chunk}
        yield {"event": "done", "data": "[DONE]"}

    return EventSourceResponse(event_generator())
