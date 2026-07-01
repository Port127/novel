# Phase 4 执行计划：design-outline（大纲设计）

> **执行目标**：完整重写 design-outline skill，包含 SKILL.md + 5 references + 2 scripts

---

## 文件清单

| 文件 | 行数估计 | 职责 |
|------|---------|------|
| `.agents/skills/design-outline/SKILL.md` | ~200 行 | 主流程：5 Phase + 品类适配 + 结构类型选择 |
| `.agents/skills/design-outline/references/outline-structure.md` | ~200 行 | 大纲结构方法论（三幕式/起承转合/英雄之旅，幕→序列→节拍嵌套） |
| `.agents/skills/design-outline/references/pacing-guide.md` | ~200 行 | 节奏设计指南（张力曲线、高潮分布、快慢交替） |
| `.agents/skills/design-outline/references/plot-frameworks.md` | ~250 行 | 经典剧情框架（升级流/复仇流/系统流/宗门流等） |
| `.agents/skills/design-outline/references/foreshadowing-guide.md` | ~150 行 | 伏笔管理（埋设/回收/跨卷追踪） |
| `.agents/skills/design-outline/references/tension-curve.md` | ~150 行 | 张力曲线设计模板 |
| `.agents/skills/design-outline/scripts/check-outline.js` | ~100 行 | 结构完整性检查（品类感知） |
| `.agents/skills/design-outline/scripts/check-pacing.js` | ~150 行 | 节奏问题检测（连续慢章、高潮间距） |

---

## 任务 4.1：创建目录结构

```bash
mkdir -p .agents/skills/design-outline/references
mkdir -p .agents/skills/design-outline/scripts
```

---

## 任务 4.2：编写 SKILL.md

### 完整内容

```markdown
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

**品类×结构映射**：

| 品类 | 推荐结构 | 推荐框架 | 典型卷数 |
|------|---------|---------|---------|
| 玄幻 | 英雄之旅 | 升级流/宗门流 | 8-15 卷 |
| 都市 | 三幕式 | 重生逆袭/文娱 | 3-6 卷 |
| 系统 | 英雄之旅 | 系统流/任务流 | 5-10 卷 |
| 言情 | 起承转合 | 感情流 | 2-4 卷 |
| 悬疑 | 三幕式 | 推理流 | 1-3 卷 |

---

### Phase 2：骨架搭建（幕级规划）

**入口条件**：结构类型已确定
**目标**：完成幕级大纲

**步骤**：
1. 根据结构类型生成幕级骨架：
   - 三幕式：建置（25%）→ 对抗（50%）→ 解决（25%）
   - 起承转合：起（15%）→ 承（35%）→ 转（35%）→ 合（15%）
   - 英雄之旅：12 阶段按幕分配
2. 为每幕确定：
   - 幕名称和章节范围
   - 核心冲突
   - 转折点（inciting_incident / midpoint / climax 等）
   - 主角状态变化（起点→终点）
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
2. 为每个序列确定：
   - 序列名称和章节范围
   - 序列目标（推进哪个冲突线）
   - 序列小高潮
   - 涉及角色
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
2. 每个节拍包含：
   - 节拍编号和名称
   - 所在章节
   - 事件描述
   - 张力值（1-5）
   - 涉及伏笔操作（埋设/推进/回收）
3. 运行 `scripts/check-pacing.js` 检测节奏问题
4. 根据检测结果调整节拍
5. 展示节拍级大纲，请用户确认

**出口条件**：节拍级大纲已确认且节奏检测通过
**加载 References**：无

---

### Phase 5：落盘验证

**入口条件**：所有层级大纲已确认
**目标**：生成输出文件并验证

**步骤**：
1. 汇总所有大纲数据
2. 写入 `settings/outline.yaml`（主大纲，对齐 outline.schema.yaml）
3. 写入 `settings/arcs.yaml`（叙事弧线，卷/弧级别）
4. 写入 `settings/pacing.yaml`（节奏曲线，章节级张力标注）
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
| 品类匹配 | SKILL.md 内置 | 检查高潮密度、伏笔风格是否符合品类要求 |
| 伏笔闭合 | check-outline.js | 检查所有伏笔是否已安排回收 |

---

## 断点恢复

**状态文件**：`_progress.md`
**格式**：同 scout-topic / worldbuilding
**恢复逻辑**：跳到最后一个 in_progress 的 Phase

---

## 输出文件

- `settings/outline.yaml`：主大纲（对齐 data/schemas/outline.schema.yaml）
- `settings/arcs.yaml`：叙事弧线（卷/弧级别的结构）
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
- 直接开始 `/nm`（章节写作）
```

---

## 任务 4.3：编写 references/outline-structure.md

### 完整内容

```markdown
# 大纲结构方法论

> **用途**：Phase 1-2 根据结构类型加载对应模板。
> **核心概念**：全书 → 幕（Act）→ 序列（Sequence）→ 节拍（Beat），层层嵌套。

---

## 三种结构类型

### 一、三幕式结构

最通用的结构，适合大多数品类。

```
┌──────────────┬───────────────────────────┬──────────────┐
│  第一幕：建置  │     第二幕：对抗           │  第三幕：解决  │
│   (25%)      │       (50%)               │    (25%)      │
│              │                           │              │
│ 日常→激励事件 │ 上升动作→中点→下降动作      │ 高潮→结局     │
│ →第一转折点   │ →第二转折点 →灵魂暗夜       │ →最终决战     │
└──────────────┴───────────────────────────┴──────────────┘
```

#### 关键节点

| 节点 | 位置 | 作用 | 示例（玄幻） |
|------|------|------|-------------|
| 激励事件 | 10-15% | 打破主角日常 | 觉醒金手指 |
| 第一转折点 | 25% | 进入新世界 | 进入宗门 |
| 中点 | 50% | 重大反转/信息 | 发现师父是反派 |
| 第二转折点 | 75% | 最坏时刻前夕 | 失去重要之人 |
| 灵魂暗夜 | 80% | 最低谷 | 被困绝境 |
| 高潮 | 90-95% | 最终对决 | 击败大Boss |

#### 多卷三幕式

长篇网文每卷可以独立使用三幕式：

```yaml
卷一（练气篇）:
  第一幕: 凡人少年，意外获得修炼功法
  第二幕: 进入宗门，修炼+对抗+宗门大比
  第三幕: 宗门危机，力挽狂澜，筑基成功

