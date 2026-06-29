# Phase 3 执行计划：design-character（人设设计）

> **执行目标**：完整重写 design-character skill，包含 SKILL.md + 5 references + 1 script

---

## 文件清单

| 文件 | 行数估计 | 职责 |
|------|---------|------|
| `.agents/skills/design-character/SKILL.md` | ~180 行 | 主流程：5 Phase + 品类感知质量门禁 |
| `.agents/skills/design-character/references/character-basics.md` | ~150 行 | 基础人设设计方法论 |
| `.agents/skills/design-character/references/protagonist-arc.md` | ~200 行 | 主角弧线设计（起点→终点→转折点） |
| `.agents/skills/design-character/references/villain-design.md` | ~150 行 | 反派设计（动机、手段、恶心度） |
| `.agents/skills/design-character/references/cool-factor-guide.md` | ~200 行 | 爽感评估指南（打脸指数/CP感/恶心度） |
| `.agents/skills/design-character/references/relationship-network.md` | ~150 行 | 关系网络设计 |
| `.agents/skills/design-character/scripts/check-characters.js` | ~100 行 | 人设完整性检查（品类感知） |

---

## 任务 3.1：创建目录结构

```bash
mkdir -p .agents/skills/design-character/references
mkdir -p .agents/skills/design-character/scripts
```

---

## 任务 3.2：编写 SKILL.md

### 完整内容

```markdown
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
- **自洽检查**：角色关系不能有矛盾（A 恨 B 但 B 不知道 A 是谁——这种信息差需要明确标注）
- check-characters.js 自动执行以上所有检查

---

## 断点恢复

**状态文件**：`_progress.md`
**格式**：同 scout-topic
**恢复逻辑**：跳到最后一个 in_progress 的 Phase

---

## 输出文件

- `settings/characters.yaml`：人物设定（对齐 data/schemas/characters.schema.yaml）

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
```

---

## 任务 3.3：编写 references/character-basics.md

### 完整内容

```markdown
# 基础角色设计方法论

> **用途**：Phase 1 品类适配 + 通用角色设计基础。

---

## 角色设计原则

1. **功能性**：每个角色都要有存在的理由——推动剧情、制造冲突、提供信息。
2. **辨识度**：读者能通过性格/口头禅/外貌特征区分角色。
3. **成长性**：主角必须有弧线变化，配角可以有小幅变化。
4. **品类适配**：不同品类的角色需求差异很大。

---

## 品类×角色适配矩阵

### 玄幻修仙

| 角色类型 | 必要性 | 典型设计 |
|---------|--------|---------|
| protagonist | required | 废柴逆袭/天才陨落重生，需要明确的修炼目标 |
| villain | required | 层级反派（小反派→中反派→大反派→终极反派） |
| master | optional | 导师/引路人，传授功法，关键时刻救场 |
| rival | optional | 同门竞争者，亦敌亦友 |
| supporting_cast | optional | 兄弟/姐妹/队友 |

### 都市言情

| 角色类型 | 必要性 | 典型设计 |
|---------|--------|---------|
| protagonist | required | 重生者/逆袭者，需要社会身份和经济基础 |
| love_interest | required | 恋爱对象，需要有吸引力和化学反应 |
| rival | optional | 情敌/商业对手 |
| best_friend | optional | 闺蜜/兄弟，提供吐槽和情感支持 |
| supporting_cast | optional | 家人/同事/朋友 |

### 系统文

| 角色类型 | 必要性 | 典型设计 |
|---------|--------|---------|
| protagonist | required | 系统宿主，需要明确系统互动方式 |
| supporting_cast | required | 队友/伙伴（系统文常组队） |
| villain | optional | 敌对势力 |
| system_npc | optional | 系统拟人化/系统精灵 |

### 言情

| 角色类型 | 必要性 | 典型设计 |
|---------|--------|---------|
| protagonist | required | 女主视角（或双视角），需要情感弧线 |
| love_interest | required | 男主，需要与女主有化学反应 |
| rival | optional | 情敌/白月光/前任 |
| best_friend | optional | 闺蜜，提供建议和搞笑 |

---

## 角色深度规则

| 角色类型 | 必填内容 | 可省略 |
|---------|---------|--------|
| protagonist（主角） | traits, psychology, arc | 外貌（部分品类） |
| antagonist（反派） | traits, psychology, arc, 动机 | 外貌 |
| supporting（配角） | traits, description | psychology, arc |
| minor（龙套） | description | traits, psychology, arc |

---

## 角色卡模板

```yaml
- name: 角色名
  role: protagonist/antagonist/supporting/minor
  archetype: 废柴逆袭/天才型/导师型/反派/龙套/其他
  description: 一句话核心描述
  traits:
    - 性格特征1
    - 性格特征2
    - 性格特征3
  psychology:                    # 主角/反派必填
    fatal_flaw: 关键缺陷
    obsession: 执念
    soft_spot: 软肋
    misbelief: 误判
  arc:                           # 主角/反派必填
    type: 成长弧线/堕落弧线/悲剧弧线/探索弧线/扁平弧线
    start: 起点状态
    end: 终点状态
    stages:
      - stage: 阶段名
        state: 该阶段状态
        chapter: 章节范围
  appearance:                    # 可选
    age: 年龄段
    gender: 性别
    features: [外貌特征]
    typical_clothing: 典型着装
  relationships: []              # Phase 4 补充
