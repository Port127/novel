---
name: scout-topic
description: 品类选择 + 选题分析。开新书或找题材时使用。
---

# scout-topic（选题侦察）

> **用途**：帮助用户选择品类、分析目标平台、制定选题策略。
> **前置条件**：项目已创建（`novel new` 或已有项目目录）。
> **输出文件**：`settings/scout_report.yaml`

---

## 核心原则 (Core Principles)

1. **防暴走与启发式交互 (UX)**：严禁一次性执行多个 Phase 或连发开放式提问。每个 Phase 结束前必须停下等待用户。提问时必须基于上下文提供 **2-3 个具体预设方案 (Option A/B/C)** 供用户选择或微调。不可越俎代庖替用户做决定。
2. **多智能体编排 (Orchestration)**：在选题决策环节（Phase 3），主 Agent 必须使用 `invoke_subagent` 唤醒 `story-architect` 子代理进行头脑风暴交互。
3. **实时保存进度 (State Persistence)**：每进入一个新的 Phase，必须立即更新项目根目录下的 `_progress.md` 的 `current_phase`。
4. **数据驱动与商业对齐 (Commercial Alignment)**：基于平台榜单数据和品类分析，同质化方向不选，必须有差异化定位。样本不足给"中"，不给"高"。
5. **素材库联动 (Ecosystem)**：在选题阶段可主动推荐用户使用 `/nm` 系列命令查询素材库热门设定。

---

## Phase 定义 (Phase State Machine)

> **【架构强制要求】**：
> 1. 生成任何结构化数据前，**必须使用 `view_file` 强制读取对应的 `data/schemas/*.schema.yaml`**。
> 2. 严禁按己意图捏造不在 Schema 中的顶级字段。
> 3. Reference 文件应当按需在具体的 Phase 中加载，不要在 Phase 1 一次性全读完。

### Phase 1：品类定位

**入口条件**：项目已创建
**目标**：确定品类（玄幻/都市/系统/言情/其他）

**步骤**：
1. **进度更新**：更新项目根目录 `_progress.md`，设置 `current_phase: 1`。
2. **强制读取 Schema**：使用 `view_file` 读取 `data/schemas/scout_report.schema.yaml`。
3. 读取 `references/genre-catalog.md`，向用户展示品类路由表。
4. **启发式交互**：提供 2-3 个品类方向（Option A/B/C）。
5. **停顿确认**：等待用户回复确认倾向的品类方向。
6. 根据用户回答，展示该品类的核心机制、结构节点、关键维度。
7. **停顿确认**：确认最终品类选择，记录到内存中（准备在最终写入 `scout_report.yaml` 时使用）。

**出口条件**：`genre` 字段已确认，用户确认进入下一阶段
**加载 References**：`genre-catalog.md`

---

### Phase 2：平台分析

**入口条件**：品类已确定
**目标**：确定目标平台 + 了解平台调性

**步骤**：
1. **进度更新**：更新项目根目录 `_progress.md`，设置 `current_phase: 2`。
2. 读取 `references/platform-profiles.md`，展示各平台特点。
3. **启发式交互**：推荐 2-3 个适合该品类的目标平台（番茄/起点/晋江/其他）供用户选择。
4. **停顿确认**：等待用户回复确认平台。
5. 展示该平台的目标读者画像、内容调性、付费模式。
6. **停顿确认**：确认最终平台选择，准备记录 `platform` 和 `target_audience`。

**出口条件**：`platform` 和 `target_audience` 字段已确认
**加载 References**：`platform-profiles.md`

---

### Phase 3：选题决策

**入口条件**：平台已确定
**目标**：基于品类+平台，产出具体的选题方向

**步骤**：
1. **进度更新**：更新项目根目录 `_progress.md`，设置 `current_phase: 3`。
2. 读取 `references/topic-decision.md`。
3. **编排指令**：[强制] 使用 `invoke_subagent` 工具唤醒 `story-architect`（故事架构师）进行多视角的选题头脑风暴与差异化评估。
4. **启发式交互**：按"选题四步"向用户提出 2-3 个（Option A/B/C）具体的选题方向：
   - 能爆的原因（先当假设）
   - 市场验证（榜单样本）
   - 差异化定位
   - 可行性 + 风险 + 验证动作
5. **停顿确认**：与用户多轮迭代探讨，直至用户 Accept。
6. 确认最终选题，准备写入 `premise` 和 `core_hooks`。

**出口条件**：`premise` 和 `core_hooks` 已确认
**加载 References**：`topic-decision.md`

---

### Phase 4：标签策略

**入口条件**：选题方向已确定
**目标**：制定标签组合策略

