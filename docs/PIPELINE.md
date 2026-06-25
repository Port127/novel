# Novel V2 Pipeline 流程

> Pipeline 是 Skills 的执行流程，确保创作按正确顺序进行。

---

## Pipeline 阶段

| 阶段 | 名称 | Skills | 输出 | 完善度阈值 |
|------|------|--------|------|-----------|
| 1 | 世界观设定 | nm + Agent 交互 | worldbuilding/ 目录 | 80% |
| 2 | 人物设定 | generate-character | characters/ 目录 | 70% |
| 3 | 大纲设定 | generate-outline | outline/ 目录 | 85% |
| 4 | 章节规划 | generate-chapter | chapters/ 目录 | 100%（每章）|
| 5 | 正文写作 | write-chapter | content/chapters/ | - |

---

## Pipeline 入口

**推荐使用 `/create-novel`**，它会：
1. 检查当前项目状态
2. 判断处于哪个阶段
3. 引导用户完成当前阶段
4. 自动进入下一阶段

---

## 各阶段详情

### 阶段 1：世界观设定

**目标**：建立小说世界的基础设定。

**Skills 组合**：
1. `/nm` — 检索同类题材素材参考
2. Agent 交互讨论 — 确认力量体系、势力、地点
3. 直接生成 — 写入 worldbuilding/ 目录各文件

**输出**：
- `worldbuilding/power_system.yaml` — 力量体系
- `worldbuilding/factions/faction_*.yaml` — 势力档案（≥3个）
- `worldbuilding/locations/location_*.yaml` — 地点档案（≥1个）
- `worldbuilding/lore/*.yaml` — 背景知识（可选）

**完善度检查**：
```bash
novel generate (内建检查) {project_id} worldbuilding --modules
```

**阈值**：
- power_system: 100%（name + levels + rules 必填）
- factions: 80%（至少3个势力，每个有完整档案）
- locations: 100%（至少1个地点）

---

### 阶段 2：人物设定

**目标**：建立小说的核心角色。

**前置依赖**：世界观完善度 ≥ 80%

**Skills 组合**：
1. `/nm` — 检索同类人物塑造参考
2. `/generate-character` — 交互生成人物档案
3. Agent 直接生成 — 写入 characters/ 目录各文件

**输出**：
- `characters/protagonist/protagonist.yaml` — 主角档案
- `characters/antagonist/antagonist_*.yaml` — 反派档案（≥1个）
- `characters/supporting/supporting_*.yaml` — 配角档案（≥3个）
- `characters/relationships.yaml` — 关系网络

**完善度检查**：
```bash
novel generate (内建检查) {project_id} characters --modules
```

**阈值**：
- protagonist: 100%（traits + psychology + arc 必填）
- antagonist: 80%（至少1个反派，每个有完整档案）
- supporting: 70%（至少3个配角）

---

### 阶段 3：大纲设定

**目标**：规划全书结构（800章）。

**前置依赖**：世界观 ≥ 80%，人物 ≥ 70%

**Skills 组合**：
1. `/nm` — 检索同类大纲结构参考
2. `/generate-outline` — 交互生成大纲
3. Agent 直接生成 — 写入 outline/ 目录各文件

**输出**：
- `outline/premise.yaml` — 核心设定
- `outline/acts/act_*.yaml` — 各幕结构（≥3幕）
- `outline/hooks.yaml` — 伏笔-回收（可选）
- `outline/pacing.yaml` — 节奏曲线（可选）

**完善度检查**：
```bash
novel generate (内建检查) {project_id} outline --modules
```

**阈值**：
- premise: 100%（premise_statement ≥ 50字）
- acts: 85%（至少3幕，每幕 ≥ 2序列，每序列 ≥ 5节拍）

---

### 阶段 4：章节规划

**目标**：将大纲转化为章节摘要。

**前置依赖**：大纲完善度 ≥ 85%

**Skills 组合**：
1. `/generate-chapter` — 从大纲转化章节摘要
2. Agent 直接生成 — 写入 chapters/ 目录各文件

**输出**：
- `chapters/_index.yaml` — 章节索引
- `chapters/chapter_*.yaml` — 各章档案（每章）

**完善度检查**：
```bash
novel generate (内建检查) {project_id} chapters --target {章节号}
```

**阈值**：
- 目标章节: 100%（summary + characters_appear + tension_level 必填）

---

### 阶段 5：正文写作

**目标**：根据章节摘要生成正文（4000字/章）。

**前置依赖**：目标章节完善度 = 100%

**Skills 组合**：
1. `/write-chapter` — 确认摘要 → 生成正文 → 续写/改写
2. Agent 直接生成 — 写入 content/chapters/ 目录

**输出**：
- `content/chapters/chapter_*.md` — 章节正文

**字数要求**：
- draft: ≥ 2000字
- written: ≥ 4000字
- revised: ≥ 4000字（已润色）

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
项目创建（project.py create）
    ↓
阶段1：世界观设定
    ↓ 完善度 ≥ 80%
阶段2：人物设定
    ↓ 完善度 ≥ 70%
阶段3：大纲设定
    ↓ 完善度 ≥ 85%
阶段4：章节规划
    ↓ 目标章节完善度 = 100%
阶段5：正文写作
    ↓
完成：导出作品
```

---

## 跳阶段处理

**禁止跳阶段**：
- 未完成阶段1 → 不能执行阶段2
- 未完成阶段2 → 不能执行阶段3
- ...

**跳阶段尝试时**：
- `/create-novel` 会阻止并提示缺失前置
- `/generate-*` Skills 会检查前置完善度

**示例**：
```
用户尝试：/generate-outline

检查结果：
  阶段1（世界观）完善度 20% ❌
  阶段2（人物）完善度 0% ❌

阻止：请先完成阶段1和阶段2
引导：是否开始世界观设定？
```

---

## 规模支持

**目标规模**：800章 × 4000字 = 320万字

**模块化设计**：
- 每个势力/人物/地点独立文件
- 每幕独立文件（含序列+节拍）
- 每章独立档案

**分批写作**：
- 阶段4可分批规划（如先规划前100章）
- 阶段5按顺序写作（从第1章开始）