# 实施计划 (Plan): Phase 0 工程架构重构

## 关联规格说明书
*   [0001-engineering-refactor.md](../specs/0001-engineering-refactor.md)

## 实施原则
1. **严格的红绿 TDD (测试驱动开发)**：编写任何业务代码前，必须先编写预期失败的测试。
2. **YAGNI (你不需要它)**：不要过度设计，只实现当下需求。

---

## 执行任务清单 (Task Breakdown)

### 任务 1: 基础设施骨架搭建 (Scaffolding)
*   **目标**: 建立项目基础环境和目录结构，确保可以安装包并运行空的测试。
*   **步骤**:
    1. 在项目根目录创建 `pyproject.toml` 文件。
        *   配置 `[build-system]` 使用 `setuptools`。
        *   配置 `[project]` 元数据，包括包名 `novel` 和版本 `0.1.0`。
        *   添加依赖: `pydantic`, `pydantic-settings`, `click`。
        *   添加可选测试依赖: `pytest`, `pytest-cov`。
        *   定义 CLI entry points: `novel = "novel.cli.main:cli"`。
    2. 创建 `.env.example`，加入示例变量 `OPENAI_API_KEY=your_key_here` 和 `PROJECT_ROOT=./novels`。
    3. 创建 `.gitignore`，忽略 `.env`, `__pycache__/`, `.pytest_cache/`, `*.egg-info/`, `.venv/`。
    4. 创建 `Makefile`，定义快捷指令: `install` (执行 `pip install -e ".[test]"`), `test` (执行 `pytest`)。
    5. 创建新目录树: `src/novel/`, `src/novel/cli/`, `src/novel/core/`, `src/novel/config/`, `src/novel/pipeline/`，并在其中放入空的 `__init__.py`。
    6. 创建 `tests/` 目录和 `tests/__init__.py`, `tests/conftest.py`。
*   **验证标准**: 运行 `make install` 成功，运行 `make test` 不报错。

### 任务 2: 统一配置管理模块开发 (Configuration Management)
*   **目标**: 接管所有的硬编码路径和 API 密钥加载。
*   **步骤**:
    1. **编写测试 (Red)**: 在 `tests/test_config.py` 中编写测试。
        *   测试能否从环境变量中正确加载 API Key。
        *   测试当缺少必填环境变量时是否能正确抛出 `ValidationError`。
    2. **编写代码 (Green)**: 在 `src/novel/config/settings.py` 中编写逻辑。
        *   继承 `pydantic_settings.BaseSettings`。
        *   定义必要的字段：`OPENAI_API_KEY` (SecretStr), `ANTHROPIC_API_KEY` (SecretStr, 可选), `PROJECTS_DIR` (默认值 `./novels`)。
        *   实例化全局的 `settings` 单例。
    3. **重构代码 (Refactor)**: 优化错误提示信息。
*   **验证标准**: `pytest tests/test_config.py` 100% 绿色通过。

### 任务 3: 原项目创建脚本迁移 (Refactoring project.py)
*   **目标**: 将散乱的 `scripts/project.py` 中的逻辑迁移到现代包架构下，并补全测试。
*   **步骤**:
    1. **分析旧代码**: 查看 `scripts/project.py` 中的 `ProjectManager` 逻辑（主要是根据模板复制文件）。
    2. **编写测试 (Red)**: 在 `tests/test_pipeline_project.py` 编写测试。
        *   测试 `create_project("test_book")` 能否在临时目录下正确生成设定文件夹和项目架构。
    3. **编写代码 (Green)**: 将逻辑重构后写入 `src/novel/pipeline/project_manager.py`。
        *   使用 `pathlib` 替代 `os.path`。
        *   通过 `settings.PROJECTS_DIR` 获取基础路径。
    4. **迁移检查**: 确保不破坏现有的 `data/schemas/` 目录结构。
*   **验证标准**: 测试覆盖率达到 90% 以上。

### 任务 4: CLI 命令行入口组装 (CLI Implementation)
*   **目标**: 淘汰直接运行 python 脚本的模式，暴露标准终端命令。
*   **步骤**:
    1. **编写测试 (Red)**: 创建 `tests/test_cli.py`。使用 `click.testing.CliRunner` 测试运行 `novel --help` 和 `novel new <book_name>` 的输出。
    2. **编写代码 (Green)**: 在 `src/novel/cli/main.py` 中使用 `click` 构建主命令 `cli()`。
        *   添加子命令 `@cli.command() def new(name): ...`，在内部调用 `project_manager.py`。
    3. **注册与安装**: 确保 `pyproject.toml` 中的 entry points 已正确配置并重新安装。
*   **验证标准**: 用户可以在终端任何地方直接输入 `novel new test_novel` 并成功生成项目。

### 任务 5: 旧日包袱清理 (Cleanup)
*   **目标**: 确保安全下线旧代码。
*   **步骤**:
    1. 跑一遍全量测试：`pytest`。
    2. 确认 `scripts/project.py`, `scripts/export.py` 等功能已经被新管线覆盖或后续不再需要。
    3. 运行 `rm -rf scripts/` 删除旧脚本目录（仅保留未来可能作为脚手架工具脚本的目录，如果确实没用了就全删）。
    4. 更新项目根目录的 `README.md`，写上新的快速开始指南（例如如何使用 `make install` 和 `novel --help`）。
*   **验证标准**: 项目结构完全清爽，无残留冗余代码，测试 100% 通过。
