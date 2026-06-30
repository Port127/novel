# Novel V4 - Agent 全局规则

AI 小说写作工具，基于纯 Skill 驱动。与 novel-material（上游素材库）配合使用。

## 技术栈与运行环境

- **Python 3.12+**
- **Node.js (v24+)**：用于运行各技能的确定性检查门禁（JS 脚本）。
- **Git**：用于版本控制与规范化提交。
- **YAML**：作为所有设定数据和元信息的载体。
- **环境优先级**：Agent 执行任何终端任务时，**必须优先使用本机 Conda 环境（当前为 `env3.12`）**，其次才是系统默认环境。

---

## 语言与沟通规范

- 所有面向用户的回复、计划、任务说明、进度更新、分析结论、决策依据、错误说明和新编写的说明性文档默认使用简体中文。
- 内部隐藏推理不会展示；所有对用户可见的推理摘要和判断依据必须使用中文。
- 命令、代码、路径、配置键、字段名、API 名称、模型名称和无法准确翻译的专有名词可以保留原文。
- 用户明确要求使用其他语言时，以用户当前请求为准。

## Git 提交规范

使用 `commit-msg` skill 生成提交信息，遵循 Conventional Commits 格式。

## 自动化工作流与 Superpower 规则

- **强制应用 Superpower 工作流**：在接收到任何非微小的开发任务、架构设计或新功能请求时，不需要用户明确指示，Agent 必须强制执行以下流程：
  1. 自动触发并应用 `brainstorming` 技能，探讨并编写 Specs 文档，并请求用户审查。
  2. 在用户审查 Specs 通过后，自动触发 `writing-plans` 技能编写极度详尽的 TDD 实施计划，并请求用户审查。
  3. 计划通过后，主动向用户提供 `subagent-driven-development` 或 `executing-plans` 两种执行方式供选择。
- **无商量余地**：绝不允许"因为觉得项目太简单"或"这是一个小功能"而跳过上述 `brainstorming` (设计) 和 `writing-plans` (计划) 流程。必须严格产出 `docs/superpowers/specs/...` 和 `docs/superpowers/plans/...`。

## 强制前置思考（拦截规则）

在输出任何实施计划（Implementation Plan）或调用写文件/修改工具之前，你**必须**在思考或回复的开头明确输出以下格式的自检块：

```superpower-check
1. 当前处于流程的第几步？(1. Specs / 2. TDD Plans / 3. Execution)
2. 用户是否已经明确审查 (review) 并批准了上一步的输出？(是/否)
3. 如果未获明确批准，我接下来直接写代码或跑命令的行为是否违规？(是/否)
```
【系统红线】：只有当自检块显示"已获用户批准（第2项为是）"，你才可以继续往下调用工具；否则必须主动停下等待用户。

---

## All-in-Skill 架构与使用方式

本项目已全面废除传统的 Python CLI 命令。所有的创作、管理、审查、导出、检查，**全部由 Agent 结合 Skills 和 JS 脚本**完成。

### Skills 是唯一入口

无论是创作小说、诊断数据，还是开发新功能，**必须通过触发对应的 Skill 交互式完成**。

**工作流**：
用户指令 → 命中对应 Skill → Agent 按照 `SKILL.md` 流程执行 → 调用内置 JS 脚本进行确定性门禁检查 → 生成 YAML/Markdown。

#### V4 Skill 架构全景图

每个 skill 采用**自包含结构**，按职责分为三大核心板块：

**1. 核心创作流 (The 9 Phases)**
| Skill | 用途 | 前置依赖 |
|-------|------|---------|
| `scout-topic` | 选题侦察（定位与受众） | 无 |
| `worldbuilding` | 世界观设计（力量/社会/规则） | 品类已选择 |
| `design-character` | 人设设计（主角/反派/配角） | 品类已选择 |
| `design-outline` | 大纲设计（结构/序列/节拍） | 品类+世界观 |
| `design-chapters` | 细纲设计（章节拆分/张力曲线） | 大纲已完成 |
| `golden-chapters` | 黄金三章（微节拍锻造） | 品类+人设+细纲 |
| `paywall-design` | 付费卡点（转折点决策） | 大纲+黄金三章 |
| `daily-write` | 日更写作（2000-5000字执行） | 章节已规划 |
| `nm` | 素材检索（调用上游库） | 无 |

**2. 运营与审查流**
| Skill | 用途 |
|-------|------|
| `review` | 多视角对抗式审查（调用子 Agent 并行或串行审查） |
| `data-diagnosis` | 数据诊断（导入平台数据，分析追读/互动，定位问题章节） |
| `stock-check` | 存稿看板（查看存稿水位、成本报告、应急建议） |
| `export-novel` | 导出作品（将正文编译为 txt/md/epub） |

