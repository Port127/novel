import pytest
from novel.core.llm.client import generate_text

@pytest.mark.asyncio
async def test_generate_text(monkeypatch):
    class MockMessage: content = "mocked"
    class MockChoice: message = MockMessage()
    class MockCreate:
        async def create(self, **kwargs):
            return type('obj', (object,), {'choices': [MockChoice()]})()
    class MockChat: completions = MockCreate()
    class MockClient:
        def __init__(self, api_key): self.chat = MockChat()

    monkeypatch.setattr("novel.core.llm.client.AsyncOpenAI", MockClient)
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    res = await generate_text("Hi")
    assert res == "mocked"
