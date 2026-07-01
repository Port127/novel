# Agent 协作体系设计

## 概述

为 novel 项目实现多 Agent 协作能力，参考 oh-story-claudecode 的 agent 设计，在 ZCode 上实现等价的多 agent 并行审查与辅助创作能力。

**核心决策**：
- 单模型（不使用 model 参数分级）
- 完整 markdown 定义文件（agent 方法论内嵌在定义中）
- 复用现有 skill references（不新建冗余参考文件）
- 保持现有 9 个 skill 的流水线结构，增量嵌入 agent 调用
- 新增独立 review skill 做多视角对抗式审查
- 暂不实现 hooks

---

## 架构

### 方案：Agent Registry + Standard Protocol

在 `.agents/agents/` 下建立 agent 注册表，每个 agent 一个完整 markdown 定义文件，约定统一的 spawn 协议（输入/输出契约）。

### 目录结构

```
.agents/
├── agents/                          # Agent 注册表
│   ├── story-architect.md           # 故事架构师
│   ├── narrative-writer.md          # 叙事写手
│   ├── character-designer.md        # 角色设计师
│   └── consistency-checker.md       # 一致性检查员
├── skills/
│   ├── review/                      # 新增：独立审查 skill
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── quality-rubric.md    # 通用评分 rubric
│   │       └── rubrics/
│   │           ├── fanqie.md        # 番茄平台标准
│   │           ├── qidian.md        # 起点平台标准
│   │           └── zhihu.md         # 知乎平台标准
│   ├── daily-write/                 # 现有，微调（+2 处 agent 调用）
│   ├── design-outline/              # 现有，微调（+1 处 agent 调用）
│   ├── design-character/            # 现有，微调（+1 处 agent 调用）
│   ├── golden-chapters/             # 现有，微调（+1 处 agent 调用）
│   └── ...                          # 其他 skill 不动
└── AGENTS.md                        # 现有，补充 agent 使用说明
```

---

## Agent 定义格式

每个 agent 是一个完整的 markdown 文件，结构如下：

```yaml
---
name: {agent-name}
version: 1.0.0
role: |
  一句话描述角色定位和核心职责。
capabilities: [创作, 审查]  # 或 [审查] 表示只读
tools: [Read, Glob, Grep, Write, Edit]  # consistency-checker 只有 Read/Glob/Grep
---
```

文件内容包含以下 section：

1. **角色定义**：你是谁，核心价值是什么
2. **参考文件路径规则**：如何查找 references（指向现有 skill 的 references 目录）
3. **参考文件体系**：表格列出每个参考文件及其使用时机
4. **创作能力**：方法论、具体技法、输出格式
5. **审查能力（附属）**：对抗性审查 prompt、检查项清单（只读 agent 无此节）
6. **禁止事项**：明确的负面约束
7. **职责边界**：拥有/不拥有的职责范围
8. **被调用协议**：标准的输入/输出契约

### 参考文件路径规则

Agent 引用参考文件时，按以下顺序查找：

1. `.agents/skills/{当前skill}/references/{文件名}` — 当前 skill 的 references
2. `.agents/skills/{其他skill}/references/{文件名}` — 其他 skill 的 references（按参考文件体系表指定的来源 skill）
3. `.agents/shared/references/{文件名}` — 全局共享 references（如有）

禁止只读裸文件名、禁止跨 agent 引用。

### 被调用协议（统一格式）

```markdown
## 被调用协议

skill 通过 Agent 工具调用你。

### 输入（skill 必须提供）
- `项目根目录`：绝对路径
- `任务类型`：创作 | 审查
- `查询参数`：具体任务描述
- `相关文件路径`：需要读取的文件列表

### 输出（你必须返回）
创作任务：结构化方案（markdown）
审查任务：
VERDICT: APPROVE / CONCERNS / REJECT
FINDINGS:
  - severity: S1/S2/S3/S4
    category: structure | character | prose | consistency | platform | factual | format
    location: 文件路径:行号
    evidence: "引用原文"
    issue: "问题描述"
    fix: "可执行修改建议"
RECOMMENDATIONS: [...]
```

### 统一 Findings Schema

所有 agent 输出审查结果时必须使用统一结构：

```yaml
- severity: S1 | S2 | S3 | S4
  category: structure | character | prose | consistency | platform | factual | format
  location: 文件路径:行号
  evidence: "引用原文或具体证据"
  issue: "问题描述"
  fix: "可执行修改建议"
```

