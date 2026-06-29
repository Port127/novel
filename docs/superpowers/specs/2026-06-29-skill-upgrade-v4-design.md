# SKILL 体系重构升级设计 (V4)

> 日期：2026-06-29
> 前置设计：[2026-06-25-skill-system-redesign.md](./2026-06-25-skill-system-redesign.md)（V3）

---

## 1. 背景与动机

### 1.1 现状问题

V3 设计的 9 个写作 skill 每个都是单一 `SKILL.md` 文件，存在以下系统性缺陷：

| 缺陷 | 表现 |
|------|------|
| **无领域知识沉淀** | 写作方法论、品类公式、平台画像全靠 LLM 临场发挥，每次调用从零开始 |
| **无确定性验证** | 质量门禁依赖 Python 引擎的关键词匹配或 LLM 自查，不可靠 |
| **无断点恢复** | 长任务中断（崩溃、超时、上下文耗尽）必须从头来 |
| **无 Phase 化流程** | 工作流线性执行，无法跳过已完成步骤或从中间恢复 |
| **Python 引擎过重** | 11 个 skill 模块 + 5 个 workflow 组件承担了本该由 skill 自包含的逻辑 |

### 1.2 参考标杆

`oh-story-claudecode` 项目（`other/oh-story-claudecode/`）提供了成熟的参照：

- 每个 skill 自包含：`SKILL.md` + `references/` + `scripts/`
- 核心 skill（story-long-write）有 **36 个 reference 文件** + **3 个 JS 验证脚本**
- 确定性脚本做质量验证（`check-ai-patterns.js`、`check-degeneration.js`、`normalize-punctuation.js`）
- Phase 化流程 + `_progress.md` 断点恢复
- References 按需加载，不一次全读

### 1.3 我们的差异化优势

与 oh-story-claudecode 的关键区别：我们有一套 Python 引擎层（`src/novel/core/skills/`），包含评分逻辑、LLM 调用、向量记忆等能力。重构后这些能力不删除，但 skill 不再依赖它们做质量门禁。

---

## 2. 架构决策

| 决策项 | 选择 | 理由 |
|--------|------|------|
| 架构模式 | **方案 B：逐 skill 独立自包含** | 每个 skill 独立持有 references/ 和 scripts/，无外部共享依赖 |
| 知识来源 | **复用改写** | 以 oh-story-claudecode 的 references 为基础，根据我们的品类和特点改写 |
| 脚本语言 | **JS** | 与 oh-story-claudecode 一致，可直接复用其脚本 |
| Python 引擎定位 | **退化为基础设施** | 只做 LLM 调用和文件 IO，skill 不再依赖引擎做质量门禁 |
| 重构范围 | **9 个写作 skill 全量** | scout-topic → worldbuilding → design-character → design-outline → design-chapters → golden-chapters → paywall-design → daily-write → data-diagnosis |

---

## 3. 通用 Skill 结构

所有 9 个 skill 遵循统一的目录结构和 SKILL.md 模板。

### 3.1 目录结构

```
.agents/skills/<skill-name>/
├── SKILL.md              ← 主文件：Phase 化流程 + 质量门禁定义
├── references/           ← 本 skill 专用的领域知识文件（按需加载）
│   ├── <topic-a>.md
│   ├── <topic-b>.md
│   └── ...
└── scripts/              ← 本 skill 专用的 JS 验证脚本
    ├── check-xxx.js
    └── ...
```

### 3.2 SKILL.md 统一结构

```markdown
---
name: <skill-name>
description: <一句话描述>
---

# <Skill 名称>

> <概述：做什么、何时使用、前置条件>

## 核心原则（3-4 条）

## Phase 定义
### Phase 1: <名称>
- **入口条件**：<前置文件或状态>
- **步骤**：<具体操作>
- **出口条件**：<本 Phase 完成的标志>
- **加载 References**：<本 Phase 需要的 reference 文件>

### Phase 2: <名称>
...

## 质量门禁
| Gate | 类型 | 检查内容 | 通过标准 |
|------|------|----------|----------|
| A    | JS 脚本 | <脚本名> | blocking 项归零 |
| B    | LLM 评估 | <评估维度> | 评分 ≥ 60 |

## 断点恢复
- 状态文件：`_progress.md`
- 记录：当前 Phase、已完成步骤、关键状态
- 恢复逻辑：读取 _progress.md，跳到最后一个已完成 Phase 的下一步

## 输出文件清单

## References 索引
| Phase | References | 用途 |
|-------|-----------|------|
| 1     | <file>    | <用途> |
```

### 3.3 关键机制

| 机制 | 说明 |
|------|------|
| **Phase 化流程** | 每个 Phase 有明确入口/出口条件，可独立执行和恢复 |
| **确定性脚本门禁** | 关键质量检查用 JS 脚本（blocking/advisory 两级），不靠 LLM 自查 |
| **断点恢复** | `_progress.md` 记录进度，崩溃后从断点续跑 |
| **References 按需加载** | 不一次全读，按 Phase 映射表加载对应文件 |
| **blocking vs advisory** | 脚本输出分两级：blocking 必须修到 0，advisory 是建议 |

---

## 4. 各 Skill 重构方案

### 4.1 scout-topic（选题侦察）

**现状**：纯交互式对话，无方法论沉淀，无平台差异化分析，无竞品数据采集。

**重构后结构**：

```
scout-topic/
├── SKILL.md
├── references/
│   ├── genre-catalog.md       ← 品类总览（10+ 网文品类公式）
│   ├── platform-profiles.md   ← 各平台读者画像、调性差异
│   ├── topic-decision.md      ← 选题决策方法论（数据→可行性→窗口期）
│   └── tag-strategy.md        ← 标签组合策略（竞争度、潜力分、饱和度）
└── scripts/
    └── check-tags.js          ← 验证标签组合是否有冲突/过饱和
```

**Phase 流程**：

