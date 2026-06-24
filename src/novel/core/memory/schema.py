from novel.core.memory.db_pool import get_pool

async def init_schema() -> None:
    pool = get_pool()
    if not pool:
        raise RuntimeError("Database pool not initialized.")
    
    async with pool.acquire() as conn:
        await conn.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        
        # Creating truth_chunks table with 1536-dimensional vector for OpenAI text-embedding-3-small
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS truth_chunks (
                id SERIAL PRIMARY KEY,
                project_id VARCHAR(255) NOT NULL,
                category VARCHAR(50) NOT NULL,
                file_path VARCHAR(500) NOT NULL,
                content TEXT NOT NULL,
                embedding vector(1536)
            );
        """)
        
        # Create HNSW index for fast approximate nearest neighbor search
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS truth_chunks_embedding_idx 
            ON truth_chunks USING hnsw (embedding vector_cosine_ops);
        """)
