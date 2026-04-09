# Architecture

## 系统拓扑
本仓库是一个以 Skill 为中心的写作系统。

核心层级：
1. 命令/Skill 层：`.claude/skills/*`
2. 状态层：`.current.yaml`、`.projects.yaml`
3. 记忆层（Cursor Rules）：
   - 通用规则：`.cursor/rules/novel-workflow.mdc`（所有项目共享）
   - 项目专属规则源：`projects/{name}/.novel/rules/context.md`、`constraints.md`
   - 活跃规则：`.cursor/rules/novel-project-context.mdc`、`novel-core-constraints.mdc`（由 `/novel-switch` 和 `/project-reindex` 同步，`/novel-init` 初始化空模板）
4. 项目模板/数据层：`templates/project/*`、`shared/styles/*`（含 `anti_ai_rules.yaml` 去AI感规则库）
5. 产品文档层：`README*.md`、`docs/*`

## 主要领域
- 项目管理与报告
- 章节生产流水线（含多版本草稿对比与提升）
- 角色与关系演进
- 时间线与剧情管理
- 钩子/伏笔生命周期管理（分级、截止、回收追踪）
- 世界观与设定集管理（含设定演化与有效期）
- 素材检索与参考（通过 `../novel-material` 素材库）
- 合规与借鉴可追溯性
- 写作风格与去 AI 质量控制（六维检测、角色语言画像 `speech_pattern`、分策略改写）
- 流程编排（8 个 pipeline 预设）
- 编辑后影响扫描与章节容量守卫

## 素材库集成
独立素材库 `../novel-material/` 提供场景、人物、技法的多维检索。集成方式：
- 项目配置：`projects/{name}/.novel/materials.yaml` 注册素材库路径和引用
- 桥接 Skill：`/material-search` 在本 workspace 内直接调用素材库检索脚本
- 写作增强：`/chapter-draft` 和 `/plot-suggest` 内置可选检索步骤
- 合规链路：`/inspiration-log` → `/inspiration-check` → `/inspiration-report` 通过素材 ID 关联
- 降级策略：素材库不存在时全部跳过，不阻断主流程

## 公开契约
- 命令契约：
  - 完整命令参考在 `docs/SPEC.md`（Skill清单）。
  - 场景使用指南在 `docs/USAGE-GUIDE.md`。
  - Skill 具体行为定义在各 `SKILL.md` 中。
- 状态契约：
  - 当前项目指针：`.current.yaml`
  - 项目列表：`.projects.yaml`
  - 项目模板基线：`templates/project/`
  - `state.yaml` 仅存储不可从源文件推导的状态（项目元信息、工作流状态、设计选择）。角色计数、设定计数、章节数等派生数据由读取方按需从源文件计算。
- 报告契约：
  - KPI/报告命令必须使用显式来源文件，缺失数据返回 `N/A`。

## 变更边界
- 更新命令行为：编辑 `.claude/skills/` 下的目标 skill 文件。
- 更新数据模型：通过 `templates/project/` 下的模板文件。
- 更新操作指引：在 `docs/` 中更新。
- 避免将业务逻辑耦合进 harness 文档；保持链接与契约稳定。

## 架构决策与已知约束

### ADR-1：state.yaml 瘦身（2026-04-08）

**决策**：`state.yaml` 只存储不可从源文件推导的状态（`project`、`protagonist`、`ingestion`、`plot.structure`、`current_focus`）。角色列表、设定计数、章节数、时间线范围、关系统计等派生数据从源文件按需计算。

**动机**：此前 12+ 个 skill 分散写入 `state.yaml` 的计数字段，导致频繁漂移和不一致，需要 `/project-reindex` 反复修复。

**代价**：`/novel-status` 等读取方需要遍历源文件才能统计，不能直接查 state.yaml。对当前项目规模（几十个文件）可忽略。

### ADR-2：单向交叉引用（2026-04-08）

**决策**：CRUD skill（`/character-add`、`/setting-add` 等）只写自己领域的文件。角色的 `cross_references` 与设定的 `character_links` 之间的双向引用统一由 `/project-reindex` 维护。

**动机**：此前 `/character-add` 会写设定文件，`/setting-add` 会写角色文件，造成循环写入。两个领域的 skill 互相依赖对方的文件 schema，任何一方改动都会打破对方。

**代价**：新增角色或设定后，交叉引用不会实时更新，需要手动运行 `/project-reindex`。日常写作中轻微的引用不一致不影响流程。

### ADR-3：Pipeline 委派规范（2026-04-08）

