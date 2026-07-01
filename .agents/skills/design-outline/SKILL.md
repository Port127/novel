---
name: design-outline
description: 大纲设计。交互式设计故事走向、结构规划、节奏检测。
---

# design-outline（大纲设计）

> **用途**：设计小说的整体故事大纲，包括幕/序列/节拍结构、节奏曲线、伏笔网络。
> **前置条件**：
> - `settings/scout_report.yaml` 存在（品类已确定）
> - `settings/worldbuilding.yaml` 存在（世界观已完成）
> - `settings/characters.yaml` 存在（人设已完成，可选但推荐）
> **输出文件**：`settings/outline.yaml`、`settings/arcs.yaml`、`settings/pacing.yaml`、`settings/notes.yaml`

---

## 核心原则 (Core Principles)

1. **防暴走与启发式交互 (UX)**：严禁一次性执行多个 Phase 或连发开放式提问。每个 Phase 结束前必须停下等待用户。提问时必须基于上下文提供 **2-3 个具体预设方案 (Option A/B/C)** 供用户选择或微调。
2. **多智能体编排 (Orchestration)**：大纲搭建中，主 Agent 负责流程统筹与落盘，重度脑暴环节必须唤醒 `story-architect` 辅助。
3. **商业对齐 (Commercial Alignment)**：必须基于 `scout_report.yaml` 的结构要求设计，刻意制造差异化。
4. **素材库联动 (Ecosystem)**：缺乏灵感时，主动向用户推荐使用 `/nm` 查询上游素材库中的大纲或情节模式。
5. **上下文闭环 (Context Loop)**：生成大纲前，必须强制读取对应的大纲 Schema（outline.schema.yaml），保证最终输出能通过结构校验。
6. **实时进度保存 (State Persistence)**：进入任何新的 Phase，必须立即更新根目录下的 `_progress.md` 文件。

### 业务核心规则
7. **结构类型匹配**：根据 `scout_report.yaml` 的 `required_elements.structure.type` 选择结构框架（三幕式/起承转合/英雄之旅）。
8. **品类感知**：不同品类的节奏模式、高潮密度、伏笔风格不同。
9. **嵌套结构**：全书 → 幕（Act）→ 序列（Sequence）→ 节拍（Beat），层层细化。
10. **节奏优先**：大纲阶段就要检测节奏问题，避免写到中期崩盘。
11. **伏笔可追踪**：每个伏笔有明确的埋设章节和回收章节。
12. **高潮驱动**：先定高潮再倒推结构（参考 `references/plot-core-methods.md`「高潮逆推法」），高潮是情绪峰值而非事件峰值。
13. **五项驱动**：每章/每卷必须至少满足压迫感/实力感/认知颠覆/资源升值/悬念增殖之一，否则章节无存在价值。
14. **AB 交织**：A 线升级感 + B 线冲突，交替推进，不能连续 3 章只有单线。

---

## Phase 定义 (Phase State Machine)

> **【架构强制要求】**：
> 1. 生成任何结构化数据前，**必须使用 `view_file` 强制读取对应的 `data/schemas/outline.schema.yaml`**。
> 2. 严禁按己意图捏造不在 Schema 中的顶级字段。
> 3. Reference 文件应当按需在具体的 Phase 中加载，不要一次性全读完。

### Phase 1：品类适配与结构选择

**入口条件**：scout_report.yaml + worldbuilding.yaml 存在
**目标**：根据品类和结构类型加载对应框架

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 1。
2. **强制读取 Schema**：使用 `view_file` 读取本次目标输出对应的 `data/schemas/outline.schema.yaml`。
3. 读取 `scout_report.yaml` 的 `genre` 和 `required_elements.structure`
4. 确定结构类型：
   - `三幕式`（默认）：适合大多数品类
   - `起承转合`：适合言情、都市日常
   - `英雄之旅`：适合玄幻、冒险
5. 读取 `references/outline-structure.md`，加载对应结构模板
6. 读取 `references/plot-frameworks.md`，加载品类对应的剧情框架
7. **高潮逆推**（参考 `references/plot-core-methods.md`「高潮逆推法与AB粗纲」）：
   - 先确定全书/全卷最终的情绪峰值
   - 从高潮倒推 2-5 个独立的戏剧单元（目标-阻碍-行动-代价）
   - 连接单元间的因果链和升级路径
8. **噱头与开篇定位**（参考 `references/plot-core-methods.md`「噱头分类与开篇流程」）：
   - 确定全书核心噱头类型
   - 开篇如何在 3 章内建立核心冲突和期待感
