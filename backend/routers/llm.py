from fastapi import APIRouter
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

from backend.config import get_llm_config, save_llm_config
from backend.services.llm_service import chat_stream

router = APIRouter(prefix="/api/llm", tags=["llm"])


class LLMConfigUpdate(BaseModel):
    api_url: str | None = None
    api_key: str | None = None
    model: str | None = None
    temperature: float | None = None
    max_tokens: int | None = None


class ChatRequest(BaseModel):
    messages: list[dict]


@router.get("/config")
async def read_config():
    """Return current LLM configuration (masks the API key)."""
    config = get_llm_config()
    safe = dict(config)
    key = safe.get("api_key", "")
    if key and len(key) > 8:
        safe["api_key"] = key[:4] + "****" + key[-4:]
    return safe


@router.put("/config")
async def update_config(req: LLMConfigUpdate):
    """Update LLM configuration."""
    config = get_llm_config()
    for field in ("api_url", "api_key", "model", "temperature", "max_tokens"):
        val = getattr(req, field)
        if val is not None:
            config[field] = val
    save_llm_config(config)
    return {"ok": True}


@router.post("/chat")
async def chat(req: ChatRequest):
    """SSE streaming chat endpoint."""

    async def event_generator():
        async for chunk in chat_stream(req.messages):
            yield {"event": "message", "data": chunk}
        yield {"event": "done", "data": "[DONE]"}

    return EventSourceResponse(event_generator())
