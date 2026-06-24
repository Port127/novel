from pydantic import BaseModel
from typing import Callable, Awaitable

class Skill(BaseModel):
    name: str
    trigger_phase: str
    system_prompt: str
    evaluation_criteria: list[str] = []

async def run_skill_pipeline(
    skills: list[Skill], 
    initial_text: str, 
    llm_func: Callable[[str, str], Awaitable[str]]
) -> str:
    current_text = initial_text
    for skill in skills:
        current_text = await llm_func(current_text, skill.system_prompt)
    return current_text
