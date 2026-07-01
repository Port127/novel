# Commercial Copilot SKILL 体系设计 (V3)

## 1. 设计原则

### 1.1 问题陈述
原有 7 个 SKILL（create-novel、generate-character 等）缺乏商业化能力：
- 无品类适配
- 无爽感维度评估
- 无付费卡点设计
- 无质量门禁（去AI味、钩子审查）
- 无存稿管理

### 1.2 设计目标
- **拆分**：每个创作阶段独立为 Skill，避免上下文耗尽
- **聚焦**：每个 Skill 专注一件事，可深入讨论
- **独立**：所有 Skill 可单独调用，无强制串联
- **引擎驱动**：底层由 Python Skill 提供能力支撑

### 1.3 删除清单
以下旧 SKILL 删除：
- `create-novel` — 无商业化能力
- `generate-character` — 无爽感维度
- `generate-outline` — 无节奏检测
- `generate-chapter` — 无微节拍
- `write-chapter` — 无质量门禁
- `revise-setting` — 旧架构产物
- `show-project` — 无存稿管理

### 1.4 保留清单
以下 SKILL 保留不动：
- `nm` — 素材检索
- `export-novel` — 导出工具
- `code-review-change` — 开发工具
- `commit-msg` — 开发工具
- `feature-planning` — 开发工具
- `refactor-planning` — 开发工具

---

## 2. 新 SKILL 体系

### 2.1 新书筹备线（7 个 Skill）

#### `/scout-topic` — 选题侦察兵
**触发**：用户开新书或想找题材

**调用引擎**：
- `GenreRouter` — 品类选择
- `ScoutTopicSkill` — 选题分析

**工作流程**：
1. 询问品类（玄幻/都市/系统文/其他）
2. 调用 `GenreRouter.set_genre()`
3. 调用 `ScoutTopicSkill.analyze_market()`
4. 输出：推荐标签组合、竞争度、潜力评分、窗口期建议

**输出文件**：`settings/scout_report.yaml`

---

#### `/worldbuilding` — 世界观设计
**触发**：新书筹备阶段 2

**调用引擎**：无（纯 Agent 交互）

**工作流程**：
1. 基于品类推荐世界观框架
2. 与用户交互讨论力量体系、社会结构、基础规则
3. 输出 `worldbuilding/` 目录文件

**输出文件**：
- `worldbuilding/power_system.yaml`
- `worldbuilding/factions/`
- `worldbuilding/locations/`

---

#### `/design-outline` — 大纲设计
**触发**：世界观完成后

**调用引擎**：`AskArchitectSkill`

**工作流程**：
1. 与用户讨论整体故事走向
2. 调用 `AskArchitectSkill.analyze_outline()`
3. 检测节奏问题、张力曲线
4. 输出大纲 + 节奏分析报告

**输出文件**：
- `outline/premise.yaml`
- `outline/acts/`
- `outline/rhythm_report.yaml`

---

#### `/design-chapters` — 细纲设计
**触发**：大纲完成后

**调用引擎**：`FleshOutChapterSkill`

**工作流程**：
1. 按大纲拆分章节（前 30-50 章）
2. 每章生成节拍表
3. 调用 `FleshOutChapterSkill.evaluate()` 检查结构
4. 输出章节规划文件

**输出文件**：`chapters/_index.yaml`

---

#### `/design-character` — 人设设计
**触发**：大纲完成后（可与细纲并行）

**调用引擎**：`DesignCharacterSkill`

**工作流程**：
1. 在世界观和大纲框架下设计人物
2. 调用 `DesignCharacterSkill.design_character()`
3. 计算打脸指数、CP感、反派恶心度
4. 输出人物设定文件

**输出文件**：
- `characters/protagonist.yaml`
- `characters/antagonist/`
- `characters/relationships.yaml`

---

#### `/golden-chapters` — 黄金三章
**触发**：人设+细纲完成后

**调用引擎**：`ForgeGoldenChaptersSkill`

**工作流程**：
1. 按品类加载微节拍模板
2. 逐段生成前三章
3. 调用 `ForgeGoldenChaptersSkill.validate_chapter()`
4. 检查：首冲突≤300字、人设建立、金手指亮相、第一个小高潮
5. 输出黄金三章初稿 + 评估报告

