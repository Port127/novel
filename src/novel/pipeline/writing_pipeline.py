import os
from pathlib import Path
from novel.core.llm.client import generate_text
from novel.core.workflow.qa_loop import run_qa_loop
from novel.pipeline.project_manager import ProjectManager

async def write_new_chapter(project_id: str, chapter_id: str, prompt: str = "") -> str:
    pm = ProjectManager()
    project_dir = pm.novels_dir / project_id
    if not project_dir.exists():
        raise ValueError(f"Project {project_id} not found.")
        
    settings_dir = project_dir / "settings"
    content_dir = project_dir / "content" / "chapters"
    content_dir.mkdir(parents=True, exist_ok=True)
    
    context = ""
    for f in ["worldbuilding.yaml", "characters.yaml", "outline.yaml"]:
        path = settings_dir / f
        if path.exists():
            context += f"\n--- {f} ---\n" + path.read_text(encoding="utf-8")
            
    sys_prompt = "You are a professional web novel writer. Write the chapter content clearly, with good pacing and dialogue."
    user_prompt = f"Context:\n{context}\n\nWrite Chapter {chapter_id}. Additional instructions: {prompt}"
    
    draft = await generate_text(user_prompt, system=sys_prompt)
    final_text = await run_qa_loop(draft, context)
    
    with open(content_dir / f"chapter_{chapter_id}.md", "w", encoding="utf-8") as f:
        f.write(final_text)
    return final_text