9. 展示结构方案和总章数/卷数建议
10. **启发式提问**：向用户展示 2-3 个结构方案 (Option A/B/C) 供选择。
11. **停顿确认**：等待用户确认整体规划后，再进入下一阶段。

**出口条件**：结构类型和总体框架已确定
**加载 References**：`outline-structure.md`、`plot-frameworks.md`、`plot-core-methods.md`

---

### Phase 2：骨架搭建（幕级/卷级规划）

**入口条件**：结构类型已确定
**目标**：完成幕级/卷级大纲

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 2。
2. 根据结构类型生成幕级骨架
3. 为每幕/每卷确定：幕名称、章节范围、核心冲突、转折点、主角状态变化
4. **卷级大纲模板**（每卷必须按此格式填写）：

```markdown
### 第X卷：{卷名}（约 {N} 万字，{M} 章）
- 功能：{铺垫/起步/第一个大爽点/中期升级/终极决战}
- 核心事件：{一句话概括本卷核心事件}
- 核心冲突：{本卷主要矛盾}
- 起始状态 → 结束状态：{主角从 {A} 变成 {B}}
- 对标结构坐标：{1/4 中点 3/4 关键情节锚点}
- 情绪弧线：{起点情绪 → 峰值 → 终点情绪}
- 本卷高潮：{一句话描述本卷最大爽点/情绪峰值}
- 待埋设伏笔：{本卷需要新埋的伏笔列表}
- 待回收伏笔：{上一卷遗留需要回收的伏笔}
```

5. 读取 `references/tension-curve.md`，绘制幕级/卷级张力曲线
6. 读取 `references/plot-core-methods.md`「高潮构建公式」，为每卷设计高潮构建路径：
   - **蓄能**：压力持续升级，读者期待值拉满
   - **假胜**：看似胜利在望（给读者短暂的满足感）
   - **崩解**：假胜被打破，更大的危机出现（情绪最低点）
   - **真胜/代价**：最终解决方案，但必须有代价
7. **启发式提问**：展示卷级大纲并提供优化建议或选项。
8. **停顿确认**：请用户确认通过。

**出口条件**：卷级大纲已确认，每卷高潮构建路径清晰
**加载 References**：`tension-curve.md`、`plot-core-methods.md`

---

### Phase 3：序列细化（序列级规划）

**入口条件**：卷级大纲已确认
**目标**：将每卷拆分为序列，完成序列级大纲

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 3。
2. 每卷拆分为 2-5 个序列（每个序列约 10-30 章）
3. 为每个序列确定：序列名称、章节范围、序列目标、序列小高潮、涉及角色
4. 读取 `references/pacing-guide.md`，检查序列间的快慢交替
5. 读取 `references/foreshadowing-guide.md`，规划伏笔的埋设与回收位置
6. **连续性追踪**（参考 `references/plot-core-methods.md`「连续性追踪与节奏管理」）：
   - 检查序列间的因果链是否连贯
   - 检查角色状态在序列间是否连续
   - 检查伏笔密度是否合理（不能连续 3 个序列无伏笔操作）
7. **启发式提问**：展示序列级大纲，询问用户是否需要增加转折或调整序列目标。
8. **停顿确认**：请用户确认通过。

**出口条件**：序列级大纲已确认
**加载 References**：`pacing-guide.md`、`foreshadowing-guide.md`、`plot-core-methods.md`

---

### Phase 4：节拍填充（节拍级规划）

**入口条件**：序列级大纲已确认
**目标**：为关键序列填充节拍

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 4。
2. 为每个序列设计 3-8 个节拍
3. 每个节拍包含：节拍编号、名称、所在章节、事件描述、张力值（1-5）、涉及伏笔操作
4. **反转设计**（参考 `references/reversal-toolkit.md`）：
   - 为关键节拍选择反转类型（7 种：身份/视角/动机/时间线/信息/认知/无反转）
   - 嵌套反转设计：反转 A 引出反转 B，B 的真正代价在反转 C
   - 误导技巧：选择性叙述/情绪引导/假线索/刻板印象利用
   - 反转自检：合理性（≥3 处暗示）、冲击力、公平性、节奏
5. 标记待验证的节奏问题；若 `settings/pacing.yaml` 已在本阶段落盘或更新，可运行 `node .agents/skills/design-outline/scripts/check-pacing.js settings/pacing.yaml` 做预检。
6. 根据节奏自检或预检结果调整节拍，最终以 Phase 5 写入文件后的脚本门禁为准。
7. **启发式提问**：展示关键节拍的反转设计，提供修改选项。
8. **停顿确认**：请用户确认节拍级大纲通过。

