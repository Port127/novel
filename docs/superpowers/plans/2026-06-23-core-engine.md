# Core Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a robust, dual-engine backend (automated generation + human-in-the-loop) for novel-v2, completely unconstrained by previous legacy structures.

**Architecture:** A native Python pipeline (`src/novel/core/`) using OpenAI SDK + Pydantic for structured generation, a state-machine QA loop, and a text-based ContextBuilder.

**Tech Stack:** Python 3.10+, OpenAI Python SDK, Pydantic, Pytest

## Global Constraints

- **Context Window & Token Limit Strategy:** To avoid conversational token limits and context exhaustion:
  1. The execution of this plan MUST use **subagent-driven-development**. The main agent should dispatch a fresh subagent for each isolated Task to ensure clean context.
  2. If the main chat approaches token limits at any point, the user can start a **brand new conversation**. In the new chat, simply tell the agent: "Read `docs/superpowers/plans/2026-06-23-core-engine.md` and continue from the first unchecked task." The plan acts as the permanent state storage.
- TDD required: Write a failing test first, run it, implement the code, run it to pass, then commit.
- Do not fear breaking the old project structure.

---

### Task 1: Environment & Dead Code Purge

**Files:**
- Create: `tests/test_config.py`
- Modify: `src/novel/config/settings.py`
- Delete: `scripts/utils/__init__.py`

**Interfaces:**
- Consumes: Environment variables (`.env`)
- Produces: `Settings` object with `OPENAI_API_KEY`

- [ ] **Step 1: Write failing test for config**

```python
# tests/test_config.py
import pytest
from pydantic import ValidationError
from novel.config.settings import get_settings

def test_settings_requires_openai_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    with pytest.raises(ValidationError):
        get_settings()

def test_settings_loads_openai_api_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-123")
    settings = get_settings()
    assert settings.OPENAI_API_KEY.get_secret_value() == "sk-test-123"
```

- [ ] **Step 2: Run test to verify failure**

Run: `pytest tests/test_config.py -v`
Expected: FAIL or passing if config already matches, but ensures test runs.

- [ ] **Step 3: Implement Settings and Purge dead code**

```bash
# Clean up dead code that causes ImportError
rm -f scripts/utils/__init__.py
rm -f scripts/utils/llm_client.py
```

```python
# src/novel/config/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from functools import lru_cache

class Settings(BaseSettings):
    OPENAI_API_KEY: SecretStr
    PROJECTS_DIR: str = "./novels"
    TEMPLATES_DIR: str = "./templates"
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()
```

- [ ] **Step 4: Run test to verify passing**

Run: `pytest tests/test_config.py -v`
Expected: PASS

- [ ] **Step 5: Commit changes**

```bash
git add tests/test_config.py src/novel/config/settings.py
git rm -f scripts/utils/__init__.py scripts/utils/llm_client.py || true
git commit -m "refactor(config): purge dead llm_client and standardise OPENAI_API_KEY"
```

---

### Task 2: Base LLM Client

**Files:**
- Create: `src/novel/core/llm/client.py`
- Create: `tests/core/llm/test_client.py`

**Interfaces:**
- Produces: `async def generate_text(prompt: str, system: str = "", model: str = "gpt-4o-mini") -> str`

- [ ] **Step 1: Write failing test**

```python
# tests/core/llm/test_client.py
import pytest
from novel.core.llm.client import generate_text

@pytest.mark.asyncio
async def test_generate_text(monkeypatch):
    class MockMessage: content = "mocked"
    class MockChoice: message = MockMessage()
    class MockCreate:
        async def create(self, **kwargs):
            return type('obj', (object,), {'choices': [MockChoice()]})()
    class MockChat: completions = MockCreate()
    class MockClient:
        def __init__(self, api_key): self.chat = MockChat()

    monkeypatch.setattr("novel.core.llm.client.AsyncOpenAI", MockClient)
    res = await generate_text("Hi")
    assert res == "mocked"
```

