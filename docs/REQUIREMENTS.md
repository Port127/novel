# 项目需求文档

> 本文档记录 Novel V2 的核心用户需求，所有架构设计和技术决策必须服务于这些需求。

## 相关文档

- [.agents/AGENTS.md](../.agents/AGENTS.md) — Agent 规则与工作流
- [README.md](../README.md) — 项目入口与功能说明
- [docs/USER_MANUAL.md](USER_MANUAL.md) — 用户使用手册
- [data/schemas/](../data/schemas/) — YAML Schema 定义

---

## 一、项目定位

**Novel V2 是一个面向网文作者的 AI 辅助写作工具。**

它不是用来"自动生成小说"的工具，而是用来**辅助作者完成创作流程**的交互式系统，从选题到完本全程支持。

**与 novel-material 的关系**：

| 项目 | 定位 | 关系 |
|------|------|------|
| novel-material | 素材检索库 | 上游，提供同类作品的结构化分析 |
| novel-v2 | 写作工具 | 本项目，调用上游检索服务辅助创作 |

---

## 二、创作流程

Novel V2 支持完整的网文创作流程，从选题到完本：

```
1. 选题侦察 (scout-topic)
   ↓
2. 世界观设计 (worldbuilding)
   ↓
3. 人设设计 (design-character)
   ↓
4. 大纲设计 (design-outline)
   ↓
5. 细纲设计 (design-chapters)
   ↓
6. 黄金三章锻造 (golden-chapters)
   ↓
7. 付费卡点设计 (paywall-design)
   ↓
8. 日更写作 (daily-write)
   ↓
9. 导出作品 (export-novel)
```

每个阶段都有完善度检查，未达标不能进入下一阶段。

---

## 三、Skills 系统

### 3.1 V4 Skill 架构

Skills 是交互式创作的核心入口。每个创作 skill 采用**自包含结构**：

```
.agents/skills/<skill-name>/
├── SKILL.md              ← Phase 化流程 + 质量门禁
├── references/           ← 领域知识文件（按需加载）
└── scripts/              ← JS 验证脚本（确定性检查）
```

**核心机制**：

| 机制 | 说明 |
|------|------|
| **Phase 化流程** | 每个 Phase 有明确入口/出口条件，可独立执行和恢复 |
| **确定性脚本门禁** | JS 脚本做质量检查（blocking/advisory 两级） |
| **断点恢复** | `_progress.md` 记录进度，崩溃后从断点续跑 |
| **品类感知** | 根据 `scout_report.yaml` 的 `required_elements` 动态决定检查内容 |

**汇总统计**：9 个创作 skill，39 个 references，14 个 JS 脚本。

### 3.2 创作类 Skills

| Skill | 用途 | Phase 数 | References | Scripts | 前置依赖 | 输出 |
|-------|------|:--------:|:----------:|:-------:|---------|------|
| `scout-topic` | 品类选择 + 选题分析 | 6 | 4 | 1 | 无 | `settings/scout_report.yaml` |
| `worldbuilding` | 世界观设计 | 5 | 4 | 1 | 品类已选择 | `settings/worldbuilding.yaml` |
| `design-character` | 人设设计（含爽感评估） | 5 | 5 | 1 | 品类已选择 | `settings/characters.yaml` |
| `design-outline` | 大纲设计（含节奏分析） | 5 | 5 | 2 | 品类+世界观 | `settings/outline.yaml` + `arcs.yaml` + `pacing.yaml` |
| `design-chapters` | 细纲设计（章节拆分） | 5 | 3 | 1 | 大纲已完成 | `settings/chapters_index.yaml` |
| `golden-chapters` | 黄金三章锻造 | 6 | 4 | 3 | 品类+人设+细纲 | `content/chapter_001-003.md` |
| `paywall-design` | 付费卡点设计 | 5 | 4 | 1 | 大纲+黄金三章 | `paywall_report.yaml` |
| `daily-write` | 日更写作（含质量门禁） | 6 | 6 | 3 | 章节已规划 | `content/chapter_XXX.md` |
| `export-novel` | 导出作品 | — | — | — | 正文已完成 | TXT/MD/EPUB |

### 3.3 辅助类 Skills

| Skill | 用途 |
|-------|------|
| `nm` | 素材检索（章节/大纲/人物/世界观/事件/细纲/深度分析） |
| `stock-check` | 库存检查 |
| `data-diagnosis` | 数据诊断 |
| `feature-planning` | 功能规划 |
| `code-review-change` | 代码审查 |
| `commit-msg` | 提交消息生成 |
| `refactor-planning` | 重构规划 |

---

## 四、品类感知质量门禁

不同品类的小说需要不同的元素。质量门禁不硬编码，而是根据每本小说的品类和声明动态检查。

