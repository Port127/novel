# Skill Contract Schema Audit Design

## 背景

本项目已经从 Python CLI 自动流水线转向 Skill 驱动的人机协同创作工作台。当前主入口是 `.agents/skills/`，数据约束来自 `data/schemas/`，流程说明分散在 `README.md`、`.agents/AGENTS.md`、`docs/REQUIREMENTS.md`、`docs/PIPELINE.md` 和各 Skill 的 `SKILL.md` 中。

前期分析发现三类风险：

- 路径口径轻微漂移，例如正文路径在 `content/chapter_*.md` 与 `content/chapters/` 之间不完全一致。
- `settings/chapters_index.yaml` 与 `settings/chapter_outlines/chapter_*.md` 的关系没有在主文档中明确说明。
- Skill 对 schema 的读取、解释、输出和脚本门禁依赖 Agent 执行纪律，缺少一份统一的合约审计结论。

本次设计目标是把“路径、输入、输出、schema、脚本、状态文件”收束为可审计合约，并新增对 `.agents/skills/` 所有 schema 使用方式的三层审查。

## 目标

建立一套 Skill 合约与 schema 审计方案，用于回答三个问题：

1. 每个 Skill 的输入、输出、路径、schema 和脚本是否与项目当前定位对齐。
2. 不同 Skill 复用同一份 schema 或同一份产物时，是否存在字段理解、路径或状态更新冲突。
3. 当前 schema 是否足够支撑 Skills 的真实输出，是否需要参考同级项目 `other/oh-story-claudecode` 补充 schema 或文档约束。

## 非目标

- 不在本轮直接实现统一 Skill Runner。
- 不重启或修复冻结遗留的 Python CLI 流水线。
- 不盲目搬运 `oh-story-claudecode` 的目录结构或字段设计。
- 不批量重构所有历史 `docs/superpowers/plans/` 旧计划，只在当前文档中明确旧计划仅供参考。
- 不覆盖用户已有修改，尤其是当前工作树中的 `docs/feedback/archive/feedback.md`。

## 推荐方案

采用“先审计、再最小修正”的方案。

### 方案 A：只改已知路径漂移

优点是改动小，可以快速统一 `content/chapter_*.md`、`paywall_report.yaml` 和章节索引说明。缺点是无法发现 schema 层面的隐性冲突，后续 Skill 仍可能按不同理解生成同一份 YAML。

### 方案 B：完整重建 schema 与 Skill Runner

优点是约束最强，可以用 runtime 强制 schema、进度和脚本门禁。缺点是范围过大，会从文档修正膨胀成系统重构，且当前需求还没有要求恢复自动化流水线。

### 方案 C：Skill 合约与 schema 审计后做最小修正

这是推荐方案。先产出 `docs/SKILL_CONTRACT_AUDIT.md`，把每个 Skill 的输入、输出、schema、脚本、状态文件和冲突结论列清楚；再根据审计结果修改主文档和少量 Skill 文档，必要时补充 schema 建议或新增轻量 schema。这样能解决当前混乱，又避免过早建设 runner。

## 审计范围

### 项目内文件

- `.agents/AGENTS.md`
- `.agents/skills/*/SKILL.md`
- `.agents/skills/*/scripts/*.js`
- `.agents/skills/*/references/*.md`
- `data/schemas/*.schema.yaml`
- `templates/default/settings/*.yaml`
- `README.md`
- `docs/REQUIREMENTS.md`
- `docs/PIPELINE.md`
- `docs/USER_MANUAL.md`
- `docs/README.md`

### 参考项目

只读参考同级项目：

- `other/oh-story-claudecode`

参考原则：

- 只吸收合约表达、schema 粒度、质量门禁边界等可迁移经验。
- 不复制与本项目定位冲突的自动化结构。
- 若参考项目字段更完整，先记录为“补充建议”，再判断是否进入本项目 schema。

## 核心合约定义

### 正文路径

统一为：

