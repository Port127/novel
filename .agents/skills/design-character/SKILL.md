---
name: design-character
description: 人设设计。与 Agent 交互设计主角、反派、配角，含爽感维度评估。
---

# design-character（人设设计）

> **用途**：设计小说人物，包括主角、反派、配角，并评估爽感维度。
> **前置条件**：`settings/scout_report.yaml` 存在（品类已确定）。
> **输出文件**：`settings/characters.yaml`

---

## 核心原则

1. **品类适配**：不同品类需要不同角色类型（玄幻需要反派，言情需要恋爱对象）。
2. **弧线驱动**：主角必须有清晰的起点→终点弧线，弧线上有关键转折点。
3. **反派即剧情**：反派的恶心程度决定打脸的爽感上限。
4. **爽感可量化**：打脸指数、CP感、反派恶心度——三维评估人设质量。
5. **关系成网**：角色不是孤立的，关系网络决定剧情张力。

---

## Phase 定义

### Phase 1：品类适配

**入口条件**：scout_report.yaml 存在
**目标**：根据品类加载对应角色框架，确定需要设计的角色类型

**步骤**：
1. 读取 `scout_report.yaml` 的 `genre` 和 `required_elements.characters`
2. 读取 `references/character-basics.md`，加载品类对应角色框架
3. 展示该品类需要设计的角色类型
4. 确认设计范围

**出口条件**：角色类型列表确定
**加载 References**：`character-basics.md`

**品类框架示例**：

| 品类 | 必需角色 | 可选角色 | 设计重点 |
|------|---------|---------|---------|
| 玄幻 | protagonist, villain | supporting_cast, rival, master | 主角逆袭弧线、反派层级 |
| 都市 | protagonist, love_interest | rival, best_friend | CP感、社会身份差 |
| 系统 | protagonist, supporting_cast | villain, system_npc | 系统交互、配角功能 |
| 言情 | protagonist, love_interest | rival, best_friend | 双弧线、CP化学反应 |
| 悬疑 | protagonist, antagonist | suspect_pool | 信息差、动机链 |

---

### Phase 2：主角设计

**入口条件**：角色类型已确认
**目标**：设计主角完整人设

**步骤**：
1. 读取 `references/protagonist-arc.md`
2. 引导用户设计：
   - 基本信息（姓名、年龄、身份）
   - 性格特征（≥3 个 traits）
   - 心理维度（缺陷/执念/软肋/误判）
   - 人物弧线（起点→终点→转折点）
   - 金手指/核心能力
   - 外貌特征（可选）
3. 写入 characters.yaml 的 protagonist 条目

**出口条件**：主角人设完整（traits + psychology + arc 均已填写）
**加载 References**：`protagonist-arc.md`

---

### Phase 3：反派设计

**入口条件**：`required_elements.characters` 包含 `villain` 或 `antagonist`
**目标**：设计反派完整人设

**步骤**：
1. 读取 `references/villain-design.md`
2. 引导用户设计：
   - 基本信息（姓名、身份、与主角的关系）
   - 动机（为什么与主角对立——必须有合理逻辑）
   - 手段（怎么对付主角——越恶心越好）
   - 恶心度设计（羞辱/背叛/夺走/威胁）
   - 弱点（最终被打败的原因）
   - 人物弧线（可选）
3. 写入 characters.yaml 的 antagonist 条目

**出口条件**：反派人设完整（动机 + 手段 + 恶心度 ≥ 7/10）
**加载 References**：`villain-design.md`

---

### Phase 4：配角与关系网络

**入口条件**：主角和反派已设计
**目标**：设计配角和关系网络

**步骤**：
1. 读取 `references/relationship-network.md`
2. 引导用户设计：
   - 配角列表（姓名、角色类型、一句话描述）
   - 每个配角与主角的关系
   - 配角之间的关系
   - 关系网络图（文字描述）
3. 写入 characters.yaml 的 supporting/minor 条目

**出口条件**：配角 ≥ 3 个，关系网络已建立
**加载 References**：`relationship-network.md`

---

### Phase 5：爽感评估与落盘

**入口条件**：所有必需角色已设计
**目标**：评估爽感三维，生成 characters.yaml 并验证

**步骤**：
1. 读取 `references/cool-factor-guide.md`
2. 评估三维爽感：
   - 打脸指数（face-slap index）
   - CP感（chemistry）
   - 反派恶心度（disgust level）
3. 如任一维度 < 6/10，给出调整建议
4. 汇总所有人设，展示给用户确认
5. 写入 `settings/characters.yaml`
6. 运行 `scripts/check-characters.js` 验证
7. 清理 `_progress.md`

**出口条件**：characters.yaml 已生成，爽感三维均 ≥ 6/10，通过完整性检查
**加载 References**：`cool-factor-guide.md`

---

## 质量门禁

- **品类感知检查**：读取 `scout_report.yaml` 的 `required_elements.characters`，检查必需角色类型是否齐全
- **深度检查**：主角/反派必须有 psychology + arc；配角至少需要 traits + description
- **爽感检查**：打脸指数/CP感/恶心度 三维均需 ≥ 6/10
- check-characters.js 自动执行以上检查

---

## 断点恢复

**状态文件**：`_progress.md`
**格式**：同 scout-topic
**恢复逻辑**：跳到最后一个 in_progress 的 Phase

---

## 输出文件

- `settings/characters.yaml`：人物设定

---

## References 索引

| Phase | References | 用途 |
|-------|-----------|------|
| 1 | character-basics.md | 基础角色设计方法论 + 品类适配 |
| 2 | protagonist-arc.md | 主角弧线设计 |
| 3 | villain-design.md | 反派设计方法论 |
| 4 | relationship-network.md | 关系网络设计 |
| 5 | cool-factor-guide.md | 爽感三维评估 |

---

## 下一步

characters.yaml 生成后，可进入：
- `/design-outline`：大纲设计（人设驱动剧情）
- `/design-chapters`：章节设计
