# Commercial Copilot SKILL 体系实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 删除 7 个旧 SKILL，新建 10 个商业化 SKILL，每个专注一个创作阶段，可独立调用。

**Architecture:** 每个 SKILL 是一个 Markdown 指令文件，指导 Claude Code 如何引导用户完成特定创作任务。底层通过 Python Skill 引擎（`src/novel/core/skills/`）提供能力支撑。

**Tech Stack:** Markdown SKILL.md files, Python 3.12, pydantic v2

**Spec:** `docs/superpowers/specs/2026-06-25-skill-system-redesign.md`

---

## 阶段划分

| 阶段 | 任务 | 内容 |
|------|------|------|
| Phase 1 | 清理 + 核心创作线 | 删除旧 SKILL，创建 `/scout-topic` `/design-character` `/golden-chapters` `/daily-write` |
| Phase 2 | 架构与数据 | 创建 `/design-outline` `/design-chapters` `/paywall-design` `/data-diagnosis` |
| Phase 3 | 管理工具 | 创建 `/stock-check` `/worldbuilding` |

---

## Phase 1: 清理 + 核心创作线

### Task 1: 删除 7 个旧 SKILL 目录

**Files:**
- Delete: `.claude/skills/create-novel/`
- Delete: `.claude/skills/generate-character/`
- Delete: `.claude/skills/generate-outline/`
- Delete: `.claude/skills/generate-chapter/`
- Delete: `.claude/skills/write-chapter/`
- Delete: `.claude/skills/revise-setting/`
- Delete: `.claude/skills/show-project/`

- [ ] **Step 1: 删除旧 SKILL 目录**

```bash
cd /Users/kiki/Documents/Project/my-github/novel/novel
rm -rf .claude/skills/create-novel
rm -rf .claude/skills/generate-character
rm -rf .claude/skills/generate-outline
rm -rf .claude/skills/generate-chapter
rm -rf .claude/skills/write-chapter
rm -rf .claude/skills/revise-setting
rm -rf .claude/skills/show-project
```

- [ ] **Step 2: 验证删除**

```bash
ls .claude/skills/
```

Expected: 只剩 commit-msg、code-review-change、export-novel、feature-planning、nm、refactor-planning

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "refactor(skills): 删除 7 个旧版 SKILL

删除以下 SKILL（无商业化能力）：
- create-novel（无品类概念）
- generate-character（无爽感维度）
- generate-outline（无节奏检测）
- generate-chapter（无微节拍）
- write-chapter（无质量门禁）
- revise-setting（旧架构产物）
- show-project（无存稿管理）"
```

---

### Task 2: 创建 `/scout-topic` — 选题侦察兵

**Files:**
- Create: `.claude/skills/scout-topic/SKILL.md`

- [ ] **Step 1: 创建 SKILL.md**

```markdown
# .claude/skills/scout-topic/SKILL.md
---
name: scout-topic
description: 品类选择 + 选题分析。开新书或找题材时使用。
---

# 选题侦察兵

帮用户选择品类、分析市场、推荐标签组合。

---

## 工作流程

### 1. 确认项目

运行 `novel list` 查看项目列表。如果是新书，先创建项目：

```bash
novel new "书名" --genre 品类 --author 作者名
```

### 2. 选择品类

询问用户目标品类：

| 品类 | 特点 | 套路模板 |
|------|------|---------|
| 玄幻 | 升级打怪、宗门斗争 | 废柴流、退婚流、拍卖会 |
| 都市 | 打脸装逼、商战 | 退婚流、隐藏身份 |
| 系统文 | 任务奖励、数值碾压 | 系统激活、任务流 |
| 其他 | 用户自定义 | - |

**确认品类后**，调用品类路由：
```python
from novel.core.genre.profile import GenreRouter
router = GenreRouter()
router.set_genre("genre/<品类>")
```

### 3. 选题分析

与用户讨论：
- 目标平台（番茄/起点/其他）
- 目标读者群体
- 近期热门题材（可结合 `/nm` 检索）

输出选题报告：

