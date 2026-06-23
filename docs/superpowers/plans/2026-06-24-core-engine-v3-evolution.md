# 核心引擎 V3 演进 (Core Engine V3 Evolution) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 全面落地 novel-v2 到 V3 的底层架构演进，完成对 PostgreSQL (pgvector) 的原生支持、建立 Truth Files 归约与全量同步机制，以及完成动态 QA 插件池引擎。

**Architecture:** 
1. **DB Layer**: 基于 `asyncpg` 实现高性能 PostgreSQL 连接池，利用 `pgvector` 存储并进行余弦相似度召回。
2. **Context Layer**: 新增 `PgContextEngine` 替代旧版文件直接拼接。
3. **Workflow Layer**: 重构 `qa_loop.py`，支持责任链模式加载 YAML 定义的 Skills。新增 `ReducerAgent`，利用 LLM 进行状态抽取并更新 Truth Files (Markdown+YAML Frontmatter)。

**Tech Stack:** Python 3.10+, `asyncpg`, `pgvector` (PostgreSQL 扩展), Pydantic, Pytest, PyYAML

## Global Constraints

- 严禁引入 SQLAlchemy 等重型 ORM，必须使用原生 `asyncpg` SQL。
- 所有的异步操作必须有 `pytest.mark.asyncio` 支持。
- 数据库连接信息通过 `Settings` 从环境变量获取，未配置 `DATABASE_URL` 时必须触发优雅降级 (Fallback) 或明确异常。
- 保证每个 Task 可独立运行通过测试，绝不遗留未定义的 Placeholder 占位符。

---

### Task 1: PostgreSQL 基础设施与连接池 (PostgreSQL Infrastructure & Pooling)

**Files:**
- Modify: `src/novel/config/settings.py`
- Create: `src/novel/core/memory/db_pool.py`
- Create: `tests/core/memory/test_db_pool.py`

**Interfaces:**
- Consumes: Environment variables
- Produces: `async def init_db_pool(settings: Settings) -> asyncpg.Pool`

- [ ] **Step 1: Write the failing test**

```python
# tests/core/memory/test_db_pool.py
import pytest
from unittest.mock import patch, AsyncMock
from novel.config.settings import Settings
from novel.core.memory.db_pool import init_db_pool, close_db_pool, get_pool

@pytest.mark.asyncio
async def test_init_and_close_db_pool():
    settings = Settings(OPENAI_API_KEY="sk-test", DATABASE_URL="postgresql://user:pass@localhost/db")
    
    with patch("novel.core.memory.db_pool.asyncpg.create_pool", new_callable=AsyncMock) as mock_create_pool:
        mock_pool = AsyncMock()
        mock_create_pool.return_value = mock_pool
        
        pool = await init_db_pool(settings)
        assert pool is not None
        assert get_pool() is pool
        mock_create_pool.assert_called_once_with("postgresql://user:pass@localhost/db", min_size=1, max_size=10)
        
        await close_db_pool()
        mock_pool.close.assert_called_once()
        assert get_pool() is None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/pytest tests/core/memory/test_db_pool.py -v`
Expected: FAIL (ModuleNotFoundError)

- [ ] **Step 3: Write minimal implementation**

```python
# src/novel/config/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    OPENAI_API_KEY: SecretStr
    PROJECTS_DIR: str = "./novels"
    TEMPLATES_DIR: str = "./templates"
    DATABASE_URL: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

# src/novel/core/memory/db_pool.py
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/pytest tests/core/memory/test_db_pool.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/novel/config/settings.py src/novel/core/memory/db_pool.py tests/core/memory/test_db_pool.py
git commit -m "feat(memory): implement asyncpg connection pool and update settings"
```

---

### Task 2: 数据库表结构初始化与 pgvector 支持 (Schema & pgvector Initialization)

**Files:**
- Create: `src/novel/core/memory/schema.py`
- Create: `tests/core/memory/test_schema.py`

