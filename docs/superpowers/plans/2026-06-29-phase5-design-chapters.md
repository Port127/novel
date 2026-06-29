# Phase 5 执行计划：design-chapters（细纲设计）

> **执行目标**：完整重写 design-chapters skill，包含 SKILL.md + 3 references + 1 script

---

## 文件清单

| 文件 | 行数估计 | 职责 |
|------|---------|------|
| `.agents/skills/design-chapters/SKILL.md` | ~150 行 | 主流程：5 Phase + 品类适配 |
| `.agents/skills/design-chapters/references/chapter-beat-guide.md` | ~200 行 | 章节节拍设计方法论（节拍类型、密度标记密/疏） |
| `.agents/skills/design-chapters/references/chapter-template.md` | ~150 行 | 章节摘要模板（五要素摘要、多线情节、人物出场、字数预算） |
| `.agents/skills/design-chapters/references/tension-design.md` | ~150 行 | 张力值分配方法 |
| `.agents/skills/design-chapters/scripts/check-chapters.js` | ~100 行 | 章节计划质量检查（节拍3-15、字数2000-5000、必填字段） |

---

## 任务 5.1：创建目录结构

```bash
mkdir -p .agents/skills/design-chapters/references
mkdir -p .agents/skills/design-chapters/scripts
```

---

## 任务 5.2：编写 SKILL.md

### 完整内容

```markdown
---
name: design-chapters
description: 细纲设计。按大纲拆分章节，生成节拍表，检查结构。
---

# design-chapters（细纲设计）

> **用途**：将大纲（outline.yaml）转化为章节计划（chapters_index.yaml）。每章包含摘要、节拍表、张力值、出场人物。
> **前置条件**：
> - `settings/outline.yaml` 存在（大纲已设计）
> - `settings/scout_report.yaml` 存在（品类已确定）
> **输出文件**：`settings/chapters_index.yaml`

---

## 核心原则

1. **节拍驱动**：每章由 3-15 个节拍组成，节拍是剧情最小单位。
2. **密度标记**：用"密/疏"标注每章节奏密度。密=多事件高压，疏=单事件沉淀。
3. **张力曲线**：每章分配张力值（1-5），整体形成波浪形曲线，不能平淡也不能全程高压。
4. **字数预算**：每章 2000-5000 字，根据事件复杂度分配。
5. **品类感知**：根据 `scout_report.yaml` 的 `required_elements.opening_hook.type` 和 `genre` 调整章节策略。

---

## Phase 定义

### Phase 1：大纲解析

**入口条件**：`outline.yaml` 存在
**目标**：解析大纲结构，提取所有节拍

**步骤**：
1. 读取 `outline.yaml`，解析 acts → sequences → beats 层级
2. 统计总节拍数、总幕数、转折点位置
3. 读取 `scout_report.yaml` 的 `genre` 和 `required_elements`
4. 展示大纲概览，让用户确认转化范围（全部 / 前 N 章 / 指定幕）

**出口条件**：节拍列表已提取，转化范围已确认
**加载 References**：无

---

### Phase 2：章节拆分

**入口条件**：节拍列表已提取
**目标**：将节拍分配到各章，确定每章的节拍组

**步骤**：
1. 读取 `references/chapter-beat-guide.md`，加载节拍设计方法论
2. 按以下规则拆分：
   - 每章 3-15 个节拍
   - 密章（动作/冲突密集）：8-15 节拍，3000-5000 字
   - 疏章（情绪/铺垫沉淀）：3-7 节拍，2000-3000 字
   - 转折点章节必须为密章
   - 每 3-5 章形成一个"小高潮-沉淀"循环
3. 展示章节拆分方案，让用户确认

**出口条件**：章节拆分方案已确认
**加载 References**：`chapter-beat-guide.md`

---

### Phase 3：章节摘要

**入口条件**：章节拆分方案已确认
**目标**：为每章生成结构化摘要

**步骤**：
1. 读取 `references/chapter-template.md`，加载章节模板
2. 按模板为每章生成摘要：
   - 五要素摘要（主线推进/人物变化/伏笔/情绪/钩子）
   - 多线情节标注（主线/副线/暗线）
   - 出场人物列表
   - 字数预算
3. 每章摘要控制在 150-300 字

**出口条件**：所有章节摘要已生成
**加载 References**：`chapter-template.md`

---

### Phase 4：张力曲线

**入口条件**：章节摘要已生成
**目标**：为每章分配张力值，形成整体张力曲线

**步骤**：
1. 读取 `references/tension-design.md`，加载张力设计方法
2. 按规则分配张力值：
   - 开篇章（第1章）：2-3（建立情境+钩子）
   - 转折点章节：4-5
   - 高潮章节：5
   - 沉淀章节：1-2
   - 相邻章节张力差不超过 2（避免突兀）
3. 展示张力曲线图（ASCII），让用户确认
4. 检查曲线是否形成波浪形

**出口条件**：张力曲线已确认，无平淡段/无全程高压
**加载 References**：`tension-design.md`

---

### Phase 5：落盘验证

**入口条件**：所有章节摘要和张力值已生成
**目标**：生成 chapters_index.yaml 并通过质量检查

**步骤**：
1. 汇总所有章节数据，展示概览
2. 写入 `settings/chapters_index.yaml`
3. 运行 `scripts/check-chapters.js settings/chapters_index.yaml` 验证
4. 展示验证结果，如有问题则回到对应 Phase 修复
5. 清理 `_progress.md`（如存在）

**出口条件**：chapters_index.yaml 已生成且通过 check-chapters.js 验证
**加载 References**：无

---

## 质量门禁

- `check-chapters.js`：检查每章节拍数（3-15）、字数（2000-5000）、必填字段完整性

---

## 断点恢复

**状态文件**：`_progress.md`（位于小说项目根目录）
**格式**：同 scout-topic
**恢复逻辑**：跳到最后一个 in_progress 的 Phase

---

## 输出文件

- `settings/chapters_index.yaml`：章节索引（对齐 data/schemas/chapters.schema.yaml）

---

## References 索引

| Phase | References | 用途 |
|-------|-----------|------|
| 1 | — | 大纲解析 |
| 2 | chapter-beat-guide.md | 节拍设计方法论 |
| 3 | chapter-template.md | 章节摘要模板 |
| 4 | tension-design.md | 张力值分配方法 |
| 5 | — | 落盘验证 |

---

## 下一步

chapters_index.yaml 生成后，可进入：
- `/golden-chapters`：黄金三章锻造（基于细纲生成前 3 章正文）
```

