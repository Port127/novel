# Skill Contract Audit

## 结论摘要

本轮审计确认：当前主流程已经以 `.agents/skills/` 为入口，`src/novel/`、根目录 `scripts/` 和 `novel` CLI 只保留为冻结遗留。需要修正的主要问题不是代码运行时，而是 Skill 合约、主文档、schema 和模板之间的口径漂移。

基线审计发现并已在本轮完成对齐的事项：

- `.agents/AGENTS.md` 曾把正文目录写成 `content/chapters/`，现已统一为 `content/chapter_*.md`，并明确旧路径不作为当前新流程路径。
- 主文档已补充 `settings/chapters_index.yaml` 与 `settings/chapter_outlines/chapter_*.md` 的双层关系。
- 高影响 Skill 中的 `scripts/*.js` 短路径已改为 `.agents/skills/<skill>/scripts/` 或 `.agents/skills/_shared/scripts/` 下的实际路径。
- `data/schemas/chapters.schema.yaml` 与 `templates/default/settings/chapters_index.yaml` 已对齐为当前章节索引合约：使用 `chapter/file/outline_file/words_target` 和 tension 1-5。
- `settings/notes.yaml` 与 `paywall_report.yaml` 已新增 dedicated schema；`history/golden_chapters_report.md`、导出配置等产物仍需后续补强。

参考项目 `other/oh-story-claudecode` 在当前执行环境中不可访问：`find /Users/kiki/Documents/Project -maxdepth 6 -type d -name oh-story-claudecode` 和 `find /Users/kiki/Documents/Project/my-github -maxdepth 6 -type d -name oh-story-claudecode` 均因权限限制失败。本轮审计不依赖该项目完成。

## 当前统一口径

- 正文路径统一使用 `content/chapter_*.md`，例如 `content/chapter_001.md`、`content/chapter_XXX.md`。
- `content/chapters/` 是旧路径，不作为当前新流程路径。
- `settings/chapters_index.yaml` 是章节总索引和跨 Skill 调度表。
- `settings/chapter_outlines/chapter_*.md` 是单章详细蓝图，由 `design-chapters` 生成，可被下游读取，但不能替代章节总索引。
- `paywall_report.yaml` 位于单本小说项目根目录；`settings/paywall_report.yaml` 是旧计划残留路径。
- `_progress.md` 位于单本小说项目根目录，只用于长任务断点恢复。
- `src/novel/`、根目录 `scripts/` 和 `novel` CLI 是冻结遗留，不定义当前创作主流程。

## Skill 输入输出总表