```yaml
# settings/scout_report.yaml
genre: genre/xuanhuan
platform: 番茄小说
target_audience: 男频18-35
tag_combinations:
  - tags: [废柴流, 系统, 升级]
    competition_level: 0.6
    potential_score: 0.8
    window: "3-6个月"
recommended_tags: [废柴流, 系统, 升级]
reasoning: "低竞争高潜力，适合切入"
```

### 4. 展示与确认

展示选题报告，询问是否调整标签组合。确认后写入 `settings/scout_report.yaml`。

---

## 输出文件

- `settings/scout_report.yaml`

## 参考

- 品类画像配置：`src/novel/core/genre/profile.py`
- 选题引擎：`src/novel/core/skills/scout_topic.py`
```

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/scout-topic/SKILL.md
git commit -m "feat(skills): 添加 /scout-topic SKILL

- 品类选择（玄幻/都市/系统文/其他）
- 选题分析（竞争度/潜力/窗口期）
- 调用 GenreRouter + ScoutTopicSkill 引擎"
```

---

### Task 3: 创建 `/design-character` — 人设设计

**Files:**
- Create: `.claude/skills/design-character/SKILL.md`

> 借鉴旧 `generate-character` 的分层询问模式，增加爽感维度评估。

- [ ] **Step 1: 创建 SKILL.md**

```markdown
# .claude/skills/design-character/SKILL.md
---
name: design-character
description: 人设设计。设计主角、反派、配角，含爽感维度评估。
---

# 人设设计

交互式设计小说人物，含爽感维度（打脸指数、CP感、反派恶心度）。

---

## 前置依赖

- 品类已选择（`settings/scout_report.yaml` 存在）
- 大纲或细纲已有初步方向

如未完成，提示用户先使用 `/scout-topic`。

---

## 工作流程

### 1. 确认项目

运行 `novel list`，选择项目。

### 2. 检查品类

读取 `settings/scout_report.yaml`，确认品类已设置。

如未设置，提示先使用 `/scout-topic`。

### 3. 分层询问（借鉴旧 generate-character 模式）

**主角**：
- 基本信息（名字、年龄、身份）
- 性格特点
- 起点状态 → 终点状态（人物弧线）
- 金手指设计（系统/传承/血脉等）

**反派**：
- 基本信息
- 动机（为什么与主角对立）
- 恶心度设计（越恶心，打脸越爽）

**配角**：
- 名字、角色类型、一句话描述
- 与主角关系

### 4. 爽感评估

基于用户确认的内容，调用引擎评估：

```python
from novel.core.skills.design_character import DesignCharacterSkill
skill = DesignCharacterSkill()
design = await skill.design_character(
    name="主角名",
    genre_id="genre/xuanhuan",  # 从 scout_report.yaml 读取
    background="主角背景",
    personality="性格特点",
    golden_finger="金手指描述",
    villain_name="反派名",
    villain_background="反派背景",
)
```

输出评估结果：

| 维度 | 评分 | 说明 |
|------|------|------|
| 打脸指数 | 9/10 | 废柴开局+隐藏身份，适合扮猪吃虎 |
| CP感 | 7/10 | 腹黑性格有嗑点 |
| 反派恶心度 | 8/10 | 多次羞辱主角，打脸爽感强 |

如评分偏低，给出调整建议。

### 5. 生成人物文件

Agent 直接生成 `settings/characters/` 目录各文件：

- `protagonist/protagonist.yaml`（主角）
- `antagonist/antagonist_*.yaml`（反派）
- `supporting/supporting_*.yaml`（配角）
- `relationships.yaml`（关系网络）

### 6. 展示与调整

展示人物列表、爽感评估、关系网络。询问是否调整。

---

## 输出文件

- `settings/characters/protagonist/protagonist.yaml`
- `settings/characters/antagonist/antagonist_*.yaml`
- `settings/characters/supporting/supporting_*.yaml`
- `settings/characters/relationships.yaml`

## 参考

- Schema: `data/schemas/characters.schema.yaml`
- 引擎: `src/novel/core/skills/design_character.py`
- 旧模式: 旧 generate-character 的分层询问流程
```

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/design-character/SKILL.md
git commit -m "feat(skills): 添加 /design-character SKILL