---

## 任务 5.3：编写 references/chapter-beat-guide.md

### 完整内容

```markdown
# 章节节拍设计方法论

> **用途**：Phase 2 章节拆分时对照使用。
> **核心概念**：节拍（Beat）是剧情最小推进单位，一个节拍 = 一个信息变化/动作/情绪转折。

---

## 节拍类型

| 类型 | 定义 | 示例 | 密度贡献 |
|------|------|------|---------|
| 动作节拍 | 角色执行物理动作 | 拔剑、奔跑、出拳 | 高 |
| 对话节拍 | 角色间信息交换 | 质问、告白、威胁 | 中 |
| 揭示节拍 | 新信息暴露 | 发现秘密、真相揭露 | 高 |
| 转折节拍 | 情境发生逆转 | 盟友背叛、绝境反转 | 极高 |
| 情绪节拍 | 角色内心变化 | 从恐惧到勇气、从希望到绝望 | 中 |
| 环境节拍 | 场景/氛围变化 | 天黑、下雨、人群涌入 | 低 |
| 伏笔节拍 | 埋设后续线索 | 物件特写、路人对话、闪念 | 低 |
| 过渡节拍 | 场景切换/时间流逝 | 赶路、等待、回忆 | 低 |

---

## 密度标记：密/疏

### 密章（高密度）

**定义**：单位字数内包含多个事件/转折，读者神经紧绷。

**适用场景**：
- 战斗/冲突场景
- 高潮段落
- 真相揭露
- 多线交汇

**节拍特征**：
- 动作节拍 + 揭示节拍交替出现
- 转折节拍占比 > 20%
- 环境节拍极少（不浪费字数在氛围上）
- 每 500 字至少一个信息变化

**示例结构**（10 节拍 / 4000 字）：
```
1. [动作] 主角冲进大厅
2. [对话] 反派的挑衅
3. [动作] 第一波交锋
4. [揭示] 发现反派的底牌
5. [转折] 盟友突然倒戈
6. [动作] 陷入包围
7. [情绪] 主角绝境中的决意
8. [动作] 发动底牌技能
9. [转折] 逆转局势
10. [伏笔] 幕后黑手观察
```

### 疏章（低密度）

**定义**：单位字数内事件较少，留出空间给情绪沉淀和人物刻画。

**适用场景**：
- 高潮后的喘息
- 日常互动/人物关系推进
- 准备/计划阶段
- 情感线推进

**节拍特征**：
- 对话节拍 + 情绪节拍为主
- 环境节拍可以出现（营造氛围）
- 过渡节拍自然连接
- 允许留白和沉默

**示例结构**（5 节拍 / 2500 字）：
```
1. [环境] 清晨的院子，鸟叫声
2. [对话] 与师父的日常对话
3. [情绪] 回忆昨晚的战斗，心有余悸
4. [伏笔] 师父暗示 upcoming 危机
5. [过渡] 收拾行装，准备出发
```

---

## 密度节奏规则

### 密疏交替

**核心原则**：不能连续 3 章以上为密章（读者疲劳），也不能连续 3 章以上为疏章（读者流失）。

**标准节奏模式**：

| 模式 | 结构 | 适用 |
|------|------|------|
| 标准波浪 | 疏→密→疏→密 | 通用 |
| 递进紧张 | 疏→中→密→更密→疏 | 卷高潮 |
| 快速切入 | 密→疏→密→疏 | 开篇 |

### 密度标记量化

| 密度 | 节拍数/章 | 字数 | 转折占比 | 信息变化频率 |
|------|----------|------|---------|------------|
| 极密 | 12-15 | 4000-5000 | > 25% | 每 300 字 |
| 密 | 8-11 | 3000-4000 | 15-25% | 每 500 字 |
| 中 | 6-7 | 2500-3500 | 10-15% | 每 700 字 |
| 疏 | 3-5 | 2000-2500 | < 10% | 每 1000 字 |

---

## 节拍编排技巧

### 节拍连接规则

1. **动作→反应**：每个动作节拍后紧跟情绪/对话节拍（不能一直打打打）
2. **铺垫→引爆**：伏笔节拍必须在 5 章内被揭示节拍引爆
3. **转折前置**：转折节拍前必须有至少 1 个情绪节拍做心理铺垫
4. **环境锚定**：场景切换时用 1 个环境节拍锚定新场景

### 节拍数量控制

| 章节类型 | 节拍数 | 说明 |
|---------|--------|------|
| 开篇章 | 5-8 | 快速建立情境 |
| 日常章 | 3-5 | 人物关系推进 |
| 冲突章 | 8-12 | 核心矛盾爆发 |
| 高潮章 | 10-15 | 全书/卷最高点 |
| 过渡章 | 3-5 | 场景切换/时间跳跃 |
| 结尾章 | 5-8 | 收束 + 下卷钩子 |

---

## 常见错误

| 错误 | 表现 | 修正 |
|------|------|------|
| 节拍过密 | 读者来不及消化 | 插入情绪节拍做喘息 |
| 节拍过疏 | 读者觉得水 | 增加揭示/伏笔节拍 |
| 节拍类型单一 | 全是对话或全是动作 | 混合搭配 |
| 伏笔无回收 | 埋了但不引爆 | 在 5 章内安排揭示节拍 |
| 转折无铺垫 | 突然反转 | 前 1-2 章节拍埋线索 |

---

## 质量检查

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | 节拍数量 | 每章 3-15 个 |
| 2 | 密疏交替 | 不连续 3 章同密度 |
| 3 | 节拍类型 | 每章至少 2 种类型 |
| 4 | 伏笔回收 | 所有伏笔节拍有计划回收点 |
| 5 | 转折铺垫 | 转折节拍前有情绪/伏笔铺垫 |
```

