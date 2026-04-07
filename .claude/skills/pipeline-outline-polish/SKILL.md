---
name: pipeline-outline-polish
description: 审查并补强现有大纲，联动世界观与一致性检查，输出更稳的剧情骨架与下一步写作任务。用于用户已有 outline，但想优化结构、节奏、转折或设定支撑时。
when_to_use: 用户已有大纲，想优化大纲、世界观支撑或剧情节奏
argument-hint: "[优化重点]"
arguments: focus
---

# 任务

把现有大纲从“能看”补强到“可继续展开写作”，必要时同步更新 `outline.md` 与 `outline.yaml`。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 读取 `{current_path}/plot/outline.md`
3. 若存在，读取 `{current_path}/plot/outline.yaml`
4. 读取 `{current_path}/worldbuilding/setting.md`
5. 若存在，读取 `{current_path}/worldbuilding/worldbuilding.yaml`
5b. 若存在，读取 `{current_path}/worldbuilding/entries/` 下的设定条目（尤其是 status: confirmed 的）
5c. 若存在，读取 `{current_path}/ingestion_brief.md`（获取原始素材理解）
6. 若存在，读取 `{current_path}/timeline/main.yaml`
7. 若存在，读取 `{current_path}/chapters/index.yaml`
8. 若存在，读取 `{current_path}/characters/*.yaml`（重点：`fatal_flaw`、`obsession`、`soft_spot`、`misbelief`、`tragedy_trigger`）
9. 若存在，读取 `{current_path}/characters/relations.yaml` 与 `{current_path}/characters/relation_events.yaml`（核对关系机制与大纲转折是否同频）

## 输入参数

- `$0+` (focus): 可选优化重点，如“中段偏松”“反派动机不够”“世界规则支撑不足”

## 执行步骤

### 1. 做双重 review

先按 `/plot-review` 审查结构、节奏、伏笔，再按 `/worldbuilding-review` 审查设定支撑度。

### 2. 判断改动级别

只做下列两类改动：

- 局部补强：可直接更新
- 结构重排：先给预览并确认，再更新

结构重排包括：

- 幕次顺序调整
- 关键反转位置变化
- 伏笔回收节点整体后移或前移

### 3. 更新大纲

结合 `/plot-suggest` 的方法补强以下内容：

- 幕次弧线与关键转折
- 中点、危机、高潮的因果链
- 伏笔埋设与回收链路
- 与世界观、时间线有关的必要说明
- 主角/关键配角的缺陷、执念、误判是否在大纲里有兑现场景；关系 `dynamic` 与张力是否在关键幕次有对应事件

执行修改时：
- 修改已有节点 → 通过 `/plot-edit` 执行（会自动做影响分析）
- 新增节点 → 通过 `/plot-add` 执行
- 设定不足或需调整 → 通过 `/setting-edit` 或 `/setting-add` 处理

同步更新：

- `plot/outline.md` 的叙述性结构
- `plot/outline.yaml` 的 structure / foreshadowing / pacing_curve 等结构化字段

### 4. 做一次总体验证

按 `/consistency-check` 的口径做轻量回看，确认：

- 新增设定不与既有章节冲突
- 时间线没有新增硬冲突
- 大纲与已存在章节目标没有明显脱节

## 输出格式

```markdown
## CurrentState
- 阶段：可写大纲
- 已完成大纲补强
- 关注重点：{{focus}}

## Risks
- {{risk_1}}
- {{risk_2}}

## NextTasks
1. 细化最薄弱的一幕或一章
2. 补齐最关键的一条世界规则/势力关系
3. 将新增转折映射到章节计划
4. 若关系与角色卡已有字段，检查是否需补 `/relationship-log` 或 `/character-edit`

## RecommendedCommands
- /plot-edit {{node}} {{changes}}
- /setting-edit {{name}} --status confirmed
- /pipeline-setting-consolidate
- /pipeline-chapter-kickoff {{chapter_id}} {{goal}}
- /consistency-check
```

## 注意事项

- 优先补能直接影响写作推进的结构问题
- 不把世界观优化做成百科扩写
- 若已写章节很多，优先避免“优化大纲导致已写正文报废”
