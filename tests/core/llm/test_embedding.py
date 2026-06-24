import sys
from unittest.mock import AsyncMock, MagicMock
import pytest

# Mock openai module to avoid ModuleNotFoundError when running tests without real credentials/installation
sys.modules["openai"] = MagicMock()

from novel.core.llm.embedding import generate_embedding

@pytest.mark.asyncio
async def test_generate_embedding():
    mock_client = AsyncMock()
    mock_response = AsyncMock()
    mock_response.data = [AsyncMock(embedding=[0.1, 0.2, 0.3])]
    mock_client.embeddings.create.return_value = mock_response
    
    result = await generate_embedding(mock_client, "Test context")
    
    assert result == [0.1, 0.2, 0.3]
    mock_client.embeddings.create.assert_called_once_with(
        model="text-embedding-3-small",
        input="Test context"
    )
