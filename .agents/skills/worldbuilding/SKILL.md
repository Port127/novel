---
name: worldbuilding
description: 世界观设计。与 Agent 交互讨论力量体系、社会结构、基础规则。
---

# worldbuilding（世界观设计）

> **用途**：设计小说的世界观设定，包括力量体系、社会结构、基础规则。
> **前置条件**：`settings/scout_report.yaml` 存在（品类已确定）。
> **输出文件**：`settings/worldbuilding.yaml`

---

## 核心原则

1. **品类适配**：不同品类的世界观重点不同（玄幻重力量体系，都市重时代背景）。
2. **自洽优先**：世界观必须内部自洽，不能有矛盾。
3. **服务于剧情**：世界观为剧情服务，不是为了设定而设定。
4. **品类感知**：根据 `scout_report.yaml` 的 `required_elements.worldbuilding` 决定设计重点。

---

## Phase 定义

### Phase 1：品类适配

**入口条件**：scout_report.yaml 存在
**目标**：根据品类加载对应框架

**步骤**：
1. 读取 `scout_report.yaml` 的 `genre` 和 `required_elements.worldbuilding`
2. 读取 `references/genre-worldbuilding.md`，加载品类对应框架
3. 展示该品类需要设计的世界观要素
4. 确认设计范围

**出口条件**：设计范围确定
**加载 References**：`genre-worldbuilding.md`

**品类框架示例**：

| 品类 | 必需要素 | 重点 |
|------|---------|------|
| 玄幻 | power_system, factions, locations | 力量等级、宗门势力 |
| 都市 | era_details, locations, social_rules | 时代背景、社会规则 |
| 系统 | system_rules, quest_mechanics | 系统规则、任务机制 |
| 言情 | locations, relationship_context | 场景、社交圈 |

---

### Phase 2：力量体系（如需要）

**入口条件**：`required_elements.worldbuilding.required` 包含 `power_system`
**目标**：设计力量体系

**步骤**：
1. 读取 `references/power-system-guide.md`
2. 引导用户设计：
   - 体系名称
   - 等级划分（3-9 级为宜）
   - 升级条件
   - 战斗表现
   - 限制与代价
3. 写入 worldbuilding.yaml 的 `power_system` 字段

**出口条件**：`power_system` 已填写
**加载 References**：`power-system-guide.md`

---

### Phase 3：社会结构（如需要）

**入口条件**：`required_elements.worldbuilding.required` 包含 `social_rules` 或 `factions`
**目标**：设计社会结构

**步骤**：
1. 读取 `references/social-structure.md`
2. 引导用户设计：
   - 主要势力（≥3 个）
   - 势力关系（敌对/同盟/中立）
   - 社会规则（阶层流动、禁忌）
3. 写入 worldbuilding.yaml

**出口条件**：势力和社会规则已填写
**加载 References**：`social-structure.md`

---

### Phase 4：基础规则（如需要）

**入口条件**：`required_elements.worldbuilding.required` 包含 `world_rules`
**目标**：设计世界运行的基础规则

**步骤**：
1. 读取 `references/world-rules.md`
2. 引导用户设计：
   - 核心规则（世界如何运行）
   - 禁忌与限制（什么不能做）
   - 特殊设定（如穿越规则、系统规则）
3. 写入 worldbuilding.yaml

**出口条件**：基础规则已填写
**加载 References**：`world-rules.md`

---

### Phase 5：落盘验证

**入口条件**：所有必需要素已设计
**目标**：生成 worldbuilding.yaml 并验证完整性

**步骤**：
1. 汇总所有设定，展示给用户确认
2. 写入 `settings/worldbuilding.yaml`
3. 运行 `scripts/check-completeness.js` 验证
4. 清理 `_progress.md`

**出口条件**：worldbuilding.yaml 已生成且通过验证
**加载 References**：无

---

## 质量门禁

- check-completeness.js：检查 `required_elements.worldbuilding.required` 中的元素是否完整

---

## 断点恢复

**状态文件**：`_progress.md`
**格式**：同 scout-topic
**恢复逻辑**：跳到最后一个 in_progress 的 Phase

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

## 下一步

worldbuilding.yaml 生成后，可进入：
- `/design-character`：人设设计
- `/design-outline`：大纲设计