```text
content/chapter_*.md
content/chapter_001.md
content/chapter_XXX.md
```

`content/chapters/` 视为旧路径，不作为当前新流程使用。

### 章节规划

`settings/chapters_index.yaml` 是章节总索引和跨 Skill 调度表，必须能支撑：

- `golden-chapters` 定位前三章摘要和微节拍。
- `daily-write` 定位目标章节、上下文和状态。
- `paywall-design` 分析张力曲线与候选切点。

`settings/chapter_outlines/chapter_*.md` 是单章详细蓝图，定位为 `design-chapters` 生成的详细细纲。它可以承载比索引更长的分场、节拍、情绪和字数预算。下游 Skill 可以读取，但不能把它当成替代 `chapters_index.yaml` 的主索引。

### 付费卡点报告

统一为项目根目录：

```text
paywall_report.yaml
```

`settings/paywall_report.yaml` 视为旧计划残留，不作为当前主路径。

### 状态文件

`_progress.md` 位于单本小说项目根目录，用于长任务断点恢复。审计时需要检查每个涉及长任务的 Skill 是否说明：

- 启动时检查 `_progress.md`。
- 进入新 Phase 时更新 `current_phase`。
- 完成后清理或标记完成。

## Schema 三层审查

### 第一层：单 Skill 与项目对齐

逐个审查 `.agents/skills/*/SKILL.md`：

- 前置输入是否存在于当前项目目录结构中。
- 输出路径是否与主文档一致。
- 生成 YAML 前是否要求读取对应 `data/schemas/*.schema.yaml`。
- 输出结构是否与 schema 和模板一致。
- 脚本调用路径是否指向当前 `.agents/skills/.../scripts/` 或共享脚本。
- 是否存在仍引用冻结 Python CLI 或旧 `scripts/` 主入口的问题。

### 第二层：跨 Skill 共用 schema 冲突

重点审查以下共享产物：

| 产物 | 生产者 | 消费者 | 冲突检查点 |
|------|--------|--------|------------|
| `settings/scout_report.yaml` | `scout-topic` | `worldbuilding`、`design-character`、`golden-chapters`、`daily-write` | `genre`、`required_elements`、标签结构是否一致 |
| `settings/worldbuilding.yaml` | `worldbuilding` | `design-character`、`design-outline` | 世界规则、势力、地点字段是否被下游正确引用 |
| `settings/characters.yaml` | `design-character` | `design-outline`、`golden-chapters`、`daily-write`、`review` | 顶级 `characters: []`、角色类型、关系、语言风格是否一致 |
| `settings/outline.yaml` | `design-outline` | `design-chapters`、`paywall-design` | 幕、序列、节拍字段是否与章节拆分一致 |
| `settings/arcs.yaml` | `design-outline` | `daily-write` | 情节点和章节关系是否有可定位字段 |
| `settings/pacing.yaml` | `design-outline` | `design-chapters`、`paywall-design` | 张力字段是否与章节索引重复或冲突 |
| `settings/chapters_index.yaml` | `design-chapters` | `golden-chapters`、`paywall-design`、`daily-write` | 章节编号、文件名、摘要、节拍、张力、状态字段是否一致 |
| `settings/notes.yaml` | `design-outline`、`daily-write` | `daily-write`、`review` | tracking 节点是否有 schema 支撑 |
| `paywall_report.yaml` | `paywall-design` | `daily-write` | `paywall_chapter`、过渡章策略和反馈承诺字段是否足够明确 |

### 第三层：schema 充分性

评估现有 schema 是否覆盖真实流程：

- `scout_report.schema.yaml` 是否足够表达平台、品类、标签、读者、required_elements。
- `worldbuilding.schema.yaml` 是否覆盖类型化世界规则、势力、地点、资源和约束。
- `characters.schema.yaml` 是否覆盖主角、反派、配角、关系、语言风格和爽感维度。
- `outline.schema.yaml` 是否覆盖 `outline.yaml`、`arcs.yaml`、`pacing.yaml` 三份输出，或需要拆分 schema。
- `chapters.schema.yaml` 是否覆盖 `chapters_index.yaml` 与 `chapter_outlines/` 的关系。
- 是否缺少 `notes.schema.yaml`、`paywall_report.schema.yaml`、`golden_chapters_report.schema.yaml` 或导出配置 schema。