**出口条件**：节拍级大纲已确认，细纲蓝图完整，节奏检测通过
**加载 References**：`reversal-toolkit.md`、`plot-core-methods.md`

#### Agent 调用：story-architect（可选增强）

如果项目已部署 story-architect agent（检查 `.agents/agents/story-architect.md` 是否存在），
可读取该文件内容，拼接以下参数后 spawn Agent 辅助大纲优化：

- 项目根目录：{当前项目绝对路径}
- 任务类型：结构优化
- 查询参数：审查大纲整体节奏与五项驱动连贯性；优化关键节拍的悬念与反转网络；绘制幕级/序列级张力曲线（不涉及单章细纲）
- 相关文件路径：settings/outline.yaml, settings/arcs.yaml, settings/pacing.yaml

如 agent 不可用，跳过此步，直接进入 Phase 5。

---

### Phase 5：落盘验证 (Quality Gate)

**入口条件**：所有层级大纲已确认
**目标**：生成输出文件并验证

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 5。
2. **最终检查**：汇总大纲数据，审查是否严格符合 `outline.schema.yaml` 结构。
3. **写入文件**：
   - 写入 `settings/outline.yaml`
   - 写入 `settings/arcs.yaml`
   - 写入 `settings/pacing.yaml`
   - 写入 `settings/notes.yaml`（必须按 `data/schemas/notes.schema.yaml` 初始化，至少包含 `tracking.recent_chapters`、`tracking.ten_chapter_summaries`、`tracking.volume_overview`、`tracking.character_states`、`tracking.foreshadowing` 和 `preferences` 节点）
4. **门禁校验**：
   - 运行 `node .agents/skills/design-outline/scripts/check-outline.js settings/scout_report.yaml settings/outline.yaml` 验证结构完整性
   - 运行 `node .agents/skills/design-outline/scripts/check-pacing.js settings/pacing.yaml` 验证节奏无问题
5. **对标节奏校验**（如有对标书）：
   - 1/4 处是否锚定第一个关键情节
   - 中点是否有重大转折或认知颠覆
   - 3/4 处是否有终极决战前的最后准备
6. **五项驱动分布检查**：
   - 连续 3 章是否有同类型定位？
   - 低压+过场章占比是否 ≤15%？
   - 每章是否至少满足一项驱动？
7. **门禁阻断**：根据脚本输出（如 `[blocking]`），如有阻断性错误必须退回修正。
8. 验证通过后，清理 `_progress.md` 文件。

**出口条件**：三个输出文件已生成且通过验证
**加载 References**：无

---

## 质量门禁

### 大纲五检（每卷/每章设计前必答）

1. **情绪交付**：本卷/本章交付什么情绪？什么剧情模式能可靠交付？
2. **核心冲突**：本卷/本章核心冲突是什么？
3. **卷节奏**：起承转合哪段加速哪段减速？
4. **伏笔管理**：本卷需要新埋设的伏笔有哪些？上一卷待回收的伏笔如何处理？
5. **章节定位分布**：高压/推进/低压/关系章的分布是否有层次？低压+过场是否克制（合计 ≤15%）？

### 脚本检测

| 检查项 | 工具 | 说明 |
|--------|------|------|
| 结构完整性 | check-outline.js | 根据结构类型检查幕/序列/节拍是否完整 |
| 节奏健康度 | check-pacing.js | 检测连续慢章、高潮间距过大等问题 |
| 伏笔闭合 | check-outline.js | 检查所有伏笔是否已安排回收 |
| 五项驱动 | check-outline.js | 每章至少满足一项驱动检查 |

---

## 断点恢复 (Recovery)

**状态文件**：`_progress.md`（位于项目根目录）

**格式范例**：
```markdown
# design-outline Progress
- current_phase: <1-5>
- status: in_progress | completed
- last_updated: <timestamp>
```

**恢复逻辑**：
- 启动时检查 `_progress.md`。
- 若状态非 completed，主动询问用户是否继续中断的进度，跳到对应的 current_phase。

---

## 输出文件

- `settings/outline.yaml`：主大纲（幕/序列/节拍三层结构）
- `settings/arcs.yaml`：叙事弧线（卷/弧级别，含高潮构建路径）
- `settings/pacing.yaml`：节奏曲线（章节级张力标注）
- `settings/notes.yaml`：状态追踪与备忘（伏笔记录/角色状态）

