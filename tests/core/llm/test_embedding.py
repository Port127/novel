import pytest
from unittest.mock import AsyncMock
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

@pytest.mark.asyncio
async def test_generate_embedding_empty_text():
    mock_client = AsyncMock()
    with pytest.raises(ValueError, match="Text for embedding cannot be empty"):
        await generate_embedding(mock_client, "   ")
        
@pytest.mark.asyncio
async def test_generate_embedding_malformed_response():
    mock_client = AsyncMock()
    mock_response = AsyncMock()
    mock_response.data = []  # Empty data
    mock_client.embeddings.create.return_value = mock_response
    
    with pytest.raises(RuntimeError, match="Received malformed embedding response from OpenAI"):
        await generate_embedding(mock_client, "Test")
