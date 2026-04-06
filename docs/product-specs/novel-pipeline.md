# Novel Pipeline

面向“写作中常用流程编排”的产品规格。

`pipeline-*` 不是替代原子 skill，而是在现有 `plot-*`、`chapter-*`、`relationship-*`、`timeline-*`、`inspiration-*`、`anti-ai-*` 之上提供一层按场景组织的预设流程。

---

## 目标

- 让用户按“我要完成什么”而不是“我要记住哪些命令”来使用系统
- 把高频写作流程收束为少量可复用的预设
- 保持现有“小而专、可组合”的 skill 体系，不引入巨型单体命令

## 非目标

- 不替代底层原子 skill
- 不在 v1 引入独立任务系统或任务看板
- 不依赖本仓库尚未实现的 `material-*`、`tag-*` 命令

---

## 设计原则

### 1. 按用户意图命名

pipeline 名称应该直接对应用户目标，而不是内部实现顺序。

推荐命名模式：

- `pipeline-{artifact}-{goal}`
- `pipeline-{stage}-{handoff}`

命名要求：

- 使用小写和连字符
- 名称中体现产物或交付止点
- 避免 `pipeline-helper`、`pipeline-all-in-one` 这类宽泛名字

### 2. 按止点设计

每个 pipeline 必须明确结束于一个可交接状态，而不是“执行了一串命令”。

v1 统一止点：

- `可写大纲`
- `可开写章节`
- `可修订草稿`
- `可执行修复清单`
- `可发前闸口`

### 3. 薄编排，厚复用

pipeline 只负责：

- 识别前置条件
- 串联已有能力
- 决定执行顺序
- 汇总结果与下一步

具体的领域逻辑仍归属各原子 skill。

### 4. 先预览，再改大结构

如果 pipeline 会：

- 重排幕次
- 改变关键反转
- 移动重要伏笔回收
- 重写大量世界观规则

则先给出变更预览并请求确认，再执行正式写入。

---

## 标准输出契约

所有 `pipeline-*` 统一输出以下结构：

```markdown
## CurrentState
- 当前处于什么阶段
- 已完成哪些关键动作

## Risks
- 当前最重要的 1-3 个风险

## NextTasks
1. 下一步最该做什么
2. 如果有依赖，说明依赖关系
3. 给出最小可执行动作

## RecommendedCommands
- /xxx
- /yyy
```

说明：

- `CurrentState` 描述现状与本次落点
- `Risks` 只列当前最关键风险，不做泛泛罗列
- `NextTasks` 以轻量任务清单代替独立任务系统
- `RecommendedCommands` 作为用户后续手动接力入口

---

## Pipeline Catalog v1

| Pipeline | 目标 | 主要输入 | 触达文件 | 止点 | 依赖能力 |
|---|---|---|---|---|---|
| `pipeline-outline-bootstrap` | 从想法到可写大纲 | premise、结构类型 | `plot/outline.md` `plot/outline.yaml` | `可写大纲` | `plot-init` `plot-suggest` `plot-add` `timeline-check` |
| `pipeline-outline-polish` | 补强现有大纲 | 当前 outline、优化目标 | `plot/outline.md` `plot/outline.yaml` | `可写大纲` | `plot-review` `worldbuilding-review` `plot-suggest` `consistency-check` |
| `pipeline-chapter-kickoff` | 从章节想法到可开写章节 | 章节ID、一句话目标 | `chapters/*.md` `chapters/index.yaml` `plot/outline.md` | `可开写章节` | `chapter-create` `chapter-update` `plot-add` |
| `pipeline-draft-polish` | 从草稿到可修订稿 | 章节ID | `chapters/*.md` `chapters/index.yaml` `quality/ai_trace_report.yaml` | `可修订草稿` | `chapter-review` `voice-check` `anti-ai-check` `anti-ai-rewrite` |
| `pipeline-continuity-gate` | 生成连续性修复清单 | 检查范围 | `timeline/main.yaml` `characters/*` `plot/outline.md` `chapters/index.yaml` | `可执行修复清单` | `relationship-check` `timeline-check` `consistency-check` |
| `pipeline-compliance-gate` | 发布前完成借鉴留痕与风险审查 | 章节ID 或范围 | `compliance/inspiration_log.yaml` `compliance/risk_report.yaml` | `可发前闸口` | `inspiration-log` `inspiration-check` `inspiration-report` |

---

## Gap Review Skills

为避免把“大纲优化”和“世界观优化”挤进泛化检查器，v1 新增两个专用 review skill：

### `plot-review`

定位：

- 审查结构骨架、主线推进、转折分布、伏笔与节奏曲线
- 给出可直接落到 `outline.md` / `outline.yaml` 的优化建议

### `worldbuilding-review`

定位：

- 审查世界规则、力量体系、势力关系、地理与剧情支撑度
- 识别“设定很多但不服务情节”与“情节依赖设定但规则缺失”的问题

---

## 执行规则

### Outline 类

- 空白或极薄大纲：可直接补全
- 已有较完整大纲：先 review，再决定局部补强还是结构重排

### Chapter 类

- 允许直接更新章节状态与章节目标
- 仅在用户明确要求时进行整章重写

### Gate 类

- 以检查、归纳、排序修复优先级为主
- 不默认批量改写正文或大范围改设定

---

## 与现有体系的关系

- `README.md` / `README-AUTHOR.md`：面向用户的流程入口
- `docs/SPEC.md`：系统级命令与能力地图
- `.claude/skills/pipeline-*`：可直接调用的预设流程
- `.claude/skills/plot-review`、`.claude/skills/worldbuilding-review`：补齐 review 缺口

---

## 后续扩展

若用户对“创建任务 + 看板追踪”的需求稳定出现，再考虑新增：

- `task-create`
- `task-board`
- `pipeline-release-gate`

v1 先用 `NextTasks` 保持轻量。
