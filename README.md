# Novel V2

Skill 驱动的人机协同小说创作工作台，面向中文网文作者。

## 当前定位

本项目已从“自动化小说生成流水线”转向“Agent + Skills + 用户实时监督确认”的创作方式。创造性写作无法可靠地交给 CLI 自动流水线完成，必须在关键节点由作者判断、确认、回退和重写。

当前维护主线：

| 模块 | 状态 | 说明 |
|------|------|------|
| `.agents/skills/` | 主入口 | 选题、世界观、人设、大纲、章节、审查、导出等全部从 Skills 触发 |
| `.agents/agents/` | 协作角色 | 故事架构师、叙事写手、人设设计师、一致性检查员等专业视角 |
| `data/schemas/` | 数据约束 | YAML 设定文件的字段规范和质量检查依据 |
| `templates/` | 项目模板 | 新书目录与基础设定模板 |
| `novels/` | 写作项目 | 每本小说的设定、正文、草稿、导出文件 |
| `src/novel/`、`scripts/`、CLI | 冻结遗留 | 保留作历史实现和基础设施参考，不再作为产品主入口维护 |

## 核心原则

- **作者主导**：Agent 负责提出方案、生成草稿和执行检查，作者负责方向判断与最终确认。
- **阶段推进**：选题、设定、大纲、细纲、正文、付费卡点等按阶段推进，不跳阶段。
- **实时监督**：创造性产物必须在关键节点展示给用户确认，不能自动一路跑到底。
- **可回退**：发现方向不对时，回退到上游 Skill 重做，而不是在下游硬补。
- **可审查**：设定、正文、卡点、质量门禁结果都落到 YAML/Markdown/报告文件中。

## 核心功能

| 功能 | 说明 | 入口 |
|------|------|------|
| 选题侦察 | 品类选择、市场判断、读者定位、required_elements 配置 | `/scout-topic` |
| 世界观设计 | 力量体系、时代背景、地点、社会规则等 | `/worldbuilding` + `/nm` |
| 人设设计 | 主角、反派、配角、关系网络、爽感维度 | `/design-character` |
| 大纲设计 | 幕、序列、节拍、伏笔、张力曲线 | `/design-outline` |
| 细纲设计 | 章节拆分、章节摘要、张力值、节拍密度 | `/design-chapters` |
| 黄金三章 | 前三章微节拍锻造、开篇钩子、去 AI 味 | `/golden-chapters` |
| 付费卡点 | 切点选择、卡点倒推、过渡章、商业复核 | `/paywall-design` |
| 日更写作 | 按章节细纲生成正文，执行双层质量门禁 | `/daily-write` |
| 素材检索 | 调用 novel-material 检索同类参考 | `/nm` |
| 审查 | 多视角审查结构、文风、人设、一致性 | `/review` |
| 导出 | 按现有正文导出 TXT/Markdown/EPUB | `/export-novel` |

## Skill 架构

每个创作 Skill 采用自包含结构：

```text
.agents/skills/<skill-name>/
├── SKILL.md              # Phase 化流程、入口条件、出口条件、质量门禁
├── references/           # 领域知识文件，按 Phase 需要加载
└── scripts/              # JS 验证脚本，执行确定性检查
```

核心机制：

- **Phase 化流程**：每个 Phase 都有明确入口、动作、出口条件。
- **用户确认点**：关键选择必须让用户确认后再落盘或进入下一阶段。
- **JS 质量门禁**：blocking 必须修到 0，advisory 作为风险提示。
- **品类感知**：根据 `settings/scout_report.yaml` 的 `required_elements` 动态决定检查内容。
- **断点恢复**：长任务通过 `_progress.md` 记录当前阶段，便于恢复。

## 使用方式

直接和 Agent 对话，触发对应 Skill：

```text
“帮我选个品类”
→ /scout-topic → 选择品类 → 分析市场 → 确认选题 → 写入 scout_report.yaml

“帮我设计世界观”
→ /worldbuilding → 逐步讨论 → 质量检查 → 写入 worldbuilding.yaml

“帮我设计主角和反派”
→ /design-character → 逐步询问 → 爽感评估 → 写入 characters.yaml

“写第 1 章”
→ /daily-write → 确认章节摘要 → 写作 → 检查 → 用户确认 → 定稿
```

