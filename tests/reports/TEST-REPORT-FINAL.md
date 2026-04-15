# 测试执行报告

> 执行时间：2026-04-09
> 测试目标：Novel Writing System（Backend API + 文件完整性 + 跨模块一致性）

---

## 执行概况

| 轮次 | 描述 | 用例数 | 通过 | 失败 | 通过率 | 耗时 |
|------|------|--------|------|------|--------|------|
| Round 1 | 基础 API 全覆盖 | 134 | 134 | 0 | 100.0% | 2.0s |
| Round 2 | 深层数据一致性 & 压力测试 | 63 | 63 | 0 | 100.0% | 6.6s |
| Round 3 | 文件审计 & 工作流模拟 | 92 | 91 | 1 | 98.9% | 1.6s |
| **总计** | | **289** | **288** | **1** | **99.7%** | **10.2s** |

---

## 测试覆盖范围

### Round 1：基础 API 全覆盖（134 例）
- Health endpoint
- **项目管理**：list / current / switch / 404 处理
- **项目创建**：模拟 novel-init（复制模板、写 meta/state、目录结构验证）
- **角色 CRUD**：创建 / 读取 / 更新 / 删除 / 409 冲突 / 404 缺失 / 特殊字符名
- **世界观 CRUD**：创建 / 读取 / 更新 / 删除 / 状态流转 / 409 / 404
- **章节 CRUD**：创建 / 读取内容 / 更新内容 / 更新元数据 / 删除 / 文件一致性
- **大纲**：GET / PUT / 内容持久化
- **时间线**：GET / POST 多事件 / 多角色事件
- **关系**：GET 关系 / GET 事件（只读 API）
- **合规/质量**：inspirations / risks / ai-trace 读取
- **Skills**：列表 / 分类 / 404 处理
- **跨模块**：state.yaml 精简性 / YAML 完整性 / 索引-文件一致性
- **边界**：Unicode / 孤儿章节 / CORS
- **现有项目读取**：灵气复苏 + 末世 两个真实项目的数据读取验证

### Round 2：深层数据一致性 & 压力测试（63 例）
- **孤儿检测**：删文件留索引 / 添文件缺索引 / 删角色残留关系 / 删章节残留钩子
- **批量压力**：20 角色 / 15 设定 / 10 章节的快速 CRUD
- **数据格式**：Emoji / 超长名 / 空内容 / 5 万字大章节 / 深嵌套 / YAML 特殊字符
- **项目隔离**：3 个项目间切换无交叉污染
- **状态一致性**：所有 YAML 可解析 / 索引-文件匹配 / meta/state 内容检查
- **API 错误处理**：无效 JSON / 缺字段 / 404 / 405 / 只读端点 POST
- **时间线**：同时间事件 / 空时间事件
- **章节状态机**：正向流转 / 跳过 / 回退 / 无效状态（无护栏）
- **快速 CRUD**：10 轮角色 + 5 轮章节的完整 create-read-update-delete 循环
- **项目切换压力**：15 次快速切换后数据隔离验证

### Round 3：文件审计 & 工作流模拟（92 例）
- **灵气复苏项目审计**：目录结构 / YAML 完整性 / 角色索引 / 五件套 / 世界观索引 / 章节文件 / 大纲 / 关系 / state / ingestion_brief / PROJECT_MAP
- **末世项目审计**：结构 / YAML / 索引 / 章节内容 / 导出
- **模板完整性**：19 个模板文件存在性 + YAML 可解析性
- **损坏恢复**：畸形 YAML / 奇怪内容 / state.yaml 缺失 / 空 YAML / 纯空白 YAML
- **完整工作流模拟**：创建 4 角色 → 3 设定 → 写大纲 → 创建 2 章（含真实正文）→ 更新状态 → 时间线 → 全链路验证
- **API 响应格式一致性**：10 个端点的返回结构规范检查

---

## 发现的问题

### BUG-001：角色 API 路由与索引 name/file 不匹配（严重）

**位置**：`backend/routers/characters.py` → `_char_path(name)`

**现象**：
- `character_index.yaml` 中 `name` 字段可以和 `file` 字段（即实际文件名）不同
- 但 API 的 `GET /api/characters/{name}` 始终用 `name` 构造文件路径：`characters/{name}.yaml`
- 当 `name ≠ 文件名` 时，API 返回 404