卷二（筑基篇）:
  第一幕: 走出宗门，进入更大的世界
  第二幕: 秘境探险+势力冲突+修为提升
  第三幕: 秘境崩塌，绝境突破，金丹大成
```

---

### 二、起承转合结构

源自东方叙事传统，适合言情、都市日常等节奏较缓的品类。

```
┌────────┬────────────┬────────────┬────────┐
│  起     │    承       │    转       │  合    │
│ (15%)  │   (35%)     │   (35%)     │ (15%) │
│        │            │            │       │
│ 建立    │  发展深化    │  突变逆转    │ 收束  │
│ 人物和  │  关系/能力   │  冲突爆发    │ 大团圆│
│ 背景    │  持续积累    │  或重大真相  │ 或BE  │
└────────┴────────────┴────────────┴────────┘
```

#### 各部分要点

| 部分 | 核心任务 | 节奏 | 关键技巧 |
|------|---------|------|---------|
| 起 | 人物登场、背景交代、初始魅力 | 中等偏快 | 开篇即亮点，3章内建立吸引力 |
| 承 | 关系发展、能力成长、世界观展开 | 波浪式上升 | 甜虐交替、小高潮不断 |
| 转 | 重大变故、真相揭露、关系危机 | 先快后慢 | 转折点要出乎意料又合情合理 |
| 合 | 解决冲突、情感归宿、主题升华 | 先快后缓 | 高潮要猛，收尾要干净 |

---

### 三、英雄之旅结构

Joseph Campbell 的单一神话结构，适合玄幻、冒险类。

```
                    ┌─── 非常世界 ───┐
                    │                │
         ⑥考验     ⑤跨越门槛     ⑦接近洞穴
           ↑                        ↓
      ④遇见导师                    ⑧磨难
           ↑                        ↓
      ③拒绝召唤                    ⑨报酬
           ↑                        ↓
      ②遇到召唤 ←── ①平凡世界 ──→ ⑩归来
                                       ↓
                                  ⑪复活（最终考验）
                                       ↓
                                  ⑫带着灵药回归
```

#### 12 阶段与章节分配

| 阶段 | 名称 | 占比 | 作用 |
|------|------|------|------|
| ① | 平凡世界 | 5% | 展示主角的日常生活 |
| ② | 冒险召唤 | 5-10% | 打破平衡的事件 |
| ③ | 拒绝召唤 | 5% | 主角犹豫/恐惧 |
| ④ | 遇见导师 | 5-10% | 获得指引/装备 |
| ⑤ | 跨越门槛 | 10% | 进入新世界/新状态 |
| ⑥ | 考验、伙伴、敌人 | 15% | 成长与试炼 |
| ⑦ | 接近最深的洞穴 | 10% | 接近终极目标 |
| ⑧ | 磨难 | 15% | 最大危机 |
| ⑨ | 报酬 | 5% | 获得宝物/力量 |
| ⑩ | 返回 | 5% | 带着收获回归 |
| ⑪ | 复活 | 10% | 最终考验/蜕变 |
| ⑫ | 带着灵药回归 | 5% | 新的平衡 |

---

## 嵌套层级详解

### 幕（Act）

全书最大的结构单位。

```yaml
act:
  number: 1
  title: "初入宗门"
  chapters: [1, 50]          # 起始章-结束章
  arc: "从废柴少年到外门第一"
  conflict: "天赋低被歧视 vs 暗中修炼突破"
  turning_point:
    chapter: 48
    description: "宗门大比一鸣惊人"
    type: first_threshold
```

### 序列（Sequence）

幕内的中等结构单位，通常围绕一个子目标展开。

```yaml
sequence:
  number: 1
  title: "外门试炼"
  chapters: [10, 25]
  goal: "通过外门试炼获得正式弟子身份"
  mini_climax: "第25章，险胜对手"
  characters_involved: [主角, 师兄A, 对手B]
```

### 节拍（Beat）

序列内的最小结构单位，对应具体章节中的关键事件。

```yaml
beat:
  number: 1
  title: "初遇灵兽"
  chapter: 12
  description: "在山中采药时遇到受伤灵兽"
  tension: 3
  foreshadowing:
    - action: plant
      hook_id: "beast_bond"
      note: "灵兽身上有神秘纹路"
```

---

## 结构类型选择指南

| 条件 | 推荐结构 | 原因 |
|------|---------|------|
| 品类=玄幻/冒险 | 英雄之旅 | 成长弧天然匹配 |
| 品类=言情/都市日常 | 起承转合 | 关系发展需要渐进式铺垫 |
| 品类=悬疑/推理 | 三幕式 | 谜团→调查→揭秘天然三幕 |
| 品类=系统文 | 英雄之旅 | 任务循环匹配试炼模式 |
| 多线叙事 | 三幕式 | 多线可以在中点交汇 |
| 短篇（<50章） | 三幕式 | 简洁直接 |
| 长篇（>200章） | 英雄之旅+分卷三幕 | 每卷独立三幕，全书英雄之旅 |

---

## 质量检查

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | 结构类型匹配 | 已根据 scout_report 选择正确结构 |
| 2 | 层级完整 | 幕→序列→节拍层级清晰 |
| 3 | 转折点明确 | 每幕都有明确的转折点 |
| 4 | 主角弧线 | 主角从 A 状态变到 B 状态，变化有过程 |
| 5 | 比例合理 | 各幕比例符合结构模板要求 |
```

---

## 任务 4.4：编写 references/pacing-guide.md

### 完整内容

