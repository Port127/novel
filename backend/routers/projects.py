from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.config import WORKSPACE_ROOT, get_current_project, get_project_root
from backend.services.yaml_service import read_yaml, write_yaml

router = APIRouter(prefix="/api/projects", tags=["projects"])


class SwitchRequest(BaseModel):
    project_name: str
    project_path: str


@router.get("")
async def list_projects():
    """List all projects, enriched with each project's meta and state."""
    projects_data = read_yaml(WORKSPACE_ROOT / ".projects.yaml")
    projects_list = projects_data.get("projects", [])
    if not projects_list:
        # Fallback: scan the projects/ directory
        projects_dir = WORKSPACE_ROOT / "projects"
        if projects_dir.exists():
            projects_list = [
                {"name": d.name, "path": f"projects/{d.name}"}
                for d in sorted(projects_dir.iterdir())
                if d.is_dir() and (d / ".novel").exists()
            ]

    result = []
    for proj in projects_list:
        name = proj.get("name", "") if isinstance(proj, dict) else str(proj)
        path = proj.get("path", f"projects/{name}") if isinstance(proj, dict) else f"projects/{name}"
        proj_dir = WORKSPACE_ROOT / path
        meta = read_yaml(proj_dir / ".novel" / "meta.yaml")
        state = read_yaml(proj_dir / ".novel" / "state.yaml")
        result.append({
            "name": name,
            "path": path,
            "meta": meta,
            "state": state,
        })
    return result


@router.get("/current")
async def get_current():
    """Get current project's meta and state."""
    info = get_current_project()
    proj_root = get_project_root()
    if not proj_root.exists():
        return {"current": info, "meta": {}, "state": {}}
    meta = read_yaml(proj_root / ".novel" / "meta.yaml")
    state = read_yaml(proj_root / ".novel" / "state.yaml")
    return {"current": info, "meta": meta, "state": state}


@router.post("/switch")
async def switch_project(req: SwitchRequest):
    """Switch the current active project."""
    proj_dir = WORKSPACE_ROOT / req.project_path
    if not proj_dir.exists():
        raise HTTPException(status_code=404, detail=f"Project path not found: {req.project_path}")
    write_yaml(WORKSPACE_ROOT / ".current.yaml", {
        "current_project": req.project_name,
        "current_path": req.project_path,
    })
    return {"ok": True, "current_project": req.project_name}