严重度定义：
- **S1**：破坏主线/角色动机/世界规则，需优先修
- **S2**：明显影响效果/留存/节奏，建议本轮修
- **S3**：局部质量问题，可排期修
- **S4**：建议项或风格微调，不阻塞

---

## 4 个 Agent 的职责设计

### 1. Story Architect（故事架构师）

**核心职责**：宏观叙事工程——题材定位、世界观构建、大纲排布、钩子/悬念/反转设计、情绪弧线、范围控制。

**被谁调用**：

| Skill | 调用时机 | 任务 |
|-------|---------|------|
| `design-outline` | Phase 3 大纲搭建 | 辅助结构设计、反转工程、情绪弧线 |
| `scout-topic` | Phase 2 题材定位 | 辅助题材分析和核心梗设计 |
| `review` | 审查 | 从结构视角找问题 |

**参考文件来源**：

| 参考文件 | 来源 skill |
|---|---|
| `hooks-guide.md` | daily-write |
| `outline-structure.md` | design-outline |
| `pacing-guide.md` | design-outline |
| `plot-frameworks.md` | design-outline |
| `foreshadowing-guide.md` | design-outline |
| `tension-curve.md` | design-outline |
| `genre-catalog.md` | scout-topic |
| `topic-decision.md` | scout-topic |
| `world-rules.md` | worldbuilding |
| `power-system-guide.md` | worldbuilding |

**工具权限**：Read, Glob, Grep, Write, Edit

---

### 2. Narrative Writer（叙事写手）

**核心职责**：正文生成、情绪弧线执行、去 AI 味、格式合规。

**被谁调用**：

| Skill | 调用时机 | 任务 |
|-------|---------|------|
| `daily-write` | Phase 4 正文写作 | 执行正文生成 |
| `golden-chapters` | Phase 3 正文生成 | 黄金三章正文写作 |
| `review` | 审查 | 从文字质量视角找问题（AI 味/格式/节奏） |

**参考文件来源**：

| 参考文件 | 来源 skill |
|---|---|
| `anti-ai-writing.md` | daily-write |
| `banned-words.md` | daily-write |
| `writing-flow.md` | daily-write |
| `quality-checklist.md` | daily-write |
| `hooks-guide.md` | daily-write |
| `genre-templates.md` | golden-chapters |
| `micro-beat-guide.md` | golden-chapters |
| `golden-rules.md` | golden-chapters |

**工具权限**：Read, Glob, Grep, Write, Edit

---

### 3. Character Designer（角色设计师）

**核心职责**：角色设定、对话风格、人物弧线、关系网络设计。

**被谁调用**：

| Skill | 调用时机 | 任务 |
|-------|---------|------|
| `design-character` | 交互式设计阶段 | 辅助主角/反派/配角深度设计 |
| `review` | 审查 | 从角色/对话视角找问题 |

**参考文件来源**：

| 参考文件 | 来源 skill |
|---|---|
| `character-basics.md` | design-character |
| `protagonist-arc.md` | design-character |
| `villain-design.md` | design-character |
| `relationship-network.md` | design-character |
| `cool-factor-guide.md` | design-character |

**工具权限**：Read, Glob, Grep, Write, Edit

---

### 4. Consistency Checker（一致性检查员）

**核心职责**：**只读**事实一致性检测——角色属性冲突、时间线矛盾、伏笔断线、世界规则违反。不做任何创作判断。

**被谁调用**：

| Skill | 调用时机 | 任务 |
|-------|---------|------|
| `daily-write` | Phase 5 质量检查（可选） | 事实一致性扫描 |
| `review` | 审查 | 事实一致性扫描 |

**参考文件来源**：

| 参考文件 | 来源 skill |
|---|---|
| `quality-checklist.md` | daily-write |
| `state-tracking.md` | daily-write |

**工具权限**：只读 — Read, Glob, Grep（prompt 中明确禁止 Write/Edit）

**检查方法**：grep-first + 推理型一致性审查
1. 发现项目关键术语（角色名、设定词、伏笔关键词）
2. 基于术语执行冲突扫描（实体冲突、设定冲突、时间线冲突）
3. 推理型审查（规则边界悖论、代价一致性、跨章因果链）

---

## Review Skill 设计

### 触发方式

```
/review、/审查、「审查一下」「帮我审一下」「check quality」
```

### 审查模式