```markdown
# 节奏设计指南

> **用途**：Phase 3-4 设计节奏、检测节奏问题时对照使用。
> **核心目标**：确保全书节奏健康，不出现连续慢章或高潮真空。

---

## 节奏基本概念

### 快慢定义

| 节奏 | 定义 | 典型内容 | 张力值 |
|------|------|---------|--------|
| 快 | 高强度冲突/动作 | 战斗、追逐、对峙、揭秘 | 4-5 |
| 中 | 有目标但无直接冲突 | 修炼、调查、准备、社交 | 2-3 |
| 慢 | 日常/描写/内心 | 日常互动、风景描写、回忆 | 1-2 |

### 快慢比例建议

| 品类 | 快:中:慢 | 说明 |
|------|----------|------|
| 玄幻 | 3:4:3 | 战斗多但不能一直打 |
| 都市 | 2:5:3 | 日常铺垫为主，爽点穿插 |
| 言情 | 2:4:4 | 甜/虐/日常三段式 |
| 系统 | 3:4:3 | 任务（快）+ 准备（中）+ 奖励日常（慢）|
| 悬疑 | 3:5:2 | 推理过程（中）为主 |

---

## 节奏设计原则

### 原则 1：快慢交替

不能连续 3 章以上都是慢节奏。

```
✓ 健康节奏：中→快→慢→中→快→中→慢→快→快→慢
✗ 问题节奏：慢→慢→慢→慢→中→慢→慢（连续4+慢章）
```

### 原则 2：高潮间距

两个高潮（张力≥4）之间不超过 15 章。

```
✓ 第10章高潮 → 第22章高潮（间距12章）
✗ 第10章高潮 → 第40章高潮（间距30章，读者流失）
```

### 原则 3：卷首卷尾加强

每卷的前3章和后3章必须是中快节奏。

```yaml
卷首:
  chapter_1: tension >= 3    # 开篇抓人
  chapter_2: tension >= 2    # 可以稍缓
  chapter_3: tension >= 3    # 重新提起

卷尾:
  last_3: tension >= 4       # 高潮收卷
  last_1: tension >= 3       # 余韵或钩子
```

### 原则 4：黄金三章

前三章决定读者去留，必须满足：
- 第1章：张力 ≥ 4（强烈开局）
- 第2章：张力 ≥ 3（维持吸引力）
- 第3章：张力 ≥ 4（第一个小高潮/转折）

---

## 节奏设计模板

### 模板 A：波浪上升型（适合玄幻/系统）

```
张力
5  │          ╱╲        ╱╲╱╲
4  │    ╱╲  ╱    ╲  ╱╲╱      ╲╱╲
3  │  ╱    ╲╱      ╲╱          ╲╱──
2  │╱
1  │╲
   └─────────────────────────────── 章节
    建置    对抗第一卷    对抗第二卷   高潮
```

特点：每个波峰比前一个更高，波谷也在上升。

### 模板 B：甜虐交替型（适合言情）

```
张力
5  │        ╱╲
4  │    ╱╲╱    ╲      ╱╲
3  │  ╱          ╲  ╱    ╲
2  │╱              ╲╱      ╲╱──
1  │╲╱
   └─────────────────────────────── 章节
    甜    虐    甜    大虐   大甜
```

特点：甜（张力2-3）和虐（张力4-5）交替，幅度逐渐加大。

### 模板 C：阶梯型（适合升级流）

```
张力
5  │                  ╱╲
4  │            ╱╲  ╱    ╲
3  │      ╱╲  ╱    ╲╱
2  │╱╲  ╱    ╲╱
1  │  ╲╱
   └─────────────────────────────── 章节
   练气  筑基   金丹   元婴   化神
```

特点：每个等级就是一个阶梯，升级战是高潮。

---

## 节奏问题检测标准

| 问题类型 | 定义 | 严重度 | 修复建议 |
|---------|------|--------|---------|
| 连续慢章 | 连续 3+ 章张力 ≤ 2 | blocking | 插入一个小冲突或信息揭示 |
| 高潮真空 | 连续 15+ 章无张力 ≥ 4 | blocking | 添加一个小高潮 |
| 高潮密集 | 连续 5+ 章张力 ≥ 4 | warning | 添加喘息章节 |
| 开局疲软 | 前3章平均张力 < 3 | blocking | 重写出局，加强第一章节奏 |
| 卷尾疲软 | 卷尾3章平均张力 < 3 | warning | 加强卷末高潮 |
| 节奏单调 | 连续 8+ 章节奏相同（无快慢变化） | warning | 插入节奏变化 |

---

## pacing.yaml 格式

```yaml
pacing:
  total_chapters: 200
  target_pacing:
    fast_ratio: 0.3
    medium_ratio: 0.4
    slow_ratio: 0.3
  
  milestones:
    - chapter: 1
      tension: 4
      note: "开局，金手指觉醒"
    - chapter: 30
      tension: 5
      note: "第一卷高潮，宗门大比"
    - chapter: 50
      tension: 4
      note: "第二卷开篇，新地图"
  
  health_check:
    max_consecutive_slow: 3
    max_climax_gap: 15
    golden_chapters_min_tension: 3
```

---

## 质量检查

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | 无连续慢章 | 不超过 3 章连续张力 ≤ 2 |
| 2 | 高潮间距合理 | 不超过 15 章无高潮 |
| 3 | 黄金三章达标 | 前3章张力满足要求 |
| 4 | 快慢交替 | 无连续 8+ 章相同节奏 |
| 5 | 卷首卷尾 | 卷首卷尾3章节奏达标 |
```

---

## 任务 4.5：编写 references/plot-frameworks.md

### 完整内容

```markdown
# 经典剧情框架

> **用途**：Phase 1 根据品类加载对应剧情框架。
> **说明**：每个框架提供标准化的剧情骨架，可根据具体项目调整。

---

## 一、升级流框架

**适用品类**：玄幻、仙侠、系统文
**核心驱动**：主角修为/能力持续提升
**爽点来源**：突破、打脸、获得宝物

### 标准循环

```
日常/修炼 → 遇到瓶颈 → 寻找突破资源 → 战斗/冒险 → 突破成功 → 新地图/新挑战
```

### 多卷结构模板

```yaml
升级流_多卷结构:
  卷一（起步）:
    level: 初始→第一阶
    setting: 小地方（村镇/小宗门）
    conflict: 被欺负，证明自己
    climax: 小比/考核一鸣惊人
    chapters: 30-50
  
  卷二（成长）:
    level: 第一阶→第二阶
    setting: 中等势力（大宗门/王城）
    conflict: 卷入更大势力斗争
    climax: 大比/秘境探险
    chapters: 50-80
  
  卷三（崛起）:
    level: 第二阶→第三阶
    setting: 大势力核心/新大陆
    conflict: 对抗顶级势力
    climax: 跨级战斗/拯救危机
    chapters: 80-120
  
  卷四+（巅峰）:
    level: 第三阶→巅峰
    setting: 世界核心/上界
    conflict: 终极之战
    climax: 最终决战
    chapters: 100-200
