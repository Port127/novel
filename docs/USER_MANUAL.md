# 用户手册

Novel V2 使用指南。

---

## 快速开始

### 1. 创建项目

```bash
novel new "我的小说" --genre 修仙 --author "作者名"
```

系统会返回项目 ID（如 `nv_20260625_abcd`），后续操作都需要用到。

### 2. 开始创作

按完整创作流程逐步进行：

```
1. /scout-topic      — 选题侦察（品类选择）
2. /worldbuilding    — 世界观设计
3. /design-character — 人设设计
4. /design-outline   — 大纲设计
5. /design-chapters  — 细纲设计
6. /golden-chapters  — 黄金三章锻造
7. /paywall-design   — 付费卡点设计
8. /daily-write      — 日更写作
9. /export-novel     — 导出作品
```

### 3. 查看进度

```bash
novel show <project_id>
novel list
```

---

## V4 Skill 系统

### 自包含结构

每个创作 skill 是自包含的，包含：

| 组件 | 说明 |
|------|------|
| `SKILL.md` | Phase 化流程定义 + 质量门禁 |
| `references/` | 领域知识文件（按需加载） |
| `scripts/` | JS 验证脚本（确定性检查） |

### Phase 化流程

每个 skill 由多个 Phase 组成，每个 Phase 有明确的入口/出口条件：

- **入口条件**：需要哪些前置文件/状态
- **出口条件**：本 Phase 完成的标志
- **加载 References**：本 Phase 需要读取的知识文件

### 断点恢复

长任务（如日更写作）通过 `_progress.md` 记录进度。如果中断：
- 再次进入 skill 时，会检测是否有未完成的进度
- 可选择从断点继续

### 品类感知

在选题阶段（scout-topic）会配置 `required_elements`，声明这本小说需要什么元素。后续所有 skill 的质量门禁据此动态调整：

```yaml
# scout_report.yaml 中的 required_elements
required_elements:
  worldbuilding:
    required: [era_details, locations, social_rules]  # 都市类
  characters:
    protagonist: required
    love_interest: required
  opening_hook:
    type: reborn_advantage
```

---

## Skills 使用指南

### /scout-topic — 选题侦察（推荐入口）

品类选择 + 选题分析，是所有后续设计的基础。

**Phase 流程**：
1. **品类定位** — 选择目标品类（玄幻/都市/系统文等）
2. **平台分析** — 分析目标平台和读者群体
3. **选题决策** — 推荐选题方向
4. **标签策略** — 推荐标签组合（通过 check-tags.js 验证）
5. **品类感知配置** — 配置 required_elements
6. **报告定稿** — 输出 `settings/scout_report.yaml`

### /worldbuilding — 世界观设计

**前置依赖**：品类已选择

**Phase 流程**：
1. **品类适配** — 基于品类推荐世界观框架
2. **力量体系** — 等级/升级/战斗（如需要）
3. **社会结构** — 势力/规则（如需要）
4. **基础规则** — 世界运行规则（如需要）
5. **落盘验证** — 通过 check-completeness.js 检查
6. **输出** — `settings/worldbuilding.yaml`

### /design-character — 人设设计

**前置依赖**：品类已选择

**Phase 流程**：
1. **品类适配** — 加载角色框架
2. **主角设计** — 分层设计主角（traits + psychology + arc）
3. **反派设计** — 反派动机/手段/恶心度（如需要）
4. **配角与关系网络** — 配角 ≥ 3 + 关系网
5. **爽感评估与落盘** — 三维评估 + check-characters.js
6. **输出** — `settings/characters.yaml`

**爽感三维评估**：
- 打脸指数（face-slap index）≥ 6/10
- CP感（chemistry）≥ 6/10
- 反派恶心度（disgust level）≥ 6/10

### /design-outline — 大纲设计

**前置依赖**：品类+世界观

**Phase 流程**：
1. **品类适配与结构选择** — 三幕式/起承转合/英雄之旅
2. **骨架搭建** — 幕级大纲 + 张力曲线
3. **序列细化** — 每幕 2-5 序列
4. **节拍填充** — 每序列 3-8 节拍
5. **落盘验证** — check-outline.js + check-pacing.js
6. **输出** — `settings/outline.yaml` + `settings/arcs.yaml` + `settings/pacing.yaml`

### /design-chapters — 细纲设计

**前置依赖**：大纲已完成

**Phase 流程**：
1. **大纲解析** — 提取节拍列表
2. **章节拆分** — 每章 3-15 节拍，密/疏标记
3. **章节摘要** — 五要素摘要 + 出场人物
4. **张力曲线** — 每章张力值（1-5）
5. **落盘验证** — check-chapters.js
6. **输出** — `settings/chapters_index.yaml`

### /golden-chapters — 黄金三章锻造

**前置依赖**：品类+人设+细纲

**Phase 流程**：
1. **品类适配** — 加载品类黄金三章模板
2. **第一章锻造** — 300字内出冲突/钩子
3. **第二章锻造** — 金手指/核心优势亮相
4. **第三章锻造** — 首个小高潮
5. **去AI味** — check-ai-patterns.js + check-degeneration.js
6. **定稿输出** — `content/chapter_001-003.md`

### /paywall-design — 付费卡点设计

**前置依赖**：大纲+黄金三章

