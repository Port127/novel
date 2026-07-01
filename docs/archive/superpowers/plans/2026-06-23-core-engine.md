# 核心引擎实施计划 (Core Engine Implementation Plan)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**目标 (Goal):** 为 novel-v2 构建一个强健的、双引擎驱动的后端（自动化生成 + 人在环路），彻底抛开之前的历史遗留结构包袱。

**架构 (Architecture):** 位于 `src/novel/core/` 的原生 Python 流水线，使用 OpenAI SDK + Pydantic 进行结构化生成，原生状态机实现质量审查循环 (QA loop)，以及基于纯文本的上下文构建器 (ContextBuilder)。

**技术栈 (Tech Stack):** Python 3.10+, OpenAI Python SDK, Pydantic, Pytest

## 全局约束 (Global Constraints)

- **上下文与 Token 限制策略:** 为了避免对话 Token 限制和上下文耗尽：
  1. 本计划的执行**必须**使用 **subagent-driven-development**（子智能体驱动开发）。主智能体应为每个独立的 Task 派生一个全新的子智能体执行，以确保上下文干净。
  2. 如果主聊天窗口在任何时候逼近 Token 限制，您可以直接开启一个**全新的对话**。在新聊天中，只需告诉智能体：“读取 `docs/superpowers/plans/2026-06-23-core-engine.md` 文件，并从第一个未勾选的任务继续执行。” 该计划文件将作为永久的状态存储。
- TDD（测试驱动开发）要求：先编写会失败的测试，运行它，实现代码，再次运行使测试通过，然后提交 (commit)。
- 放手去干，不要担心破坏旧的项目结构。

---

### 任务 1: 环境配置与死代码清理 (Task 1: Environment & Dead Code Purge)

**文件 (Files):**
- 创建 (Create): `tests/test_config.py`
- 修改 (Modify): `src/novel/config/settings.py`
- 删除 (Delete): `scripts/utils/__init__.py`

**接口定义 (Interfaces):**
- 消费 (Consumes): 环境变量 (`.env`)
- 产出 (Produces): 包含 `OPENAI_API_KEY` 的 `Settings` 对象

- [ ] **步骤 1: 编写 Config 的失败测试**

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

- [ ] **步骤 2: 运行测试并确认失败**

运行: `pytest tests/test_config.py -v`
预期结果: 失败（如果配置已经匹配则通过，但确保它能运行）

- [ ] **步骤 3: 实现 Settings 并清理死代码**

