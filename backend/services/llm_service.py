from typing import AsyncGenerator
import json

import httpx

from backend.config import get_llm_config


async def chat_stream(messages: list[dict]) -> AsyncGenerator[str, None]:
    """Stream chat completions from an OpenAI-compatible API.

    Yields text content chunks as they arrive.
    """
    config = get_llm_config()
    api_url = config.get("api_url", "")
    api_key = config.get("api_key", "")
    model = config.get("model", "gpt-4o-mini")
    temperature = config.get("temperature", 0.7)
    max_tokens = config.get("max_tokens", 4096)

    if not api_url:
        yield "[Error] LLM API URL not configured."
        return

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": True,
    }

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream(
                "POST", api_url, json=payload, headers=headers
            ) as resp:
                if resp.status_code != 200:
                    body = await resp.aread()
                    yield f"[Error] LLM API returned {resp.status_code}: {body.decode()}"
                    return

                async for line in resp.aiter_lines():
                    if not line.startswith("data: "):
                        continue
                    data_str = line[6:]
                    if data_str.strip() == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data_str)
                        delta = chunk.get("choices", [{}])[0].get("delta", {})
                        text = delta.get("content", "")
                        if text:
                            yield text
                    except json.JSONDecodeError:
                        continue
    except httpx.ConnectError:
        yield "[Error] Cannot connect to LLM API."
    except httpx.ReadTimeout:
        yield "[Error] LLM API request timed out."
    except Exception as e:
        yield f"[Error] LLM request failed: {e}"