- 分层询问模式（主角→反派→配角）
- 爽感维度评估（打脸指数/CP感/反派恶心度）
- 调用 DesignCharacterSkill 引擎
- 借鉴旧 generate-character 交互模式"
```

---

### Task 4: 创建 `/golden-chapters` — 黄金三章

**Files:**
- Create: `.claude/skills/golden-chapters/SKILL.md`

- [ ] **Step 1: 创建 SKILL.md**

```markdown
# .claude/skills/golden-chapters/SKILL.md
---
name: golden-chapters
description: 黄金三章锻造。按微节拍逐段生成前三章，验证结构。
---

# 黄金三章锻造

前三章决定生死。按品类模板，逐段生成，严格验证结构。

---

## 前置依赖

- 品类已选择
- 人设已完成（`settings/characters/` 存在）
- 细纲已有初步方向

---

## 工作流程

### 1. 确认项目与品类

读取 `settings/scout_report.yaml` 获取品类。

### 2. 加载品类模板

```python
from novel.core.skills.forge_golden_chapters import ForgeGoldenChaptersSkill
skill = ForgeGoldenChaptersSkill()
template = skill.get_genre_template("genre/xuanhuan")
```

展示品类标准套路：

| 品类 | 标准套路 |
|------|---------|
| 玄幻 | 废柴受辱 → 金手指觉醒 → 首次反击 |
| 都市 | 被退婚/背叛 → 隐藏身份曝光 → 第一波打脸 |
| 系统文 | 系统激活 → 首个任务 → 奖励碾压 |

### 3. 逐章生成

**第一章**：
- 300 字内出第一冲突
- 立住主角人设
- 展示主角起点状态

**第二章**：
- 金手指亮相
- 展示金手指机制与限制

**第三章**：
- 第一个小高潮
- 让读者看到"爽"的可能性

### 4. 结构验证

每章生成后调用引擎验证：

```python
analysis = await skill.validate_chapter(
    text=chapter_text,
    chapter_number=1,
    genre_id="genre/xuanhuan"
)
```

检查清单：
- [ ] 首冲突 ≤ 300 字？
- [ ] 人设建立？
- [ ] 金手指亮相？
- [ ] 第一个小高潮？

未通过项给出修改建议。

### 5. 输出

生成 `content/chapter_001.md`、`chapter_002.md`、`chapter_003.md`。

输出评估报告：

```yaml
# golden_chapters_report.yaml
chapter_1:
  first_conflict_at_word: 250
  character_setup: true
  score: 85
chapter_2:
  golden_finger_reveal: true
  score: 80
chapter_3:
  first_climax: true
  score: 90
overall: 85
passed: true
```

---

## 输出文件

- `content/chapter_001.md`
- `content/chapter_002.md`
- `content/chapter_003.md`
- `golden_chapters_report.yaml`

## 参考

- 引擎: `src/novel/core/skills/forge_golden_chapters.py`
- 品类模板: `TEMPLATES` 字典
```

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/golden-chapters/SKILL.md
git commit -m "feat(skills): 添加 /golden-chapters SKILL

- 按品类模板逐段生成前三章
- 结构验证（首冲突/人设/金手指/高潮）
- 调用 ForgeGoldenChaptersSkill 引擎"
```

---

### Task 5: 创建 `/daily-write` — 日更写作

**Files:**
- Create: `.claude/skills/daily-write/SKILL.md`

> 借鉴旧 `write-chapter` 的续写/改写模式，增加质量门禁流水线。

- [ ] **Step 1: 创建 SKILL.md**

