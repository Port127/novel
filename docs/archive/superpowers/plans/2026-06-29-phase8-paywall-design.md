# Phase 8 执行计划：paywall-design（付费卡点设计）

> **执行目标**：完整重写 paywall-design skill，包含 SKILL.md + 4 references + 1 script
> **核心价值**：卡点选错，读者全跑。好的卡点 = 爽点兑现 + 致命悬念。

---

## 文件清单

| 文件 | 行数估计 | 职责 |
|------|---------|------|
| `.agents/skills/paywall-design/SKILL.md` | ~150 行 | 主流程：卡点分析 + 过渡章设计 + 验证 |
| `.agents/skills/paywall-design/references/paywall-psychology.md` | ~150 行 | 读者付费心理 |
| `.agents/skills/paywall-design/references/cut-point-method.md` | ~150 行 | 卡点选择方法论 |
| `.agents/skills/paywall-design/references/transition-guide.md` | ~150 行 | 过渡章设计（免费末章+付费首章） |
| `.agents/skills/paywall-design/references/platform-paywall.md` | ~150 行 | 平台付费模式 |
| `.agents/skills/paywall-design/scripts/check-paywall.js` | ~100 行 | 卡点验证脚本 |

---

## 任务 8.1：创建目录结构

```bash
mkdir -p .agents/skills/paywall-design/references
mkdir -p .agents/skills/paywall-design/scripts
```

---

## 任务 8.2：编写 SKILL.md

### 完整内容

```markdown
---
name: paywall-design
description: 付费卡点设计。分析大纲找最优切割点，设计过渡章节奏。
---

# paywall-design（付费卡点设计）

> **用途**：分析大纲找到最优付费切割点，设计过渡章（免费末章+付费首章）。
> **前置条件**：大纲已完成（`settings/outline.yaml` 存在）、黄金三章已完成。
> **输出文件**：`settings/paywall_report.yaml`

---

## 核心原则

1. **爽点兑现**：卡点前必须有至少一次爽点（读者爽了才愿意花钱）
2. **致命悬念**：卡点处必须有一个让读者"不花钱就难受"的悬念
3. **不骗读者**：付费首章必须兑现承诺，不能卡点后立刻无聊
4. **数据验证**：有数据时用数据验证卡点选择

---

## Phase 定义

### Phase 1：分析大纲

**入口条件**：outline.yaml 和 chapters_index.yaml 存在
**目标**：理解故事结构，找到候选卡点

**步骤**：
1. 读取 `settings/outline.yaml` 获取故事结构
2. 读取 `settings/chapters_index.yaml` 获取章节列表
3. 读取 `settings/scout_report.yaml` 获取品类
4. 标记所有章节的"爽点"和"悬念"位置
5. 生成候选卡点列表

**出口条件**：候选卡点列表已生成
**加载 References**：`cut-point-method.md`

**候选卡点格式**：

```yaml
candidates:
  - chapter: 20
    type: 爽点兑现+悬念
    score: 85
    reason: "主角首次击败小反派（爽点），大反派手下出现（新悬念）"
  - chapter: 25
    type: 身份揭示
    score: 78
    reason: "主角隐藏身份即将曝光（悬念），但前面爽点不够"
