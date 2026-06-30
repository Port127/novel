---
name: worldbuilding
description: 世界观设计。与 Agent 交互讨论力量体系、社会结构、基础规则。
---

# worldbuilding（世界观设计）

> **用途**：设计小说的世界观设定，包括力量体系、社会结构、基础规则。
> **前置条件**：`settings/scout_report.yaml` 存在（品类已确定）。
> **输出文件**：`settings/worldbuilding.yaml`

---

## 核心原则 (Core Principles)

1. **品类适配**：不同品类的世界观重点不同（玄幻重力量体系，都市重时代背景）。
2. **自洽优先**：世界观必须内部自洽，不能有矛盾。
3. **服务于剧情**：世界观为剧情服务，不是为了设定而设定。
4. **品类感知**：根据 `scout_report.yaml` 的 `required_elements.worldbuilding` 决定设计重点。
5. **素材库联动**：如果遇到不熟悉的设定或需要寻找灵感，请务必主动使用 `/nm search world` 去素材库中检索同类参考。
6. **多智能体编排 (Orchestration)**：本技能的核心设计环节（Phase 2 至 Phase 4.5）中，主 Agent 必须使用 `invoke_subagent` 唤醒 `story-architect` 子代理，由其承担专业的架构师角色与用户进行头脑风暴，主 Agent 负责统筹和最终落盘。
7. **启发式交互原则 (UX)**：严禁向用户连续抛出开放式提问（如“您想怎么设计？”）。Agent 必须基于品类、故事简介及竞争分析，主动向用户提供 2-3 个富有创意的具体预设方案（Option A/B/C）供其选择或微调。

---

## Phase 定义 (Phase State Machine)

> **【架构强制要求】**：
> 1. 生成任何结构化数据前，**必须使用 `view_file` 强制读取对应的 `data/schemas/*.schema.yaml`**。
> 2. 严禁按己意图捏造不在 Schema 中的顶级字段。
> 3. Reference 文件应当按需在具体的 Phase 中加载，不要在 Phase 1 一次性全读完。

### Phase 1：品类适配

**入口条件**：scout_report.yaml 存在
**目标**：根据品类加载对应框架

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 1。
2. **强制前置动作**：使用 `view_file` 工具读取 `data/schemas/worldbuilding.schema.yaml`。在整个设定过程中，所有产出字段必须完全符合该 Schema 结构，严禁自创顶级字段。
3. 读取 `scout_report.yaml` 的 `genre` 和 `required_elements.worldbuilding`。
4. **商业对齐**：深入分析 `scout_report.yaml` 中的 `competition_analysis`（竞争分析）和 `core_hooks`（核心卖点）。在后续各 Phase 提供选项时，必须刻意制造差异化以避免同质化，确保世界观完美支撑设定的核心爽点。
5. 读取 `references/genre-worldbuilding.md`，加载品类对应框架。
6. 综合以上信息，向用户展示该品类需要设计的世界观要素。
7. **停顿确认**：等待用户确认设计范围后，再进入下一阶段。

**出口条件**：设计范围确定
**加载 References**：`genre-worldbuilding.md`

**品类框架示例**（所有要素必须映射至 `worldbuilding.schema.yaml` 的对应字段）：

| 品类 | 必需要素 | 重点 |
|------|---------|------|
| 玄幻 | power_system, factions, locations | 力量等级、宗门势力 |
| 都市 | core_rules, locations | 时代背景、社会规则（映射至 core_rules） |
| 系统 | power_system, core_rules | 系统规则（作为 power_system）、任务机制（映射至 core_rules） |
| 言情 | locations, factions | 场景、社交圈（映射至 factions 或 locations） |

---

### Phase 2：力量体系（如需要）

**入口条件**：`required_elements.worldbuilding.required` 包含 `power_system`
**目标**：设计力量体系

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 2。
2. 读取 `references/power-system-guide.md`
3. **编排指令**：[强制] 唤醒子 Agent `story-architect` 承接本阶段的具体交互设计。
4. **启发式交互**：Agent 必须基于 Phase 1 的商业对齐要求，给出 2-3 套（Option A/B/C）关于以下内容的力量体系组合方案：
   - 体系名称与等级划分（3-9 级为宜）
   - 升级条件与战斗表现
   - 限制与代价
5. **停顿确认**：与用户多轮迭代，直到本环节内容被用户确认。
6. 将确认的数据暂存于内存中，准备最后写入 worldbuilding.yaml 的 `power_system` 字段。

**出口条件**：`power_system` 设定完成并在内存中就绪
**加载 References**：`power-system-guide.md`

---

### Phase 3：社会结构（如需要）