| Skill | 主要输入 | 主要输出 | 使用 schema | 脚本门禁 | 状态文件 | 对齐结论 |
|-------|----------|----------|-------------|----------|----------|----------|
| scout-topic | 用户选题目标、平台偏好、`references/*.md` | `settings/scout_report.yaml` | `data/schemas/scout_report.schema.yaml` | `node .agents/skills/scout-topic/scripts/check-tags.js settings/scout_report.yaml` | 无明确 `_progress.md` 合约 | 基本对齐；可继续作为下游品类和 required_elements 来源。 |
| worldbuilding | `settings/scout_report.yaml`、世界观 references | `settings/worldbuilding.yaml` | `data/schemas/worldbuilding.schema.yaml` | `node .agents/skills/worldbuilding/scripts/check-completeness.js settings/scout_report.yaml settings/worldbuilding.yaml` | `_progress.md` | 基本对齐；脚本路径已是当前路径。 |
| design-character | `settings/scout_report.yaml`、`settings/worldbuilding.yaml`、人物 references | `settings/characters.yaml` | `data/schemas/characters.schema.yaml` | `node .agents/skills/design-character/scripts/check-characters.js {project_dir}/settings/scout_report.yaml {project_dir}/settings/characters.yaml` | 无明确 `_progress.md` 合约 | 基本对齐；`{project_dir}` 占位符需要执行时替换。 |
| design-outline | `settings/scout_report.yaml`、`settings/worldbuilding.yaml`、`settings/characters.yaml` | `settings/outline.yaml`、`settings/arcs.yaml`、`settings/pacing.yaml`、`settings/notes.yaml` | `data/schemas/outline.schema.yaml` 只覆盖 `outline.yaml` 主结构；`settings/notes.yaml` 使用 `data/schemas/notes.schema.yaml`；`arcs/pacing` 由模板与脚本门禁约束 | `node .agents/skills/design-outline/scripts/check-outline.js settings/scout_report.yaml settings/outline.yaml`；`node .agents/skills/design-outline/scripts/check-pacing.js settings/pacing.yaml` | `_progress.md` | 已对齐脚本路径，并补充 `outline/arcs/pacing/notes` 的 schema 边界。 |
| design-chapters | `settings/outline.yaml`、`settings/scout_report.yaml`、章节 references | `settings/chapters_index.yaml`、`settings/chapter_outlines/chapter_*.md` | `data/schemas/chapters.schema.yaml` | `node .agents/skills/design-chapters/scripts/check-chapters.js settings/chapters_index.yaml`；`node .agents/skills/design-chapters/scripts/check-outlines.js settings/chapter_outlines/` | `_progress.md` | 已对齐脚本路径、总索引与单章蓝图关系，并统一 `chapter/file/outline_file/words_target/tension 1-5` 为当前标准。 |
| golden-chapters | `settings/outline.yaml`、`settings/chapters_index.yaml`、`settings/scout_report.yaml`、`settings/characters.yaml` | `content/chapter_001.md`、`content/chapter_002.md`、`content/chapter_003.md`、`history/golden_chapters_report.md` | 正文无直接 schema；报告缺 dedicated schema | `node .agents/skills/golden-chapters/scripts/check-golden-structure.js ...`；`node .agents/skills/golden-chapters/scripts/check-ai-patterns.js ...`；`node .agents/skills/golden-chapters/scripts/check-degeneration.js ...` | `_progress.md` | 已对齐脚本路径，并说明前三章可读取 `chapter_outlines/` 补足微节拍。 |
| paywall-design | `settings/outline.yaml`、`settings/chapters_index.yaml` | `paywall_report.yaml` | `data/schemas/paywall_report.schema.yaml` | `node .agents/skills/paywall-design/scripts/check-paywall.js settings/chapters_index.yaml paywall_report.yaml` | `_progress.md` | 已对齐脚本路径，保持根目录 `paywall_report.yaml` 口径，并新增报告字段门禁。 |
| daily-write | `settings/chapters_index.yaml`、`settings/notes.yaml`、前文正文、可选 `settings/chapter_outlines/chapter_*.md`、可选 `paywall_report.yaml` | `content/chapter_XXX.md`，并更新 `settings/notes.yaml`、`settings/chapters_index.yaml` 状态 | 正文无直接 schema；`settings/notes.yaml` 使用 `data/schemas/notes.schema.yaml` | `node .agents/skills/_shared/scripts/check-ai-patterns.js --check content/chapter_{N}.md`、`node .agents/skills/daily-write/scripts/normalize-punctuation.js content/chapter_{N}.md`、`node .agents/skills/_shared/scripts/check-degeneration.js --check content/chapter_{N}.md` | `_progress.md` | 脚本路径基本对齐；需要明确章节索引与详细蓝图读取优先级。 |
| review | 正文、`settings/outline.yaml`、`settings/arcs.yaml`、`settings/pacing.yaml`、`settings/characters.yaml`、追踪记录 | 对话审查报告或用户指定路径 | 统一 Findings Schema 写在 Skill 内；无文件级 dedicated schema | 可运行共享 `check-ai-patterns.js`、`check-degeneration.js` | 无明确 `_progress.md` 合约 | 基本对齐；报告结构为文本合约。 |
| data-diagnosis | 平台导出 CSV、可选 `settings/chapters_index.yaml` | `data_diagnosis_report.yaml` | 无直接 schema | 当前写法为 `scripts/analyze-metrics.js` 短路径 | 无明确 `_progress.md` 合约 | 非本轮高影响 Skill；后续应补脚本路径和报告 schema。 |
| stock-check | 存稿目录、章节状态、成本信息 | 存稿看板输出 | 无直接 schema | 无脚本门禁 | 无明确 `_progress.md` 合约 | 辅助 Skill，当前不阻断主创作合约。 |
| export-novel | `content/chapter_*.md`、项目元数据、导出目标 | `exports/` 下成稿文件 | 缺导出配置 schema | 无明确脚本门禁 | 无明确 `_progress.md` 合约 | 后续应补导出配置和目录职责说明。 |
| nm | 素材库查询条件、品类/关键词 | 检索结果、入库建议 | 无直接 schema | `nm search` 外部能力 | 无明确 `_progress.md` 合约 | 与创作主流程弱耦合；只作为参考素材输入。 |
| feature-planning | 用户功能需求、现状代码/文档 | `docs/superpowers/specs/*.md` 或用户指定方案文档 | 无直接 schema | 无脚本门禁 | 无明确 `_progress.md` 合约 | 工程辅助 Skill，不参与小说产物 schema。 |
| refactor-planning | 重构目标、现状代码/文档 | 重构痛点分析和执行计划文档 | 无直接 schema | 无脚本门禁 | 无明确 `_progress.md` 合约 | 工程辅助 Skill，不参与小说产物 schema。 |
| code-review-change | 指定变更、调用链和上下游证据 | 结构化审查报告 | 无直接 schema | 无脚本门禁 | 无明确 `_progress.md` 合约 | 工程辅助 Skill，不参与小说产物 schema。 |
| commit-msg | Git 变更、验证信息 | Conventional Commit 中文提交信息或提交结果 | 无直接 schema | 提交信息自检规则 | 无明确 `_progress.md` 合约 | 工程辅助 Skill，受项目提交规范约束。 |

