# Novel V2 Pipeline 流程

> Pipeline 是 Skills 的执行流程，确保创作按正确顺序进行。

---

## Pipeline 阶段

| 阶段 | 名称 | Skills | 输出 | 完善度阈值 |
|------|------|--------|------|-----------|
| 0 | 选题侦察 | scout-topic | `settings/scout_report.yaml` | - |
| 1 | 世界观设定 | worldbuilding + nm | `settings/worldbuilding.yaml` | 80% |
| 2 | 人设设计 | design-character | `settings/characters.yaml` | 70% |
| 3 | 大纲设计 | design-outline | `settings/outline.yaml` + `settings/arcs.yaml` | 85% |
| 4 | 细纲设计 | design-chapters | `settings/chapters_index.yaml` | 100%（每章）|
| 5 | 黄金三章 | golden-chapters | `content/chapter_001-003.md` | - |
| 6 | 付费卡点 | paywall-design | `paywall_report.yaml` | - |
| 7 | 日更写作 | daily-write | `content/chapter_*.md` | - |
| 8 | 导出 | export-novel | TXT/MD/EPUB | - |

---

## Pipeline 入口

**推荐使用完整创作流程**，它会：
1. 从选题开始，逐步引导
2. 检查当前项目状态
3. 判断处于哪个阶段
4. 引导用户完成当前阶段
5. 自动进入下一阶段

---

## 各阶段详情

### 阶段 0：选题侦察

**目标**：选择品类，分析市场。

**Skills 组合**：
1. `/scout-topic` — 品类选择 + 选题分析
2. `/nm` — 检索同类题材素材参考

**输出**：
- `settings/scout_report.yaml` — 品类、目标读者、标签组合

---

### 阶段 1：世界观设定

**目标**：建立小说世界的基础设定。

**Skills 组合**：
1. `/nm` — 检索同类题材素材参考
2. `/worldbuilding` — 交互式设计世界观
3. Agent 直接生成 — 写入 worldbuilding.yaml

**输出**：
- `settings/worldbuilding.yaml` — 世界观设定（力量体系、社会结构、背景知识等）

**完善度检查**：
```bash
novel generate (内建检查) {project_id} worldbuilding --modules
```

**阈值**：
- power_system: 100%（name + levels + rules 必填）
- factions: 80%（至少3个势力，每个有完整档案）
- locations: 100%（至少1个地点）

---

### 阶段 2：人设设计

**目标**：设计主角、反派、配角，含爽感维度评估。

**前置依赖**：品类已选择（阶段 0）

**Skills 组合**：
1. `/nm` — 检索同类人物塑造参考
2. `/design-character` — 交互式人设设计 + 爽感评估
3. Agent 直接生成 — 写入 characters.yaml

**输出**：
- `settings/characters.yaml` — 人物设定（主角、反派、配角、关系网络）

**完善度检查**：
```bash
# 通过 Skill 检查爽感维度
/design-character
```

**阈值**：
- protagonist: 100%（打脸指数/CP感 ≥ 7）
- antagonist: 80%（反派恶心度 ≥ 7）
- supporting: 70%（至少3个配角）

---

### 阶段 3：大纲设计

**目标**：规划全书结构，含节奏分析。

**前置依赖**：世界观 ≥ 80%，人物 ≥ 70%

**Skills 组合**：
1. `/nm` — 检索同类大纲结构参考
2. `/design-outline` — 交互式大纲设计 + 节奏分析
3. Agent 直接生成 — 写入 outline/ 目录各文件

**输出**：
- `outline/premise.yaml` — 核心设定
- `outline/acts/act_*.yaml` — 各幕结构（≥3幕）
- `outline/hooks.yaml` — 伏笔-回收（可选）
- `outline/pacing.yaml` — 节奏曲线（可选）

**完善度检查**：
```bash
# 通过 Skill 检查节奏
/design-outline
```

**阈值**：
- premise: 100%（premise_statement ≥ 50字）
- acts: 85%（至少3幕，节奏曲线合理）
- pacing: 无连续3章以上慢节奏

---

### 阶段 4：细纲设计

**目标**：按大纲拆分章节，每章生成节拍表。

**前置依赖**：大纲完善度 ≥ 85%

**Skills 组合**：
1. `/design-chapters` — 章节拆分 + 节拍表生成
2. Agent 直接生成 — 写入 chapters/ 目录各文件

