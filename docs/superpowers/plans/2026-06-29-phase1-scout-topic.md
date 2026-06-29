# Phase 1 执行计划：scout-topic（选题侦察）

> **执行目标**：完整重写 scout-topic skill，包含 SKILL.md + 4 references + 1 script

---

## 文件清单

| 文件 | 行数估计 | 职责 |
|------|---------|------|
| `.agents/skills/scout-topic/SKILL.md` | ~200 行 | 主流程：5 Phase + 质量门禁 + 断点恢复 |
| `.agents/skills/scout-topic/references/genre-catalog.md` | ~480 行 | 品类框架速查（从 oh-story 复用改写） |
| `.agents/skills/scout-topic/references/platform-profiles.md` | ~200 行 | 各平台读者画像 + 调性差异 |
| `.agents/skills/scout-topic/references/topic-decision.md` | ~150 行 | 选题决策方法论 |
| `.agents/skills/scout-topic/references/tag-strategy.md` | ~150 行 | 标签组合策略 |
| `.agents/skills/scout-topic/scripts/check-tags.js` | ~150 行 | 标签冲突/饱和度检测 |

---

## 任务 1.1：创建目录结构

```bash
mkdir -p .agents/skills/scout-topic/references
mkdir -p .agents/skills/scout-topic/scripts
```

---

## 任务 1.2：编写 SKILL.md

### 完整内容

```markdown
---
name: scout-topic
description: 品类选择 + 选题分析。开新书或找题材时使用。
---

# scout-topic（选题侦察）

> **用途**：帮助用户选择品类、分析目标平台、制定选题策略。
> **前置条件**：项目已创建（`novel new` 或已有项目目录）。
> **输出文件**：`settings/scout_report.yaml`

---

## 核心原则

1. **数据驱动**：基于平台榜单数据和品类分析，不凭感觉选。
2. **品类先行**：先定品类，再定题材，最后定标签。
3. **差异化**：同质化方向不选，必须有差异化定位。
4. **可行性**：样本不足给"中"，不给"高"。内置知识模式一律"中"。

---

## Phase 定义

### Phase 1：品类定位

**入口条件**：项目已创建
**目标**：确定品类（玄幻/都市/系统/言情/其他）

**步骤**：
1. 读取 `references/genre-catalog.md`，向用户展示品类路由表
2. 询问用户倾向的品类方向
3. 根据用户回答，展示该品类的核心机制、结构节点、关键维度
4. 确认品类选择，记录到 `scout_report.yaml` 的 `genre` 字段

**出口条件**：`genre` 字段已填写
**加载 References**：`genre-catalog.md`

---

### Phase 2：平台分析

**入口条件**：品类已确定
**目标**：确定目标平台 + 了解平台调性

**步骤**：
1. 读取 `references/platform-profiles.md`，展示各平台特点
2. 询问用户目标平台（番茄/起点/晋江/其他）
3. 展示该平台的目标读者画像、内容调性、付费模式
4. 确认平台选择，记录到 `scout_report.yaml` 的 `platform` 和 `target_audience` 字段

**出口条件**：`platform` 和 `target_audience` 字段已填写
**加载 References**：`platform-profiles.md`

---

### Phase 3：选题决策

**入口条件**：平台已确定
**目标**：基于品类+平台，产出具体的选题方向

**步骤**：
1. 读取 `references/topic-decision.md`
2. 按"选题四步"引导用户：
   - 能爆的原因（先当假设）
   - 市场验证（榜单样本）
   - 差异化定位
   - 可行性 + 风险 + 验证动作
3. 产出 2-3 个选题方向，写入 `scout_report.yaml` 的 `premise` 和 `core_hooks`

**出口条件**：`premise` 和 `core_hooks` 已填写
**加载 References**：`topic-decision.md`

---

### Phase 4：标签策略

**入口条件**：选题方向已确定
**目标**：制定标签组合策略

**步骤**：
1. 读取 `references/tag-strategy.md`
2. 分析目标品类的热门标签 + 竞争度
3. 设计标签组合（3-6 个主要标签 + 次要标签）
4. 运行 `scripts/check-tags.js` 验证标签组合
5. 确认标签，记录到 `scout_report.yaml` 的 `recommended_tags` 和 `tag_analysis`

**出口条件**：标签组合已通过 check-tags.js 验证
**加载 References**：`tag-strategy.md`

---

### Phase 5：品类感知配置

**入口条件**：标签已确定
**目标**：引导用户填写 `required_elements`，供后续 skill 做质量门禁

**步骤**：
1. 根据已选品类，展示该品类的默认 `required_elements`（见 spec Section 10.6）
2. 询问用户是否需要调整（增删必需/可选元素）
3. 确认并写入 `scout_report.yaml` 的 `required_elements` 字段

**出口条件**：`required_elements` 已填写
**加载 References**：无（使用内置品类默认值）

**品类默认值参考**：

| 品类 | worldbuilding.required | characters | opening_hook.type | structure.type |
|------|------------------------|------------|-------------------|----------------|
| xuanhuan | power_system, factions, locations | protagonist+mentor+villain | golden_finger | 三幕式 |
| urban | era_details, locations, social_rules | protagonist+supporting_cast | conflict | 起承转合 |
| system | system_rules, quest_mechanics | protagonist+system_entity | golden_finger | 三幕式 |
| romance | locations, relationship_context | protagonist+love_interest | meet_cute | 起承转合 |

---

### Phase 6：报告定稿

**入口条件**：所有字段已填写
**目标**：生成完整的 scout_report.yaml

**步骤**：
1. 汇总所有字段，展示给用户确认
2. 如有遗漏，提示补充
3. 写入 `settings/scout_report.yaml`
4. 清理 `_progress.md`（如存在）

**出口条件**：scout_report.yaml 已生成
**加载 References**：无

---

## 质量门禁

本 skill 无自动化脚本门禁，但有以下检查：

- Phase 4 使用 `check-tags.js` 验证标签组合无冲突
- Phase 5 确保 `required_elements` 至少声明了 worldbuilding、characters、opening_hook、structure

---

## 断点恢复

**状态文件**：`_progress.md`（位于小说项目根目录）

**格式**：
```markdown
# scout-topic Progress
- current_phase: <1-6>
- status: in_progress | completed
- last_updated: <timestamp>
```

**恢复逻辑**：
- 启动时检查 `_progress.md`
- 若存在且 status != completed，提示用户是否继续上次进度
- 跳到对应 Phase 继续执行

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

## 下一步

scout_report.yaml 生成后，可进入：
- `/worldbuilding`：世界观设计
- `/design-character`：人设设计
```