```

---

## 品类适配检查清单

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | 品类识别正确 | 已根据 scout_report.yaml 选择框架 |
| 2 | 必需角色齐全 | required 中的角色类型都已设计 |
| 3 | 深度达标 | 主角/反派有 psychology + arc |
| 4 | 功能明确 | 每个角色都有存在的理由 |
```

---

## 任务 3.4：编写 references/protagonist-arc.md

### 完整内容

```markdown
# 主角弧线设计

> **用途**：Phase 2 设计主角时对照使用。
> **核心**：起点→终点→转折点，弧线决定故事走向。

---

## 设计原则

1. **起点要低**：起点越低，逆袭越爽（废柴流的核心逻辑）。
2. **终点要高**：终点不一定是天下第一，但必须有质变。
3. **转折点要痛**：转折需要代价，无痛的成长不叫弧线。
4. **内外一致**：内心成长和外在实际变化要同步。

---

## 起点设计

### 经典起点模板

| 起点类型 | 描述 | 爽感潜力 | 适用品类 |
|---------|------|---------|---------|
| 废柴型 | 天赋极差、被人看不起 | ★★★★★ | 玄幻、都市 |
| 陨落型 | 曾经辉煌、跌落谷底 | ★★★★☆ | 玄幻、都市 |
| 重生型 | 带着记忆回到过去 | ★★★★★ | 都市、玄幻 |
| 普通人型 | 平凡生活被打破 | ★★★☆☆ | 系统、悬疑 |
| 隐忍型 | 有实力但被迫隐藏 | ★★★★☆ | 都市、玄幻 |

### 起点要素清单

```yaml
start_state:
  social_status: 社会地位（底层/中层/上层）
  power_level: 实力等级（弱/中/强）
  emotional_state: 情感状态（绝望/迷茫/平静）
  material_condition: 物质条件（贫穷/普通/富裕）
  key_loss: 核心缺失（尊严/亲人/记忆/自由）
```

**关键**：起点状态决定"打脸"的基数。起点越低，同样程度的逆袭，打脸效果越强。

---

## 终点设计

### 终点类型

| 终点类型 | 描述 | 示例 |
|---------|------|------|
| 登顶型 | 成为最强/最高 | 仙界至尊、商业帝国 |
| 自由型 | 获得自由/解脱 | 摆脱控制、打破枷锁 |
| 守护型 | 守护了重要的人/事物 | 保护了家人、守住了宗门 |
| 超越型 | 超越自我/宿命 | 打破诅咒、逆转命运 |
| 归隐型 | 功成身退 | 归隐山林、平凡生活 |

### 终点要素清单

```yaml
end_state:
  social_status: 最终社会地位
  power_level: 最终实力等级
  emotional_state: 最终情感状态
  relationships: 最终人际关系
  legacy: 留下的遗产/影响
