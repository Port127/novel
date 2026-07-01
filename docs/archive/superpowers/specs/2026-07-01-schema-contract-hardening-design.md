# Schema Contract Hardening Design

## 背景

上一轮 Skill 合约审计已经把当前主流程的路径口径收束到 `.agents/skills/`、`content/chapter_*.md`、`settings/chapters_index.yaml`、`settings/chapter_outlines/chapter_*.md` 和根目录 `paywall_report.yaml`。

审计同时暴露出下一层问题：多个跨 Skill 共享产物仍然缺少足够硬的 schema、模板或脚本约束。当前风险不再主要是“路径写错”，而是“同一份 YAML/Markdown 被不同 Skill 读写时，字段边界和校验责任不够稳定”。

已知缺口集中在：

- `data/schemas/chapters.schema.yaml` 与 `templates/default/settings/chapters_index.yaml` 字段和张力范围不一致。
- `settings/chapter_outlines/chapter_*.md` 只有 Markdown 模板，没有可验证的 frontmatter/schema 合约。
- `settings/notes.yaml` 被 `design-outline` 和 `daily-write` 共同读写，但缺少 dedicated schema。
- `paywall_report.yaml` 被 `paywall-design` 生成、`daily-write` 消费，但缺少 dedicated schema。
- `settings/outline.yaml`、`settings/arcs.yaml`、`settings/pacing.yaml` 的 schema 边界还需要进一步明确。

## 目标

本轮设计目标是进行 **Schema 合约补强**，把主创作链路里跨 Skill 共享的结构化产物推进到“可验证、可维护、可供未来 runner 调用”的状态。

具体目标：

1. 统一 `chapters.schema.yaml` 与默认模板的字段、张力范围和统计结构。
2. 为 `chapter_outlines` 的 frontmatter 设计可验证合约。
3. 为 `notes.yaml` 设计 dedicated schema，支撑上下文追踪、伏笔、角色状态和长篇续写。
4. 为 `paywall_report.yaml` 设计 dedicated schema，支撑卡点策略和下游日更读取。
5. 明确 `outline.yaml`、`arcs.yaml`、`pacing.yaml` 的 schema 边界：是继续由一个 schema 覆盖，还是拆分为多份 schema。
6. 定义 schema 与 JS 门禁脚本的关系，避免只补 schema 但执行仍靠 Agent 口头遵守。

## 非目标

- 不实现统一 Skill Runner。
- 不恢复或改造冻结遗留 Python CLI。
- 不重写所有 Skill 内容。
- 不批量清理历史 `docs/superpowers/plans/` 和 `docs/feedback/archive/`。
- 不把 `other/oh-story-claudecode` 的目录结构直接搬进本项目。
- 不要求正文 Markdown 本身有完整 schema；正文质量仍由 Skill 方法论、确定性脚本和用户判断共同保障。

## 设计原则

### 1. Schema 优先约束跨 Skill 共享产物

只有当一个产物满足任一条件时，本轮才优先补 schema：

- 被一个 Skill 生产、另一个 Skill 消费。
- 被多个 Skill 共同读写。
- 会影响后续章节生成、卡点、导出或审查。
- 现有模板与 schema 已经发生字段漂移。

因此本轮优先级是：

1. `chapters_index.yaml`
2. `chapter_outlines/chapter_*.md` frontmatter
3. `notes.yaml`
4. `paywall_report.yaml`
5. `outline/arcs/pacing` 边界

`golden_chapters_report`、导出配置、`data-diagnosis` 报告和辅助 Skill 产物只记录为后续扩展，除非实施阶段发现它们已经阻塞主链路。

### 2. Schema 与模板必须同源

凡是 `templates/default/settings/*.yaml` 中提供的新项目初始结构，都必须与 `data/schemas/*.schema.yaml` 保持一致。模板不能继续使用旧字段名或旧范围。

本轮要明确：

- 哪个字段名是当前标准。
- 哪些旧字段需要删除、迁移或标注为兼容。
- 张力值、状态值、章节编号和文件名的范围如何表达。
- 模板注释是否足够指导 Agent 生成合规数据。

### 3. Markdown 产物使用 frontmatter 合约

`settings/chapter_outlines/chapter_*.md` 是 Markdown，不需要把全文正文结构 YAML 化。但它的 frontmatter 必须稳定，至少覆盖：

- 章节编号。
- 对应正文文件。
- 状态。
- 目标字数。
- 章节功能。
- 张力值。
- 涉及角色。
- 关联情节点。
- 是否可用于下游写作。

正文部分继续由 `references/chapter-template.md` 约束结构和写法。

### 4. JS 门禁负责可确定检查

Schema 负责字段结构，JS 门禁负责执行时检查。两者边界：

- Schema 检查字段存在、类型、枚举、范围。
- JS 检查跨字段关系、文件存在、章节编号连续、脚本入参、统计合理性。
- 语义质量仍交给 Skill 评估和用户确认。