**3. 开发与超级工作流**
| Skill | 用途 |
|-------|------|
| `feature-planning` | 新功能开发规划（Specs -> 实施步骤） |
| `refactor-planning` | 重构计划制定 |
| `code-review-change` | 变动影响与隐患审查 |
| `commit-msg` | 规范化 Git 提交信息生成 |

---

## 强制信息源约束（Skills 详情规避）

> [!IMPORTANT]  
> **Agent 严禁依赖自身记忆或本全局文件的概括来执行具体技能！**
> 因为每个技能的具体 Phase 流程、约束条件和输出格式可能会随时更新，全局规则不负责记录这些执行细节。

**执行规则**：
每当需要进入一个新的 Skill（如 `scout-topic`、`worldbuilding` 等），你必须使用 `view_file` 工具去完整读取该技能目录（`.agents/skills/<skill-name>/`）下的 `SKILL.md` 文件。
如果 `SKILL.md` 引用了 `references/` 下的知识文件或 `data/schemas/` 下的数据字典，**也必须老老实实去读取源文件**，绝对不准靠猜测生成内容。

---



## 目录结构

### 项目目录

```
novels/{project_id}/
├── project.yaml           # 项目元信息
├── settings/              # 设定文件（扁平化结构）
│   ├── worldbuilding.yaml # 世界观设定
│   ├── characters.yaml    # 人物设定
│   ├── outline.yaml       # 大纲
│   ├── arcs.yaml          # 细纲（Arc结构）
│   ├── pacing.yaml        # 节奏规划
│   ├── chapters_index.yaml # 章节索引
│   └── notes.yaml         # 草稿/笔记
├── references/            # 项目特有参考资料
│   ├── 2009_era_details.yaml
│   ├── locations/
│   ├── dungeons/
│   └── ...
├── content/chapters/      # 章节正文
│   └── chapter_*.md
├── drafts/                # 草稿文件夹
├── exports/               # 导出文件
└── history/               # AI 生成历史
```

### 项目根目录

```
novel/
├── novels/                    # 写作项目目录
├── src/novel/                 # 历史遗留/纯基础设施
├── data/schemas/              # YAML Schema 定义
├── templates/                 # 项目模板
├── scripts/                   # 全局工具脚本
├── .superpowers/              # TDD Plans 和 Specs 规划文档存放区
├── .agents/agents/            # 专业子 Agent 提示词定义
└── .agents/skills/            # Agent Skills（V4 自包含结构）
    ├── <skill-name>/
    │   ├── SKILL.md           # Phase 化流程定义
    │   ├── references/        # 领域知识文件
    │   └── scripts/           # JS 验证脚本
    └── _shared/scripts/       # 共享脚本
```

**核心原则**：创作类操作全部通过 Skills 完成，Agent 直接生成内容。质量门禁由 JS 脚本（确定性检查）+ LLM 评估（语义检查）双层保障。

---

## 状态流转

### 项目状态

```
planning → drafting → revising → completed
```

| 状态 | 说明 | 允许操作 |
|------|------|---------|
| planning | 设定阶段 | Skills: worldbuilding, design-character, design-outline, design-chapters |
| drafting | 写作阶段 | Skills: golden-chapters, paywall-design, daily-write |
| revising | 修改阶段 | Skills: daily-write (改写模式) |
| completed | 完成 | Skills: export-novel |

### 章节状态

```
planned → draft → written → revised
```

| 状态 | 说明 |
|------|------|
| planned | 已规划，有摘要，无正文 |
| draft | 有正文（< 1500 字）|
| written | 正文完成（≥ 1500 字）|
| revised | 已润色修改 |

---

## 开发规范

### ID 规范

格式：`nv_{YYYYMMDD}_{random4}`（系统自动生成）

### 草稿系统

- **项目内草稿**：优先记录/读取 `settings/notes.yaml`，作为跨技能的备忘录。
- **用户直接提供**：通过对话交互式让用户提供脑洞想法。
- **外部文件导入**：直接使用 `view_file` 读取用户指定的本地文件内容。

### Schema 参考约束

> [!WARNING]
> Agent 在生成任何设定 YAML（如世界观、人设、大纲等）之前，**必须**使用 `view_file` 读取对应的 `.schema.yaml` 文件！严禁按自己的理解随意构造数据结构！

