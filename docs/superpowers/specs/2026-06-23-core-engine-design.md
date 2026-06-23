# 核心引擎架构设计 (Core Engine Architecture Design)

## 1. 概述 (Overview)
本设计的核心目标是将 `novel-v2` 升级为一个**“底座全自动，上层可交互”**的双引擎驱动（Dual-Engine）写作系统。
一方面，底层的 `src/novel/core/` 将提供坚实的自动化生成、上下文组装和质量自检管线；另一方面，我们将保留并桥接现有的 `Claude Skills`，作为“人在环路 (Human-in-the-Loop)”的精修切入点，允许创作者随时中断管线并进行自然语言级别的干预和微调。

## 2. 架构决策与技术选型 (Architectural Decisions & Tech Stack)

基于“构建一个健壮、易调试的原生生成流水线”的目标，我们做出以下选型：

- **大模型客户端与结构化输出**：直接使用原生的 `openai` Python SDK 配合 `Pydantic`。我们将避免引入类似 LangChain 这样沉重的框架，以保持抽象层的轻量和易于调试。由 Pydantic 强制约束 JSON schema 的输出。
- **工作流编排**：使用原生 Python 状态机。我们暂时不引入 LangGraph，而是通过显式的 while 循环和状态流转来实现“质量校验循环（QA Loop）”，这样能最精准地控制重试逻辑。
- **记忆与上下文**：构建一个基于纯文本动态拼接的 `ContextBuilder`。在第一阶段，它会读取静态的 YAML 文件（世界观、人物设定、前文摘要）并组装到系统提示词中。
- **人在环路 (Human-in-the-Loop)**：采用“基于文件的断点 + Skills 桥接”模式。底层引擎只负责输出达到质量下限的草稿并落盘，用户随后可以通过对话窗口直接调用已有的 `revise-setting` 或 `write-chapter` 技能对生成的文件进行外科手术级的精修。

## 3. 组件设计 (Component Design)

整个架构被划分为独立但可协同的几个组件，串联起小说的生成管线。

### 3.1 基础设施与配置清理
- **配置项统一**：目前 `.env` 中使用的是 `LLM_API_KEY`，但代码里的 `pydantic-settings` 期待的是 `OPENAI_API_KEY`。我们将统一采用 `OPENAI_API_KEY` 解决这个冲突。
- **清理死代码**：移除 `scripts/utils/__init__.py` 中对 `llm_client.py` 的无效导入，修复导致整个项目无法启动的 ImportError。

### 3.2 核心 LLM 层 (`src/novel/core/llm/`)
- **`client.py`**：对 `AsyncOpenAI` 的轻量封装，负责鉴权、模型路由和异步文本生成。
- **`structured.py` (StructuredGenerator)**：一个高阶生成器，接收 Pydantic schema 和 Prompt。它会将 JSON schema 注入到 System Prompt 中，并解析大模型的返回值。
  - **自愈重试 (Self-Healing Retry)**：如果发生 `ValidationError` 或 JSON 解析错误，它会将确切的错误信息重新喂给大模型要求修复，直到达到 `MAX_RETRIES` 限制。

### 3.3 上下文构建器 (`src/novel/core/memory/`)
- **`context_builder.py`**：负责防止大模型“幻觉”的核心工具类。在生成第 N 章草稿前，它会：
  1. 读取全局 `worldbuilding` YAML。
  2. 提取与本章相关的 `characters`。
  3. 加载全书大纲，以及第 N-3 到 N-1 章的摘要。
  4. 将这些信息格式化为高信息密度、低 Token 消耗的 Markdown 文本，塞入系统提示词。

### 3.4 QA 工作流引擎 (`src/novel/core/workflow/`)
- **`qa_loop.py`**：实现“自我批评与修改”的闭环。它拿到初稿后，根据预设标准（字数达标、格式正确、设定无冲突）进行审查，如果不合格，则携带修改意见打回给大模型重写。
- **`chapter_writer.py`**：主控管线，将上述组件拼装起来：
  `ContextBuilder` -> `StructuredGenerator (写初稿)` -> `QA Loop` -> `保存 Markdown 终稿`。

### 3.5 双引擎交付：批量生成与交互式精修
- **`scripts/generate.py`** (自动化底座)：新增的无头执行入口，支持一键跑批，例如 `python scripts/generate.py chapter <project_id> --chapters 1-10`。
- **Skills 桥接 (交互层)**：底层的 Python API (`chapter_writer` 和 `qa_loop`) 必须设计为可被外部调用的模块。现存的 `.claude/skills` 可以直接读取被 `generate.py` 落盘的文件，让用户通过对话发起微调；并且未来可以将底层的高级校验能力提供给 Skills 使用。

## 4. 异常处理与降级 (Error Handling & Fallbacks)
- **Token 超载**：如果组装出来的 Context 超过了模型的上下文窗口限制，ContextBuilder 会自动降级，仅保留大纲和紧邻的上一章摘要。
- **重试耗尽**：如果 `StructuredGenerator` 耗尽了重试次数依然无法给出合法的 JSON，它会抛出明确的 `GenerationError`，让工作流安全挂起（Pause），等待人工通过编辑器介入修复。

## 5. 测试策略 (Testing Strategy)
- **单元测试**：使用 Mock 的 OpenAI 响应（包括成功的 JSON 和故意损坏的 JSON）来测试 `StructuredGenerator`，证明其自愈重试机制真实有效。
- **集成测试**：Mock 一个质量低劣的初稿，验证 `qa_loop` 能否精准地判定不合格，并成功触发重写流程。