| Phase | 内容 | 入口 | 出口 | References |
|-------|------|------|------|------------|
| 1. 品类定位 | 读 genre-catalog.md，确认目标品类 | 项目已创建 | 品类确定 | genre-catalog.md |
| 2. 平台分析 | 读 platform-profiles.md，分析目标平台调性 | 品类确定 | 平台+品类匹配 | platform-profiles.md |
| 3. 选题决策 | 按 topic-decision.md 评估候选题材 | 平台确定 | 选题报告草稿 | topic-decision.md |
| 4. 标签策略 | 按 tag-strategy.md 组合标签 | 选题确定 | 标签方案 | tag-strategy.md |
| 5. 报告定稿 | 运行 check-tags.js，写入 scout_report.yaml | 标签方案完成 | 报告落盘 | — |

**输出文件**：`settings/scout_report.yaml`

**来源**：oh-story-claudecode 的 `story-long-scan/references/` 中的 topic-decision.md、genre-catalog 类文件改写。

---

### 4.2 worldbuilding（世界观设计）

**现状**：纯聊天，无质量门禁，无品类适配框架，无完整性检查。

**重构后结构**：

```
worldbuilding/
├── SKILL.md
├── references/
│   ├── power-system-guide.md   ← 力量体系设计方法论（等级、升级条件、战斗表现）
│   ├── social-structure.md     ← 社会结构设计（势力关系、社会规则、阶层流动）
│   ├── world-rules.md          ← 基础规则设计（世界运行法则、禁忌与限制）
│   └── genre-worldbuilding.md  ← 品类×世界观适配矩阵
└── scripts/
    └── check-completeness.js   ← 验证世界观 YAML 完整性
```

**Phase 流程**：

| Phase | 内容 | 入口 | 出口 | References |
|-------|------|------|------|------------|
| 1. 品类适配 | 读 genre-worldbuilding.md，加载品类框架 | scout_report.yaml 存在 | 框架确定 | genre-worldbuilding.md |
| 2. 力量体系 | 按 power-system-guide.md 设计 | 框架确定 | 力量体系定稿 | power-system-guide.md |
| 3. 社会结构 | 按 social-structure.md 设计 | 力量体系完成 | 势力/规则定稿 | social-structure.md |
| 4. 基础规则 | 按 world-rules.md 设计 | 社会结构完成 | 世界规则定稿 | world-rules.md |
| 5. 落盘验证 | 生成 worldbuilding.yaml，运行 check-completeness.js | 全部完成 | 完整性通过 | — |

**质量门禁**（品类感知，见 Section 10）：
- check-completeness.js：检查 `scout_report.yaml` 声明的 `required_elements.worldbuilding.required` 中的元素是否完整

**输出文件**：`settings/worldbuilding.yaml`（对齐 `data/schemas/worldbuilding.schema.yaml`）

**来源**：oh-story-claudecode 的 `story-long-write/references/` 中世界观相关文件改写。

---

### 4.3 design-character（人设设计）

**现状**：爽感评估靠 Python 引擎简单关键词打分，方法论不透明，无人设设计方法论沉淀。

**重构后结构**：

```
design-character/
├── SKILL.md
├── references/
│   ├── character-basics.md      ← 角色设计基础方法论
│   ├── protagonist-arc.md       ← 主角弧光设计（起点→终点→转折阶段）
│   ├── villain-design.md        ← 反派设计（动机、手段、厌恶度设计）
│   ├── cool-factor-guide.md     ← 爽感维度评估指南（打脸指数/CP感/厌恶度）
│   └── relationship-network.md  ← 关系网络设计方法论
└── scripts/
    └── check-characters.js      ← 验证角色 YAML 完整性
```

**Phase 流程**：

| Phase | 内容 | 入口 | 出口 | References |
|-------|------|------|------|------------|
| 1. 品类校准 | 读 cool-factor-guide.md，了解品类爽感权重 | scout_report.yaml 存在 | 评估框架确定 | cool-factor-guide.md |
| 2. 主角设计 | 按 protagonist-arc.md 设计 | 框架确定 | 主角定稿 | protagonist-arc.md |
| 3. 反派设计 | 按 villain-design.md 设计 | 主角定稿 | 反派定稿 | villain-design.md |
| 4. 配角群 | 按 character-basics.md 设计配角+关系网 | 反派定稿 | 配角定稿 | character-basics.md, relationship-network.md |
| 5. 爽感评估 | 按 cool-factor-guide.md 六维打分，运行 check-characters.js | 角色全定 | 评分通过+YAML落盘 | cool-factor-guide.md |

**质量门禁**（品类感知，见 Section 10）：
- check-characters.js：检查 `scout_report.yaml` 声明的 `required_elements.characters` 中的角色类型是否完整

**输出文件**：`settings/characters.yaml`（对齐 `data/schemas/characters.schema.yaml`）

**来源**：oh-story-claudecode 的 `story-long-write/references/` 中 character-basics、dialogue-mastery 等改写。

---

### 4.4 design-outline（大纲设计）

**现状**：节奏分析靠 Python 引擎关键词检测，无结构方法论沉淀，无伏笔管理。

**重构后结构**：

```
design-outline/
├── SKILL.md
├── references/
│   ├── outline-structure.md      ← 大纲结构方法论（三幕/序列/节拍 三层嵌套）
│   ├── pacing-guide.md           ← 节奏设计指南（紧张曲线、高潮分布、快慢交替）
│   ├── plot-frameworks.md        ← 经典剧情框架库（升级流/复仇流/系统流/宗门流等）
│   ├── foreshadowing-guide.md    ← 伏笔管理方法论（埋设/呼应/跨卷追踪）
│   └── tension-curve.md          ← 张力曲线设计（每卷/每序列起伏模板）
└── scripts/
    ├── check-outline.js          ← 验证大纲结构完整性（前提≥50字、幕≥3、节拍≥15）
    └── check-pacing.js           ← 检测节奏问题（连续3+慢章、高潮间距过大）
```

**Phase 流程**：

