import pytest
import json
import sys
from unittest.mock import AsyncMock, patch, MagicMock

@pytest.fixture(autouse=True)
def mock_asyncpg():
    with patch.dict("sys.modules", {"asyncpg": MagicMock()}):
        yield

@pytest.mark.asyncio
async def test_retrieve_context(mock_asyncpg):
    from novel.core.memory.pg_context_engine import retrieve_context
    with patch("novel.core.memory.pg_context_engine.get_pool") as mock_get_pool:
        mock_pool = MagicMock()
        mock_get_pool.return_value = mock_pool
        mock_connection = AsyncMock()
        
        mock_acquire_context = AsyncMock()
        mock_acquire_context.__aenter__.return_value = mock_connection
        mock_pool.acquire.return_value = mock_acquire_context
        
        # Mock database fetch response
        mock_connection.fetch.return_value = [
            {"content": "Relevant context 1", "distance": 0.1},
            {"content": "Relevant context 2", "distance": 0.2}
        ]
        
        results = await retrieve_context("project_1", [0.1, 0.2, 0.3], limit=2)
        
        assert len(results) == 2
        assert results[0] == "Relevant context 1"
        assert results[1] == "Relevant context 2"
        
        # Check if proper pgvector cosine operator (<=>) is used
        query_call = mock_connection.fetch.call_args[0][0]
        assert "<=>" in query_call
        assert "project_id = $1" in query_call

@pytest.mark.asyncio
async def test_store_context(mock_asyncpg):
    from novel.core.memory.pg_context_engine import store_context
    with patch("novel.core.memory.pg_context_engine.get_pool") as mock_get_pool:
        
        mock_pool = MagicMock()
        mock_get_pool.return_value = mock_pool
        mock_connection = AsyncMock()
        
        mock_acquire_context = AsyncMock()
        mock_acquire_context.__aenter__.return_value = mock_connection
        mock_pool.acquire.return_value = mock_acquire_context

        # Mock transaction
        mock_transaction_context = AsyncMock()
        mock_transaction_context.__aenter__.return_value = AsyncMock()
        mock_connection.transaction = MagicMock(return_value=mock_transaction_context)
        
        chunks_with_embeddings = [
            ("Chunk 1", [0.1, 0.2, 0.3]),
            ("Chunk 2", [0.4, 0.5, 0.6])
        ]
        
        await store_context("proj_2", "cat_1", "file.md", chunks_with_embeddings)
        
        assert mock_connection.execute.call_count == 2
        
        # Check first insert
        first_call_args = mock_connection.execute.call_args_list[0]
        assert "INSERT INTO truth_chunks" in first_call_args[0][0]
        assert first_call_args[0][1] == "proj_2"
        assert first_call_args[0][2] == "cat_1"
        assert first_call_args[0][3] == "file.md"
        assert first_call_args[0][4] == "Chunk 1"
        assert first_call_args[0][5] == json.dumps([0.1, 0.2, 0.3])