```

---

## 转折点设计

### 转折点类型

| 类型 | 描述 | 效果 | 示例 |
|------|------|------|------|
| 觉醒型 | 突然领悟/觉醒 | 实力飞跃 | 获得传承、系统激活 |
| 失去型 | 失去重要的人/物 | 性格转变 | 师父牺牲、宝物被夺 |
| 背叛型 | 被信任的人背叛 | 信任崩塌 | 兄弟反目、爱人背叛 |
| 选择型 | 面临两难选择 | 价值观确立 | 救人还是夺宝 |
| 暴露型 | 隐藏身份/实力暴露 | 格局变化 | 扮猪吃虎后暴露 |

### 转折点节奏

```
前期（1-30章）：1-2 个小转折（获得金手指、初次展现实力）
中期（31-100章）：2-3 个中转折（失去重要的人、价值观挑战）
后期（100+章）：1-2 个大转折（终极觉醒、最终选择）
```

### 转折点模板

```yaml
arc:
  type: 成长弧线
  start: 废柴，被全族嘲笑
  end: 仙界至尊，万人敬仰
  stages:
    - stage: 觉醒
      state: 获得系统/传承，开始修炼
      chapter: 1-10
      turning_point: 觉醒型
    - stage: 初露锋芒
      state: 打败小反派，进入大宗门
      chapter: 11-30
      turning_point: 暴露型
    - stage: 至暗时刻
      state: 师父牺牲，被迫逃亡
      chapter: 31-50
      turning_point: 失去型
    - stage: 浴火重生
      state: 领悟大道，突破瓶颈
      chapter: 51-80
      turning_point: 觉醒型
    - stage: 登顶
      state: 打败终极反派，成为至尊
      chapter: 81-100
      turning_point: 选择型
```

---

## 弧线类型详解

### 成长弧线（最常用）
- 起点：弱/废柴/底层
- 终点：强/至尊/巅峰
- 关键：成长过程要有起伏，不能一路升级

### 堕落弧线
- 起点：善良/正义
- 终点：黑化/堕落
- 关键：每个阶段的堕落都要有合理触发

### 悲剧弧线
- 起点：有希望
- 终点：一切毁灭
- 关键：悲剧要有意义，不是为虐而虐

### 探索弧线
- 起点：无知/迷茫
- 终点：理解/接受
- 关键：探索过程的发现要出人意料

### 扁平弧线
- 起点=终点：角色不变，但改变周围世界
- 关键：适合配角或特定品类（如无敌流）

---

## 质量检查

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | 起点够低 | 读者能产生同情/代入感 |
| 2 | 终点清晰 | 能用一句话说出终点状态 |
| 3 | 转折点 ≥ 3 | 至少 3 个关键转折点 |
| 4 | 转折有代价 | 每次转折都有代价/牺牲 |
| 5 | 内外一致 | 内心成长和外在变化同步 |
| 6 | 弧线类型明确 | 已选择并标注弧线类型 |
```

---

## 任务 3.5：编写 references/villain-design.md

### 完整内容