### 4.1 三层结构

| 层 | 位置 | 内容 |
|----|------|------|
| **品类模板** | skill references | "玄幻通常需要力量体系" 等建议 |
| **小说声明** | `scout_report.yaml` 的 `required_elements` | "这本需要 era_details、locations" |
| **实际数据** | `settings/*.yaml` | 具体的力量体系设计、角色设计等 |

### 4.2 required_elements 示例

```yaml
# scout_report.yaml
required_elements:
  worldbuilding:
    required: [era_details, locations, social_rules]
    optional: [business_opportunities]
  characters:
    protagonist: required
    love_interest: required
    rival: optional
  opening_hook:
    type: reborn_advantage
    description: "前世记忆+行业洞察"
  structure:
    type: 起承转合
    target_arcs: 4
```

### 4.3 品类默认值

| 品类 | 默认 worldbuilding | 默认 characters | 默认 opening_hook | 默认 structure |
|------|-------------------|-----------------|-------------------|----------------|
| xuanhuan | power_system, factions, locations | protagonist+mentor+villain | golden_finger | 三幕式, 幕≥3 |
| urban | era_details, locations, social_rules | protagonist+supporting_cast | conflict | 起承转合, arcs≥4 |
| system | system_rules, quest_mechanics | protagonist+system_entity | golden_finger | 三幕式, 幕≥3 |
| romance | locations, relationship_context | protagonist+love_interest | meet_cute | 起承转合, arcs≥3 |

---

## 五、CLI 命令

管理类操作通过 CLI 命令完成，只做文件系统操作，不调用 LLM：

```bash
# 项目管理
novel new "书名" --genre 类型 --author 作者
novel list
novel show <project_id>
novel delete <project_id>
```

**注意**：创作类操作（世界观、人设、大纲、正文等）全部通过 Skills 完成，Agent 直接生成内容。

---

## 六、目录结构

### 项目目录

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
│   ├── _index.yaml
│   └── ...
├── content/               # 正文
│   └── chapter_*.md
├── drafts/                # 草稿
├── exports/               # 导出
└── _progress.md           # 断点恢复状态（daily-write 等）
```

### 项目根目录

```
novel/
├── novels/                    # 写作项目目录
├── src/novel/                 # 核心引擎（退化为基础设施）
├── data/schemas/              # YAML Schema 定义
├── templates/                 # 项目模板
└── .agents/skills/            # Agent Skills（V4 自包含结构）
```

---

## 七、状态流转

### 项目状态

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

## 八、质量门禁

### 8.1 质量门禁架构

采用**双层质量门禁**：JS 脚本（确定性检查）+ LLM 评估（语义检查）。

### 8.2 各 Skill 质量门禁

| Skill | JS 脚本 | LLM 评估 |
|-------|--------|---------|
| scout-topic | check-tags.js | — |
| worldbuilding | check-completeness.js | — |
| design-character | check-characters.js | 爽感三维评估 |
| design-outline | check-outline.js + check-pacing.js | — |
| design-chapters | check-chapters.js | — |
| golden-chapters | check-golden-structure.js + check-ai-patterns.js + check-degeneration.js | — |
| daily-write | check-ai-patterns.js + check-degeneration.js + normalize-punctuation.js | 反AI五层评分 ≥ 60 + 钩子评分 ≥ 60 |
| paywall-design | check-paywall.js | — |

### 8.3 JS 脚本规范

| 属性 | 说明 |
|------|------|
| 语言 | JavaScript（Node.js） |
| 依赖 | 仅 Node.js 内建模块（fs, path） |
| 级别 | blocking（必须修到 0）/ advisory（建议） |
| 退出码 | 0=通过，1=有问题，2=脚本错误 |

---

## 九、硬规则

**必须：**
- 创作类操作使用 Skills 交互式完成
- 逐步询问，不跳过用户确认
- 尊重已有设定，逐步细化让用户确认
- 状态流转按顺序进行
- 品类选择前置（所有设计依赖品类）

**禁止：**
- 跳过用户确认直接生成
- 在未规划章节时写作正文
- 跳阶段：未完成品类时设计世界观/人物/大纲
- 覆盖已有设定

---

## 十、成功标准

本项目是否成功，取决于用户能否在实际写作中：

1. **交互式创作流畅**：询问 → 确认 → 生成 → 调整的流程顺畅
2. **设定一致性**：世界观/人物设定在整个写作过程中保持一致
3. **正文质量可接受**：生成正文语义连贯，符合章纲要求，通过双层质量门禁
4. **商业化适配**：支持黄金三章、付费卡点等网文商业化需求
5. **进度可控**：用户可随时查看项目状态和统计
6. **断点恢复**：长任务中断后可从断点续跑