- [ ] **Step 2: Run test to verify failure**

Run: `pytest tests/core/llm/test_client.py -v`
Expected: FAIL with ModuleNotFoundError

- [ ] **Step 3: Implement client.py**

```python
# src/novel/core/llm/client.py
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
```

- [ ] **Step 4: Run test to verify passing**

Run: `pytest tests/core/llm/test_client.py -v`
Expected: PASS

- [ ] **Step 5: Commit changes**

```bash
git add src/novel/core/llm/client.py tests/core/llm/test_client.py
git commit -m "feat(llm): base async openai client"
```

---

### Task 3: Structured Generator with Self-Healing

**Files:**
- Create: `src/novel/core/llm/structured.py`
- Create: `tests/core/llm/test_structured.py`

**Interfaces:**
- Consumes: `generate_text`
- Produces: `async def generate_structured(prompt: str, schema: Type[BaseModel], system: str = "", retries: int = 2) -> BaseModel`

- [ ] **Step 1: Write failing test**

```python
# tests/core/llm/test_structured.py
import pytest
from pydantic import BaseModel
from novel.core.llm.structured import generate_structured, GenerationError

class DummySchema(BaseModel):
    name: str

@pytest.mark.asyncio
async def test_generate_structured_success(monkeypatch):
    async def mock_generate(*args, **kwargs): return '{"name": "Alice"}'
    monkeypatch.setattr("novel.core.llm.structured.generate_text", mock_generate)
    res = await generate_structured("Q", DummySchema)
    assert res.name == "Alice"

@pytest.mark.asyncio
async def test_generate_structured_retry_fail(monkeypatch):
    async def mock_generate(*args, **kwargs): return 'invalid json'
    monkeypatch.setattr("novel.core.llm.structured.generate_text", mock_generate)
    with pytest.raises(GenerationError):
        await generate_structured("Q", DummySchema, retries=1)
```

- [ ] **Step 2: Run test to verify failure**

Run: `pytest tests/core/llm/test_structured.py -v`
Expected: FAIL

- [ ] **Step 3: Implement structured.py**

```python
# src/novel/core/llm/structured.py
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
```

- [ ] **Step 4: Run test to verify passing**

Run: `pytest tests/core/llm/test_structured.py -v`
Expected: PASS

- [ ] **Step 5: Commit changes**

```bash
git add src/novel/core/llm/structured.py tests/core/llm/test_structured.py
git commit -m "feat(llm): structured pydantic generation with self-healing retries"
```

---

### Task 4: Memory Context Builder

**Files:**
- Create: `src/novel/core/memory/context_builder.py`
- Create: `tests/core/memory/test_context_builder.py`

**Interfaces:**
- Produces: `def build_chapter_context(project_dir: str) -> str`

- [ ] **Step 1: Write failing test**

```python
# tests/core/memory/test_context_builder.py
from pathlib import Path
from novel.core.memory.context_builder import build_chapter_context
import yaml

def test_build_chapter_context(tmp_path):
    wb_dir = tmp_path / "settings" / "worldbuilding"
    wb_dir.mkdir(parents=True)
    with open(wb_dir / "power.yaml", "w", encoding="utf-8") as f:
        yaml.dump({"system": "magic"}, f)
    ctx = build_chapter_context(str(tmp_path))
    assert "magic" in ctx
```

- [ ] **Step 2: Run test to verify failure**

Run: `pytest tests/core/memory/test_context_builder.py -v`
Expected: FAIL

- [ ] **Step 3: Implement context_builder.py**

```python
# src/novel/core/memory/context_builder.py
import yaml
from pathlib import Path

def build_chapter_context(project_dir: str) -> str:
    proj_path = Path(project_dir)
    context_parts = []
    wb_dir = proj_path / "settings" / "worldbuilding"
    if wb_dir.exists():
        for file in wb_dir.glob("*.yaml"):
            with open(file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                context_parts.append(f"[{file.name}]\n{yaml.dump(data, allow_unicode=True)}")
    return "\n\n".join(context_parts)
```