### 5. 为未来 runner 留接口，但不实现 runner

每个 schema 应能被未来 runner 发现和调用，但本轮只设计约定，不写 runner。

建议约定：

- YAML 产物在 `data/schemas/<artifact>.schema.yaml` 中有 dedicated schema。
- Markdown + frontmatter 产物在 `data/schemas/<artifact>_frontmatter.schema.yaml` 中约束 frontmatter。
- Skill 文档声明“输出文件 → schema → gate script”的映射。

## 方案比较

### 方案 A：只修 `chapters.schema.yaml` 与模板

优点：

- 范围最小。
- 直接修掉当前 P1。
- 不会牵动更多 Skill 文档。

缺点：

- `notes.yaml` 和 `paywall_report.yaml` 仍靠文档纪律。
- `chapter_outlines` 仍然没有可验证入口。
- 未来 runner 仍缺少关键合约。

适用场景：只想快速降低新项目初始化错误。

### 方案 B：主链路 Schema 合约补强

优点：

- 覆盖章节规划、详细细纲、上下文追踪、付费卡点和大纲边界。
- 能把上一轮审计中 P1/P2 的主链路问题一次收束。
- 不引入 runtime，风险可控。
- 为未来 runner 和更严格门禁留出清晰接口。

缺点：

- 会新增或修改多份 schema、模板和 Skill 说明。
- 需要谨慎处理已有字段兼容和脚本校验边界。

这是推荐方案。

### 方案 C：直接设计统一 Skill Runner

优点：

- 最终能强制读取 schema、记录 `_progress.md`、调用脚本、收集门禁结果。
- 可以从执行层减少 Agent 纪律依赖。

缺点：

- 会把本轮从 schema 合约补强扩大为运行框架设计。
- 需要重新定义 Skill 执行模型、错误恢复、用户确认点和日志格式。
- 很容易和当前“人机协同、Skill 驱动”的节奏冲突。

适用场景：schema 合约稳定后，作为下一阶段独立 spec。

## 推荐设计

采用方案 B：主链路 Schema 合约补强。

### 产物一：章节索引 schema/template 对齐

目标文件：

- `data/schemas/chapters.schema.yaml`
- `templates/default/settings/chapters_index.yaml`
- `.agents/skills/design-chapters/scripts/check-chapters.js`
- `.agents/skills/design-chapters/SKILL.md`
- `docs/SKILL_CONTRACT_AUDIT.md`

设计要求：

- 选择一套标准字段，不再让模板和 schema 使用不同命名。
- 保留 `chapter` 或 `number` 之一，不能两者并列作为当前标准。
- 保留 `words_target` 或 `word_count` 之一，明确含义。
- 明确 `tension` 范围是 1-5 还是 1-10，并同步脚本。
- 明确状态枚举：`planned`、`draft`、`written`、`revised`。
- 明确 `file` 字段指向 `content/chapter_XXX.md`。
- 明确如果章节有详细蓝图，索引中如何引用 `settings/chapter_outlines/chapter_XXX.md`。

### 产物二：chapter_outlines frontmatter 合约

目标文件：

- `data/schemas/chapter_outline_frontmatter.schema.yaml`
- `.agents/skills/design-chapters/references/chapter-template.md`
- `.agents/skills/design-chapters/scripts/check-outlines.js`
- `.agents/skills/design-chapters/SKILL.md`

设计要求：

- 只约束 frontmatter，不约束 Markdown 正文全文。
- frontmatter 必须能和 `chapters_index.yaml` 对齐。
- `check-outlines.js` 至少检查：
  - frontmatter 是否存在。
  - 章节编号是否与文件名一致。
  - `content_file` 是否与索引中的 `file` 一致。
  - `status`、`tension`、`target_words` 是否在合法范围。
  - 必要字段缺失时返回 blocking。

### 产物三：notes.yaml schema

目标文件：

- `data/schemas/notes.schema.yaml`
- `templates/default/settings/notes.yaml`
- `.agents/skills/design-outline/SKILL.md`
- `.agents/skills/daily-write/SKILL.md`
- `.agents/skills/daily-write/references/state-tracking.md`

设计要求：

- 支撑 `daily-write` 的三层上下文结构：
  - 近 5 章详记。
  - 十章概要。
  - 卷级总览。
- 支撑角色状态追踪：
  - 角色名。
  - 当前状态。
  - 最近变化章节。
  - 未解决矛盾。
- 支撑伏笔追踪：
  - 伏笔 ID。
  - 埋设章节。
  - 当前状态。
  - 计划回收章节。
- 支撑写作备忘：
  - 用户偏好。
  - 禁用设定。
  - 待确认事项。

### 产物四：paywall_report.yaml schema

目标文件：

- `data/schemas/paywall_report.schema.yaml`
- `.agents/skills/paywall-design/SKILL.md`
- `.agents/skills/paywall-design/scripts/check-paywall.js`
- `.agents/skills/daily-write/SKILL.md`

