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

推荐使用 `/create-novel` skill，它会引导你完成整个流程：

```
/create-novel
→ 检查项目状态
→ 引导完成当前阶段
→ 自动进入下一阶段
```

### 3. 查看进度

```bash
novel show <project_id>
novel stats <project_id>
```

---

## Skills 使用指南

### /create-novel — 创作入口（推荐）

统一的创作流程管理，按阶段引导：

| 阶段 | 设定类型 | 完善度阈值 |
|------|---------|-----------|
| 1 | 世界观 | 80% |
| 2 | 人物 | 70% |
| 3 | 大纲 | 85% |
| 4 | 章节规划 | 100% |
| 5 | 正文写作 | - |

### /nm — 素材检索

需要参考时调用：

```
"查一下修仙类的小说"
→ 查分类 → 检索参考 → 糅合建议
```

### /generate-character — 人物设计

交互式询问：
1. 主角设定（名字、性格、起点、终点）
2. 反派设定（动机、冲突）
3. 配角设定（功能、弧线）
4. 人物关系

### /generate-outline — 大纲规划

交互式询问：
1. 核心设定（一句话概括）
2. 主角弧线
3. 冲突设计
4. 结构规划（幕数、章数）

### /generate-chapter — 章节规划

将大纲转化为章节摘要和张力曲线。

### /write-chapter — 正文写作

1. 确认章节摘要
2. 询问写作方向（可选）
3. 生成正文
4. 选择：接受 / 续写 / 改写

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

### 统计与导出

```bash
# 统计信息
novel stats <project_id> [--detail]

# 导出作品
novel export <project_id> --format txt|md|epub
```

---

## 项目状态

### 项目状态流转

```
planning → drafting → revising → completed
```

| 状态 | 允许操作 |
|------|---------|
| planning | 生成设定、规划章节 |
| drafting | 写正文、续写、改写 |
| revising | 改写、润色 |
| completed | 导出、统计 |

### 章节状态

```
planned → draft → written → revised
```

| 状态 | 说明 |
|------|------|
| planned | 有摘要，无正文 |
| draft | 有正文（< 1500 字）|
| written | 正文完成（≥ 1500 字）|
| revised | 已润色修改 |

---

## 草稿系统

可以通过多种方式提供初始想法：

| 来源 | 使用方式 |
|------|----------|
| `settings/notes.yaml` | 项目内草稿区，自动读取 |
| 直接提供 | `--from-draft "想法..."` |
| 外部文件 | `--from-draft path/to/file.txt` |

---

## 常见问题

### Q: 可以跳过阶段吗？

不可以。每个阶段有完善度检查，未达标不能进入下一阶段。

### Q: 可以修改已完成的设定吗？

可以，但需要重新检查完善度，并可能影响后续阶段。

### Q: 如何参考其他小说？

使用 `/nm` skill 检索素材库，获取同类作品的结构分析。

---

## 目录结构

单个项目的完整结构：

```
novels/{project_id}/
├── project.yaml           # 项目元信息
├── settings/              # 设定文件
│   ├── worldbuilding/     # 世界观
│   ├── characters/        # 人物
│   ├── outline/           # 大纲
│   ├── chapters/          # 章节规划
│   └── notes.yaml         # 草稿
├── content/chapters/      # 正文
├── exports/               # 导出文件
└── history/               # 生成历史
```
