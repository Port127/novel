# AI小说写作系统 - 业务能力补全清单（已归档）

> **归档说明（2026-04）**：本文档为早期规划文档。A-D 模块（P0）已全部实现，E-G 模块（P1）属于独立项目 novel-material。KPI 口径定义仍有参考价值。

> 面向真实写作流程：从“能用”升级到“能长期连载、能管控风险、能复盘提效”。

---

## 1) 现状结论

当前项目已具备基础能力：项目管理、角色管理、剧情骨架、时间线、素材入库与检索、风格改写、一致性检查。  
但在真实业务场景下，还缺少一组关键中台能力：

- 章节生产流水线不完整（缺少草稿-定稿-发布状态流）
- 角色关系只有“静态图”，缺少“关系随章节变化”的追踪
- 借鉴程度无法量化与预警（合规风险点）
- 去 AI 感没有可执行的质检指标
- 素材检索仍偏“全文搜索”，缺少段落级/剧情级/人物级索引
- 素材标签体系尚未规范化（同义词、层级、冲突标签）

---

## 2) 建议新增业务模块

### A. 章节生产管理（P0）✅ 已实现

**目标**：把章节写作变成可追踪流程，而不是单次生成。

新增能力：

- 章节状态机：`idea -> outline -> draft -> revise -> final -> published`
- 章节元数据：目标字数、视角角色、剧情目的、冲突类型、伏笔埋设/回收
- 章节看板：按状态查看章节积压和风险章节

建议新增文件：

- `projects/{name}/chapters/index.yaml`
- `projects/{name}/chapters/{chapter_id}.md`

建议新增命令：

- `/chapter-create [章节号] [一句话目标]`
- `/chapter-update [章节号] --status [状态]`
- `/chapter-board [--status 状态]`
- `/chapter-review [章节号]`（结构、节奏、角色行为一致性）

---

### B. 角色关系演进（P0）✅ 已实现

**目标**：关系不只“是什么”，还要知道“何时变化、为何变化”。

新增能力：

- 关系事件日志：在第几章、因为什么事件，关系从 A 变到 B
- 关系强度分值：如 `[-5, +5]`，可随剧情变更
- 单角色关系时间线：辅助写“人物弧光”

建议新增文件：

- `projects/{name}/characters/relations.yaml`（当前关系快照）
- `projects/{name}/characters/relation_events.yaml`（变更日志）

建议新增命令：

- `/relationship-log [角色1] [角色2] [变化描述] --chapter [章节号]`
- `/relationship-evolution [角色名]`
- `/relationship-check`（检测“前章死敌后章无理由并肩”等跳变）

---

### C. 借鉴程度与合规防线（P0）✅ 已实现

**目标**：允许借鉴，但可量化、可解释、可追溯。

新增能力：

- 借鉴登记：每章声明参考素材来源、借鉴维度（设定/节奏/桥段/表达）
- 风险评分：段落级相似风险、表达复用风险、桥段复用风险
- 改写建议：给出“改设定、改冲突、改叙事顺序”的降重建议

建议新增文件：

- `projects/{name}/compliance/inspiration_log.yaml`
- `projects/{name}/compliance/risk_report.yaml`

建议新增命令：

- `/inspiration-log [章节号] [素材ID] [借鉴点]`
- `/inspiration-check [章节号]`
- `/inspiration-report [范围]`

---

### D. 去 AI 感质量工程（P0）✅ 已实现

**目标**：把“感觉像 AI”变成可检查项，而不靠主观争论。

新增能力（评分维度）：

- 句式重复率（连续短句、并列句模板化）
- 高频套话密度（如“不由得”“仿佛”“这一刻”等）
- 叙事机械感（同节奏段落重复）
- 对话人格区分度（角色说话风格是否同质）

建议新增文件：

- `shared/styles/anti_ai_rules.yaml`
- `projects/{name}/quality/ai_trace_report.yaml`

建议新增命令：

- `/anti-ai-check [章节号]`
- `/anti-ai-rewrite [章节号] --level [1-3]`
- `/voice-check [角色名] [章节范围]`

---

### E. 素材标签治理（P1）➡️ 属于 novel-material 项目

**目标**：标签可复用、可检索、可统计，而不是自由文本堆积。

新增能力：

- 标签字典（规范名、别名、禁用词）
- 层级标签：题材/情绪/场景/人物原型/冲突类型
- 自动打标 + 人工确认闭环

建议新增文件：

- `../novel-material/data/tags.yaml`（素材库独立项目）
- `../novel-material/data/index.yaml`（补充 `normalized_tags` 字段）

建议新增命令：

- `/tag-add [标签] --alias [别名] --group [分组]`
- `/tag-merge [旧标签] [新标签]`
- `/material-retag [素材ID] [标签...]`

---

### F. 素材分段与剧情索引（P1）➡️ 属于 novel-material 项目

**目标**：从“素材级搜索”升级为“片段级检索与复用”。

新增能力：

- 分段切片：按段落/场景切分素材
- 片段指纹：记录主题、情绪、冲突、角色、场景、时间
- 剧情索引：素材片段可映射到“起-承-转-合/三幕/爽点节奏”

建议新增文件：