**决策**：Pipeline 引用子 skill 时统一使用两种措辞——"调用 /skill-name"（完整执行）或"参照 /skill-name（具体部分）"（引用部分逻辑）。禁止"按 X 的标准/口径/方法"等模糊写法。详见 `_protocols/pipeline-delegation.md`。

**动机**：模糊措辞导致 AI 可能不读取子 skill 的实际定义，内联的审查逻辑与子 skill 更新脱节。

### ADR-4：章节摘要链与角色状态快照（2026-04-08）

**决策**：`chapters/index.yaml` 新增 `summary` 和 `characters_involved` 字段，角色卡新增 `current_state` 块。`/chapter-update` 在状态推进到 `draft`/`final` 时自动生成摘要和更新角色状态。`/chapter-draft` 写新章时优先读取摘要链和角色当前状态，而非回读全部正文。

**动机**：写到第 20 章时，AI 不知道前 19 章发生了什么，导致人物行为不一致、信息重复交代、伏笔遗漏。读全部正文既昂贵又容易超出上下文窗口。

**代价**：每次推进章节状态多一步摘要生成（约 100 字），每个主要角色多一步状态更新。对已写但未生成摘要的旧章节，需手动补跑 `/chapter-update --status draft`。

### ADR-5：角色语言画像与去AI感闭环（2026-04-08）

**决策**：角色模板新增 `speech_pattern` 块（语气/句式/粗话/口头禅/禁用词等），`anti_ai_rules.yaml` 扩展为六维规则库（套话/句式/比喻/描写/对白/转折）。三层闭环：`chapter-draft` 源头写对 → `anti-ai-check` 六维检测 → `anti-ai-rewrite` 分策略修复。

**动机**：AI 生成文本的两个核心问题——比喻/描写堆砌和对白同质化——此前缺乏量化检测维度和针对性修复策略。对白改写没有角色语言画像可参照，只能做笼统的"去AI感"。

**代价**：创建角色时多了 `speech_pattern` 需要填（至少填 tone + profanity_level + sample_lines）。对已存在的角色卡需要手动补充或通过 `--auto-fill` 从章节对白中提炼。

### ADR-6：分级钩子/伏笔系统（2026-04-09）

**决策**：`plot/outline.yaml` 中 `foreshadowing` 升级为结构化数组，每个钩子包含 `id`、`name`、`level`（major/minor/micro）、`status`（planted/pending/recovered/abandoned）、`recovery_deadline`（type/value/hard）、`recovery_conditions`、`linked_hooks`。新增三个 skill：`/hook-add`（登记）、`/hook-query`（查询，含时间轴视图和逾期过滤）、`/hook-resolve`（回收/放弃/延期）。`/pipeline-chapter-kickoff` 开写时自动提醒近期到期钩子，`/chapter-review` 按级别检查伏笔密度，`/consistency-check` 纳入钩子健康度检查。

**动机**：此前伏笔仅以自由文本记录在大纲中，没有分级、截止时间和回收追踪。写到中后期容易遗漏 minor/micro 钩子，major 钩子的回收也无法量化监控。

**代价**：每个伏笔需要在埋设时额外花 1 步登记（`/hook-add`），回收时 1 步确认（`/hook-resolve`）。对已有项目中未登记的旧伏笔，需要补录。

### ADR-7：设定演化与有效期（2026-04-09）

**决策**：设定模板新增 `valid_from`、`valid_until`、`expiry_trigger`、`supersedes`、`superseded_by` 字段。`/setting-add` 支持 `--supersedes` 创建接替设定并自动废弃旧版。`/setting-edit` 支持 `--evolve` 以旧设定为基础演化新版。`/chapter-draft` 生成初稿时过滤过期设定，`/pipeline-chapter-kickoff` 开写时提醒即将过期设定，`/consistency-check` 检查设定有效期与章节引用的一致性。

**动机**：长篇连载中世界观规则会随剧情推进而变化（"融合第二阶段后旧规则失效"），此前只能手动标记 deprecated，没有新旧设定的关联链，也无法自动过滤过期设定。

**代价**：每个有生命周期的设定需要额外设置有效期字段。`/chapter-draft` 读取设定时多一步过滤逻辑。对于永久有效的设定，不需要填这些字段（默认全生命周期有效）。

### ADR-8：多版本章节草稿（2026-04-09）

**决策**：`chapters/index.yaml` 新增 `versions` 数组和 `active_version` 字段。`/chapter-draft --alt [备注]` 生成备选版本文件（`ch001_v2.md`），新增 `/chapter-compare` 对比多版本，`/chapter-update --promote v{N}` 提升备选为主版本。

