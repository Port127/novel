import json
from openai import AsyncOpenAI
from novel.core.memory.db_pool import get_pool
from novel.core.llm.embedding import generate_embedding

async def retrieve_context(project_id: str, query_embedding: list[float], limit: int = 5) -> list[str]:
    pool = get_pool()
    if not pool:
        raise RuntimeError("Database pool not initialized.")
        
    embedding_str = json.dumps(query_embedding)
    
    query = """
        SELECT content, embedding <=> $2::vector AS distance
        FROM truth_chunks
        WHERE project_id = $1
        ORDER BY distance ASC
        LIMIT $3;
    """
    
    async with pool.acquire() as conn:
        records = await conn.fetch(query, project_id, embedding_str, limit)
        return [record["content"] for record in records]

async def store_context(
    client: AsyncOpenAI,
    project_id: str,
    category: str,
    file_path: str,
    markdown_content: str
) -> None:
    pool = get_pool()
    if not pool:
        raise RuntimeError("Database pool not initialized.")

    # Split markdown body into chunks (by double newline)
    chunks = [chunk.strip() for chunk in markdown_content.split("\n\n") if chunk.strip()]

    query = """
        INSERT INTO truth_chunks (project_id, category, file_path, content, embedding)
        VALUES ($1, $2, $3, $4, $5::vector);
    """

    async with pool.acquire() as conn:
        # We can insert in a transaction
        async with conn.transaction():
            for chunk in chunks:
                embedding = await generate_embedding(client, chunk)
                embedding_str = json.dumps(embedding)
                await conn.execute(query, project_id, category, file_path, chunk, embedding_str)