```markdown
# .claude/skills/daily-write/SKILL.md
---
name: daily-write
description: 日更写作入口。扩写 → 核查 → 去AI味 → 钩子审查，通过质量门禁后定稿。
---

# 日更写作

交互式写作章节正文，通过质量门禁流水线确保输出质量。

---

## 前置依赖

- 章节已规划（`settings/chapters/_index.yaml` 有摘要）

---

## 工作流程

### 1. 选择章节

展示待写章节列表，选择本章目标。

### 2. 检查衔接

展示前章结尾 300 字 + 本章摘要，确认衔接点。

### 3. 写作方向

询问写作方向（情节推进/人物展示/环境氛围/对话为主）。

### 4. 生成正文

Agent 直接生成正文（2000-3000 字/章）。

### 5. 质量门禁流水线

生成后自动进入质量检查：

**Gate 1: 事实核查**
```python
from novel.core.skills.check_logic import CheckLogicSkill
skill = CheckLogicSkill()
verdict = await skill.evaluate({"content": chapter_text})
```
- 检查角色名称、时间线、地点一致性
- 未通过 → 给出修正建议

**Gate 2: 去 AI 味**
```python
from novel.core.skills.anti_ai_polish import AntiAiPolishSkill
skill = AntiAiPolishSkill()
verdict = await skill.evaluate(chapter_text)
```
- 五层检测（词汇/句式/段落/叙事/情感）
- 综合分 < 60 → 必须修改
- 检测到的禁词 → 列出替换建议

**Gate 3: 钩子审查**
```python
from novel.core.skills.audit_hooks import AuditHooksSkill
skill = AuditHooksSkill()
verdict = await skill.evaluate(chapter_text)
```
- 检查最后 800 字悬念强度
- 检查全文冲突密度
- 检查章节标题点击吸引力
- 未通过 → 建议修改结尾或标题

### 6. 展示正文 + 审查报告

展示正文开头 500 字 + 结尾 300 字 + 质量审查摘要。

### 7. 续写/改写

不满意时可选：
- **续写**：在已有正文基础上继续写作
- **改写**：修改已有正文（润色/扩充/精简/重写）
- **重新过审**：修改后重新跑质量门禁

### 8. 定稿

通过所有门禁后，写入 `content/chapter_XXX.md`。

---

## 质量门禁标准

| 门禁 | 检查项 | 通过标准 |
|------|--------|---------|
| 事实核查 | 角色/时间/地点一致性 | 无硬逻辑错误 |
| 去AI味 | 五层综合评分 | ≥ 60 分 |
| 钩子审查 | 悬念强度 | ≥ 60 分 |
| 钩子审查 | 冲突密度 | ≥ 60 分 |

---

## 输出文件

- `content/chapter_XXX.md`

## 参考

- 引擎: `src/novel/core/skills/anti_ai_polish.py`、`audit_hooks.py`、`check_logic.py`
- 旧模式: 旧 write-chapter 的续写/改写流程
```

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/daily-write/SKILL.md
git commit -m "feat(skills): 添加 /daily-write SKILL

- 质量门禁流水线（事实核查→去AI味→钩子审查）
- 续写/改写模式
- 调用 AntiAiPolishSkill + AuditHooksSkill + CheckLogicSkill 引擎
- 借鉴旧 write-chapter 交互模式"
```

---

## Phase 2: 架构与数据

### Task 6: 创建 `/design-outline` — 大纲设计

**Files:**
- Create: `.claude/skills/design-outline/SKILL.md`

- [ ] **Step 1: 创建 SKILL.md**

```markdown
# .claude/skills/design-outline/SKILL.md
---
name: design-outline
description: 大纲设计。交互式设计整体故事走向，检测节奏问题。
---

# 大纲设计

交互式设计小说大纲，含节奏检测和张力曲线分析。

---

## 前置依赖

- 世界观已设计（`settings/worldbuilding/` 存在）
- 品类已选择

---

## 工作流程

### 1. 确认项目

运行 `novel list`，选择项目。

### 2. 交互式询问（借鉴旧 generate-outline 模式）

按以下顺序逐步确认：

**核心设定**：一句话概括故事核心

**主角设定**：名字、起点状态、终点状态

**冲突设计**：
- 外部冲突（主要对手/障碍）
- 内部冲突（主角的心理矛盾）

**结构规划**：
- 总章数
- 幕数（建议三幕式）
- 每幕核心事件

**确认生成**：汇总后请用户确认

### 3. 节奏分析

生成大纲后调用引擎检测节奏：

```python
from novel.core.skills.ask_architect import AskArchitectSkill
skill = AskArchitectSkill()
verdict = skill.evaluate({"chapters": chapter_list})
```