```markdown
# 反派设计方法论

> **用途**：Phase 3 设计反派时对照使用。
> **核心**：反派越恶心，打脸越爽。反派是主角的磨刀石。

---

## 设计原则

1. **动机合理**：反派与主角对立必须有逻辑，不能为恶而恶。
2. **手段恶心**：手段越恶心，被打脸时读者越爽。
3. **有层次感**：长篇需要多层反派（小→中→大→终极）。
4. **有弱点**：反派的弱点决定最终如何被打败。

---

## 反派层级设计

### 层级模板

| 层级 | 身份 | 恶心度 | 存活周期 | 作用 |
|------|------|--------|---------|------|
| 小反派 | 同门/同学/小头目 | 3-5 | 10-30章 | 给主角练手，积累打脸爽感 |
| 中反派 | 宗门长老/公司高管 | 5-7 | 30-60章 | 制造真正威胁，推动成长 |
| 大反派 | 宗主/商业巨头 | 7-9 | 60-100章 | 核心冲突，考验主角极限 |
| 终极反派 | 天帝/幕后黑手 | 9-10 | 100+章 | 最终对决，全书高潮 |

**关键**：每一层反派都比上一层更恶心、更难对付。

---

## 动机设计

### 动机类型

| 类型 | 描述 | 示例 | 复杂度 |
|------|------|------|--------|
| 利益冲突 | 与主角争夺资源/地位 | 争夺宝物、抢夺地盘 | ★★☆☆☆ |
| 仇恨驱动 | 与主角有旧仇 | 杀父之仇、灭门之恨 | ★★★☆☆ |
| 嫉妒/恐惧 | 嫉妒主角天赋/恐惧主角成长 | 怕被超越、怕失去地位 | ★★★☆☆ |
| 理念对立 | 与主角的价值观根本对立 | 正邪对立、路线之争 | ★★★★☆ |
| 宿命对立 | 命运安排的对立 | 预言中的宿敌、血脉诅咒 | ★★★★★ |

**建议**：中后期反派的动机应该更复杂（理念对立/宿命对立），避免"纯恶"。

---

## 恶心度设计

### 恶心行为分级

| 等级 | 行为类型 | 示例 | 打脸爽感 |
|------|---------|------|---------|
| 1-3 | 言语侮辱 | 嘲笑、讽刺、看不起 | 一般 |
| 4-5 | 行为打压 | 抢夺资源、设置障碍、当众羞辱 | 较爽 |
| 6-7 | 伤害亲友 | 伤害主角的朋友/家人、背叛 | 很爽 |
| 8-9 | 夺走一切 | 灭门、毁掉修为、夺走爱人 | 极爽 |
| 10 | 不可饶恕 | 虐杀无辜、毁灭世界 | 必须打脸 |

### 恶心度节奏

```
小反派（1-3 级）：嘲笑主角是废物 → 被打脸
中反派（4-6 级）：抢夺主角资源、伤害朋友 → 被打脸
大反派（7-9 级）：灭门、毁掉一切 → 被打脸
终极反派（10 级）：不可饶恕之罪 → 终极打脸
```

**核心公式**：恶心度 = 打脸爽感上限

---

## 反派弱点设计

| 弱点类型 | 描述 | 示例 |
|---------|------|------|
| 傲慢 | 看不起主角 | "一个废物也配跟我斗？" |
| 信息差 | 不知道主角的底牌 | 不知道主角有系统 |
| 情感弱点 | 有在意的人/事 | 唯一在乎的弟子 |
| 力量缺陷 | 能力有死角 | 强大但有致命破绽 |
| 内部矛盾 | 势力内部不团结 | 手下有二心 |

---

## 反派卡模板

```yaml
- name: 反派名
  role: antagonist
  archetype: 反派
  description: 一句话描述
  tier: 小反派/中反派/大反派/终极反派
  traits:
    - 性格特征1
    - 性格特征2
  psychology:
    fatal_flaw: 关键缺陷（傲慢/贪婪/偏执）
    obsession: 执念（权力/复仇/控制）
    soft_spot: 软肋（如有）
    misbelief: 误判（对主角的误判）
  motivation:
    type: 利益冲突/仇恨驱动/嫉妒恐惧/理念对立/宿命对立
    description: 动机详述
    connection_to_protagonist: 与主角的关系
  disgusting_level: 8  # 1-10
  disgusting_behaviors:
    - 恶心行为1
    - 恶心行为2
  weakness: 弱点描述
  arc:
    type: 堕落弧线/扁平弧线
    start: 起点状态
    end: 被打败/死亡/洗白
  relationships:
    - to: 主角名
      type: 死敌
      description: 关系描述
```

---

## 质量检查

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | 动机合理 | 能解释"为什么与主角对立" |
| 2 | 恶心度 ≥ 7 | 中后期反派恶心度 ≥ 7/10 |
| 3 | 有弱点 | 每个反派都有明确的弱点 |
| 4 | 层级清晰 | 长篇需要 ≥ 2 层反派 |
| 5 | 被打脸方式 | 已规划如何被打败 |
```

---

## 任务 3.6：编写 references/cool-factor-guide.md

### 完整内容

