import random
import string
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import yaml

from novel.config.settings import get_settings

class ProjectManager:
    """Manages the lifecycle of novel projects."""
    
    def __init__(self):
        self.settings = get_settings()
        self.novels_dir = Path(self.settings.PROJECTS_DIR)
        self.templates_dir = Path(self.settings.TEMPLATES_DIR)

    def generate_project_id(self) -> str:
        """Generate a unique project ID: nv_{YYYYMMDD}_{random4}"""
        date_str = datetime.now().strftime("%Y%m%d")
        random_str = "".join(random.choices(string.ascii_lowercase + string.digits, k=4))
        return f"nv_{date_str}_{random_str}"

    def list_available_templates(self) -> List[Dict[str, str]]:
        """List all available templates in the templates directory."""
        if not self.templates_dir.exists():
            return []

        templates = []
        for template_dir in self.templates_dir.iterdir():
            if template_dir.is_dir():
                template_yaml = template_dir / "template.yaml"
                if template_yaml.exists():
                    with open(template_yaml, encoding="utf-8") as f:
                        data = yaml.safe_load(f) or {}
                    templates.append({
                        "name": template_dir.name,
                        "description": data.get("description", ""),
                        "version": data.get("template_version", "1.0")
                    })
        return templates

    def create_project(
        self, 
        name: str, 
        genre: str = "修仙", 
        author: str = "匿名", 
        template: str = "default"
    ) -> Optional[str]:
        """Create a new project from a template."""
        template_dir = self.templates_dir / template
        if not template_dir.exists():
            raise ValueError(f"Template '{template}' does not exist.")

        project_id = self.generate_project_id()
        project_dir = self.novels_dir / project_id

        # Ensure parent directory exists
        self.novels_dir.mkdir(parents=True, exist_ok=True)

        # Copy template structure
        shutil.copytree(template_dir, project_dir)

        # Create required dynamic directories
        (project_dir / "drafts").mkdir(exist_ok=True)
        (project_dir / "exports").mkdir(exist_ok=True)
        (project_dir / "history").mkdir(exist_ok=True)

        # Update project.yaml
        project_yaml_path = project_dir / "project.yaml"
        if project_yaml_path.exists():
            with open(project_yaml_path, encoding="utf-8") as f:
                project_data = yaml.safe_load(f) or {}
        else:
            project_data = {}

        today = datetime.now().strftime("%Y-%m-%d")
        project_data.update({
            "project_id": project_id,
            "name": name,
            "author": author,
            "genre": genre,
            "created": today,
            "updated": today
        })

        with open(project_yaml_path, "w", encoding="utf-8") as f:
            yaml.dump(project_data, f, allow_unicode=True, default_flow_style=False)

        return project_id

    def list_projects(self) -> List[Dict[str, str]]:
        """List all novel projects in the projects directory."""
        if not self.novels_dir.exists():
            return []

        projects = []
        for project_dir in sorted(self.novels_dir.iterdir()):
            if project_dir.is_dir() and project_dir.name.startswith("nv_"):
                project_yaml = project_dir / "project.yaml"
                if project_yaml.exists():
                    with open(project_yaml, encoding="utf-8") as f:
                        data = yaml.safe_load(f) or {}
                    projects.append({
                        "id": project_dir.name,
                        "name": data.get("name", "Unknown"),
                        "genre": data.get("genre", "Unknown"),
                        "status": data.get("status", "Unknown"),
                        "chapters": data.get("stats", {}).get("chapters_written", 0),
                        "words": data.get("stats", {}).get("words_total", 0),
                        "pipeline_stage": data.get("pipeline_status", {}).get("current_stage", 0),
                    })
        return projects

    def delete_project(self, project_id: str) -> bool:
        """Delete a project by its ID."""
        project_dir = self.novels_dir / project_id
        if not project_dir.exists():
            return False

        shutil.rmtree(project_dir)
        return True

    def show_project(self, project_id: str) -> Optional[Dict]:
        """Show details for a specific project."""
        project_dir = self.novels_dir / project_id
        if not project_dir.exists():
            return None

        project_yaml = project_dir / "project.yaml"
        if not project_yaml.exists():
            return None

        with open(project_yaml, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
            
        return data
