# 核心引擎 V3 演进 (Core Engine V3 Evolution) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 演进 novel-v2 引擎，集成基于 PostgreSQL 的检索引擎、独立的真相归约智能体 (Reducer Agent) 以及插件化提示词管线 (Plugin Pipeline)。

**Architecture:** 采用“写-记分离”模式，新增 Reducer Agent 异步维护 Markdown 真相文件并更新 PostgreSQL 向量表。原 QA Loop 升级为动态加载 YAML 插件的 Pipeline 模式，以支持“去 AI 味”等门禁拦截。

**Tech Stack:** Python 3.10+, PostgreSQL, pgvector, asyncpg, Pydantic, Pytest

## Global Constraints

- 测试必须使用 `pytest` 并遵循 TDD 流程。
- 不引入类似 SQLAlchemy 的重型 ORM，直接使用 `asyncpg` 和轻量化 SQL 语句。
- 保证原有 `settings.py` 结构扩展，不破坏已有逻辑。
- 所有中文字符串必须正常处理。

---

### Task 1: 升级全局配置支持 PostgreSQL (Update Settings for PostgreSQL)

**Files:**
- Modify: `src/novel/config/settings.py`
- Modify: `tests/test_config.py`

**Interfaces:**
- Produces: `Settings` 新增 `DATABASE_URL` (支持空值退化容错)

- [ ] **Step 1: Write the failing test**

```python
# tests/test_config.py 的末尾追加
def test_settings_loads_database_url(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-123")
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/db")
    from novel.config.settings import Settings
    settings = Settings()
    assert settings.DATABASE_URL == "postgresql://user:pass@localhost:5432/db"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/pytest tests/test_config.py::test_settings_loads_database_url -v`
Expected: FAIL (ValidationError for extra fields or missing field if not ignored)

- [ ] **Step 3: Write minimal implementation**

```python
# 修改 src/novel/config/settings.py 中 Settings 类，追加：
class Settings(BaseSettings):
    OPENAI_API_KEY: SecretStr
    PROJECTS_DIR: str = "./novels"
    TEMPLATES_DIR: str = "./templates"
    DATABASE_URL: str | None = None # 新增 PostgreSQL 数据库连接

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/pytest tests/test_config.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/novel/config/settings.py tests/test_config.py
git commit -m "feat(config): add DATABASE_URL for pgvector integration"
```

---

### Task 2: 插件化提示词解析器 (Plugin Skill Loader)

**Files:**
- Create: `src/novel/core/skills/loader.py`
- Create: `tests/core/skills/test_loader.py`

**Interfaces:**
- Produces: `def load_skill(yaml_path: str) -> dict`

- [ ] **Step 1: Write the failing test**

```python
# tests/core/skills/test_loader.py
import pytest
from novel.core.skills.loader import load_skill

def test_load_skill(tmp_path):
    skill_file = tmp_path / "deslop.yaml"
    skill_file.write_text("trigger_phase: review\nsystem_prompt: 'No AI words'\n")
    skill = load_skill(str(skill_file))
    assert skill["trigger_phase"] == "review"
    assert skill["system_prompt"] == "No AI words"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/pytest tests/core/skills/test_loader.py -v`
Expected: FAIL (ModuleNotFoundError)

- [ ] **Step 3: Write minimal implementation**

```python
# src/novel/core/skills/loader.py
import yaml
from pathlib import Path

def load_skill(yaml_path: str) -> dict:
    with open(yaml_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/pytest tests/core/skills/test_loader.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/novel/core/skills/loader.py tests/core/skills/test_loader.py
git commit -m "feat(skills): add yaml skill loader for prompt pipeline"
```

---

### Task 3: 归约智能体核心存储层 (Reducer Agent Truth Files)

**Files:**
- Create: `src/novel/core/workflow/reducer.py`
- Create: `tests/core/workflow/test_reducer.py`

**Interfaces:**
- Produces: `async def update_truth_file(project_dir: str, category: str, content: str) -> bool`

- [ ] **Step 1: Write the failing test**

```python
# tests/core/workflow/test_reducer.py
import pytest
import os
from novel.core.workflow.reducer import update_truth_file

@pytest.mark.asyncio
async def test_update_truth_file(tmp_path):
    proj_dir = str(tmp_path)
    success = await update_truth_file(proj_dir, "characters", "# Character List")
    assert success is True
    file_path = tmp_path / "truth" / "characters" / "index.md"
    assert file_path.read_text() == "# Character List"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/pytest tests/core/workflow/test_reducer.py -v`
Expected: FAIL (ModuleNotFoundError)

- [ ] **Step 3: Write minimal implementation**

```python
# src/novel/core/workflow/reducer.py
import os
from pathlib import Path

async def update_truth_file(project_dir: str, category: str, content: str) -> bool:
    base_dir = Path(project_dir) / "truth" / category
    base_dir.mkdir(parents=True, exist_ok=True)
    file_path = base_dir / "index.md"
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return True
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/pytest tests/core/workflow/test_reducer.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/novel/core/workflow/reducer.py tests/core/workflow/test_reducer.py
git commit -m "feat(workflow): add reducer agent truth file updating mechanism"
```
