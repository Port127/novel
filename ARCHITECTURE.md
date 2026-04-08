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
- 章节生产流水线
- 角色与关系演进
- 时间线与剧情管理
- 世界观与设定集管理
- 素材检索与参考（通过 `../novel-material` 素材库）
- 合规与借鉴可追溯性
- 写作风格与去 AI 质量控制（六维检测、角色语言画像 `speech_pattern`、分策略改写）
- 流程编排（8 个 pipeline 预设）

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

### 已知接受的代价

- `/consistency-check` 仍需读取 13+ 种文件类型（God Reader），后续可通过拆分为 per-domain 子检查并由 consistency-check 汇总来减轻。
- `/project-reindex` 仍需写入全部索引和交叉引用（God Writer），这是 ADR-2 的必然结果。保持为低频维护工具即可。