| 模式 | 行为 | 说明 |
|------|------|------|
| `full` | spawn 全部 4 个 agent | 默认模式，全方位审查 |
| `lean` | spawn story-architect + consistency-checker | 只查结构 + 事实 |
| `solo` | 不 spawn agent，主线程直接查 | 降级模式 or 轻量审查 |

未指定时默认 `full`。

### 审查流程

```
Phase 0：预检与降级
  ├── 检查 .agents/agents/ 下 4 个 agent 定义是否存在
  ├── 确定实际执行模式（full/lean/solo）
  └── 识别目标平台 → 加载对应 rubric（fanqie/qidian/zhihu/generic）

Phase 1：收集待审查内容
  ├── 确定审查范围（用户指定 or 最近修改的正文文件）
  ├── 读取支撑材料（正文/设定/大纲/追踪文件）
  └── 运行确定性预检脚本（check-ai-patterns.js / check-degeneration.js）

Phase 2：并行 Spawn Agent（full/lean 模式）
  ├── Agent 1: story-architect      → 结构/节奏/钩子视角
  ├── Agent 2: character-designer   → 角色/对话/关系视角（仅 full）
  ├── Agent 3: narrative-writer     → 文字质量/AI味视角（仅 full）
  └── Agent 4: consistency-checker  → 事实一致性/伏笔视角

Phase 3：综合裁决
  ├── 合并去重所有 FINDINGS（按 S1→S4 排序）
  ├── 呈现分歧（agent 间有冲突意见时，让用户裁决）
  └── 输出综合审查报告
```

### 报告格式

```markdown
=== 故事审查报告 ===
Requested Mode: full | lean | solo
Effective Mode: full | lean | solo
Fallback: none | agent unavailable -> solo | spawn failed -> solo
审查范围: {文件列表}

## 结论汇总
- story-architect:      APPROVE / CONCERNS(n) / REJECT / NOT_RUN
- character-designer:   APPROVE / CONCERNS(n) / REJECT / NOT_RUN
- narrative-writer:     APPROVE / CONCERNS(n) / REJECT / NOT_RUN
- consistency-checker:  APPROVE / CONCERNS(n) / REJECT / NOT_RUN

## 严重度统计
- S1: n
- S2: n
- S3: n
- S4: n

## 综合评定
APPROVE / CONCERNS / REJECT

## 发现的问题
（按统一 Findings Schema 列出，S1→S4 排序）

## Agent 分歧（如有）

## 修改建议（按优先级排列）
```

### Review Skill 自有 References

| 文件 | 用途 |
|------|------|
| `references/quality-rubric.md` | 通用评分标准（S1-S4 定义、14 项审查维度） |
| `references/rubrics/fanqie.md` | 番茄小说平台标准 |
| `references/rubrics/qidian.md` | 起点中文网平台标准 |
| `references/rubrics/zhihu.md` | 知乎盐言平台标准 |

### 降级逻辑

```
4 个 agent 定义都存在 → full
缺 narrative-writer 或 character-designer → lean（如果请求 full）
缺 story-architect 或 consistency-checker → solo
任何 agent spawn 失败 → solo
```

---

## 现有 Skill 集成

### 各 Skill 的 Agent 集成点

#### 1. `design-outline` — 新增 story-architect 调用

在 Phase 3（大纲搭建）末尾新增段落：

```markdown
#### Agent 调用：story-architect

如果项目已部署 story-architect agent（检查 `.agents/agents/story-architect.md` 是否存在），
读取该文件内容，拼接以下参数后 spawn Agent：

- 项目根目录：{当前项目绝对路径}
- 任务类型：创作
- 查询参数：辅助大纲排布、钩子/反转设计、情绪弧线设计
- 相关文件路径：settings/outline.yaml, settings/pacing.yaml

如 agent 不可用，由主线程直接完成。
```

#### 2. `design-character` — 新增 character-designer 调用

在交互式设计阶段新增段落：

```markdown
#### Agent 调用：character-designer

如果项目已部署 character-designer agent（检查 `.agents/agents/character-designer.md` 是否存在），
读取该文件内容，拼接以下参数后 spawn Agent：

- 项目根目录：{当前项目绝对路径}
- 任务类型：创作
- 查询参数：辅助角色深度设计（三层标签、九维深化、语言风格档案）
- 相关文件路径：settings/characters.yaml

如 agent 不可用，由主线程直接完成。
```

#### 3. `daily-write` — 新增 narrative-writer + consistency-checker 调用

Phase 4（正文写作）新增：