---

## 任务 1.3：编写 references/genre-catalog.md

> **来源**：直接复制 oh-story-claudecode 的 `skills/story-long-write/references/genre-catalog.md`
> **行数**：约 480 行
> **内容**：品类框架速查（追妻火葬场、重生复仇、仙侠/玄幻、都市高武、文娱/娱乐圈等 20+ 品类）

```bash
cp other/oh-story-claudecode/skills/story-long-write/references/genre-catalog.md \
   .agents/skills/scout-topic/references/genre-catalog.md
```

---

## 任务 1.4：编写 references/platform-profiles.md

### 完整内容

```markdown
# 平台画像手册

> **用途**：Phase 2 选择目标平台时对照使用。

---

## 平台总览

| 平台 | 调性 | 核心读者 | 付费模式 | 内容偏好 |
|------|------|---------|---------|---------|
| 番茄小说 | 免费+广告 | 下沉市场、碎片化阅读 | 免费（广告分成） | 快节奏、强钩子、爽点密集 |
| 起点中文网 | 付费订阅 | 核心网文读者、愿意付费 | 千字付费（5分/千字） | 深度剧情、世界观完整、文笔可稍慢 |
| 晋江文学城 | 付费订阅 | 女性读者为主 | VIP 章节付费 | 感情线细腻、人设鲜明、HE 偏好 |
| 七猫小说 | 免费+广告 | 下沉市场、中老年读者 | 免费（广告分成） | 接地气、世情、家庭伦理 |
| 刺猬猫 | 付费订阅 | 二次元向、同人爱好者 | 章节付费 | 二次元梗、同人、轻小说风格 |

---

## 番茄小说

### 读者画像
- 年龄：18-35 岁为主
- 场景：通勤、睡前、碎片时间
- 特征：耐心有限，前 3 章不吸引就弃书

### 内容调性
- **开篇**：300 字内必须出冲突/钩子
- **节奏**：每 2000 字至少一个爽点/反转
- **钩子密度**：章末必须有悬念
- **篇幅**：单章 2000-3000 字为宜

### 付费模式影响
- 免费模式 → 靠广告分成 → 需要高阅读量
- 高阅读量 = 强钩子 + 快节奏 + 持续爽点
- 不用考虑"深度铺垫"，读者没耐心

### 热门标签（男频）
重生、都市、系统、赘婿、神医、战神、金手指、逆袭

### 热门标签（女频）
穿越、重生、宫斗、甜宠、复仇、豪门、娱乐圈

---

## 起点中文网

### 读者画像
- 年龄：20-40 岁
- 特征：核心网文读者，愿意为好书付费，对质量有要求

### 内容调性
- **开篇**：可以稍慢，但前 10 章必须建立核心设定
- **节奏**：允许铺垫，但每章必须有信息增量
- **世界观**：必须完整自洽，读者会考据
- **篇幅**：单章 3000-5000 字

### 付费模式影响
- 千字付费 → 读者会计算性价比
- 水字数会被骂 → 每段都要有信息量
- 可以写长，但不能写水

### 热门标签
玄幻、仙侠、都市、历史、科幻、游戏、体育

---

## 晋江文学城

### 读者画像
- 年龄：18-35 岁女性为主
- 特征：重视感情线、人设、HE

### 内容调性
- **感情线**：必须细腻，男女主互动是核心
- **人设**：鲜明、有记忆点
- **结局**：HE（Happy Ending）偏好强烈
- **篇幅**：单章 3000-4000 字

### 热门标签
言情、耽美、穿越、重生、宫斗、娱乐圈、校园、仙侠

---

## 七猫小说

### 读者画像
- 年龄：30-50 岁，下沉市场
- 特征：喜欢接地气、贴近生活的故事

### 内容调性
- **题材**：世情、家庭伦理、乡村、都市生活
- **语言**：通俗易懂，少用网文梗
- **节奏**：中等，不需要太快

### 热门标签
都市、乡村、家庭、伦理、情感

---

## 刺猬猫

### 读者画像
- 年龄：15-30 岁，二次元向
- 特征：喜欢二次元梗、同人、轻小说风格

### 内容调性
- **二次元梗**：大量使用，读者会 get
- **同人**：已有 IP 的同人创作
- **轻小说**：日式轻小说风格

### 热门标签
同人、二次元、轻小说、穿越、系统

---

## 平台选择决策树

```
你的目标读者是谁？
├─ 下沉市场、碎片化阅读 → 番茄/七猫
│  └─ 男频 → 番茄
│  └─ 中老年/世情 → 七猫
├─ 核心网文读者、愿意付费 → 起点
│  └─ 男频 → 起点
├─ 女性读者、重视感情线 → 晋江
└─ 二次元/同人 → 刺猬猫
```

---

## 质量检查

选完平台后，核对：

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | 了解平台调性 | 能说出该平台的开篇节奏、钩子密度要求 |
| 2 | 了解付费模式 | 知道该平台的付费方式及其对内容的影响 |
| 3 | 标签匹配 | 选择的标签在该平台是热门标签 |
| 4 | 读者画像清晰 | 能描述目标读者的年龄、场景、特征 |
```

