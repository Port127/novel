# Novel V2 - Agent 全局规则

AI 小说写作工具，支持交互式创作和 CLI 操作。与 novel-material（上游素材库）配合使用。

## 技术栈

- Python 3.x
- YAML 数据格式
- Agent Skills（创作入口）+ CLI（管理工具）

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

## 使用方式定位

### Skills 是创作入口

创作类操作（大纲、人物、正文）**必须通过 Skills 交互式完成**，因为：

- 用户需要参与创意过程（写小说是跟 Agent 讨论出来的）
- 需要逐步询问、确认、调整
- **Agent 直接生成内容**，不调用脚本

**工作流**：
Skills → Agent 交互讨论 → 直接生成 YAML/Markdown → 不调用脚本

#### V4 Skill 架构

每个创作 skill 采用**自包含结构**（方案 B）：

```
.agents/skills/<skill-name>/
├── SKILL.md              ← 主文件：Phase 化流程 + 质量门禁定义
├── references/           ← 本 skill 专用的领域知识文件（按需加载）
│   ├── <topic-a>.md
│   └── ...
└── scripts/              ← 本 skill 专用的 JS 验证脚本
    ├── check-xxx.js
    └── ...
```

**核心机制**：

| 机制 | 说明 |
|------|------|
| **Phase 化流程** | 每个 Phase 有明确入口/出口条件，可独立执行和恢复 |
| **确定性脚本门禁** | JS 脚本做质量检查（blocking/advisory 两级），不靠 LLM 自查 |
| **断点恢复** | `_progress.md` 记录进度，崩溃后从断点续跑 |
| **References 按需加载** | 不一次全读，按 Phase 映射表加载对应文件 |
| **品类感知** | 根据 `scout_report.yaml` 的 `required_elements` 动态决定检查内容 |

| Skill | 用途 | Phase 数 | References | Scripts | 前置依赖 |
|-------|------|:--------:|:----------:|:-------:|---------|
| `scout-topic` | 选题侦察 | 6 | 4 | 1 | 无 |
| `worldbuilding` | 世界观设计 | 5 | 4 | 1 | 品类已选择 |
| `design-character` | 人设设计 | 5 | 5 | 1 | 品类已选择 |
| `design-outline` | 大纲设计 | 5 | 5 | 2 | 品类+世界观 |
| `design-chapters` | 细纲设计 | 5 | 3 | 1 | 大纲已完成 |
| `golden-chapters` | 黄金三章 | 6 | 4 | 3 | 品类+人设+细纲 |
| `paywall-design` | 付费卡点 | 5 | 4 | 1 | 大纲+黄金三章 |
| `daily-write` | 日更写作 | 6 | 6 | 3 | 章节已规划 |
| `export-novel` | 导出作品 | — | — | — | 正文已完成 |
| `nm` | 素材检索 | — | — | — | 无 |

### CLI 是管理工具

管理类操作**通过 CLI 命令完成**，因为：

- 机械操作，无需创意参与
- 执行明确，结果可预期
- **只做文件系统操作，不调用 LLM**

| 命令 | 用途 |
|------|------|
| `novel new` | 创建项目 |
| `novel list` | 列出项目 |
| `novel show` | 查看详情 |
| `novel delete` | 删除项目 |

### nm 是素材检索入口

需要参考时调用 `nm` skill：

- 查分类 → 检索参考 → 糅合建议

---

## Skills 详情

### 完整创作流程（9 阶段）

```
阶段0：选题侦察 (/scout-topic)
    ↓
阶段1：世界观设计 (/worldbuilding)
    ↓ 完善度 ≥ 80%
阶段2：人设设计 (/design-character)
    ↓ 完善度 ≥ 70%
阶段3：大纲设计 (/design-outline)
    ↓ 完善度 ≥ 85%
阶段4：细纲设计 (/design-chapters)
    ↓ 目标章节完善度 = 100%
阶段5：黄金三章锻造 (/golden-chapters)
    ↓
阶段6：付费卡点设计 (/paywall-design)
    ↓
阶段7：日更写作 (/daily-write)
    ↓
阶段8：导出作品 (/export-novel)
```

### /scout-topic — 选题侦察

**Phase 流程**：

```
Phase 1: 品类定位 → 品类确定
Phase 2: 平台分析 → 平台+读者确定
Phase 3: 选题决策 → premise+core_hooks 填写
Phase 4: 标签策略 → 标签组合通过 check-tags.js
Phase 5: 品类感知配置 → required_elements 填写
Phase 6: 报告定稿 → scout_report.yaml 落盘
```

**输出**：`settings/scout_report.yaml`

### /worldbuilding — 世界观设计

**前置依赖**：品类已选择

**Phase 流程**：

```
Phase 1: 品类适配 → 加载品类框架
Phase 2: 力量体系 → 等级/升级/战斗（如需要）
Phase 3: 社会结构 → 势力/规则（如需要）
Phase 4: 基础规则 → 世界规则（如需要）
Phase 5: 落盘验证 → check-completeness.js 检查
```

**输出**：`settings/worldbuilding.yaml`

### /design-character — 人设设计

**前置依赖**：品类已选择

**Phase 流程**：

```
Phase 1: 品类适配 → 加载角色框架
Phase 2: 主角设计 → traits + psychology + arc
Phase 3: 反派设计 → 动机 + 手段 + 恶心度（如需要）
Phase 4: 配角与关系网络 → 配角 ≥ 3 + 关系网
Phase 5: 爽感评估 → 三维评估 + check-characters.js
```