**Interfaces:**
- Consumes: `get_pool()` from `db_pool.py`
- Produces: `async def init_schema() -> None`

- [ ] **Step 1: Write the failing test**

```python
# tests/core/memory/test_schema.py
import pytest
from unittest.mock import AsyncMock, patch
from novel.core.memory.schema import init_schema

@pytest.mark.asyncio
async def test_init_schema():
    with patch("novel.core.memory.schema.get_pool") as mock_get_pool:
        mock_pool = AsyncMock()
        mock_get_pool.return_value = mock_pool
        mock_connection = AsyncMock()
        mock_pool.acquire.return_value.__aenter__.return_value = mock_connection
        
        await init_schema()
        
        # Verify execute was called with vector extension and table creation
        calls = mock_connection.execute.call_args_list
        assert any("CREATE EXTENSION IF NOT EXISTS vector" in call[0][0] for call in calls)
        assert any("CREATE TABLE IF NOT EXISTS truth_chunks" in call[0][0] for call in calls)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/pytest tests/core/memory/test_schema.py -v`
Expected: FAIL (ModuleNotFoundError)

- [ ] **Step 3: Write minimal implementation**

```python
# src/novel/core/memory/schema.py
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/pytest tests/core/memory/test_schema.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/novel/core/memory/schema.py tests/core/memory/test_schema.py
git commit -m "feat(memory): add schema initialization with pgvector extension"
```

---

### Task 3: Embedding 生成服务 (Embedding Generation Service)

**Files:**
- Create: `src/novel/core/llm/embedding.py`
- Create: `tests/core/llm/test_embedding.py`

**Interfaces:**
- Produces: `async def generate_embedding(client: AsyncOpenAI, text: str) -> list[float]`

- [ ] **Step 1: Write the failing test**

```python
# tests/core/llm/test_embedding.py
import pytest
from unittest.mock import AsyncMock
from novel.core.llm.embedding import generate_embedding

@pytest.mark.asyncio
async def test_generate_embedding():
    mock_client = AsyncMock()
    mock_response = AsyncMock()
    mock_response.data = [AsyncMock(embedding=[0.1, 0.2, 0.3])]
    mock_client.embeddings.create.return_value = mock_response
    
    result = await generate_embedding(mock_client, "Test context")
    
    assert result == [0.1, 0.2, 0.3]
    mock_client.embeddings.create.assert_called_once_with(
        model="text-embedding-3-small",
        input="Test context"
    )
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/pytest tests/core/llm/test_embedding.py -v`
Expected: FAIL

- [ ] **Step 3: Write minimal implementation**

```python
# src/novel/core/llm/embedding.py
from openai import AsyncOpenAI

async def generate_embedding(client: AsyncOpenAI, text: str) -> list[float]:
    response = await client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/pytest tests/core/llm/test_embedding.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/novel/core/llm/embedding.py tests/core/llm/test_embedding.py
git commit -m "feat(llm): add async embedding generation via OpenAI"
```

---

### Task 4: 真相文件 Markdown 与 YAML Frontmatter 解析器 (Truth File Parser)

**Files:**
- Create: `src/novel/core/workflow/truth_parser.py`
- Create: `tests/core/workflow/test_truth_parser.py`

**Interfaces:**
- Produces: `def parse_truth_file(content: str) -> tuple[dict, str]`

- [ ] **Step 1: Write the failing test**

```python
# tests/core/workflow/test_truth_parser.py
from novel.core.workflow.truth_parser import parse_truth_file

def test_parse_truth_file():
    content = "---\nname: 陈汉升\nstatus: alive\n---\n# 陈汉升\n主角，渣男。"
    metadata, body = parse_truth_file(content)
    assert metadata == {"name": "陈汉升", "status": "alive"}
    assert body.strip() == "# 陈汉升\n主角，渣男。"

def test_parse_truth_file_no_frontmatter():
    content = "# 简单文本\n无 Metadata。"
    metadata, body = parse_truth_file(content)
    assert metadata == {}
    assert body.strip() == "# 简单文本\n无 Metadata。"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/pytest tests/core/workflow/test_truth_parser.py -v`