---

## 任务 5.4：编写 references/chapter-template.md

### 完整内容

```markdown
# 章节摘要模板

> **用途**：Phase 3 生成章节摘要时对照使用。
> **核心结构**：五要素摘要 + 多线情节 + 出场人物 + 字数预算。

---

## 章节摘要结构

每章摘要包含以下字段：

```yaml
chapter:
  number: 1                    # 章节号
  title: "第一章 开始"          # 标题
  density: 密                   # 密度标记（密/中/疏）
  tension: 3                    # 张力值（1-5）
  words_target: 3000            # 目标字数
  summary:                      # 五要素摘要
    main_plot: ""               # 主线推进
    character_change: ""        # 人物变化
    foreshadowing: ""           # 伏笔（埋设/回收）
    emotion: ""                 # 情绪基调
    hook: ""                    # 章末钩子
  plotlines:                    # 多线情节
    main: ""                    # 主线内容
    sub: ""                     # 副线内容（可选）
    hidden: ""                  # 暗线内容（可选）
  characters:                   # 出场人物
    - name: ""
      role: protagonist
      function: ""              # 本章功能
  beats: []                     # 节拍列表
  beat_ref:                     # 对应大纲节拍
    act: 1
    sequence: 1
    beats: [1, 2, 3]
```

---

## 五要素摘要

### 1. main_plot（主线推进）

**定义**：本章在主线剧情上推进了什么？

**写法**：一句话概括，15-50 字。

**示例**：
- 主角发现师父的真实身份，决定离开宗门
- 林浩在比赛中击败对手，获得进入内门的资格
- 苏晚发现男主的秘密，两人的关系产生裂痕

### 2. character_change（人物变化）

**定义**：本章中主角/重要角色发生了什么内在变化？

**写法**：从 A 状态变为 B 状态，20-60 字。

**示例**：
- 主角从信任师父变为怀疑一切，开始独立判断
- 女主从逃避变为直面，决定不再隐藏身份
- 配角从旁观者变为参与者，做出关键选择

### 3. foreshadowing（伏笔）

**定义**：本章埋设了什么伏笔？回收了什么伏笔？

**写法**：标注"埋设"或"回收"，说明伏笔内容。

**示例**：
- 【埋设】师父留下的玉佩在月光下发出异光
- 【回收】第 3 章提到的神秘人，本章揭示为男主
- 【埋设】远处传来的钟声，与主角梦境中的钟声相同

### 4. emotion（情绪基调）

**定义**：本章的主导情绪是什么？

**写法**：1-2 个情绪词 + 强度（1-5）。

**示例**：
- 紧张(4) → 释然(2)
- 压抑(3) → 爆发(5)
- 温馨(2) → 不安(3)

### 5. hook（章末钩子）

**定义**：章末留给读者的悬念/期待是什么？

**写法**：一句话描述，让读者想知道"然后呢？"

**示例**：
- 主角打开门，看到不该看到的人
- 系统提示音响起："检测到隐藏任务……"
- 她转过身，嘴角带着一抹意味深长的笑

---

## 多线情节标注

### 主线（main）

**定义**：推动核心剧情的情节线，每章必须推进。

### 副线（sub）

**定义**：感情线、配角线、支线任务等，可隔章推进。

### 暗线（hidden）

**定义**：读者尚未完全察觉的线索，通过伏笔节拍暗示。

---

## 出场人物

### 字段说明

| 字段 | 说明 |
|------|------|
| name | 人物名称 |
| role | 角色类型（protagonist/love_interest/villain/mentor/supporting） |
| function | 本章功能（推动剧情/提供信息/制造冲突/情感支撑） |

### 人物密度控制

| 章节类型 | 出场人数 | 说明 |
|---------|---------|------|
| 独白章 | 1-2 | 聚焦主角内心 |
| 日常章 | 2-4 | 人物关系推进 |
| 群戏章 | 4-8 | 多线交汇/大型事件 |
| 战斗章 | 2-5 | 参战方 + 观战方 |

---

## 字数预算

### 预算分配原则

| 要素 | 占比 | 说明 |
|------|------|------|
| 动作/冲突 | 40-50% | 核心内容 |
| 对话 | 20-30% | 信息交换 |
| 环境/氛围 | 10-15% | 场景锚定 |
| 心理/情绪 | 10-15% | 人物刻画 |
| 过渡/衔接 | 5-10% | 自然连接 |

### 字数范围

| 密度 | 目标字数 | 适用范围 |
|------|---------|---------|
| 极密 | 4000-5000 | 高潮/大战 |
| 密 | 3000-4000 | 冲突/转折 |
| 中 | 2500-3500 | 标准章节 |
| 疏 | 2000-2500 | 过渡/铺垫 |

---

## 质量检查

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | 五要素完整 | 每章都有 main_plot/character_change/emotion/hook |
| 2 | 字数合理 | 2000-5000 字 |
| 3 | 人物明确 | 出场人物列表不为空 |
| 4 | 钩子存在 | 每章末尾有章末钩子 |
| 5 | 主线推进 | main_plot 不为空 |
```