**入口条件**：`required_elements.worldbuilding.required` 包含 `factions`
**目标**：设计社会结构

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 3。
2. 读取 `references/social-structure.md`
3. **编排指令**：[强制] 唤醒子 Agent `story-architect` 承接本阶段交互。
4. **启发式交互**：Agent 提供 2-3 套社会势力架构的预设方案（Option A/B/C），必须包含：
   - 主要势力（≥3 个）与势力关系（敌对/同盟/中立）
   - 剧情预留：**必须**为主角预留成长的舞台，确保势力间存在利益冲突。
5. **停顿确认**：与用户多轮迭代直到确认。
6. 数据暂存于内存中，对应 Schema 的 `factions` 字段。

**出口条件**：势力设定完成并在内存中就绪
**加载 References**：`social-structure.md`

---

### Phase 4：基础规则（如需要）

**入口条件**：`required_elements.worldbuilding.required` 包含 `core_rules`
**目标**：设计世界运行的基础规则

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 4。
2. 读取 `references/world-rules.md`
3. **编排指令**：[强制] 唤醒子 Agent `story-architect` 承接本阶段交互。
4. **启发式交互**：Agent 提供 2-3 套包含以下规则的预设方案：
   - 核心规则（世界如何运行）
   - 禁忌与限制（什么不能做）
   - 特殊设定（如时代铁律、系统机制）
5. **停顿确认**：与用户多轮迭代直到确认。
6. 数据暂存于内存中，对应 Schema 的 `core_rules` 字段。

**出口条件**：基础规则设定完成并在内存中就绪
**加载 References**：`world-rules.md`

---

### Phase 4.5：场景与背景 (Locations & Lore)（如需要）

**入口条件**：`required_elements.worldbuilding.required` 包含 `locations` 或 `lore`
**目标**：设计核心地理场景与历史传说

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 4.5。
2. **编排指令**：[强制] 唤醒子 Agent `story-architect` 承接本阶段交互。
3. **启发式交互**：Agent 提供 2-3 套场景风格与背景设定的组合方案（Option A/B/C），包含：
   - 主舞台（如核心城市、宗门所在地）与关键探索地（如秘境）
   - 关键历史事件（如诸神黄昏）与重要特殊物品（Artifacts）
4. **停顿确认**：与用户多轮迭代直到确认。
5. 数据暂存于内存中，对应 Schema 的 `locations` 和 `lore` 字段。

**出口条件**：场景与背景设定完成并在内存中就绪
**加载 References**：无

---

### Phase 5：落盘验证

**入口条件**：所有必需要素已设计
**目标**：生成 worldbuilding.yaml 并验证完整性

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 5。
2. **最终检查**：汇总所有内存中的设定，审查是否严格符合 Phase 1 中读取的 `data/schemas/worldbuilding.schema.yaml` 的数据结构。
3. **写入文件**：以合规格式写入 `settings/worldbuilding.yaml`。
4. **门禁校验**：运行 `node .agents/skills/worldbuilding/scripts/check-completeness.js settings/scout_report.yaml settings/worldbuilding.yaml` 进行强制验证。
5. 若脚本抛出 `[blocking]` 错误，必须阻断流程并修正。
6. 验证通过后，清理 `_progress.md` 文件。

**出口条件**：目标文件已合规生成并写入硬盘，通过脚本门禁。
**加载 References**：无

---

## 质量门禁 (Quality Gates)

- **脚本校验**：`check-completeness.js` 检查 `required_elements.worldbuilding.required` 中的元素是否完整存在且非空。
- **拦截逻辑**：当脚本输出 `[blocking]` 缺少必需元素时，流程阻断，Agent 必须自动修正或请求用户补充信息。

---

## 断点恢复 (Recovery)

**状态文件**：`_progress.md`（位于项目根目录）

**格式范例**：
```markdown
# worldbuilding Progress
- current_phase: <1-5>
- status: in_progress | completed
- last_updated: <timestamp>
```

**恢复逻辑**：
- 启动时检查 `_progress.md`。
- 若状态非 completed，主动询问用户是否继续中断的进度，跳到对应的 current_phase。

---

## 输出文件

- `settings/worldbuilding.yaml`：世界观设定

---

## References 索引

| Phase | References | 用途 |
|-------|-----------|------|
| 1 | genre-worldbuilding.md | 品类×世界观适配矩阵 |
| 2 | power-system-guide.md | 力量体系设计方法论 |
| 3 | social-structure.md | 社会结构设计 |
| 4 | world-rules.md | 基础规则设计 |
| 5 | — | 落盘验证 |

---

## 下一步 (Next Steps)

worldbuilding.yaml 生成后，可进入：
- `/design-character`：人设设计
- `/design-outline`：大纲设计