```markdown
# 爽感评估指南

> **用途**：Phase 5 评估人设爽感时对照使用。
> **核心**：三维评估——打脸指数、CP感、反派恶心度。

---

## 评估概述

人设的"爽感"可以量化为三个维度：

| 维度 | 适用品类 | 目标分数 | 核心公式 |
|------|---------|---------|---------|
| 打脸指数（face-slap index） | 玄幻/都市/系统 | ≥ 7/10 | 起点落差 × 扮猪程度 × 围观反应 |
| CP感（chemistry） | 言情/都市 | ≥ 7/10 | 人设互补 × 互动张力 × 名场面潜力 |
| 反派恶心度（disgust level） | 全品类 | ≥ 7/10 | 恶心行为 × 持续时间 × 打脸期待 |

**及格线**：每个适用维度 ≥ 6/10，建议 ≥ 7/10。

---

## 维度一：打脸指数

### 计算公式

```
打脸指数 = 起点落差(1-3) × 扮猪程度(1-3) × 围观反应(1-3) / 3
```

### 起点落差

| 落差 | 描述 | 分值 |
|------|------|------|
| 小 | 普通→优秀 | 1 |
| 大 | 废柴→强者 | 2 |
| 极大 | 被灭门→仙界至尊 | 3 |

### 扮猪程度

| 程度 | 描述 | 分值 |
|------|------|------|
| 无 | 一直很强，不需要隐藏 | 1 |
| 部分 | 隐藏部分实力 | 2 |
| 完全 | 完全隐藏身份/实力 | 3 |

### 围观反应

| 反应 | 描述 | 分值 |
|------|------|------|
| 个人 | 只有当事人震惊 | 1 |
| 群体 | 一个圈子震惊 | 2 |
| 天下 | 天下震动 | 3 |

### 打脸类型参考

| 类型 | 描述 | 爽感 |
|------|------|------|
| 实力打脸 | 用绝对实力碾压 | ★★★★☆ |
| 身份打脸 | 暴露隐藏身份 | ★★★★★ |
| 知识打脸 | 用知识/经验碾压 | ★★★★☆ |
| 资源打脸 | 用资源碾压 | ★★★☆☆ |
| 反转打脸 | 先示弱后反杀 | ★★★★★ |

### 评分标准

| 分数 | 评级 | 说明 |
|------|------|------|
| 1-3 | 差 | 缺乏打脸潜力，需要重新设计起点 |
| 4-6 | 一般 | 有打脸空间但不够爽，建议增加落差/扮猪 |
| 7-8 | 良好 | 打脸设计到位，读者会爽 |
| 9-10 | 极佳 | 经典打脸配置，读者会拍大腿叫好 |

---

## 维度二：CP感

### 计算公式

```
CP感 = 人设互补(1-3) × 互动张力(1-3) × 名场面潜力(1-3) / 3
```

### 人设互补

| 互补度 | 描述 | 分值 |
|--------|------|------|
| 相似 | 两人性格接近 | 1 |
| 互补 | 性格有互补但不过分 | 2 |
| 反差 | 极端反差（冰山×暖男/腹黑×单纯） | 3 |

### 互动张力

| 张力 | 描述 | 分值 |
|------|------|------|
| 低 | 平淡相处，没有摩擦 | 1 |
| 中 | 有拌嘴、有暧昧拉扯 | 2 |
| 高 | 爱恨交织、误会重重、身份对立 | 3 |

### 名场面潜力

| 潜力 | 描述 | 分值 |
|------|------|------|
| 低 | 想不到经典场景 | 1 |
| 中 | 有 1-2 个潜在名场面 | 2 |
| 高 | 多个名场面（壁咚/挡刀/表白/分离重逢） | 3 |

### CP 类型参考

| 类型 | 描述 | 嗑点 |
|------|------|------|
| 欢喜冤家 | 互相看不顺眼→真香 | 拌嘴→心动 |
| 冰山融化 | 冷面×暖阳 | 冰山为一人破例 |
| 青梅竹马 | 从小认识→确认关系 | 回忆杀、日常甜 |
| 宿敌变CP | 敌人→暧昧→在一起 | 爱恨交织 |
| 先婚后爱 | 契约关系→真感情 | 假戏真做 |

### 评分标准

| 分数 | 评级 | 说明 |
|------|------|------|
| 1-3 | 差 | 没有CP感，读者不会嗑 |
| 4-6 | 一般 | 有基础但需要增加互动张力 |
| 7-8 | 良好 | CP感充足，读者会嗑 |
| 9-10 | 极佳 | 经典CP配置，读者会催更 |

---

## 维度三：反派恶心度

### 评估维度

| 方面 | 1-3 | 4-6 | 7-10 |
|------|------|------|------|
| 对主角的态度 | 看不起/嘲讽 | 打压/抢夺资源 | 灭门/夺走一切 |
| 持续时间 | 短期冲突 | 多次冲突 | 持续压迫，积累仇恨 |
| 手段卑劣度 | 明面对抗 | 暗地里使绊子 | 背叛/利用主角信任 |
| 伤害程度 | 轻微 | 影响修炼/事业 | 伤害亲友/毁灭一切 |

### 评分标准

| 分数 | 评级 | 说明 |
|------|------|------|
| 1-3 | 差 | 反派不够恶心，打脸无爽感 |
| 4-6 | 一般 | 有一定仇恨但不强烈 |
| 7-8 | 良好 | 读者恨得牙痒痒，期待打脸 |
| 9-10 | 极佳 | 读者恨不得亲自动手，打脸时极度舒爽 |

---

## 综合评估模板

```yaml
cool_factor_assessment:
  face_slap_index:
    score: 8/10
    breakdown:
      gap: 3          # 起点落差：废柴→至尊
      disguise: 2     # 扮猪程度：隐藏部分实力
      audience: 3     # 围观反应：天下震动
    notes: "废柴开局+隐藏身份，适合扮猪吃虎"

  chemistry:
    score: 7/10
    breakdown:
      complement: 3   # 人设互补：冰山×暖阳
      tension: 2      # 互动张力：有暧昧拉扯
      scene_potential: 2  # 名场面潜力：壁咚+挡刀
    notes: "反差人设有嗑点，建议增加名场面"

  disgust_level:
    score: 8/10
    notes: "灭门之仇+多次羞辱，打脸爽感强"
    villain_list:
      - name: 小反派
        level: 5
      - name: 大反派
        level: 8
      - name: 终极反派
        level: 10
