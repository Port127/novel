from openai import AsyncOpenAI
import logging

logger = logging.getLogger(__name__)

async def generate_embedding(client: AsyncOpenAI, text: str) -> list[float]:
    """
    Generate an embedding vector for the given text using OpenAI API.
    
    Raises:
        ValueError: If the text is empty.
        openai.APIError (and subclasses): If the OpenAI API call fails.
        RuntimeError: If the API returns a malformed response without embedding data.
    """
    if not text.strip():
        raise ValueError("Text for embedding cannot be empty")
        
    try:
        response = await client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
    except Exception as e:
        logger.error(f"OpenAI embedding generation failed: {e}")
        raise
        
    if not response.data or not response.data[0].embedding:
        raise RuntimeError("Received malformed embedding response from OpenAI")
        
    return response.data[0].embedding