```

---

### Phase 2：评估与选择卡点

**入口条件**：候选卡点列表存在
**目标**：选出最优卡点

**步骤**：
1. 读取 `references/paywall-psychology.md` 了解读者心理
2. 对每个候选卡点评分：
   - 前置爽点是否充分？（0-30 分）
   - 悬念强度如何？（0-30 分）
   - 读者情绪是否在高点？（0-20 分）
   - 付费后内容是否有吸引力？（0-20 分）
3. 展示评分结果，推荐最优卡点
4. 检查卡点前是否有"读者低谷"（主角正在受苦/无聊）→ 警告
5. 用户确认后记录 `paywall_chapter`

**出口条件**：`paywall_chapter` 已确定
**加载 References**：`paywall-psychology.md`

**评分标准**：

| 总分 | 结论 |
|------|------|
| ≥ 80 | 优秀卡点，可直接使用 |
| 60-79 | 可用，但建议优化 |
| < 60 | 不推荐，需要重新选择 |

---

### Phase 3：设计过渡章

**入口条件**：`paywall_chapter` 已确定
**目标**：设计免费末章和付费首章的节奏

**步骤**：
1. 读取 `references/transition-guide.md`
2. 设计免费末章（`paywall_chapter - 1` 或 `paywall_chapter`）：
   - 爽点兑现场景
   - 致命悬念抛出
   - 节奏设计
3. 设计付费首章（`paywall_chapter + 1`）：
   - 200 字内爽感反馈
   - 新弧线展开
   - 持续吸引力
4. 展示设计方案，用户确认

**出口条件**：过渡章设计方案已确认
**加载 References**：`transition-guide.md`

---

### Phase 4：平台适配

**入口条件**：过渡章设计已完成
**目标**：根据目标平台调整卡点

**步骤**：
1. 读取 `references/platform-paywall.md`
2. 根据目标平台调整：
   - 起点/番茄：按章节付费
   - 盐言/知乎：按篇/合集付费
   - 微信读书：全本付费
3. 如有多个平台，以主平台为准
4. 运行 `scripts/check-paywall.js` 验证卡点

**出口条件**：平台适配完成
**加载 References**：`platform-paywall.md`

---

### Phase 5：生成报告

**入口条件**：所有 Phase 完成
**目标**：生成 paywall_report.yaml

**步骤**：
1. 汇总所有分析结果
2. 写入 `settings/paywall_report.yaml`
3. 展示报告摘要
4. 清理 `_progress.md`

**出口条件**：paywall_report.yaml 已生成
**加载 References**：无

**报告格式**：

```yaml
paywall_report:
  paywall_chapter: 25
  platform: qidian
  score: 85
  reasoning: "第24章主角首次击败小反派（爽点兑现），第25章开头大反派登场（新悬念）"
  pre_paywall_hooks:
    - chapter: 20
      hook: "主角获得神秘传承"
    - chapter: 23
      hook: "对手身份暗示"
  free_last_chapter:
    chapter: 24
    design:
      - 爽点兑现：主角击败小反派
      - 致命悬念：大反派手下现身
    tension_curve: "上升→爆发→悬念"
  paid_first_chapter:
    chapter: 25
    design:
      - 200字内：大反派手下放狠话，主角冷静回应（爽感）
      - 中段：展开新弧线（大反派势力揭秘）
      - 结尾：新悬念（更大的挑战）
    tension_curve: "立刻拉升→持续→新悬念"
  warnings: []
```

---

## 质量门禁

- `check-paywall.js`：验证卡点前后章节是否满足条件
  - 卡点前是否有爽点？
  - 卡点处是否有悬念？
  - 付费首章开头是否有吸引力？

---

## 断点恢复

**状态文件**：`_progress.md`
**格式**：同其他 skill
**恢复逻辑**：跳到最后一个 `in_progress` 的 Phase

---

## 输出文件

- `settings/paywall_report.yaml`

---

## References 索引

| Phase | References | 用途 |
|-------|-----------|------|
| 1 | cut-point-method.md | 卡点选择方法论 |
| 2 | paywall-psychology.md | 读者付费心理 |
| 3 | transition-guide.md | 过渡章设计 |
| 4 | platform-paywall.md | 平台付费模式 |
| 5 | — | 生成报告 |

---

## 下一步

卡点设计完成后，可进入：
- `/daily-write`：开始写正文（写到卡点附近时特别关注过渡章节奏）
- `/data-diagnosis`：上架后用数据验证卡点选择
```

---

## 任务 8.3：编写 references/paywall-psychology.md

### 完整内容

