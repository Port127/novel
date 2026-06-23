import json
from typing import Type, TypeVar
from pydantic import BaseModel, ValidationError
from .client import generate_text

T = TypeVar('T', bound=BaseModel)

class GenerationError(Exception): pass

async def generate_structured(prompt: str, schema: Type[T], system: str = "", retries: int = 2) -> T:
    sys_prompt = system + f"\nOutput ONLY raw JSON matching this schema:\n{schema.model_json_schema()}"
    current_prompt = prompt
    for attempt in range(retries + 1):
        try:
            raw = await generate_text(current_prompt, sys_prompt)
            clean = raw.strip().removeprefix("```json").removesuffix("```").strip()
            return schema(**json.loads(clean))
        except (json.JSONDecodeError, ValidationError) as e:
            if attempt == retries:
                raise GenerationError(f"Failed after {retries} retries. Error: {e}")
            current_prompt = prompt + f"\n\nLast attempt failed: {e}\nFix the JSON."
