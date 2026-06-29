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

## Skills 使用指南

### /scout-topic — 选题侦察（推荐入口）

品类选择 + 选题分析，是所有后续设计的基础。

**交互流程**：
1. 选择目标品类（玄幻/都市/系统文等）
2. 分析目标平台和读者群体
3. 推荐标签组合
4. 输出 `settings/scout_report.yaml`

### /worldbuilding — 世界观设计

**前置依赖**：品类已选择

**交互流程**：
1. 基于品类推荐世界观框架
2. 逐步讨论力量体系、社会结构、基础规则
3. 生成 `settings/worldbuilding.yaml`

### /design-character — 人设设计

**前置依赖**：品类已选择

**交互流程**：
1. 分层设计主角、反派、配角
2. 爽感评估（打脸指数/CP感/反派恶心度）
3. 生成 `settings/characters.yaml`

### /design-outline — 大纲设计

**前置依赖**：品类+世界观

**交互流程**：
1. 交互式设计整体故事走向
2. 节奏检测和张力曲线分析
3. 生成 `settings/outline.yaml` + `settings/arcs.yaml`

### /design-chapters — 细纲设计

**前置依赖**：大纲已完成

**交互流程**：
1. 按大纲拆分章节
2. 每章生成节拍表
3. 检查结构合理性
4. 生成 `settings/chapters_index.yaml`

### /golden-chapters — 黄金三章锻造

**前置依赖**：品类+人设+细纲

**交互流程**：
1. 按品类模板逐章生成前三章
2. 结构验证（首冲突/人设/金手指/小高潮）
3. 生成 `content/chapter_001-003.md`

### /paywall-design — 付费卡点设计

**前置依赖**：大纲+黄金三章

**交互流程**：
1. 分析大纲找最优切割点
2. 设计过渡章节奏（免费末章+付费首章）
3. 生成 `paywall_report.yaml`

### /daily-write — 日更写作

**前置依赖**：章节已规划

**交互流程**：
1. 选择章节，检查衔接
2. 生成正文（2000-3000 字/章）
3. 质量门禁流水线：
   - 事实核查（角色/时间/地点一致性）
   - 去AI味（五层检测，≥ 60 分）
   - 钩子审查（悬念强度/冲突密度，≥ 60 分）
4. 通过所有门禁后定稿

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

日更写作包含 4 层质量检查：

| 门禁 | 检查项 | 通过标准 |
|------|--------|---------|
| 事实核查 | 角色/时间/地点一致性 | 无硬逻辑错误 |
| 去AI味 | 五层综合评分 | ≥ 60 分 |
| 钩子审查 | 悬念强度 | ≥ 60 分 |
| 钩子审查 | 冲突密度 | ≥ 60 分 |

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

### Q: 付费卡点如何设计？

`/paywall-design` 会分析大纲，找到最优切割点（爽点兑现+新悬念），并设计过渡章节奏。

---

## 目录结构

单个项目的完整结构：

```
novels/{project_id}/
├── project.yaml           # 项目元信息
├── settings/              # 设定文件
│   ├── scout_report.yaml  # 选题报告
│   ├── worldbuilding/     # 世界观
│   ├── characters/        # 人物
│   ├── outline/           # 大纲
│   └── chapters/          # 细纲
├── content/               # 正文
│   └── chapters/
├── paywall_report.yaml    # 付费卡点报告
├── drafts/                # 草稿
├── exports/               # 导出文件
└── history/               # 生成历史
```
