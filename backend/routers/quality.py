from fastapi import APIRouter

from backend.config import get_project_root
from backend.services.yaml_service import read_yaml

router = APIRouter(prefix="/api/quality", tags=["quality"])


@router.get("/ai-trace")
async def get_ai_trace():
    """Read the AI trace report."""
    data = read_yaml(get_project_root() / "quality" / "ai_trace_report.yaml")
    return {"reports": data.get("reports", [])}