**输出**：
- `chapters/_index.yaml` — 章节索引
- `chapters/chapter_*.yaml` — 各章档案（每章）

**完善度检查**：
```bash
# 通过 Skill 检查章节结构
/design-chapters
```

**阈值**：
- 目标章节: 100%（summary + tension + beats 必填）
- 节拍数量: 3-15 个/章
- 目标字数: 2000-5000 字/章

---

### 阶段 5：黄金三章锻造

**目标**：按品类模板，逐段生成前三章，验证结构。

**前置依赖**：品类+人设+细纲已完成

**Skills 组合**：
1. `/golden-chapters` — 逐章生成 + 结构验证
2. Agent 直接生成 — 写入 content/chapter_001-003.md

**输出**：
- `content/chapter_001.md`
- `content/chapter_002.md`
- `content/chapter_003.md`
- `golden_chapters_report.yaml`

**验证清单**：
- 首冲突 ≤ 300 字？
- 人设建立？
- 金手指亮相？
- 第一个小高潮？

---

### 阶段 6：付费卡点设计

**目标**：分析大纲，找到最优付费切割点。

**前置依赖**：大纲+黄金三章已完成

**Skills 组合**：
1. `/paywall-design` — 卡点分析 + 过渡章设计
2. Agent 直接生成 — 写入 paywall_report.yaml

**输出**：
- `paywall_report.yaml` — 卡点位置、理由、过渡章设计

---

### 阶段 7：日更写作

**目标**：根据章节摘要生成正文，通过质量门禁。

**前置依赖**：目标章节完善度 = 100%

**Skills 组合**：
1. `/daily-write` — 确认摘要 → 生成正文 → 质量门禁
2. Agent 直接生成 — 写入 content/chapter_*.md

**质量门禁**：
- 事实核查（角色/时间/地点一致性）
- 去AI味（五层检测，≥ 60 分）
- 钩子审查（悬念强度/冲突密度，≥ 60 分）

**字数要求**：
- draft: ≥ 2000字
- written: ≥ 3000字
- revised: ≥ 3000字（已润色）

---

## Pipeline 状态追踪

项目 `project.yaml` 中包含 `pipeline_status` 字段：

```yaml
pipeline_status:
  current_stage: 2                # 当前阶段
  completed_stages: [1]           # 已完成阶段
  blocked_stages: []              # 阻塞阶段（前置依赖不满足）
```

---

## 流程图

```
阶段0：选题侦察（品类选择）
    ↓
阶段1：世界观设定
    ↓ 完善度 ≥ 80%
阶段2：人设设计（含爽感评估）
    ↓ 完善度 ≥ 70%
阶段3：大纲设计（含节奏分析）
    ↓ 完善度 ≥ 85%
阶段4：细纲设计（章节拆分）
    ↓ 目标章节完善度 = 100%
阶段5：黄金三章锻造
    ↓
阶段6：付费卡点设计
    ↓
阶段7：日更写作（质量门禁）
    ↓
阶段8：导出作品
```

---

## 跳阶段处理

**禁止跳阶段**：
- 未完成阶段1 → 不能执行阶段2
- 未完成阶段2 → 不能执行阶段3
- ...

**跳阶段尝试时**：
- Skills 会检查前置完善度
- 未达标会阻止并提示缺失前置

**示例**：
```
用户尝试：/design-outline

检查结果：
  阶段0（品类）未设置 ❌
  阶段1（世界观）完善度 20% ❌
  阶段2（人设）完善度 0% ❌

阻止：请先完成品类选择和世界观设定
引导：是否开始选题侦察？
```

---

## 规模支持

**目标规模**：支持 100-1000 章长篇连载

**模块化设计**：
- 每个势力/人物/地点独立文件
- 每幕独立文件（含序列+节拍）
- 每章独立档案

**分批写作**：
- 阶段4可分批规划（如先规划前100章）
- 阶段7按顺序写作（从第1章开始）

---

## 商业化支持

Novel V2 内置网文商业化流程：

| 功能 | 说明 |
|------|------|
| 黄金三章 | 前3章决定生死，按品类模板严格验证结构 |
| 付费卡点 | 分析大纲找最优切割点，设计过渡章节奏 |
| 质量门禁 | 事实核查 + 去AI味 + 钩子审查 |
| 爽感评估 | 打脸指数/CP感/反派恶心度 |