**Phase 流程**：
1. **大纲分析** — 标记候选切点
2. **切点决策** — 评估候选点
3. **过渡设计** — 免费末章+付费首章
4. **平台适配** — 番茄/起点/晋江差异
5. **落盘验证** — check-paywall.js
6. **输出** — `paywall_report.yaml`

### /daily-write — 日更写作

**前置依赖**：章节已规划

**Phase 流程**：
1. **选题确认** — 选择章节
2. **上下文加载** — 前章末300字+本章细纲+追踪文件
3. **写作执行** — 2000-5000 字/章
4. **确定性检查** — check-ai-patterns.js + check-degeneration.js + normalize-punctuation.js
5. **LLM 评估** — 反AI评分 ≥ 60 + 钩子评分 ≥ 60
6. **定稿** — `content/chapter_XXX.md`

**断点恢复**：如果中断，再次进入会提示是否续跑。

### /nm — 素材检索

需要参考时调用：

```
"查一下修仙类的小说"
→ 查分类 → 检索参考 → 糅合建议
```

支持检索：章节/大纲/人物/世界观/事件/细纲/深度分析

### /export-novel — 导出作品

支持格式：TXT、Markdown、EPUB

---

## CLI 命令

### 项目管理

```bash
# 创建项目
novel new "书名" --genre 类型 --author 作者

# 列出项目
novel list

# 查看详情
novel show <project_id>

# 删除项目
novel delete <project_id>
```

---

## 项目状态

### 项目状态流转

```
planning → drafting → revising → completed
```

| 状态 | 允许操作 |
|------|---------|
| planning | 世界观/人设/大纲/细纲设计 |
| drafting | 日更写作、黄金三章、付费卡点 |
| revising | 改写、润色 |
| completed | 导出 |

### 章节状态

```
planned → draft → written → revised
```

| 状态 | 说明 |
|------|------|
| planned | 有摘要，无正文 |
| draft | 有正文草稿 |
| written | 正文完成 |
| revised | 已润色 |

---

## 质量门禁

### 双层架构

| 层 | 工具 | 说明 |
|----|------|------|
| **确定性检查** | JS 脚本 | blocking 必须修到 0，advisory 是建议 |
| **语义检查** | LLM 评估 | 反AI五层评分、钩子评分等 |

### 各 Skill 门禁

| Skill | JS 脚本 | 通过标准 |
|-------|--------|---------|
| scout-topic | check-tags.js | 无标签冲突 |
| worldbuilding | check-completeness.js | required 元素完整 |
| design-character | check-characters.js | 必需角色齐全 + 深度达标 |
| design-outline | check-outline.js + check-pacing.js | 结构完整 + 节奏健康 |
| design-chapters | check-chapters.js | 节拍 3-15 + 字数 2000-5000 |
| golden-chapters | check-ai-patterns.js + check-degeneration.js | blocking 归零 |
| daily-write | 3 个 JS 脚本 + LLM 评估 | blocking 归零 + 评分 ≥ 60 |
| paywall-design | check-paywall.js | 切点章张力 > 均值 |

---

## 常见问题

### Q: 可以跳过阶段吗？

不可以。每个阶段有完善度检查，未达标不能进入下一阶段。品类选择（阶段0）是所有设计的基础。

### Q: 可以修改已完成的设定吗？

可以，但需要重新检查完善度，并可能影响后续阶段。

### Q: 如何参考其他小说？

使用 `/nm` skill 检索素材库，获取同类作品的结构分析。

### Q: 黄金三章有什么要求？

前三章决定生死，必须满足：
- 首冲突 ≤ 300 字
- 人设建立
- 金手指亮相
- 第一个小高潮

### Q: 写作中断了怎么办？

日更写作（daily-write）支持断点恢复。`_progress.md` 记录当前章节和 Phase，再次进入 skill 时会提示是否续跑。

### Q: 什么是品类感知？

在选题阶段（scout-topic）会配置 `required_elements`，声明这本小说需要什么元素。后续 skill 的质量门禁据此动态调整，例如都市类不检查力量体系，玄幻类不检查时代背景。

### Q: 付费卡点如何设计？

`/paywall-design` 会分析大纲，找到最优切割点（爽点兑现+新悬念），并设计过渡章节奏。不同平台（番茄/起点/晋江）有不同的策略。

---

## 目录结构

单个项目的完整结构：

```
novels/{project_id}/
├── project.yaml           # 项目元信息
├── settings/              # 设定文件（扁平化结构）
│   ├── scout_report.yaml  # 选题报告（含 required_elements）
│   ├── worldbuilding.yaml # 世界观设定
│   ├── characters.yaml    # 人物设定
│   ├── outline.yaml       # 大纲
│   ├── arcs.yaml          # 细纲（Arc结构）
│   ├── pacing.yaml        # 节奏规划
│   ├── chapters_index.yaml # 章节索引
│   └── notes.yaml         # 草稿/笔记
├── references/            # 项目特有参考资料
│   ├── _index.yaml        # 顶层索引
│   └── ...                # 按小说需求自由组织
├── content/               # 正文
│   └── chapter_*.md
├── drafts/                # 草稿
├── exports/               # 导出文件
└── _progress.md           # 断点恢复状态（如有）
```
