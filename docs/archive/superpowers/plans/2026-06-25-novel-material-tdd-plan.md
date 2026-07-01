# TDD 实施计划: Novel Material CLI 桥接接入 (2026-06-25)

## 1. 目标
通过测试驱动开发 (TDD)，以安全、解耦的 CLI 桥接模式实现 `novel` 对外部系统 `novel-material` 的检索调用，打通 V3 架构中外部检索微服务的基础链路。

## 2. 详细实现步骤 (TDD 循环)

### Step 1: 配置扩展 (Config)
*   **Test**: 在 `tests/test_config.py` 中增加对 `NOVEL_MATERIAL_DIR` 的验证。
*   **Impl**: 在 `src/novel/config/settings.py` 中向 `Settings` 类添加 `NOVEL_MATERIAL_DIR: str | None = None`，并通过 `.env` 注入。

### Step 2: 模型定义 (Models)
*   **Test**: 无需单独为纯数据结构写测试，将在下一步连带测试。
*   **Impl**: 在 `src/novel/core/memory/material_client.py` 中，定义用于承接 `nm` 命令输出的 Pydantic 模型：
    *   `MaterialSearchResult`: 包含 `id`, `text`, `score`, `metadata` (对应小说原数据、chapter等)。

### Step 3: MaterialClient 核心类 (Mocking Test)
*   **Test**: 创建 `tests/core/test_material_client.py`。
    *   使用 `unittest.mock.patch` 拦截 `asyncio.create_subprocess_exec`。
    *   **测试场景 1**: 模拟 `nm search insight` 成功返回一段合法 JSON，断言 `search_insight` 方法返回了正确的 `MaterialSearchResult` 列表。
    *   **测试场景 2**: 模拟 CLI 命令执行失败 (Return Code != 0) 或 JSON 解析失败，断言抛出合理的异常 (如 `MaterialServiceError`) 或降级返回空列表。
    *   **测试场景 3**: 测试当 `NOVEL_MATERIAL_DIR` 未配置时，客户端快速失败或返回空数据。
*   **Impl**: 实现 `MaterialClient` 类。
    *   使用 `asyncio.create_subprocess_exec` 在配置的 `NOVEL_MATERIAL_DIR` (即 `cwd`) 目录下执行 `["nm", "search", ...]`。
    *   实现方法：`async def search_insight(self, query: str, limit: int = 5) -> list[MaterialSearchResult]`

### Step 4: Context 组装工具 (Integration Helper)
*   **Test**: 在 `test_material_client.py` 增加一个对工具函数的测试，验证返回的 JSON 列表被正确组装成带有 `[Reference Material]` 标签的 Markdown 字符串。
*   **Impl**: 在 `material_client.py` 增加 `build_material_context(query: str) -> str` 辅助函数，将检索结果格式化为适用于大模型的 Prompt 注入块。

## 3. 设计决策确认

- **环境执行方式确认**：上述设计中，默认使用类似 `cd $NOVEL_MATERIAL_DIR && nm search ...` 的方式执行。这要求运行 `novel` 的机器必须能够在其路径下直接找到或激活 `nm` 环境。我们将默认尝试调用环境隔离下的 `nm` 命令。
- **后续规划**：完成上述基础 Client 后，我们就可以在 `generation_pipeline.py` 中择机注入 `build_material_context()` 的结果了。
