from openai import AsyncOpenAI
from novel.config.settings import get_settings

async def generate_text(prompt: str, system: str = "", model: str = "gpt-4o-mini") -> str:
    settings = get_settings()
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY.get_secret_value())
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = await client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content
