import os
import yaml
from pathlib import Path
from pydantic import BaseModel
from novel.core.llm.client import generate_text
from novel.pipeline.project_manager import ProjectManager

async def generate_worldbuilding(project_id: str, prompt: str) -> str:
    pm = ProjectManager()
    project_dir = pm.novels_dir / project_id
    if not project_dir.exists():
        raise ValueError(f"Project {project_id} not found.")
        
    settings_dir = project_dir / "settings"
    settings_dir.mkdir(parents=True, exist_ok=True)
    
    sys_prompt = "You are an expert novel worldbuilder. Output ONLY raw YAML containing power_system, factions, locations, and lore. Do not use markdown blocks like ```yaml."
    user_prompt = f"Create worldbuilding settings based on this prompt: {prompt}"
    
    yaml_text = await generate_text(user_prompt, system=sys_prompt)
    yaml_text = yaml_text.removeprefix("```yaml").removesuffix("```").strip()
    
    with open(settings_dir / "worldbuilding.yaml", "w", encoding="utf-8") as f:
        f.write(yaml_text)
    return yaml_text

async def generate_characters(project_id: str, prompt: str) -> str:
    pm = ProjectManager()
    project_dir = pm.novels_dir / project_id
    if not project_dir.exists():
        raise ValueError(f"Project {project_id} not found.")
        
    settings_dir = project_dir / "settings"
    settings_dir.mkdir(parents=True, exist_ok=True)
    
    world_context = ""
    world_file = settings_dir / "worldbuilding.yaml"
    if world_file.exists():
        world_context = world_file.read_text(encoding="utf-8")
        
    sys_prompt = "You are an expert novel character designer. Output ONLY raw YAML containing protagonist, antagonist, supporting characters, and relationships. Do not use markdown blocks."
    user_prompt = f"World context:\n{world_context}\n\nCreate character settings based on this prompt: {prompt}"
    
    yaml_text = await generate_text(user_prompt, system=sys_prompt)
    yaml_text = yaml_text.removeprefix("```yaml").removesuffix("```").strip()
    
    with open(settings_dir / "characters.yaml", "w", encoding="utf-8") as f:
        f.write(yaml_text)
    return yaml_text

async def generate_outline(project_id: str) -> str:
    pm = ProjectManager()
    project_dir = pm.novels_dir / project_id
    if not project_dir.exists():
        raise ValueError(f"Project {project_id} not found.")
        
    settings_dir = project_dir / "settings"
    settings_dir.mkdir(parents=True, exist_ok=True)
    
    context = ""
    if (settings_dir / "worldbuilding.yaml").exists():
        context += (settings_dir / "worldbuilding.yaml").read_text(encoding="utf-8") + "\n"
    if (settings_dir / "characters.yaml").exists():
        context += (settings_dir / "characters.yaml").read_text(encoding="utf-8") + "\n"
        
    sys_prompt = "You are an expert novel outliner. Output ONLY raw YAML containing premise, acts, plotlines, and hooks. Do not use markdown blocks."
    user_prompt = f"Context:\n{context}\n\nCreate a full novel outline."
    
    yaml_text = await generate_text(user_prompt, system=sys_prompt)
    yaml_text = yaml_text.removeprefix("```yaml").removesuffix("```").strip()
    
    with open(settings_dir / "outline.yaml", "w", encoding="utf-8") as f:
        f.write(yaml_text)
    return yaml_text
