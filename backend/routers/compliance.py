from fastapi import APIRouter

from backend.config import get_project_root
from backend.services.yaml_service import read_yaml

router = APIRouter(prefix="/api/compliance", tags=["compliance"])


@router.get("/inspirations")
async def get_inspirations():
    """Read the inspiration log."""
    data = read_yaml(get_project_root() / "compliance" / "inspiration_log.yaml")
    return {"entries": data.get("entries", [])}


@router.get("/risks")
async def get_risks():
    """Read the risk report."""
    data = read_yaml(get_project_root() / "compliance" / "risk_report.yaml")
    return {"entries": data.get("entries", [])}