```

### 节奏要点
- 每次突破之间不超过 30 章
- 打脸方式要变化（不能总是同一个套路）
- 新地图要带来新的规则和对手

---

## 二、复仇流框架

**适用品类**：玄幻、都市、历史
**核心驱动**：复仇目标驱动
**爽点来源**：逐步变强、逐个击破仇人、真相揭露

### 结构模板

```yaml
复仇流结构:
  起（灭门/受辱）:
    event: 家族被灭/被人陷害/遭受奇耻大辱
    emotion: 愤怒、绝望
    hook: 获得复仇的力量/机会
    chapters: 10-20
  
  承（积蓄力量）:
    pattern: 修炼→小复仇→更大目标→更大修炼
   仇人列表:
      - name: 仇人A（小Boss）
        chapter_defeat: 50
        difficulty: 容易
      - name: 仇人B（中Boss）
        chapter_defeat: 120
        difficulty: 困难
      - name: 仇人C（大Boss）
        chapter_defeat: 200
        difficulty: 极难
    chapters: 30-150
  
  转（真相揭露）:
    revelation: 发现仇人背后还有更大的黑手
    twist: 原来灭门有隐情/恩人是真凶
    emotion: 动摇、痛苦、重新定义目标
    chapters: 150-180
  
  合（终极复仇）:
    final_battle: 击败最终仇人
    cost: 复仇的代价
    ending: 新的开始 or 同归于尽
    chapters: 180-220
```

### 节奏要点
- 仇人实力阶梯式上升
- 每个仇人的击败方式要不同
- 复仇过程中穿插成长和新关系

---

## 三、系统流框架

**适用品类**：系统文、游戏文
**核心驱动**：系统任务驱动 + 奖励反馈
**爽点来源**：任务完成、稀有奖励、系统升级

### 系统节奏循环

```
任务发布 → 任务准备 → 执行任务 → 危机/意外 → 完成任务 → 奖励发放 → 短暂日常
    ↑                                                              │
    └──────────────────── 新任务 ←──────────────────────────────────┘
```

### 任务类型设计

```yaml
任务体系:
  日常任务:
    frequency: 每 3-5 章
    difficulty: 低
    reward: 基础资源
    function: 维持节奏感
  
  主线任务:
    frequency: 每卷 1-2 个
    difficulty: 中高
    reward: 重大能力提升
    function: 推动剧情
  
  隐藏任务:
    frequency: 每 20-30 章触发 1 个
    difficulty: 不确定
    reward: 稀有/独特
    function: 惊喜感、探索感
  
  危机任务:
    frequency: 每卷高潮
    difficulty: 极高（失败惩罚严重）
    reward: 蜕变级
    function: 高潮节点
```

### 节奏要点
- 系统不能让主角太轻松（有限制和惩罚）
- 任务设计要有意外（不是简单的 A→B→C）
- 奖励要有惊喜感（盲盒机制）

---

## 四、宗门流框架

**适用品类**：玄幻、仙侠
**核心驱动**：宗门内的地位提升 + 宗门间的势力对抗
**爽点来源**：宗门大比、地位提升、宗门兴衰

### 宗门篇模板

```yaml
宗门篇:
  入门篇:
    status: 外门弟子/杂役
    conflict: 被老弟子欺负、资源匮乏
    goal: 通过考核进入内门
    chapters: 20-30
  
  内门篇:
    status: 内门弟子
    conflict: 派系斗争、资源争夺
    goal: 成为核心弟子/真传弟子
    chapters: 30-50
  
  大比篇:
    status: 代表宗门参赛
    conflict: 与其他宗门天才对抗
    goal: 夺冠/证明实力
    chapters: 15-25
    climax_type: 跨级战胜强敌
  
  危机篇:
    status: 宗门面临灭门危机
    conflict: 外敌入侵/内部叛变
    goal: 拯救宗门
    chapters: 20-30
    climax_type: 力挽狂澜
```

---

## 五、重生/穿越流框架

**适用品类**：都市重生、历史穿越
**核心驱动**：先知优势 + 蝴蝶效应
**爽点来源**：精准预判、抢先布局、逆袭翻盘

### 重生流结构

```yaml
重生流结构:
  开局:
    hook: 重生到关键节点
    advantage: 知道未来走向
    first_move: 利用先知优势获取第一桶金/避免第一个坑
    chapters: 5-10
  
  布局期:
    pattern: 预判事件→提前布局→收获成果
    escalation: 从个人小事到商业大事
    complication: 蝴蝶效应导致部分预知失效
    chapters: 30-60
  
  对抗期:
    conflict: 因为改变历史，引来新的对手/困难
    twist: 前世的敌人也受到影响，关系变化
    chapters: 40-80
  
  收获期:
    climax: 最大的布局完成
    resolution: 所有线索收束
    chapters: 20-30
```

### 节奏要点
- 先知优势要逐渐减弱（蝴蝶效应）
- 不能一直顺风顺水，要有意外
- 前世的遗憾要逐个弥补

---

## 六、文娱流框架

**适用品类**：都市文娱、娱乐圈
**核心驱动**：作品发布 + 名声提升
**爽点来源**：作品爆红、装逼打脸、行业地位提升

### 文娱流节奏

```yaml
文娱流结构:
  起步:
    work: 第一部作品（歌/书/剧本）
    impact: 小范围轰动
    status: 无名小卒→圈内新人
    chapters: 20-30
  
  上升:
    work: 连续几部作品
    impact: 逐步扩大影响力
    status: 新人→知名→一线
    conflict: 同行嫉妒、资本打压
    chapters: 40-80
  
  巅峰:
    work: 代表作品
    impact: 行业震动
    status: 一线→顶级
    conflict: 行业变革、新旧势力交替
    chapters: 30-50