**动机**：同一章节可能有多种写法（悬疑开场 vs 动作开场），此前只能手动管理文件和对比，没有结构化的版本追踪。

**代价**：备选版本的文件和元数据增加了磁盘占用和 `index.yaml` 复杂度。提升版本后旧主版本降级为备选，不自动删除。

### ADR-9：编辑后影响扫描与章节容量守卫（2026-04-09）

**决策**：新增两个协议——`post-edit-impact-scan.md` 要求 `setting-edit` 和 `character-edit` 在修改核心数据后，自动扫描已写章节中可能存在的冲突并向用户发出警告（不自动修改正文）。`chapter-scope-guard.md` 要求 `chapter-draft` 和 `pipeline-chapter-kickoff` 在生成前检查章节容量，防止将多章剧情塞入单章。

**动机**：修改设定/角色后，已写章节可能出现与新设定不一致的内容，此前只有全局 consistency-check 能发现，没有即时反馈。章节容量方面，AI 容易将一个跨多章的剧情弧线压缩到单章中，导致信息密度过高。

**代价**：编辑操作后多一步扫描（扫描范围限于引用了修改内容的章节），开写新章前多一步容量检查。两者都只产出警告，不阻断流程。

### ADR-10：名字解析协议与命名配置（2026-04-09）

**决策**：新增 `_protocols/name-resolution.md` 定义称呼选择规则（按 POV 与角色关系亲疏）、项目级命名规范（`meta.yaml` 新增 `naming` 配置：era/culture/forbidden_patterns）、重命名事务化（dry-run → confirm → execute）。`character-add` 起名时参照命名配置，`character-edit` 改名走事务化流程，`chapter-draft` 和 `anti-ai-rewrite` 生成/改写时遵守称呼选择规则。

**动机**：名字/别称处理散落在 10+ 个 skill 中，AI 生成文本时默认用正式名覆盖别称，改名操作影响面大但无预览机制，起名风格不受项目配置约束。

**代价**：`meta.yaml` 多了一个配置块（默认值已预设，不填也能用）。改名操作多了一步 dry-run 预览。

### ADR-11：预检完整性协议（2026-04-09）

**决策**：新增 `_protocols/preflight-integrity.md`，在 `pipeline-chapter-kickoff`、`chapter-draft`、`chapter-update`、`pipeline-draft-polish` 的前置检查中嵌入轻量完整性验证（目标章节 ± 2 章范围）。检测孤儿索引/文件、版本文件缺失、前序章节 summary 缺失等问题。`novel-doctor` 新增 `--quick` 模式。

**动机**：用户手动删文件或 git 操作后，skill 运行时无法检测孤儿引用，导致级联修改。每个 skill 各自处理缺失文件，无统一模式。

**代价**：每次关键操作前多读 5-10 个文件做校验（< 3 秒）。极少数情况下预检会阻断操作要求用户先修复。

### ADR-12：大纲分层与粒度检测（2026-04-09）

**决策**：`plot-add` 新增内容粒度检测——根据输入内容的具体程度（场景级/章节级/幕级）引导写入正确位置。场景级内容 → 章节文件 `## 场景大纲`，幕级内容 → `outline.md`。粒度不匹配时主动提示用户选择。

**动机**：`outline.md` 被当成万能容器，章节级细节和幕级结构混杂，导致大纲臃肿且不可用。

**代价**：`plot-add` 的判断逻辑更复杂，偶尔可能误判粒度需要用户纠正。

### ADR-13：风格生命周期管理（2026-04-09）

**决策**：新增 `_protocols/style-lifecycle.md` 定义风格模板的三阶段生命周期——积累期（0-2 章不触发）、提炼触发（≥ 3 章 draft 时主动发起提炼流程）、漂移检测（每 10 章提醒更新）。`chapter-update` 和 `pipeline-draft-polish` 分别负责触发和检测。

**动机**：`style-create` 完全被动，用户必须记得手动跑。chapter-update 的弱提示容易被忽略。

**代价**：提炼流程会中断 chapter-update 的输出（用户可选跳过）。`meta.yaml` 新增 `style.extracted_at_chapter` 字段。

### ADR-14：素材消化结构化输出与置信度标记（2026-04-09）