检查项：
- 是否连续 3 章以上慢节奏？
- 张力曲线是否合理？
- 高潮节点分布是否均匀？

### 4. 生成大纲文件

Agent 直接生成 `settings/outline/` 目录各文件：
- `premise.yaml`（核心设定）
- `acts/act_*.yaml`（各幕结构）
- `hooks.yaml`（伏笔-回收）
- `pacing.yaml`（节奏曲线）

### 5. 展示与调整

展示大纲结构 + 节奏分析报告。询问是否需要调整。

---

## 输出文件

- `settings/outline/premise.yaml`
- `settings/outline/acts/act_*.yaml`
- `settings/outline/hooks.yaml`
- `settings/outline/pacing.yaml`

## 参考

- Schema: `data/schemas/outline.schema.yaml`
- 引擎: `src/novel/core/skills/ask_architect.py`
- 旧模式: 旧 generate-outline 的交互流程
```

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/design-outline/SKILL.md
git commit -m "feat(skills): 添加 /design-outline SKILL

- 交互式大纲设计（核心设定→冲突→结构）
- 节奏检测 + 张力曲线分析
- 调用 AskArchitectSkill 引擎
- 借鉴旧 generate-outline 交互模式"
```

---

### Task 7: 创建 `/design-chapters` — 细纲设计

**Files:**
- Create: `.claude/skills/design-chapters/SKILL.md`

- [ ] **Step 1: 创建 SKILL.md**

```markdown
# .claude/skills/design-chapters/SKILL.md
---
name: design-chapters
description: 细纲设计。按大纲拆分章节，生成节拍表，检查结构。
---

# 细纲设计

按大纲拆分章节，每章生成节拍表，检查结构合理性。

---

## 前置依赖

- 大纲已设计（`settings/outline/` 存在）

---

## 工作流程

### 1. 检查大纲

展示大纲结构，确认转化范围（全部 / 前 N 章）。

### 2. 确认参数

- 章节数
- 每章字数（短章 1500-2000 / 标准 2000-3000 / 长章 3000-5000）

### 3. 生成章节计划

基于大纲节拍，转化为章节摘要。每章包含：
- number（章节号）
- title（标题）
- summary（摘要）
- tension（张力值）
- beats（节拍表）

### 4. 结构检查

调用引擎检查每章结构：

```python
from novel.core.skills.flesh_out_chapter import FleshOutChapterSkill
skill = FleshOutChapterSkill()
verdict = skill.evaluate(outline)
```

检查项：
- 必要字段是否齐全？
- 节拍数量是否合理（3-15 个）？
- 目标字数是否合理（2000-5000）？

### 5. 展示与调整

展示前 5-10 章预览 + 张力曲线。询问是否合并/拆分/调整。

### 6. 生成章节文件

Agent 生成 `settings/chapters/_index.yaml`。

---

## 章节状态

| 状态 | 含义 |
|------|------|
| planned | 已规划，有摘要，无正文 |
| draft | 有正文草稿 |
| written | 正文完成 |
| revised | 已润色 |

## 输出文件

- `settings/chapters/_index.yaml`

## 参考

- Schema: `data/schemas/chapters.schema.yaml`
- 引擎: `src/novel/core/skills/flesh_out_chapter.py`
```

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/design-chapters/SKILL.md
git commit -m "feat(skills): 添加 /design-chapters SKILL

- 按大纲拆分章节 + 节拍表
- 结构检查（字段/节拍/字数）
- 调用 FleshOutChapterSkill 引擎"
```

---

### Task 8: 创建 `/paywall-design` — 付费卡点设计

**Files:**
- Create: `.claude/skills/paywall-design/SKILL.md`

- [ ] **Step 1: 创建 SKILL.md**

```markdown
# .claude/skills/paywall-design/SKILL.md
---
name: paywall-design
description: 付费卡点设计。分析大纲找最优切割点，设计过渡章节奏。
---

# 付费卡点设计

分析大纲，找到最优付费切割点，设计过渡章节奏。

---

## 前置依赖

- 大纲已完成
- 黄金三章已完成

---

## 工作流程

### 1. 分析大纲