`data/schemas/outline.schema.yaml` 只约束 `settings/outline.yaml` 的主结构。`settings/arcs.yaml` 和 `settings/pacing.yaml` 由对应模板、`check-pacing.js` 与本 Skill 文档共同约束；`settings/notes.yaml` 必须遵循 `data/schemas/notes.schema.yaml`。若后续发现 `arcs/pacing` 被多个 Skill 共同读写且字段含义继续扩展，应单独设计 dedicated schema。

**输出文件格式**：

```yaml
# outline.yaml 示例结构
structure:
  type: 三幕式  # 或 起承转合/英雄之旅
  total_chapters: 300
  total_volumes: 5

volumes:
  - volume: 1
    name: 卷名
    chapters: [1, 60]
    function: 铺垫
    core_event: 一句话
    start_state: 主角初始状态
    end_state: 卷末状态

sequences:
  - sequence: 1
    volume: 1
    chapters: [1, 20]
    goal: 序列目标
    mini_climax: 序列小高潮

beats:
  - beat: 1
    chapter: 1
    event: 事件描述
    tension: 3  # 1-5
    foreshadow: 埋设/回收/无
```

---

## 大纲粒度指引

不同阶段使用不同粒度：

| 粒度 | 适用场景 | 包含内容 | 详细程度 |
|------|---------|---------|---------|
| **全书骨架** | 题材定位阶段 | 总卷数、总章数、核心冲突、终极高潮 | 极简 |
| **卷级大纲** | Phase 2 | 每卷功能、核心事件、起止状态、高潮路径 | 中等 |
| **序列大纲** | Phase 3 | 每序列目标、小高潮、伏笔规划、角色弧线 | 较详 |
| **节拍大纲** | Phase 4 | 每节拍事件、张力值、伏笔操作 | 详细 |

**原则**：从粗到细，逐层细化。上层未确认不进入下层。

---

## References 索引

| Phase | References | 用途 |
|-------|-----------|------|
| 1 | outline-structure.md、plot-frameworks.md、plot-core-methods.md | 结构方法论 + 品类剧情框架 + 高潮逆推/噱头分类 |
| 2 | tension-curve.md、plot-core-methods.md | 幕级张力曲线 + 高潮构建公式 |
| 3 | pacing-guide.md、foreshadowing-guide.md、plot-core-methods.md | 节奏设计 + 伏笔规划 + 连续性追踪 |
| 4 | reversal-toolkit.md、plot-core-methods.md | 反转设计 + 细纲蓝图 |
| 5 | — | 落盘验证 |

---

## 下一步 (Next Steps)

大纲完成后，可进入：
- `/design-chapters`：根据大纲生成的节拍表，进一步执行单章细纲的详尽设计。
- `/paywall-design`：付费卡点与过渡节奏设计（可选）。

---

## 数据输出范式示例 (可选，但必须合规)

> ⚠️ **警告**：大模型往往会优先模仿当前上下文中的示例。此处示例必须 100% 贴合目标 Schema。

```yaml
# outline.yaml 示例：
premise: "核心前提..."
theme: ["成长", "复仇"]
acts:
  - act: 1
    title: "第一幕"
    chapters: [1, 20]
    sequences:
      - sequence: 1
        title: "序列1"
        chapters: [1, 10]
        beats:
          - beat: 1
            title: "节拍1"
            chapter: 1
            description: "..."
            tension: 3
```

---

## 大纲常见错误速查

| 错误类型 | 表现 | 修正方法 | 参考 |
|---------|------|---------|------|
| 高潮缺失 | 全卷无明确情绪峰值 | 先定高潮再倒推结构 | plot-core-methods.md |
| 节奏崩塌 | 连续 5 章以上同类型定位 | 按高压→低压→推进交替排列 | pacing-guide.md |
| 伏笔遗忘 | 埋了伏笔但无回收计划 | 每个伏笔标注回收章节 | foreshadowing-guide.md |
| 反转无力 | 反转无铺垫或无冲击力 | 确保 ≥3 处暗示，用自检清单验证 | reversal-toolkit.md |
| 章节空转 | 章节不满足五项驱动任一 | 删除或重新设计章节功能 | plot-core-methods.md |
| AB 线断裂 | 连续 3 章只有单线推进 | 重新设计交织节奏 | plot-core-methods.md |
| 细纲过薄 | 缺少内容概括/情节安排/人物关系 | 按细纲蓝图模板补齐 | — |
| 对标失调 | 1/4·中点·3/4 无关键情节锚点 | 重新调整章节定位分布 | — |