---

## 任务 5.5：编写 references/tension-design.md

### 完整内容

```markdown
# 张力值分配方法

> **用途**：Phase 4 设计张力曲线时对照使用。
> **核心概念**：张力值（1-5）衡量读者在阅读该章时的紧张程度和情绪投入。

---

## 张力值定义

| 值 | 等级 | 读者状态 | 适用场景 |
|----|------|---------|---------|
| 1 | 极低 | 放松、舒适 | 日常铺垫、温馨互动 |
| 2 | 低 | 平静、好奇 | 信息交代、准备阶段 |
| 3 | 中 | 关注、期待 | 冲突酝酿、计划执行 |
| 4 | 高 | 紧张、兴奋 | 激烈冲突、危机时刻 |
| 5 | 极高 | 屏息、震撼 | 高潮爆发、重大转折 |

---

## 张力曲线规则

### 规则 1：波浪形

**核心**：张力不能一条直线，必须像波浪一样起伏。

```
正确：∧∨∧∨∧∨（波浪形）
错误：∧∧∧∧∧∧（全程高压，读者疲劳）
错误：∨∨∨∨∨∨（全程平淡，读者流失）
```

### 规则 2：渐进上升

**核心**：每一"波"的峰值比前一波更高，直到卷高潮。

```
标准模式：
  2-3-2  |  3-4-3  |  4-5-3  |  5
  第一波    第二波    第三波   高潮