```

---

## 框架选择矩阵

| 品类 | 主框架 | 副框架 | 说明 |
|------|--------|--------|------|
| 玄幻 | 升级流 | 宗门流 | 升级为主线，宗门为场景 |
| 都市 | 重生流/文娱流 | 复仇流 | 看具体题材 |
| 系统 | 系统流 | 升级流 | 系统驱动，升级反馈 |
| 言情 | 感情线主导 | 无固定 | 关系发展为核心 |
| 悬疑 | 推理线主导 | 复仇流 | 谜团驱动 |

---

## 质量检查

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | 框架匹配 | 已根据品类选择合适框架 |
| 2 | 循环节奏 | 爽点循环周期合理 |
| 3 | 升级曲线 | 不出现长时间无成长 |
| 4 | 冲突升级 | 冲突随剧情逐步升级 |
| 5 | 框架融合 | 主副框架配合良好 |
```

---

## 任务 4.6：编写 references/foreshadowing-guide.md

### 完整内容

```markdown
# 伏笔管理指南

> **用途**：Phase 3-4 规划伏笔的埋设与回收时对照使用。
> **核心目标**：确保每条伏笔都有明确的回收点，不烂尾。

---

## 伏笔类型

| 类型 | 定义 | 回收周期 | 示例 |
|------|------|---------|------|
| 短线伏笔 | 当卷内回收 | 5-30 章 | 某人的神秘身份→本卷揭晓 |
| 中线伏笔 | 跨 1-2 卷回收 | 30-100 章 | 神秘老者给的物品→关键时刻派上用场 |
| 长线伏笔 | 跨 3+ 卷回收 | 100+ 章 | 主角身世之谜→最终卷揭晓 |
| 角色伏笔 | 角色行为暗示 | 不定 | 某配角的反常行为→暗示叛变 |
| 世界观伏笔 | 世界规则的暗示 | 不定 | 灵气衰退的现象→暗示上古大战 |

---

## 伏笔设计原则

### 原则 1：每条伏笔都要登记

```yaml
hook:
  hook_id: "old_man_ring"
  type: 道具
  planted_chapter: 5
  detail: "神秘老者送给主角一枚看似普通的戒指"
  harvest_chapter: 150
  resolution: "戒指是上古传承钥匙，在生死关头激活"
  status: pending    # pending / harvested / abandoned
```

### 原则 2：伏笔要自然

**好的伏笔**：融入剧情，回头看才发现是伏笔
- 主角随手救了一只小动物 → 后期动物报恩

**差的伏笔**：刻意突出，读者一看就知道是伏笔
- "这个看似普通的石头一定有大用处！" → 太刻意

### 原则 3：短线补偿长线

长线伏笔回收间隔太长，读者会忘记。需要用短线伏笔保持"伏笔→回收"的满足感。

```
短线伏笔：每 10-30 章回收一次（维持满足感）
中线伏笔：每 50-100 章回收一次（惊喜感）
长线伏笔：跨卷回收（震撼感）
```

### 原则 4：伏笔可以交叉

一条伏笔的回收可以触发另一条伏笔的埋设。

```
第5章：埋设伏笔A（神秘信件）
第50章：回收伏笔A → 同时埋设伏笔B（信中提到的人名）
第120章：回收伏笔B（那个人原来是大Boss的师父）
```

---

## 伏笔追踪表

### 按卷追踪

```yaml
foreshadowing:
  卷一:
    planted:
      - hook_id: "ring_mystery"
        chapter: 5
        type: 道具
        target: 卷三
      - hook_id: "senior_sister_secret"
        chapter: 15
        type: 角色
        target: 卷一
    harvested:
      - hook_id: "senior_sister_secret"
        chapter: 45
        resolution: "师姐原来是前掌门之女"
  
  卷二:
    planted:
      - hook_id: "secret_realm_mark"
        chapter: 60
        type: 世界观
        target: 卷四
    harvested:
      - hook_id: "ring_mystery"
        chapter: 80
        resolution: "戒指是秘境钥匙"
```

### 伏笔密度建议

| 卷位置 | 新埋伏笔数 | 回收伏笔数 | 说明 |
|--------|-----------|-----------|------|
| 第一卷 | 3-5 | 1-2 | 多埋少收，制造悬念 |
| 中间卷 | 2-3 | 2-3 | 埋收平衡 |
| 倒数二卷 | 1-2 | 3-5 | 多收少埋，开始收网 |
| 最终卷 | 0 | 所有剩余 | 全部收束，不留烂尾 |

---

## 伏笔与 hooks 字段对应

outline.yaml 的 `hooks` 字段格式：

```yaml
hooks:
  - hook_id: "unique_id"
    hook_type: 道具/人物/悬念/信息/情感
    planted_chapter: 5
    detail: "伏笔描述"
    harvested_chapter: 150          # 可选，规划阶段可以先不填
    resolution: "回收方式"          # 可选
```

---

## 常见伏笔问题

| 问题 | 表现 | 解决 |
|------|------|------|
| 伏笔遗忘 | 埋了没收 | 每卷结束时检查 pending 列表 |
| 伏笔过密 | 一卷埋了10+伏笔 | 控制密度，优先短线 |
| 回收草率 | 一句话带过 | 回收要有仪式感 |
| 伏笔冲突 | 两条伏笔回收后互相矛盾 | 提前规划交叉伏笔的关系 |

---

## 质量检查

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | 伏笔有回收 | 每条 planted 都有对应的 harvested 计划 |
| 2 | 密度合理 | 每卷 3-5 条新伏笔 |
| 3 | 短线补偿 | 每 20 章内至少有 1 次短线回收 |
| 4 | 最终清零 | 最终卷结束时 pending = 0 |
| 5 | 无冲突 | 伏笔之间不矛盾 |
```

---

## 任务 4.7：编写 references/tension-curve.md

### 完整内容

