import asyncpg
from novel.config.settings import Settings

_pool: asyncpg.Pool | None = None

async def init_db_pool(settings: Settings) -> asyncpg.Pool:
    global _pool
    if not settings.DATABASE_URL:
        raise ValueError("DATABASE_URL is not configured.")
    _pool = await asyncpg.create_pool(settings.DATABASE_URL, min_size=1, max_size=10)
    return _pool

async def close_db_pool() -> None:
    global _pool
    if _pool:
        await _pool.close()
        _pool = None

def get_pool() -> asyncpg.Pool | None:
    return _pool