- [ ] **Step 4: Run test to verify passing**

Run: `pytest tests/core/memory/test_context_builder.py -v`
Expected: PASS

- [ ] **Step 5: Commit changes**

```bash
git add src/novel/core/memory/context_builder.py tests/core/memory/test_context_builder.py
git commit -m "feat(memory): text based context assembler"
```

---

### Task 5: QA Workflow Loop

**Files:**
- Create: `src/novel/core/workflow/qa_loop.py`
- Create: `tests/core/workflow/test_qa_loop.py`

**Interfaces:**
- Consumes: `generate_structured`
- Produces: `async def run_qa_loop(draft: str, context: str) -> str`

- [ ] **Step 1: Write failing test**

```python
# tests/core/workflow/test_qa_loop.py
import pytest
from novel.core.workflow.qa_loop import run_qa_loop

@pytest.mark.asyncio
async def test_qa_loop_passes(monkeypatch):
    async def mock_gen(*args, **kwargs):
        class MockVerdict:
            passed = True
            revised_text = "Good text"
        return MockVerdict()
    
    monkeypatch.setattr("novel.core.workflow.qa_loop.generate_structured", mock_gen)
    res = await run_qa_loop("draft", "ctx")
    assert res == "Good text"
```

- [ ] **Step 2: Run test to verify failure**

Run: `pytest tests/core/workflow/test_qa_loop.py -v`
Expected: FAIL

- [ ] **Step 3: Implement qa_loop.py**

```python
# src/novel/core/workflow/qa_loop.py
from pydantic import BaseModel
from novel.core.llm.structured import generate_structured

class QAVerdict(BaseModel):
    passed: bool
    feedback: str
    revised_text: str

async def run_qa_loop(draft: str, context: str, max_iterations: int = 2) -> str:
    current_text = draft
    for _ in range(max_iterations):
        prompt = f"Context:\n{context}\n\nDraft:\n{current_text}\n\nReview this draft. If good, passed=true and copy to revised_text. Else passed=false, explain in feedback, and provide improved revised_text."
        verdict = await generate_structured(prompt, QAVerdict, system="You are an expert editor.")
        current_text = verdict.revised_text
        if verdict.passed:
            break
    return current_text
```

- [ ] **Step 4: Run test to verify passing**

Run: `pytest tests/core/workflow/test_qa_loop.py -v`
Expected: PASS

- [ ] **Step 5: Commit changes**

```bash
git add src/novel/core/workflow/qa_loop.py tests/core/workflow/test_qa_loop.py
git commit -m "feat(workflow): implement state-machine QA loop for self-correction"
```

---

### Task 6: CLI Headless Entrypoint

**Files:**
- Create: `scripts/generate_engine.py`

**Interfaces:**
- Produces: CLI tool to trigger generation and stop for Human-in-the-Loop review

- [ ] **Step 1: Implement generate_engine.py**

```python
# scripts/generate_engine.py
import asyncio
import click
from novel.core.memory.context_builder import build_chapter_context
from novel.core.llm.client import generate_text
from novel.core.workflow.qa_loop import run_qa_loop

@click.command()
@click.argument('project_dir')
def run(project_dir):
    async def main():
        print("1. Assembling Context...")
        ctx = build_chapter_context(project_dir)
        print("2. Generating Draft...")
        draft = await generate_text(f"Write chapter 1 based on context:\n{ctx}")
        print("3. Running QA Loop...")
        final = await run_qa_loop(draft, ctx)
        print("\n--- FINAL OUTPUT ---\n")
        print(final)
        print("\n[PAUSED FOR HUMAN IN THE LOOP] You can now use Claude Skills to refine this draft.")
    asyncio.run(main())

if __name__ == '__main__':
    run()
```

- [ ] **Step 2: Commit changes**

```bash
git add scripts/generate_engine.py
git commit -m "feat(cli): add core engine run script with HitL pause point"
```
