import pytest
import json
from unittest.mock import AsyncMock, patch
from novel.core.memory.material_client import MaterialClient, MaterialSearchResult, MaterialServiceError, build_material_context

@pytest.fixture
def mock_subprocess_exec():
    with patch("asyncio.create_subprocess_exec") as mock_exec:
        yield mock_exec

@pytest.mark.asyncio
async def test_search_insight_success(mock_subprocess_exec, monkeypatch):
    monkeypatch.setenv("NOVEL_MATERIAL_DIR", "/fake/dir")
    
    # Mock the process returned by create_subprocess_exec
    mock_process = AsyncMock()
    
    mock_stdout_data = [
        {
            "id": "nm_001",
            "text": "This is a great insight.",
            "score": 0.95,
            "metadata": {"chapter": 1}
        }
    ]
    
    mock_process.communicate.return_value = (json.dumps(mock_stdout_data).encode("utf-8"), b"")
    mock_process.returncode = 0
    mock_subprocess_exec.return_value = mock_process
    
    client = MaterialClient("/fake/dir")
    results = await client.search_insight("test query", limit=1)
    
    assert len(results) == 1
    assert isinstance(results[0], MaterialSearchResult)
    assert results[0].id == "nm_001"
    assert results[0].text == "This is a great insight."
    assert results[0].score == 0.95
    assert results[0].metadata["chapter"] == 1
    
    # Check if subprocess was called correctly
    mock_subprocess_exec.assert_called_once()
    args, kwargs = mock_subprocess_exec.call_args
    assert args[0] == "nm"
    assert "search" in args
    assert "insight" in args
    assert kwargs.get("cwd") == "/fake/dir"

@pytest.mark.asyncio
async def test_search_insight_failure(mock_subprocess_exec, monkeypatch):
    monkeypatch.setenv("NOVEL_MATERIAL_DIR", "/fake/dir")
    
    mock_process = AsyncMock()
    mock_process.communicate.return_value = (b"", b"Error occurred")
    mock_process.returncode = 1
    mock_subprocess_exec.return_value = mock_process
    
    client = MaterialClient("/fake/dir")
    with pytest.raises(MaterialServiceError, match="CLI execution failed"):
        await client.search_insight("test query")

@pytest.mark.asyncio
async def test_search_insight_no_dir():
    client = MaterialClient(None)
    results = await client.search_insight("test query")
    assert results == []

@pytest.mark.asyncio
async def test_build_material_context_success(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("NOVEL_MATERIAL_DIR", "/fake/dir")
    
    async def mock_search_insight(self, query, limit=5):
        return [
            MaterialSearchResult(id="nm_001", text="Insight 1", score=0.9, metadata={"chapter": 1}),
            MaterialSearchResult(id="nm_002", text="Insight 2", score=0.8, metadata={})
        ]
        
    with patch.object(MaterialClient, "search_insight", new=mock_search_insight):
        context = await build_material_context("test query")
        
        assert "[Reference Material: nm_001]" in context
        assert "Insight 1" in context
        assert "chapter: 1" in context
        assert "[Reference Material: nm_002]" in context
        assert "Insight 2" in context

@pytest.mark.asyncio
async def test_build_material_context_no_dir(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setattr("novel.core.memory.material_client.get_settings", lambda: type("Settings", (), {"NOVEL_MATERIAL_DIR": None}))
    context = await build_material_context("test")
    assert context == ""