Expected: FAIL

- [ ] **Step 3: Write minimal implementation**

```python
# src/novel/core/workflow/truth_parser.py
import yaml
import re

def parse_truth_file(content: str) -> tuple[dict, str]:
    if content.startswith("---\n"):
        parts = content.split("---\n", 2)
        if len(parts) >= 3:
            try:
                metadata = yaml.safe_load(parts[1]) or {}
                body = parts[2]
                return metadata, body
            except yaml.YAMLError:
                pass
    return {}, content
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/pytest tests/core/workflow/test_truth_parser.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/novel/core/workflow/truth_parser.py tests/core/workflow/test_truth_parser.py
git commit -m "feat(workflow): add truth file frontmatter parser"
```

---

### Task 5: PostgreSQL 语义检索引擎 (PgContextEngine)

**Files:**
- Create: `src/novel/core/memory/pg_context_engine.py`
- Create: `tests/core/memory/test_pg_context_engine.py`

**Interfaces:**
- Consumes: `generate_embedding`, `get_pool`
- Produces: `async def retrieve_context(project_id: str, query_embedding: list[float], limit: int = 5) -> list[str]`

- [ ] **Step 1: Write the failing test**

```python
# tests/core/memory/test_pg_context_engine.py
import pytest
import json
from unittest.mock import AsyncMock, patch
from novel.core.memory.pg_context_engine import retrieve_context

@pytest.mark.asyncio
async def test_retrieve_context():
    with patch("novel.core.memory.pg_context_engine.get_pool") as mock_get_pool:
        mock_pool = AsyncMock()
        mock_get_pool.return_value = mock_pool
        mock_connection = AsyncMock()
        mock_pool.acquire.return_value.__aenter__.return_value = mock_connection
        
        # Mock database fetch response
        mock_connection.fetch.return_value = [
            {"content": "Relevant context 1", "distance": 0.1},
            {"content": "Relevant context 2", "distance": 0.2}
        ]
        
        results = await retrieve_context("project_1", [0.1, 0.2, 0.3], limit=2)
        
        assert len(results) == 2
        assert results[0] == "Relevant context 1"
        assert results[1] == "Relevant context 2"
        
        # Check if proper pgvector cosine operator (<=>) is used
        query_call = mock_connection.fetch.call_args[0][0]
        assert "<=>" in query_call
        assert "project_id = $1" in query_call
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/pytest tests/core/memory/test_pg_context_engine.py -v`
Expected: FAIL

- [ ] **Step 3: Write minimal implementation**

```python
# src/novel/core/memory/pg_context_engine.py
import json
from novel.core.memory.db_pool import get_pool

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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/pytest tests/core/memory/test_pg_context_engine.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/novel/core/memory/pg_context_engine.py tests/core/memory/test_pg_context_engine.py
git commit -m "feat(memory): implement pgvector cosine similarity retrieval"
```

---

### Task 6: 插件技能定义与责任链 (Plugin Skill Pipeline)

**Files:**
- Create: `src/novel/core/skills/pipeline.py`
- Create: `tests/core/skills/test_pipeline.py`

**Interfaces:**
- Produces: `Skill` (Pydantic model)
- Produces: `async def run_skill_pipeline(skills: list[Skill], initial_text: str) -> str`

- [ ] **Step 1: Write the failing test**

