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

Skills 是交互式创作的核心入口。Agent 直接生成内容，不调用脚本。

### 创作类 Skills

| Skill | 用途 | 前置依赖 | 输出 |
|-------|------|---------|------|
| `scout-topic` | 品类选择 + 选题分析 | 无 | `settings/scout_report.yaml` |
| `worldbuilding` | 世界观设计 | 品类已选择 | `settings/worldbuilding/` |
| `design-character` | 人设设计（含爽感评估） | 品类已选择 | `settings/characters/` |
| `design-outline` | 大纲设计（含节奏分析） | 品类+世界观 | `settings/outline/` |
| `design-chapters` | 细纲设计（章节拆分） | 大纲已完成 | `settings/chapters/` |
| `golden-chapters` | 黄金三章锻造 | 品类+人设+细纲 | `content/chapter_001-003.md` |
| `paywall-design` | 付费卡点设计 | 大纲+黄金三章 | `paywall_report.yaml` |
| `daily-write` | 日更写作（含质量门禁） | 章节已规划 | `content/chapter_XXX.md` |
| `export-novel` | 导出作品 | 正文已完成 | TXT/MD/EPUB |

### 辅助类 Skills

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
├── settings/              # 设定文件
│   ├── scout_report.yaml  # 选题报告
│   ├── worldbuilding/     # 世界观
│   │   ├── power_system.yaml
│   │   ├── factions/
│   │   ├── locations/
│   │   └── lore/
│   ├── characters/        # 人物
│   │   ├── protagonist/
│   │   ├── antagonist/
│   │   ├── supporting/
│   │   └── relationships.yaml
│   ├── outline/           # 大纲
│   │   ├── premise.yaml
│   │   ├── acts/
│   │   ├── hooks.yaml
│   │   └── pacing.yaml
│   └── chapters/          # 细纲
│       └── _index.yaml
├── content/               # 正文
│   └── chapters/
├── drafts/                # 草稿
├── exports/               # 导出
└── history/               # 历史
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

日更写作（daily-write）包含质量门禁流水线：

| 门禁 | 检查项 | 通过标准 |
|------|--------|---------|
| 事实核查 | 角色/时间/地点一致性 | 无硬逻辑错误 |
| 去AI味 | 五层综合评分 | ≥ 60 分 |
| 钩子审查 | 悬念强度 | ≥ 60 分 |
| 钩子审查 | 冲突密度 | ≥ 60 分 |

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
3. **正文质量可接受**：生成正文语义连贯，符合章纲要求，通过质量门禁
4. **商业化适配**：支持黄金三章、付费卡点等网文商业化需求
5. **进度可控**：用户可随时查看项目状态和统计
