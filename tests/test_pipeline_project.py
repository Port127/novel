import os
import shutil
from pathlib import Path
import pytest
import yaml

from novel.pipeline.project_manager import ProjectManager
from novel.config.settings import get_settings

@pytest.fixture
def temp_project_env(tmp_path, monkeypatch):
    """Setup a temporary directory for novels and templates."""
    novels_dir = tmp_path / "novels"
    templates_dir = tmp_path / "templates"
    
    # Create a dummy default template
    default_template = templates_dir / "default"
    default_template.mkdir(parents=True)
    
    template_yaml = default_template / "template.yaml"
    template_yaml.write_text("description: Default Template\ntemplate_version: '1.0'")
    
    project_yaml = default_template / "project.yaml"
    project_yaml.write_text("name: ''\nauthor: ''\ngenre: ''")
    
    # Override settings
    monkeypatch.setenv("PROJECTS_DIR", str(novels_dir))
    monkeypatch.setenv("TEMPLATES_DIR", str(templates_dir))
    monkeypatch.setenv("OPENAI_API_KEY", "dummy_key")
    monkeypatch.setenv("PVD_DOTENV_IGNORE", "1")
    get_settings.cache_clear()
    
    return tmp_path

def test_list_available_templates(temp_project_env):
    pm = ProjectManager()
    templates = pm.list_available_templates()
    
    assert len(templates) == 1
    assert templates[0]["name"] == "default"
    assert templates[0]["description"] == "Default Template"

def test_create_project(temp_project_env):
    pm = ProjectManager()
    project_id = pm.create_project(name="Test Book", genre="Fantasy", author="AI", template="default")
    
    assert project_id is not None
    assert project_id.startswith("nv_")
    
    settings = get_settings()
    project_dir = Path(settings.PROJECTS_DIR) / project_id
    
    assert project_dir.exists()
    assert (project_dir / "drafts").exists()
    assert (project_dir / "history").exists()
    
    # Check if project.yaml was updated
    with open(project_dir / "project.yaml", "r") as f:
        data = yaml.safe_load(f)
        
    assert data["name"] == "Test Book"
    assert data["genre"] == "Fantasy"
    assert data["author"] == "AI"
    assert data["project_id"] == project_id

def test_list_and_delete_project(temp_project_env):
    pm = ProjectManager()
    project_id = pm.create_project(name="Book 1")
    
    projects = pm.list_projects()
    assert len(projects) == 1
    assert projects[0]["id"] == project_id
    assert projects[0]["name"] == "Book 1"
    
    success = pm.delete_project(project_id)
    assert success is True
    
    projects = pm.list_projects()
    assert len(projects) == 0