```

### 规则 3：相邻平滑

**核心**：相邻章节的张力差不超过 2。

| 当前章张力 | 下章允许范围 |
|-----------|-------------|
| 1 | 1-3 |
| 2 | 1-4 |
| 3 | 1-5 |
| 4 | 2-5 |
| 5 | 3-5 |

**例外**：高潮章后的沉淀章可以从 5 降到 2（读者需要喘息）。

### 规则 4：开篇定位

**核心**：第 1 章张力定在 2-3，不能太低（没钩子）也不能太高（没空间升）。

| 品类 | 建议开篇张力 | 原因 |
|------|------------|------|
| 玄幻/系统 | 3 | 快速冲突，金手指吸引 |
| 都市言情 | 2-3 | 建立情境 + 情感钩子 |
| 悬疑 | 3-4 | 谜团本身就是张力 |
| 日常 | 2 | 慢热铺垫 |

---

## 张力曲线模板

### 短篇（30 章）

```
张力
5 |                    *           *
4 |         *      *     *     *
3 |    *  *   *  *         *  *
2 |  *        *               *
1 | *
  +----------------------------------
    1  5  10  15  20  25  30  章节
```

### 中篇（100 章）

```
张力
5 |         *              *                    *
4 |    *  *   *        *     *              *  *
3 |  *        *      *         *          *
2 | *           *  *              *     *
1 |*              *                  *
  +--------------------------------------------------
    1    20    40    60    80    100  章节