```markdown
# 张力曲线设计模板

> **用途**：Phase 2 绘制幕级张力曲线时对照使用。
> **核心目标**：为每个关键章节标注张力值，形成可视化曲线。

---

## 张力值定义

| 张力值 | 级别 | 场景类型 | 读者情绪 |
|--------|------|---------|---------|
| 1 | 极低 | 日常描写、过渡、环境描写 | 平静/放松 |
| 2 | 低 | 轻度日常、准备阶段、信息铺垫 | 舒缓 |
| 3 | 中 | 冲突开始、小对抗、社交博弈 | 关注 |
| 4 | 高 | 战斗、对峙、重大揭秘、感情转折 | 紧张/兴奋 |
| 5 | 极高 | 高潮、生死抉择、终极对决、大反转 | 激动/震撼 |

---

## 经典张力曲线模板

### 模板 A：三幕式标准曲线

```
张力
5  │                                    ╱╲
4  │    ╱╲              ╱╲╱╲          ╱    ╲
3  │  ╱    ╲          ╱      ╲      ╱
2  │╱        ╲      ╱        ╲   ╱
1  │           ╲  ╱            ╲╱
   └──────────────────────────────────── 章节
    10%    25%     50%      75%  90%  100%
    激励   第一    中点     第二  灵魂  高潮
    事件   转折             转折  暗夜
```

**关键张力点**：

```yaml
tension_key_points:
  opening:
    chapter: 1
    tension: 4
    note: "开局要抓人"
  
  inciting_incident:
    chapter_ratio: 0.12
    tension: 3
    note: "激励事件打破平衡"
  
  first_turning_point:
    chapter_ratio: 0.25
    tension: 4
    note: "进入新世界"
  
  midpoint:
    chapter_ratio: 0.50
    tension: 4
    note: "重大反转/信息"
  
  second_turning_point:
    chapter_ratio: 0.75
    tension: 3
    note: "跌入低谷"
  
  dark_night:
    chapter_ratio: 0.80
    tension: 2
    note: "灵魂暗夜，最低点"
  
  climax:
    chapter_ratio: 0.92
    tension: 5
    note: "最终对决，全书最高潮"
  
  resolution:
    chapter_ratio: 0.98
    tension: 3
    note: "收束余韵"
```

---

### 模板 B：多卷波浪曲线（长篇网文）

```
张力
5  │          ╱╲            ╱╲          ╱╲
4  │    ╱╲  ╱    ╲    ╱╲  ╱    ╲  ╱╲  ╱
3  │  ╱    ╲╱      ╲╱    ╲╱      ╲╱  ╲╱
2  │╱
1  │
   └──────────────────────────────────── 章节
    │卷一│    │卷二│    │卷三│   │卷四│
```

**特点**：
- 每卷有自己的小高潮（张力4-5）
- 卷与卷之间有张力回落（卷末→卷首过渡）
- 全书最高潮在最终卷

**多卷张力规则**：

```yaml
multi_volume_rules:
  volume_climax:
    min_tension: 4
    note: "每卷末尾必须有高潮"
  
  volume_transition:
    max_drop: 2
    note: "卷间过渡张力下降不超过2级"
  
  escalation:
    rule: "后一卷的高潮 ≥ 前一卷的高潮"
    note: "张力峰值逐步上升"
  
  final_volume:
    climax_tension: 5
    note: "最终卷高潮必须是全书最高"
```

---

### 模板 C：双线交织曲线

```
张力
5  │      A           A         A
4  │    ╱╲  B       ╱╲  B    ╱╲  B
3  │  ╱    ╲╱ ╲   ╱    ╲╱  ╱    ╲╱
2  │╱        A  ╲╱      A  ╱
1  │             B
   └──────────────────────────────────── 章节
    ── A线（现实线）  ── B线（副本线/感情线）
```

**特点**：
- A线和B线交替上升
- 一条线缓时另一条线紧张
- 两线在高潮处汇合

---

## 张力曲线与章节映射

### 章节张力标注格式

```yaml
pacing_curve:
  - chapter: 1
    tension: 4
    note: "开局，金手指觉醒"
  - chapter: 2
    tension: 3
    note: "了解金手指规则"
  - chapter: 3
    tension: 4
    note: "第一次使用金手指，小规模打脸"
  - chapter: 10
    tension: 5
    note: "第一序列高潮，击败小Boss"
```

### 自动张力分配规则

| 章节类型 | 默认张力 | 浮动范围 |
|---------|---------|---------|
| 开局章 | 4 | 3-5 |
| 日常章 | 2 | 1-3 |
| 修炼/准备章 | 2 | 2-3 |
| 小冲突章 | 3 | 3-4 |
| 战斗章 | 4 | 3-5 |
| 高潮章 | 5 | 4-5 |
| 转折章 | 4 | 3-5 |
| 过渡章 | 2 | 1-2 |
| 卷末章 | 4 | 4-5 |

---

## 质量检查

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | 开局张力 | 第1章张力 ≥ 3 |
| 2 | 高潮峰值 | 全书至少有1个张力5的点 |
| 3 | 张力上升 | 后一卷高潮 ≥ 前一卷高潮 |
| 4 | 低谷缓冲 | 高潮后有张力回落（不一直维持5） |
| 5 | 最终高潮 | 最终卷高潮是全书最高点 |
```

---

## 任务 4.8：编写 scripts/check-outline.js

### 完整内容