```python
from novel.core.skills.design_paywall import DesignPaywallSkill
skill = DesignPaywallSkill()
analysis = await skill.analyze_outline(outline_text)
```

### 2. 展示推荐卡点

输出：
- 推荐切割章节
- 切割理由（爽点兑现 + 新悬念）
- 警告（如当前处于主角低谷期）

### 3. 设计过渡章

**免费末章**：
- 必须做到"爽点兑现 + 致命悬念"双保险
- 读者合上这一章时，必须"不花钱就难受"

**付费首章**：
- 开头 200 字内必须立刻给出爽感反馈
- 随后展开新弧线

### 4. 评估过渡章

```python
verdict = await skill.evaluate(transition_chapter_text)
```

检查：
- 爽点是否兑现？
- 悬念是否抛出？

### 5. 输出

生成 `paywall_report.yaml`：

```yaml
paywall_chapter: 25
reasoning: "第24章主角首次击败小反派（爽点兑现），第25章开头大反派登场（新悬念）"
free_last_chapter_design:
  - 爽点兑现
  - 致命悬念抛出
paid_first_chapter_design:
  - 200字内爽感反馈
  - 展开新弧线
```

---

## 输出文件

- `paywall_report.yaml`

## 参考

- 引擎: `src/novel/core/skills/design_paywall.py`
```

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/paywall-design/SKILL.md
git commit -m "feat(skills): 添加 /paywall-design SKILL

- 分析大纲推荐付费切割点
- 设计过渡章节奏（免费末章+付费首章）
- 调用 DesignPaywallSkill 引擎"
```

---

### Task 9: 创建 `/data-diagnosis` — 数据诊断

**Files:**
- Create: `.claude/skills/data-diagnosis/SKILL.md`

- [ ] **Step 1: 创建 SKILL.md**

```markdown
# .claude/skills/data-diagnosis/SKILL.md
---
name: data-diagnosis
description: 数据诊断。导入平台数据，分析追读率/互动率，定位问题章节。
---

# 数据诊断

导入平台后台数据，分析追读率、互动率，定位问题章节并给出改进建议。

---

## 工作流程

### 1. 导入数据

用户从平台后台导出数据 CSV，提供文件路径。

### 2. 解析数据

```python
from novel.core.skills.analyze_stats import AnalyzeStatsSkill
skill = AnalyzeStatsSkill()
chapter_stats = skill.parse_stats_csv(csv_data)
```

### 3. 综合分析

```python
overall = skill.calculate_overall_stats(chapter_stats)
retention_issues = skill.detect_retention_drop(chapter_stats)
engagement_issues = skill.detect_low_engagement(chapter_stats)
verdict = skill.evaluate(chapter_stats)
```

### 4. 展示诊断报告

输出：

```
== 数据诊断报告 ==

总体数据：
- 总章数: 50
- 平均追读率: 65%
- 平均完读率: 72%

问题章节：
- 第12章：追读率下降 25%（从 70% 降至 52%）
- 第23章：互动率偏低（评论 3，平均 25）

改进建议：
- 第12章节奏拖沓，建议精简
- 第23章缺少冲突，建议增加打脸情节
```

### 5. 输出

生成 `data_diagnosis_report.yaml`。

---

## 输出文件

- `data_diagnosis_report.yaml`

## 参考

- 引擎: `src/novel/core/skills/analyze_stats.py`
```

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/data-diagnosis/SKILL.md
git commit -m "feat(skills): 添加 /data-diagnosis SKILL

- CSV 数据导入
- 追读率/互动率分析
- 问题章节定位 + 改进建议
- 调用 AnalyzeStatsSkill 引擎"
```

---

## Phase 3: 管理工具

### Task 10: 创建 `/stock-check` — 存稿看板

**Files:**
- Create: `.claude/skills/stock-check/SKILL.md`

- [ ] **Step 1: 创建 SKILL.md**

```markdown
# .claude/skills/stock-check/SKILL.md
---
name: stock-check
description: 存稿看板。查看存稿水位、成本报告、应急建议。
---

# 存稿看板

查看存稿状态、成本消耗、应急建议。

---

## 工作流程

### 1. 统计存稿

