# Phase 2 执行计划：worldbuilding（世界观设计）

> **执行目标**：完整重写 worldbuilding skill，包含 SKILL.md + 4 references + 1 script

---

## 文件清单

| 文件 | 行数估计 | 职责 |
|------|---------|------|
| `.agents/skills/worldbuilding/SKILL.md` | ~180 行 | 主流程：5 Phase + 品类适配 |
| `.agents/skills/worldbuilding/references/power-system-guide.md` | ~200 行 | 力量体系设计方法论 |
| `.agents/skills/worldbuilding/references/social-structure.md` | ~150 行 | 社会结构设计 |
| `.agents/skills/worldbuilding/references/world-rules.md` | ~150 行 | 基础规则设计 |
| `.agents/skills/worldbuilding/references/genre-worldbuilding.md` | ~200 行 | 品类×世界观适配矩阵 |
| `.agents/skills/worldbuilding/scripts/check-completeness.js` | ~100 行 | 世界观完整性检查 |

---

## 任务 2.1：创建目录结构

```bash
mkdir -p .agents/skills/worldbuilding/references
mkdir -p .agents/skills/worldbuilding/scripts
```

---

## 任务 2.2：编写 SKILL.md

### 完整内容

```markdown
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

- `settings/worldbuilding.yaml`：世界观设定（对齐 data/schemas/worldbuilding.schema.yaml）

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
```

---

## 任务 2.3：编写 references/genre-worldbuilding.md

### 完整内容

```markdown
# 品类×世界观适配矩阵

> **用途**：Phase 1 根据品类加载对应框架。

---

## 玄幻修仙

### 必需要素
- **power_system**：修炼等级（练气→筑基→金丹→元婴→化神...）、功法分类、战斗表现
- **factions**：宗门/家族/势力（≥3 个）、势力关系、地盘划分
- **locations**：秘境、城市、宗门所在地

### 设计重点
- 力量等级必须清晰，不能后期崩坏
- 升级条件要明确（资源/悟性/机缘）
- 宗门层级（外门/内门/核心/长老/掌门）

### 模板
```yaml
power_system:
  name: 修仙体系
  type: 修炼
  ranks:
    - name: 练气期
      capabilities: 基础法术
      breakthrough: 灵石+悟性
    - name: 筑基期
      capabilities: 御剑飞行
      breakthrough: 筑基丹
    # ... 更多等级
  rules: 灵气浓度影响修炼速度
  limitations: 渡劫失败会陨落
```

---

## 都市言情

### 必需要素
- **era_details**：时代背景（2009/2015/现代...）、社会特征、科技水平
- **locations**：城市、学校、公司、标志性地点
- **social_rules**：社交规则、阶层差异、行业规则

### 设计重点
- 时代细节要准确（物价、科技、流行文化）
- 地点要有真实感（可虚构但要有原型）
- 社交规则要符合现实逻辑

### 模板
```yaml
era_details:
  year: 2009
  characteristics:
    - 智能手机刚普及
    - 微博兴起
    - 房价开始上涨
locations:
  - name: 合工大
    type: 大学
    description: 主场景，校园日常
factions: []  # 都市可不设势力
```

---

## 系统文

### 必需要素
- **system_rules**：系统名称、激活条件、功能
- **quest_mechanics**：任务类型、奖励机制、惩罚机制
- **reward_system**：奖励分类、升级曲线

### 设计重点
- 系统规则要自洽（为什么有系统？限制是什么？）
- 任务设计要有层次感（日常/主线/隐藏）
- 奖励要有吸引力但不能太无敌

### 模板
```yaml
system_rules:
  name: 全能系统
  activation: 意外触发
  functions: [任务发布, 奖励发放, 技能兑换]
quest_mechanics:
  daily_quests: 简单任务，稳定奖励
  main_quests: 推动剧情，高奖励
  hidden_quests: 触发条件特殊，稀有奖励
reward_system:
  currency: 积分
  exchange: 技能/道具/属性点
