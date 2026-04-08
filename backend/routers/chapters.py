from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.config import get_project_root
from backend.services.yaml_service import read_yaml, write_yaml, read_markdown, write_markdown

router = APIRouter(prefix="/api/chapters", tags=["chapters"])


class ChapterCreate(BaseModel):
    id: str
    title: str
    pov: str = ""
    goal: str = ""
    word_target: int = 3000
    content: str = ""


class ChapterContentUpdate(BaseModel):
    content: str


class ChapterMetaUpdate(BaseModel):
    title: str | None = None
    status: str | None = None
    pov: str | None = None
    goal: str | None = None
    word_target: int | None = None
    hooks_planted: list[str] | None = None
    hooks_revealed: list[str] | None = None
    summary: str | None = None
    characters_involved: list[str] | None = None


def _index_path():
    return get_project_root() / "chapters" / "index.yaml"


def _chapter_md(chapter_id: str):
    return get_project_root() / "chapters" / f"{chapter_id}.md"


@router.get("")
async def list_chapters():
    """Return chapter index."""
    index = read_yaml(_index_path())
    return {"chapters": index.get("chapters", [])}


@router.get("/{chapter_id}")
async def get_chapter(chapter_id: str):
    """Return chapter metadata + prose content."""
    index = read_yaml(_index_path())
    meta = None
    for ch in index.get("chapters", []):
        if ch.get("id") == chapter_id:
            meta = dict(ch)
            break
    if meta is None:
        raise HTTPException(status_code=404, detail=f"Chapter not found: {chapter_id}")

    content = read_markdown(_chapter_md(chapter_id))
    return {"meta": meta, "content": content}


@router.post("")
async def create_chapter(req: ChapterCreate):
    """Create a new chapter markdown file and add to index."""
    md_path = _chapter_md(req.id)
    if md_path.exists():
        raise HTTPException(status_code=409, detail=f"Chapter already exists: {req.id}")

    write_markdown(md_path, req.content)

    index_path = _index_path()
    index = read_yaml(index_path)
    chapters = index.get("chapters", [])
    chapters.append({
        "id": req.id,
        "title": req.title,
        "status": "outline",
        "pov": req.pov,
        "goal": req.goal,
        "word_target": req.word_target,
        "word_actual": len(req.content),
        "hooks_planted": [],
        "hooks_revealed": [],
        "summary": "",
        "characters_involved": [],
    })
    index["chapters"] = chapters
    write_yaml(index_path, index)
    return {"ok": True, "id": req.id}


@router.put("/{chapter_id}")
async def update_chapter_content(chapter_id: str, req: ChapterContentUpdate):
    """Update chapter prose content."""
    md_path = _chapter_md(chapter_id)

    # Verify chapter exists in index
    index = read_yaml(_index_path())
    found = any(ch.get("id") == chapter_id for ch in index.get("chapters", []))
    if not found:
        raise HTTPException(status_code=404, detail=f"Chapter not found: {chapter_id}")

    write_markdown(md_path, req.content)

    # Update word_actual in index
    index_path = _index_path()
    index = read_yaml(index_path)
    for ch in index.get("chapters", []):
        if ch.get("id") == chapter_id:
            ch["word_actual"] = len(req.content)
            break
    write_yaml(index_path, index)
    return {"ok": True, "id": chapter_id}


@router.put("/{chapter_id}/meta")
async def update_chapter_meta(chapter_id: str, req: ChapterMetaUpdate):
    """Update chapter metadata in the index."""
    index_path = _index_path()
    index = read_yaml(index_path)
    target = None
    for ch in index.get("chapters", []):
        if ch.get("id") == chapter_id:
            target = ch
            break
    if target is None:
        raise HTTPException(status_code=404, detail=f"Chapter not found: {chapter_id}")

    for field in ("title", "status", "pov", "goal", "word_target",
                  "hooks_planted", "hooks_revealed", "summary", "characters_involved"):
        val = getattr(req, field)
        if val is not None:
            target[field] = val

    write_yaml(index_path, index)
    return {"ok": True, "id": chapter_id}


@router.delete("/{chapter_id}")
async def delete_chapter(chapter_id: str):
    """Delete chapter markdown and remove from index."""
    md_path = _chapter_md(chapter_id)
    if md_path.exists():
        md_path.unlink()

    index_path = _index_path()
    index = read_yaml(index_path)
    index["chapters"] = [ch for ch in index.get("chapters", []) if ch.get("id") != chapter_id]
    write_yaml(index_path, index)
    return {"ok": True, "id": chapter_id}
