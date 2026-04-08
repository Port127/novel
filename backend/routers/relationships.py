from fastapi import APIRouter

from backend.config import get_project_root
from backend.services.yaml_service import read_yaml

router = APIRouter(prefix="/api/relationships", tags=["relationships"])


@router.get("")
async def get_relationships():
    """Read the relationship graph."""
    data = read_yaml(get_project_root() / "characters" / "relations.yaml")
    return {
        "relations": data.get("relations", []),
        "total": data.get("total", 0),
    }


@router.get("/events")
async def get_relation_events():
    """Read relationship evolution events."""
    data = read_yaml(get_project_root() / "characters" / "relation_events.yaml")
    return {"events": data.get("events", [])}
