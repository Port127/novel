import sys
from unittest.mock import patch, AsyncMock, MagicMock
sys.modules['asyncpg'] = MagicMock()

import pytest
from novel.config.settings import Settings
from novel.core.memory.db_pool import init_db_pool, close_db_pool, get_pool

@pytest.mark.asyncio
async def test_init_and_close_db_pool():
    settings = Settings(OPENAI_API_KEY="sk-test", DATABASE_URL="postgresql://user:pass@localhost/db")
    
    with patch("novel.core.memory.db_pool.asyncpg.create_pool", new_callable=AsyncMock) as mock_create_pool:
        mock_pool = AsyncMock()
        mock_create_pool.return_value = mock_pool
        
        pool = await init_db_pool(settings)
        assert pool is not None
        assert get_pool() is pool
        mock_create_pool.assert_called_once_with("postgresql://user:pass@localhost/db", min_size=1, max_size=10)
        
        await close_db_pool()
        mock_pool.close.assert_called_once()
        assert get_pool() is None