```

---

## 张力值与章节类型映射

| 章节类型 | 张力范围 | 典型值 |
|---------|---------|--------|
| 开篇引入 | 2-3 | 3 |
| 日常铺垫 | 1-2 | 2 |
| 冲突酝酿 | 3-4 | 3 |
| 冲突爆发 | 4-5 | 5 |
| 高潮余波 | 2-3 | 2 |
| 转折章节 | 4-5 | 4 |
| 过渡章节 | 1-2 | 2 |
| 卷终章 | 4-5 | 5 |

---

## 张力曲线设计流程

### Step 1：确定关键节点

在曲线上先标注以下点：
- 开篇（第 1 章）：张力 2-3
- 第一转折点：张力 3-4
- 中点：张力 4
- 第二转折点/黑暗时刻：张力 4-5
- 高潮：张力 5
- 结尾：张力 3-4

### Step 2：填充过渡

在关键节点之间填充过渡章节，形成波浪。

### Step 3：检查曲线

- 是否有连续 3 章以上张力相同？（太平淡）
- 是否有连续 3 章以上张力 >= 4？（太紧张）
- 波浪峰值是否递进？（没有递进 = 结构松散）

### Step 4：微调

根据具体章节内容微调，确保张力值与章节事件匹配。

---

## 常见错误

| 错误 | 表现 | 修正 |
|------|------|------|
| 平原曲线 | 全篇 2-3，无起伏 | 增加高潮章，提升波峰 |
| 过山车曲线 | 1→5→1→5 频繁跳 | 加入过渡章节平滑 |
| 高开低走 | 开篇 5，后面全 2 | 开篇降为 2-3，给上升留空间 |
| 无递进 | 每波峰值相同 | 后一波峰值比前一波高 0.5-1 |

---

## 质量检查

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | 波浪形 | 有明显起伏，非直线 |
| 2 | 递进性 | 每波峰值 >= 前一波 |
| 3 | 平滑性 | 相邻章张力差 ≤ 2 |
| 4 | 开篇定位 | 第 1 章张力 2-3 |
| 5 | 高潮到位 | 全书/卷最高张力 = 5 |
```

---

## 任务 5.6：编写 scripts/check-chapters.js

### 完整内容

