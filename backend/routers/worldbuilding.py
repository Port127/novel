from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.config import get_project_root
from backend.services.yaml_service import read_yaml, write_yaml

router = APIRouter(prefix="/api/worldbuilding", tags=["worldbuilding"])


class EntryCreate(BaseModel):
    id: str
    name: str
    category: str = "world_rule"
    status: str = "tentative"
    data: dict = {}


class EntryUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
    status: str | None = None
    data: dict | None = None


def _index_path():
    return get_project_root() / "worldbuilding" / "worldbuilding.yaml"


def _entry_path(entry_id: str):
    return get_project_root() / "worldbuilding" / "entries" / f"{entry_id}.yaml"


@router.get("")
async def get_worldbuilding():
    """Return the worldbuilding index."""
    return read_yaml(_index_path())


@router.get("/entries/{entry_id}")
async def get_entry(entry_id: str):
    """Read a specific worldbuilding entry."""
    path = _entry_path(entry_id)
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Entry not found: {entry_id}")
    return read_yaml(path)


@router.post("/entries")
async def create_entry(req: EntryCreate):
    """Create a worldbuilding entry and add to index."""
    path = _entry_path(req.id)
    if path.exists():
        raise HTTPException(status_code=409, detail=f"Entry already exists: {req.id}")

    entry_data = {
        "id": req.id,
        "name": req.name,
        "category": req.category,
        "status": req.status,
        **(req.data or {}),
    }
    write_yaml(path, entry_data)

    index_path = _index_path()
    index = read_yaml(index_path)
    entries = index.get("entries", [])
    entries.append({
        "id": req.id,
        "name": req.name,
        "category": req.category,
        "status": req.status,
        "file": f"entries/{req.id}.yaml",
    })
    index["entries"] = entries
    write_yaml(index_path, index)
    return {"ok": True, "id": req.id}


@router.put("/entries/{entry_id}")
async def update_entry(entry_id: str, req: EntryUpdate):
    """Update a worldbuilding entry and its index record."""
    path = _entry_path(entry_id)
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Entry not found: {entry_id}")

    data = read_yaml(path)
    if req.data is not None:
        data.update(req.data)
    if req.name is not None:
        data["name"] = req.name
    if req.category is not None:
        data["category"] = req.category
    if req.status is not None:
        data["status"] = req.status
    write_yaml(path, data)

    index_path = _index_path()
    index = read_yaml(index_path)
    for entry in index.get("entries", []):
        if entry.get("id") == entry_id:
            if req.name is not None:
                entry["name"] = req.name
            if req.category is not None:
                entry["category"] = req.category
            if req.status is not None:
                entry["status"] = req.status
            break
    write_yaml(index_path, index)
    return {"ok": True, "id": entry_id}


@router.delete("/entries/{entry_id}")
async def delete_entry(entry_id: str):
    """Delete a worldbuilding entry and remove from index."""
    path = _entry_path(entry_id)
    if path.exists():
        path.unlink()

    index_path = _index_path()
    index = read_yaml(index_path)
    index["entries"] = [e for e in index.get("entries", []) if e.get("id") != entry_id]
    write_yaml(index_path, index)
    return {"ok": True, "id": entry_id}