| Schema | 路径 |
|--------|------|
| 项目元信息 | `data/schemas/project.schema.yaml` |
| 世界观 | `data/schemas/worldbuilding.schema.yaml` |
| 人设 | `data/schemas/characters.schema.yaml` |
| 大纲 | `data/schemas/outline.schema.yaml` |
| 章节 | `data/schemas/chapters.schema.yaml` |
| **完善度标准** | `data/schemas/completeness.schema.yaml` |

---

## 硬规则

**必须：**
- 创作类操作使用 Skills 交互式完成
- 逐步询问，不跳过用户确认
- 尊重已有设定，逐步细化让用户确认
- 状态流转按顺序进行
- **强制完善度检查**：前置设定必须达标才能进入下一阶段

**禁止：**
- 跳过用户确认直接生成
- 在未规划章节时写作正文
- 修改已 revised 状态章节时不创建备份
- **跳阶段**：未完成世界观时生成人物/大纲，未完成人物时生成大纲

**完善度检查机制**：
不再使用命令行进行校验。阶段流转的阻断与放行，**完全依赖执行所在 Skill 的 `/scripts/` 目录下的 JS 脚本**（例如 `check-tags.js`, `check-completeness.js`）。如果 JS 脚本报 blocking 错误，Agent 必须停下并修正。

---

## 与 novel-material 的协作

通过 `/nm` skill 调用素材库：

### 能力范围

| 能力 | 命令 | 说明 |
|------|------|------|
| 素材列表 | `nm material list` | 查已入库素材列表 |
| 入库数量检查 | `nm material list --genre` | 查某类型已入库数量 |
| 章节检索 | `nm search chapter` | 语义搜索同类章节写法 |
| 大纲检索 | `nm search outline` | 查同类大纲结构 |
| 人物检索 | `nm search character` | 查同类人物塑造 |
| 世界观检索 | `nm search world` | 查同类世界观设定 |
| 事件检索 | `nm search event` | 查同类事件场景 |
| 细纲检索 | `nm search detail` | 查同类细纲结构 |
| 深度分析检索 | `nm search insight` | 查 chapter_insights 深度分析 |

### 使用流程

```
用户写作 → 切换到素材库项目 → 执行检索命令
    → 数量不足？提示用户执行 nm pipeline full 入库
    → 检索到参考 → 展示结构化摘要 → 糅合写作
```

### 入库阈值

默认阈值：某类型素材少于 **50 本** 时建议入库。

### 入库操作

入库需用户**自己切换到 novel-material 项目**执行：

```bash
cd ../novel-material
nm pipeline full <文件路径>
```

Agent 不自动触发入库操作。

---

## 授权模式

本项目使用**完全授权模式**。Agent 可自主执行以下操作：

- Bash/Shell 命令、Git 操作、文件系统操作
- 包管理器（npm、pip 等）
- 文件读写、创建、删除
- Web 搜索和获取
- 运行后台任务、测试、部署

敏感操作会显示提示，但 Agent 可自主决定执行。

---

## Agent 协作 (Orchestration)

本项目部署了 4 个专业 Agent（定义在 `.agents/agents/`）：

| Agent | 职责 | 工具权限 |
|-------|------|---------|
| story-architect | 故事架构师：题材/世界观/大纲/反转/情绪弧线 | Read+Write+Edit |
| narrative-writer | 叙事写手：正文写作/去AI味/格式合规 | Read+Write+Edit |
| character-designer | 角色设计师：角色设定/对话风格/人物弧线 | Read+Write+Edit |
| consistency-checker | 一致性检查员：事实冲突/伏笔断线/时间线检测 | 只读 (Read+Glob+Grep) |

### 调用方式与通信

1. **编排与唤醒**：主 Agent（作为 Orchestrator）在关键步骤时，**必须主动使用 `invoke_subagent` 工具**，唤醒对应的 Agent 在后台工作。
2. **通信**：唤醒后，主 Agent 使用 `send_message` 工具与子 Agent 进行对话、派发任务或收取结果。
3. **独立审查指令**：使用 `/review` 触发对应 skill，启动多 Agent 对抗式审查：
   - `full` 模式：并行 spawn 4 个 Agent。
   - `lean` 模式：只 spawn 架构师 + 检查员。
   - `solo` 模式：主线程自行审查。

### 降级策略

所有 agent 调用遵循统一降级规则。如果在特定沙箱环境或资源受限时，`invoke_subagent` 工具不可用：
1. `.agents/agents/{agent}.md` 不存在 → solo
2. Agent spawn 失败 → solo，并在回复中标注 `Fallback: spawn failed -> solo`
3. 当前已在 subagent 内部 → 不允许嵌套 spawn，直接 fallback 到 solo。

此时主 Agent 需要将子 Agent 的提示词内容加载到自身的上下文中，直接进行 Roleplay 完成任务。