```javascript
#!/usr/bin/env node
// check-outline.js — 大纲结构完整性检查（品类感知）
// Usage: node check-outline.js <scout_report.yaml> <outline.yaml>

const fs = require('fs');
const yaml = require('js-yaml');

function main() {
  const scoutFile = process.argv[2];
  const outlineFile = process.argv[3];

  if (!scoutFile || !outlineFile) {
    console.error('Usage: node check-outline.js <scout_report.yaml> <outline.yaml>');
    process.exit(2);
  }

  const scout = yaml.load(fs.readFileSync(scoutFile, 'utf8'));
  const outline = yaml.load(fs.readFileSync(outlineFile, 'utf8'));

  const findings = [];
  const genre = scout.genre || '未知';
  const structureType = scout.required_elements?.structure?.type || '三幕式';

  // 1. 前提检查
  if (!outline.premise || outline.premise.trim() === '') {
    findings.push({ severity: 'blocking', message: '缺少 premise（核心前提）' });
  }

  // 2. 幕结构检查
  if (!outline.acts || outline.acts.length === 0) {
    findings.push({ severity: 'blocking', message: '缺少 acts（幕结构）' });
  } else {
    // 根据结构类型检查幕数
    const expectedActs = getExpectedActCount(structureType);
    if (outline.acts.length < expectedActs.min) {
      findings.push({
        severity: 'blocking',
        message: `${structureType}结构至少需要 ${expectedActs.min} 幕，当前 ${outline.acts.length} 幕`,
      });
    }

    // 检查每幕必要字段
    for (const act of outline.acts) {
      if (!act.title) {
        findings.push({ severity: 'warning', message: `第 ${act.act} 幕缺少 title` });
      }
      if (!act.chapters || act.chapters.length !== 2) {
        findings.push({ severity: 'warning', message: `第 ${act.act} 幕缺少 chapters 范围` });
      }
      if (!act.turning_point) {
        findings.push({ severity: 'warning', message: `第 ${act.act} 幕缺少 turning_point` });
      }

      // 检查序列
      if (act.sequences && act.sequences.length > 0) {
        for (const seq of act.sequences) {
          if (!seq.title) {
            findings.push({ severity: 'warning', message: `序列 ${seq.sequence} 缺少 title` });
          }
        }
      }
    }
  }

  // 3. 伏笔闭合检查
  if (outline.hooks && outline.hooks.length > 0) {
    const planted = outline.hooks.filter(h => h.planted_chapter);
    const harvested = outline.hooks.filter(h => h.harvested_chapter);
    const pending = planted.length - harvested.length;
    if (pending > 5) {
      findings.push({
        severity: 'warning',
        message: `有 ${pending} 条伏笔未安排回收，建议补充回收计划`,
      });
    }
  }

  // 4. 主题标签检查
  if (!outline.theme || outline.theme.length === 0) {
    findings.push({ severity: 'warning', message: '缺少 theme（主题标签）' });
  }

  // 5. 品类特定检查
  const genreChecks = getGenreChecks(genre, outline);
  findings.push(...genreChecks);

  // 输出结果
  if (findings.length === 0) {
    console.log('✓ 大纲结构完整性检查通过');
    process.exit(0);
  }

  const blocking = findings.filter(f => f.severity === 'blocking');
  for (const f of findings) {
    console.log(`[${f.severity}] ${f.message}`);
  }
  console.log(`\n总计: ${findings.length} 项 (${blocking.length} blocking, ${findings.length - blocking.length} warning)`);
  process.exit(blocking.length > 0 ? 1 : 0);
}

function getExpectedActCount(structureType) {
  switch (structureType) {
    case '三幕式': return { min: 3, max: 5 };
    case '起承转合': return { min: 4, max: 6 };
    case '英雄之旅': return { min: 3, max: 5 };
    default: return { min: 3, max: 5 };
  }
}

function getGenreChecks(genre, outline) {
  const checks = [];

  // 玄幻：检查是否有升级节点
  if (genre.includes('玄幻') || genre.includes('仙侠')) {
    const hasLevelUp = outline.hooks?.some(h =>
      h.detail && (h.detail.includes('突破') || h.detail.includes('升级'))
    );
    if (!hasLevelUp && outline.acts?.length > 1) {
      checks.push({
        severity: 'warning',
        message: '玄幻/仙侠品类建议在大纲中标注升级/突破节点',
      });
    }
  }

  // 言情：检查是否有感情线标记
  if (genre.includes('言情')) {
    if (!outline.plotlines || outline.plotlines.length === 0) {
      checks.push({
        severity: 'warning',
        message: '言情品类建议设置感情线（plotlines）',
      });
    }
  }

  return checks;
}

main();
```

---

## 任务 4.9：编写 scripts/check-pacing.js

### 完整内容