```

---

## 调整建议模板

当某一维度不达标时，参考以下调整方向：

### 打脸指数 < 6
- 降低起点（让主角更惨）
- 增加扮猪元素（隐藏身份/实力）
- 设计围观场景（需要有观众）
- 增加反转打脸（先示弱后反杀）

### CP感 < 6
- 增加人设反差（性格互补）
- 设计互动场景（增加接触机会）
- 增加张力（误会/身份对立/禁忌）
- 设计名场面（壁咚/挡刀/分离重逢）

### 反派恶心度 < 6
- 升级恶心行为（从嘲讽升级到实际伤害）
- 延长压迫时间（让仇恨积累更久）
- 增加背叛元素（利用主角信任）
- 伤害主角在意的人（触动读者情感）
```

---

## 任务 3.7：编写 references/relationship-network.md

### 完整内容

```markdown
# 关系网络设计

> **用途**：Phase 4 设计配角和关系网络时对照使用。

---

## 设计原则

1. **以主角为中心**：所有关系都围绕主角展开。
2. **功能互补**：每个配角承担不同功能（辅助/搞笑/信息/冲突）。
3. **关系有动态**：关系可以变化（敌人→朋友、朋友→敌人）。
4. **不过度复杂**：配角 ≤ 10 个核心关系，避免读者记不住。

---

## 角色功能分类

| 功能 | 描述 | 示例 |
|------|------|------|
| 辅助型 | 帮助主角成长/战斗 | 队友、导师 |
| 冲突型 | 给主角制造麻烦 | 竞争对手、内奸 |
| 情感型 | 提供情感支持/牵绊 | 恋人、家人、挚友 |
| 信息型 | 提供关键信息 | 线人、智者 |
| 搞笑型 | 调节气氛 | 搞笑搭档、吐槽役 |
| 镜像型 | 映射主角的另一种可能 | 走了另一条路的"影子" |

---

## 关系类型

| 类型 | 描述 | 动态可能性 |
|------|------|-----------|
| 师徒 | 教导与被教导 | 可能反目、可能超越 |
| 兄弟/姐妹 | 深厚的友谊 | 可能背叛、可能生死与共 |
| 恋人 | 爱情关系 | 可能分离、可能误会 |
| 对手 | 竞争关系 | 可能化敌为友、可能升级仇恨 |
| 主仆 | 从属关系 | 可能平等化、可能反叛 |
| 仇敌 | 深仇大恨 | 可能和解（少见）、至死方休 |
| 盟友 | 利益/目标一致 | 可能因利益分裂 |

---

## 关系网络模板

### 配角卡

```yaml
- name: 配角名
  role: supporting/minor
  archetype: 导师型/兄弟型/搞笑型/龙套
  description: 一句话描述
  traits:
    - 性格特征1
    - 性格特征2
  function: 辅助型/冲突型/情感型/信息型/搞笑型
  relationships:
    - to: 主角名
      type: 兄弟
      description: 关系描述
      importance: primary/secondary/minor
    - to: 另一配角
      type: 对手
      description: 关系描述
      importance: secondary
