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

| Skill | 用途 | 交互流程 | 前置依赖 |
|-------|------|----------|---------|
| `create-novel` | 统一入口（推荐）| 依赖检查 → 流程引导 → 按顺序完成 | 无 |
| `revise-setting` | 修订设定 | 选择类型 → 冲突检查 → 同步修订 | 设定存在 |
| `generate-outline` | 生成大纲 | 完善度检查 → 核心设定 → 结构 → 确认 | 世界观+人物 ≥ 阈值 |
| `generate-character` | 生成人物 | 完善度检查 → 主角 → 反派 → 配角 → 确认 | 世界观 ≥ 阈值 |
| `generate-chapter` | 章节规划 | 确认大纲 → 转化章纲 → 张力曲线 | 大纲完善 |
| `write-chapter` | 写正文 | 确认摘要 → 询问方向 → 生成 → 调整 | 章节规划存在 |
| `show-project` | 查看进度 | 确认项目 → 展示状态统计 | 无 |
| `export-novel` | 导出作品 | 确认项目 → 选择格式 → 导出 | 无 |
| `nm` | 素材检索 | 检索素材库（章节/大纲/人物/世界观/事件/细纲/深度分析）| 无 |

### CLI 是管理工具

管理类操作**通过 CLI 脚本完成**，因为：

- 机械操作，无需创意参与
- 执行明确，结果可预期
- **只做文件系统操作，不调用 LLM**

| CLI | 用途 |
|-----|------|
| `project.py` | 创建/删除/查看项目 |
| `stats.py` | 统计字数、章数、进度 |
| `export.py` | 导出 TXT/MD/EPUB |

### nm 是素材检索入口

需要参考时调用 `nm` skill：

- 查分类 → 检索参考 → 糅合建议

---

## Skills 详情

### /create-novel — 创作流程管理（推荐入口）

**核心原则**：小说应该"生长和演进"，而非"一次性生成"。

**交互流程：**

```
1. 检查项目状态（planning/drafting/revising/completed）
   ↓
2. 检查依赖完善度（worldbuilding/characters/outline）
   ↓
3. 根据状态引导用户进入正确阶段
   ↓
4. 跳阶段时阻止并提示缺失设定
```

**流程阶段**：

| 阶段 | 设定类型 | 前置依赖 | 完善度阈值 |
|------|---------|---------|-----------|
| 1 | 世界观 | 无 | 80% |
| 2 | 人物 | 世界观完善 | 70% |
| 3 | 大纲 | 世界观+人物完善 | 85% |
| 4 | 章节规划 | 大纲完善 | 100% |
| 5 | 正文 | 章节规划存在 | - |

**使用建议**：新项目推荐使用此 Skill，它会引导你逐步完成设定。

### /revise-setting — 修订设定

**交互流程：**

```
1. 选择设定类型（世界观/人物/大纲）
   ↓
2. 展示当前设定
   ↓
3. 询问修订内容
   ↓
4. 冲突检查（检查与其他设定的引用关系）
   ↓
5. 处理冲突（同步修订 / 取消）
   ↓
6. 完善度重新检查
```

**冲突检查**：修订势力 → 检查人物关联；修订人物 → 检查大纲引用。

### /generate-outline — 生成大纲

**交互流程：**

```
1. 确认项目（选择或创建）
   ↓
2. 检查前置完善度（强制）
   - worldbuilding ≥ 80% ?
   - characters ≥ 70% ?
   - 不满足 → 提示缺失字段，引导先完成前置设定
   ↓
3. 检查草稿来源（notes.yaml 或用户描述）
   ↓
4. 逐步询问：
   - 核心设定：一句话概括故事
   - 主角设定：名字、起点、终点
   - 冲突设计：外部冲突、内部冲突
   - 结构规划：章数、幕数
   ↓
5. 汇总展示，用户确认
   ↓
6. Agent 直接生成 outline/ 目录各文件
   ↓
7. 展示结果，询问是否调整
```

### /generate-character — 生成人物

**交互流程：**

```
1. 确认项目
   ↓
2. 检查前置完善度（强制）
   - worldbuilding ≥ 80% ?
   - 不满足 → 提示缺失字段，引导先完成世界观设定
   ↓
3. 检查已有世界观设定
   ↓
4. 逐步询问：
   - 主角：名字、性格、起点状态、终点状态
   - 反派：动机、与主角的冲突
   - 关键配角：功能定位、人物弧线
   - 人物关系：核心关系、张力来源
   ↓
5. 汇总展示，用户确认
   ↓
6. Agent 直接生成 characters/ 目录各文件
   ↓
7. 展示结果，询问是否调整
```

### /generate-chapter — 章节规划

**交互流程：**

```
1. 确认项目
   ↓
2. 检查大纲是否存在
   ↓
3. 确认章数范围
   ↓
4. Agent 直接生成 chapters/_index.yaml
   ↓
5. 展示张力曲线，询问是否调整
```

### /write-chapter — 写正文

**交互流程：**

```
1. 确认项目和章节号
   ↓
2. 展示章节摘要和上下文
   ↓
3. 询问写作方向（可选）
   ↓
4. Agent 直接生成正文 Markdown
   ↓
5. 展示正文，询问：
   - 接受？
   - 续写？
   - 改写（润色/扩展/精简）？
   ↓
6. 根据用户选择继续操作
```

### /show-project — 查看进度

**交互流程：**

```
1. 确认项目
   ↓
2. 展示：基本信息 + 统计 + 设定状态 + 章节进度
```

### /export-novel — 导出作品

**交互流程：**

```
1. 确认项目
   ↓
2. 询问导出格式（txt/md/epub）
   ↓
3. 调用 export.py 导出
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
├── settings/              # 设定文件（模块化目录）
│   ├── worldbuilding/
│   │   ├── power_system.yaml
│   │   ├── factions/_index.yaml + faction_*.yaml
│   │   ├── locations/_index.yaml + location_*.yaml
│   │   └── lore/*.yaml
│   ├── characters/
│   │   ├── protagonist/protagonist.yaml
│   │   ├── antagonist/_index.yaml + antagonist_*.yaml
│   │   ├── supporting/_index.yaml + supporting_*.yaml
│   │   └── relationships.yaml
│   ├── outline/
│   │   ├── premise.yaml
│   │   ├── acts/_index.yaml + act_*.yaml
│   │   ├── hooks.yaml
│   │   └── pacing.yaml
│   ├── chapters/
│   │   ├── _index.yaml
│   │   └── chapter_template.yaml
│   └── notes.yaml         # 草稿/笔记
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
├── src/novel/                 # V3 核心引擎及 CLI
│   ├── project.py             # 项目管理
│   ├── stats.py               # 统计查看
│   ├── export.py              # 导出
│   └── utils/
│       └── completeness_check.py  # 完善度检查
├── data/schemas/              # YAML Schema 定义
└── .agents/skills/            # Agent Skills
```

**注意**：generate.py、write.py、llm_client.py 已删除，Skills 直接生成内容。

---

## 状态流转

### 项目状态

```
planning → drafting → revising → completed
```

| 状态 | 说明 | 允许操作 |
|------|------|---------|
| planning | 设定阶段 | Skills: generate-outline, generate-character, generate-chapter |
| drafting | 写作阶段 | Skills: write-chapter |
| revising | 修改阶段 | Skills: write-chapter (改写模式) |
| completed | 完成 | CLI: export |

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