```markdown
#### Agent 调用：narrative-writer

如果项目已部署 narrative-writer agent（检查 `.agents/agents/narrative-writer.md` 是否存在），
读取该文件内容，拼接以下参数后 spawn Agent：

- 项目根目录：{当前项目绝对路径}
- 任务类型：创作
- 查询参数：执行正文写作（章节 {N}）
- 相关文件路径：content/chapter_{N}.md, 相关 references

如 agent 不可用，由主线程直接写作。
```

Phase 5（质量检查）新增：

```markdown
#### Agent 调用：consistency-checker

如果项目已部署 consistency-checker agent（检查 `.agents/agents/consistency-checker.md` 是否存在），
读取该文件内容，拼接以下参数后 spawn Agent：

- 项目根目录：{当前项目绝对路径}
- 任务类型：审查
- 检查范围：{本次写作的章节}
- 已知角色：{从 settings/characters.yaml 提取角色名列表}

如 agent 不可用，由主线程直接检查。
```

#### 4. `golden-chapters` — 新增 narrative-writer 调用

Phase 3（正文生成）新增：

```markdown
#### Agent 调用：narrative-writer

如果项目已部署 narrative-writer agent（检查 `.agents/agents/narrative-writer.md` 是否存在），
读取该文件内容，拼接以下参数后 spawn Agent：

- 项目根目录：{当前项目绝对路径}
- 任务类型：创作
- 查询参数：执行黄金三章正文写作
- 相关文件路径：content/chapter_001.md, chapter_002.md, chapter_003.md

如 agent 不可用，由主线程直接写作。
```

### 改动量评估

每个 skill 的 SKILL.md 只需在对应 Phase 末尾新增一段 "Agent 调用" 说明（约 10-15 行），不改变现有 Phase 流程和退出条件。改动是增量式的。

---

## 统一降级策略

所有 agent 调用遵循同一套降级规则：

```
┌─ .agents/agents/{agent}.md 存在？
│   ├── 否 → solo（主线程直接做），不报错
│   └── 是 → Read 文件 → 组装 prompt → Agent spawn
│              ├── 成功 → 使用 agent 输出
│              └── 失败 → solo，在输出中标注 Fallback
│
└─ 当前已在 subagent 内？
    └── 是 → 不嵌套 spawn，直接 solo
```

降级时的行为：
- 不报错、不中断流程
- 在输出/报告中标注 `Fallback: agent unavailable -> solo`
- 主线程用对应 skill 的 references 直接完成任务

---

## AGENTS.md 补充

在项目 `.agents/AGENTS.md` 中新增 Agent 使用说明段落：

```markdown
## Agent 协作

本项目部署了 4 个专业 Agent（定义在 .agents/agents/）：

| Agent | 职责 | 权限 |
|-------|------|------|
| story-architect | 故事架构师：题材/世界观/大纲/反转/情绪弧线 | Read+Write+Edit |
| narrative-writer | 叙事写手：正文写作/去AI味/格式合规 | Read+Write+Edit |
| character-designer | 角色设计师：角色设定/对话风格/人物弧线 | Read+Write+Edit |
| consistency-checker | 一致性检查员：事实冲突/伏笔断线/时间线检测 | 只读 |

各 Skill 在关键步骤会自动 spawn 对应 Agent。Agent 不可用时自动降级为 solo 模式。
独立审查请使用 /review 命令。
```

---

## 交付清单

| 交付物 | 数量 | 说明 |
|--------|------|------|
| Agent 定义文件 | 4 个 | `.agents/agents/{name}.md` |
| 新 review skill | 1 个 | SKILL.md + 4 个 rubric references |
| 现有 skill 微调 | 4 个 | design-outline, design-character, daily-write, golden-chapters |
| AGENTS.md 补充 | 1 处 | 新增 Agent 使用说明段落 |

**总计**：新建 8 个文件（4 agent + 1 SKILL.md + 3 rubric references + 1 quality-rubric），修改 5 个文件（4 skill + AGENTS.md）

---

## 不在范围内

- Hooks（session-start, pre-write guard 等）— 后续迭代
- Model 分级（opus/sonnet/haiku）— 当前单模型
- story-setup 部署器 — 当前项目不需要跨 CLI 部署
- 多端兼容（OpenCode / Codex）— 仅 ZCode
- 路由入口 skill — 保持现有 skill 直接调用方式
- story-explorer / story-researcher / chapter-extractor agent — 非核心，后续按需添加