```markdown
# 读者付费心理

> **用途**：Phase 2 评估卡点时理解读者心理。

---

## 核心心理模型

读者付费的本质是"为继续获得快感而付费"。不是为"已经获得的"付费，而是为"即将获得的"付费。

---

## 付费决策三要素

### 1. 沉没成本

读者已经读了 X 万字，投入了时间和情感。放弃意味着前面的投入"白费了"。

**利用方式**：
- 让读者与角色建立情感连接（前期功夫）
- 累积未解的悬念和伏笔
- 让读者关心角色的命运

**注意**：沉没成本只能"辅助"，不能"依赖"。如果内容无聊，读者宁可止损。

---

### 2. 即时满足预期

读者付费是因为"付费后马上能看到爽的内容"。

**利用方式**：
- 卡点前展示"爽的可能性"（但不完全兑现）
- 卡点处暗示"下一章更精彩"
- 付费首章立刻兑现一个爽点

**注意**：如果付费后内容拉胯，读者会觉得被骗，弃书+差评。

---

### 3. 损失厌恶

读者不付费就"错过了"精彩内容。损失带来的痛苦 > 获得带来的快乐。

**利用方式**：
- 卡点处抛出重大悬念（不花钱就不知道答案）
- 暗示下一章有"大场面"
- 让读者感受到"角色的命运悬于一线"

**注意**：威胁式卡点（故意虐主角逼读者花钱）会引发反感，要适度。

---

## 读者类型与付费倾向

| 类型 | 占比 | 付费倾向 | 卡点策略 |
|------|------|---------|---------|
| 冲动型 | 40% | 情绪到了就付 | 在高潮点卡 |
| 犹豫型 | 35% | 需要"推一把" | 悬念+爽点双保险 |
| 理性型 | 15% | 先看质量再决定 | 展示写作实力 |
| 白嫖型 | 10% | 不付费 | 不浪费时间 |

---

## 付费时机

### 最佳付费时机（读者情绪高点）

1. **爽点刚兑现**：读者正爽，意犹未尽
2. **悬念刚抛出**：读者想知道答案
3. **反转刚发生**：读者震惊，想看后续
4. **情感共鸣时**：读者被感动，愿意支持

### 最差付费时机（读者情绪低点）

1. **主角低谷期**：读者跟着郁闷，不想继续
2. **节奏拖沓时**：读者已经不耐烦
3. **过渡阶段**：读者觉得"等等再看也行"
4. **刚爽完的平静期**：读者已经满足

---

## 卡点前的情绪曲线

理想的卡点前情绪曲线：

```
情绪
  ↑
  │     ★爽点           ★卡点（情绪最高点）
  │    / \              / 
  │   /   \            /  ← 悬念拉起
  │  /     \    /\    /
  │ /       \  /  \  /
  │/         \/    \/
  └──────────────────────→ 章节
```

**关键**：
- 卡点前至少有一个爽点（让读者尝到甜头）
- 爽点后可以有小低谷（节奏调节）
- 卡点处情绪必须在上升（不是下降）

---

## 付费后的心理

读者付费后的心理变化：

1. **期待**："花钱了，一定要好看"
2. **审视**：付费首章会被更严格地审视
3. **验证**：如果首章好看 → 满足 → 继续付费
4. **失望**：如果首章无聊 → 被骗感 → 弃书/差评

**结论**：付费首章的质量比免费章节更重要。
```

---

## 任务 8.4：编写 references/cut-point-method.md

### 完整内容