**决策**：`ingestion_brief.md` 改为 YAML front matter + Markdown body，每条提取内容附带 HTML 注释形式的机读元数据（`confidence: verbatim|inferred|supplemented` + `source_lines`）。`from-extraction.md` 补充机读格式定义。`pipeline-outline-bootstrap` 消费时按置信度分级处理：verbatim 直接用，inferred 标注后用，supplemented 必须单独确认。

**动机**：纯 markdown 的 ingestion_brief 无法机读来源，下游 skill 偷偷混入非来源内容（如把 outline 的内容混入"从草稿提取的情节"）。

**代价**：ingestion_brief 格式更复杂，手动编辑时需注意 HTML 注释。

### ADR-15：操作日志与来源水印（2026-04-09）

**决策**：新增 `_protocols/operation-journal.md` 和 `templates/project/.novel/ops_log.yaml`。多文件写入 skill 在操作前后记录日志，启动时检测未完成操作。`chapter-draft` 在写作备忘区追加"内容来源追溯"表，标记每个生成段落的来源和置信度。

**动机**：多 skill 写同一文件无协调机制，操作中断导致半写状态无法检测。chapter-draft 生成的内容无法追溯哪些来自大纲、哪些是 AI 补充。

**代价**：ops_log.yaml 需要定期清理（协议定义了自动清理策略）。来源水印表增加章节文件长度（标记为可删除）。

### ADR-16：上下文预算协议（2026-04-09）

**决策**：新增 `_protocols/context-budget.md`，定义三级读取策略——索引优先（默认）、聚焦读取（针对性操作）、全量扫描（显式触发）。`chapter-draft` 上下文按 P0-P4 分级，预算超过 15000 字时从 P4 向上裁剪。`consistency-check` 改为分阶段加载（三轮）。skill 中的读取步骤用 `[索引优先]`、`[聚焦读取]`、`[必读]`、`[可裁剪]` 标记说明策略。

**动机**：skill 执行时读取大量文件导致 AI 注意力稀释、context rot 和不可预测行为。Anthropic 上下文工程研究表明"找到最小的高信号 token 集合"是控制生成质量的关键。

**代价**：部分 skill 的上下文加载逻辑更复杂。`consistency-check` 从一次性加载改为三轮分阶段，代码行数增加。极少数需要跨域上下文的操作可能需要用户显式请求全量扫描。

### ADR-17：评估闸门与反馈闭环（2026-04-09）

**决策**：新增 `_protocols/eval-gate.md`。三项核心机制——(1) 评估结果落盘：`chapter-review`、`voice-check`、`anti-ai-check` 的结论写入 `chapters/{chapter_id}_review.yaml`；(2) 阈值阻断：`pipeline-draft-polish` 推进状态前检查分数，低于阈值不推进（`--force`/`--threshold` 可覆盖）；(3) 反馈闭环：`chapter-draft` 生成前读取已有 review 文件，提取 blocking_issues 和 high priority suggestions 注入写作指令。

**动机**：此前审查结果只输出到终端，无法跨 skill 共享，也无法形成"写→审→改"的闭环。AI 重复生成时容易重犯已知问题。

**代价**：每次审查多一步文件写入。`_review.yaml` 随章节增多会增加磁盘占用。阈值是默认值，用户需要根据项目实际情况调优。

### ADR-18：机械化校验（2026-04-09）

**决策**：新增 `project-lint` skill，做机械化文件/索引一致性检查（vs `novel-doctor` 侧重目录结构）。覆盖 7 个检查域：章节文件-索引一致性、角色文件-索引一致性、设定文件-索引一致性、钩子健康度、操作日志健康度、交叉引用完整性、命名规范。支持 `--fix` 自动修复安全项（孤儿索引、遗留 in_progress、日志清理），错误消息直接嵌入修复命令。对缺失的可选文件（ops_log.yaml、naming 配置）跳过检查并输出信息提示。

**动机**：此前"软约束"只写在协议文档中，依赖 AI 自觉遵循。用户手动删文件或 git 操作后产生孤儿引用，skill 运行时才发现。doctor 和 lint 职责不同——doctor 检查"骨架"（目录/配置），lint 检查"数据引用链"。

**代价**：lint 运行时需要读取多个索引和文件，对大型项目（100+ 章）可能需要数秒。`--fix` 仅修索引不碰内容文件，但仍需谨慎使用。

### 已知接受的代价

- `/consistency-check` 仍需读取 13+ 种文件类型（God Reader），后续可通过拆分为 per-domain 子检查并由 consistency-check 汇总来减轻。
- `/project-reindex` 仍需写入全部索引和交叉引用（God Writer），这是 ADR-2 的必然结果。保持为低频维护工具即可。