```javascript
#!/usr/bin/env node
// check-pacing.js — 节奏问题检测
// Usage: node check-pacing.js <outline.yaml> [pacing.yaml]

const fs = require('fs');
const yaml = require('js-yaml');

function main() {
  const outlineFile = process.argv[2];
  const pacingFile = process.argv[3];

  if (!outlineFile) {
    console.error('Usage: node check-pacing.js <outline.yaml> [pacing.yaml]');
    process.exit(2);
  }

  const outline = yaml.load(fs.readFileSync(outlineFile, 'utf8'));
  const pacing = pacingFile && fs.existsSync(pacingFile)
    ? yaml.load(fs.readFileSync(pacingFile, 'utf8'))
    : null;

  const findings = [];

  // 提取张力数据
  const tensionData = extractTensionData(outline, pacing);

  if (tensionData.length === 0) {
    console.log('⚠ 无法提取张力数据，跳过节奏检测');
    process.exit(0);
  }

  // 1. 连续慢章检测
  const slowChapters = findConsecutiveSlow(tensionData, 3);
  for (const group of slowChapters) {
    findings.push({
      severity: 'blocking',
      message: `连续 ${group.length} 章慢节奏（第${group[0].chapter}-${group[group.length - 1].chapter}章），张力均 ≤ 2`,
      chapters: group.map(g => g.chapter),
    });
  }

  // 2. 高潮间距检测
  const climaxChapters = tensionData.filter(t => t.tension >= 4);
  if (climaxChapters.length > 0) {
    const gaps = findClimaxGaps(climaxChapters, 15);
    for (const gap of gaps) {
      findings.push({
        severity: 'blocking',
        message: `高潮间距过大：第${gap.from}章到第${gap.to}章（间距${gap.distance}章），无张力 ≥ 4 的章节`,
      });
    }
  }

  // 3. 黄金三章检测
  const firstThree = tensionData.slice(0, 3);
  if (firstThree.length >= 3) {
    const avgTension = firstThree.reduce((sum, t) => sum + t.tension, 0) / 3;
    if (avgTension < 3) {
      findings.push({
        severity: 'blocking',
        message: `黄金三章平均张力 ${avgTension.toFixed(1)} < 3，开局吸引力不足`,
      });
    }
    if (firstThree[0].tension < 3) {
      findings.push({
        severity: 'warning',
        message: `第1章张力 ${firstThree[0].tension} < 3，开局偏弱`,
      });
    }
  }

  // 4. 高潮密集检测
  const denseClimax = findDenseClimax(tensionData, 5);
  for (const group of denseClimax) {
    findings.push({
      severity: 'warning',
      message: `连续 ${group.length} 章高张力（第${group[0].chapter}-${group[group.length - 1].chapter}章），读者可能疲劳`,
    });
  }

  // 5. 节奏单调检测
  const monotone = findMonotoneRhythm(tensionData, 8);
  for (const group of monotone) {
    const avgT = (group.reduce((s, t) => s + t.tension, 0) / group.length).toFixed(1);
    findings.push({
      severity: 'warning',
      message: `连续 ${group.length} 章节奏单调（第${group[0].chapter}-${group[group.length - 1].chapter}章，平均张力 ${avgT}）`,
    });
  }

  // 6. 卷末检查（如果有 pacing milestones）
  if (pacing?.pacing?.milestones) {
    const milestones = pacing.pacing.milestones;
    const lastMilestone = milestones[milestones.length - 1];
    if (lastMilestone && lastMilestone.tension < 4) {
      findings.push({
        severity: 'warning',
        message: `全书最后标记点（第${lastMilestone.chapter}章）张力 ${lastMilestone.tension} < 4，高潮力度不足`,
      });
    }
  }

  // 输出结果
  if (findings.length === 0) {
    console.log('✓ 节奏检测通过');
    console.log(`  张力数据点: ${tensionData.length}`);
    console.log(`  高潮章节数: ${climaxChapters.length}`);
    console.log(`  平均张力: ${(tensionData.reduce((s, t) => s + t.tension, 0) / tensionData.length).toFixed(2)}`);
    process.exit(0);
  }

  const blocking = findings.filter(f => f.severity === 'blocking');
  for (const f of findings) {
    console.log(`[${f.severity}] ${f.message}`);
  }
  console.log(`\n总计: ${findings.length} 项 (${blocking.length} blocking, ${findings.length - blocking.length} warning)`);
  process.exit(blocking.length > 0 ? 1 : 0);
}

function extractTensionData(outline, pacing) {
  const data = [];

  // 从 outline 的 beats 提取
  if (outline.acts) {
    for (const act of outline.acts) {
      if (act.sequences) {
        for (const seq of act.sequences) {
          if (seq.beats) {
            for (const beat of seq.beats) {
              if (beat.chapter && beat.tension !== undefined) {
                data.push({ chapter: beat.chapter, tension: beat.tension });
              }
            }
          }
        }
      }
    }
  }

  // 从 pacing.yaml 的 pacing_curve 提取（补充或覆盖）
  if (pacing?.pacing_curve) {
    for (const point of pacing.pacing_curve) {
      const existing = data.findIndex(d => d.chapter === point.chapter);
      if (existing >= 0) {
        data[existing].tension = point.tension;
      } else {
        data.push({ chapter: point.chapter, tension: point.tension });
      }
    }
  }

  // 从 pacing.yaml 的 milestones 提取
  if (pacing?.pacing?.milestones) {
    for (const ms of pacing.pacing.milestones) {
      const existing = data.findIndex(d => d.chapter === ms.chapter);
      if (existing < 0) {
        data.push({ chapter: ms.chapter, tension: ms.tension });
      }
    }
  }

  // 按章节排序
  data.sort((a, b) => a.chapter - b.chapter);
  return data;
}

function findConsecutiveSlow(data, threshold) {
  const groups = [];
  let current = [];

  for (const item of data) {
    if (item.tension <= 2) {
      current.push(item);
    } else {
      if (current.length >= threshold) {
        groups.push([...current]);
      }
      current = [];
    }
  }
  if (current.length >= threshold) {
    groups.push(current);
  }
  return groups;
}

function findClimaxGaps(climaxChapters, maxGap) {
  const gaps = [];
  for (let i = 1; i < climaxChapters.length; i++) {
    const distance = climaxChapters[i].chapter - climaxChapters[i - 1].chapter;
    if (distance > maxGap) {
      gaps.push({
        from: climaxChapters[i - 1].chapter,
        to: climaxChapters[i].chapter,
        distance,
      });
    }
  }
  return gaps;
}

function findDenseClimax(data, threshold) {
  const groups = [];
  let current = [];

  for (const item of data) {
    if (item.tension >= 4) {
      current.push(item);
    } else {
      if (current.length >= threshold) {
        groups.push([...current]);
      }
      current = [];
    }
  }
  if (current.length >= threshold) {
    groups.push(current);
  }
  return groups;
}

function findMonotoneRhythm(data, threshold) {
  const groups = [];
  let current = [];

  // 将张力分为三档：低(1-2)、中(3)、高(4-5)
  function getLevel(tension) {
    if (tension <= 2) return 'low';
    if (tension === 3) return 'mid';
    return 'high';
  }

  for (const item of data) {
    const level = getLevel(item.tension);
    if (current.length === 0 || getLevel(current[0].tension) === level) {
      current.push(item);
    } else {
      if (current.length >= threshold) {
        groups.push([...current]);
      }
      current = [item];
    }
  }
  if (current.length >= threshold) {
    groups.push(current);
  }
  return groups;
}

main();
```

---

## 执行顺序

1. 创建目录结构
2. 编写 SKILL.md
3. 编写 references/outline-structure.md
4. 编写 references/pacing-guide.md
5. 编写 references/plot-frameworks.md
6. 编写 references/foreshadowing-guide.md
7. 编写 references/tension-curve.md
8. 编写 scripts/check-outline.js
9. 编写 scripts/check-pacing.js
10. 验证脚本可运行（准备测试数据，运行 check-outline.js 和 check-pacing.js）
11. Commit

---

## 依赖关系

```
scout_report.yaml ──┐
                    ├──→ design-outline ──→ outline.yaml
worldbuilding.yaml ─┤                  ──→ arcs.yaml
                    │                  ──→ pacing.yaml
characters.yaml ────┘（可选，有人设更好）
```

---

## 与 Phase 2 的对比

| 维度 | Phase 2 (worldbuilding) | Phase 4 (design-outline) |
|------|------------------------|--------------------------|
| Phase 数 | 5 | 5 |
| References 数 | 4 | 5 |
| Scripts 数 | 1 | 2 |
| 输出文件数 | 1 | 3 |
| 品类感知方式 | required_elements.worldbuilding | required_elements.structure.type + genre |
| 复杂度 | 中（线性流程） | 高（嵌套结构 + 多维检测） |
