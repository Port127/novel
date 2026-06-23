import yaml
from pathlib import Path

def build_chapter_context(project_dir: str) -> str:
    proj_path = Path(project_dir)
    context_parts = []
    wb_dir = proj_path / "settings" / "worldbuilding"
    if wb_dir.exists():
        for file in wb_dir.glob("*.yaml"):
            with open(file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                context_parts.append(f"[{file.name}]\n{yaml.dump(data, allow_unicode=True)}")
    return "\n\n".join(context_parts)