**输出**：`settings/characters.yaml`

### /design-outline — 大纲设计

**前置依赖**：品类+世界观

**Phase 流程**：

```
Phase 1: 品类适配与结构选择 → 三幕式/起承转合/英雄之旅
Phase 2: 骨架搭建 → 幕级大纲 + 张力曲线
Phase 3: 序列细化 → 每幕 2-5 序列
Phase 4: 节拍填充 → 每序列 3-8 节拍
Phase 5: 落盘验证 → check-outline.js + check-pacing.js
```

**输出**：`settings/outline.yaml` + `settings/arcs.yaml` + `settings/pacing.yaml`

### /design-chapters — 细纲设计

**前置依赖**：大纲已完成

**Phase 流程**：

```
Phase 1: 大纲解析 → 提取节拍列表
Phase 2: 章节拆分 → 每章 3-15 节拍，密/疏标记
Phase 3: 章节摘要 → 五要素摘要 + 出场人物
Phase 4: 张力曲线 → 每章张力值（1-5）
Phase 5: 落盘验证 → check-chapters.js
```

**输出**：`settings/chapters_index.yaml`

### /golden-chapters — 黄金三章锻造

**前置依赖**：品类+人设+细纲

**Phase 流程**：

```
Phase 1: 品类适配 → 加载品类黄金三章模板
Phase 2: 第一章锻造 → 300字内出冲突/钩子
Phase 3: 第二章锻造 → 金手指/核心优势亮相
Phase 4: 第三章锻造 → 首个小高潮
Phase 5: 去AI味 → check-ai-patterns.js + check-degeneration.js
Phase 6: 定稿输出 → chapter_001-003.md
```

**输出**：`content/chapter_001.md`、`content/chapter_002.md`、`content/chapter_003.md`

### /paywall-design — 付费卡点设计

**前置依赖**：大纲+黄金三章

**Phase 流程**：

```
Phase 1: 大纲分析 → 标记候选切点
Phase 2: 切点决策 → 评估候选点
Phase 3: 过渡设计 → 免费末章+付费首章
Phase 4: 平台适配 → 番茄/起点/晋江差异
Phase 5: 落盘验证 → check-paywall.js
```

**输出**：`paywall_report.yaml`

### /daily-write — 日更写作

**前置依赖**：章节已规划

**Phase 流程**：

```
Phase 1: 选题确认 → 确定目标章节
Phase 2: 上下文加载 → 前章末300字+本章细纲+追踪文件
Phase 3: 写作执行 → 2000-5000 字/章
Phase 4: 确定性检查 → check-ai-patterns.js + check-degeneration.js + normalize-punctuation.js
Phase 5: LLM 评估 → 反AI评分 ≥ 60 + 钩子评分 ≥ 60
Phase 6: 定稿 → content/chapter_XXX.md + 更新追踪
```

**断点恢复**：`_progress.md` 记录当前章节和 Phase，崩溃后自动续跑

**质量门禁**：
- JS 脚本：AI 模式检测、退化检测、标点规范
- LLM 评估：反AI五层评分 ≥ 60、钩子评分 ≥ 60

### /export-novel — 导出作品

**交互流程：**

```
1. 确认项目
   ↓
2. 询问导出格式（txt/md/epub）
   ↓
3. Agent 生成导出文件
   ↓
4. 展示导出路径
```

### /nm — 素材检索

**交互流程：**

```
1. 用户提出参考需求
   ↓
2. 切换到素材库项目：cd ../novel-material
   ↓
3. 执行检索命令（nm search chapter/outline/character/world/event/detail/insight）
   ↓
4. 展示检索结果（结构化摘要）
   ↓
5. 理解参考特点，糅合建议
```

---

## CLI 命令（管理工具）

### 项目管理

```bash
novel new "书名" --genre 修仙 --author 作者名 --template default
novel list
novel show <project_id>
novel delete <project_id>
```

### 统计查看

```bash
novel stats <project_id> [--detail]
```

### 导出

```bash
novel export <project_id> --format txt|md|epub
```

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
├── src/novel/                 # 核心引擎（退化为基础设施）
├── data/schemas/              # YAML Schema 定义
├── templates/                 # 项目模板
└── .agents/skills/            # Agent Skills（V4 自包含结构）
    ├── <skill-name>/
    │   ├── SKILL.md           # Phase 化流程定义
    │   ├── references/        # 领域知识文件
    │   └── scripts/           # JS 验证脚本
    └── _shared/scripts/       # 共享脚本（check-ai-patterns 等）
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

| 来源 | 使用方式 |
|------|----------|
| `settings/notes.yaml` | 项目内草稿区，Skill 自动读取 |
| 直接提供内容 | `--from-draft "想法..."` |
| 外部文件 | `--from-draft path/to/file.txt` |

### Schema 参考

| Schema | 路径 |
|--------|------|
| 项目元信息 | `data/schemas/project.schema.yaml` |
| 世界观 | `data/schemas/worldbuilding.schema.yaml` |
| 人物 | `data/schemas/characters.schema.yaml` |
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

**完善度检查命令**：
```bash
novel generate (内建检查) {project_id} worldbuilding
novel generate (内建检查) {project_id} characters
novel generate (内建检查) {project_id} outline
```

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