| Phase | 内容 | 入口 | 出口 | References |
|-------|------|------|------|------------|
| 1. 核心前提 | 确定一句话前提+主题+基调 | worldbuilding.yaml 存在 | 前提定稿 | outline-structure.md |
| 2. 结构规划 | 按 outline-structure.md 设计幕→序列→节拍 | 前提定稿 | 骨架完成 | outline-structure.md |
| 3. 剧情填充 | 按 plot-frameworks.md 填充具体事件 | 骨架完成 | 剧情定稿 | plot-frameworks.md |
| 4. 节奏调优 | 按 pacing-guide.md + tension-curve.md 调整 | 剧情定稿 | check-pacing.js 通过 | pacing-guide.md, tension-curve.md |
| 5. 伏笔规划 | 按 foreshadowing-guide.md 设计伏笔网络 | 节奏通过 | 伏笔表定稿 | foreshadowing-guide.md |
| 6. 落盘验证 | 生成 outline.yaml + arcs.yaml + pacing.yaml，运行 check-outline.js | 全部完成 | 完整性通过 | — |

**质量门禁**（品类感知，见 Section 10）：
- check-outline.js：前提 ≥ 50 字、结构按 `required_elements.structure.type` 检查（三幕式则幕≥3，起承转合则arcs≥4）
- check-pacing.js：无连续 3+ 慢章、高潮间距合理

**输出文件**：`settings/outline.yaml`、`settings/arcs.yaml`、`settings/pacing.yaml`

**来源**：oh-story-claudecode 的 `story-long-write/references/` 中 plot-frameworks、hook 方法论改写。

---

### 4.5 design-chapters（细纲设计）

**现状**：章节节拍生成粗糙，无张力值计算方法论，无章节间连贯性检查。

**重构后结构**：

```
design-chapters/
├── SKILL.md
├── references/
│   ├── chapter-beat-guide.md    ← 章节节拍设计方法论（节拍类型、密度标记 密/疏）
│   ├── chapter-template.md      ← 章节摘要模板（五段式概要+多线剧情+出场人物+字数预算）
│   └── tension-design.md        ← 张力值分配方法（基于大纲节奏自动计算+手动微调）
└── scripts/
    └── check-chapters.js        ← 验证细纲质量（节拍3-15、字数2000-5000、张力曲线合理）
```

**Phase 流程**：

| Phase | 内容 | 入口 | 出口 | References |
|-------|------|------|------|------------|
| 1. 参数确认 | 总章数、每章字数目标、转换范围 | outline.yaml 存在 | 参数确定 | — |
| 2. 节拍拆分 | 按 chapter-beat-guide.md 拆章节节拍 | 参数确定 | 节拍表完成 | chapter-beat-guide.md |
| 3. 摘要生成 | 按 chapter-template.md 生成每章摘要 | 节拍表完成 | 摘要完成 | chapter-template.md |
| 4. 张力分配 | 按 tension-design.md 赋张力值 | 摘要完成 | 张力曲线完成 | tension-design.md |
| 5. 预览调优 | 展示前 5-10 章+张力曲线，支持合并/拆分 | 张力完成 | 用户确认 | — |
| 6. 落盘验证 | 生成 chapters_index.yaml，运行 check-chapters.js | 确认完成 | 验证通过 | — |

**质量门禁**：
- check-chapters.js：节拍数 3-15、字数目标 2000-5000、必填字段完整

**输出文件**：`settings/chapters_index.yaml`（对齐 `data/schemas/chapters.schema.yaml`）

---

### 4.6 golden-chapters（黄金三章锻造）

**现状**：品类模板只有简单关键词描述，无微节拍生成机制，验证粗糙。

**重构后结构**：

```
golden-chapters/
├── SKILL.md
├── references/
│   ├── golden-rules.md           ← 黄金三章核心法则（300字内冲突/金手指/首个小高潮）
│   ├── genre-templates.md        ← 品类×黄金三章节拍模板（玄幻/都市/系统/各品类独立模板）
│   ├── micro-beat-guide.md       ← 微节拍设计指南（段级节奏控制）
│   └── anti-ai-writing.md        ← 反 AI 写作指南
└── scripts/
    ├── check-ai-patterns.js      ← AI 模式检测
    ├── check-degeneration.js     ← 退化检测
    └── check-golden-structure.js ← 黄金三章结构专项检查
```

**Phase 流程**：

| Phase | 内容 | 入口 | 出口 | References |
|-------|------|------|------|------------|
| 1. 品类确认 | 读 genre-templates.md，加载品类节拍模板 | characters.yaml + scout_report.yaml 存在 | 模板加载 | genre-templates.md |
| 2. 第一章 | 按 golden-rules.md 写（300字内必须出冲突） | 模板加载 | 第一章初稿 | golden-rules.md, micro-beat-guide.md |
| 3. 第二章 | 按 `required_elements.opening_hook.type` 展示核心优势（金手指/重生优势/相遇等） | 第一章完成 | 第二章初稿 | golden-rules.md |
| 4. 第三章 | 首个小高潮（展示"爽"的潜力） | 第二章完成 | 第三章初稿 | golden-rules.md |
| 5. 结构验证 | 运行 check-golden-structure.js | 三章初稿完成 | blocking 清零 | — |
| 6. 去 AI 味 | 运行 check-ai-patterns.js + check-degeneration.js | 结构通过 | 脚本全部通过 | anti-ai-writing.md |
| 7. 定稿 | 写入 chapter_001~003.md + 评估报告 | 全部通过 | 文件落盘 | — |

**质量门禁**（品类感知，见 Section 10）：
- check-golden-structure.js：按 `required_elements.opening_hook.type` 检查对应的开篇钩子（golden_finger / reborn_advantage / meet_cute / conflict）
- check-ai-patterns.js：blocking 项归零
- check-degeneration.js：blocking 项归零

**输出文件**：`content/chapter_001.md`、`content/chapter_002.md`、`content/chapter_003.md`、`golden_chapters_report.yaml`

**来源**：oh-story-claudecode 的 `story-short-write/references/genre-styles/` 和 `story-long-write/references/` 改写。

---

### 4.7 daily-write（日更写作）

**现状**：3 个质量门禁靠 Python 引擎，无反 AI 领域知识沉淀，无断点恢复，无上下文追踪机制。

