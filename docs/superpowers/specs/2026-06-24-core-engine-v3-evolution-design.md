# 核心引擎 V3 演进：真相文件、外部检索引擎与插件化技能架构设计

## 1. 背景

我们的核心引擎 (novel-v2) 已经实现了基于 Pydantic 的自愈生成器与基础 QA 循环，为稳定性打下了基础。然而对比周边同类的高级开源项目（如 `inkos`、`oh-story-claudecode`、`novel-material` 等），我们在处理“长篇小说上下文坍塌”和“深度网文技法适配”上存在明显短板：
1. **上下文容量崩溃**：当前纯文本加载的方式对于 500 章级别的超长篇毫无招架之力，极易导致大模型注意力涣散。
2. **事实一致性薄弱**：每次生成都缺乏对“已确立设定的真相”的强制校验与更新机制。
3. **缺乏“网文灵魂”**：目前的提示词过于基础，缺乏如“去 AI 味”、“黄金三章”、“情绪拉扯”等经由社区验证的成熟 Prompt 工程实践。

为解决上述问题，本设计方案旨在将引擎向 V3 版本演进。

## 2. 目标与非目标

### 2.1 目标
- **引入 PostgreSQL + pgvector 微服务架构**：对标 `novel-material`，对接外部千亿级存储能力的向量数据库，为后续超大规模小说的语义召回提供企业级地基。
- **构建后置审计与真相归约机制 (Reducer Pattern)**：对标 `inkos`，建立权威的 Markdown + YAML “真相文件”体系，并由独立的记录智能体 (Auditor) 负责维护。
- **设计插件化技能池 (Plugin Pipeline)**：对标 `awesome-novel-skill`，将写作套路与门禁检查抽象为独立的技能配置文件，使引擎获得极强的热插拔与扩展能力。

### 2.2 非目标
- 不开发 Web 端界面或复杂的可视化后台。
- 不修改原有的基础 `AsyncOpenAI` 客户端底座和 Pydantic 自愈逻辑，仅在更高维度进行编排。

## 3. 总体架构

```text
User Request
  │
  ▼
[Context Builder] <── (向量/分词联合检索) ──> [PostgreSQL + pgvector]
  │                                                  ▲
  ▼                                                  │ (异步写入)
[写作智能体 Writer Agent]                            │
  │                                                  │
  ▼                                                  │
[QA 插件化循环 QA Loop Pipeline]                     │
  ├── 插件 A: 悬念与情绪钩子检查 (Hook)              │
  ├── 插件 B: 去 AI 味洗稿清洗 (Deslop)              │
  └── 插件 C: 逻辑一致性校验                         │
  │                                                  │
  ▼ (定稿出炉)                                       │
[最新章节 New Chapter] ──────────────────────────────┘
  │
  ▼ (触发监听)
[归约智能体 Reducer Agent]
  ├── 阅读最新章节
  ├── 提取人物/时间线/设定的状态变化
  └── 更新本地 Truth Files (Markdown) 并同步至 PostgreSQL
```

## 4. 详细设计

### 4.1 PostgreSQL + pgvector 外部检索引擎
- 取消原本全部合并为单一长文本的 `context_builder.py`，取而代之的是 `pg_context_engine.py`。
- **存储方案**：对接外部 PostgreSQL 实例，创建 `truth_chunks` 和 `chapter_embeddings` 表。
- **检索逻辑**：在生成新章时，通过关键字（人物名、地名）与当前意图的 Embedding 结合进行混合检索 (Hybrid Search)，确保仅召回最核心的 Token 上下文。

### 4.2 后置审计与真相归约机制 (Truth Reducer)
- **目录规范**：在根目录建立 `truth/characters/`, `truth/timeline/` 和 `truth/rules/`。
- **异步处理**：主干流程生成章节后即告完成。随后异步拉起**专门的归约智能体 (Reducer Agent)**。
- **职责边界**：归约智能体的唯一任务是审读新章节，计算出“真相 Diff”，修改本地 Markdown 档案，并触发 PostgreSQL 的增量 Embeddings 更新。这种设计彻底将“写”和“记”解耦，大幅降低了写作 Agent 的负载，并提升了一致性。

### 4.3 插件化提示词技能池 (Plugin Pipeline)
- 摒弃在代码中硬编码长篇大论的 Prompt。
- **技能抽象**：新增 `src/novel/core/skills/` 目录。每个技能（如 `deslop.yaml`）包含：
  - `trigger_phase`: 触发阶段 (Draft, Review, Polish)
  - `system_prompt`: 注入的提示词
  - `evaluation_criteria`: 验收门禁规则（例如“不可出现‘宛如’等比喻”）
- **动态组装**：QA Loop 升级为 Pipeline 模式。引擎会根据当前项目的配置（如要求极度去 AI 味，同时需要虐主悬念），动态加载相应技能插件作为连续的评估器。

## 5. 失败处理与状态语义

| 异常情况 | 系统处理策略 | 影响范围 |
|---|---|---|
| PostgreSQL 连接断开 | 暂停 Context 检索与 Reducer 写入，触发警报并挂起流水线等待修复。 | 🔴 Blocker |
| QA 插件连续打回 | 若连续 3 次触发诸如 Deslop 插件的重写拦截，系统抛出警告并输出当前最好版本，避免无限循环。 | 🟠 Degraded |
| 归约智能体提取失败 | 新章节内容混乱导致无法归约设定，记录 `parse_error`，但不影响已发布的新章节。 | 🟡 Warning |

## 6. 测试策略与验收标准

- **架构解耦验收**：必须证明关闭 Reducer Agent 时，写作流程依然可以凭借现有 PostgreSQL 数据进行生成，证明其异步性。
- **插件动态加载验收**：通过添加一个测试用假插件 (dummy_skill.yaml)，必须能观测到生成的草稿被该插件强制改写，且移除插件后恢复正常。
- **向量召回验收**：需要准备一批不少于 100 章的测试小说语料库，测试 Context Builder 能否稳定在 2000 Tokens 的截断范围内召回前文埋下的微小伏笔。

## 7. 兼容与迁移

- 本次升级将引入重量级的 PostgreSQL 环境要求，建议通过 `docker-compose.yml` 提供开箱即用的本地容器支持以降低开发者的上手门槛。
- 原有的 `evaluation.yaml` 将提供向后兼容脚本，平滑迁移至新的 PostgreSQL 表结构中。
