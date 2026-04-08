from urllib.parse import unquote

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.config import get_project_root
from backend.services.yaml_service import read_yaml, write_yaml

router = APIRouter(prefix="/api/characters", tags=["characters"])


class CharacterCreate(BaseModel):
    name: str
    role: str = "minor"
    archetype: str = ""
    first_appearance: str = ""
    affiliation: list[str] = []
    data: dict = {}


class CharacterUpdate(BaseModel):
    role: str | None = None
    archetype: str | None = None
    first_appearance: str | None = None
    affiliation: list[str] | None = None
    data: dict | None = None


def _index_path():
    return get_project_root() / "characters" / "character_index.yaml"


def _char_path(name: str):
    return get_project_root() / "characters" / f"{name}.yaml"


@router.get("")
async def list_characters():
    """Return the character index entries."""
    index = read_yaml(_index_path())
    return {"entries": index.get("entries", []), "total": index.get("total", 0)}


@router.get("/{name}")
async def get_character(name: str):
    """Read a single character's full YAML data."""
    name = unquote(name)
    path = _char_path(name)
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Character not found: {name}")
    data = read_yaml(path)
    return data


@router.post("")
async def create_character(req: CharacterCreate):
    """Create a new character file and add to index."""
    path = _char_path(req.name)
    if path.exists():
        raise HTTPException(status_code=409, detail=f"Character already exists: {req.name}")

    char_data = {
        "name": req.name,
        "role": req.role,
        "archetype": req.archetype,
        "first_appearance": req.first_appearance,
        "affiliation": req.affiliation,
        **(req.data or {}),
    }
    write_yaml(path, char_data)

    index_path = _index_path()
    index = read_yaml(index_path)
    entries = index.get("entries", [])
    entries.append({
        "name": req.name,
        "role": req.role,
        "archetype": req.archetype,
        "file": f"characters/{req.name}.yaml",
        "first_appearance": req.first_appearance,
        "affiliation": req.affiliation,
        "scene_count": 0,
    })
    index["entries"] = entries
    index["total"] = len(entries)
    write_yaml(index_path, index)
    return {"ok": True, "name": req.name}


@router.put("/{name}")
async def update_character(name: str, req: CharacterUpdate):
    """Update a character's YAML file and index entry."""
    name = unquote(name)
    path = _char_path(name)
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Character not found: {name}")

    char_data = read_yaml(path)
    if req.data is not None:
        char_data.update(req.data)
    if req.role is not None:
        char_data["role"] = req.role
    if req.archetype is not None:
        char_data["archetype"] = req.archetype
    if req.first_appearance is not None:
        char_data["first_appearance"] = req.first_appearance
    if req.affiliation is not None:
        char_data["affiliation"] = req.affiliation
    write_yaml(path, char_data)

    # Update index entry
    index_path = _index_path()
    index = read_yaml(index_path)
    for entry in index.get("entries", []):
        if entry.get("name") == name:
            if req.role is not None:
                entry["role"] = req.role
            if req.archetype is not None:
                entry["archetype"] = req.archetype
            if req.first_appearance is not None:
                entry["first_appearance"] = req.first_appearance
            if req.affiliation is not None:
                entry["affiliation"] = req.affiliation
            break
    write_yaml(index_path, index)
    return {"ok": True, "name": name}


@router.delete("/{name}")
async def delete_character(name: str):
    """Delete a character file and remove from index."""
    name = unquote(name)
    path = _char_path(name)
    if path.exists():
        path.unlink()

    index_path = _index_path()
    index = read_yaml(index_path)
    entries = [e for e in index.get("entries", []) if e.get("name") != name]
    index["entries"] = entries
    index["total"] = len(entries)
    write_yaml(index_path, index)
    return {"ok": True, "name": name}
