import json
import asyncio
from typing import Any
from pydantic import BaseModel, Field
from novel.config.settings import get_settings

class MaterialSearchResult(BaseModel):
    id: str
    text: str
    score: float = 0.0
    metadata: dict[str, Any] = Field(default_factory=dict)

class MaterialServiceError(Exception):
    pass

class MaterialClient:
    def __init__(self, novel_material_dir: str | None = None):
        self.material_dir = novel_material_dir
        
    async def search_insight(self, query: str, limit: int = 5) -> list[MaterialSearchResult]:
        if not self.material_dir:
            return []
            
        cmd = ["nm", "search", "insight", query, "--limit", str(limit), "--json"]
        
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.material_dir
            )
            stdout, stderr = await process.communicate()
        except Exception as e:
            raise MaterialServiceError(f"CLI execution failed: {e}")
            
        if process.returncode != 0:
            raise MaterialServiceError(f"CLI execution failed with code {process.returncode}: {stderr.decode('utf-8')}")
            
        try:
            data = json.loads(stdout.decode('utf-8'))
            results = []
            for item in data:
                # Based on novel-material json format
                results.append(MaterialSearchResult(
                    id=item.get("id", item.get("material_id", "unknown")),
                    text=item.get("text", item.get("content", "")),
                    score=float(item.get("score", 0.0)),
                    metadata=item.get("metadata", {})
                ))
            return results
        except json.JSONDecodeError as e:
            raise MaterialServiceError(f"Failed to parse JSON response: {e}")

async def build_material_context(query: str, limit: int = 5) -> str:
    settings = get_settings()
    client = MaterialClient(settings.NOVEL_MATERIAL_DIR)
    
    try:
        results = await client.search_insight(query, limit)
    except Exception:
        return ""
        
    if not results:
        return ""
        
    context_parts = []
    for res in results:
        meta_str = ", ".join(f"{k}: {v}" for k, v in res.metadata.items())
        block = f"[Reference Material: {res.id}]\n{res.text}"
        if meta_str:
            block += f"\n(Metadata: {meta_str})"
        context_parts.append(block)
        
    return "\n\n".join(context_parts)
