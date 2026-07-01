# 核心生成链路与 CLI 落地设计 (Core Generation & CLI Implementation Design)

## 1. 背景

昨天项目已经完成了核心引擎 (V3 架构前置) 的重构，底层的 `src/novel/core/llm` (支持结构化解析和容错) 与 `src/novel/core/workflow` (QA Loop 循环) 均已建立，同时 CLI 也迁移到了 `src/novel/cli/main.py`。
然而，目前 CLI 层面尚未接入负责处理设定的 `generate` 命令与负责正文的 `write` 命令，导致底层引擎处于“空转”状态，用户无法通过命令实际触发小说的创作流。

本设计旨在基于昨日的重构成果，将核心生成逻辑补齐在 Pipeline 层，并桥接到 CLI 入口。

## 2. 目标

- **新增 Pipeline 业务层**：在 `src/novel/pipeline/` 下新增 `generation_pipeline.py` 和 `writing_pipeline.py`，负责拼接项目设定的 Prompt，并调度 `core.llm` 引擎进行输出。
- **完善 CLI 交互入口**：在现有的 `src/novel/cli/main.py` 中引入 `novel generate` 和 `novel write` 命令组，抛弃过时的 `scripts/generate.py` 等脚本。

## 3. 详细设计

### 3.1 设定生成管线 (`src/novel/pipeline/generation_pipeline.py`)
依赖 `core.llm.client` 和 `core.llm.structured`。
- 提供 `generate_worldbuilding(project_id, prompt)`
- 提供 `generate_characters(project_id, prompt)`
- 提供 `generate_outline(project_id)`
**工作流**：读取对应项目的 `settings/` YAML -> 将用户 Prompt 与 Schema 发送至大模型结构化提取 -> 结果保存回对应 YAML。

### 3.2 写作生成管线 (`src/novel/pipeline/writing_pipeline.py`)
依赖 `core.workflow.qa_loop` 与基础客户端。
- 提供 `write_new_chapter(project_id, chapter_id, prompt)`
- 提供 `continue_chapter(project_id, chapter_id)`
- 提供 `revise_chapter(project_id, chapter_id, mode)`
**工作流**：将世界观/大纲拼装为 Context -> 大模型输出初稿 -> QA Loop 自愈处理 -> 终稿写入 `content/chapters/chapter_*.md`。

### 3.3 命令行集成 (`src/novel/cli/main.py`)
新增 `click.Group` 注册：
```python
@cli.group()
def generate():
    """Generate settings (world, character, outline)."""
    pass

@generate.command("world")
def generate_world(...):
    pass
# 依此类推...

@cli.group()
def write():
    """Write chapter content."""
    pass
```

## 4. 实施优先级
1. 先建立 `generation_pipeline.py` 和对应的 `cli generate` 命令，测试生成世界观设定是否能跑通。
2. 然后建立 `writing_pipeline.py` 和对应的 `cli write` 命令，打通章纲到正文的链路。