不要把 CLI 当作推荐入口。`novel new`、`novel generate`、`scripts/export.py` 等历史实现仍保留在仓库中，但不再作为当前创作流程的依据。

冻结遗留代码可能仍有 Python 测试未通过。除非任务明确要求维护 `src/novel/`、根目录 `scripts/` 或 `novel` CLI，否则这些测试结果不作为当前 Skill 主流程是否可用的判断依据。

## 创作流程

```text
阶段 0：选题侦察        → settings/scout_report.yaml
    ↓ 用户确认品类、读者、题材卖点
阶段 1：世界观设定      → settings/worldbuilding.yaml
    ↓ 检查 required_elements.worldbuilding
阶段 2：人物设定        → settings/characters.yaml
    ↓ 检查主角、反派、配角与爽感维度
阶段 3：大纲设定        → settings/outline.yaml + arcs.yaml + pacing.yaml
    ↓ 检查结构、伏笔、节奏
阶段 4：章节规划        → settings/chapters_index.yaml
    ↓ 每章摘要、节拍、张力值可审查
阶段 5：黄金三章        → content/chapter_001-003.md
    ↓ 检查开篇钩子、AI 味、退化问题
阶段 6：付费卡点        → paywall_report.yaml
    ↓ 检查切点、卡点倒推、商业复核
阶段 7：日更写作        → content/chapter_*.md
    ↓ 按章确认和定稿
阶段 8：导出作品        → exports/
```

强制顺序不是为了形式，而是为了避免后续正文建立在不稳定设定上。用户可以随时回退到上游阶段重做。

## 项目目录

```text
novel/
├── .agents/
│   ├── AGENTS.md              # Agent 全局规则
│   ├── agents/                # 专业子 Agent 提示词
│   └── skills/                # 当前主入口：创作、审查、导出、诊断等 Skills
├── data/schemas/              # YAML Schema 与完善度标准
├── docs/                      # 当前文档
├── templates/                 # 新书项目模板
├── novels/                    # 写作项目目录
├── src/novel/                 # 冻结遗留 Python 基础设施，不再作为主入口维护
└── scripts/                   # 冻结遗留脚本，不再作为主入口维护
```

单本小说目录：

```text
novels/{project_id}/
├── project.yaml
├── settings/
│   ├── scout_report.yaml
│   ├── worldbuilding.yaml
│   ├── characters.yaml
│   ├── outline.yaml
│   ├── arcs.yaml
│   ├── pacing.yaml
│   ├── chapters_index.yaml
│   ├── chapter_outlines/
│   └── notes.yaml
├── references/
├── content/
│   └── chapter_*.md
├── drafts/
├── exports/
└── _progress.md
```

章节规划采用双层结构：`settings/chapters_index.yaml` 是章节总索引和跨 Skill 调度表；`settings/chapter_outlines/chapter_*.md` 是单章详细蓝图，用于承载更长的分场、节拍、情绪和字数预算。下游 Skill 可以读取详细蓝图，但必须以章节总索引作为主入口。

## 文档导航

- [用户手册](docs/USER_MANUAL.md)：按用户目标说明如何触发 Skills。
- [需求文档](docs/REQUIREMENTS.md)：记录产品原则、维护边界和成功标准。
- [Pipeline 流程](docs/PIPELINE.md)：说明各阶段输入、输出、确认点、门禁和回退策略。
- [文档目录](docs/README.md)：文档入口和适用范围。
- [Schema 定义](data/schemas/)：YAML 文件字段规范。

如文档和冻结遗留 CLI/Python 代码冲突，以当前文档、`.agents/AGENTS.md` 和 `.agents/skills/` 为准。

## 与 novel-material 协作

`novel-material` 是上游素材检索库，本项目通过 `/nm` Skill 检索同类作品结构化参考。

```text
用户提出创作问题
→ /nm 查询分类或素材数量
→ 检索章节/大纲/人物/世界观/事件/细纲/深度分析
→ Agent 提炼可借鉴结构
→ 用户确认后糅合进当前项目
```

默认阈值：某类型素材少于 50 本时，建议先补充入库。入库操作由用户在 `novel-material` 项目中自行执行，本项目不自动触发。