```bash
# 清理导致 ImportError 的死代码
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

- [ ] **步骤 4: 运行测试并确认通过**

运行: `pytest tests/test_config.py -v`
预期结果: 通过 (PASS)

- [ ] **步骤 5: 提交更改 (Commit)**

```bash
git add tests/test_config.py src/novel/config/settings.py
git rm -f scripts/utils/__init__.py scripts/utils/llm_client.py || true
git commit -m "refactor(config): purge dead llm_client and standardise OPENAI_API_KEY"
```

---

### 任务 2: 基础 LLM 客户端 (Task 2: Base LLM Client)

**文件 (Files):**
- 创建: `src/novel/core/llm/client.py`
- 创建: `tests/core/llm/test_client.py`

**接口定义 (Interfaces):**
- 产出 (Produces): `async def generate_text(prompt: str, system: str = "", model: str = "gpt-4o-mini") -> str`

- [ ] **步骤 1: 编写失败测试**

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

- [ ] **步骤 2: 运行测试并确认失败**

运行: `pytest tests/core/llm/test_client.py -v`
预期结果: 失败 (ModuleNotFoundError)

- [ ] **步骤 3: 实现 client.py**

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

- [ ] **步骤 4: 运行测试并确认通过**

运行: `pytest tests/core/llm/test_client.py -v`
预期结果: 通过 (PASS)

- [ ] **步骤 5: 提交更改 (Commit)**

```bash
git add src/novel/core/llm/client.py tests/core/llm/test_client.py
git commit -m "feat(llm): base async openai client"
```

---

### 任务 3: 带自愈重试的结构化生成器 (Task 3: Structured Generator with Self-Healing)

**文件 (Files):**
- 创建: `src/novel/core/llm/structured.py`
- 创建: `tests/core/llm/test_structured.py`

**接口定义 (Interfaces):**
- 消费 (Consumes): `generate_text`
- 产出 (Produces): `async def generate_structured(prompt: str, schema: Type[BaseModel], system: str = "", retries: int = 2) -> BaseModel`

- [ ] **步骤 1: 编写失败测试**

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

- [ ] **步骤 2: 运行测试并确认失败**

运行: `pytest tests/core/llm/test_structured.py -v`
预期结果: 失败 (FAIL)

- [ ] **步骤 3: 实现 structured.py**

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

- [ ] **步骤 4: 运行测试并确认通过**

运行: `pytest tests/core/llm/test_structured.py -v`
预期结果: 通过 (PASS)

- [ ] **步骤 5: 提交更改 (Commit)**

```bash
git add src/novel/core/llm/structured.py tests/core/llm/test_structured.py
git commit -m "feat(llm): structured pydantic generation with self-healing retries"
```

---

### 任务 4: 记忆与上下文构建器 (Task 4: Memory Context Builder)

**文件 (Files):**
- 创建: `src/novel/core/memory/context_builder.py`
- 创建: `tests/core/memory/test_context_builder.py`

**接口定义 (Interfaces):**
- 产出 (Produces): `def build_chapter_context(project_dir: str) -> str`

- [ ] **步骤 1: 编写失败测试**

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

- [ ] **步骤 2: 运行测试并确认失败**

运行: `pytest tests/core/memory/test_context_builder.py -v`
预期结果: 失败 (FAIL)

- [ ] **步骤 3: 实现 context_builder.py**

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

- [ ] **步骤 4: 运行测试并确认通过**

运行: `pytest tests/core/memory/test_context_builder.py -v`
预期结果: 通过 (PASS)

- [ ] **步骤 5: 提交更改 (Commit)**

```bash
git add src/novel/core/memory/context_builder.py tests/core/memory/test_context_builder.py
git commit -m "feat(memory): text based context assembler"
```

---

### 任务 5: QA 质量工作流循环 (Task 5: QA Workflow Loop)

**文件 (Files):**
- 创建: `src/novel/core/workflow/qa_loop.py`
- 创建: `tests/core/workflow/test_qa_loop.py`

**接口定义 (Interfaces):**
- 消费: `generate_structured`
- 产出: `async def run_qa_loop(draft: str, context: str) -> str`

- [ ] **步骤 1: 编写失败测试**

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

- [ ] **步骤 2: 运行测试并确认失败**

运行: `pytest tests/core/workflow/test_qa_loop.py -v`
预期结果: 失败 (FAIL)

- [ ] **步骤 3: 实现 qa_loop.py**

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

- [ ] **步骤 4: 运行测试并确认通过**

运行: `pytest tests/core/workflow/test_qa_loop.py -v`
预期结果: 通过 (PASS)

- [ ] **步骤 5: 提交更改 (Commit)**

```bash
git add src/novel/core/workflow/qa_loop.py tests/core/workflow/test_qa_loop.py
git commit -m "feat(workflow): implement state-machine QA loop for self-correction"
```

---

### 任务 6: CLI 无头执行入口 (Task 6: CLI Headless Entrypoint)

**文件 (Files):**
- 创建: `scripts/generate_engine.py`

**接口定义 (Interfaces):**
- 产出: 触发自动化生成并在 Human-in-the-Loop（人在环路）审查点暂停的 CLI 工具。

- [ ] **步骤 1: 实现 generate_engine.py**

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

- [ ] **步骤 2: 提交更改 (Commit)**

```bash
git add scripts/generate_engine.py
git commit -m "feat(cli): add core engine run script with HitL pause point"
```