- `../novel-material/data/chunks/{material_id}.yaml`
- `../novel-material/data/plot_index.yaml`

建议新增命令：

- `/material-chunk [素材ID]`
- `/material-index-plot [素材ID]`
- `/material-search-plot [剧情需求描述]`

---

### G. 素材人物索引（P1）➡️ 属于 novel-material 项目

**目标**：快速找到“某类人物写法”，避免角色塑形同质化。

新增能力：

- 人物卡抽取：目标、动机、缺陷、转折点、口头禅、行为模式
- 人物原型标签：导师、野心家、破碎主角、反差喜剧等
- 同类人物对比：同素材内/跨素材比较

建议新增文件：

- `../novel-material/data/character_index.yaml`

建议新增命令：

- `/material-index-character [素材ID]`
- `/material-search-character [人物需求]`
- `/character-archetype-map [项目名]`

---

## 3) 推荐数据结构（最小可用版）

### `chapters/index.yaml`

```yaml
chapters:
  - id: ch001
    title: 山村惊变
    status: draft
    pov: 张三
    goal: 建立危机并触发离村
    word_target: 3000
    word_actual: 2780
    hooks_planted: [hook_001]
    hooks_revealed: []
    updated: 2026-04-01
```

### `../novel-material/data/chunks/{material_id}.yaml`

```yaml
material_id: nm_novel_20260404_a1b2
chunks:
  - chunk_id: c001
    text_ref: "第12-18段"
    summary: 初遇冲突，强弱对比
    tags: [冲突升级, 人物初见]
    mood: 紧张
    plot_role: 第一幕-诱因
    characters: [主角, 反派]
```

### `projects/{name}/compliance/risk_report.yaml`

```yaml
chapter: ch003
overall_risk: medium
risk_items:
  - type: expression_similarity
    level: high
    evidence: "与素材 mat_012 在关键句式上连续重合"
    suggestion: "调整句法并替换比喻源域"
```

---

## 4) KPI 口径定义（建议）

> 用于 `/novel-kpi` 与 `/project-weekly-report` 的统一统计口径，避免“同指标不同算法”。

| 指标 | 定义口径 | 计算方式（建议） | 数据来源 |
|------|----------|------------------|----------|
| 连续更新率 | 统计范围内有“新增章节/状态推进/正文更新”记录的天数占比 | `活跃天数 / 范围总天数` | `chapters/index.yaml` + 章节更新时间 |
| 完稿率 | 状态为 `final` 或 `published` 的章节占比 | `完稿章节数 / 总章节数` | `chapters/index.yaml` |
| 返工率 | 进入 `revise` 状态的章节占比 | `revise章节数 / 总章节数` | `chapters/index.yaml` |
| 借鉴风险消解率 | 高借鉴风险章节中已完成修复的比例 | `已修复高风险章节 / 高风险章节总数` | `compliance/risk_report.yaml` |
| AI痕迹消解率 | AI高风险章节中已改写并复检通过的比例 | `已消解章节 / AI高风险章节总数` | `quality/ai_trace_report.yaml` |
| 关系冲突修复率 | 检出的关系跳变问题中已补桥接事件的比例 | `已修复关系问题 / 关系问题总数` | `characters/relation_events.yaml` + 关系检查结果 |
| 借鉴登记覆盖率 | 已登记借鉴信息的章节占比 | `有登记章节数 / 实际创作章节数` | `compliance/inspiration_log.yaml` + `chapters/index.yaml` |
| 素材复用集中度 | Top1素材被引用次数占总引用次数比例 | `Top1引用次数 / 总引用次数` | `compliance/inspiration_log.yaml` |

口径约束建议：

- 统一“分母口径”：章节相关指标默认以 `chapters/index.yaml` 中范围内章节为分母
- 缺失数据不补零：标记为 `N/A` 并给出补录建议
- 周报与 KPI 共用同一口径表，防止数字打架

---

## 5) 实施优先级（建议）

**2026-04 更新**：第 1-2 阶段已全部完成。第 3 阶段属于 novel-material 项目。

- ~~**第1阶段（1周）**：章节状态机、关系演进日志、去 AI 感检查~~ ✅
- ~~**第2阶段（1周）**：借鉴合规检查、标签字典治理~~ ✅
- **第3阶段（1-2周）**：素材分段索引、剧情索引、人物索引 → novel-material 项目

---

## 6) 第一批应新增的 Skill（建议名）

**2026-04 更新**：前四行已全部实现，后两行属于 novel-material 项目。

- ~~`/chapter-create` `/chapter-update` `/chapter-board` `/chapter-review`~~ ✅
- ~~`/relationship-log` `/relationship-evolution` `/relationship-check`~~ ✅
- ~~`/inspiration-log` `/inspiration-check` `/inspiration-report`~~ ✅
- ~~`/anti-ai-check` `/anti-ai-rewrite` `/voice-check`~~ ✅
- `/tag-add` `/tag-merge` `/material-retag` → novel-material
- `/material-chunk` `/material-index-plot` `/material-index-character` → novel-material

这些技能优先覆盖“写得出来 + 写得稳 + 风险可控 + 素材可复用”四个核心目标。

