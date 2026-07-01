# Core Generation & CLI TDD Implementation Plan

## 目标
遵循 Superpower 工作流，为核心生成链路 (Specs: `2026-06-25-core-cli-generation-design.md`) 补齐极度详尽的 TDD (测试驱动开发) 实施计划。虽然部分业务代码刚刚已被我越过流程直接写出，但依然必须通过严谨的单元测试体系进行回溯巩固与边界验证。

## 测试框架与环境
- 测试框架: `pytest`, `pytest-asyncio`
- Mock 工具: `unittest.mock.patch` 或 `pytest-mock` (核心要求：绝对隔离底层的 OpenAI API 调用，不能产生真实计费)

## 任务拆解与 TDD 计划

### 阶段 1: 核心管线测试 (Pipeline Tests)
**目标文件**: `tests/test_pipelines.py`
1. [ ] **测试世界观生成 (`test_generate_worldbuilding`)**: 
   - **前置准备**: 初始化 `ProjectManager` 并使用 `new` 创建临时测试项目。
   - **Mock**: `novel.core.llm.client.generate_text` 返回预设的标准 YAML 字符串。
   - **断言**: 检查管线返回字符串是否去除了 markdown 标记，且验证项目目录下真实生成了 `settings/worldbuilding.yaml`。
2. [ ] **测试人物/大纲生成 (`test_generate_outline`)**:
   - **前置准备**: 预先在临时项目中放置 `worldbuilding.yaml` 和 `characters.yaml`。
   - **断言**: 确保上下文组装逻辑读取到了上述文件，且能正常输出 `outline.yaml`。
3. [ ] **测试正文写作 (`test_write_new_chapter`)**:
   - **前置准备**: 提供章节设定的上下文环境。
   - **Mock**: 拦截 `generate_text` (返回草稿) 和 `run_qa_loop` (返回终稿)。
   - **断言**: 确保终稿成功写入 `content/chapters/chapter_1.md`，且验证字数或基础格式。

### 阶段 2: 命令行集成测试 (CLI Tests)
**目标文件**: `tests/test_cli_generation.py`
1. [ ] **测试 generate 命令组**:
   - **实现**: 使用 `click.testing.CliRunner` 执行 `novel generate world <test_id>`。
   - **断言**: Exit code 为 0，拦截标准输出包含 "✅ Generated worldbuilding" 字样。
2. [ ] **测试 write 命令组**:
   - **实现**: 使用 `CliRunner` 执行 `novel write new <test_id> 1`。
   - **断言**: Exit code 为 0，并且成功触发异步任务完成文本输出。

### 阶段 3: 异常与容错测试 (Edge Cases)
**目标文件**: `tests/test_edge_cases.py`
1. [ ] **非法 Project ID 拦截**: 
   - 传入不存在的项目 ID 给 `generate_worldbuilding`，断言是否抛出预期的 `ValueError`，且不会遗留脏目录。
2. [ ] **LLM 格式损坏容错**: 
   - 测试当大模型返回的文本带有异常的 Markdown block (````yaml... ```` 或者没有 block) 时，`removeprefix` 和 `removesuffix` 的清洗逻辑是否能保证写入最终文件的全是纯净的 YAML 内容。