```markdown
# 卡点选择方法论

> **用途**：Phase 1 分析大纲时选择候选卡点。

---

## 卡点选择的黄金公式

**最优卡点 = 爽点兑现 × 致命悬念**

两个要素缺一不可：
- 只有爽点没有悬念 → 读者爽完了，不急着看下一章
- 只有悬念没有爽点 → 读者还没尝到甜头，不愿意花钱

---

## 卡点候选位置分析

### 按故事结构

| 故事位置 | 适合卡点？ | 原因 |
|---------|-----------|------|
| 第一幕结束 | ⭐⭐⭐ | 第一个小高潮，读者已被吸引 |
| 第二幕前半 | ⭐⭐ | 有冲突但可能不够爽 |
| 第二幕后半 | ⭐⭐⭐⭐ | 冲突升级，悬念积累 |
| 第二幕高潮 | ⭐⭐⭐⭐⭐ | 最佳位置，情绪最高 |
| 第三幕开始 | ⭐⭐⭐ | 可用，但需要前面铺垫足够 |

### 按章节类型

| 章节类型 | 适合卡点？ | 条件 |
|---------|-----------|------|
| 打脸章 | ✅ | 打脸后立刻出新悬念 |
| 升级章 | ✅ | 升级后立刻展示新挑战 |
| 揭秘章 | ✅ | 揭秘后立刻出更大谜题 |
| 反转章 | ✅✅ | 最佳卡点类型 |
| 战斗章 | ✅ | 战斗结束/暂停时卡 |
| 感情章 | ⚠️ | 需要与主线冲突结合 |
| 日常章 | ❌ | 太平淡，不适合卡 |
| 过渡章 | ❌ | 没有高潮点 |

---

## 卡点评分模型

### 四个维度

| 维度 | 分值 | 评估标准 |
|------|------|---------|
| 前置爽点 | 0-30 | 卡点前 3-5 章的爽点数量和强度 |
| 悬念强度 | 0-30 | 卡点处悬念的大小和紧迫性 |
| 情绪位置 | 0-20 | 卡点处读者情绪在高点还是低点 |
| 后续吸引力 | 0-20 | 付费后内容的吸引力 |

### 评分细则

**前置爽点（0-30）**：

| 分数 | 标准 |
|------|------|
| 25-30 | 卡点前 3 章内有 2+ 个强爽点 |
| 15-24 | 卡点前 5 章内有 2+ 个爽点 |
| 5-14 | 卡点前有爽点但不够强 |
| 0-4 | 卡点前基本没有爽点 |

**悬念强度（0-30）**：

| 分数 | 标准 |
|------|------|
| 25-30 | 生死悬念/身份揭秘/重大反转 |
| 15-24 | 中等悬念（对手出现/新挑战） |
| 5-14 | 弱悬念（日常疑问） |
| 0-4 | 没有悬念 |

**情绪位置（0-20）**：

| 分数 | 标准 |
|------|------|
| 16-20 | 情绪在高点（刚爽完/刚反转） |
| 10-15 | 情绪在中上（平稳偏上） |
| 5-9 | 情绪在中下（低谷中） |
| 0-4 | 情绪在最低点（主角正在受苦） |

**后续吸引力（0-20）**：

| 分数 | 标准 |
|------|------|
| 16-20 | 付费后立刻有大场面/大反转 |
| 10-15 | 付费后有明确的新方向 |
| 5-9 | 付费后内容尚可 |
| 0-4 | 付费后没有明确吸引力 |

---

## 卡点警告

以下情况出现时，即使评分高也需要警告：

| 警告 | 原因 | 处理 |
|------|------|------|
| 主角正在低谷 | 读者跟着郁闷，付费意愿低 | 往前移 1-2 章到爽点处 |
| 连续 3 章无冲突 | 读者已经不耐烦 | 先加冲突再卡 |
| 悬念是"假的" | 卡点暗示的大场面不存在 | 修改大纲，让悬念兑现 |
| 卡点太早（前 10 章） | 读者还没建立信任 | 至少等黄金三章后 |
| 卡点太晚（后 1/3） | 可能已经流失大量读者 | 考虑提前 |

---

## 多卡点策略

如果故事较长（100 章以上），可以有多个卡点区域：

1. **主卡点**：最重要的付费分割线（通常在第 20-30 章）
2. **副卡点**：每个大弧线结束处
3. **微卡点**：每 5-10 章一个小钩子

本 skill 只设计主卡点。副卡点和微卡点在 `/design-chapters` 细纲阶段处理。
```

---

## 任务 8.5：编写 references/transition-guide.md

### 完整内容

```markdown
# 过渡章设计

> **用途**：Phase 3 设计免费末章和付费首章。
> **核心目标**：让读者"不花钱就难受"（免费末章）+ "花钱真值"（付费首章）。

---

## 免费末章设计

### 定位

免费末章 = 读者在付费前看到的最后一章。它的唯一使命：**让读者点开付费按钮**。

### 双保险结构

免费末章必须做到"爽点兑现 + 致命悬念"双保险：

| 要素 | 说明 | 权重 |
|------|------|------|
| 爽点兑现 | 读者在这里尝到甜头 | 50% |
| 致命悬念 | 读者必须知道后面怎样 | 50% |

只有爽点没有悬念 → 读者满足地离开（不付费）
只有悬念没有爽点 → 读者没有动力付费

### 节奏设计

```
开头：承接前章（快）
  ↓
前段：冲突升级（快）
  ↓
中段：爽点兑现（极快）← 全章最爽的地方
  ↓
后段：短暂缓冲（慢）← 让读者喘口气
  ↓