## 产物设计

### 新增审计文档

路径：

```text
docs/SKILL_CONTRACT_AUDIT.md
```

建议结构：

```markdown
# Skill Contract Audit

## 结论摘要

## 当前统一口径

## Skill 输入输出总表

## Schema 使用矩阵

## 跨 Skill 冲突清单

## Schema 缺口与补充建议

## 参考 oh-story-claudecode 的可借鉴点

## 后续实施建议
```

### 最小修正文档

根据审计结论修改：

- `.agents/AGENTS.md`：统一正文路径和 schema 读取规则。
- `README.md`：补充 `chapters_index.yaml` 与 `chapter_outlines/` 的关系、Python 冻结测试说明。
- `docs/REQUIREMENTS.md`：补充 Skill 合约边界和 schema 充分性原则。
- `docs/PIPELINE.md`：补充阶段 4 的双层细纲结构和阶段 6 的根目录 `paywall_report.yaml`。
- `docs/USER_MANUAL.md`：必要时同步用户可见路径。

### 最小修正 Skill

根据审计结论优先修正：

- `.agents/skills/design-chapters/SKILL.md`
- `.agents/skills/daily-write/SKILL.md`
- `.agents/skills/golden-chapters/SKILL.md`
- `.agents/skills/paywall-design/SKILL.md`
- `.agents/skills/design-outline/SKILL.md`

这些 Skill 直接连接章节索引、正文、卡点和上下文追踪，是最容易发生跨合约冲突的位置。

## 验证策略

### 文本检索验证

使用 `rg` 检查残留口径：

```bash
rg -n "content/chapters|settings/paywall_report|chapter_outlines|chapters_index|paywall_report|content/chapter_" README.md docs .agents
```

目标：

- 当前主文档不再把 `content/chapters/` 作为新流程路径。
- `settings/paywall_report.yaml` 只出现在历史文档或明确标注为旧路径的上下文中。
- `chapters_index.yaml` 与 `chapter_outlines/` 的关系被明确说明。

### 脚本可用性验证

检查 Skill 中出现的 JS 脚本路径是否存在：

```bash
rg -n "node .*\\.js" .agents/skills
```

必要时运行低风险的脚本帮助命令或使用最小样例验证脚本入参顺序。

### Schema 覆盖验证

对照 `data/schemas/*.schema.yaml`、`templates/default/settings/*.yaml` 和 Skill 示例，人工确认字段是否可落盘、可被下游读取、可被脚本检查。

## 风险与边界

- 当前 Python 测试可能仍然红，本轮不把 Python 测试作为 Skill 合约审计通过条件。
- 旧计划文档可能继续保留历史路径，不能把历史目录全部改写为当前事实，否则会破坏历史记录。
- 如果发现 schema 明显缺失，优先记录建议；只有当现有 Skill 已经依赖该结构时，才新增或修改 schema。
- 若参考项目 `oh-story-claudecode` 与本项目产品定位冲突，以本项目当前 README、REQUIREMENTS、PIPELINE 和 `.agents/skills/` 为准。

## 成功标准

- 有一份可维护的 `docs/SKILL_CONTRACT_AUDIT.md`，能回答每个 Skill 的输入、输出、schema、脚本和状态文件。
- 主文档和关键 Skill 对正文路径、章节索引、单章细纲、付费报告位置的描述一致。
- 跨 Skill 共用 schema 的冲突被明确列出，并区分“必须修正”和“后续建议”。
- schema 缺口被记录，必要补充项有明确理由和影响范围。
- 后续实现计划可以基于本 spec 拆成小步任务，而不需要重新讨论方向。