**步骤**：
1. **进度更新**：更新项目根目录 `_progress.md`，设置 `current_phase: 4`。
2. 读取 `references/tag-strategy.md`。
3. 分析目标品类的热门标签 + 竞争度。
4. **启发式交互**：设计 2-3 套标签组合（3-6 个主要标签 + 次要标签），向用户展示。
5. **停顿确认**：等待用户选择或确认最终标签策略。
6. 将当前草稿（包含 `recommended_tags.primary` 列表格式）临时写入 `settings/scout_report.yaml`。
7. **门禁校验**：执行终端命令验证标签：`node .agents/skills/scout-topic/scripts/check-tags.js settings/scout_report.yaml`。
8. 根据脚本输出的 `[blocking]` 或 `[advisory]` 信息，决定是否需要修正标签。如有冲突必须阻断重做并重新验证。

**出口条件**：标签组合已通过 `check-tags.js` 验证并获用户确认
**加载 References**：`tag-strategy.md`

---

### Phase 5：品类感知配置

**入口条件**：标签已确定
**目标**：引导用户填写 `required_elements`，供后续 skill 做质量门禁

**步骤**：
1. **进度更新**：更新项目根目录 `_progress.md`，设置 `current_phase: 5`。
2. 根据已选品类，向用户展示该品类的默认 `required_elements`（参考下表），提供是否增删的方案。
3. **停顿确认**：等待用户回复确认。
4. 根据确认结果准备 `required_elements` 数据。

**规范格式**：
必须严格遵循 Phase 1 读取的 Schema 生成 `required_elements` 字段，严禁层级错乱：
```yaml
required_elements:
  worldbuilding:
    required: [power_system, factions, locations]
  characters:
    protagonist: required
    mentor: required
    villain: required
  opening_hook:
    type: golden_finger
  structure:
    type: 三幕式
```

**品类默认值参考**：

| 品类 | worldbuilding.required | characters | opening_hook.type | structure.type |
|------|------------------------|------------|-------------------|----------------|
| xuanhuan | power_system, factions, locations | protagonist, mentor, villain | golden_finger | 三幕式 |
| urban | core_rules, locations, factions | protagonist, supporting_cast | conflict | 起承转合 |
| system | power_system, core_rules | protagonist, system_entity | golden_finger | 三幕式 |
| romance | locations, factions | protagonist, love_interest | meet_cute | 起承转合 |
| suspense | core_rules, locations | protagonist, suspect_pool | mystery_hook | 三幕式 |

**出口条件**：`required_elements` 已确认
**加载 References**：无（使用内置品类默认值）

---

### Phase 6：报告定稿

**入口条件**：所有字段已确认
**目标**：生成完整的 `scout_report.yaml`

**步骤**：
1. **进度更新**：更新项目根目录 `_progress.md`，设置 `current_phase: 6`。
2. **最终检查**：汇总所有字段，展示给用户进行最终确认。审查是否完全符合 Phase 1 中读取的 Schema 结构。
3. **停顿确认**：如有遗漏提示补充，等待用户最后 Accept。
4. **写入文件**：以完整合规的 YAML 格式覆盖写入 `settings/scout_report.yaml`。
5. 验证无误后，清理 `_progress.md` 文件（若存在），并向用户宣告本技能完成。

**出口条件**：`settings/scout_report.yaml` 已完整合规生成
**加载 References**：无

---

## 质量门禁 (Quality Gates)

本 skill 包含**自动化脚本检查门禁**：

- Phase 4 使用 `check-tags.js` 验证标签组合无冲突、无过度饱和。
- **拦截逻辑**：存在 `[blocking]` 级别冲突时必须阻断重做。
- Phase 5 结构约束：需要确保 `required_elements` 至少声明了 `worldbuilding`、`characters`、`opening_hook`、`structure`。

---

## 断点恢复 (Recovery)

**状态文件**：`_progress.md`（位于小说项目根目录）

**格式**：
```markdown
# scout-topic Progress
- current_phase: <1-6>
- status: in_progress | completed
- last_updated: <timestamp>
```

**恢复逻辑**：
- 启动时检查 `_progress.md`。
- 若存在且 status != completed，提示用户是否继续上次进度。
- 跳到对应的 current_phase 继续执行。
- **强制要求：每完成或进入一个新的 Phase，必须重新写入/更新 `_progress.md`。**
- **用户回退**：若用户在探讨中途推翻之前的决定并要求回退，请主动更新 `_progress.md` 的 `current_phase` 至对应的早期阶段并重新开始。

---

## 输出文件

- `settings/scout_report.yaml`：选题侦察报告（完整格式见 data/schemas/scout_report.schema.yaml）

---

## References 索引

| Phase | References | 用途 |
|-------|-----------|------|
| 1 | genre-catalog.md | 品类框架速查，选择品类 |
| 2 | platform-profiles.md | 平台画像，选择平台 |
| 3 | topic-decision.md | 选题决策方法论 |
| 4 | tag-strategy.md | 标签组合策略 |
| 5 | （内置默认值） | 品类感知配置 |
| 6 | — | 报告定稿 |

---

## 下一步 (Next Steps)

scout_report.yaml 生成后，可进入：
- `/worldbuilding`：世界观设计
- `/design-character`：人设设计