**重构后结构**：

```
daily-write/
├── SKILL.md
├── references/
│   ├── writing-flow.md        ← 单章写作 13 步流程
│   ├── anti-ai-writing.md     ← 反 AI 写作指南
│   ├── banned-words.md        ← 违禁词表（分级）
│   ├── hooks-guide.md         ← 钩子方法论（章钩/悬念/段钩）
│   ├── quality-checklist.md   ← 质量检查清单
│   └── state-tracking.md      ← 状态追踪协议
└── scripts/
    ├── check-ai-patterns.js    ← AI 模式检测
    ├── check-degeneration.js   ← 退化检测
    └── normalize-punctuation.js ← 标点规范化
```

**Phase 流程**：

| Phase | 内容 | 入口 | 出口 | References |
|-------|------|------|------|------------|
| 1. 选题确认 | 读 chapters_index.yaml，选目标章节 | 项目存在 | 章节选定 | — |
| 2. 上下文加载 | 前章末 300 字+本章细纲+追踪文件 | 章节选定 | 上下文就绪 | state-tracking.md |
| 3. 写作执行 | 按 writing-flow.md 的 13 步写 | 上下文就绪 | 初稿生成 | writing-flow.md |
| 4. 确定性检查 | 运行 3 个 JS 脚本 | 初稿生成 | blocking 清零 | — |
| 5. LLM 评估 | 反 AI 评分+钩子评分（≥60 通过） | 脚本通过 | 评分通过 | anti-ai-writing.md, banned-words.md, hooks-guide.md, quality-checklist.md |
| 6. 定稿 | 写入 chapter_XXX.md，更新追踪 | 全部通过 | 章节完成 | — |

**断点恢复**：`_progress.md` 记录当前写到第几章、第几步，崩溃后自动续跑。

**质量门禁**：
- check-ai-patterns.js：blocking 项归零
- check-degeneration.js：blocking 项归零
- normalize-punctuation.js：修改文件中的标点问题
- LLM 反 AI 评分 ≥ 60（5 层：词汇/句法/段落/叙事/情感）
- LLM 钩子评分 ≥ 60（悬念强度+冲突密度）

**输出文件**：`content/chapter_XXX.md`

**来源**：oh-story-claudecode 的 `story-long-write/` 整体改写，scripts 直接复用。

---

### 4.8 paywall-design（付费卡点设计）

**现状**：切点分析靠关键词匹配，无付费心理分析框架，无跨平台付费策略差异。

**重构后结构**：

```
paywall-design/
├── SKILL.md
├── references/
│   ├── paywall-psychology.md    ← 付费心理分析（读者决策点、损失厌恶、沉没成本）
│   ├── cut-point-method.md      ← 切点选择方法论（爽点兑现+新悬念双重保险）
│   ├── transition-guide.md      ← 过渡章节设计（免费末章+付费首章节奏）
│   └── platform-paywall.md      ← 各平台付费模式差异（番茄免费/起点千字/晋江VIP）
└── scripts/
    └── check-paywall.js         ← 验证切点合理性（切点章张力>均值、前后悬念密度达标）
```

**Phase 流程**：

| Phase | 内容 | 入口 | 出口 | References |
|-------|------|------|------|------------|
| 1. 大纲分析 | 按 cut-point-method.md 分析张力曲线，标记候选切点 | outline.yaml + chapters_index.yaml 存在 | 候选切点列表 | cut-point-method.md |
| 2. 切点决策 | 按 paywall-psychology.md 评估候选点 | 候选列表 | 切点确定 | paywall-psychology.md |
| 3. 过渡设计 | 按 transition-guide.md 设计过渡章 | 切点确定 | 过渡方案定稿 | transition-guide.md |
| 4. 平台适配 | 按 platform-paywall.md 调整 | 过渡方案定稿 | 平台适配完成 | platform-paywall.md |
| 5. 落盘验证 | 生成 paywall_report.yaml，运行 check-paywall.js | 全部完成 | 验证通过 | — |

**质量门禁**：
- check-paywall.js：切点章张力值 > 全章均值、前后章悬念密度达标

**输出文件**：`paywall_report.yaml`

---

### 4.9 data-diagnosis（数据诊断）

**现状**：只有 CSV 导入+简单阈值检测，无诊断方法论，无跨章节趋势分析。

**重构后结构**：

```
data-diagnosis/
├── SKILL.md
├── references/
│   ├── metrics-guide.md           ← 指标体系（读完率/互动率/追读率/打赏率）
│   ├── diagnosis-method.md        ← 诊断方法论（异常→章节定位→原因→建议）
│   ├── chapter-problem-patterns.md ← 章节问题模式库（数据特征映射）
│   └── report-template.md         ← 诊断报告模板
└── scripts/
    └── analyze-metrics.js         ← CSV 指标计算+异常标记+趋势数据
```

**Phase 流程**：

| Phase | 内容 | 入口 | 出口 | References |
|-------|------|------|------|------------|
| 1. 数据导入 | 读取平台 CSV 数据 | CSV 文件存在 | 数据解析完成 | — |
| 2. 指标计算 | 运行 analyze-metrics.js | 数据解析完成 | 指标就绪 | — |
| 3. 异常定位 | 按 diagnosis-method.md 定位问题章节 | 指标就绪 | 问题章节列表 | diagnosis-method.md |
| 4. 原因分析 | 按 chapter-problem-patterns.md 匹配模式 | 问题章节列表 | 原因报告 | chapter-problem-patterns.md |
| 5. 报告输出 | 按 report-template.md 生成报告 | 分析完成 | 报告落盘 | report-template.md, metrics-guide.md |

**输出文件**：`data_diagnosis_report.yaml`

---

## 5. 汇总统计

### 5.1 References 数量