## Schema 使用矩阵

| Schema 或产物 | 生产 Skill | 消费 Skill | 当前覆盖 | 风险 |
|---------------|------------|------------|----------|------|
| `data/schemas/scout_report.schema.yaml` | `scout-topic` | `worldbuilding`、`design-character`、`design-outline`、`golden-chapters`、`daily-write` | 覆盖平台、品类、读者、标签、`required_elements` | 当前较完整；执行时必须确保 `required_elements` 被下游真实使用。 |
| `data/schemas/worldbuilding.schema.yaml` | `worldbuilding` | `design-character`、`design-outline`、`daily-write` | 覆盖世界类型、核心规则、力量体系、势力、地点、lore | 与 `required_elements.worldbuilding` 依赖脚本校验，基本可用。 |
| `data/schemas/characters.schema.yaml` | `design-character` | `design-outline`、`golden-chapters`、`daily-write`、`review` | 覆盖顶级 `characters: []`、角色类型、关系、心理和弧线 | 语言风格、爽感维度主要靠 Skill references，不完全由 schema 约束。 |
| `data/schemas/outline.schema.yaml` | `design-outline` | `design-chapters`、`paywall-design`、`review` | 只覆盖 `settings/outline.yaml` 核心结构、幕/序列/节拍、hooks、pacing_curve | `settings/arcs.yaml`、`settings/pacing.yaml` 由对应模板、Skill 文档和脚本门禁约束；`settings/notes.yaml` 已由 `data/schemas/notes.schema.yaml` 约束。 |
| `data/schemas/chapters.schema.yaml` | `design-chapters` | `golden-chapters`、`paywall-design`、`daily-write`、`data-diagnosis` | 覆盖 `settings/chapters_index.yaml` 的章节列表、正文路径、细纲路径、状态、摘要、节拍、张力和统计 | 已与默认 `chapters_index.yaml` 模板对齐；单章细纲 frontmatter 由 `data/schemas/chapter_outline_frontmatter.schema.yaml` 约束。 |
| `data/schemas/chapter_outline_frontmatter.schema.yaml` | `design-chapters` | `daily-write`、`golden-chapters`、`review` | 覆盖 `settings/chapter_outlines/chapter_*.md` 的 YAML Frontmatter，正文 Markdown 结构继续由 `references/chapter-template.md` 约束 | 已由 `check-outlines.js` 检查必要字段、章节号、路径、状态、密度、张力和预算。 |
| `settings/arcs.yaml` | `design-outline` | `daily-write`、`review` | 由模板和 Skill 文档说明，使用 `chapter_range` 或 `beat_refs` 定位 | 暂不拆 dedicated schema，后续若多 Skill 写入再补。 |
| `settings/pacing.yaml` | `design-outline` | `design-chapters`、`paywall-design`、`review` | 由模板和 `check-pacing.js` 约束，章节级 `tension` 范围统一为 1-5 | 暂不拆 dedicated schema，后续若多 Skill 写入再补。 |
| `data/schemas/notes.schema.yaml` | `design-outline`、`daily-write` | `daily-write`、`review` | 覆盖 `settings/notes.yaml` 的三层上下文、角色状态、伏笔追踪和写作偏好节点 | 已新增 dedicated schema，后续可补脚本门禁。 |
| `data/schemas/paywall_report.schema.yaml` | `paywall-design` | `daily-write` | 覆盖根目录 `paywall_report.yaml` 的付费切点、候选切点、最终切点、悬念承诺、风险项和商业复核 | 已由 `check-paywall.js` 检查必填字段、最终切点一致性和切点张力。 |
| `history/golden_chapters_report.md` | `golden-chapters` | `review`、作者复盘 | Markdown 报告，无 dedicated schema | 报告结构不稳定但风险较低；可后续模板化。 |
| `exports/` | `export-novel` | 作者、发布平台 | 由导出 Skill 说明，缺导出配置 schema | 目标格式、章节顺序、元数据和过滤规则需要后续单独设计。 |