设计要求：

- 顶级必须包含 `paywall_chapter`。
- 明确候选切点、最终切点、免费末章悬念、付费首章反馈承诺。
- 明确风险项和商业复核结论。
- `daily-write` 能读取该文件并判断目标章节是否处于卡点前后。
- `check-paywall.js` 继续检查张力和悬念密度，同时增加 schema 字段存在性校验。

### 产物五：outline/arcs/pacing 边界决策

目标文件：

- `data/schemas/outline.schema.yaml`
- 可选新增 `data/schemas/arcs.schema.yaml`
- 可选新增 `data/schemas/pacing.schema.yaml`
- `templates/default/settings/arcs.yaml`
- `templates/default/settings/pacing.yaml`
- `.agents/skills/design-outline/SKILL.md`
- `.agents/skills/design-outline/scripts/check-outline.js`
- `.agents/skills/design-outline/scripts/check-pacing.js`

设计要求：

- 如果保持一个 `outline.schema.yaml`，必须在 schema 注释和 Skill 中明确它覆盖哪些文件、哪些字段不覆盖。
- 如果拆分 schema，必须让 `design-outline` 的输出和脚本门禁分别引用对应 schema。
- `pacing.yaml` 的张力范围必须和 `chapters_index.yaml` 一致，避免一个用 1-5、另一个用 1-10。
- `arcs.yaml` 必须能被 `daily-write` 按章节或情节点定位。

## 数据流

推荐后的数据流如下：

```text
design-outline
  -> settings/outline.yaml        -> outline.schema.yaml
  -> settings/arcs.yaml           -> arcs schema 或 outline.schema.yaml 的明确子集
  -> settings/pacing.yaml         -> pacing schema 或 outline.schema.yaml 的明确子集
  -> settings/notes.yaml          -> notes.schema.yaml

design-chapters
  -> settings/chapters_index.yaml -> chapters.schema.yaml
  -> settings/chapter_outlines/   -> chapter_outline_frontmatter.schema.yaml + chapter-template.md

paywall-design
  -> paywall_report.yaml          -> paywall_report.schema.yaml

daily-write
  <- chapters_index.yaml
  <- chapter_outlines/chapter_N.md
  <- notes.yaml
  <- paywall_report.yaml
  -> content/chapter_N.md
  -> updates notes.yaml / chapters_index.yaml
```

## 错误处理

Schema 或脚本发现问题时，按三类处理：

| 类型 | 示例 | 处理 |
|------|------|------|
| blocking | 必填字段缺失、章节编号不连续、张力范围非法、paywall_chapter 不存在 | 阻断当前 Skill，要求修正后重跑门禁 |
| advisory | 缺少推荐字段、字数预算偏离、伏笔回收章节过远 | 展示给用户，由用户决定是否调整 |
| legacy | 历史字段仍存在但当前流程不用 | 不阻断，但在审计文档记录迁移建议 |

## 测试与验证

实施阶段需要采用“基线失败 → 修改 → 验证通过”的闭环。

建议验证：

1. 先构造当前模板与 schema 的不一致案例，证明现有检查不能覆盖。
2. 修改 schema/template 后，运行脚本验证最小样例通过。
3. 构造缺字段、非法张力、章节编号不连续、paywall_chapter 缺失等负例，确认脚本返回 blocking。
4. 使用 `rg` 检查 Skill 文档中 schema 路径和脚本路径均指向真实文件。
5. 不运行 Python 测试作为本轮通过条件，除非实施内容触碰冻结 Python。

## 风险与边界

- 新增 schema 可能暴露现有模板和示例不合规，需要同步更新模板。
- 如果一次拆分 `outline/arcs/pacing` 过细，可能导致实施范围变大；实施计划应允许先做边界说明，再决定是否拆 schema。
- `chapter_outlines` 是 Markdown，过度 schema 化会伤害可读性；本轮只约束 frontmatter。
- `notes.yaml` 是长期演进文件，schema 应保留适度扩展空间。
- `paywall_report.yaml` 需要兼顾商业判断和脚本可检查字段，不能把所有语义判断硬编码进脚本。

## 成功标准

- `chapters.schema.yaml` 与 `templates/default/settings/chapters_index.yaml` 不再字段漂移。
- `chapter_outlines` 有稳定 frontmatter 合约，并被 `check-outlines.js` 检查。
- `notes.yaml` 有 dedicated schema，能支撑 `design-outline` 初始化和 `daily-write` 更新。
- `paywall_report.yaml` 有 dedicated schema，并被 `paywall-design` 和 `daily-write` 明确引用。
- `outline/arcs/pacing` 的 schema 边界在文档和 Skill 中明确，不再让一个 schema 模糊覆盖多个产物。
- `docs/SKILL_CONTRACT_AUDIT.md` 更新为“schema 缺口已进入设计/实施”的状态。
- 没有把统一 Skill Runner 混入本轮实施。
