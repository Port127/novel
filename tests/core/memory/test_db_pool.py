import sys
from unittest.mock import patch, AsyncMock, MagicMock
import pytest

from novel.config.settings import Settings

@pytest.fixture(autouse=True)
def mock_asyncpg():
    with patch.dict("sys.modules", {"asyncpg": MagicMock()}):
        yield

@pytest.mark.asyncio
async def test_init_and_close_db_pool(mock_asyncpg):
    settings = Settings(OPENAI_API_KEY="sk-test", DATABASE_URL="postgresql://user:pass@localhost/db")
    
    # Import locally to ensure sys.modules mock is active
    from novel.core.memory import db_pool
    
    with patch.object(db_pool.asyncpg, "create_pool", new_callable=AsyncMock) as mock_create_pool:
        mock_pool = AsyncMock()
        mock_create_pool.return_value = mock_pool
        
        pool = await db_pool.init_db_pool(settings)
        assert pool is not None
        assert db_pool.get_pool() is pool
        mock_create_pool.assert_called_once_with("postgresql://user:pass@localhost/db", min_size=1, max_size=10)
        
        await db_pool.close_db_pool()
        mock_pool.close.assert_called_once()
        assert db_pool.get_pool() is None

@pytest.mark.asyncio
async def test_init_db_pool_missing_url(mock_asyncpg):
    settings = Settings(OPENAI_API_KEY="sk-test", DATABASE_URL=None)
    from novel.core.memory import db_pool
    
    with pytest.raises(ValueError, match="DATABASE_URL is not configured."):
        await db_pool.init_db_pool(settings)
