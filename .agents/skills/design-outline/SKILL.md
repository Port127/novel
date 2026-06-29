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
> **输出文件**：`settings/outline.yaml`、`settings/arcs.yaml`、`settings/pacing.yaml`

---

## 核心原则

1. **结构类型匹配**：根据 `scout_report.yaml` 的 `required_elements.structure.type` 选择结构框架（三幕式/起承转合/英雄之旅）。
2. **品类感知**：不同品类的节奏模式、高潮密度、伏笔风格不同。
3. **嵌套结构**：全书 → 幕（Act）→ 序列（Sequence）→ 节拍（Beat），层层细化。
4. **节奏优先**：大纲阶段就要检测节奏问题，避免写到中期崩盘。
5. **伏笔可追踪**：每个伏笔有明确的埋设章节和回收章节。

---

## Phase 定义

### Phase 1：品类适配与结构选择

**入口条件**：scout_report.yaml + worldbuilding.yaml 存在
**目标**：根据品类和结构类型加载对应框架

**步骤**：
1. 读取 `scout_report.yaml` 的 `genre` 和 `required_elements.structure`
2. 确定结构类型：
   - `三幕式`（默认）：适合大多数品类
   - `起承转合`：适合言情、都市日常
   - `英雄之旅`：适合玄幻、冒险
3. 读取 `references/outline-structure.md`，加载对应结构模板
4. 读取 `references/plot-frameworks.md`，加载品类对应的剧情框架
5. 展示结构方案和总章数/卷数建议
6. 确认整体规划

**出口条件**：结构类型和总体框架已确定
**加载 References**：`outline-structure.md`、`plot-frameworks.md`

---

### Phase 2：骨架搭建（幕级规划）

**入口条件**：结构类型已确定
**目标**：完成幕级大纲

**步骤**：
1. 根据结构类型生成幕级骨架
2. 为每幕确定：幕名称、章节范围、核心冲突、转折点、主角状态变化
3. 读取 `references/tension-curve.md`，绘制幕级张力曲线
4. 展示幕级大纲，请用户确认

**出口条件**：幕级大纲已确认
**加载 References**：`tension-curve.md`

---

### Phase 3：序列细化（序列级规划）

**入口条件**：幕级大纲已确认
**目标**：将每幕拆分为序列，完成序列级大纲

**步骤**：
1. 每幕拆分为 2-5 个序列（每个序列约 10-30 章）
2. 为每个序列确定：序列名称、章节范围、序列目标、序列小高潮、涉及角色
3. 读取 `references/pacing-guide.md`，检查序列间的快慢交替
4. 读取 `references/foreshadowing-guide.md`，规划伏笔的埋设与回收位置
5. 展示序列级大纲，请用户确认

**出口条件**：序列级大纲已确认
**加载 References**：`pacing-guide.md`、`foreshadowing-guide.md`

---

### Phase 4：节拍填充（节拍级规划）

**入口条件**：序列级大纲已确认
**目标**：为关键序列填充节拍

**步骤**：
1. 为每个序列设计 3-8 个节拍
2. 每个节拍包含：节拍编号、名称、所在章节、事件描述、张力值（1-5）、涉及伏笔操作
3. 运行 `scripts/check-pacing.js` 检测节奏问题
4. 根据检测结果调整节拍
5. 展示节拍级大纲，请用户确认

**出口条件**：节拍级大纲已确认且节奏检测通过
**加载 References**：无

#### Agent 调用：story-architect（可选增强）

如果项目已部署 story-architect agent（检查 `.agents/agents/story-architect.md` 是否存在），
可读取该文件内容，拼接以下参数后 spawn Agent 辅助大纲优化：

- 项目根目录：{当前项目绝对路径}
- 任务类型：审查
- 查询参数：审查当前大纲的结构完整性、钩子质量、反转设计、情绪弧线
- 相关文件路径：settings/outline.yaml, settings/arcs.yaml, settings/pacing.yaml

如 agent 不可用，跳过此步，直接进入 Phase 5。

---

### Phase 5：落盘验证

**入口条件**：所有层级大纲已确认
**目标**：生成输出文件并验证

**步骤**：
1. 汇总所有大纲数据
2. 写入 `settings/outline.yaml`
3. 写入 `settings/arcs.yaml`
4. 写入 `settings/pacing.yaml`
5. 运行 `scripts/check-outline.js` 验证结构完整性
6. 运行 `scripts/check-pacing.js` 验证节奏无问题
7. 清理 `_progress.md`

**出口条件**：三个输出文件已生成且通过验证
**加载 References**：无

---

## 质量门禁

| 检查项 | 工具 | 说明 |
|--------|------|------|
| 结构完整性 | check-outline.js | 根据结构类型检查幕/序列/节拍是否完整 |
| 节奏健康度 | check-pacing.js | 检测连续慢章、高潮间距过大等问题 |
| 伏笔闭合 | check-outline.js | 检查所有伏笔是否已安排回收 |

---

## 断点恢复

**状态文件**：`_progress.md`
**格式**：同 scout-topic
**恢复逻辑**：跳到最后一个 in_progress 的 Phase

---

## 输出文件

- `settings/outline.yaml`：主大纲
- `settings/arcs.yaml`：叙事弧线（卷/弧级别）
- `settings/pacing.yaml`：节奏曲线（章节级张力标注）

---

## References 索引

| Phase | References | 用途 |
|-------|-----------|------|
| 1 | outline-structure.md、plot-frameworks.md | 结构方法论 + 品类剧情框架 |
| 2 | tension-curve.md | 幕级张力曲线设计 |
| 3 | pacing-guide.md、foreshadowing-guide.md | 节奏设计 + 伏笔规划 |
| 4 | — | 节拍填充 + 节奏检测 |
| 5 | — | 落盘验证 |

---

## 下一步

大纲完成后，可进入：
- `/golden-chapters`：黄金三章设计
- `/paywall-design`：付费墙设计
- `/design-chapters`：细纲设计