结尾：致命悬念（快）← 全章最后的钩子
```

### 爽点兑现设计

| 品类 | 推荐爽点类型 | 示例 |
|------|------------|------|
| 玄幻 | 打脸/升级/获宝 | 击败欺负自己的师兄 |
| 都市 | 身份揭示/逆袭/打脸 | 被嘲笑的人其实是总裁 |
| 系统 | 任务完成/奖励发放 | 完成高难任务，获得逆天奖励 |
| 言情 | 情感确认/甜蜜互动 | 两人关系突破 |
| 悬疑 | 线索揭秘/推理成功 | 破解关键线索 |

### 致命悬念设计

| 类型 | 说明 | 效果 |
|------|------|------|
| 生死悬念 | 角色面临生命危险 | 最强紧迫感 |
| 身份悬念 | 身份即将曝光/新身份出现 | 好奇心驱动 |
| 选择悬念 | 角色面临两难选择 | 代入感驱动 |
| 反转悬念 | 事情出现意想不到的变化 | 震惊驱动 |
| 预告悬念 | 暗示下一章有更大事件 | 期待驱动 |

**悬念强度排序**：生死 > 反转 > 身份 > 选择 > 预告

### 免费末章禁忌

1. ❌ 不要平淡收尾（"今天就这样吧"）
2. ❌ 不要过度虐主（读者跟着难受不想付钱）
3. ❌ 不要把悬念拖到下一章（必须在本章末尾）
4. ❌ 不要引入新角色（分散注意力）
5. ❌ 不要写太多日常（稀释紧张感）

---

## 付费首章设计

### 定位

付费首章 = 读者付费后看到的第一章。它的使命：**让读者觉得"钱花得值"**。

### 200 字法则

付费首章的**前 200 字**必须立刻给出爽感反馈。

| 时间段 | 任务 |
|--------|------|
| 前 200 字 | 立刻兑现爽感（回应免费末章的悬念） |
| 200-800 字 | 展开新弧线（给读者新的期待） |
| 800-结尾 | 持续吸引（保持节奏，不让读者后悔） |

### 为什么是 200 字？

- 读者付费后第一反应是"看看值不值"
- 前 200 字决定了读者的付费满意度
- 如果前 200 字无聊 → "被骗了" → 弃书 + 差评

### 爽感反馈设计

| 类型 | 说明 | 示例 |
|------|------|------|
| 回应悬念 | 免费末章的悬念立刻有回应 | 大反派现身 → 主角冷静应对 |
| 爽点延续 | 免费末章的爽点继续发酵 | 击败小反派 → 众人震惊 |
| 新信息冲击 | 立刻抛出重要信息 | 系统提示：隐藏任务触发 |
| 角色魅力 | 展示角色的魅力时刻 | 主角说出帅气的台词 |

### 新弧线展开

爽感反馈之后，必须立刻展开新弧线，让读者有继续读下去的理由：

| 新弧线类型 | 说明 | 示例 |
|-----------|------|------|
| 新对手 | 更强的敌人出现 | 小反派背后的势力 |
| 新目标 | 新的追求目标 | 更强的宝物/更高的境界 |
| 新危机 | 新的威胁出现 | 身份即将暴露 |
| 新篇章 | 进入新地图/新阶段 | 从外门进入内门 |

---

## 过渡章连贯性检查

| # | 检查项 | 标准 |
|---|--------|------|
| 1 | 免费末章有爽点？ | 至少有 1 个明确爽点 |
| 2 | 免费末章有悬念？ | 最后 300 字有致命悬念 |
| 3 | 付费首章 200 字内有反馈？ | 前 200 字回应了悬念 |
| 4 | 付费首章有新弧线？ | 800 字内展开了新方向 |
| 5 | 前后衔接自然？ | 读者不会觉得断裂 |
| 6 | 情绪曲线正确？ | 免费末章上升到顶，付费首章开头不坠崖 |
```

---

## 任务 8.6：编写 references/platform-paywall.md

### 完整内容