---

## 任务 1.5：编写 references/topic-decision.md

> **来源**：复制 oh-story-claudecode 的 `skills/story-long-scan/references/topic-decision.md` 并改写
> **行数**：约 80 行
> **内容**：选题决策方法论（选题四步、可行性判断、决策模板）

### 完整内容

```markdown
# 选题决策：从数据到"写什么能爆"

把市场数据变成能直接用的选题建议：**推荐写什么、为什么能爆、行不行、怎么验证**。

---

## 决策路由

| 你在做什么 | 看这节 |
|-----------|--------|
| 把市场数据变成选题建议 | 选题四步 |
| 判断一个方向行不行 | 可行性判断 |
| 没联网/没榜单数据 | 内置知识模式 |
| 落盘交付 | 选题报告模板 |

---

## 选题四步

每个推荐选题都走完这四步，缺一不可：

1. **能爆的原因（先当假设）**：从重复出现的样本（排除单本个例）+ 新元素提取，推出"这个方向能爆，依靠 X 结构/梗/人设吃这波读者"。单本上榜只是个例。这里只写假设，标 `待验证`。

2. **市场验证**：同方向有几本 + 趋势（↑/→/↓）+ 反例（同方向有没有扑街的）。样本越多、趋势越稳，越可信。

3. **差异化定位**：作者优势 × 市场缺口 = "你的版本和现有的不同在哪"。没有差异化 = 同质化挤不进去。

4. **可行性 + 风险 + 验证动作**：给出可行性高/中/低、最可能的失败点、开写前怎么低成本验证。

---

## 可行性判断

分三档；样本不够时不许给"高"：

| 可行性 | 含义 | 条件 |
|--------|------|------|
| 高 | 可放心写 | 同方向样本够（≥15）+ 趋势↑或→ + 素材能撑 + 有差异化空间 |
| 中 | 可写但先验证 | 样本够但趋势↓ / 或差异化不清 / 或素材半撑 |
| 低 | 不建议 | 已饱和（扑街多）/ 或素材撑不住 / 或平台调性不符 |

**硬规则**：数据稀疏（有效样本 < 15）时，不许给"高"，强制降到"中"。

**内置知识模式**：无榜单、纯凭知识库时，所有方向一律给"中"。

---

## 选题报告模板

输出到 `scout_report.yaml`，核心字段：

```yaml
premise: 一句话前提（50字以上）
core_hooks:
  - name: 钩子名称
    description: 描述
    hook_type: 钩子类型
competition_analysis:
  overall_competition: 0.5  # 0-1
  overall_potential: 0.8    # 0-1
  reasoning: 分析理由
  market_window: 市场窗口判断