```

### 关系网络图（文字版）

```
          ┌─────────┐
          │  师父    │
          │ (导师型) │
          └────┬────┘
               │ 师徒
          ┌────┴────┐     ┌─────────┐
          │  主角   │─────│  恋人    │
          │(protagonist)│  │(love_interest)│
          └────┬────┘     └─────────┘
         ┌─────┼─────┐
    兄弟 │     │ 仇敌  │ 竞争
    ┌────┴──┐  ┌┴─────┐
    │ 兄弟  │  │ 反派  │
    │(supporting)│ │(antagonist)│
    └───────┘  └──────┘
```

---

## 关系动态设计

### 关系变化节点

| 阶段 | 可能的变化 | 触发条件 |
|------|-----------|---------|
| 前期 | 陌生人→相识 | 共同经历 |
| 前期 | 对手→尊重 | 实力认可 |
| 中期 | 朋友→背叛 | 利益冲突/被迫 |
| 中期 | 暧昧→确认 | 关键时刻/危机 |
| 中期 | 盟友→敌人 | 理念分歧 |
| 后期 | 敌人→和解 | 共同对抗更大威胁 |
| 后期 | 师徒→超越 | 主角成长到超越师父 |

### 关系变化模板

```yaml
relationship_changes:
  - who: 配角名
    from: 对手
    to: 盟友
    trigger: 共同对抗大反派
    chapter: 45
    significance: 扩大了主角的势力
  - who: 另一配角名
    from: 朋友
    to: 叛徒
    trigger: 被反派威胁家人
    chapter: 60
    significance: 主角遭遇重大打击
```

---

## 质量检查

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | 配角数量 | 核心配角 ≥ 3 个 |
| 2 | 功能覆盖 | 至少覆盖 3 种功能 |
| 3 | 关系完整 | 每个角色都有与主角的关系 |
| 4 | 有动态 | 至少 2 段关系有变化 |
| 5 | 无孤立角色 | 没有与其他角色毫无关系的配角 |
```

---

## 任务 3.8：编写 scripts/check-characters.js

### 完整内容

