import pytest
from click.testing import CliRunner

from novel.cli.main import cli
from novel.config.settings import get_settings

@pytest.fixture
def cli_env(tmp_path, monkeypatch):
    """Setup a temporary environment for CLI tests."""
    novels_dir = tmp_path / "novels"
    templates_dir = tmp_path / "templates"
    
    default_template = templates_dir / "default"
    default_template.mkdir(parents=True)
    (default_template / "template.yaml").write_text("description: CLI Template\ntemplate_version: '1.0'")
    (default_template / "project.yaml").write_text("name: ''\nauthor: ''\ngenre: ''")
    
    monkeypatch.setenv("PROJECTS_DIR", str(novels_dir))
    monkeypatch.setenv("TEMPLATES_DIR", str(templates_dir))
    monkeypatch.setenv("OPENAI_API_KEY", "dummy_key")
    monkeypatch.setenv("PVD_DOTENV_IGNORE", "1")
    get_settings.cache_clear()
    
    return tmp_path

def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "novel" in result.output.lower()

def test_cli_new_project(cli_env):
    runner = CliRunner()
    result = runner.invoke(cli, ["new", "MyCLINovel", "--author", "Tester"])
    
    assert result.exit_code == 0
    assert "successfully" in result.output.lower() or "✅" in result.output
    
    settings = get_settings()
    projects = list((cli_env / "novels").iterdir())
    assert len(projects) == 1
    assert "nv_" in projects[0].name

def test_cli_list_projects(cli_env):
    runner = CliRunner()
    # Create one first
    runner.invoke(cli, ["new", "ListMe"])
    
    result = runner.invoke(cli, ["list"])
    assert result.exit_code == 0
    assert "ListMe" in result.output