```
```

---

## 任务 1.6：编写 references/tag-strategy.md

### 完整内容

```markdown
# 标签组合策略

> **用途**：Phase 4 设计标签组合时对照使用。

---

## 标签分类

| 类型 | 定义 | 示例 |
|------|------|------|
| 流量标签 | 搜索量大，自带流量 | 重生、都市、系统 |
| 精准标签 | 圈定核心读者 | 文娱、副本、文抄公 |
| 差异化标签 | 区别于同类作品 | 脑洞、歌曲副本 |
| 场景标签 | 故事发生场景 | 校园、豪门、末世 |
| 爽点标签 | 明确爽文预期 | 金手指、逆袭、打脸 |

---

## 组合策略

### 3-6 个主要标签

```
1 个流量标签 + 1-2 个精准标签 + 1 个差异化标签 + 1-2 个场景/爽点标签
```

**示例**（都市文娱）：
- 流量：重生、都市
- 精准：文娱
- 差异化：脑洞
- 场景：校园
- 爽点：金手指、逆袭

组合：`重生, 文娱, 多女主, 脑洞, 校园, 金手指`

---

## 竞争度评估

| 竞争度 | 含义 | 判断标准 |
|--------|------|---------|
| 高 | 同类作品多 | 标签在平台作品数 > 5000 |
| 中 | 有一定竞争 | 1000-5000 |
| 低 | 竞争小 | < 1000 |

**策略**：
- 流量标签必然高竞争，但必须有
- 差异化标签应该是低竞争
- 整体组合不要全是高竞争

---

## 饱和度判断

**过饱和**：标签组合中 > 3 个高竞争标签 = 过饱和，难出头

**解决**：
1. 增加差异化标签
2. 换精准标签（更细分）
3. 调整题材方向

---

## 质量检查

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | 标签数量 | 主要标签 3-6 个 |
| 2 | 流量标签 | 至少 1 个 |
| 3 | 差异化标签 | 至少 1 个 |
| 4 | 无冲突 | 纯爱≠后宫，BE≠HE |
| 5 | 不过饱和 | 高竞争标签 ≤ 3 个 |
```

---

## 任务 1.7：编写 scripts/check-tags.js

### 完整内容

```javascript
#!/usr/bin/env node
// check-tags.js — 标签组合冲突/饱和度检测
// Usage: node check-tags.js <scout_report.yaml>

const fs = require('fs');
const yaml = require('js-yaml');

// 标签冲突表（互斥标签组合）
const CONFLICTS = [
  ['纯爱', '后宫'],
  ['纯爱', '多女主'],
  ['BE', 'HE'],
  ['爽文', '虐文'],
  ['日常', '热血'],
];

// 饱和度阈值（标签在同平台作品数超过此值 = 过饱和）
const SATURATION_THRESHOLD = 5000;

function main() {
  const file = process.argv[2];
  if (!file) {
    console.error('Usage: node check-tags.js <scout_report.yaml>');
    process.exit(2);
  }

  const report = yaml.load(fs.readFileSync(file, 'utf8'));
  const tags = report.recommended_tags?.primary || [];
  const platform = report.platform || '';

  const findings = [];

  // 检查冲突
  for (const [a, b] of CONFLICTS) {
    if (tags.includes(a) && tags.includes(b)) {
      findings.push({
        severity: 'blocking',
        type: 'conflict',
        message: `标签冲突: "${a}" 和 "${b}" 互斥`,
      });
    }
  }

  // 检查饱和度（需要平台数据，这里简化处理）
  // TODO: 接入实际平台数据
  // for (const tag of tags) {
  //   const count = getPlatformTagCount(platform, tag);
  //   if (count > SATURATION_THRESHOLD) {
  //     findings.push({
  //       severity: 'advisory',
  //       type: 'saturation',
  //       message: `标签 "${tag}" 在 ${platform} 作品数 ${count}，可能过饱和`,
  //     });
  //   }
  // }

  // 输出结果
  if (findings.length === 0) {
    console.log('✓ 标签组合无冲突');
    process.exit(0);
  }

  for (const f of findings) {
    console.log(`[${f.severity}] ${f.message}`);
  }

  const hasBlocking = findings.some(f => f.severity === 'blocking');
  process.exit(hasBlocking ? 1 : 0);
}

main();
```

---

## 执行顺序

1. 创建目录结构
2. 编写 SKILL.md
3. 编写 genre-catalog.md（最大，约 480 行）
4. 编写 platform-profiles.md
5. 编写 topic-decision.md
6. 编写 tag-strategy.md
7. 编写 check-tags.js
8. 验证脚本可运行
9. Commit

---

## 下一步

Phase 1 完成后，进入 Phase 2 (worldbuilding) 或 Phase 3 (design-character)，可并行。
