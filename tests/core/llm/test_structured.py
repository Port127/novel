import pytest
from pydantic import BaseModel
from novel.core.llm.structured import generate_structured, GenerationError

class DummySchema(BaseModel):
    name: str

@pytest.mark.asyncio
async def test_generate_structured_success(monkeypatch):
    async def mock_generate(*args, **kwargs): return '{"name": "Alice"}'
    monkeypatch.setattr("novel.core.llm.structured.generate_text", mock_generate)
    res = await generate_structured("Q", DummySchema)
    assert res.name == "Alice"

@pytest.mark.asyncio
async def test_generate_structured_retry_fail(monkeypatch):
    async def mock_generate(*args, **kwargs): return 'invalid json'
    monkeypatch.setattr("novel.core.llm.structured.generate_text", mock_generate)
    with pytest.raises(GenerationError):
        await generate_structured("Q", DummySchema, retries=1)