```markdown
# 平台付费模式

> **用途**：Phase 4 根据目标平台调整卡点设计。

---

## 平台分类

### 按章付费平台

| 平台 | 模式 | 特点 |
|------|------|------|
| 起点中文网 | VIP 章节按章付费 | 千字 5 分，读者习惯按章购买 |
| 番茄小说 | 免费+广告，付费跳过广告 | 读者对付费敏感度低 |
| 纵横中文网 | VIP 章节按章付费 | 类似起点 |
| 17K | VIP 章节按章付费 | 类似起点 |

**卡点策略**：
- 卡点可以精确到章节
- 前 30-50 章免费（建立读者基础）
- 卡点选在读者已经养成阅读习惯后
- 每章定价统一，不需要考虑"一章值不值"

### 按篇/合集付费平台

| 平台 | 模式 | 特点 |
|------|------|------|
| 盐言故事 | 按篇/合集付费 | 单篇 1-5 元，合集更优惠 |
| 知乎 | 盐选专栏 | 读者期望高质量 |
| 豆瓣阅读 | 按篇付费 | 读者偏文艺 |

**卡点策略**：
- 卡点是"试读结束"的位置
- 试读部分必须完整展示写作实力
- 卡点位置通常在全篇的 20-30% 处
- 试读结束处必须有极强悬念

### 全本付费平台

| 平台 | 模式 | 特点 |
|------|------|------|
| 微信读书 | 全本定价/会员免费 | 作者按阅读量分成 |
| kindle | 全本定价 | 需要完整书籍 |

**卡点策略**：
- 没有传统意义上的"卡点"
- 重点是"试读章节"的质量（前 3-5 章）
- 书籍简介和目录决定购买

---

## 平台特定规则

### 起点中文网

- VIP 起始章节：通常 25-40 章（编辑建议）
- 免费字数要求：≥ 8 万字
- 上架后每日更新：≥ 2 章（保持订阅）
- 卡点建议：第一个小高潮后，第二个弧线开始前

### 番茄小说

- 免费模式为主，广告收入
- 付费章节（如有）：通常在 30-50 章后
- 卡点建议：读者留存率最高的章节
- 重点关注：追读率数据

### 盐言故事

- 试读比例：约 20-30%
- 单篇字数：1-5 万字
- 卡点建议：全篇最关键的转折前
- 试读部分 = 完整的第一幕

---

## 平台选择建议

| 品类 | 推荐平台 | 原因 |
|------|---------|------|
| 玄幻/仙侠 | 起点/纵横 | 品类用户基数大 |
| 都市 | 起点/番茄 | 品类适配 |
| 短篇言情 | 盐言/知乎 | 品类用户集中 |
| 悬疑/推理 | 盐言/豆瓣 | 品类适配 |
| 系统文 | 番茄/起点 | 品类用户多 |

---

## 跨平台策略

如果同时发布多个平台：

1. 以主平台的卡点为准
2. 其他平台可以微调（如果平台规则不同）
3. 内容保持一致，只调整免费/付费的分割线

---

## 数据验证

上架后，用以下数据验证卡点选择：

| 指标 | 健康值 | 异常值 | 含义 |
|------|--------|--------|------|
| 付费转化率 | > 5% | < 2% | 卡点设计是否有效 |
| 首订率 | > 50% | < 30% | 付费首章是否留住人 |
| 追订率 | > 60% | < 40% | 后续章节质量是否稳定 |

异常时用 `/data-diagnosis` 进一步分析。
```

---

## 任务 8.7：编写 scripts/check-paywall.js

### 完整内容

```javascript
#!/usr/bin/env node
'use strict';

// check-paywall.js — 卡点验证脚本
// Usage: node check-paywall.js <paywall_report.yaml> <chapters_index.yaml>

const fs = require('fs');
const path = require('path');

const USAGE = `Usage: node check-paywall.js [--json] <paywall_report.yaml> <chapters_index.yaml>

验证付费卡点设计是否合理：
  - 卡点前是否有爽点章节
  - 卡点处是否有悬念章节
  - 付费首章是否有设计方案
  - 卡点位置是否在合理范围