```python
# tests/core/skills/test_pipeline.py
import pytest
from novel.core.skills.pipeline import Skill, run_skill_pipeline

@pytest.mark.asyncio
async def test_run_skill_pipeline():
    skill1 = Skill(name="Remove AI", trigger_phase="deslop", system_prompt="Remove metaphors")
    skill2 = Skill(name="Add Hook", trigger_phase="hook", system_prompt="Add suspense at end")
    
    # Mocking the LLM modifier function for the test
    async def mock_modifier(text, prompt):
        return f"{text} -> {prompt[:5]}"
        
    result = await run_skill_pipeline([skill1, skill2], "Chapter start.", llm_func=mock_modifier)
    assert result == "Chapter start. -> Remov -> Add H"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/pytest tests/core/skills/test_pipeline.py -v`
Expected: FAIL

- [ ] **Step 3: Write minimal implementation**

```python
# src/novel/core/skills/pipeline.py
from pydantic import BaseModel
from typing import Callable, Awaitable

class Skill(BaseModel):
    name: str
    trigger_phase: str
    system_prompt: str
    evaluation_criteria: list[str] = []

async def run_skill_pipeline(
    skills: list[Skill], 
    initial_text: str, 
    llm_func: Callable[[str, str], Awaitable[str]]
) -> str:
    current_text = initial_text
    for skill in skills:
        current_text = await llm_func(current_text, skill.system_prompt)
    return current_text
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/pytest tests/core/skills/test_pipeline.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/novel/core/skills/pipeline.py tests/core/skills/test_pipeline.py
git commit -m "feat(skills): add plugin skill pipeline for QA sequence"
```

---

### Task 7: Reducer Agent 数据同步层 (Reducer Agent DB Sync)

**Files:**
- Create: `src/novel/core/workflow/reducer.py` (Update)
- Create: `tests/core/workflow/test_reducer.py` (Update)

**Interfaces:**
- Consumes: `get_pool`, `generate_embedding`
- Produces: `async def sync_truth_to_db(project_id: str, file_path: str, content: str, embedding: list[float]) -> None`

- [ ] **Step 1: Write the failing test**

```python
# tests/core/workflow/test_reducer_sync.py
import pytest
import json
from unittest.mock import AsyncMock, patch
from novel.core.workflow.reducer import sync_truth_to_db

@pytest.mark.asyncio
async def test_sync_truth_to_db():
    with patch("novel.core.workflow.reducer.get_pool") as mock_get_pool:
        mock_pool = AsyncMock()
        mock_get_pool.return_value = mock_pool
        mock_connection = AsyncMock()
        mock_pool.acquire.return_value.__aenter__.return_value = mock_connection
        
        await sync_truth_to_db("proj1", "truth/characters/chen.md", "Content", [0.1, 0.2])
        
        query_call = mock_connection.execute.call_args[0][0]
        assert "INSERT INTO truth_chunks" in query_call
        assert "ON CONFLICT" not in query_call # Simple insert for now
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/pytest tests/core/workflow/test_reducer_sync.py -v`
Expected: FAIL

- [ ] **Step 3: Write minimal implementation**

```python
# src/novel/core/workflow/reducer.py (Append)
import json
from novel.core.memory.db_pool import get_pool

async def sync_truth_to_db(project_id: str, file_path: str, content: str, embedding: list[float]) -> None:
    pool = get_pool()
    if not pool:
        raise RuntimeError("Database pool not initialized.")
        
    embedding_str = json.dumps(embedding)
    
    query = """
        INSERT INTO truth_chunks (project_id, category, file_path, content, embedding)
        VALUES ($1, $2, $3, $4, $5::vector)
    """
    
    # Simple extraction of category from path (e.g., truth/characters/chen.md -> characters)
    parts = file_path.split("/")
    category = parts[1] if len(parts) > 1 else "general"
    
    async with pool.acquire() as conn:
        await conn.execute(query, project_id, category, file_path, content, embedding_str)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/pytest tests/core/workflow/test_reducer_sync.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/novel/core/workflow/reducer.py tests/core/workflow/test_reducer_sync.py
git commit -m "feat(workflow): implement DB synchronization for truth files"
```