```

---

## 悬疑推理

### 必需要素
- **crime_rules**：犯罪类型、作案手法、破案逻辑
- **investigation_procedures**：调查流程、证据链、推理方法
- **suspect_pool**：嫌疑人列表、动机、不在场证明

### 设计重点
- 推理逻辑要严密
- 证据链要完整
- 嫌疑人动机要合理

---

## 品类适配检查清单

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | 品类识别正确 | 已根据 scout_report.yaml 选择框架 |
| 2 | 必需要素完整 | required 中的元素都已设计 |
| 3 | 自洽性 | 各要素之间没有矛盾 |
| 4 | 服务于剧情 | 设定能支撑后续剧情发展 |
```

---

## 任务 2.4：编写 references/power-system-guide.md

### 完整内容

```markdown
# 力量体系设计方法论

> **用途**：Phase 2 设计力量体系时对照使用。
> **适用**：玄幻、仙侠、系统文等需要力量等级的品类。

---

## 设计原则

1. **等级清晰**：读者能明确知道谁强谁弱
2. **升级有条件**：不能想升就升，要有条件/代价
3. **战斗有策略**：不是纯数值碾压，要有策略空间
4. **后期不崩**：等级体系能支撑长篇连载

---

## 等级设计模板

### 经典修仙体系（9 级）
| 等级 | 特征 | 寿元 | 突破条件 |
|------|------|------|---------|
| 练气 | 基础法术 | 100 | 灵石 |
| 筑基 | 御剑飞行 | 200 | 筑基丹 |
| 金丹 | 分身术 | 500 | 金丹天劫 |
| 元婴 | 瞬移 | 1000 | 元婴天劫 |
| 化神 | 领域 | 2000 | 领悟天道 |
| 炼虚 | 空间法则 | 5000 | 虚空试炼 |
| 合体 | 合体技 | 10000 | 天劫 |
| 大乘 |  quasi-仙 | 50000 | 仙劫 |
| 真仙 | 仙人 | ∞ | 飞升 |

### 都市异能体系（5 级）
| 等级 | 特征 | 比例 |
|------|------|------|
| F | 微弱异能 | 90% |
| E | 实用级 | 8% |
| D | 精英级 | 1.5% |
| C | 大师级 | 0.4% |
| B-A-S | 传说级 | 0.1% |

---

## 升级条件设计

| 类型 | 示例 | 优点 | 缺点 |
|------|------|------|------|
| 资源型 | 灵石/丹药/金币 | 清晰直观 | 容易变成打怪升级 |
| 悟性型 | 领悟/突破/顿悟 | 有爽感 | 难写 |
| 任务型 | 完成系统任务 | 有目标感 | 太游戏化 |
| 代价型 | 献祭/牺牲 | 有戏剧性 | 太虐 |

**建议**：混合使用，不同等级用不同条件

---

## 战斗表现设计

| 等级差 | 表现 | 示例 |
|--------|------|------|
| 同级 | 激烈对战 | 双方各有胜负手 |
| 差 1 级 | 苦战但能赢 | 主角靠策略/底牌 |
| 差 2 级 | 勉强自保 | 逃跑/求援 |
| 差 3+ 级 | 碾压 | 一招秒杀 |

**关键**：让读者感受到等级差距的压迫感

---

## 常见坑

| 坑 | 表现 | 解决 |
|----|------|------|
| 等级崩坏 | 后期等级不值钱 | 前期控制升级速度 |
| 战力膨胀 | 动辄毁天灭地 | 限制高战力出手条件 |
| 打脸疲劳 | 总是扮猪吃虎 | 变换打脸方式 |

---

## 质量检查

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | 等级数量 | 5-9 级为宜 |
| 2 | 升级条件 | 每级都有明确条件 |
| 3 | 战斗表现 | 能感受到等级差距 |
| 4 | 限制与代价 | 有使用限制，不是无敌 |
| 5 | 自洽性 | 等级之间没有矛盾 |
```

---

## 任务 2.5：编写 references/social-structure.md

### 完整内容

```markdown
# 社会结构设计

> **用途**：Phase 3 设计社会结构时对照使用。

---

## 设计原则

1. **服务于冲突**：社会结构要能制造冲突
2. **有流动性**：阶层可以流动（不然主角怎么逆袭？）
3. **有规则**：社会有自己的规则，角色要遵守或打破

---

## 势力设计模板

### 势力卡
```yaml
faction:
  name: 势力名称
  type: 宗门/家族/公司/组织
  strength: 强/中/弱
  territory: 地盘
  key_figures:
    - name:  leader
      role: 掌门
    - name: xxx
      role: 长老
  goals: 目标
  conflicts: 与其他势力的矛盾