| Skill | References 数 | 关键文件 |
|-------|:---:|------|
| scout-topic | 4 | genre-catalog, platform-profiles, topic-decision, tag-strategy |
| worldbuilding | 4 | power-system-guide, social-structure, world-rules, genre-worldbuilding |
| design-character | 5 | character-basics, protagonist-arc, villain-design, cool-factor-guide, relationship-network |
| design-outline | 5 | outline-structure, pacing-guide, plot-frameworks, foreshadowing-guide, tension-curve |
| design-chapters | 3 | chapter-beat-guide, chapter-template, tension-design |
| golden-chapters | 4 | golden-rules, genre-templates, micro-beat-guide, anti-ai-writing |
| daily-write | 6 | writing-flow, anti-ai-writing, banned-words, hooks-guide, quality-checklist, state-tracking |
| paywall-design | 4 | paywall-psychology, cut-point-method, transition-guide, platform-paywall |
| data-diagnosis | 4 | metrics-guide, diagnosis-method, chapter-problem-patterns, report-template |
| **合计** | **39** | |

### 5.2 Scripts 数量

| Skill | Scripts 数 | 文件 |
|-------|:---:|------|
| scout-topic | 1 | check-tags.js |
| worldbuilding | 1 | check-completeness.js |
| design-character | 1 | check-characters.js |
| design-outline | 2 | check-outline.js, check-pacing.js |
| design-chapters | 1 | check-chapters.js |
| golden-chapters | 3 | check-ai-patterns.js, check-degeneration.js, check-golden-structure.js |
| daily-write | 3 | check-ai-patterns.js, check-degeneration.js, normalize-punctuation.js |
| paywall-design | 1 | check-paywall.js |
| data-diagnosis | 1 | analyze-metrics.js |
| **合计** | **14** | |

> 注：check-ai-patterns.js、check-degeneration.js、normalize-punctuation.js 在 golden-chapters 和 daily-write 中各持有一份独立副本（方案 B 自包含原则）。

### 5.3 Python 引擎退化映射

| Python 模块 | 原用途 | 重构后替代方案 |
|------------|--------|--------------|
| `anti_ai_polish.py` | 5层AI检测评分 | 迁移到 daily-write/golden-chapters 的 references/anti-ai-writing.md + scripts/check-ai-patterns.js |
| `audit_hooks.py` | 钩子审计 | 迁移到 daily-write 的 references/hooks-guide.md + LLM 评估 |
| `check_logic.py` | 事实核查 | 迁移到 daily-write 的 references/state-tracking.md + LLM 评估 |
| `forge_golden_chapters.py` | 黄金三章验证 | 迁移到 golden-chapters 的 scripts/check-golden-structure.js |
| `ask_architect.py` | 节奏分析 | 迁移到 design-outline 的 scripts/check-pacing.js + references/pacing-guide.md |
| `design_character.py` | 爽感评分 | 迁移到 design-character 的 references/cool-factor-guide.md + LLM 评估 |
| `design_paywall.py` | 付费卡点分析 | 迁移到 paywall-design 的 references/cut-point-method.md + scripts/check-paywall.js |
| `flesh_out_chapter.py` | 细纲验证 | 迁移到 design-chapters 的 scripts/check-chapters.js |
| `scout_topic.py` | 选题分析 | 迁移到 scout-topic 的 references/topic-decision.md + scripts/check-tags.js |
| `analyze_stats.py` | 数据分析 | 迁移到 data-diagnosis 的 scripts/analyze-metrics.js + references/diagnosis-method.md |

Python 引擎代码**不删除**，保留为备用基础设施。Skill 层面不再依赖它做质量门禁。

---

## 6. 实施约束

### 6.1 不改动的 Skill

以下 skill 不在本次重构范围：
- `nm` — 素材检索工具
- `export-novel` — 导出工具
- `stock-check` — 存稿看板
- `code-review-change` — 代码审查
- `commit-msg` — 提交信息
- `feature-planning` — 功能规划
- `refactor-planning` — 重构规划

### 6.2 Reference 文件编写原则

1. **从 oh-story-claudecode 复用改写**，不从零编写
2. **按 Phase 组织**，每个文件服务于特定 Phase
3. **按需加载**，不要求一次全部读入
4. **自包含**，每个 skill 持有自己的副本（方案 B）
5. **中文编写**，代码标识符用英文

### 6.3 Script 编写原则

1. **JS 编写**，Node.js 可直接运行
2. **blocking/advisory 两级**，blocking 必须修到 0
3. **检测脚本只报告不修改**（check-* 系列），修改脚本才改文件（normalize-*）
4. **跳过 YAML frontmatter 和代码块**
5. **退出码**：0=通过，1=有问题，2=脚本错误
6. **3 个通用脚本**（check-ai-patterns.js、check-degeneration.js、normalize-punctuation.js）从 oh-story-claudecode 直接复用，按需微调

### 6.4 断点恢复协议

每个 Phase 化 skill 的 `_progress.md` 格式：

```markdown
# Progress

- **current_phase**: <当前 Phase 编号>
- **current_step**: <当前步骤>
- **status**: in_progress | completed | paused
- **last_updated**: <时间戳>

## Phase Status
- [x] Phase 1: <名称> — completed
- [ ] Phase 2: <名称> — in_progress
- [ ] Phase 3: <名称> — pending
```

恢复逻辑：启动时检查 `_progress.md`，若存在且 status != completed，跳到最后一个 in_progress 的 Phase 继续执行。

---

## 7. Novel-level References（小说专属知识）

每本小说项目已有自己的专属 reference 文件，存放该小说的结构化世界数据。这些与 skill 自带的通用 references 是两个层次。

### 7.1 两层 References 的区别

| 层次 | 位置 | 格式 | 内容 | 性质 |
|------|------|------|------|------|
| **Skill references** | `.agents/skills/<skill>/references/` | Markdown | 通用方法论（"怎么写好钩子"、"反 AI 写作指南"） | 所有小说共享，很少变 |
| **Novel references** | `novels/<book>/references/` | YAML | 这本小说的专属世界数据（力量体系、时代背景、地点、副本、参考小说分析） | 仅本小说使用，随剧情演进 |

### 7.2 现有结构（已验证，仅供参考）

以 `nv_20260625_00t3`（都市文娱小说）为例：

