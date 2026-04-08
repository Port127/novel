from fastapi import APIRouter
from pydantic import BaseModel

from backend.config import get_project_root
from backend.services.yaml_service import read_yaml, write_yaml

router = APIRouter(prefix="/api/timeline", tags=["timeline"])


class TimelineEvent(BaseModel):
    time: str
    event: str
    chapter: str = ""
    characters: list[str] = []
    notes: str = ""


@router.get("")
async def get_timeline():
    """Read the main timeline."""
    data = read_yaml(get_project_root() / "timeline" / "main.yaml")
    return {"events": data.get("events", []), "threads": data.get("threads", [])}


@router.post("")
async def add_event(req: TimelineEvent):
    """Append an event to the main timeline."""
    path = get_project_root() / "timeline" / "main.yaml"
    data = read_yaml(path)
    events = data.get("events", [])
    events.append({
        "time": req.time,
        "event": req.event,
        "chapter": req.chapter,
        "characters": req.characters,
        "notes": req.notes,
    })
    data["events"] = events
    write_yaml(path, data)
    return {"ok": True, "count": len(events)}