```

### 势力关系矩阵
| | 势力A | 势力B | 势力C |
|---|-------|-------|-------|
| 势力A | — | 敌对 | 同盟 |
| 势力B | 敌对 | — | 中立 |
| 势力C | 同盟 | 中立 | — |

---

## 社会规则设计

| 类型 | 示例 | 冲突来源 |
|------|------|---------|
| 阶层规则 | 贵族/平民不可通婚 | 主角打破规则 |
| 行业规则 | 炼丹师必须加入公会 | 主角独立发展 |
| 禁忌 | 禁止研究禁术 | 主角不得不研究 |

---

## 质量检查

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | 势力数量 | ≥ 3 个 |
| 2 | 势力关系 | 有明确的敌对/同盟/中立 |
| 3 | 冲突来源 | 势力之间有明显矛盾 |
| 4 | 流动性 | 主角有可能改变现状 |
```

---

## 任务 2.6：编写 references/world-rules.md

### 完整内容

```markdown
# 基础规则设计

> **用途**：Phase 4 设计世界运行规则时对照使用。

---

## 设计原则

1. **核心规则少而精**：3-5 条核心规则足矣
2. **规则有代价**：使用规则要有代价
3. **规则可被打破**：但打破要有后果

---

## 规则设计模板

```yaml
world_rules:
  core_rules:
    - rule: 规则描述
      exception: 例外情况
      cost: 使用代价
    - rule: ...
  taboos:
    - 禁忌描述
    - 违反后果
```

---

## 示例

### 修仙世界
```yaml
core_rules:
  - rule: 灵气是修炼基础
    exception: 某些秘境灵气稀薄
    cost: 灵气枯竭会跌落境界
  - rule: 渡劫才能升级
    exception: 特殊体质可免劫
    cost: 渡劫失败会陨落
taboos:
  - 弑师：被天下唾弃
  - 使用禁术：折寿
```

### 都市重生
```yaml
core_rules:
  - rule: 历史会按原样发生
    exception: 主角改变了关键节点
    cost: 改变越大，蝴蝶效应越强
taboos:
  - 暴露重生身份：被当成疯子
  - 过度改变历史：失去先知优势
```

---

## 质量检查

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | 规则数量 | 3-5 条核心规则 |
| 2 | 自洽性 | 规则之间没有矛盾 |
| 3 | 有代价 | 使用规则有代价 |
| 4 | 服务于剧情 | 规则能制造冲突 |
```

---

## 任务 2.7：编写 scripts/check-completeness.js

### 完整内容

```javascript
#!/usr/bin/env node
// check-completeness.js — 世界观完整性检查
// Usage: node check-completeness.js <scout_report.yaml> <worldbuilding.yaml>

const fs = require('fs');
const yaml = require('js-yaml');

function main() {
  const scoutFile = process.argv[2];
  const worldFile = process.argv[3];

  if (!scoutFile || !worldFile) {
    console.error('Usage: node check-completeness.js <scout_report.yaml> <worldbuilding.yaml>');
    process.exit(2);
  }

  const scout = yaml.load(fs.readFileSync(scoutFile, 'utf8'));
  const world = yaml.load(fs.readFileSync(worldFile, 'utf8'));

  const required = scout.required_elements?.worldbuilding?.required || [];
  const findings = [];

  for (const elem of required) {
    if (!world[elem] || isEmpty(world[elem])) {
      findings.push({
        severity: 'blocking',
        message: `缺少必需的世界观元素: ${elem}`,
      });
    }
  }

  if (findings.length === 0) {
    console.log('✓ 世界观完整性检查通过');
    process.exit(0);
  }

  for (const f of findings) {
    console.log(`[${f.severity}] ${f.message}`);
  }
  process.exit(1);
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
3. 编写 genre-worldbuilding.md
4. 编写 power-system-guide.md
5. 编写 social-structure.md
6. 编写 world-rules.md
7. 编写 check-completeness.js
8. 验证脚本可运行
9. Commit
