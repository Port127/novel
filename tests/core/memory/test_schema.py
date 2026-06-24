import sys
from unittest.mock import MagicMock

# Mock asyncpg before importing modules that depend on it
sys.modules["asyncpg"] = MagicMock()

import pytest
from unittest.mock import AsyncMock, patch
from novel.core.memory.schema import init_schema

@pytest.mark.asyncio
async def test_init_schema():
    with patch("novel.core.memory.schema.get_pool") as mock_get_pool:
        mock_pool = MagicMock()
        mock_get_pool.return_value = mock_pool
        mock_connection = AsyncMock()
        mock_pool.acquire.return_value.__aenter__.return_value = mock_connection
        
        await init_schema()
        
        # Verify execute was called with vector extension and table creation
        calls = mock_connection.execute.call_args_list
        assert any("CREATE EXTENSION IF NOT EXISTS vector" in call[0][0] for call in calls)
        assert any("CREATE TABLE IF NOT EXISTS truth_chunks" in call[0][0] for call in calls)
