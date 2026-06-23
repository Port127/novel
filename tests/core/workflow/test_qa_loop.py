import pytest
from novel.core.workflow.qa_loop import run_qa_loop

@pytest.mark.asyncio
async def test_qa_loop_passes(monkeypatch):
    async def mock_gen(*args, **kwargs):
        class MockVerdict:
            passed = True
            revised_text = "Good text"
        return MockVerdict()
    
    monkeypatch.setattr("novel.core.workflow.qa_loop.generate_structured", mock_gen)
    res = await run_qa_loop("draft", "ctx")
    assert res == "Good text"
