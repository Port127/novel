from fastapi import APIRouter
from pydantic import BaseModel

from backend.config import get_project_root
from backend.services.yaml_service import read_yaml, read_markdown, write_markdown

router = APIRouter(prefix="/api/plot", tags=["plot"])


class OutlineUpdate(BaseModel):
    content: str


@router.get("/outline")
async def get_outline():
    """Read outline.md and outline.yaml, return both."""
    root = get_project_root()
    md = read_markdown(root / "plot" / "outline.md")
    yaml_data = read_yaml(root / "plot" / "outline.yaml")
    return {"markdown": md, "structured": yaml_data}


@router.put("/outline")
async def update_outline(req: OutlineUpdate):
    """Write outline markdown content."""
    root = get_project_root()
    write_markdown(root / "plot" / "outline.md", req.content)
    return {"ok": True}