```
novels/nv_20260625_00t3/references/
├── songs_timeline.yaml           ← 639行：歌曲发布时间线+入梦窗口期
├── 2009_era_details.yaml         ← 728行：2009年时代细节
├── business/
│   └── internet_2009_2015.yaml   ← 213行：互联网创业机会
├── locations/
│   ├── hfut_campus.yaml          ← 548行：合工大校园场景地图
│   └── hefei_universities.yaml   ← 183行：合肥高校信息
├── dungeons/
│   └── 001_庐州月.yaml           ← 132行：第一个副本完整设计
└── novels/
    └── _index.yaml               ← 69行：参考小说分析索引
```

**这是特定小说的特定结构，不是通用模板。** 不同品类的小说会有完全不同的目录结构。

### 7.3 目录结构规范

**不预设固定子目录。** 每个小说项目按自己的需求创建结构。

唯一约定：顶层 `_index.yaml` 必须存在，负责发现"有什么"。

```
novels/<book>/references/
├── _index.yaml              ← 必须：顶层索引
├── <任意子目录或文件>        ← 按小说需求自由组织
└── ...
```

不同品类的可能结构：

| 品类 | 可能的子目录示例 |
|------|-----------------|
| 都市重生 | era_details/、business/、songs/、locations/ |
| 玄幻修仙 | power_system/、sects/、realms/、artifacts/ |
| 系统文 | system_rules/、quests/、rewards/ |
| 言情 | relationships/、events/、emotional_arc/ |

### 7.4 格式约定

**不强制统一格式，按内容性质选择：**