**复现**：
```
GET /api/characters/阮声         → 404（索引里叫"阮声"，文件叫"倒灌者·无名.yaml"）
GET /api/characters/倒灌者·无名  → 200（直接用文件名能访问）
GET /api/characters/韩炽 / 韩凝  → 404（索引里叫"韩炽 / 韩凝"，文件叫"共振者·双子.yaml"）
GET /api/characters/共振者·双子  → 200（直接用文件名能访问）
```

**影响**：
- 前端从索引获取角色列表后，用 `name` 去请求详情，会 404
- 更新（PUT）和删除（DELETE）同样受影响
- 涉及的现有角色：阮声、韩炽/韩凝

**修复建议**：
1. `GET /{name}` 先查 `character_index.yaml`，从匹配条目的 `file` 字段获取实际路径
2. 或者：确保 `name` 和 `file` stem 始终一致（skill 层约束）

---

### FINDING-001：API 层无章节状态机护栏（设计缺陷）

**现象**：
- `PUT /chapters/{id}/meta` 的 `status` 字段无验证
- 可以直接 `outline → final`（跳过 draft/revise）
- 可以 `final → draft`（任意回退）
- 可以设为 `invalid_status`（无效值也接受）

**影响**：
- Skill 层有状态保护逻辑，但直接 API 调用绕过了保护
- 前端如果直接调 API 修改状态，可能产生不合规的状态流转

---

### FINDING-002：删除操作不清理跨模块引用（设计缺陷）

**现象**：
- `DELETE /characters/{name}` 不清理 `relations.yaml` 中的相关记录（孤儿关系）
- `DELETE /chapters/{id}` 不清理 `outline.yaml` 的 `foreshadowing` 中引用该章的钩子（孤儿钩子）
- `DELETE /worldbuilding/entries/{id}` 不清理引用方的 `character_links`/`setting_links`

**影响**：
- 多次删除后数据中累积"幽灵引用"
- 需要定期 `/project-reindex` 清理

---

### FINDING-003：灵气复苏项目角色索引实际不一致

**现象**：
- `character_index.yaml` 中有 `韩炽 / 韩凝` 和 `阮声`
- 实际文件名是 `共振者·双子.yaml` 和 `倒灌者·无名.yaml`
- 索引的 `file` 字段正确指向了实际文件，但 `name` 字段与文件名不匹配

**影响**：
- 与 BUG-001 叠加，这两个角色通过 API 完全不可按名字访问
- 前端列表能看到但点击看不到详情

---

### FINDING-004：API 未校验写入数据格式

**现象**：
- 角色/章节/设定的自定义 `data` 字段无 schema 验证
- 任何结构的 JSON 都能写入
- 时间线事件的 `time` 可以为空字符串

**影响**：
- 理论上不是 bug（灵活性设计），但可能导致垃圾数据
- 建议至少对核心字段做最小验证

---

## 未覆盖的领域（需后续测试）

| 领域 | 原因 | 建议 |
|------|------|------|
| LLM Skill 执行（`/api/skills/execute`） | 需要有效的 LLM API key | 配置后测试 SSE 流 |
| 前端 UI 交互 | 需要启动前端服务 | 手动 + E2E 测试 |
| Skill 文件级行为 | Skills 是 AI 指令，非可执行代码 | 通过 AI 对话测试 |
| 并发写入竞态 | Python 单进程 | 多线程压力测试 |
| `.cursor/rules/` 同步 | 需要 Cursor 环境 | 手动验证 |

---

## 测试数据位置

| 文件 | 内容 |
|------|------|
| `tests/run_tests.py` | Round 1：基础 API 测试（134 例） |
| `tests/run_tests_deep.py` | Round 2：深层测试（63 例） |
| `tests/run_tests_audit.py` | Round 3：审计和工作流（92 例） |
| `tests/test-report.json` | Round 1 JSON 结果 |
| `tests/test-report-deep.json` | Round 2 JSON 结果 |
| `tests/test-report-audit.json` | Round 3 JSON 结果 |
| `tests/manual-test-cases.md` | 完整 442 条测试设计文档 |
| `projects/测试小说_自动化/` | 测试创建的完整小说项目（含角色、章节、设定等真实数据） |