## 跨 Skill 冲突清单

| 严重级别 | 冲突 | 证据 | 建议 |
|----------|------|------|------|
| P1 必须修正 | `content/chapters/` 与 `content/chapter_*.md` 路径漂移 | 基线时 `.agents/AGENTS.md` 项目目录写 `content/chapters/`；README、PIPELINE、golden-chapters、daily-write 使用 `content/chapter_*.md` | 本轮已修正 `.agents/AGENTS.md` 和必要主文档，统一为 `content/chapter_*.md`。 |
| P1 必须修正 | `chapters_index.yaml` 与 `chapter_outlines/` 关系未在主文档充分说明 | 基线时 `design-chapters` 已输出两者，但 README、REQUIREMENTS、PIPELINE、USER_MANUAL 只强调 `chapters_index.yaml` | 本轮已补充双层结构：总索引用于调度，详细蓝图用于单章执行。 |
| P1 必须修正 | Skill 中 `scripts/*.js` 相对路径可能指向错误目录 | 基线时 `design-chapters`、`golden-chapters`、`paywall-design`、`design-outline` 存在短路径 | 本轮已修正高影响 Skill；其他辅助 Skill 后续补。 |
| P1 已修正 | `chapters.schema.yaml` 与 `templates/default/settings/chapters_index.yaml` 字段不一致 | 历史漂移：schema 使用 `chapter/file/words_target/words/stats` 和 tension 1-5；模板使用旧字段 `number/word_count/target_chapters/completed_chapters` 和 tension 1-10 | 本轮已统一为 `chapter/file/outline_file/words_target/words/stats`，张力范围为 1-5。 |
| P2 建议修正 | `settings/paywall_report.yaml` 与根目录 `paywall_report.yaml` 历史残留 | 设计稿和计划已标注旧路径；主流程 Skill 当前多使用根目录 `paywall_report.yaml` | 本轮验证主文档和高影响 Skill 不把 `settings/paywall_report.yaml` 当当前路径。 |
| P2 已修正 | `notes.yaml` tracking 节点缺少 dedicated schema | `design-outline` 初始化 `settings/notes.yaml`，`daily-write` 持续读写，模板只有注释 | 本轮已新增 `data/schemas/notes.schema.yaml`，并同步默认模板、`design-outline`、`daily-write` 与状态追踪参考。 |
| P2 已修正 | `paywall_report.yaml` 缺少 dedicated schema | `paywall-design` 生成，`daily-write` 消费；脚本只抽取 `paywall_chapter` | 本轮已新增 `data/schemas/paywall_report.schema.yaml`，并增强 `check-paywall.js` 字段门禁。 |
| P2 已修正 | `outline.schema.yaml` 与 `outline/arcs/pacing` 三文件边界不清 | `design-outline` 输出四个文件，但 schema 文件名和注释只指向 `outline.yaml` | 本轮保持 `outline.schema.yaml` 只约束 `outline.yaml` 主结构，并通过模板、`check-pacing.js` 与 Skill 文档明确相邻产物边界。 |
| P3 记录观察 | 参考项目不可访问 | 两次 `find` 均因 `Operation not permitted` 失败 | 本轮不阻断；如后续开放权限，可补充参考项目对照。 |