```javascript
#!/usr/bin/env node
// check-characters.js — 人设完整性检查（品类感知）
// Usage: node check-characters.js <scout_report.yaml> <characters.yaml>

const fs = require('fs');
const yaml = require('js-yaml');

function main() {
  const scoutFile = process.argv[2];
  const charFile = process.argv[3];

  if (!scoutFile || !charFile) {
    console.error('Usage: node check-characters.js <scout_report.yaml> <characters.yaml>');
    process.exit(2);
  }

  const scout = yaml.load(fs.readFileSync(scoutFile, 'utf8'));
  const chars = yaml.load(fs.readFileSync(charFile, 'utf8'));

  const requiredMap = scout.required_elements?.characters || {};
  const characters = chars.characters || [];
  const findings = [];

  // 1. 检查必需角色类型是否存在
  const roleMap = {};
  for (const c of characters) {
    if (c.role === 'protagonist') roleMap.protagonist = true;
    if (c.role === 'antagonist') roleMap.antagonist = true;
    if (c.role === 'supporting') roleMap.supporting_cast = true;
    if (c.role === 'minor') roleMap.minor = true;
  }

  // 检查 required 角色类型
  for (const [type, level] of Object.entries(requiredMap)) {
    if (level === 'required' && !roleMap[type]) {
      // 特殊映射：love_interest 可能是 supporting 或 protagonist
      if (type === 'love_interest') {
        const hasLoveInterest = characters.some(c =>
          c.relationships?.some(r => r.type === '恋人' || r.type === 'love_interest')
        );
        if (!hasLoveInterest && !roleMap.antagonist) {
          findings.push({
            severity: 'blocking',
            message: `缺少必需的角色类型: ${type}`,
          });
        }
      } else {
        findings.push({
          severity: 'blocking',
          message: `缺少必需的角色类型: ${type}`,
        });
      }
    }
  }

  // 2. 检查每个角色的深度
  for (const c of characters) {
    const name = c.name || '(未命名)';
    const role = c.role || '(未设定)';

    if (!c.name) {
      findings.push({ severity: 'blocking', message: '存在未命名的角色' });
    }
    if (!c.role) {
      findings.push({ severity: 'blocking', message: `${name}: 缺少 role 字段` });
    }

    // 主角和反派需要完整深度
    if (role === 'protagonist' || role === 'antagonist') {
      if (!c.traits || c.traits.length === 0) {
        findings.push({ severity: 'blocking', message: `${name}: 缺少性格特征 (traits)` });
      }
      if (!c.psychology || isEmpty(c.psychology)) {
        findings.push({ severity: 'blocking', message: `${name}: 缺少心理维度 (psychology)` });
      }
      if (!c.arc || !c.arc.start || !c.arc.end) {
        findings.push({ severity: 'blocking', message: `${name}: 缺少人物弧线 (arc.start/end)` });
      }
    }

    // 配角至少需要 traits + description
    if (role === 'supporting') {
      if (!c.description) {
        findings.push({ severity: 'warning', message: `${name}: 缺少描述 (description)` });
      }
      if (!c.traits || c.traits.length === 0) {
        findings.push({ severity: 'warning', message: `${name}: 配角建议添加性格特征 (traits)` });
      }
    }
  }

  // 3. 检查是否有主角
  const hasProtagonist = characters.some(c => c.role === 'protagonist');
  if (!hasProtagonist) {
    findings.push({ severity: 'blocking', message: '缺少主角 (protagonist)' });
  }

  // 4. 检查关系网络
  const protagonist = characters.find(c => c.role === 'protagonist');
  if (protagonist && (!protagonist.relationships || protagonist.relationships.length === 0)) {
    findings.push({ severity: 'warning', message: '主角没有关系设定，建议建立关系网络' });
  }

  // 输出结果
  if (findings.length === 0) {
    console.log('✓ 人设完整性检查通过');
    process.exit(0);
  }

  const blocking = findings.filter(f => f.severity === 'blocking');
  const warnings = findings.filter(f => f.severity === 'warning');

  for (const f of findings) {
    console.log(`[${f.severity}] ${f.message}`);
  }

  console.log(`\n共 ${blocking.length} 个阻塞问题，${warnings.length} 个警告`);
  process.exit(blocking.length > 0 ? 1 : 0);
}

function isEmpty(val) {
  if (val === null || val === undefined) return true;
  if (typeof val === 'string') return val.trim() === '';
  if (Array.isArray(val)) return val.length === 0;
  if (typeof val === 'object') return Object.keys(val).length === 0;
  return false;
}

main();
```

---

## 执行顺序

1. 创建目录结构
2. 编写 SKILL.md
3. 编写 character-basics.md
4. 编写 protagonist-arc.md
5. 编写 villain-design.md
6. 编写 cool-factor-guide.md
7. 编写 relationship-network.md
8. 编写 check-characters.js
9. 验证脚本可运行
10. Commit
