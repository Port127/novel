# 规格说明书 (Spec): Phase 0 工程架构重构

## 1. 背景与问题陈述
当前的 `novel` 项目是一个松散的脚本集合（如 `scripts/project.py`, `scripts/export.py` 等），仅仅依赖一个基础的 `requirements.txt`。它完全缺乏规范的模块结构、测试框架、环境变量管理以及标准化的命令行入口。这种“脚本堆砌”的结构无法支撑未来高度复杂的多 Agent 小说生成引擎。

## 2. 目标与非目标 (Goals and Non-Goals)

### 目标
*   建立标准的 Python `src-layout` 目录结构（`src/novel/`）。
*   引入 `pyproject.toml` 实现更稳健的依赖与项目管理。
*   在 `tests/` 目录下建立 `pytest` 测试基建（为 TDD 铺路）。
*   引入规范的配置管理模块（使用 `pydantic-settings` 和 `.env` 来管理 API Keys 和路径）。
*   将散乱的旧脚本重构为统一的命令行工具 (CLI)。

### 非目标
*   本阶段**不**编写任何新的 AI 生成逻辑（规划师、执笔人、审查员等）。
*   本阶段**不**修改 `data/schemas/` 和 `templates/` 目录下的现存 YAML 结构文件。
*   本阶段**不**改变小说最终的导出文件格式。

## 3. 架构与组件设计

### 3.1 目录结构规划
项目将被重塑为以下现代化架构：
```
novel/
├── .env                  # 本地环境变量配置 (Git忽略)
├── .env.example          # 环境变量示例模板
├── pyproject.toml        # 核心配置文件及依赖声明
├── Makefile              # 常用任务命令 (install, test, lint)
├── config/               # 存放配置加载逻辑
├── data/                 # 原有数据结构，保持不变
├── src/
│   └── novel/
│       ├── __init__.py
│       ├── cli/          # 命令行入口程序
│       ├── core/         # 核心业务逻辑
│       └── pipeline/     # 调度管线
└── tests/                # 对应 src 的单元测试目录
```

### 3.2 依赖管理
将从 `requirements.txt` 全面迁移到 `pyproject.toml`。我们将引入标准构建系统，核心依赖库包括：`pytest`, `pydantic`, `pydantic-settings`，以及用于构建 CLI 的 `click` 或 `typer`。

### 3.3 配置管理
所有的硬编码路径和 API Keys 将全部迁移至 `src/novel/config/settings.py`。该模块利用 `pydantic-settings` 的 `BaseSettings` 类，自动从 `.env` 文件读取并校验环境变量。

## 4. 测试策略 (Testing Strategy)
*   **框架**：使用 `pytest`。
*   **硬性要求**：必须严格遵循 TDD (测试驱动开发) 原则。在 `src/novel/` 中创建的任何新 Python 模块，必须在 `tests/` 目录下有对应的 `test_<module>.py`。
*   **覆盖率要求**：在进入下一阶段前，配置加载器 (config loader) 和 CLI 核心入口点必须 100% 通过单元测试。

## 5. 迁移与重构计划
1.  **脚手架搭建 (Scaffolding)**: 创建全新的空目录结构 (`src/novel/`, `tests/`, `config/`) 及其基础配置文件 (`pyproject.toml`, `.env.example`, `Makefile`)。
2.  **配置基座 (Configuration Base)**: 基于 `pydantic-settings` 编写统一配置加载器，并完成相关的测试用例。
3.  **脚本重构 (Refactor Scripts)**: 将旧版 `scripts/project.py` 等脚本中的有效逻辑提取到 `src/novel/pipeline/` 目录下，并补充测试。
4.  **入口对接 (CLI Integration)**: 利用全新的 CLI 模块 (`src/novel/cli/main.py`) 对外暴露命令，并在 `pyproject.toml` 中配置 `[project.scripts]` 以生成终端指令。
5.  **清理战场 (Cleanup)**: 当所有新测试全部绿色通过后，删除旧的 `scripts/` 目录。