## Schema 缺口与补充建议

| 建议 | 类型 | 理由 | 优先级 | 本轮动作 |
|------|------|------|--------|----------|
| 新增 `notes.schema.yaml` | dedicated schema | `settings/notes.yaml` 被 `design-outline` 和 `daily-write` 共同读写，承载伏笔、角色状态、上下文摘要 | P2 | 已新增 dedicated schema，后续可补脚本门禁 |
| 新增 `paywall_report.schema.yaml` | dedicated schema | `paywall_report.yaml` 连接付费设计与日更执行，当前脚本只检查部分字段 | P2 | 已新增 dedicated schema，并由 `check-paywall.js` 执行字段门禁 |
| 为 `settings/chapter_outlines/chapter_*.md` 增加 schema 或模板约束 | frontmatter/schema | 单章蓝图是下游写作的重要输入，目前主要依赖 `references/chapter-template.md` | P2 | 已新增 `chapter_outline_frontmatter.schema.yaml`，并由 `check-outlines.js` 执行字段门禁 |
| 新增 `golden_chapters_report` 模板或 schema | 报告模板 | `history/golden_chapters_report.md` 用于复盘和后续审查，但结构稳定性要求低于 YAML | P3 | 仅记录 |
| 新增导出配置 schema | dedicated schema | `exports/` 的格式、章节顺序、元数据过滤会影响发布成稿 | P3 | 后续单独设计 |
| 评估 `outline/arcs/pacing` 是否拆分 schema | schema 拆分 | `outline.schema.yaml` 只明确覆盖 `outline.yaml` 核心结构，无法完整约束 `arcs.yaml` 与 `pacing.yaml` | P2 | 本轮不拆 schema；已通过模板、脚本和 Skill 文档明确边界 |
| 统一 `chapters.schema.yaml` 与 `templates/default/settings/chapters_index.yaml` | schema/template 对齐 | 两者字段名、统计字段、张力范围不同，容易导致新项目初始化即偏离 schema | P1 | 已实施，当前标准为 `chapter/file/outline_file/words_target/tension 1-5` |

## 参考 oh-story-claudecode 的可借鉴点

本轮只吸收参考项目中有助于表达 Skill 合约、schema 边界、质量门禁和目录职责的经验；不复制与本项目 Skill 驱动、人机协同定位冲突的自动化结构。

当前环境无法读取 `other/oh-story-claudecode`，因此本节只记录待补充方向：

- 若后续可访问参考项目，应优先比较 schema 粒度，而不是复制目录结构。
- 参考重点应放在“每个产物由谁生产、谁消费、字段边界在哪里、质量门禁如何表达”。
- 如果参考项目存在更完整的 `notes`、`paywall`、章节蓝图或导出配置约束，应先作为补充建议进入本审计文档，再决定是否修改本项目 schema。

## 后续实施建议

1. 已完成 `chapters.schema.yaml` 与 `templates/default/settings/chapters_index.yaml` 的字段、路径和张力范围对齐。
2. 已新增 `chapter_outline_frontmatter.schema.yaml`、`notes.schema.yaml` 和 `paywall_report.schema.yaml`，并同步高影响 Skill 的读写规则。
3. 已明确 `outline.schema.yaml` 只约束 `settings/outline.yaml` 主结构，`arcs/pacing` 暂由模板、Skill 文档和脚本门禁约束。
4. 后续可单独设计 Skill Runner、导出配置 schema、`data-diagnosis` 报告 schema 和历史文档隔离策略。
5. 辅助 Skill 中的短脚本路径，如 `data-diagnosis`，可在下一轮统一清理。