退出码：
  0 = 验证通过
  1 = 有警告或错误
  2 = 参数错误`;

const options = { json: false, files: [] };

for (let i = 2; i < process.argv.length; i += 1) {
  const arg = process.argv[i];
  if (arg === '--json') {
    options.json = true;
  } else if (arg === '-h' || arg === '--help') {
    process.stdout.write(`${USAGE}\n`);
    process.exit(0);
  } else if (arg.startsWith('-')) {
    die(`Unknown option: ${arg}`);
  } else {
    options.files.push(arg);
  }
}

if (options.files.length < 2) {
  die('Need paywall_report.yaml and chapters_index.yaml');
}

function die(message) {
  console.error(message);
  console.error(USAGE.trimEnd());
  process.exit(2);
}

function loadYaml(filePath) {
  const resolved = path.resolve(filePath);
  let content;
  try {
    content = fs.readFileSync(resolved, 'utf8');
  } catch (err) {
    die(`Cannot read ${filePath}: ${err.message}`);
  }
  // 简易 YAML 解析：只处理简单的 key: value 结构
  const result = {};
  const lines = content.split(/\r?\n/);
  let currentKey = null;
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const match = /^(\w[\w_]*):\s*(.*)$/.exec(trimmed);
    if (match) {
      const key = match[1];
      const value = match[2].replace(/^["']|["']$/g, '').trim();
      result[key] = value || {};
      currentKey = key;
    }
  }
  return result;
}

const report = loadYaml(options.files[0]);
const chaptersIndex = loadYaml(options.files[1]);

const findings = [];

// 提取卡点章节号
const paywallChapter = parseInt(report.paywall_chapter, 10);
if (isNaN(paywallChapter) || paywallChapter < 1) {
  findings.push({
    severity: 'blocking',
    type: 'missing-paywall-chapter',
    message: 'paywall_report.yaml 中缺少 paywall_chapter 字段',
  });
}

// 检查卡点位置范围
if (!isNaN(paywallChapter)) {
  if (paywallChapter < 5) {
    findings.push({
      severity: 'warning',
      type: 'too-early',
      message: `卡点在第 ${paywallChapter} 章，可能太早（< 5 章），读者还没建立信任`,
    });
  }

  if (paywallChapter > 60) {
    findings.push({
      severity: 'warning',
      type: 'too-late',
      message: `卡点在第 ${paywallChapter} 章，可能太晚（> 60 章），读者可能已经流失`,
    });
  }
}

// 检查是否有 reasoning
if (!report.reasoning || report.reasoning === '') {
  findings.push({
    severity: 'warning',
    type: 'missing-reasoning',
    message: '缺少卡点选择理由（reasoning 字段为空）',
  });
}

// 检查是否有过渡章设计
const hasFreeDesign = report.free_last_chapter && report.free_last_chapter !== '';
const hasPaidDesign = report.paid_first_chapter && report.paid_first_chapter !== '';

if (!hasFreeDesign) {
  findings.push({
    severity: 'warning',
    type: 'missing-free-design',
    message: '缺少免费末章设计方案（free_last_chapter 字段为空）',
  });
}

if (!hasPaidDesign) {
  findings.push({
    severity: 'warning',
    type: 'missing-paid-design',
    message: '缺少付费首章设计方案（paid_first_chapter 字段为空）',
  });
}

// 检查评分
const score = parseInt(report.score, 10);
if (isNaN(score)) {
  findings.push({
    severity: 'warning',
    type: 'missing-score',
    message: '缺少卡点评分（score 字段为空）',
  });
} else if (score < 60) {
  findings.push({
    severity: 'warning',
    type: 'low-score',
    message: `卡点评分 ${score} < 60，建议重新选择卡点位置`,
  });
}

// 输出结果
if (options.json) {
  process.stdout.write(`${JSON.stringify({ findings }, null, 2)}\n`);
} else {
  if (findings.length === 0) {
    console.log('✓ 卡点验证通过');
  } else {
    for (const f of findings) {
      const icon = f.severity === 'blocking' ? '✗' : '⚠';
      console.log(`${icon} [${f.severity}] ${f.type}: ${f.message}`);
    }
  }
}

const hasBlocking = findings.some((f) => f.severity === 'blocking');
if (hasBlocking) process.exit(1);
if (findings.length > 0) process.exit(1);
process.exit(0);
```

---

## 执行顺序

1. 创建目录结构
2. 编写 SKILL.md
3. 编写 paywall-psychology.md
4. 编写 cut-point-method.md
5. 编写 transition-guide.md
6. 编写 platform-paywall.md
7. 编写 check-paywall.js
8. 验证脚本可运行
9. Commit
