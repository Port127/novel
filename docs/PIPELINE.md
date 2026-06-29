# Novel V2 Pipeline 流程

> Pipeline 是 Skills 的执行流程，确保创作按正确顺序进行。
> 所有创作 skill 采用 V4 自包含结构：Phase 化流程 + references/ + scripts/。

---

## Pipeline 阶段

| 阶段 | 名称 | Skills | 输出 | 完善度阈值 |
|------|------|--------|------|-----------|
| 0 | 选题侦察 | scout-topic | `settings/scout_report.yaml` | - |
| 1 | 世界观设定 | worldbuilding + nm | `settings/worldbuilding.yaml` | 80% |
| 2 | 人设设计 | design-character | `settings/characters.yaml` | 70% |
| 3 | 大纲设计 | design-outline | `settings/outline.yaml` + `settings/arcs.yaml` + `settings/pacing.yaml` | 85% |
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

**目标**：选择品类，分析市场，配置品类感知参数。

**Skills 组合**：
1. `/scout-topic` — 6 Phase 流程（品类定位→平台分析→选题决策→标签策略→品类感知配置→报告定稿）
2. `/nm` — 检索同类题材素材参考（可选）

**输出**：
- `settings/scout_report.yaml` — 品类、目标读者、标签组合、`required_elements`

**关键产出**：`required_elements` 字段声明了这本小说需要什么元素（力量体系/时代背景/角色类型/开篇钩子/结构类型），后续所有 skill 的质量门禁据此动态检查。

---

### 阶段 1：世界观设定

**目标**：建立小说世界的基础设定。

**前置依赖**：品类已选择（阶段 0）

**Skills 组合**：
1. `/nm` — 检索同类题材素材参考（可选）
2. `/worldbuilding` — 5 Phase 流程（品类适配→力量体系→社会结构→基础规则→落盘验证）

**输出**：
- `settings/worldbuilding.yaml` — 世界观设定（力量体系、社会结构、背景知识等）

**质量门禁**：
- `check-completeness.js` — 检查 `required_elements.worldbuilding.required` 中的元素是否完整

---

### 阶段 2：人设设计

**目标**：设计主角、反派、配角，含爽感维度评估。

**前置依赖**：品类已选择（阶段 0）

**Skills 组合**：
1. `/nm` — 检索同类人物塑造参考（可选）
2. `/design-character` — 5 Phase 流程（品类适配→主角设计→反派设计→配角与关系网络→爽感评估与落盘）

**输出**：
- `settings/characters.yaml` — 人物设定（主角、反派、配角、关系网络）

**质量门禁**：
- `check-characters.js` — 品类感知检查：必需角色类型齐全、主角/反派有 psychology + arc

**爽感三维评估**：
- 打脸指数（face-slap index）≥ 6/10
- CP感（chemistry）≥ 6/10
- 反派恶心度（disgust level）≥ 6/10

---

### 阶段 3：大纲设计

**目标**：规划全书结构，含节奏分析。

**前置依赖**：世界观 ≥ 80%

**Skills 组合**：
1. `/nm` — 检索同类大纲结构参考（可选）
2. `/design-outline` — 5 Phase 流程（品类适配→骨架搭建→序列细化→节拍填充→落盘验证）

**输出**：
- `settings/outline.yaml` — 主大纲
- `settings/arcs.yaml` — 叙事弧线
- `settings/pacing.yaml` — 节奏曲线

**质量门禁**：
- `check-outline.js` — 结构完整性（幕数/前提/伏笔闭合）
- `check-pacing.js` — 节奏健康度（连续慢章/高潮间距/黄金三章）

---

### 阶段 4：细纲设计

**目标**：按大纲拆分章节，每章生成节拍表。

**前置依赖**：大纲完善度 ≥ 85%

**Skills 组合**：
1. `/design-chapters` — 5 Phase 流程（大纲解析→章节拆分→章节摘要→张力曲线→落盘验证）

**输出**：
- `settings/chapters_index.yaml` — 章节索引（每章含摘要、节拍、张力值）

**质量门禁**：
- `check-chapters.js` — 节拍数 3-15、字数 2000-5000、密度连续性

---

### 阶段 5：黄金三章锻造

**目标**：按品类模板，逐段生成前三章，验证结构。

**前置依赖**：品类+人设+细纲已完成

**Skills 组合**：
1. `/golden-chapters` — 6 Phase 流程（品类适配→第一章→第二章→第三章→去AI味→定稿）

**输出**：
- `content/chapter_001.md`
- `content/chapter_002.md`
- `content/chapter_003.md`

**质量门禁**：
- `check-golden-structure.js` — 按 `opening_hook.type` 检查品类开篇钩子
- `check-ai-patterns.js` — AI 味检测，blocking 项归零
- `check-degeneration.js` — 退化检测，blocking 项归零

---

### 阶段 6：付费卡点设计

**目标**：分析大纲，找到最优付费切割点。

**前置依赖**：大纲+黄金三章已完成

**Skills 组合**：
1. `/paywall-design` — 5 Phase 流程（大纲分析→切点决策→过渡设计→平台适配→落盘验证）

**输出**：
- `paywall_report.yaml` — 卡点位置、理由、过渡章设计

**质量门禁**：
- `check-paywall.js` — 切点章张力 > 均值

---

### 阶段 7：日更写作

**目标**：根据章节摘要生成正文，通过质量门禁。

**前置依赖**：目标章节完善度 = 100%

**Skills 组合**：
1. `/daily-write` — 6 Phase 流程（选题确认→上下文加载→写作执行→确定性检查→LLM评估→定稿）

**输出**：
- `content/chapter_XXX.md`

**质量门禁**（双层）：
- **JS 脚本**（确定性）：`check-ai-patterns.js` + `check-degeneration.js` + `normalize-punctuation.js`
- **LLM 评估**（语义）：反AI五层评分 ≥ 60、钩子评分 ≥ 60

**断点恢复**：`_progress.md` 记录当前章节和 Phase，崩溃后自动续跑

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
阶段0：选题侦察（品类选择 + required_elements 配置）
    ↓
阶段1：世界观设定
    ↓ check-completeness.js 验证
阶段2：人设设计（含三维爽感评估）
    ↓ check-characters.js 验证
阶段3：大纲设计（含节奏分析）
    ↓ check-outline.js + check-pacing.js 验证
阶段4：细纲设计（章节拆分）
    ↓ check-chapters.js 验证
阶段5：黄金三章锻造
    ↓ check-golden-structure.js + check-ai-patterns.js 验证
阶段6：付费卡点设计
    ↓ check-paywall.js 验证
阶段7：日更写作（JS脚本 + LLM 评估双层门禁）
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
- 每个 skill 自包含，39 个 references + 14 个 JS 脚本
- 大纲采用 幕→序列→节拍 三层嵌套结构
- 章节索引含节拍表 + 张力曲线

**分批写作**：
- 阶段4可分批规划（如先规划前100章）
- 阶段7按顺序写作（从第1章开始），支持断点恢复

---

## 商业化支持

Novel V2 内置网文商业化流程：

| 功能 | 说明 |
|------|------|
| 黄金三章 | 前3章决定生死，按品类模板严格验证结构 |
| 付费卡点 | 分析大纲找最优切割点，设计过渡章节奏 |
| 质量门禁 | JS 脚本确定性检查 + LLM 语义评估 |
| 爽感评估 | 打脸指数/CP感/反派恶心度（三维 ≥ 6/10） |
| 品类感知 | 根据 required_elements 动态调整质量检查 |