```javascript
#!/usr/bin/env node
// check-chapters.js — 章节计划质量检查
// Usage: node check-chapters.js <chapters_index.yaml>

const fs = require('fs');
const yaml = require('js-yaml');

// 常量定义
const MIN_BEATS = 3;
const MAX_BEATS = 15;
const MIN_WORDS = 2000;
const MAX_WORDS = 5000;
const MIN_TENSION = 1;
const MAX_TENSION = 5;
const MAX_SAME_DENSITY = 3;  // 不允许连续超过此数量的同密度章节

// 必填字段
const REQUIRED_FIELDS = ['number', 'title', 'summary', 'tension', 'words_target', 'beats', 'characters'];

function main() {
  const file = process.argv[2];
  if (!file) {
    console.error('Usage: node check-chapters.js <chapters_index.yaml>');
    process.exit(2);
  }

  let data;
  try {
    data = yaml.load(fs.readFileSync(file, 'utf8'));
  } catch (err) {
    console.error(`无法读取文件: ${file}`);
    process.exit(2);
  }

  const chapters = data.chapters;
  if (!chapters || !Array.isArray(chapters) || chapters.length === 0) {
    console.error('[blocking] chapters 为空或不存在');
    process.exit(1);
  }

  const findings = [];

  // 检查每章
  for (const ch of chapters) {
    const chNum = ch.number || '?';

    // 必填字段检查
    for (const field of REQUIRED_FIELDS) {
      if (ch[field] === undefined || ch[field] === null || ch[field] === '') {
        findings.push({
          severity: 'blocking',
          chapter: chNum,
          message: `第 ${chNum} 章缺少必填字段: ${field}`,
        });
      }
    }

    // 节拍数检查
    const beats = ch.beats || [];
    if (beats.length < MIN_BEATS) {
      findings.push({
        severity: 'blocking',
        chapter: chNum,
        message: `第 ${chNum} 章节拍数不足: ${beats.length}（最少 ${MIN_BEATS}）`,
      });
    }
    if (beats.length > MAX_BEATS) {
      findings.push({
        severity: 'advisory',
        chapter: chNum,
        message: `第 ${chNum} 章节拍数过多: ${beats.length}（最多 ${MAX_BEATS}）`,
      });
    }

    // 字数检查
    const words = ch.words_target || 0;
    if (words < MIN_WORDS) {
      findings.push({
        severity: 'blocking',
        chapter: chNum,
        message: `第 ${chNum} 章字数过少: ${words}（最少 ${MIN_WORDS}）`,
      });
    }
    if (words > MAX_WORDS) {
      findings.push({
        severity: 'advisory',
        chapter: chNum,
        message: `第 ${chNum} 章字数过多: ${words}（最多 ${MAX_WORDS}）`,
      });
    }

    // 张力值检查
    const tension = ch.tension || 0;
    if (tension < MIN_TENSION || tension > MAX_TENSION) {
      findings.push({
        severity: 'blocking',
        chapter: chNum,
        message: `第 ${chNum} 章张力值越界: ${tension}（范围 ${MIN_TENSION}-${MAX_TENSION}）`,
      });
    }

    // 摘要检查
    if (ch.summary && typeof ch.summary === 'object') {
      if (!ch.summary.main_plot && !ch.summary.hook) {
        findings.push({
          severity: 'advisory',
          chapter: chNum,
          message: `第 ${chNum} 章摘要缺少 main_plot 或 hook`,
        });
      }
    }
  }

  // 密度连续性检查
  if (chapters.length >= MAX_SAME_DENSITY) {
    for (let i = 0; i <= chapters.length - MAX_SAME_DENSITY; i++) {
      const densities = chapters.slice(i, i + MAX_SAME_DENSITY).map(c => c.density);
      if (densities.length === MAX_SAME_DENSITY && densities.every(d => d === densities[0]) && densities[0] != null) {
        findings.push({
          severity: 'advisory',
          chapter: chapters[i].number,
          message: `第 ${chapters[i].number}-${chapters[i + MAX_SAME_DENSITY - 1].number} 章连续 ${MAX_SAME_DENSITY} 章密度为"${densities[0]}"，建议调整`,
        });
      }
    }
  }

  // 相邻张力差检查
  for (let i = 1; i < chapters.length; i++) {
    const prev = chapters[i - 1].tension;
    const curr = chapters[i].tension;
    if (prev != null && curr != null && Math.abs(curr - prev) > 2) {
      findings.push({
        severity: 'advisory',
        chapter: chapters[i].number,
        message: `第 ${chapters[i - 1].number}→${chapters[i].number} 章张力跳变过大: ${prev}→${curr}（差值 ${Math.abs(curr - prev)}）`,
      });
    }
  }

  // 输出结果
  if (findings.length === 0) {
    console.log(`✓ 章节计划检查通过（共 ${chapters.length} 章）`);
    process.exit(0);
  }

  for (const f of findings) {
    console.log(`[${f.severity}] 第 ${f.chapter} 章: ${f.message}`);
  }

  const hasBlocking = findings.some(f => f.severity === 'blocking');
  if (hasBlocking) {
    console.log(`\n✗ 发现 ${findings.filter(f => f.severity === 'blocking').length} 个阻断问题，需修复`);
    process.exit(1);
  } else {
    console.log(`\n△ 发现 ${findings.length} 个建议，可酌情调整`);
    process.exit(0);
  }
}

main();
```

---

## 执行顺序

1. 创建目录结构
2. 编写 SKILL.md
3. 编写 chapter-beat-guide.md
4. 编写 chapter-template.md
5. 编写 tension-design.md
6. 编写 check-chapters.js
7. 验证脚本可运行
8. Commit

---

## 下一步

design-chapters 完成后，进入 Phase 6 (golden-chapters)：黄金三章锻造。