**输出文件**：
- `content/chapter_001.md`
- `content/chapter_002.md`
- `content/chapter_003.md`
- `golden_chapters_report.yaml`

---

#### `/paywall-design` — 付费卡点设计
**触发**：黄金三章完成后

**调用引擎**：`DesignPaywallSkill`

**工作流程**：
1. 调用 `DesignPaywallSkill.analyze_outline()`
2. 分析最优付费切割点（爽点兑现后 + 新悬念抛出）
3. 设计过渡章节奏
4. 输出付费卡点建议 + 过渡章评估

**输出文件**：`paywall_report.yaml`

---

### 2.2 日常创作线（2 个 Skill）

#### `/daily-write` — 日更写作
**触发**：日常写作

**调用引擎**：
- `FleshOutChapterSkill` — 节拍扩写
- `CheckLogicSkill` — 事实核查
- `AntiAiPolishSkill` — 去AI味
- `AuditHooksSkill` — 钩子审查

**工作流程**：
1. 选择待写章节
2. 扩写（调用 `FleshOutChapterSkill`）
3. 事实核查（调用 `CheckLogicSkill`）
4. 去 AI 味（调用 `AntiAiPolishSkill`，五层检测）
5. 钩子审查（调用 `AuditHooksSkill`）
6. 输出：通过审查的定稿

**质量门禁**：
- AntiAi 综合分 ≥ 60
- Hook 悬念强度 ≥ 60
- 无事实错误

**输出文件**：`content/chapter_XXX.md`

---

#### `/stock-check` — 存稿看板
**触发**：随时查看

**调用引擎**：`DailyUpdateManager`

**工作流程**：
1. 统计存稿（精修/粗稿/大纲三级）
2. 计算存稿水位（绿色≥10 / 黄色≥6 / 红色≤5）
3. 评估成本消耗
4. 输出存稿报告 + 应急建议

**输出**：控制台报告（不写文件）

---

### 2.3 数据复盘线（1 个 Skill）

#### `/data-diagnosis` — 数据诊断
**触发**：发布 5-10 章后

**调用引擎**：`AnalyzeStatsSkill`

**工作流程**：
1. 导入平台数据（CSV）
2. 调用 `AnalyzeStatsSkill`
3. 检测追读率下降、低互动章节
4. 输出诊断报告 + 改进建议

**输出文件**：`data_diagnosis_report.yaml`

---

## 3. SKILL 与引擎映射

| SKILL | 引擎层 | 职责 |
|-------|--------|------|
| `/scout-topic` | `GenreRouter` + `ScoutTopicSkill` | 品类选择 + 选题分析 |
| `/worldbuilding` | 无（纯交互） | 世界观设计 |
| `/design-outline` | `AskArchitectSkill` | 大纲设计 + 节奏检测 |
| `/design-chapters` | `FleshOutChapterSkill` | 细纲设计 + 结构检查 |
| `/design-character` | `DesignCharacterSkill` | 人设设计 + 爽感评估 |
| `/golden-chapters` | `ForgeGoldenChaptersSkill` | 黄金三章 + 结构验证 |
| `/paywall-design` | `DesignPaywallSkill` | 付费卡点分析 |
| `/daily-write` | `AntiAiPolish` + `AuditHooks` + `CheckLogic` | 日更写作 + 质量门禁 |
| `/data-diagnosis` | `AnalyzeStatsSkill` | 数据分析 + 问题诊断 |
| `/stock-check` | `DailyUpdateManager` | 存稿管理 + 成本监控 |

---

## 4. 实施计划

### Phase 1：核心创作线（优先）
1. `/scout-topic`
2. `/design-character`
3. `/golden-chapters`
4. `/daily-write`

### Phase 2：架构与数据
5. `/design-outline`
6. `/design-chapters`
7. `/paywall-design`
8. `/data-diagnosis`

### Phase 3：管理工具
9. `/stock-check`
10. `/worldbuilding`

---

## 5. User Review Required

> [!IMPORTANT]
> - 本设计彻底删除 7 个旧 SKILL，新建 10 个独立 SKILL
> - 每个 SKILL 专注一个创作阶段，可独立调用
> - 底层由 Python Skill 引擎提供能力支撑
> - 请确认整体架构是否符合你的创作习惯