```python
from novel.core.workflow.daily_manager import DailyUpdateManager
from novel.core.workflow.manuscript_store import ManuscriptStore, ManuscriptTier

manager = DailyUpdateManager(
    written_chapters=written,
    published_chapters=published,
    mode="fine"
)
status = manager.check_reserves()
```

### 2. 展示看板

```
== 存稿看板 ==

存稿水位: 🟢 正常（12 章）
- 精修稿: 5 章（可直接发布）
- 粗稿: 4 章（需去AI味）
- 大纲稿: 3 章（需扩写）

成本报告:
- 今日消耗: $3.20
- 剩余预算: $11.80

建议:
- 存稿充足，可切换精细模式
```

### 3. 应急建议

| 水位 | 等级 | 建议 |
|------|------|------|
| ≥10 章 | 🟢 正常 | 正常运行 |
| 6-9 章 | 🟡 预警 | 暂停非紧急任务 |
| ≤5 章 | 🔴 危险 | 切换快速模式 |

---

## 输出

控制台报告（不写文件）

## 参考

- 引擎: `src/novel/core/workflow/daily_manager.py`、`manuscript_store.py`
```

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/stock-check/SKILL.md
git commit -m "feat(skills): 添加 /stock-check SKILL

- 存稿水位统计（精修/粗稿/大纲三级）
- 成本报告
- 应急建议
- 调用 DailyUpdateManager 引擎"
```

---

### Task 11: 创建 `/worldbuilding` — 世界观设计

**Files:**
- Create: `.claude/skills/worldbuilding/SKILL.md`

- [ ] **Step 1: 创建 SKILL.md**

```markdown
# .claude/skills/worldbuilding/SKILL.md
---
name: worldbuilding
description: 世界观设计。与 Agent 交互讨论力量体系、社会结构、基础规则。
---

# 世界观设计

交互式设计小说世界观，包括力量体系、社会结构、基础规则。

---

## 前置依赖

- 品类已选择（`settings/scout_report.yaml` 存在）

---

## 工作流程

### 1. 确认项目

运行 `novel list`，选择项目。

### 2. 品类适配

读取 `settings/scout_report.yaml`，基于品类推荐世界观框架：

| 品类 | 推荐框架 |
|------|---------|
| 玄幻 | 修炼等级体系、宗门势力、天材地宝 |
| 都市 | 社会阶层、商业规则、隐藏势力 |
| 系统文 | 系统规则、任务机制、奖励体系 |

### 3. 交互讨论

与用户逐步讨论：

**力量体系**：
- 等级划分
- 升级条件
- 战力表现

**社会结构**：
- 主要势力
- 势力关系
- 社会规则

**基础规则**：
- 世界运行的核心规则
- 禁忌/限制

### 4. 生成文件

Agent 直接生成 `settings/worldbuilding/` 目录各文件：
- `power_system.yaml`（力量体系）
- `factions/faction_*.yaml`（势力档案）
- `locations/location_*.yaml`（地点档案）
- `lore/*.yaml`（传说/术语）

### 5. 展示与调整

展示世界观概览。询问是否调整。

---

## 输出文件

- `settings/worldbuilding/power_system.yaml`
- `settings/worldbuilding/factions/`
- `settings/worldbuilding/locations/`
- `settings/worldbuilding/lore/`

## 参考

- 模板: `templates/default/settings/worldbuilding/`
```

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/worldbuilding/SKILL.md
git commit -m "feat(skills): 添加 /worldbuilding SKILL

- 品类适配的世界观框架推荐
- 交互式讨论（力量体系→社会结构→基础规则）
- Agent 直接生成 worldbuilding 目录文件"
```

---

## 验收标准

| 检查项 | 标准 |
|--------|------|
| 旧 SKILL 删除 | 7 个目录全部删除 |
| 新 SKILL 创建 | 10 个 SKILL.md 全部创建 |
| SKILL 格式 | 每个 SKILL.md 有 frontmatter（name + description） |
| 引擎引用 | 每个 SKILL.md 引用对应的 Python 引擎 |
| 交互流程 | 每个 SKILL.md 有清晰的工作流程 |