| 内容性质 | 格式 | 示例 |
|---------|------|------|
| 结构化数据（时间线、属性、关系、清单） | YAML | songs_timeline.yaml、locations/*.yaml |
| 散文/笔记/指南（创作笔记、角色声音样本） | Markdown | creative_notes.md、voice_samples.md |
| 索引文件 | YAML（固定） | _index.yaml |

### 7.5 拆分策略

单文件超过 300 行时考虑拆分，原则：

- **按时间/章节拆**：如 `songs_2009.yaml`、`songs_2010.yaml`
- **按子领域拆**：如 `campus_buildings.yaml`、`campus_surroundings.yaml`
- **不按格式拆**：不要一个 YAML 一个 MD 说同一件事

### 7.4 优先级规则

**Novel references > Skill references**。

理由：novel references 是"这本的现实数据"，skill references 是"通用方法论"。当两者冲突时，现实覆盖方法论。例如：
- Skill reference 说"力量体系建议 5-9 级"
- Novel reference 的 YAML 说"本作力量体系 = 3 级"
- → 以 novel reference 为准

### 7.5 上下文管理策略

Novel references 文件较大（100-700+ 行），全部加载会导致上下文爆炸。策略：

1. **索引先行**：顶层 `_index.yaml` 记录每个文件/子目录的名称+一句话摘要+行数。Skill 启动时只读索引（约 30-50 行），再按需决定是否读具体文件。

2. **按需加载**：Skill 的 Phase 映射表标注"本 Phase 可能需要哪些领域的 novel references"，执行时按索引匹配后选择性读取。

3. **大文件分段读取**：超过 200 行的 YAML 文件，按需读取特定 section（如只读 `locations/hfut_campus.yaml` 的 `entrances` 部分），不全部加载。

4. **加载预算**：每个 Phase 最多加载 2 个 novel reference 文件（或同一文件的多个 section），总不超过 500 行。超出则优先加载与当前 Phase 最相关的。

### 7.6 _index.yaml 格式（顶层）

索引文件负责描述"有什么"，不规定"应该有什么"：

```yaml
# 本小说的 references 索引
# 供 skill 启动时快速了解可用数据

novel_id: "nv_20260625_00t3"
novel_title: "重生之文娱大时代"
genre: "urban"
era: "2009-2015"

# 按实际存在的文件/目录列出，不要求固定结构
entries:
  - path: "songs_timeline.yaml"
    format: yaml
    lines: 639
    summary: "歌曲发布时间线+入梦窗口期+用户选定歌曲"
    used_by: ["daily-write", "design-chapters"]

  - path: "2009_era_details.yaml"
    format: yaml
    lines: 728
    summary: "2009年时代细节（社会/科技/文化/网络）"
    used_by: ["daily-write", "worldbuilding"]

  - path: "business/"
    type: directory
    summary: "互联网创业机会+商战素材"
    children:
      - path: "internet_2009_2015.yaml"
        lines: 213
        summary: "2009-2015年互联网创业机会清单"

  - path: "locations/"
    type: directory
    summary: "合肥地理信息（校园/城市）"
    children:
      - path: "hfut_campus.yaml"
        lines: 548
        summary: "合工大屯溪路校区场景地图"
      - path: "hefei_universities.yaml"
        lines: 183
        summary: "合肥高校信息"

  - path: "dungeons/"
    type: directory
    summary: "入梦副本设计（按歌曲主题）"
    children:
      - path: "001_庐州月.yaml"
        lines: 132
        summary: "第一个副本：庐州月（古风/爱情）"

  - path: "novels/"
    type: directory
    summary: "参考小说分析"
    index_file: "novels/_index.yaml"
```

索引的维护：
- 新增 reference 文件时，同步更新 `_index.yaml`
- skill 启动时只读 `_index.yaml`（约 50-100 行），不扫描目录
- `used_by` 字段可选，用于 skill 快速判断哪些文件与自己相关

### 7.7 Skill 如何消费 Novel References

在 skill 的 Phase 映射表中增加一列"Novel References"：

| Phase | 内容 | Skill References | Novel References |
|-------|------|-----------------|-----------------|
| 2. 上下文加载 | 加载背景数据 | state-tracking.md | `_index.yaml` → 按需读取相关领域 |
| 3. 写作执行 | 写具体场景 | writing-flow.md | `_index.yaml` → 按场景类型匹配 |

匹配逻辑（不硬编码子目录名）：
1. 读 `novels/<book>/references/_index.yaml`
2. 根据当前场景类型（如"校园"、"商战"、"感情戏"），匹配 summary 中包含相关关键词的 entry
3. 读取对应文件（或 section）
4. 将数据作为上下文注入写作

---

## 8. Novel-Material (nm) 集成

`nm` 是素材检索工具，用于搜索参考小说、大纲、人设、章节等外部素材。在重构后的架构中，nm 作为各 skill 的**按需参考能力**集成，但不过度依赖。

### 8.1 定位：辅助参考，不做支柱

nm 目前还在成长期，素材库质量参差不齐。**只做参考，不做决策依据**。skill 可以在需要外部素材时调用 nm，但不应将 nm 返回的结果作为质量门禁的判定条件。

### 8.2 使用优先级

按实用性排序：

| 优先级 | 场景 | 说明 |
|:---:|------|------|
| **★★★** | **正文创作**（daily-write） | 写到特定场景时（战斗、美食、医术、感情戏），搜索同类场景的参考正文。**最高价值** |
| **★★** | **结构设计**（design-outline, design-chapters） | 参考标杆作品的爽点节奏、大纲结构、细纲密度 |
| **★★** | **黄金三章**（golden-chapters） | 参考标杆作品的开篇节奏和冲突设计 |
| **★** | **人设设计**（design-character） | 参考类似人设的标杆角色 |
| **★** | **世界观**（worldbuilding） | 参考同类型小说的力量体系设定 |
| **✗** | **选题**（scout-topic） | **不使用**。素材库良莠不齐，选题应基于平台数据和品类分析，不基于素材库 |

### 8.3 集成方式

在各 skill 的 Phase 中增加**可选步骤**（非强制），标注为：

```markdown
- **可选：素材参考**：如需外部参考，调用 `/nm` 搜索 <具体搜索目标>。
  返回结果仅作参考，不纳入质量判定。
```

具体集成点：

| Skill | 在哪个 Phase 集成 | 搜索什么 |
|-------|------------------|----------|
| daily-write | Phase 3（写作执行） | 当前场景类型的参考正文片段 |
| golden-chapters | Phase 2-4（写各章时） | 同品类标杆作品的对应章节 |
| design-outline | Phase 3（剧情填充） | 同剧情框架的标杆大纲结构 |
| design-chapters | Phase 2（节拍拆分） | 标杆作品的章节密度和节奏 |
| design-character | Phase 2-3（主角/反派设计） | 类似人设的标杆角色 |
| worldbuilding | Phase 2（力量体系） | 同类型小说的力量体系参考 |

**不集成的 skill**：scout-topic、paywall-design、data-diagnosis

### 8.4 使用约束

1. **不自动调用**：nm 搜索需要用户确认或在 skill 提示下手动触发
2. **结果不缓存**：每次搜索独立，不将 nm 结果持久化到 references/
3. **质量不信任**：nm 返回的素材可能有 AI 味、结构问题，使用时必须经过当前 skill 的质量门禁过滤
4. **不替代方法论**：nm 提供"别人怎么写的"，skill references 提供"应该怎么写"。两者不混淆

---

## 10. 品类感知的质量门禁

不同品类的小说需要不同的元素。质量门禁不能硬编码"必须有力量体系"或"必须有金手指"，而应根据每本小说的品类和声明动态检查。

### 10.1 问题回顾

以下质量门禁存在"特定当通用"的问题：

| Skill | 硬编码假设 | 不适用于 |
|-------|-----------|---------|
| worldbuilding | `力量体系有名称/等级/规则` | 都市言情、日常系 |
| design-character | `反派 ≥ 1` | 治愈系、无明确对手的故事 |
| design-outline | `幕 ≥ 3`（三幕式） | 起承转合、英雄之旅等其他结构 |
| golden-chapters | `金手指展示` | 纯文学、言情（没有"金手指"概念） |

### 10.2 解决方案：分层配置

**三层结构**：

| 层 | 位置 | 内容 | 谁维护 |
|----|------|------|--------|
| **品类模板** | skill references（如 `genre-worldbuilding.md`） | "玄幻通常需要力量体系" 等建议 | skill 设计时编写 |
| **小说声明** | `settings/scout_report.yaml` 的 `required_elements` | "这本需要 era_details、locations，不需要 power_system" | scout-topic skill 引导用户填写 |
| **实际数据** | `novels/<book>/references/` + `settings/*.yaml` | 具体的力量体系设计、角色设计等 | 各 skill 执行时生成 |

### 10.3 scout_report.yaml 新增 `required_elements`

每本小说在选题阶段声明"这本需要什么元素"：

```yaml
# settings/scout_report.yaml
genre: "urban"
platform: "fanqie"
target_audience: "18-30岁男性，喜欢重生逆袭"
tags: ["都市重生", "文娱", "2009年代"]

# 新增：这本小说的必要元素声明
required_elements:
  worldbuilding:
    required:
      - era_details        # 时代背景（都市必需）
      - locations          # 地点（必需）
      - social_rules       # 社会规则
    optional:
      - business_opportunities
      - songs_timeline
    # 注意：没有 power_system（这本不是玄幻）
  
  characters:
    protagonist: required
    love_interest: required    # 有言情线
    rival: optional            # 对手可选
    supporting_cast: required
    # 注意：没有 villain（不是复仇文）
  
  opening_hook:
    type: "reborn_advantage"   # 重生优势（都市重生特有）
    description: "前世记忆+行业洞察"
    # 注意：不是 golden_finger（不是玄幻/系统文）
  
  structure:
    type: "起承转合"           # 不用三幕式
    target_arcs: 4
    beats_per_arc: [8, 12, 12, 8]  # 起8章、承12章、转12章、合8章
```

### 10.4 Skill References 提供品类模板

各 skill 的 references 提供"品类×元素"建议矩阵，供 scout-topic 引导用户填写 `required_elements` 时参考：

**genre-worldbuilding.md 示例**：

```markdown
## 品类×世界观元素矩阵

### 玄幻修仙
必需：power_system, factions, locations
建议：artifacts, lore, realms

### 都市言情
必需：era_details, locations, social_rules
建议：career_background, relationship_context

### 系统文
必需：system_rules, quest_mechanics, reward_system
建议：power_system, factions

### 重生都市
必需：era_details, business_opportunities, locations
建议：songs_timeline（文娱方向）, future_knowledge

### 悬疑推理
必需：crime_rules, investigation_procedures, suspect_pool
建议：forensic_details, legal_system
```

**genre-character-archetypes.md 示例**：

```markdown
## 品类×角色类型矩阵

### 玄幻爽文
必需：protagonist, mentor, villain, face_slap_targets
建议：love_interest, rival, comic_relief

### 都市言情
必需：protagonist, love_interest, supporting_cast
建议：rival（情敌）, family_members, career_mentor

### 复仇文
必需：protagonist, antagonist, allies
建议：informant, betrayer, final_boss

### 日常治愈
必需：protagonist, supporting_cast
建议：pets, neighbors, childhood_friends
# 注意：没有 villain，冲突来自生活而非对手
```

### 10.5 Quality Gates 脚本动态检查

质量门禁脚本读取 `scout_report.yaml` 的 `required_elements`，动态决定检查什么：

**check-completeness.js 伪代码**：

```javascript
// 读取小说声明
const scoutReport = loadYaml('settings/scout_report.yaml');
const required = scoutReport.required_elements || {};

// 检查 worldbuilding
const worldbuilding = loadYaml('settings/worldbuilding.yaml');
const requiredWorld = required.worldbuilding?.required || [];

for (const elem of requiredWorld) {
  if (!worldbuilding[elem] || isEmpty(worldbuilding[elem])) {
    report.blocking(`缺少必需的世界观元素: ${elem}`);
  }
}

// 不检查未在 required 中声明的元素
// 例如：如果 required 没声明 power_system，就不检查
```

**check-golden-structure.js 伪代码**：

```javascript
// 读取开篇钩子类型
const openingHook = scoutReport.required_elements?.opening_hook;
const hookType = openingHook?.type || 'conflict';  // 默认：300字内冲突

if (hookType === 'golden_finger') {
  // 玄幻/系统文：检查金手指展示
  checkGoldenFingerReveal(chapter2);
} else if (hookType === 'reborn_advantage') {
  // 都市重生：检查重生优势展示
  checkRebornAdvantage(chapter1);
} else if (hookType === 'meet_cute') {
  // 言情：检查相遇/化学反应
  checkMeetCute(chapter1);
} else {
  // 通用：检查首个冲突
  checkFirstConflict(chapter1, withinChars: 300);
}
```

### 10.6 各品类的默认建议

如果 `scout_report.yaml` 没有声明 `required_elements`，skill 使用品类默认值：

| 品类 | 默认 worldbuilding 必需 | 默认 characters 必需 | 默认 opening_hook | 默认 structure |
|------|------------------------|---------------------|-------------------|----------------|
| xuanhuan | power_system, factions, locations | protagonist, mentor, villain | golden_finger | 三幕式, 幕≥3 |
| urban | era_details, locations, social_rules | protagonist, supporting_cast | conflict (300字) | 起承转合, arcs≥4 |
| system | system_rules, quest_mechanics | protagonist, system_entity | golden_finger | 三幕式, 幕≥3 |
| romance | locations, relationship_context | protagonist, love_interest | meet_cute | 起承转合, arcs≥3 |
| suspense | crime_rules, investigation_procedures | protagonist, suspect_pool | mystery_hook | 三幕式, 幕≥3 |

### 10.7 对现有 Skill 设计的影响

以下 skill 的质量门禁描述需要更新为品类感知：

| Skill | 原描述 | 更新为 |
|-------|--------|--------|
| worldbuilding | `力量体系有名称/等级/规则、势力 ≥ 3、地点 ≥ 1` | `检查 scout_report.yaml 声明的 required_elements.worldbuilding.required 中的元素是否完整` |
| design-character | `主角需 traits+psychology+arc、反派 ≥ 1、配角 ≥ 3` | `检查 required_elements.characters 中声明的角色类型是否完整` |
| design-outline | `前提 ≥ 50 字、幕 ≥ 3、节拍 ≥ 15` | `前提 ≥ 50 字、结构按 required_elements.structure.type 检查` |
| golden-chapters | `前 300 字有冲突、金手指展示、首个高潮存在` | `按 required_elements.opening_hook.type 检查对应的开篇钩子` |

### 10.8 对 Novel References 消费的影响

Section 7.7 中的 Phase 映射表不再指定具体子目录名：

```markdown
| Phase | 内容 | Skill References | Novel References |
|-------|------|-----------------|-----------------|
| 2. 上下文加载 | 加载背景数据 | state-tracking.md | `_index.yaml` → 按需读取相关领域 |
| 3. 写作执行 | 写具体场景 | writing-flow.md | `_index.yaml` → 按场景类型匹配 |
```

匹配逻辑：
1. 读 `novels/<book>/references/_index.yaml`
2. 根据当前场景类型（如"校园"、"商战"、"感情戏"），匹配 summary 中包含相关关键词的 entry
3. 读取对应文件（或 section）

不硬编码 `locations/` 或 `dungeons/`，让索引驱动匹配。

---

## 11. 风险与缓解

| 风险 | 缓解措施 |
|------|----------|
| Reference 文件内容质量不达标 | 先复用 oh-story-claudecode 的成熟内容，再逐步迭代 |
| JS 脚本无法覆盖所有验证场景 | JS 做确定性检查（正则/计数），LLM 做语义评估，两层互补 |
| 断点恢复状态文件污染 | 每个 skill 完成后清理 `_progress.md`；新任务开始时检测并提示是否续跑 |
| 方案 B 导致重复文件（如 anti-ai-writing.md 出现在多个 skill） | 接受重复换取独立性；后续可通过 git hook 检测内容漂移 |
| Python 引擎废弃后功能回退 | 引擎代码保留不删，skill 可随时回退调用引擎 |
| 品类感知配置缺失 | scout-topic 引导用户填写 `required_elements`；未填写时使用品类默认值（Section 10.6） |
